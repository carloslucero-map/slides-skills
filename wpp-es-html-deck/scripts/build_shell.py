#!/usr/bin/env python3
"""
build_shell.py v4 — generate a self-contained WPP Enterprise Solutions | MAP deck shell.

Why this exists
---------------
Two things are painful and error-prone to redo by hand on every deck, and both are
non-negotiable brand rules (see design-system/README.md):

  1. The deck must be ONE self-contained .html file — fonts, illustrations and the
     logo all base64/SVG-inlined, never external paths (references/HTML-BUILD.md §2a).
  2. The title / agenda / divider / thank-you slides are LOCKED compositions and
     must be reproduced verbatim (the Fixed slides cards). Sanctioned per-deck choices (cover art,
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
# The brand assets are the design system's, copied into design-system/ by
# authoring/refresh_design_system.py (SOURCE.json says from which version).
DS = os.path.join(SKILL, "design-system")
FONTS = os.path.join(DS, "fonts")
LOGOS = os.path.join(DS, "logos")
ILLOS = os.path.join(DS, "illustrations")



def _ds_json(name):
    with open(os.path.join(DS, name), encoding="utf-8") as f:
        return json.load(f)


# The design system's own values, from its copy in design-system/: tokens.json
# for :root and the fonts, fixed-slides.json for the divider colourways, the
# outros, the cover art, the agenda's rows and the dot presets. The copy is
# written only by the refresh (authoring/refresh_design_system.py); no brand
# value is written in this file.
TOKENS = _ds_json("tokens.json")
FIXED = _ds_json("fixed-slides.json")
_COLOURS = {t["name"]: t["value"]["light"] for t in TOKENS["color"]["tokens"]}
_SPACING = {t["name"]: t["value"] for t in TOKENS["spacing"]["tokens"]}


def tok(name):
    """A colour token as CSS: hex upper-case, an alias ({wpp-cream}) as var()."""
    v = _COLOURS[name]
    return f"var(--{v[1:-1]})" if v.startswith("{") else v.upper()

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

# Sanctioned per-deck divider colourways (the DividerSlide card). Geometry NEVER varies —
# only the colour keys a/b/c resolved by the emitted DOTCOLORS map, plus the
# divider background/text role vars. The design system's DividerSlide card holds
# every colour a divider uses: ground, type, sub-label, its dot hue ("a"), the
# footer on its big bottom-right dot, the confidential line, and the second and
# third dot colours ("b", "c") that only dividerStyle "classic" draws.
COLOURWAYS = {
    name: {"bg": c["ground"], "text": c["type"], "sub": c["subLabel"],
           "navy_section": c["ground"] == tok("wpp-navy"),
           "foot": c["footer"], "edge": c["confidential"],
           "a": c["dots"], "b": c["classicB"], "c": c["classicC"]}
    for name, c in FIXED["colourways"].items()
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

# The outros are the design system's (ThankYouSlide): ground, type, the three
# dot colours of the thankyou preset, and the colours of the footer furniture.
OUTROS = {
    name: {"bg": o["ground"], "text": o["type"], "navy_section": o["ground"] == tok("wpp-navy"),
           "foot": o["footer"], "edge": o["confidential"], **o["dots"]}
    for name, o in FIXED["outros"].items()
}

# Registered covers (the CoverSlide card): same locked frame (type block + navy badge
# untouched) — only the art layer swaps. The covers are the design system's
# (CoverSlide): an art file full-bleed or right-anchored, or a dot preset.
COVERS = {
    name: ({"art": "img-full" if c["placement"] == "full-bleed" else "img-right", "file": c["file"]}
           if "file" in c else {"art": "css", "preset": c["preset"]})
    for name, c in FIXED["covers"].items()
}

# v4 divider geometry (the DividerSlide card): "playbook" = one-hue macro scatter + bottom-pinned
# Thin caps title (the default); "classic" = the v3 right-anchored quartet.
DIVIDER_STYLES = ("playbook", "classic")

# Shipped motif-mechanism art, addressable from spec.illustrations. Paths are
# relative to design-system/. Three classes share the one template/clone mechanism:
# halftone illustrations, full-bleed textures, and the navy-duotone photo
# library (design-system/asset-notes.md; the photos are already duotone: place via data-motif,
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
    # v4 canonical square-grid dot conversions (scripts/halftone.py, HTML-BUILD §13.3)
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
    """One @font-face block per weight, base64 data-URI src — fully self-contained.
    The faces are the design system's WPP family (tokens.json type.fonts); its
    single-weight families (WPP Thin, Light, Medium) are for Claude Design Slides."""
    out = []
    for face in TOKENS["type"]["fonts"]:
        if face["family"] != "WPP":
            continue
        data = b64(os.path.join(DS, face["file"]))
        out.append(
            f"@font-face{{font-family:'{face['family']}';"
            f"src:url('data:font/woff2;base64,{data}') format('woff2');"
            f"font-weight:{face['weight']};font-display:swap;}}"
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
    return f"data:{mime};base64," + b64(os.path.join(DS, rel))


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
               f'src="data:image/png;base64,{b64(os.path.join(ILLOS, cover["file"]))}" alt="">')
    elif cover["art"] == "img-right":
        art = (f'    <img class="cover-art cover-art--right" '
               f'src="data:image/png;base64,{b64(os.path.join(ILLOS, cover["file"]))}" alt="">')
    else:
        art = (f'    <div class="cover-dots" data-dots="{cover["preset"]}" '
               'aria-hidden="true"></div>')
    presenter = (f'\n        <span class="presenter">{esc(spec["presenter"])}</span>'
                 if spec["presenter"] else "")
    return f"""
  <!-- ===== LOCKED TITLE SLIDE — registered cover art: {spec['cover']} (the CoverSlide card).
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


