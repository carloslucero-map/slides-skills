#!/usr/bin/env python3
"""
build_shell.py v4 — generate a self-contained WPP Enterprise Solutions | MAP deck shell.

Why this exists
---------------
Two things are painful and error-prone to redo by hand on every deck, and both are
non-negotiable brand rules (see references/WPP-ES-DESIGN-GUIDELINE.md):

  1. The deck must be ONE self-contained .html file — fonts, illustrations and the
     logo all base64/SVG-inlined, never external paths (§2a).
  2. The title / agenda / divider / thank-you slides are LOCKED compositions and
     must be reproduced verbatim (§12.0). Sanctioned per-deck choices (cover art,
     divider colourway, outro, design direction) are spec keys — never hand edits
     to the locked geometry.

Usage
-----
  python build_shell.py --spec spec.json --out deck.html
  python build_shell.py --out demo.html          # built-in demo deck (banner-stamped)

spec.json v2 (title/subtitle/month/presenter/chapters REQUIRED with --spec):
  {
    "title":     "AI NATIVE",              // SHORT, 2-4 words, ALL CAPS
    "subtitle":  "One-sentence subheader",
    "month":     "July 2026",
    "presenter": "Name",                   // "" is legal = no presenter line
    "chapters":  ["Plain title", ...]      // 1-6; or rich form:
    //           [{"title":"…","slides":[{"headline":"…","archetype":"cols-3",
    //                                     "notes":"…","source":"…"}]}]
    "direction":        "editorial-quiet", // | statement-led | data-forward | high-impact
    "dividerColourway": "orange",          // | orange-600 | orange-500 | white | navy-dots | navy-full
    "dividerStyle":     "playbook",        // v4 default | classic (v3 geometry)
    "cover":            "mountain",        // | crystal | coral | dots | playbook
    "outro":            "light",           // | dark
    "motion":           "subtle",          // | full | off (default per direction)
    "confidential":     false,
    "lang":             "en",              // en | es built in
    "strings":          {"agenda":"…","thankyou":"…","section":"…","confidential":"…"},
    "contact":          {"name":"…","role":"…","email":"…"},
    "microDeck":        null,              // auto: true when <=4 content slides or 1 chapter
    "illustrations":    ["rocks"]          // motifs pre-inlined as <template data-asset="…">
  }

A v1 five-key spec builds unchanged and its four locked slides render identically
to v1 output. Page numbers are recomputed at runtime — adding or removing slides
during the fill step never requires manual renumbering.
"""
import argparse, base64, html, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FONTS = os.path.join(SKILL, "assets", "fonts")
LOGOS = os.path.join(SKILL, "assets", "logos")
ILLOS = os.path.join(SKILL, "assets", "illustrations")

FONT_WEIGHTS = [("Thin", 100), ("Light", 300), ("Regular", 400), ("Medium", 500), ("Bold", 700)]

BRAND = "WPP Enterprise Solutions | MAP"

STRINGS = {
    "en": {"agenda": "Agenda", "thankyou": "Thank you.", "section": "Section {n}",
           "confidential": "PRIVATE & CONFIDENTIAL",
           "notes_ph": "Speaker notes for this slide go here."},
    "es": {"agenda": "Agenda", "thankyou": "Gracias.", "section": "Sección {n}",
           "confidential": "PRIVADO Y CONFIDENCIAL",
           "notes_ph": "Notas del presentador para esta diapositiva."},
}

DIRECTIONS = ("editorial-quiet", "statement-led", "data-forward", "high-impact")

# Sanctioned per-deck divider colourways (§11 / §12.3). Geometry NEVER varies —
# only the colour keys a/b/c resolved by the emitted DOTCOLORS map, plus the
# divider background/text role vars. "orange" is byte-for-byte the v1 look.
COLOURWAYS = {
    "orange":     {"bg": "#FAFAF0", "text": "#000050", "sub": "#D94E0E", "navy_section": False,
                   "foot": "#000050", "edge": "#000050",
                   "a": "#FF7800", "b": "#F9BD5D", "c": "#D94E0E"},
    "orange-600": {"bg": "#FAFAF0", "text": "#000050", "sub": "#D94E0E", "navy_section": False,
                   "foot": "#000050", "edge": "#000050",
                   "a": "#F9BD5D", "b": "#FF7800", "c": "#D94E0E"},
    "orange-500": {"bg": "#FAFAF0", "text": "#000050", "sub": "#D94E0E", "navy_section": False,
                   "foot": "#000050", "edge": "#000050",
                   "a": "#FFF5CD", "b": "#F9BD5D", "c": "#FF7800"},
    "white":      {"bg": "#FAFAF0", "text": "#000050", "sub": "#D94E0E", "navy_section": False,
                   "foot": "#000050", "edge": "#000050",
                   "a": "#FFFFFF", "b": "#FFFFFF", "c": "#FFF5CD"},
    # navy-dots: the bottom-right locked dot is navy, so the footer/pageno that
    # sit on it flip to white (the sliver left of the dot is negligible).
    "navy-dots":  {"bg": "#FAFAF0", "text": "#000050", "sub": "#D94E0E", "navy_section": False,
                   "foot": "#FFFFFF", "edge": "#000050",
                   "a": "#000050", "b": "#000050", "c": "#FF7800"},
    # navy-full: cream dot bottom-right -> navy footer on it; edge text on navy bg -> white.
    "navy-full":  {"bg": "#000050", "text": "#FFFFFF", "sub": "#F9BD5D", "navy_section": True,
                   "foot": "#000050", "edge": "#FFFFFF",
                   "a": "#FAFAF0", "b": "#FFFFFF", "c": "#FF7800"},
}
# Default colourway per direction (explicit dividerColourway always wins).
DIRECTION_COLOURWAY = {"editorial-quiet": "orange", "statement-led": "navy-dots",
                       "data-forward": "orange", "high-impact": "navy-full"}

# Motion system (v3.2): a runtime choreography layer over the kit — elements
# move, colours never do (transform/opacity only; flat fills stay flat).
# Auto-off for prefers-reduced-motion, print, and headless capture
# (navigator.webdriver), so the verifier and PDFs always see the static deck.
MOTIONS = ("full", "subtle", "off")
DIRECTION_MOTION = {"editorial-quiet": "subtle", "statement-led": "full",
                    "data-forward": "subtle", "high-impact": "full"}

OUTROS = {
    "light": {"bg": "#FAFAF0", "text": "#000050", "navy_section": False,
              "foot": "#000050", "edge": "#000050",
              "a": "#FF7800", "b": "#F9BD5D", "c": "#D94E0E"},
    # dark: the big bottom-right dot is cream -> footer/pageno on it stay navy;
    # the bottom-left confidential line sits on the navy bg -> white.
    "dark":  {"bg": "#000050", "text": "#FFFFFF", "navy_section": True,
              "foot": "#000050", "edge": "#FFFFFF",
              "a": "#FAFAF0", "b": "#FFFFFF", "c": "#FF7800"},
}

# Registered cover alternates (§12.1a): same locked frame (type block + navy
# badge untouched) — only the art layer swaps.
COVERS = {
    "mountain": {"art": "img-full",  "file": "WPPOpen_Mountain-01.png"},
    "crystal":  {"art": "img-right", "file": "WPPOpen_Crystal-01.png"},
    "coral":    {"art": "img-right", "file": "WPPOpen_Coral-01.png"},
    "dots":     {"art": "css",       "preset": "cover-dots"},
    # v4: the playbook's own cover language (p.1) — pure type on Cream with a
    # sparse Orange 600 mid-dot drift off the top-right. Zero raster payload.
    "playbook": {"art": "css",       "preset": "cover-playbook"},
}

# v4 divider geometry (§12.3): "playbook" = one-hue macro scatter + bottom-pinned
# Thin caps title (the default); "classic" = the v3 right-anchored quartet.
DIVIDER_STYLES = ("playbook", "classic")

# Shipped motif-mechanism art, addressable from spec.illustrations. Paths are
# relative to assets/. Three classes share the one template/clone mechanism:
# halftone illustrations (§9.1a), full-bleed textures (§9.1b), and the
# navy-duotone photo library (§9.2a — already duotone: place via data-motif,
# NEVER wrap these in .duo).
MOTIF_FILES = {
    # halftone illustrations
    "mountain":        "illustrations/WPPOpen_Mountain-01.png",
    "mountain-orange": "illustrations/MAP_Mountain-01_Orange.png",
    "peaks-orange":    "illustrations/MAP_Peaks-01_Orange.png",
    "crystal":         "illustrations/WPPOpen_Crystal-01.png",
    "crystal-orange":  "illustrations/WPPOpen_Crystal-01_Orange.png",
    "coral":           "illustrations/WPPOpen_Coral-01.png",
    "coral-orange":    "illustrations/WPPOpen_Coral-01_Orange.png",
    "rocks":           "illustrations/WPPOpen_Rocks-01.png",
    "rocks-orange":    "illustrations/WPPOpen_Rocks-01_Orange.png",
    "ribbon-orange":   "illustrations/WPPOpen_Ribbon-01_Orange.png",
    "ribbon-navy":     "illustrations/WPPOpen_Ribbon-01_Navy.png",
    # v4 canonical square-grid dot conversions (scripts/halftone.py, §9.1c)
    "dot-lighthouse":  "illustrations/HT_Lighthouse-01.png",
    "dot-dancers-orange": "illustrations/HT_Dancers-01_Orange.png",
    # full-bleed background textures (cream fields — backdrops, not ink)
    "contours":        "textures/contours-cream.png",
    "orbs":            "textures/orbs-cream.png",
    # navy-duotone photo library (internal-WPP-use-only)
    "photo-lighthouse": "photos/photo-lighthouse.png",
    "photo-handoff":    "photos/photo-handoff.webp",
    "photo-confetti":   "photos/photo-confetti.png",
    "photo-chess":      "photos/photo-chess.png",
    "photo-globe":      "photos/photo-globe.png",
    "photo-pencils":    "photos/photo-pencils.png",
    "photo-dancers":    "photos/photo-dancers.png",
    "photo-gears":      "photos/photo-gears.png",
    "photo-fibers":     "photos/photo-fibers.png",
    "photo-team":       "photos/photo-team.webp",
    "photo-diver":      "photos/photo-diver.jpg",
    "photo-fjord":      "photos/photo-fjord.jpg",
    "photo-ridge":      "photos/photo-ridge.jpg",
}

REQUIRED_KEYS = ("title", "subtitle", "month", "presenter", "chapters")
KNOWN_KEYS = set(REQUIRED_KEYS) | {"specVersion", "direction", "dividerColourway", "cover",
                                   "outro", "confidential", "lang", "strings", "contact",
                                   "microDeck", "illustrations", "motion", "dividerStyle"}


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def font_face_css():
    """One @font-face block per weight, base64 data-URI src — fully self-contained."""
    out = []
    for name, weight in FONT_WEIGHTS:
        data = b64(os.path.join(FONTS, f"WPP-{name}.woff2"))
        out.append(
            "@font-face{font-family:'WPP';"
            f"src:url('data:font/woff2;base64,{data}') format('woff2');"
            f"font-weight:{weight};font-display:swap;}}"
        )
    return "\n".join(out)


def read_svg_inline(path):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    i = s.find("<svg")
    return s[i:] if i != -1 else s


MOTIF_MIME = {".png": "image/png", ".webp": "image/webp",
              ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def motif_uri(name):
    rel = MOTIF_FILES[name]
    mime = MOTIF_MIME[os.path.splitext(rel)[1].lower()]
    return f"data:{mime};base64," + b64(os.path.join(SKILL, "assets", rel))


def esc(s):
    return html.escape(str(s), quote=True)


# --- validation ------------------------------------------------------------------

def validate_spec(raw):
    """Validate the RAW parsed spec (pre-merge) so 'missing' and 'defaulted' stay
    distinguishable. Returns (errors, warnings) as lists of strings."""
    errors, warnings = [], []

    for k in REQUIRED_KEYS:
        if k not in raw:
            errors.append(f"spec.{k} is required (presenter may be \"\" for no presenter line)")

    ch = raw.get("chapters")
    if ch is not None:
        if not isinstance(ch, list):
            errors.append("spec.chapters must be a LIST of titles or chapter objects "
                          "(a bare string would explode into per-character sections)")
        else:
            if len(ch) == 0:
                errors.append("spec.chapters must have at least one chapter")
            if len(ch) > 6:
                errors.append(f"{len(ch)} chapters — the locked agenda holds at most 6. "
                              "Split the deck into parts.")
            for n, c in enumerate(ch, 1):
                if isinstance(c, str):
                    title = c
                elif isinstance(c, dict) and isinstance(c.get("title"), str):
                    title = c["title"]
                    slides = c.get("slides", [{}])
                    if not isinstance(slides, list) or not slides:
                        errors.append(f"chapter {n}: slides must be a non-empty list")
                else:
                    errors.append(f"chapter {n}: must be a string title or an object with a "
                                  "\"title\" key")
                    continue
                if len(title) > 45:
                    warnings.append(f"chapter {n} title is {len(title)} chars — agenda rows "
                                    "run under the dot cluster past ~45")

    title = raw.get("title")
    if isinstance(title, str) and len(title.split()) > 4:
        warnings.append(f"cover title is {len(title.split())} words — the locked cover wants "
                        "2-4 ALL-CAPS words")
    presenter = raw.get("presenter")
    if isinstance(presenter, str) and presenter.count(",") >= 2:
        warnings.append("3+ presenter names — prefer a team name")
    if presenter == "Presenter name" or (title == "AI NATIVE" and raw.get("month") == "July 2026"):
        errors.append("spec carries demo placeholder values — replace them with the real "
                      "cover metadata (this is exactly the silent-demo-cover bug)")

    for key, allowed in (("direction", DIRECTIONS), ("dividerColourway", tuple(COLOURWAYS)),
                         ("cover", tuple(COVERS)), ("outro", tuple(OUTROS)),
                         ("motion", MOTIONS), ("dividerStyle", DIVIDER_STYLES)):
        v = raw.get(key)
        if v is not None and v not in allowed:
            errors.append(f"spec.{key} = {v!r} — allowed: {', '.join(allowed)}")

    lang = raw.get("lang")
    if lang is not None and lang not in STRINGS and "strings" not in raw:
        warnings.append(f"lang {lang!r} has no built-in strings (built-in: "
                        f"{', '.join(STRINGS)}) — furniture text falls back to English; "
                        "pass spec.strings to translate it")

    for m in raw.get("illustrations") or []:
        if m not in MOTIF_FILES:
            errors.append(f"spec.illustrations: unknown motif {m!r} — shipped: "
                          f"{', '.join(MOTIF_FILES)}")

    for k in raw:
        if k not in KNOWN_KEYS:
            warnings.append(f"unknown spec key {k!r} ignored (typo?)")

    return errors, warnings


def normalize_chapters(chapters):
    """-> [{"title": str, "slides": [{"headline","archetype","notes","source"}...]}]"""
    out = []
    for c in chapters:
        if isinstance(c, str):
            out.append({"title": c, "slides": [
                {"headline": c, "archetype": "", "notes": "", "source": ""}]})
        else:
            slides = c.get("slides") or [{}]
            norm = []
            for s in slides:
                norm.append({
                    "headline": s.get("headline") or c["title"],
                    "archetype": s.get("archetype", ""),
                    "notes": s.get("notes", ""),
                    "source": s.get("source", ""),
                })
            out.append({"title": c["title"], "slides": norm})
    return out


# --- slide builders ----------------------------------------------------------------

def furniture(spec, extra=""):
    """Footer brand line + pageno (+ confidential line) common to non-cover slides."""
    conf = ""
    if spec["confidential"]:
        conf = f'\n    <div class="confidential">{esc(spec["_strings"]["confidential"])}</div>'
    return (f'{extra}\n    <div class="footer-brand">{BRAND}</div>\n'
            f'    <div class="pageno"></div>{conf}')


def title_slide(spec, white_logo_svg):
    cover = COVERS[spec["cover"]]
    if cover["art"] == "img-full":
        art = (f'    <img class="cover-art cover-art--full" '
               f'src="{motif_uri("mountain")}" alt="">')
    elif cover["art"] == "img-right":
        art = (f'    <img class="cover-art cover-art--right" '
               f'src="data:image/png;base64,{b64(os.path.join(ILLOS, cover["file"]))}" alt="">')
    else:
        art = (f'    <div class="cover-dots" data-dots="{cover["preset"]}" '
               'aria-hidden="true"></div>')
    presenter = (f'\n        <span class="presenter">{esc(spec["presenter"])}</span>'
                 if spec["presenter"] else "")
    return f"""
  <!-- ===== LOCKED TITLE SLIDE — registered cover art: {spec['cover']} (§12.1a).
       Type block and navy badge never change; only the art layer is a sanctioned swap. ===== -->
  <section class="slide cover-mountain" data-slide-id="cover">
{art}
    <div class="cover-mountain__head">
      <h1 class="cover-mountain__title">{esc(spec['title'])}</h1>
      <p class="cover-mountain__sub">{esc(spec['subtitle'])}</p>
      <p class="cover-mountain__meta">
        <span class="month">{esc(spec['month'])}</span>{presenter}
      </p>
    </div>
    <div class="cover-mountain__badge">{white_logo_svg}</div>
  </section>"""


def agenda_slide(spec, chapters):
    dense = len(chapters) == 6
    top0, step = (224, 128) if dense else (266, 148)
    rows = []
    for i, ch in enumerate(chapters):
        rows.append(
            f'      <div class="toc-row" style="top:{top0 + i * step}px;">'
            f'<span class="n">{i + 1}.</span><span class="t">{esc(ch["title"])}</span></div>'
        )
    rows = "\n".join(rows)
    cls = "slide agenda agenda--dense" if dense else "slide agenda"
    return f"""
  <!-- ===== LOCKED AGENDA — numbered vertical list, Orange dot cluster ===== -->
  <section class="{cls}" data-slide-id="agenda">
    <h2 class="headline">{esc(spec['_strings']['agenda'])}</h2>
    <div class="toc-dots" data-dots="agenda" aria-hidden="true"></div>
{rows}{furniture(spec)}
  </section>"""


def divider_slide(spec, num, title):
    navy = " slide--navy" if COLOURWAYS[spec["dividerColourway"]]["navy_section"] else ""
    sub = spec["_strings"]["section"].format(n=num)
    if spec["dividerStyle"] == "classic":
        return f"""
  <!-- ===== LOCKED DIVIDER (classic v3 geometry) — identical on every section ===== -->
  <section class="slide divider{navy}" data-slide-id="divider-{num}">
    <div class="dv-dots" data-dots="divider" aria-hidden="true"></div>
    <div class="dv-num">{num:02d}.</div>
    <div class="dv-sub">{esc(sub)}</div>
    <h2 class="dv-title">{esc(title)}</h2>{furniture(spec)}
  </section>"""
    return f"""
  <!-- ===== LOCKED DIVIDER (v4 playbook composition, §12.3) — identical on every
       section; one-hue macro scatter, title pinned bottom-left ===== -->
  <section class="slide divider{navy}" data-slide-id="divider-{num}">
    <div class="dv-dots" data-dots="divider-playbook" aria-hidden="true"></div>
    <div class="dv-num">{num:02d}.</div>
    <div class="dv-block">
      <div class="dv-sub">{esc(sub)}</div>
      <h2 class="dv-title">{esc(title)}</h2>
    </div>{furniture(spec)}
  </section>"""


def content_placeholder(spec, slide, chap_n, slide_n):
    arch = slide["archetype"]
    arch_attr = f' data-archetype="{esc(arch)}"' if arch else ""
    hint = (f"Suggested archetype: {arch} — see assets/snippets/ for the matching block."
            if arch else "Pick the archetype that fits (guideline §12.4-§12.13), then "
            "assemble it from assets/snippets/ — don't re-derive layouts.")
    source = (f'\n    <div class="source">{esc(slide["source"])}</div>'
              if slide["source"] else "")
    notes = esc(slide["notes"]) if slide["notes"] else esc(spec["_strings"]["notes_ph"])
    return f"""
  <!-- ===== CONTENT SLIDE — REPLACE the .content-band with a real archetype.
       {hint}
       Keep the .slide wrapper, headline, footer furniture and the empty .pageno
       (page numbers are computed at runtime — never hand-number).
       Cream background is inherited. Add class "slide--navy" for a deliberate dark
       moment (max ~1 in 6) or "slide--tint" for an Orange 500 accent moment. ===== -->
  <section class="slide" data-slide-id="c{chap_n}-s{slide_n}"{arch_attr}>
    <h2 class="headline">{esc(slide['headline'])}</h2>
    <div class="content-band">
      <p class="body">Placeholder — replace with the {esc(arch) if arch else 'chosen'} archetype
      from assets/snippets/. Body copy stays Navy on Cream.</p>
    </div>{source}{furniture(spec)}
    <aside class="notes" hidden>{notes}</aside>
  </section>"""


def thankyou_slide(spec):
    navy = " slide--navy" if OUTROS[spec["outro"]]["navy_section"] else ""
    contact = ""
    c = spec.get("contact")
    if c:
        lines = "".join(f"<span>{esc(v)}</span>" for v in
                        (c.get("name"), c.get("role"), c.get("email")) if v)
        contact = f'\n    <div class="ty-contact">{lines}</div>'
    return f"""
  <!-- ===== LOCKED THANK-YOU — mandatory final slide (outro: {spec['outro']}) ===== -->
  <section class="slide thank-you{navy}" data-slide-id="thankyou">
    <div class="ty-dots" data-dots="thankyou" aria-hidden="true"></div>
    <div class="ty">{esc(spec['_strings']['thankyou'])}</div>{contact}{furniture(spec)}
  </section>"""


# --- CSS ---------------------------------------------------------------------------

# Kit v3.3 — icon suite, sparkle accents, duotone photography (mined from the
# real MAP deck). Icons/sparks are inline SVG normalized to currentColor
# (assets/icons/*.svg — paste at fill time, CSS recolours). .duo is the ONE
# sanctioned photo treatment outside .screenshot: navy shadows / cream
# highlights via grayscale+screen+multiply — works on ANY user image at
# runtime, no preprocessing, flat by construction.
KIT_V33_CSS = """
/* --- Kit v3.3: icons, sparkles, duotone photography --- */
.icon{width:44px;height:44px;color:var(--wpp-navy);margin-bottom:18px;}
.icon svg{width:100%;height:100%;display:block;}
.icon--orange{color:var(--orange-700);}
.icon--lg{width:64px;height:64px;}
.slide--navy .icon,.panel--nav .icon{color:var(--wpp-cream);}
.spark{position:absolute;width:34px;height:34px;color:var(--orange-700);z-index:1;}
.spark svg{width:100%;height:100%;display:block;}
.spark--navy{color:var(--wpp-navy);}
.spark--lg{width:56px;height:56px;}
.duo{position:absolute;overflow:hidden;background:var(--wpp-navy);isolation:isolate;}
.duo img{width:100%;height:100%;object-fit:cover;display:block;
  filter:grayscale(1) contrast(1.08) brightness(1.04);mix-blend-mode:screen;
  print-color-adjust:exact;-webkit-print-color-adjust:exact;}
"""


# Motion system v3.2 — choreography classes the runtime assigns (zero markup).
# Doctrine (guideline §14): elements move, colours never do — flat fills stay
# flat. Keyframes animate the INDIVIDUAL `translate`/`scale` properties, never
# the `transform` shorthand: several kit elements are POSITIONED with base
# transforms (.big-statement/.motif/.compare-art translateY(-50%) centring,
# .tl-label translateX(-50%)) and shorthand keyframes would clobber them
# mid-flight and snap ("teleport") on release. Individual properties compose
# with the base transform — and with the pointer-parallax, which owns
# `transform` exclusively. The global prefers-reduced-motion block above
# kills all of this wholesale.
MOTION_CSS = """
/* --- Motion v3.2 (scoped by body[data-motion]) --- */
body:not([data-motion=off]) .slide.is-active{animation:m-slide .38s ease-out both;}
body[data-motion=off] .m-in{animation:none!important;}
.m-in{--mi:0;animation-duration:.62s;animation-timing-function:cubic-bezier(.2,.75,.15,1);
  animation-fill-mode:backwards;animation-delay:calc(90ms + var(--mi)*75ms);}
.m-rise{animation-name:m-rise;}
.m-fade{animation-name:m-fade;animation-duration:.5s;}
.m-wipe{animation-name:m-wipe;animation-duration:.72s;}
.m-pop{animation-name:m-pop;animation-timing-function:cubic-bezier(.34,1.56,.4,1);
  animation-fill-mode:both;}
.m-grow{animation-name:m-grow;transform-origin:top center;animation-fill-mode:both;}
.m-draw{animation-name:m-draw;transform-origin:left center;animation-duration:.95s;
  animation-fill-mode:both;}
.m-float-in{animation-name:m-float-in;animation-duration:.9s;}
.m-drift{animation-name:m-drift;animation-duration:1.05s;}
@keyframes m-slide{from{opacity:0;}to{opacity:1;}}
@keyframes m-rise{from{opacity:0;translate:0 34px;}to{opacity:1;translate:0 0;}}
@keyframes m-fade{from{opacity:0;}to{opacity:1;}}
@keyframes m-wipe{from{opacity:0;translate:70px 0;}to{opacity:1;translate:0 0;}}
@keyframes m-pop{from{opacity:0;scale:.25;}to{opacity:1;scale:1;}}
@keyframes m-grow{from{scale:1 0;}to{scale:1 1;}}
@keyframes m-draw{from{scale:0 1;}to{scale:1 1;}}
@keyframes m-float-in{from{opacity:0;translate:0 48px;}to{opacity:1;translate:0 0;}}
@keyframes m-drift{from{opacity:0;translate:80px 0;}to{opacity:1;translate:0 0;}}
/* Ambient life (full only): dots breathe after their pop; motif art floats. */
.m-live .dot.m-in{animation-name:m-pop,m-breathe;
  animation-duration:.62s,7.5s;
  animation-timing-function:cubic-bezier(.34,1.56,.4,1),ease-in-out;
  animation-delay:calc(90ms + var(--mi)*75ms),calc(1.4s + var(--mi)*.43s);
  animation-iteration-count:1,infinite;animation-direction:normal,alternate;
  animation-fill-mode:both,none;}
.m-live .motif img,.m-live .compare-art img{animation:m-float 9s ease-in-out 1.2s infinite alternate;}
@keyframes m-breathe{from{scale:1;}to{scale:1.055;}}
@keyframes m-float{from{translate:0 0;}to{translate:0 -14px;}}
/* Alive layer v2: deck progress hairline · kinetic word-stagger · fragments
   · ambient Ken Burns on duotones · sparkle twinkle. */
#prog{position:fixed;left:0;bottom:0;height:3px;width:0;background:var(--orange-700);
  z-index:55;transition:width .5s cubic-bezier(.2,.75,.15,1);}
body[data-motion=off] #prog{display:none;}
.mw{display:inline-block;}
body:not([data-motion=off]) .frag-off{opacity:0;translate:0 18px;}
body:not([data-motion=off]) [data-build]{transition:opacity .5s ease,
  translate .5s cubic-bezier(.2,.75,.15,1);}
.m-live .duo img{animation:m-kenburns 16s ease-in-out infinite alternate;}
.m-live .spark.m-in{animation-name:m-pop,m-twinkle;
  animation-duration:.62s,3.4s;
  animation-timing-function:cubic-bezier(.34,1.56,.4,1),ease-in-out;
  animation-delay:calc(90ms + var(--mi)*75ms),calc(1.1s + var(--mi)*.7s);
  animation-iteration-count:1,infinite;animation-direction:normal,alternate;
  animation-fill-mode:both,none;}
@keyframes m-kenburns{from{scale:1;translate:0 0;}to{scale:1.07;translate:-14px -8px;}}
@keyframes m-twinkle{from{rotate:-10deg;scale:.94;}to{rotate:10deg;scale:1.06;}}
/* Hover life — the deck answers the mouse like a web page. Movement only,
   never colour (§14); real pointers only; off = off.
   Hover offsets live on `transform`, NEVER on `translate`: the entrance
   keyframes animate `translate`, and a hover transition contesting the same
   property completes invisibly under the running animation, then snaps
   ("teleports") the moment the animation releases the property (§15.7).
   None of these hover targets carries a base transform, so transform is free. */
@media (hover:hover){
  body:not([data-motion=off]) .tbx,
  body:not([data-motion=off]) .proc>div,
  body:not([data-motion=off]) .cols>div,
  body:not([data-motion=off]) .kpi,
  body:not([data-motion=off]) .milestone,
  body:not([data-motion=off]) .hero-row>div,
  body:not([data-motion=off]) .compare-left,
  body:not([data-motion=off]) .compare-right,
  body:not([data-motion=off]) .toc-row{transition:transform .28s cubic-bezier(.2,.75,.15,1);}
  body:not([data-motion=off]) .tbx:hover,
  body:not([data-motion=off]) .proc>div:hover{transform:translateY(-8px);}
  body:not([data-motion=off]) .cols>div:hover,
  body:not([data-motion=off]) .kpi:hover,
  body:not([data-motion=off]) .milestone:hover,
  body:not([data-motion=off]) .hero-row>div:hover,
  body:not([data-motion=off]) .compare-left:hover,
  body:not([data-motion=off]) .compare-right:hover{transform:translateY(-6px);}
  body:not([data-motion=off]) .toc-row:hover{transform:translateX(14px);}
  body:not([data-motion=off]) .stat-circle{transition:scale .3s cubic-bezier(.34,1.56,.4,1);}
  body:not([data-motion=off]) .stat-circle:hover{scale:1.05;}
  body:not([data-motion=off]) .hero-num{display:inline-block;transform-origin:left bottom;
    transition:scale .3s cubic-bezier(.34,1.56,.4,1);}
  body:not([data-motion=off]) .hero-num:hover{scale:1.06;}
  body:not([data-motion=off]) .takeaway::before,
  body:not([data-motion=off]) .takeaway::after{transition:width .3s ease;}
  body:not([data-motion=off]) .takeaway:hover::before,
  body:not([data-motion=off]) .takeaway:hover::after{width:44px;}
}
/* Pointer parallax (full only) — art layers only, text never moves. */
body[data-motion=full] .lift,body[data-motion=full] .cover-dots,
body[data-motion=full] .toc-dots,body[data-motion=full] .dv-dots,
body[data-motion=full] .ty-dots{
  transform:translate(calc(var(--parx,0)*14px),calc(var(--pary,0)*10px));
  transition:transform .7s cubic-bezier(.2,.75,.15,1);}
body[data-motion=full] .motif{
  transform:translate(calc(var(--parx,0)*24px),calc(var(--pary,0)*16px));
  transition:transform .7s cubic-bezier(.2,.75,.15,1);}
/* Variants whose base transform centres them must keep that offset in the
   parallax calc, or the parallax rule statically drops them (doctrine bug). */
body[data-motion=full] .motif--right{
  transform:translate(calc(var(--parx,0)*24px),calc(-50% + var(--pary,0)*16px));}
body[data-motion=full] .motif--backdrop{
  transform:translate(calc(-50% + var(--parx,0)*24px),calc(-50% + var(--pary,0)*16px));}
body[data-motion=full] .num-ghost{
  transform:translate(calc(var(--parx,0)*34px),calc(var(--pary,0)*22px));
  transition:transform .7s cubic-bezier(.2,.75,.15,1);}
@media print{.m-in,.slide.is-active{animation:none!important;opacity:1!important;transform:none!important;}
  #prog{display:none!important;}
  .frag-off{opacity:1!important;translate:0 0!important;}}
"""


def base_css(spec):
    cw = COLOURWAYS[spec["dividerColourway"]]
    ot = OUTROS[spec["outro"]]
    return f"""
:root{{
  --wpp-navy:#000050; --wpp-cream:#FAFAF0; --wpp-white:#FFFFFF;
  --orange-900:#6A290A; --orange-800:#D94E0E; --orange-700:#FF7800;
  --orange-600:#F9BD5D; --orange-500:#FFF5CD;
  --bg:var(--wpp-cream); --bg-alt:var(--wpp-white); --bg-tint:var(--orange-500);
  --bg-dark:var(--wpp-navy); --text:var(--wpp-navy); --text-inv:var(--wpp-white);
  --accent:var(--orange-700);
  /* v4 semantic data colours (§3.8): favourable numbers glow, unfavourable stay ink */
  --data-pos:var(--orange-700); --data-neg:var(--wpp-navy);
  /* v4 layout tokens (§2): 40px module, 80px content edge — deviating from these
     is what the §15.9 content-edge probe flags */
  --grid:40px; --m-edge:40px; --m-text:56px; --band-top:305px; --band-bottom:60px;
  /* Per-deck sanctioned choices (spec keys) — defaults are the v1 look */
  --dv-bg:{cw['bg']}; --dv-text:{cw['text']}; --dv-sub:{cw['sub']};
  --dv-foot:{cw['foot']}; --dv-edge:{cw['edge']};
  --ty-bg:{ot['bg']}; --ty-text:{ot['text']};
  --ty-foot:{ot['foot']}; --ty-edge:{ot['edge']};
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{height:100%;background:#0a0a1a;}}
#stage{{position:fixed;inset:0;overflow:hidden;background:#0a0a1a;}}
#frame{{position:absolute;top:0;left:0;width:1920px;height:1080px;transform-origin:top left;}}

/* Base slide — Cream is the one consistent content background (§3.3a) */
.slide{{
  position:absolute;top:0;left:0;width:1920px;height:1080px;overflow:hidden;
  background:var(--bg);color:var(--text);
  font-family:'WPP','Poppins','Century Gothic',system-ui,sans-serif;
  font-weight:300;font-feature-settings:"salt" 1;display:none;
}}
body:not(.js) #frame .slide:first-of-type{{display:block;}}
body.js .slide.is-active{{display:block;}}
.slide--navy{{background:var(--bg-dark);color:var(--text-inv);}}
.slide--tint{{background:var(--bg-tint);}}
.slide--white{{background:var(--bg-alt);}}   /* rare only — see §3.3a */

/* GROUND BAND — a partial-height ground change, measured off the source deck
   rather than invented. Slide 86 turns White from y=580 on an otherwise Cream
   slide and runs its numeral row ACROSS that boundary; the crossing is what
   makes the composition read as one object instead of two stacked rows.
   .slide--white could not express this: it repaints the whole slide.
   --ground-y is the split (default 580px, the measured value). Content sits
   above the band because the band is a ::before at z-index 0.
   Not a licence to invent grounds: §3.3a still governs which two may meet. */
.slide--ground{{--ground-y:580px;}}
.slide--ground::before{{content:"";position:absolute;left:0;right:0;top:var(--ground-y);bottom:0;background:var(--bg-alt);z-index:0;}}
.slide--ground > *{{position:relative;z-index:1;}}

/* Standard content furniture (§7). v4 typography contract (§4.2): headlines
   Light 300, running text Regular 400 — weight, not just size, carries the
   hierarchy. Footer furniture is Regular per the playbook ("footers"). */
.slide > .headline{{position:absolute;left:var(--m-edge);top:73px;font-weight:300;font-size:54px;line-height:.9;letter-spacing:-.005em;max-width:calc(1920px - 2*var(--m-edge));}}
.headline--caps{{font-size:48px;line-height:.94;letter-spacing:.01em;text-transform:uppercase;}} /* Light-caps "strong emphasis" title (§4.3); ≤1 in 4 content slides */
.hl{{font-weight:500;}} /* v4 title highlight (§4.4): ONE key token per title, weight only */
.slide > .subtitle{{position:absolute;left:var(--m-edge);top:177px;font-weight:500;font-size:24px;letter-spacing:.12em;text-transform:uppercase;color:var(--orange-800);}}
.slide > .content-band{{position:absolute;left:var(--m-edge);top:var(--band-top);right:var(--m-edge);bottom:var(--band-bottom);}}
.subhead{{font-weight:400;font-size:24px;line-height:1.15;letter-spacing:.08em;text-transform:uppercase;margin-bottom:20px;max-width:1200px;}} /* v4 Regular-caps sub-headline tier (§4.3): supports the headline / leads the body */
.body{{font-weight:400;font-size:26px;line-height:1.32;max-width:1200px;}}
.stat--pos{{color:var(--data-pos);}} /* §3.8/§10.1 — favourable direction; ≥300 weight below 90px */
.stat--neg{{color:var(--data-neg);}} /* §3.8/§10.1 — unfavourable direction, declared in markup */
.footer-brand{{position:absolute;right:var(--m-edge);bottom:34px;font-weight:700;font-size:16px;letter-spacing:.01em;color:var(--text);}}
.slide--navy .footer-brand{{color:var(--text-inv);}}
.pageno{{position:absolute;right:var(--m-edge);bottom:14px;font-weight:400;font-size:11px;opacity:.7;letter-spacing:.08em;text-transform:uppercase;}}
.slide--navy .pageno{{color:var(--text-inv);}}
.confidential{{position:absolute;left:var(--m-edge);bottom:14px;font-weight:400;font-size:11px;opacity:.7;letter-spacing:.08em;text-transform:uppercase;}}
.source{{position:absolute;left:var(--m-edge);bottom:60px;font-weight:400;font-size:12px;opacity:.75;}}
.dot{{position:absolute;border-radius:50%;}}

/* ---- LOCKED TITLE SLIDE (art layer swaps by registered cover; frame never changes) ---- */
.slide.cover-mountain{{background:#FAFAF0;color:#000050;}}
.cover-art{{z-index:0;pointer-events:none;}}
.cover-art--full{{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover;object-position:center;}}
.cover-art--right{{position:absolute;right:-140px;top:50%;transform:translateY(-50%);width:1440px;height:auto;}}
.cover-dots{{position:absolute;inset:0;overflow:hidden;z-index:0;pointer-events:none;}}
.cover-mountain__head{{position:absolute;left:var(--m-edge);top:88px;z-index:2;max-width:1040px;}}
.cover-mountain__title{{font-weight:300;font-size:81px;line-height:.9;letter-spacing:0;text-transform:uppercase;color:#000050;}}
.cover-mountain__sub{{margin:26px 0 0;font-weight:300;font-size:31px;line-height:1.16;color:#000050;max-width:900px;}}
.cover-mountain__meta{{margin:34px 0 0;font-weight:400;font-size:24px;line-height:1.3;color:#000050;}}
.cover-mountain__meta .month{{display:block;text-transform:uppercase;letter-spacing:-.01em;color:#FF7800;}}
.cover-mountain__meta .presenter{{display:block;}}
.cover-mountain__badge{{position:absolute;right:0;bottom:0;z-index:2;background:#000050;padding:46px 80px 60px 64px;display:flex;align-items:center;}}
.cover-mountain__badge svg{{display:block;width:300px;height:auto;}}

/* ---- LOCKED AGENDA ---- */
.slide.agenda .headline{{position:absolute;top:112px;left:var(--m-edge);font-weight:300;font-size:54px;line-height:1.02;letter-spacing:-.005em;}}
.slide.agenda .toc-dots{{position:absolute;right:0;top:0;width:520px;height:520px;overflow:visible;}}
.slide.agenda .toc-row{{position:absolute;left:var(--m-edge);display:flex;align-items:baseline;gap:44px;}}
.slide.agenda .toc-row .n{{font-weight:100;font-size:88px;line-height:1;color:#FF7800;width:118px;letter-spacing:-.02em;}}
.slide.agenda .toc-row .t{{font-weight:300;font-size:50px;line-height:1;color:#000050;}}
.slide.agenda--dense .toc-row .n{{font-size:72px;width:98px;}}
.slide.agenda--dense .toc-row .t{{font-size:42px;}}

/* ---- LOCKED DIVIDER (colourway via role vars; geometry immutable) ----
   v4 default = the playbook composition (§12.3): one-hue macro scatter +
   bottom-pinned Thin caps title (sub-label stacked above it in .dv-block).
   dividerStyle:"classic" keeps the v3 geometry (absolute dv-sub/dv-title). */
.slide.divider{{background:var(--dv-bg);color:var(--dv-text);}}
.slide.divider .dv-dots{{position:absolute;inset:0;overflow:hidden;}}
.slide.divider .dv-num{{position:absolute;top:56px;left:var(--m-edge);font-weight:100;font-size:104px;line-height:1;letter-spacing:-.02em;}}
.slide.divider .dv-sub{{position:absolute;left:84px;bottom:150px;font-weight:500;font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:var(--dv-sub);}}
.slide.divider .dv-title{{position:absolute;left:var(--m-edge);bottom:214px;font-weight:100;font-size:104px;line-height:.86;letter-spacing:-.02em;text-transform:uppercase;max-width:1180px;text-wrap:balance;}}
.slide.divider .dv-block{{position:absolute;left:var(--m-edge);bottom:96px;max-width:1560px;z-index:1;}}
.slide.divider .dv-block .dv-sub{{position:static;display:block;margin-bottom:26px;}}
.slide.divider .dv-block .dv-title{{position:static;font-size:136px;line-height:.88;max-width:1560px;}}
.slide.divider .footer-brand,.slide.divider .pageno{{color:var(--dv-foot);}}
.slide.divider .confidential{{color:var(--dv-edge);}}

/* ---- LOCKED THANK-YOU (outro via role vars) ---- */
.slide.thank-you{{background:var(--ty-bg);}}
.slide.thank-you .ty-dots{{position:absolute;inset:0;overflow:hidden;}}
.slide.thank-you .ty{{position:absolute;left:var(--m-edge);top:430px;font-weight:300;font-size:99px;line-height:.9;color:var(--ty-text);}}
.slide.thank-you .ty-contact{{position:absolute;left:var(--m-edge);top:580px;font-weight:400;font-size:24px;line-height:1.5;color:var(--ty-text);}}
.slide.thank-you .ty-contact span{{display:block;}}
.slide.thank-you .footer-brand,.slide.thank-you .pageno{{color:var(--ty-foot);}}
.slide.thank-you .confidential{{color:var(--ty-edge);}}

/* ===== ARCHETYPE KIT (§12.4-§12.13) — assemble content slides from assets/snippets/ ===== */
.lift{{position:absolute;inset:0;overflow:hidden;pointer-events:none;}}
.cols{{position:absolute;left:var(--m-edge);top:260px;right:80px;display:grid;gap:80px;align-items:start;}}
.cols-2{{grid-template-columns:repeat(2,1fr);}}
.cols-3{{grid-template-columns:repeat(3,1fr);}}
.cols-4{{grid-template-columns:repeat(4,1fr);gap:56px;}}
.cols .body{{font-size:24px;}}
.cols-4 .body{{font-size:22px;}}
.col-sub{{font-weight:500;font-size:24px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px;}}
.col-dot{{width:16px;height:16px;border-radius:50%;background:var(--wpp-navy);margin-bottom:22px;}}
.pill{{display:inline-block;background:var(--wpp-navy);color:var(--wpp-white);border-radius:999px;padding:10px 26px;font-weight:500;font-size:15px;letter-spacing:.08em;text-transform:uppercase;}}
.slide--navy .pill{{background:var(--wpp-cream);color:var(--wpp-navy);}}
.tbx-row{{position:absolute;left:var(--m-edge);right:80px;top:280px;display:flex;align-items:stretch;gap:28px;}}
.tbx{{background:var(--wpp-white);padding:32px 36px;flex:1;font-weight:400;font-size:22px;line-height:1.3;}}
.tbx .col-sub{{font-size:20px;}}
.sep-dot{{align-self:center;flex:0 0 16px;width:16px;height:16px;border-radius:50%;background:var(--wpp-navy);}}
.sep-arrow{{align-self:center;flex:0 0 22px;width:0;height:0;border-top:15px solid transparent;border-bottom:15px solid transparent;border-left:22px solid var(--wpp-navy);}}
.big-statement{{position:absolute;left:var(--m-edge);top:50%;transform:translateY(-50%);font-weight:100;font-size:150px;line-height:.82;letter-spacing:-.02em;max-width:1640px;}}
.big-quote{{position:absolute;left:120px;top:170px;max-width:1620px;font-weight:100;font-size:120px;line-height:1.04;letter-spacing:-.01em;}}
.quote-attr{{position:absolute;left:120px;bottom:190px;font-weight:500;font-size:30px;letter-spacing:.1em;text-transform:uppercase;}}
.compare-art{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:964px;pointer-events:none;}}
.compare-art img{{width:100%;height:auto;display:block;}}  /* §15.2 — an unconstrained clone renders at native size and paints over the headline */
/* §15.2 — the 964px centrepiece spans x478-1442; 370px text zones keep ≥24px
   clearance from the art's hard crop edges on both sides. */
.compare-left{{position:absolute;left:var(--m-edge);top:420px;width:370px;font-weight:400;font-size:24px;line-height:1.35;}}
.compare-right{{position:absolute;right:80px;top:420px;width:370px;font-weight:400;font-size:24px;line-height:1.35;}}
.stat-circle{{display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:50%;background:var(--wpp-navy);color:var(--wpp-white);text-align:center;}}
.stat-circle .v{{font-weight:100;font-size:90px;line-height:1;}}
.stat-circle .l{{font-weight:500;font-size:18px;letter-spacing:.1em;text-transform:uppercase;margin-top:10px;max-width:80%;}}
.stat-circle--orange{{background:var(--orange-700);color:var(--wpp-navy);}}
.bubble-row{{position:absolute;left:var(--m-edge);right:80px;top:260px;bottom:140px;display:flex;align-items:center;justify-content:space-evenly;}}
.kpi-row{{position:absolute;left:var(--m-edge);right:80px;top:340px;display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:80px;}}
.kpi .v{{font-weight:100;font-size:110px;line-height:1;}}
.kpi .l{{font-weight:500;font-size:18px;letter-spacing:.1em;text-transform:uppercase;margin-top:12px;}}
.orbit{{position:absolute;border-radius:50%;border:1px dotted var(--wpp-navy);}}
.proc{{position:absolute;left:var(--m-edge);right:80px;top:300px;display:grid;grid-template-columns:repeat(5,1fr);gap:40px;}}
.proc .n{{font-weight:100;font-size:64px;line-height:1;color:var(--orange-800);}}  /* orange-800: thin numerals need ≥3:1 on white/cream (§15.5) */
.proc .step-l{{font-weight:500;font-size:15px;letter-spacing:.1em;text-transform:uppercase;margin:16px 0 12px;}}
.proc .body{{font-size:20px;}}
.timeline{{position:absolute;left:var(--m-edge);right:80px;top:540px;height:1px;background:var(--wpp-navy);}}
.tl-node{{position:absolute;top:-8px;width:16px;height:16px;border-radius:50%;background:var(--wpp-navy);}}
.tl-node--accent{{background:var(--orange-700);}}
.tl-label{{position:absolute;top:28px;transform:translateX(-50%);font-weight:500;font-size:16px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;}}
.team-grid{{position:absolute;left:var(--m-edge);right:80px;top:280px;display:grid;grid-template-columns:repeat(4,1fr);gap:64px;}}
.team-grid--3{{grid-template-columns:repeat(3,1fr);}}
.person .ph{{width:180px;height:180px;border-radius:50%;background:var(--wpp-navy);overflow:hidden;}}
.person .ph img{{width:100%;height:100%;object-fit:cover;}}
/* No-photo default: WPP Thin initials monogram (never a grey placeholder). */
.person .ph-init{{display:flex;align-items:center;justify-content:center;width:100%;height:100%;
  font-weight:100;font-size:64px;color:var(--wpp-cream);letter-spacing:.05em;}}
.team-grid--wide .ph-init{{font-size:92px;}}
.person .nm{{font-weight:500;font-size:24px;margin-top:20px;}}
.person .rl{{font-weight:400;font-size:20px;margin-top:4px;}}
.person .bio{{font-weight:400;font-size:16px;line-height:1.35;margin-top:12px;}}
.img-right-text{{position:absolute;left:var(--m-edge);top:260px;width:640px;}}
/* v4 §15.9: media anchors to edges — .img-right-media now bleeds to the right
   canvas edge (x880-1920); the margin opens for the image, the inner edge holds
   the grid. Floating mid-canvas media rectangles are a verifier FAIL. */
.img-right-media{{position:absolute;right:0;top:240px;bottom:140px;width:1040px;overflow:hidden;}}
.img-right-media img{{width:100%;height:100%;object-fit:cover;}}
.img-half-media{{position:absolute;right:0;top:0;bottom:0;width:960px;}}
.img-half-media img{{width:100%;height:100%;object-fit:cover;}}
/* v4 media anchoring utilities (§12.9/§15.9): every media block bleeds or corners. */
.media{{position:absolute;overflow:hidden;z-index:0;}}
.media img{{width:100%;height:100%;object-fit:cover;display:block;}}
.media--bleed-r{{left:880px;right:0;top:240px;bottom:140px;}}
.media--bleed-l{{left:0;right:1040px;top:240px;bottom:140px;}}
.media--bleed-b{{left:var(--m-edge);right:80px;top:560px;bottom:0;}}
.media--bleed-t{{left:var(--m-edge);right:80px;top:0;bottom:640px;}}
.media--corner-br{{right:0;bottom:0;width:840px;height:560px;}}
.media--corner-tr{{right:0;top:0;width:840px;height:520px;}}
.screenshot{{display:block;max-width:100%;outline:1px solid var(--wpp-navy);}}
.datatable{{border-collapse:collapse;font-weight:400;font-size:22px;}}
.datatable th{{font-weight:500;font-size:16px;letter-spacing:.1em;text-transform:uppercase;text-align:left;padding:0 48px 14px 0;border-bottom:1px solid var(--wpp-navy);}}
.datatable td{{padding:14px 48px 14px 0;border-bottom:1px solid var(--wpp-navy);}}
/* House expandable card (§13.4): flat at rest, Orange 600 outline on hover,
   CTA flips Navy->Orange 700 and the arrow nudges 4px right. */
.card{{background:var(--wpp-white);padding:36px;cursor:pointer;}}
.card:hover{{outline:2px solid var(--orange-600);}}
.card:focus-visible{{outline:2px solid var(--wpp-navy);}}
.card-cta{{display:inline-block;margin-top:22px;font-weight:500;font-size:18px;color:var(--wpp-navy);}}
.card-cta .arrow{{display:inline-block;transition:transform .15s ease;}}
.card:hover .card-cta{{color:var(--orange-700);}}
.card:hover .card-cta .arrow{{transform:translateX(4px);}}
.card-detail{{display:none;margin-top:18px;}}
.card.is-open .card-detail{{display:block;}}


/* ===== KIT v3 — COMPOSITION SYSTEM (guideline §12.15) — append-only ===== */
/* Panels / splits (R1, R13). Headline caps: right panel >=768px -> headline max-width 1040px inline. */
.panel{{position:absolute;top:0;bottom:0;right:0;z-index:0;}}
.panel--left{{left:0;right:auto;}}
.panel--w440{{width:440px;}}
.panel--w768{{width:768px;}}
.panel--w960{{width:960px;}}
.panel--nav{{background:var(--wpp-navy);color:var(--text-inv);}}
.panel--tint{{background:var(--bg-tint);}}
.panel--white{{background:var(--bg-alt);}}
.panel--orange{{background:var(--orange-700);color:var(--wpp-navy);}} /* high-impact direction only */
.panel-inner{{position:absolute;inset:64px 56px;display:flex;flex-direction:column;gap:36px;}}
.panel--nav:not(.panel--left)~.footer-brand,.panel--nav:not(.panel--left)~.pageno{{color:var(--wpp-white);}}
/* Hero numerals (R3) */
.hero-num{{font-weight:100;font-size:240px;line-height:.8;letter-spacing:-.02em;}}
.hero-num--s{{font-size:144px;}}
.hero-num--l{{font-size:280px;}}
.hero-num--xl{{font-size:320px;}}
.hero-num--m{{font-size:192px;}}      /* MEASURED: bank slide 86 numeral, 96pt x 2 */
.hero-num--solid{{font-weight:400;}}  /* the bank sets numerals in Regular, not Thin —
                                         .hero-num's weight 100 is a kit invention */
.hero-num--orange{{color:var(--orange-700);}}
.hero-row{{position:absolute;left:var(--m-edge);right:80px;top:280px;display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:64px;}}
.hero-row .n{{font-weight:100;font-size:144px;line-height:1;}}
/* §15.7 — count-up must not reflow layout: equal 1fr tracks above + tabular
   figures here keep every digit tick the same width. */
.hero-num,.hero-row .n,.kpi .v,.stat-circle .v,.proc .n,[data-count]{{font-variant-numeric:tabular-nums lining-nums;}}
.hero-row .l{{font-weight:500;font-size:18px;letter-spacing:.1em;text-transform:uppercase;margin-top:16px;}}
.hero-row .d{{font-weight:400;font-size:20px;line-height:1.35;margin-top:14px;}}
.vrule{{position:absolute;width:1px;background:var(--wpp-navy);}}
.num-ghost{{position:absolute;font-weight:100;font-size:560px;line-height:.75;z-index:0;color:var(--orange-500);pointer-events:none;}}
.num-ghost--white{{color:var(--wpp-white);}}
.num-ghost--cream{{color:var(--wpp-cream);}}
/* Motif art utilities. Payload dedup: slides carry a .motif host whose data-motif names a
   shipped asset; NAV_JS clones the img from the matching template at load — one payload, N uses. */
.motif{{position:absolute;z-index:0;pointer-events:none;}}
.motif img{{width:100%;height:auto;display:block;}}
.motif--right{{right:-160px;top:50%;transform:translateY(-50%);width:1100px;}}   /* text-safe: x < 1200 */
.motif--bottom{{right:-120px;bottom:-160px;width:1400px;}}                        /* text-safe: y < 560 */
.motif--backdrop{{left:50%;top:54%;transform:translate(-50%,-50%);width:900px;}}
.motif--panel{{inset:0;overflow:hidden;}}
.motif--panel img{{width:100%;height:100%;object-fit:cover;}}
.motif--bleed{{inset:0;}}
.motif--bleed img{{width:1920px;height:1080px;object-fit:cover;}}
/* Density variants */
.cols--spacious{{top:340px;gap:120px;}}
.cols--compact{{top:240px;gap:56px;}}
.cols--compact .body{{font-size:22px;}}
.tbx-row--fill{{top:260px;bottom:200px;}}
.tbx-row--fill .tbx{{display:flex;flex-direction:column;gap:18px;}}
.proc--cards{{top:260px;bottom:380px;gap:32px;}}  /* §15.4 — cards hug content; pair with a .takeaway to anchor the freed bottom band */
.proc--cards>div{{background:var(--bg-alt);padding:36px 32px;}}
.kpi-row--low{{top:auto;bottom:150px;}}
.team-grid--wide{{grid-template-columns:repeat(3,1fr);bottom:160px;}}
.team-grid--wide .ph{{width:260px;height:260px;}}
/* Full-height scaffolding (kills the dead lower band structurally) */
.canvas{{position:absolute;left:var(--m-edge);right:80px;top:240px;bottom:120px;}}
.canvas-grid{{display:grid;grid-template-columns:repeat(12,1fr);grid-auto-rows:1fr;gap:24px;height:100%;}}
/* v4 card-grid modifier (§12.14/§13.4): expandable cards expand INDIVIDUALLY —
   auto rows + start alignment, and the opened detail is an OVERLAY dropping
   over whatever sits below (flat white panel, no reflow): no sibling ever
   moves or stretches. The bento's default 1fr rows would stretch the whole
   row — verifier FAIL. */
.canvas-grid--cards{{grid-auto-rows:auto;align-items:start;align-content:start;}}
.canvas-grid--cards .card{{position:relative;}}
.canvas-grid--cards .card.is-open{{z-index:6;}}
.canvas-grid--cards .card.is-open .card-detail{{position:absolute;left:0;right:0;top:100%;
  margin-top:0;background:var(--wpp-white);padding:0 36px 30px;z-index:6;}}
.cell{{padding:40px;background:var(--bg-alt);}}
.cell--nav{{background:var(--wpp-navy);color:var(--text-inv);}}
.cell--tint{{background:var(--bg-tint);}}
.takeaway{{position:absolute;left:160px;right:160px;bottom:120px;font-weight:300;font-size:48px;line-height:1.15;padding:14px 44px;}}
.takeaway::before,.takeaway::after{{content:"";position:absolute;top:0;bottom:0;width:23px;border-top:1px solid var(--wpp-navy);border-bottom:1px solid var(--wpp-navy);}}
.takeaway::before{{left:0;border-left:1px solid var(--wpp-navy);}}
.takeaway::after{{right:0;border-right:1px solid var(--wpp-navy);}}
.slide--navy .takeaway::before,.slide--navy .takeaway::after{{border-color:var(--wpp-cream);}}
.ruler{{position:absolute;left:var(--m-edge);right:80px;height:1px;background:var(--wpp-navy);}}
.ruler-ticks{{position:absolute;left:var(--m-edge);right:80px;display:flex;justify-content:space-between;}}
.ruler-ticks span{{width:1px;height:17px;background:var(--wpp-navy);}}
.ruler-ticks span.major{{height:27px;}}
.ruler-label{{position:absolute;font-weight:500;font-size:15px;letter-spacing:.1em;text-transform:uppercase;}}
.stem{{position:absolute;width:1px;background:var(--orange-700);}}
.milestone{{position:absolute;width:250px;}}
.milestone .md{{width:14px;height:14px;border-radius:50%;background:var(--orange-700);}}
.milestone .ml{{font-weight:500;font-size:15px;letter-spacing:.08em;text-transform:uppercase;margin-top:10px;}}
.milestone .mb{{font-weight:400;font-size:18px;line-height:1.3;margin-top:8px;}}
.gantt{{position:absolute;left:var(--m-edge);right:80px;top:240px;bottom:200px;}}
.bar{{position:absolute;height:6px;}}
.lane-dot{{position:absolute;width:16px;height:16px;border-radius:50%;background:var(--wpp-navy);}}
.flag{{position:absolute;width:206px;height:46px;background:var(--wpp-navy);color:var(--wpp-white);font-weight:500;font-size:15px;letter-spacing:.06em;text-transform:uppercase;display:flex;align-items:center;justify-content:center;}} /* 15px = §4.5 floor */
/* High-impact extras */
.big-statement--poster{{font-size:220px;line-height:.8;}}
.layer-1{{z-index:1;}}
.layer-2{{z-index:2;}}

/* Orbit / hub diagrams */
.orbit-hub{{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:50%;}}
.orbit-node{{position:absolute;text-align:center;font:500 18px/1.2 'WPP',system-ui,sans-serif;
  color:var(--wpp-navy);letter-spacing:.04em;text-transform:uppercase;}}
.orbit-node .pill{{margin:0 auto 6px;}}

/* Logo wall */
.logo-row{{display:flex;align-items:center;gap:40px;padding:16px 0;border-bottom:1px solid rgba(0,0,80,.1);}}
.logo-row:last-child{{border-bottom:none;}}
.logo-row img,.logo-row svg{{max-height:44px;max-width:110px;display:block;}}
.logo-row .col-sub{{min-width:200px;flex-shrink:0;margin:0;}}

/* Venn */
.venn{{position:relative;margin:0 auto;}}
.venn-set{{position:absolute;border-radius:50%;display:flex;align-items:center;justify-content:center;
  border:2px solid var(--wpp-navy);background:rgba(0,0,80,.06);}}
.venn-set--orange{{border-color:var(--orange-700);background:rgba(249,189,93,.1);}}
.venn-label{{position:absolute;font:500 20px/1.2 'WPP',system-ui,sans-serif;text-align:center;
  color:var(--wpp-navy);max-width:180px;}}

/* Image-top cards */
.card-img{{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;}}

/* HUD */
#hud{{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:50;
  font:600 12px/1 'WPP',system-ui,sans-serif;color:#fff;opacity:.5;letter-spacing:.1em;
  background:rgba(0,0,0,.35);padding:6px 12px;border-radius:999px;user-select:none;}}
.notes{{display:none;}}
body.notes-on .slide.is-active .notes{{display:block;position:absolute;left:var(--m-edge);right:80px;bottom:70px;
  font:300 18px/1.4 'WPP',system-ui,sans-serif;color:var(--text);background:rgba(250,250,240,.92);
  padding:16px 20px;max-height:200px;overflow:auto;z-index:40;}}
body.notes-on .slide--navy.is-active .notes{{color:#FAFAF0;background:rgba(0,0,80,.88);}}
.noscript-banner{{position:fixed;left:0;right:0;top:0;z-index:60;background:#000050;color:#FAFAF0;
  font:300 15px/1.4 system-ui,sans-serif;padding:10px 16px;text-align:center;}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important;}}}}

/* Print / PDF: every slide its own 1920x1080 page (Ctrl+P -> save as PDF) */
@media print{{
  html,body{{background:#fff;height:auto;}}
  #stage{{position:static;overflow:visible;}}
  #frame{{position:static;transform:none!important;width:1920px;height:auto;}}
  .slide{{display:block!important;position:relative;page-break-after:always;break-after:page;}}
  #hud,.noscript-banner{{display:none!important;}}
}}
@page{{size:1920px 1080px;margin:0;}}
""" + KIT_V33_CSS + MOTION_CSS


# --- JS ------------------------------------------------------------------------------

def field_micro_defs(seed=407, n=110):
    """v4 MICRO register (§5): deterministic organic scatter — dense at the
    cluster heart (right-of-centre), dissolving outward, a few fused pairs.
    Generated at build time so renders are byte-stable for the verifier."""
    rng = random.Random(seed)
    defs, tries = [], 0
    while len(defs) < n and tries < n * 30:
        tries += 1
        x = rng.gauss(1560, 250)
        y = rng.gauss(430, 290)
        if not (1130 <= x <= 1960) or not (60 <= y <= 950):
            continue
        d = round(rng.uniform(18, 30))
        defs.append([d, round(x), round(y), "a"])
    return defs


def nav_js(spec):
    cw = COLOURWAYS[spec["dividerColourway"]]
    ot = OUTROS[spec["outro"]]
    dotcolors = json.dumps({
        "agenda":   {"a": "#FF7800", "b": "#F9BD5D", "c": "#D94E0E"},
        "divider":  {"a": cw["a"], "b": cw["b"], "c": cw["c"]},
        "divider-playbook": {"a": cw["a"], "b": cw["b"], "c": cw["c"]},
        "thankyou": {"a": ot["a"], "b": ot["b"], "c": ot["c"]},
        "cover-dots":  {"a": "#FFFFFF", "b": "#FFF5CD", "c": "#F9BD5D"},
        "cover-playbook": {"b": "#F9BD5D"},
        "lift-corner": {"a": "#FFFFFF", "b": "#FFFFFF", "c": "#FFF5CD"},
        "lift-orange-soft": {"a": "#FFF5CD", "b": "#F9BD5D", "c": "#FFF5CD"},
        "lift-navy-corner": {"a": "#FAFAF0", "b": "#FFF5CD", "c": "#FAFAF0"},
        # v3 content-slide dot fields: tone-on-tone default; accent for statement
        # moments; navy variant is text-safe by guideline rule (never behind text).
        "field-right": {"a": "#FFFFFF", "b": "#FFF5CD", "c": "#F9BD5D"},
        "field-bottom": {"a": "#FFFFFF", "b": "#FFF5CD", "c": "#F9BD5D"},
        "field-tl": {"a": "#FFFFFF", "b": "#FFF5CD", "c": "#F9BD5D"},
        "field-accent": {"a": "#FF7800", "b": "#F9BD5D", "c": "#D94E0E"},
        "field-navy": {"a": "#000050", "b": "#FF7800", "c": "#F9BD5D"},
        # v4 register fields (§5): one hue per field — micro accent orange,
        # mid soft O600, macro quietest O500 (huge shapes must whisper).
        "field-micro": {"a": "#FF7800"},
        "field-mid": {"a": "#F9BD5D"},
        "field-macro": {"a": "#FFF5CD"},
    })
    # v4 presets (§5/§12.3): playbook divider scatter (one hue, ≥2 edges bled,
    # one fused pair, top-left number zone and bottom-left title zone kept clear;
    # the 560px bottom-right dot preserves every colourway's footer-contrast
    # contract from the classic preset), the playbook cover drift, and the
    # MID/MACRO register fields. MICRO is generated (seeded — byte-stable).
    dots_v4 = json.dumps({
        "divider-playbook": [
            [300, 700, -120, "a"], [200, 930, -60, "a"],
            [680, 1360, -240, "a"], [420, 1660, 240, "a"],
            [180, 1240, 180, "a"], [560, 1500, 740, "a"], [90, 1150, 430, "a"],
        ],
        "cover-playbook": [
            [300, 1500, -140, "b"], [170, 1690, 150, "b"], [130, 1600, 240, "b"],
            [90, 1350, 90, "b"], [200, 1810, 340, "b"],
        ],
        "field-mid": [
            [420, 1700, -160, "a"], [340, 1330, -120, "a"], [480, 1760, 300, "a"],
            [300, 1420, 260, "a"], [360, 1520, 560, "a"], [260, 1720, 700, "a"],
            [300, 1060, 720, "a"], [200, 1160, 140, "a"], [420, 1620, 860, "a"],
            [140, 1260, 480, "a"],
        ],
        "field-macro": [
            [1400, -500, -780, "a"], [1750, 1050, -300, "a"], [1150, 650, 860, "a"],
        ],
        "field-micro": field_micro_defs(),
    })
    return r"""
(function(){
  document.body.className+=' js';
  var frame=document.getElementById('frame');
  var stage=document.getElementById('stage');
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var i=0, hud=document.getElementById('hud'), hint=document.getElementById('hud-hint'),
      count=document.getElementById('hud-count'), prog=document.getElementById('prog');

  // Motif dedup: clone inlined <template data-asset> art into [data-motif] hosts.
  document.querySelectorAll('[data-motif]').forEach(function(h){
    var t=document.querySelector('template[data-asset="'+h.getAttribute('data-motif')+'"]');
    if(t&&t.content&&t.content.firstElementChild) h.appendChild(t.content.firstElementChild.cloneNode(true));
  });

  // Runtime page numbers — slides can be added/removed during the fill step
  // without any renumbering. The baked totals in comments are advisory only.
  slides.forEach(function(s,k){var p=s.querySelector('.pageno');
    if(p)p.textContent=('0'+(k+1)).slice(-2)+' / '+slides.length;});

  function fit(){
    var vw=innerWidth, vh=innerHeight, s=Math.min(vw/1920, vh/1080);
    frame.style.transform='translate('+((vw-1920*s)/2)+'px,'+((vh-1080*s)/2)+'px) scale('+s+')';
  }
  function show(n){
    // Same-slide guard (§15.7): at deck boundaries (or a hashchange to the
    // current index) re-showing the visible slide would strip + re-add every
    // m-* class and replay the choreography — a full-slide visual snap.
    var t=Math.max(0,Math.min(slides.length-1,n));
    if(t===i&&slides[t].classList.contains('is-active'))return;
    i=t;
    slides.forEach(function(s,k){s.classList.toggle('is-active',k===i);});
    if(count) count.textContent=(i+1)+' / '+slides.length;
    if(history.replaceState) history.replaceState(null,'','#'+(i+1));
    if(prog) prog.style.width=((i+1)/slides.length*100)+'%';
    mPlay(slides[i]);
  }
  function goHash(){var n=parseInt(location.hash.slice(1),10); if(!isNaN(n)) show(n-1);}

  var chapterStarts=[];
  slides.forEach(function(s,k){
    var id=s.getAttribute('data-slide-id')||'';
    if(id.indexOf('divider-')===0) chapterStarts.push(k);
  });

  addEventListener('keydown',function(e){
    var t=e.target;
    if(t&&(t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.tagName==='SELECT'))return;
    if((e.key==='Enter'||e.key===' ')&&document.activeElement&&
       document.activeElement.classList&&document.activeElement.classList.contains('card')){
      var ac=document.activeElement;ac.classList.toggle('is-open');
      ac.setAttribute('aria-expanded',ac.classList.contains('is-open'));
      e.preventDefault();return;
    }
    if(e.key===' '&&document.activeElement!==document.body)return;
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){next();e.preventDefault();}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){show(i-1);e.preventDefault();}
    else if(e.key==='Home'){show(0);}
    else if(e.key==='End'){show(slides.length-1);}
    else if(e.key==='n'||e.key==='N'){document.body.classList.toggle('notes-on');}
    else if(e.key==='f'||e.key==='F'){(document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen());}
    else if(e.key==='?'){if(hint)hint.style.display=hint.style.display==='none'?'':'none';}
    else if(e.key>='1'&&e.key<='9'){var d=chapterStarts[+e.key-1];if(d!==undefined)show(d);}
  });

  stage.addEventListener('click',function(e){
    if(e.target.closest('a,button,[role="button"],input,textarea,select,summary,.card,[data-no-nav]'))return;
    if(String(getSelection&&getSelection()).length)return;
    if(e.clientX>innerWidth*0.5) next(); else show(i-1);
  });
  // §13.4 individual expansion: each card toggles ALONE — never siblings.
  document.addEventListener('click',function(e){
    var c=e.target.closest('.card');
    if(c){c.classList.toggle('is-open');
      c.setAttribute('aria-expanded',c.classList.contains('is-open'));}
  });

  // Locked dot compositions — geometry verbatim from the approved compositions.
  // Colour keys a/b/c resolve through DOTCOLORS (per-deck sanctioned colourway).
  function mkdots(host,defs,palette){
    defs.forEach(function(d){var e=document.createElement('div');e.className='dot';
      e.style.width=e.style.height=d[0]+'px';e.style.left=d[1]+'px';e.style.top=d[2]+'px';
      e.style.background=(palette&&palette[d[3]])||d[3];host.appendChild(e);});
  }
  var DOTS={
    agenda:[[360,300,-130,'a'],[150,170,300,'b'],[80,120,170,'c']],
    divider:[[760,1500,-200,'a'],[560,1500,740,'a'],[180,1360,560,'b'],[90,1300,300,'c']],
    thankyou:[[760,1500,620,'a'],[300,1640,-120,'b'],[150,1360,760,'c']],
    'cover-dots':[[900,1240,-280,'a'],[560,1500,430,'a'],[360,1060,300,'b'],[300,1330,840,'a'],[150,1170,720,'c']],
    'lift-corner':[[420,1700,880,'a'],[180,1560,780,'b'],[90,1500,1000,'c']],
    'lift-orange-soft':[[420,1700,880,'a'],[180,1560,780,'b'],[90,1500,1000,'c']],
    'lift-navy-corner':[[420,1700,880,'a'],[180,1560,780,'b'],[90,1500,1000,'c']],
    // field-right hugs the right EDGE (≤100px intrusion past x1740, solid 'c'
    // dot fully off-canvas): the old cluster put a solid mid-orange dot at
    // x1520 — inside the third column's text zone on cols-3 layouts (§15.2).
    'field-right':[[560,1640,-200,'a'],[300,1740,440,'b'],[150,1848,310,'c'],[90,1780,790,'a']],
    'field-bottom':[[520,1640,820,'a'],[260,320,940,'b'],[120,240,800,'c'],[80,620,1000,'b']],
    'field-tl':[[300,-110,-110,'a'],[130,230,90,'b'],[70,140,300,'c']],
    'field-accent':[[560,1640,-200,'a'],[300,1740,440,'b'],[150,1848,310,'c'],[90,1780,790,'a']],
    'field-navy':[[520,1640,820,'a'],[260,320,940,'b'],[120,240,800,'c']]
  };
  // v4 presets (playbook divider/cover + register fields) — build-time data.
  var DOTS_V4=__DOTSV4__;
  for(var dk in DOTS_V4) DOTS[dk]=DOTS_V4[dk];
  var DOTCOLORS=__DOTCOLORS__;
  document.querySelectorAll('[data-dots]').forEach(function(h){
    var k=h.getAttribute('data-dots'); mkdots(h, DOTS[k]||[], DOTCOLORS[k]);
  });

  // --- Motion v3.2: runtime choreography over the kit (guideline §14).
  // Elements move, colours never do. Auto-off: reduced-motion, headless
  // capture (navigator.webdriver), print. URL override: ?motion=off|subtle|full
  // ('?motion=force' keeps full even under webdriver — motion smoke-tests).
  var mParam=(location.search.match(/[?&]motion=([a-z]+)/)||[])[1];
  if(mParam==='force') document.body.setAttribute('data-motion','full');
  else if(mParam) document.body.setAttribute('data-motion',mParam);
  else if(navigator.webdriver||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))
    document.body.setAttribute('data-motion','off');
  function mLevel(){return document.body.getAttribute('data-motion')||'off';}

  var M_ROLES=[
    ['.mw','m-rise'],
    ['.panel','m-wipe'],['.compare-art','m-float-in'],['.motif','m-float-in'],
    ['.duo','m-fade'],['.icon','m-pop'],['.spark','m-pop'],
    ['.num-ghost','m-drift'],['.headline','m-rise'],['.subtitle','m-rise'],
    ['.subhead','m-rise'],['.media','m-fade'],['.card','m-rise'],
    ['.cover-mountain__title','m-rise'],['.cover-mountain__sub','m-rise'],
    ['.cover-mountain__meta','m-rise'],['.cover-art--right','m-float-in'],
    ['.dv-num','m-rise'],['.dv-sub','m-rise'],['.dv-title','m-rise'],
    ['.toc-row','m-rise'],
    ['.big-statement','m-rise'],['.big-quote','m-rise'],['.quote-attr','m-rise'],
    ['.hero-row>div','m-rise'],['.cols>div','m-rise'],['.proc>div','m-rise'],
    ['.tbx','m-rise'],['.kpi','m-rise'],['.stat-circle','m-rise'],
    ['.milestone','m-rise'],['.compare-left','m-rise'],['.compare-right','m-rise'],
    ['.content-band','m-rise'],
    ['.vrule','m-grow'],['.stem','m-grow'],
    ['.ruler','m-draw'],['.timeline','m-draw'],['.gantt .bar','m-draw'],
    ['.ruler-ticks','m-fade'],['.ruler-label','m-fade'],['.tl-label','m-fade'],
    ['.tl-node','m-pop'],['.sep-dot','m-pop'],['.sep-arrow','m-fade'],['.flag','m-fade'],
    ['.takeaway','m-rise']
  ];
  var M_ALL='m-in m-rise m-fade m-wipe m-pop m-grow m-draw m-float-in m-drift'.split(' ');
  function mSet(e,role,idx){
    M_ALL.forEach(function(c){e.classList.remove(c);});
    void e.offsetWidth;
    e.style.setProperty('--mi',Math.min(idx,12));
    e.classList.add('m-in',role);
  }
  // Kinetic type: split the big text moments into word spans (once per element)
  // so each word rises on its own beat. Plain-text elements only.
  function mWords(s){
    s.querySelectorAll('.big-statement,.big-quote,.dv-title,.cover-mountain__title')
     .forEach(function(e){
      if(e.getAttribute('data-mw')||e.children.length)return;
      var w=(e.textContent||'').trim().split(/\s+/);
      if(w.length<2||w.length>14)return;
      e.setAttribute('data-mw','1');
      e.innerHTML=w.map(function(x){
        return '<span class="mw">'+x.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span>';
      }).join(' ');
    });
  }
  function mPlay(s){
    if(!s||mLevel()==='off')return;
    var k=0,seen=[];
    M_ROLES.forEach(function(r){
      s.querySelectorAll(r[0]).forEach(function(e){
        if(seen.indexOf(e)>=0||e.closest('.notes'))return;
        if(e.getAttribute('data-mw')||e.closest('[data-build]'))return;
        seen.push(e); mSet(e,r[1],k++);
      });
    });
    s.querySelectorAll('.dot').forEach(function(e,j){
      if(seen.indexOf(e)<0&&!e.closest('[data-build]')) mSet(e,'m-pop',Math.min(2+j,9));
    });
    // Fragments: [data-build] blocks hide on activation and reveal one per
    // forward step (→ / Space / click) before the deck advances.
    s.querySelectorAll('[data-build]').forEach(function(e){e.classList.add('frag-off');});
    s.classList.toggle('m-live',mLevel()==='full');
    mCount(s);
  }
  function mFrag(){
    if(mLevel()==='off')return false;
    var f=slides[i].querySelector('[data-build].frag-off');
    if(f){f.classList.remove('frag-off');return true;}
    return false;
  }
  function next(){ if(!mFrag()) show(i+1); }
  // Count-up: display figures animate 0 -> value on first reveal. Locale-aware:
  // comma decimals, dot thousands, prefix/suffix and zero-padding preserved.
  function mCount(s){
    if(mLevel()==='off')return;
    var sel='.hero-num,.hero-row .n,.kpi .v,.stat-circle .v,.proc .n,[data-count]';
    s.querySelectorAll(sel).forEach(function(e){
      if(e.getAttribute('data-mc'))return;
      var m=(e.textContent||'').match(/^([^0-9]*)([0-9][0-9.,]*)([\s\S]*)$/);
      if(!m)return;
      // Never count words that merely contain a digit ('1 Sep', '12 weeks'):
      // a counting calendar date reads as a glitch, and the digit-count change
      // mid-flight reflows the row (§15.7). %, +, x and one-letter units pass.
      if(/[A-Za-z]/.test(m[1])||/[A-Za-z]{2,}/.test(m[3]))return;
      var raw=m[2],dm=raw.match(/,([0-9]+)$/),dec=dm?dm[1].length:0,
          thou=/[0-9]\.[0-9]{3}(?![0-9])/.test(raw),
          pad=/^0[0-9]/.test(raw)?raw.length:0,
          v=parseFloat(raw.replace(/\./g,'').replace(',','.'));
      if(isNaN(v))return;
      e.setAttribute('data-mc',e.textContent);
      // Pin the final rendered width for the count's duration so the ticking
      // digits never resize auto-sized grid tracks / re-wrap siblings (§15.7).
      e.style.minWidth=e.offsetWidth+'px';
      var t0=performance.now(),D=950;
      function fmt(x){
        var t=dec?x.toFixed(dec).replace('.',','):String(Math.round(x));
        if(thou)t=t.replace(/\B(?=([0-9]{3})+(?![0-9]))/g,'.');
        while(pad&&t.length<pad)t='0'+t;
        return m[1]+t+m[3];
      }
      requestAnimationFrame(function step(now){
        var p=Math.min(1,(now-t0)/D);p=1-Math.pow(1-p,3);
        if(p<1){e.textContent=fmt(v*p);requestAnimationFrame(step);}
        else{e.textContent=e.getAttribute('data-mc');e.style.minWidth='';}
      });
    });
  }
  // Pointer parallax (full only): the art layers trail the cursor a few px.
  var mpx=0,mpy=0,mpr=null;
  stage.addEventListener('pointermove',function(e){
    if(mLevel()!=='full')return;
    mpx=(e.clientX/innerWidth)*2-1; mpy=(e.clientY/innerHeight)*2-1;
    if(!mpr)mpr=requestAnimationFrame(function(){mpr=null;
      stage.style.setProperty('--parx',mpx.toFixed(3));
      stage.style.setProperty('--pary',mpy.toFixed(3));});
  });

  if(hint) setTimeout(function(){hint.style.display='none';},5000);
  addEventListener('resize',fit); addEventListener('hashchange',goHash);
  // Split kinetic-type targets ONCE, before first paint: splitting after the
  // slide is visible can re-run text-wrap balancing over the new spans and
  // visibly re-break lines (Safari, §15.7). Seed the parallax vars so the
  // first pointermove never lurches art layers from an unset state.
  if(mLevel()!=='off') slides.forEach(mWords);
  stage.style.setProperty('--parx','0'); stage.style.setProperty('--pary','0');
  fit();
  var h=parseInt(location.hash.slice(1),10);
  show(!isNaN(h)?h-1:0);
})();
""".replace("__DOTCOLORS__", dotcolors).replace("__DOTSV4__", dots_v4)


# --- document ------------------------------------------------------------------------

def build(spec, demo=False):
    white_logo = read_svg_inline(os.path.join(LOGOS, "WPP_ES_MAP_logo_WHITE.svg"))
    chapters = normalize_chapters(spec["chapters"])
    n_content = sum(len(c["slides"]) for c in chapters)

    # Auto micro-deck only for single-chapter decks; for the <=4-final-content-
    # slides case set microDeck:true explicitly at plan time (a multi-chapter
    # SHELL always under-counts — placeholders get expanded during the fill step).
    micro = spec["microDeck"]
    if micro is None:
        micro = len(chapters) == 1
    if micro:
        print("micro-deck mode: agenda and dividers omitted "
              f"({len(chapters)} chapter(s), {n_content} planned content slide(s))",
              file=sys.stderr)

    slides = [title_slide(spec, white_logo)]
    if not micro:
        slides.append(agenda_slide(spec, chapters))
    for cn, ch in enumerate(chapters, start=1):
        if not micro:
            slides.append(divider_slide(spec, cn, ch["title"]))
        for sn, sl in enumerate(ch["slides"], start=1):
            slides.append(content_placeholder(spec, sl, cn, sn))
    slides.append(thankyou_slide(spec))

    templates = ""
    for m in spec.get("illustrations") or []:
        templates += (f'\n<template data-asset="{esc(m)}">'
                      f'<img src="{motif_uri(m)}" alt=""></template>')

    s = spec["_strings"]
    demo_banner = "\n<!-- DEMO DECK — not for delivery: built without --spec -->" if demo else ""
    total = len(slides)
    noscript = ("This deck uses JavaScript for navigation — only the first slide is shown. "
                "Open it in any browser with JavaScript enabled.")
    return f"""<!doctype html>
<html lang="{esc(spec['lang'])}">{demo_banner}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{BRAND} — {esc(spec['title'])}</title>
<style>
{font_face_css()}
{base_css(spec)}
</style>
</head>
<body data-direction="{esc(spec['direction'])}" data-motion="{esc(spec['motion'])}">
<noscript><div class="noscript-banner">{noscript}</div></noscript>
<div id="stage"><div id="frame">
{''.join(slides)}
</div></div>
<div id="prog" aria-hidden="true"></div>
<div id="hud" aria-hidden="true"><span id="hud-count">1 / {total}</span><span id="hud-hint"> · ←→ navigate · F fullscreen · N notes · ? help</span></div>{templates}
<script>
{nav_js(spec)}
</script>
</body>
</html>
"""


DEMO_SPEC = {
    "title": "AI NATIVE",
    "subtitle": "How WPP Enterprise Solutions | MAP moves to an AI-native way of working",
    "month": "July 2026",
    "presenter": "Presenter name",
    "chapters": ["Why this matters", "Where we're taking MAP", "The champion role"],
}

DEFAULTS = {
    "direction": "editorial-quiet",
    "dividerColourway": None,   # resolved from direction if absent
    "cover": "mountain",
    "outro": "light",
    "confidential": False,
    "lang": "en",
    "strings": {},
    "contact": None,
    "microDeck": None,
    "illustrations": [],
    "motion": None,             # resolved from direction if absent
    "dividerStyle": "playbook", # v4 default; "classic" = the v3 geometry
}


def resolve(raw):
    """Merge defaults into a validated raw spec and resolve derived values."""
    spec = dict(DEFAULTS)
    spec.update({k: v for k, v in raw.items() if v is not None})
    if not spec.get("dividerColourway"):
        spec["dividerColourway"] = DIRECTION_COLOURWAY[spec["direction"]]
    if not spec.get("motion"):
        spec["motion"] = DIRECTION_MOTION[spec["direction"]]
    strings = dict(STRINGS.get(spec["lang"], STRINGS["en"]))
    strings.update(spec.get("strings") or {})
    spec["_strings"] = strings
    return spec


def main():
    ap = argparse.ArgumentParser(description="Build a self-contained WPP ES | MAP deck shell.")
    ap.add_argument("--spec", help="Path to JSON spec (see module docstring for the v2 schema).")
    ap.add_argument("--out", default="deck.html", help="Output HTML path (default deck.html).")
    args = ap.parse_args()

    if args.spec:
        with open(args.spec, "r", encoding="utf-8") as f:
            raw = json.load(f)
        errors, warnings = validate_spec(raw)
        for w in warnings:
            print(f"warning: {w}", file=sys.stderr)
        if errors:
            for e in errors:
                print(f"error: {e}", file=sys.stderr)
            sys.exit(2)
        demo = False
    else:
        raw = dict(DEMO_SPEC)
        demo = True
        print("no --spec given: building the DEMO deck (banner-stamped, "
              "verify_deck.py flags it unless run with --demo)", file=sys.stderr)

    spec = resolve(raw)
    out_html = build(spec, demo=demo)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out_html)
    n_slides = out_html.count('<section class="slide')
    print(f"Wrote {args.out}  ({len(out_html) // 1024} KB, {n_slides} slides, "
          f"cover={spec['cover']}, colourway={spec['dividerColourway']}, "
          f"outro={spec['outro']}, fully self-contained)")


if __name__ == "__main__":
    main()