# Where the agenda's rows sit, from the design system's AgendaSlide card.
AGENDA = FIXED["agenda"]


def agenda_slide(spec, chapters):
    dense = len(chapters) == AGENDA["dense"]["chapters"]
    rows_at = AGENDA["dense"] if dense else AGENDA["rows"]
    top0, step = rows_at["top"], rows_at["pitch"]
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
  <!-- ===== LOCKED DIVIDER (v4 playbook composition, the DividerSlide card) — identical on every
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
            if arch else "Pick the archetype that fits (the design system's layout catalogue), then "
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

# The stylesheet is the design system's components/bundle.css, copied into
# design-system/bundle.css: the base slide, furniture, the fixed slides, the
# kit, icons and duotone, the motion classes and the print rules. Only :root is
# written here, because its last nine properties are per deck (the colourway
# and outro role vars); every other :root value is read from tokens.json.
def _bundle():
    with open(os.path.join(DS, "bundle.css"), encoding="utf-8") as f:
        css = f.read()
    start = css.index(":root{")
    end = css.index("\n}\n", start) + len("\n}\n")
    return css[:start], css[end:]


def base_css(spec):
    cw = COLOURWAYS[spec["dividerColourway"]]
    ot = OUTROS[spec["outro"]]
    head, rules = _bundle()
    s = _SPACING
    return head + f""":root{{
  --wpp-navy:{tok('wpp-navy')}; --wpp-cream:{tok('wpp-cream')}; --wpp-white:{tok('wpp-white')};
  --orange-900:{tok('orange-900')}; --orange-800:{tok('orange-800')}; --orange-700:{tok('orange-700')};
  --orange-600:{tok('orange-600')}; --orange-500:{tok('orange-500')};
  --bg:{tok('bg')}; --bg-alt:{tok('bg-alt')}; --bg-tint:{tok('bg-tint')};
  --bg-dark:{tok('bg-dark')}; --text:{tok('text')}; --text-inv:{tok('text-inv')};
  --accent:{tok('accent')};
  /* v4 semantic data colours (guideline 09): favourable numbers glow, unfavourable stay ink */
  --data-pos:{tok('data-pos')}; --data-neg:{tok('data-neg')};
  /* v4 layout tokens (guideline 03): {s['grid']} module, {s['m-edge']} content edge ({s['m-text']} for running
     copy) — deviating from these is what the §15.9 content-edge probe flags */
  --grid:{s['grid']}; --m-edge:{s['m-edge']}; --m-text:{s['m-text']}; --band-top:{s['band-top']}; --band-bottom:{s['band-bottom']};
  /* Per-deck sanctioned choices (spec keys) — defaults are the v1 look */
  --dv-bg:{cw['bg']}; --dv-text:{cw['text']}; --dv-sub:{cw['sub']};
  --dv-foot:{cw['foot']}; --dv-edge:{cw['edge']};
  --ty-bg:{ot['bg']}; --ty-text:{ot['text']};
  --ty-foot:{ot['foot']}; --ty-edge:{ot['edge']};
}}
""" + rules


# --- JS ------------------------------------------------------------------------------

def field_micro_defs(seed=407, n=110):
    """v4 MICRO register (guideline 04): deterministic organic scatter — dense at the
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


# The order the presets and their colours are emitted in; any preset the design
# system adds follows these, sorted.
DOT_ORDER = ("agenda", "divider", "divider-playbook", "thankyou", "cover-dots",
             "cover-playbook", "lift-corner", "lift-orange-soft", "lift-navy-corner",
             "field-right", "field-bottom", "field-tl", "field-accent", "field-navy",
             "field-micro", "field-mid", "field-macro")

def _ordered(d):
    return {k: d[k] for k in sorted(d, key=lambda k: (DOT_ORDER.index(k) if k in DOT_ORDER
                                                      else len(DOT_ORDER), k))}


def nav_js(spec):
    cw = COLOURWAYS[spec["dividerColourway"]]
    ot = OUTROS[spec["outro"]]
    # Dot colours: the per-deck ones follow the spec's colourway and outro; the
    # rest are the design system's (fixed-slides.json dotColours), tone-on-tone
    # fields, the accent field for statement moments, the text-safe navy field,
    # one hue per v4 register field.
    dotcolors = json.dumps(_ordered(dict(
        FIXED["dotColours"],
        **{"divider": {"a": cw["a"], "b": cw["b"], "c": cw["c"]},
           "divider-playbook": {"a": cw["a"], "b": cw["b"], "c": cw["c"]},
           "thankyou": {"a": ot["a"], "b": ot["b"], "c": ot["c"]}})))
    # Presets: the design system's, then (as build-time data merged over them)
    # the playbook divider and cover and the v4 register fields; MICRO is
    # generated (seeded, byte-stable) by field_micro_defs().
    v4_keys = ("divider-playbook", "cover-playbook", "field-mid", "field-macro", "field-micro")
    dots = json.dumps(_ordered({k: v for k, v in FIXED["dots"].items() if k not in v4_keys}))
    dots_v4 = json.dumps({
        "divider-playbook": FIXED["dots"]["divider-playbook"],
        "cover-playbook": FIXED["dots"]["cover-playbook"],
        "field-mid": FIXED["dots"]["field-mid"],
        "field-macro": FIXED["dots"]["field-macro"],
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
  var DOTS=__DOTS__;
  // v4 presets (playbook divider/cover + register fields) — build-time data.
  var DOTS_V4=__DOTSV4__;
  for(var dk in DOTS_V4) DOTS[dk]=DOTS_V4[dk];
  var DOTCOLORS=__DOTCOLORS__;
  document.querySelectorAll('[data-dots]').forEach(function(h){
    var k=h.getAttribute('data-dots'); mkdots(h, DOTS[k]||[], DOTCOLORS[k]);
  });

  // --- Motion v3.2: runtime choreography over the kit (HTML-BUILD §14).
  // Elements move, colours never do. Auto-off: reduced-motion, headless
  // capture (navigator.webdriver), print. URL override: ?motion=off|subtle|full
  // ('?motion=force' keeps full even under webdriver — motion smoke-tests).
  var mParam=(location.search.match(/[?&]motion=([a-z]+)/)||[])[1];
  if(mParam==='force') document.body.setAttribute('data-motion','full');
  else if(mParam) document.body.setAttribute('data-motion',mParam);
  else if(navigator.webdriver||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))
    document.body.setAttribute('data-motion','off');
  function mLevel(){return document.body.getAttribute('data-motion')||'off';}

  // GENERIC ROLE HOOKS for the canon (§14). The 25 canon templates each invent
  // their own class names — 432 of them — and none were in this list, so twelve
  // of them animated NOTHING but the slide fade while kit slides moved. The fix
  // is not 432 entries: templates declare the generic role alongside their own
  // class (class="m-unit spc-col"), exactly as they do for the fine-print type
  // tier. These sit first so the canon's stagger reads lead -> art -> units.
  var M_ROLES=[
    ['.mw','m-rise'],
    ['.m-lead','m-rise'],['.m-art','m-float-in'],['.m-unit','m-rise'],
    ['.m-mark','m-pop'],['.m-bar','m-draw'],
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
""".replace("__DOTCOLORS__", dotcolors).replace("__DOTSV4__", dots_v4).replace("__DOTS__", dots)


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
