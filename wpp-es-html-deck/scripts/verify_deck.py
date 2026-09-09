#!/usr/bin/env python3
"""
verify_deck.py — verify a generated WPP Enterprise Solutions | MAP deck .html.

Companion to build_shell.py: the builder emits a shell whose four locked slides
are correct by construction, but the fill step (archetypes, copy, images) is
manual — this script re-checks everything that step can break:

  1. Self-containment — no external URLs, no non-data src/href/url() refs,
     no @import, no file-path asset references (guideline §2a: ONE .html
     file, ever).
  2. Banned strings — stale brand names, demo placeholders, lorem ipsum,
     and the demo banner (allowed only with --demo).
  3. Structure — cover first, thank-you last, exactly one of each, lang attr,
     data-slide-id + runtime .pageno furniture everywhere, agenda rows ==
     divider count (<=6).
  4. Cover title length (2-4 words wanted; WARN only — user may have approved).
  5. Brand discipline — no gradients or shadows (box-/text-/drop-shadow)
     anywhere, border-radius only 50% (dots/circles) or 999px (pills),
     slide--white usage flagged, and every hex/rgb()/hsl() colour literal
     checked against the closed palette (§3.1/§3.2/§3.6; WARN with slide
     numbers — inspect, then fix or justify).
  6. Sizes — whole file vs --max-size-mb; each inlined image vs ~300KB raw.
  7. Speaker notes present on at least one slide.
  8. Optional headless-Chrome screenshots (--screenshots DIR) with a
     blank-render heuristic. Every slide by default; --quick restores the
     old fast subset, --slides 4,7,9 shoots only those (re-shoot loop).
  9. Composition tripwire (KIT v3, §12.15) — with --screenshots + Pillow,
     measures how much of each content slide's y432-990 band is bare
     background; a dead lower half FAILs (statement/quote archetypes and
     data-composition="intentional-air" soften to WARN), and >=95%
     background over the full canvas is an under-composed FAIL unless the
     slide explicitly declares intentional-air (declarations always print).
 10. Motif templates — every data-motif="X" needs <template data-asset="X">.
 11. Duplicate payloads — a base64 payload >=50 KB inlined 2+ times should
     be a data-motif template clone instead (one payload, N placements).
 12. Deck rhythm (C6, WARN-only) — adjacent content slides sharing
     data-archetype + treatment fingerprint (adjacency resets at dividers),
     or one archetype carrying more than half the content slides.
 13. Geometry laws (§15) — with --screenshots, a headless-Chrome probe
     records glyph-accurate rects for every text/positioned element and
     mechanically enforces: no text × text overlaps (FAIL), no decor
     covering >30% of a text rect (FAIL; full-bleed art exempt, and a
     data-text-safe="true" declaration on the decor or an ancestor softens
     to WARN — always printed for the art pass to re-check by eye), text
     inside the safe area (the deck's own --m-edge +/- 8px) / y>=20 (FAIL), no
     non-furniture text in the footer band y>985 (FAIL), sibling grids
     aligned within 6px with even gaps within 8px (WARN). Locked slides
     (cover/agenda/divider-*/thankyou) are exempt from the margin and
     footer laws — their geometry is locked by build_shell — but keep the
     overlap laws.
 14. Furniture contrast — with --screenshots + Pillow, each furniture
     element (.footer-brand, .pageno, .confidential, .source) is sampled
     in its screenshot: WCAG contrast of the computed text colour vs the
     median background under the glyphs. <2.0 FAIL, <3.0 WARN — catches
     cream-on-cream furniture sitting on decorative circles.

Usage
-----
  python verify_deck.py deck.html
  python verify_deck.py deck.html --demo                 # demo banner allowed
  python verify_deck.py deck.html --screenshots shots/   # render + composition
  python verify_deck.py deck.html --screenshots shots/ --quick
  python verify_deck.py deck.html --screenshots shots/ --slides 4,7,9
  python verify_deck.py deck.html --max-size-mb 5

Prints one line per check ("PASS/FAIL/WARN name — detail").
Exit 0 when every check passes (warnings allowed), exit 1 on any failure.
"""
import argparse, html, json, os, re, shutil, subprocess, sys, tempfile

# Headless Chrome is required for --screenshots and the geometry probe.
# Resolution order: $WPP_DECK_CHROME, then the usual install paths per platform,
# then anything Chrome-shaped on PATH. Empty string means "not installed here".
CHROME_CANDIDATES = (
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # Linux
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
    # Windows
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
)
CHROME_ON_PATH = ("google-chrome", "google-chrome-stable", "chromium",
                  "chromium-browser", "chrome")


def _find_chrome() -> str:
    """Absolute path to a headless-capable Chrome, or "" when none is found."""
    override = os.environ.get("WPP_DECK_CHROME", "").strip()
    if override:
        return override if os.path.isfile(override) else ""
    for path in CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    for name in CHROME_ON_PATH:
        found = shutil.which(name)
        if found:
            return found
    return ""


CHROME = _find_chrome()
CHROME_HELP = ("Chrome not found. Install Google Chrome, or point "
               "$WPP_DECK_CHROME at the binary.")

DEMO_BANNER = "DEMO DECK — not for delivery"

# Case-sensitive banned strings (stale brand + shell placeholders)...
BANNED = ("VML MAP", "VMLMAP", "Presenter name", "REPLACE WITH REAL CONTENT")
# ...and case-insensitive ones.
BANNED_CI = ("lorem ipsum",)

ALLOWED_RADII = {"50%", "999px"}   # dots/circles and pills — nothing else (§13)

# Closed palette (§3.1 primary, §3.2 orange ramp, §3.6 tertiary data-viz sets)
# plus the generator's own internals (letterbox chrome). 6-digit uppercase.
PALETTE_HEX = {
    "000050", "FAFAF0", "FFFFFF",                                   # §3.1
    "6A290A", "D94E0E", "FF7800", "F9BD5D", "FFF5CD",               # §3.2
    "FFC8DC", "FFB4B4", "D2BEFF", "80C0F5", "15FFCC", "B4FF64",     # §3.6 light
    "FFFF78",
    "8C0050", "500000", "500050", "00423E", "005000", "A0A000",     # §3.6 dark
    "0A1E78",
    "0A0A1A",                                                       # stage letterbox
}
# rgb()/rgba() triples the shell itself emits (translucent navy/cream/orange
# washes + the one sanctioned black scrim); anything else is off-palette.
PALETTE_RGB = ({(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
                for h in PALETTE_HEX} | {(0, 0, 0)})

MAX_IMG_B64 = 420 * 1024           # ~300KB raw per inlined image
BLANK_PNG_BYTES = 20 * 1024        # a blank 1920x1080 render compresses tiny

# Composition tripwire (KIT v3, guideline §12.15) --------------------------------
BG_NAVY = (0x00, 0x00, 0x50)       # slide--navy   #000050
BG_TINT = (0xFF, 0xF5, 0xCD)       # slide--tint   #FFF5CD
BG_CREAM = (0xFA, 0xFA, 0xF0)      # default slide #FAFAF0
BG_TOL = 12                        # per-channel tolerance when matching background
ZONE_TOP, ZONE_BOT, DESIGN_H = 432, 990, 1080   # dead-band zone in design pixels
COMP_FAIL, COMP_WARN = 0.92, 0.83  # zone background fraction thresholds (v4 tightened, §12.15a C2)
COMP_SOFT_FAIL = 0.97              # statement/quote archetypes FAIL only past this
COMP_FULL_FAIL = 0.95              # full-canvas background fraction — always FAIL

DUP_PAYLOAD_MIN = 50 * 1024        # base64 chars — repeated payloads this big WARN

_failed = False
_records = []          # (status, name, detail) — used only by the contact sheet


def report(status, name, detail):
    global _failed
    if status == "FAIL":
        _failed = True
    _records.append((status, name, detail))
    print(f"{status} {name} — {detail}")


def flagged_slides():
    """Slide numbers that FAILed or WARNed — these still need a full-res look."""
    out = set()
    for status, name, detail in _records:
        if status == "PASS":
            continue
        for m in re.finditer(r"slide[s]?\s+(\d+(?:\s*,\s*\d+)*)", f"{name} {detail}", re.I):
            for part in m.group(1).split(","):
                if part.strip().isdigit():
                    out.add(int(part))
    return out


# --- deck parsing ------------------------------------------------------------------

def strip_b64(text):
    """Replace every base64 data-URI payload with a stub. Payloads are random
    enough to contain banned substrings or 'http' by accident, so every string
    scan below runs on this stripped text."""
    return re.sub(r";base64,[A-Za-z0-9+/=]+", ";base64,STRIPPED", text)


def strip_xmlns(text):
    """Drop xmlns / xmlns:* attribute values — the only sanctioned http:// URLs
    (SVG namespace declarations in the inlined logo)."""
    return re.sub(r"""xmlns(:[A-Za-z0-9_.-]+)?\s*=\s*("[^"]*"|'[^']*')""", 'xmlns=""', text)


def parse_slides(text):
    """-> [{"cls": [tokens], "attrs": str, "body": str}] for each
    <section class="slide...">. Slides never nest, so a flat scan is safe."""
    slides = []
    for m in re.finditer(r'<section\s+class="(slide[^"]*)"([^>]*)>', text):
        end = text.find("</section>", m.end())
        slides.append({
            "cls": m.group(1).split(),
            "attrs": m.group(2),
            "body": text[m.end():end if end != -1 else len(text)],
        })
    return slides


def slide_id(s):
    m = re.search(r'data-slide-id="([^"]*)"', s["attrs"])
    return m.group(1) if m else None


# --- checks ------------------------------------------------------------------------

def check_self_contained(text):
    scan = strip_xmlns(strip_b64(text))

    hits = re.findall(r"https?://[^\s\"'<>)]*", scan)
    if hits:
        report("FAIL", "external URLs", f"{len(hits)} found (first: {hits[0]})")
    else:
        report("PASS", "external URLs", "no http(s):// outside xmlns/base64")

    bad = []
    for m in re.finditer(r"""\b(src|href)\s*=\s*("([^"]*)"|'([^']*)')""", scan):
        val = m.group(3) if m.group(3) is not None else m.group(4)
        if not (val.startswith("data:") or val.startswith("#")):
            bad.append(f'{m.group(1)}="{val[:60]}"')
    for m in re.finditer(r"""url\(\s*['"]?([^)'"]+)""", scan):
        if not m.group(1).startswith("data:"):
            bad.append(f"url({m.group(1)[:60]})")
    for m in re.finditer(
            r"""(?:src|href)\s*=\s*['"][^'"]*\.(?:woff2|png|svg|jpe?g|css|js)['"]""", scan):
        bad.append(m.group(0)[:70])
    if bad:
        report("FAIL", "non-inlined refs", "; ".join(bad[:5]) +
               (f" (+{len(bad) - 5} more)" if len(bad) > 5 else ""))
    else:
        report("PASS", "non-inlined refs", "every src/href/url() is data: or #fragment")

    n_imp = scan.count("@import")
    report("FAIL" if n_imp else "PASS", "@import",
           f"{n_imp} occurrence(s) — external stylesheets break self-containment"
           if n_imp else "not present")


def check_banned(text, demo):
    # Raw-text needle: the broken-img stub is base64-shaped, so strip_b64 would
    # hide it from the scan below (an unfilled image slot must never ship).
    if re.search(r";base64,\s*REPLACE\b", text):
        report("FAIL", "banned strings",
               "'base64,REPLACE' image stub — an image slot was never filled")

    ph = [s for s in ("Partner A", "Logo 1") if s in text]
    if ph:
        report("WARN", "placeholder names",
               ", ".join(repr(s) for s in ph) + " — logo-wall wordmark tiles still "
               "carry kit placeholder names; swap in the real partner names")

    scan = strip_b64(text)
    banned = BANNED
    if demo:
        # The built-in demo spec deliberately ships this placeholder; a --demo
        # run should be able to go fully green.
        banned = tuple(s for s in BANNED if s != "Presenter name")
    found = [s for s in banned if s in scan]
    found += [s for s in BANNED_CI if s.lower() in scan.lower()]
    if found:
        report("FAIL", "banned strings", ", ".join(repr(s) for s in found))
    else:
        report("PASS", "banned strings", "none of the placeholder/stale-brand strings")

    if DEMO_BANNER in scan:
        if demo:
            report("PASS", "demo banner", "present, allowed by --demo")
        else:
            report("FAIL", "demo banner", f"{DEMO_BANNER!r} — demo decks are not "
                   "deliverable (re-run build_shell.py with a real --spec, or pass --demo)")
    elif demo:
        report("WARN", "demo banner", "--demo given but no demo banner in the file")
    else:
        report("PASS", "demo banner", "absent")


def check_structure(text, slides):
    n = text.count('<section class="slide')
    report("PASS" if n >= 3 else "FAIL", "slide count",
           f"{n} slides" + ("" if n >= 3 else " — a deck needs at least cover + content + thank-you"))
    if not slides:
        return

    covers = sum(1 for s in slides if "cover-mountain" in s["cls"])
    thanks = sum(1 for s in slides if "thank-you" in s["cls"])
    first_ok = "cover-mountain" in slides[0]["cls"]
    last_ok = "thank-you" in slides[-1]["cls"]
    if first_ok and last_ok and covers == 1 and thanks == 1:
        report("PASS", "cover/thank-you", "first slide is the cover, last is the "
               "thank-you, exactly one of each")
    else:
        report("FAIL", "cover/thank-you",
               f"first={'cover' if first_ok else slides[0]['cls']}, "
               f"last={'thank-you' if last_ok else slides[-1]['cls']}, "
               f"covers={covers}, thankyous={thanks}")

    if re.search(r"<html\s+lang=", text):
        report("PASS", "html lang", "lang attribute present")
    else:
        report("FAIL", "html lang", "<html lang=…> missing")

    missing = [i + 1 for i, s in enumerate(slides) if not slide_id(s)]
    report("PASS" if not missing else "FAIL", "data-slide-id",
           "every slide carries one" if not missing else f"missing on slide(s) {missing}")

    nopage = [i + 1 for i, s in enumerate(slides)
              if "cover-mountain" not in s["cls"] and 'class="pageno"' not in s["body"]]
    report("PASS" if not nopage else "FAIL", "pageno furniture",
           "every non-cover slide has an empty .pageno"
           if not nopage else f"missing on slide(s) {nopage} — page numbers won't render")

    agendas = [s for s in slides if "agenda" in s["cls"]]
    dividers = [s for s in slides if (slide_id(s) or "").startswith("divider-")]
    if agendas:
        rows = agendas[0]["body"].count('class="toc-row"')
        if rows == len(dividers) and rows <= 6:
            report("PASS", "agenda/dividers", f"{rows} toc-rows == {len(dividers)} dividers")
        else:
            report("FAIL", "agenda/dividers",
                   f"{rows} toc-rows vs {len(dividers)} divider slides"
                   + (" (locked agenda holds at most 6)" if rows > 6 else ""))
    else:
        report("PASS", "agenda/dividers",
               f"no agenda slide (micro-deck), {len(dividers)} dividers")


def check_cover_title(text):
    m = re.search(r'class="cover-mountain__title"[^>]*>(.*?)</h1>', text, re.S)
    if not m:
        report("FAIL", "cover title", "no .cover-mountain__title found on the cover")
        return
    title = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).strip()
    words = len(title.split())
    if 2 <= words <= 4:
        report("PASS", "cover title", f"{title!r} ({words} words)")
    else:
        report("WARN", "cover title", f"{title!r} is {words} words — the locked cover "
               "wants 2-4 (OK only if the user approved it)")


def check_brand(text):
    for needle, why in (("gradient(", "gradients are off-brand"),
                        ("box-shadow", "shadows are off-brand (flat design only)"),
                        ("text-shadow", "shadows are off-brand (flat design only)"),
                        ("drop-shadow(", "shadows are off-brand (flat design only)")):
        if needle in text:
            report("FAIL", f"brand: {needle.rstrip('(')}",
                   f"{text.count(needle)} occurrence(s) — {why}")
        else:
            report("PASS", f"brand: {needle.rstrip('(')}", "not present")

    bad = sorted({v.strip() for v in re.findall(r"border-radius\s*:\s*([^;}'\"]+)", text)}
                 - ALLOWED_RADII)
    report("PASS" if not bad else "FAIL", "brand: border-radius",
           "only 50% / 999px" if not bad
           else f"off-brand value(s): {', '.join(bad)} (only 50% and 999px allowed)")

    uses = re.findall(r'class="[^"]*slide--white[^"]*"', text)
    if uses:
        report("WARN", "brand: slide--white",
               f"{len(uses)} slide(s) use the rare white background — see §3.3a")
    else:
        report("PASS", "brand: slide--white", "not used")


def _off_palette(chunk):
    """Colour literals in `chunk` that sit outside the closed palette."""
    bad = set()
    for m in re.finditer(r"#([0-9a-fA-F]{3,8})\b", chunk):
        h = m.group(1).upper()
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        elif len(h) == 8:
            h = h[:6]
        elif len(h) != 6:
            continue
        if h not in PALETTE_HEX:
            bad.add("#" + m.group(1))
    for m in re.finditer(r"\brgba?\(([^)]*)\)", chunk):
        nums = re.findall(r"-?\d+(?:\.\d+)?", m.group(1))
        if len(nums) >= 3 and tuple(int(float(n)) for n in nums[:3]) not in PALETTE_RGB:
            bad.add(m.group(0)[:40])
    bad.update(m.group(0)[:40] for m in re.finditer(r"\bhsla?\([^)]*\)", chunk))
    return sorted(bad)


def check_palette(text, slides):
    """§13: 'no colours outside this document'. Hand-built charts and pasted
    art are where off-palette hexes sneak in; base64/xmlns stripped first."""
    offenders = []
    head = text.split("<section", 1)[0]
    for where, chunk in [("head/style", head)] + [
            (f"slide {i} ({slide_id(s) or '?'})", s["body"])
            for i, s in enumerate(slides, 1)]:
        for v in _off_palette(strip_xmlns(strip_b64(chunk))):
            offenders.append(f"{where}: {v}")
    if offenders:
        report("WARN", "brand: palette", "; ".join(offenders[:6]) +
               (f" (+{len(offenders) - 6} more)" if len(offenders) > 6 else "") +
               " — outside the closed palette (§3.1/§3.2/§3.6)")
    else:
        report("PASS", "brand: palette",
               "every colour literal is in the closed palette (§3.1/§3.2/§3.6)")


def check_sizes(path, text, max_mb):
    size = os.path.getsize(path)
    report("PASS" if size <= max_mb * 1024 * 1024 else "FAIL", "total size",
           f"{size / 1024 / 1024:.2f} MB (limit {max_mb} MB)")

    over = []
    payloads = re.findall(r"data:image/[a-zA-Z0-9.+-]+;base64,([A-Za-z0-9+/=]+)", text)
    for i, p in enumerate(payloads, 1):
        if len(p) > MAX_IMG_B64:
            over.append(f"image #{i}: {len(p) // 1024} KB encoded")
    if over:
        report("WARN", "image payloads", "; ".join(over) +
               f" — over {MAX_IMG_B64 // 1024} KB encoded (~300 KB raw); recompress")
    else:
        report("PASS", "image payloads",
               f"{len(payloads)} inlined image(s), all <= {MAX_IMG_B64 // 1024} KB encoded")


def check_notes(text):
    n = text.count('<aside class="notes"')
    if n:
        report("PASS", "speaker notes", f"present on {n} slide(s)")
    else:
        report("WARN", "speaker notes", "no <aside class=\"notes\"> anywhere — "
               "the fill step should carry the spec's notes through")


def check_motif_templates(text):
    """Every data-motif="X" placement needs the <template data-asset="X"> it
    clones from (NAV_JS does the cloning at load — see build_shell.py KIT v3)."""
    used = sorted(set(re.findall(r'data-motif\s*=\s*"([^"]+)"', text)))
    if not used:
        return   # no motif placements — nothing to verify, stay silent
    have = set(re.findall(r'<template[^>]*\sdata-asset\s*=\s*"([^"]+)"', text))
    missing = [u for u in used if u not in have]
    if missing:
        report("FAIL", "motif templates",
               "data-motif without a matching <template data-asset>: " + ", ".join(missing))
    else:
        report("PASS", "motif templates",
               f"{len(used)} motif name(s), each has a <template data-asset>")


# Native pixel widths of shipped motif-mechanism assets (§9.1a/§9.1b/§9.2a) —
# routing a small asset into a big host upscales and pixelates silently.
MOTIF_NATIVE_W = {
    "mountain": 1920, "mountain-orange": 1920, "peaks-orange": 1920,
    "crystal": 1920, "crystal-orange": 1920, "coral": 1920, "coral-orange": 1920,
    "rocks": 964, "rocks-orange": 964, "ribbon-orange": 964, "ribbon-navy": 964,
    "contours": 1920, "orbs": 1920,
    "photo-lighthouse": 1150, "photo-handoff": 1200, "photo-confetti": 1100,
    "photo-chess": 1200, "photo-globe": 820, "photo-pencils": 1050,
    "photo-dancers": 1050, "photo-gears": 900, "photo-fibers": 1150,
    "photo-team": 1000, "photo-diver": 1600, "photo-fjord": 1600,
    "photo-ridge": 1600,
}
HOST_RENDER_W = {"motif--bleed": 1920, "motif--bottom": 1400, "motif--right": 1100,
                 "motif--panel": 960, "motif--backdrop": 900}


def check_motif_routing(text):
    """WARN when a motif's native width sits below its host's render width
    (>~1.1x upscale) — the pixelation the eyes-on pass should re-check."""
    bad = []
    for m in re.finditer(r'<div class="motif ([^"]*)"[^>]*data-motif="([^"]+)"', text):
        classes, name = m.group(1), m.group(2)
        nat = MOTIF_NATIVE_W.get(name)
        if not nat:
            continue
        for cls, w in HOST_RENDER_W.items():
            if cls in classes and nat < 0.9 * w:
                bad.append(f"{name} ({nat}px native) in .{cls} (~{w}px)")
    if bad:
        report("WARN", "motif routing", "; ".join(sorted(set(bad))) +
               " — asset narrower than its host, it will upscale; use a "
               "1920px-class asset or a smaller host")
    else:
        report("PASS", "motif routing",
               "every routed motif is at or above its host's render width")


def check_duplicate_payloads(text):
    counts = {}
    for m in re.finditer(r";base64,([A-Za-z0-9+/=]+)", text):
        p = m.group(1)
        if len(p) >= DUP_PAYLOAD_MIN:
            counts[p] = counts.get(p, 0) + 1
    dups = sorted(((len(p), c) for p, c in counts.items() if c >= 2), reverse=True)
    if dups:
        report("WARN", "duplicate payloads",
               "; ".join(f"{sz // 1024} KB payload x{c}" for sz, c in dups[:5]) +
               " — motif duplicated — use data-motif cloning (one template, N placements)")
    else:
        report("PASS", "duplicate payloads",
               f"no base64 payload >= {DUP_PAYLOAD_MIN // 1024} KB appears twice")


def _treatment(s):
    """Coarse treatment fingerprint for C6: background class + dot presets +
    motifs + panel modifiers. Same archetype with a different fingerprint is
    legitimate rhythm; identical fingerprints adjacent is the C6 smell."""
    bg = "navy" if "slide--navy" in s["cls"] else \
         "tint" if "slide--tint" in s["cls"] else "light"
    return (bg,
            tuple(sorted(re.findall(r'data-dots="([^"]*)"', s["body"]))),
            tuple(sorted(re.findall(r'data-motif="([^"]*)"', s["body"]))),
            tuple(sorted(re.findall(r'class="panel (panel--[^"]*)"', s["body"]))))


def check_photography(slides):
    """§9.2 (WARN-only, coarse): a content slide embedding <img> outside the
    sanctioned wrappers (.duo duotone, .screenshot keyline, data-motif clone
    hosts) is probably a full-colour photo — the one look the brand bans."""
    flagged = []
    for i, s in enumerate(slides, 1):
        sid = slide_id(s) or ""
        if sid in ("cover", "agenda", "thankyou") or sid.startswith("divider-"):
            continue
        body = re.sub(r"<!--.*?-->", "", s["body"], flags=re.S)  # comments don't render
        if "<img" not in body:
            continue
        if not any(k in body for k in ('class="duo', "duo ", "screenshot", "data-motif")):
            flagged.append(f"s{i}")
    if flagged:
        report("WARN", "photography",
               "raw <img> outside .duo/.screenshot/motif on " + ", ".join(flagged) +
               " — full-colour photos are off-brand (§9.2: duotone or keyline)")
    else:
        report("PASS", "photography",
               "no raw <img> outside the sanctioned treatments")


def check_rhythm(slides):
    """C6 deck-rhythm tripwire (§12.15a, WARN-only) — a pure text scan over
    data-archetype + a coarse treatment fingerprint. The eyes-on art pass
    owns the full C6 call; this just stops a monotone deck shipping silently."""
    pairs, counts = [], {}
    prev = None                                    # (slide no, archetype, treatment)
    for i, s in enumerate(slides, 1):
        sid = slide_id(s) or ""
        if sid in ("cover", "agenda", "thankyou") or sid.startswith("divider-"):
            prev = None                            # a divider is a legitimate rhythm break
            continue
        m = re.search(r'data-archetype="([^"]*)"', s["attrs"])
        arch = (m.group(1) if m else "").strip()
        if not arch:
            prev = None                            # unfilled placeholder — nothing to compare
            continue
        counts[arch] = counts.get(arch, 0) + 1
        treat = _treatment(s)
        if prev and prev[1] == arch and prev[2] == treat:
            pairs.append(f"s{prev[0]}+s{i} ({arch})")
        prev = (i, arch, treat)

    n_known = sum(counts.values())
    if not n_known:
        print("SKIP rhythm — no data-archetype attributes on content slides")
        return
    if pairs:
        report("WARN", "rhythm adjacency",
               "adjacent content slides share archetype + treatment (C6) — "
               "vary the treatment or swap one: " + ", ".join(pairs))
    else:
        report("PASS", "rhythm adjacency",
               "no two adjacent content slides share archetype + treatment")
    if n_known >= 4:
        top, n_top = max(counts.items(), key=lambda kv: kv[1])
        if n_top * 2 > n_known:
            report("WARN", "rhythm spread",
                   f'"{top}" carries {n_top} of {n_known} content slides — '
                   "redistribute via the quick-map (SKILL.md step 1)")
        else:
            report("PASS", "rhythm spread",
                   f"{len(counts)} archetypes over {n_known} content slides "
                   f"(max {n_top}x {top})")


def build_contact_sheet(shots, n_slides, outpath, cols=4, tw=480, th=270, flagged=()):
    """Tile every captured slide into ONE image for the art-direction pass.

    Reading 12 full-res slides costs ~12x the tokens of reading one sheet, and
    for deck rhythm (C6) the sheet is actually the better view — repetition is
    visible at a glance. The §15 geometry checks run on the DOM, not on pixels,
    so nothing measurable is lost by looking at thumbnails.

    LIMIT, and it is not optional: at 480x270 you CANNOT judge type legibility,
    glyph collisions or contrast. Those are the verifier's job. Slides the
    verifier flagged get re-read at full resolution — that is what `flagged` is
    for; they are marked on the sheet.

    Purely additive: nothing calls this unless --contact-sheet is passed, and
    the per-slide PNGs are still written exactly as before.
    """
    if not shots:
        report("WARN", "contact sheet", "no screenshots captured — nothing to tile")
        return None
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        report("WARN", "contact sheet", "Pillow not installed — skipped")
        return None

    ns = sorted(shots)
    rows = (len(ns) + cols - 1) // cols
    pad, band = 8, 18
    W = cols * tw + (cols + 1) * pad
    H = rows * (th + band) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (232, 232, 232))
    d = ImageDraw.Draw(sheet)

    for i, n in enumerate(ns):
        try:
            im = Image.open(shots[n]).convert("RGB").resize((tw, th))
        except Exception as e:
            report("WARN", f"contact sheet slide {n}", str(e))
            continue
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + band + pad)
        sheet.paste(im, (x, y))
        mark = "  << FLAGGED - read at full resolution" if n in flagged else ""
        d.text((x + 2, y + th + 3), f"slide {n}{mark}", fill=(20, 20, 20))
        if n in flagged:
            d.rectangle([x - 2, y - 2, x + tw + 1, y + th + 1], outline=(255, 120, 0), width=3)

    os.makedirs(os.path.dirname(os.path.abspath(outpath)) or ".", exist_ok=True)
    sheet.save(outpath)
    missing = [n for n in range(1, n_slides + 1) if n not in shots]
    report("PASS", "contact sheet",
           f"{outpath} — {len(ns)}/{n_slides} slides tiled "
           f"({os.path.getsize(outpath) // 1024} KB)"
           + (f"; not captured: {missing}" if missing else ""))
    if flagged:
        report("WARN", "contact sheet",
               f"read these at full resolution, the sheet cannot judge them: {sorted(flagged)}")
    return outpath


def check_screenshots(path, n_slides, outdir, quick=False, only=None):
    """Render slides to PNG. Returns {slide_number: png_path} for every shot
    that captured and passed the blank-render heuristic (composition input)."""
    shots = {}
    if not CHROME:
        report("FAIL", "screenshots", CHROME_HELP)
        return shots
    os.makedirs(outdir, exist_ok=True)
    abspath = os.path.abspath(path)
    if only:                                       # --slides N,N,… re-shoot loop
        targets = [n for n in only if 1 <= n <= n_slides]
        bad = [n for n in only if not 1 <= n <= n_slides]
        if bad:
            report("WARN", "screenshots", f"--slides out of range (deck has {n_slides} "
                   f"slides): {', '.join(map(str, bad))}")
    elif quick:                                    # old fast subset
        targets = list(range(1, n_slides + 1)) if n_slides <= 12 else [1, 2, n_slides]
    else:                                          # default: every slide
        targets = list(range(1, n_slides + 1))
    for n in targets:
        shot = os.path.join(os.path.abspath(outdir), f"slide-{n}.png")
        # ?motion=off pins the shell's motion layer to its final static state —
        # captures must never freeze a mid-entrance frame (webdriver detection
        # alone is not guaranteed for plain CLI --screenshot runs).
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--window-size=1920,1080",
               "--hide-scrollbars", f"--screenshot={shot}",
               f"file://{abspath}?motion=off#{n}"]
        try:
            subprocess.run(cmd, capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            report("FAIL", f"screenshot slide {n}", "Chrome timed out")
            continue
        if not os.path.isfile(shot) or os.path.getsize(shot) == 0:
            report("FAIL", f"screenshot slide {n}", f"{shot} missing or empty")
        elif os.path.getsize(shot) <= BLANK_PNG_BYTES:
            report("FAIL", f"screenshot slide {n}",
                   f"{os.path.getsize(shot) // 1024} KB — looks like a blank render")
        else:
            report("PASS", f"screenshot slide {n}",
                   f"{shot} ({os.path.getsize(shot) // 1024} KB)")
            shots[n] = shot
    return shots


def _bg_fraction(img, bg, box=None):
    """Fraction of pixels in `box` (whole image if None) within BG_TOL per
    channel of `bg`. Pure Pillow (point ops + darker), no numpy needed."""
    from PIL import ImageChops
    region = img.crop(box) if box else img
    masks = []
    for ch, target in zip(region.split(), bg):
        lo, hi = target - BG_TOL, target + BG_TOL
        masks.append(ch.point(lambda v, lo=lo, hi=hi: 255 if lo <= v <= hi else 0))
    m = ImageChops.darker(ImageChops.darker(masks[0], masks[1]), masks[2])
    total = region.size[0] * region.size[1]
    return (m.histogram()[255] / total) if total else 0.0


def check_composition(slides, shots):
    """KIT v3 tripwire (§12.15): a content slide whose y432-990 band is nearly
    all background has a dead lower half — a layout smell the archetype fill
    step must fix with a §12.15 recipe, not by leaving air."""
    try:
        from PIL import Image
    except ImportError:
        print("SKIP composition — Pillow not installed (pip install pillow); "
              "dead-zone measurement skipped")
        return
    measured = 0
    for i, s in enumerate(slides, 1):
        sid = slide_id(s) or ""
        if sid in ("cover", "agenda", "thankyou") or sid.startswith("divider-"):
            continue                                   # locked furniture slides
        shot = shots.get(i)
        if not shot:
            continue                                   # not captured this run
        measured += 1

        bg = BG_NAVY if "slide--navy" in s["cls"] else \
             BG_TINT if "slide--tint" in s["cls"] else BG_CREAM
        img = Image.open(shot).convert("RGB")
        w, h = img.size
        y0, y1 = round(ZONE_TOP * h / DESIGN_H), round(ZONE_BOT * h / DESIGN_H)
        zone_frac = _bg_fraction(img, bg, (0, y0, w, y1))
        full_frac = _bg_fraction(img, bg)

        m = re.search(r'data-archetype="([^"]*)"', s["attrs"])
        arch = m.group(1) if m else ""
        soft = "statement" in arch or "quote" in arch
        air = 'data-composition="intentional-air"' in s["attrs"]

        if zone_frac >= COMP_FAIL:
            status, why = "FAIL", "dead lower half — assemble from a §12.15 recipe"
        elif zone_frac >= COMP_WARN:
            status, why = "WARN", "lower half is mostly background — consider a §12.15 recipe"
        else:
            status, why = "PASS", ""
        if status == "FAIL" and soft and zone_frac < COMP_SOFT_FAIL:
            status = "WARN"
            why += f" (statement/quote archetype — WARN below {COMP_SOFT_FAIL})"
        if status == "FAIL" and air:
            status = "WARN"
            why += " (downgraded by declaration)"
        if full_frac >= COMP_FULL_FAIL:
            # Thin display type is pixel-light: a template-faithful R3 slide can
            # measure ~0.96 full-canvas. An EXPLICIT intentional-air declaration
            # (always printed, and every slide is eyeballed in the art pass)
            # softens this to WARN; undeclared slides still hard-fail.
            status = "WARN" if air else "FAIL"
            why = (why + "; " if why else "") + \
                f"under-composed — bg {full_frac:.2f} over the full canvas"

        detail = f"bg {zone_frac:.2f} in y{ZONE_TOP}-{ZONE_BOT}"
        if air:
            detail += ' [data-composition="intentional-air"]'
        if why:
            detail += " — " + why
        report(status, f"composition s{i} ({sid})", detail)
    if not measured:
        print("SKIP composition — no content-slide screenshots captured to measure")


# --- geometry + furniture contrast (§15 layout laws) --------------------------------

# Injected into a temp copy of the deck; Chrome --headless=new --dump-dom then
# returns a <pre id="geo"> JSON: for every text-bearing / positioned element on
# every slide, its element box, glyph-accurate own-text rect (Range client
# rects), computed color/bg/font-size, decor classification and whether a
# data-text-safe="true" declaration covers it — all clipped by overflow-hidden
# ancestors and reported relative to the slide (frame transform killed).
GEO_PROBE_JS = r"""
<style id="probe-kill">*{animation:none!important;transition:none!important;caret-color:transparent!important}
#frame{transform:none!important}#hud,#prog,.noscript-banner{display:none!important}</style>
<script id="probe">
(function(){
  function run(){
    try{
      document.body.setAttribute('data-motion','off');
      document.body.classList.remove('notes-on');
      var frame=document.getElementById('frame'); if(frame) frame.style.transform='none';
      var slides=[].slice.call(document.querySelectorAll('.slide'));
      var POS='.dot,.motif,.panel,.orbit,.stat-circle,.card,.cell,img,svg,.media,.duo,.img-right-media,.img-half-media';
      var DECOR='.dot,.lift,.motif,.spark,.dv-dots,.ty-dots,.toc-dots,.num-ghost,.cover-art,.vrule,.ruler,.stem,.compare-art,.lift img,.lift svg';
      function ownText(el){var t='';for(var n=el.firstChild;n;n=n.nextSibling){if(n.nodeType===3)t+=n.nodeValue;}
        return t.replace(/\s+/g,' ').trim();}
      function clip(r,el,stop){ // intersect rect with every overflow-clipping ancestor up to slide
        var x1=r.left,y1=r.top,x2=r.right,y2=r.bottom,p=el.parentElement;
        while(p){
          var cs=getComputedStyle(p),o=cs.overflow+cs.overflowX+cs.overflowY;
          if(/hidden|clip|auto|scroll/.test(o)||p===stop){
            var pr=p.getBoundingClientRect();
            x1=Math.max(x1,pr.left);y1=Math.max(y1,pr.top);
            x2=Math.min(x2,pr.right);y2=Math.min(y2,pr.bottom);
          }
          if(p===stop)break;
          p=p.parentElement;
        }
        return {left:x1,top:y1,width:Math.max(0,x2-x1),height:Math.max(0,y2-y1)};
      }
      function textRect(el){ // union of own text-node client rects (glyph-accurate)
        var range=document.createRange(),x1=1/0,y1=1/0,x2=-1/0,y2=-1/0,found=false;
        for(var n=el.firstChild;n;n=n.nextSibling){
          if(n.nodeType!==3||!n.nodeValue.trim())continue;
          range.selectNodeContents(n);
          var rs=range.getClientRects();
          for(var q=0;q<rs.length;q++){var rr=rs[q];
            if(rr.width===0&&rr.height===0)continue;
            found=true;x1=Math.min(x1,rr.left);y1=Math.min(y1,rr.top);
            x2=Math.max(x2,rr.right);y2=Math.max(y2,rr.bottom);}
        }
        return found?{left:x1,top:y1,width:x2-x1,height:y2-y1}:null;
      }
      var out=[];
      slides.forEach(function(s,si){
        slides.forEach(function(o){o.style.display=(o===s)?'block':'none';
          o.classList.toggle('is-active',o===s);});
        var sr=s.getBoundingClientRect();
        var id=s.id||s.getAttribute('data-slide-id')||('slide-'+(si+1));
        var els=[].slice.call(s.querySelectorAll('*'));
        var recOf=new Map();
        els.forEach(function(el){
          if(el.closest('.notes')||el.closest('template'))return;
          var txt=ownText(el);
          var isPos=false; try{isPos=el.matches(POS);}catch(e){}
          if(!txt&&!isPos)return;
          var cs=getComputedStyle(el);
          if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity===0)return;
          var r0=el.getBoundingClientRect();
          if(r0.width<1&&r0.height<1)return;
          var r=clip(r0,el,s);
          if(r.width<1&&r.height<1)return;
          var tr=txt?textRect(el):null;
          if(tr)tr=clip({left:tr.left,top:tr.top,right:tr.left+tr.width,bottom:tr.top+tr.height,
                         width:tr.width,height:tr.height},el,s);
          var cls=(el.getAttribute('class')||'').trim().split(/\s+/).filter(Boolean);
          var sel=el.tagName.toLowerCase()+(cls.length?'.'+cls.join('.'):'');
          var pIdx=-1,p=el.parentElement;
          while(p&&p!==s){if(recOf.has(p)){pIdx=recOf.get(p);break;}p=p.parentElement;}
          var rec={slide:id,i:out.length,parent:pIdx,sel:sel,
            x:+(r.left-sr.left).toFixed(1),y:+(r.top-sr.top).toFixed(1),
            w:+r.width.toFixed(1),h:+r.height.toFixed(1),
            color:cs.color,bg:cs.backgroundColor,fs:cs.fontSize,
            text:txt.slice(0,40),hasText:!!(txt&&tr&&tr.width>0&&tr.height>0),pos:isPos,
            decor:(function(){try{return el.matches(DECOR);}catch(e){return false;}})(),
            safe:!!el.closest('[data-text-safe="true"]'),
            insetok:!!el.closest('[data-inset-ok]'),
            cardgrid:(function(){try{if(!el.matches('.card'))return '';
              var pc=getComputedStyle(el.parentElement);
              return pc.display.indexOf('grid')>-1?pc.gridAutoRows+'|'+pc.alignItems:'';}catch(e){return '';}})(),
            zi:cs.zIndex};
          if(tr&&tr.width>0&&tr.height>0){
            rec.tx=+(tr.left-sr.left).toFixed(1);rec.ty=+(tr.top-sr.top).toFixed(1);
            rec.tw=+tr.width.toFixed(1);rec.th=+tr.height.toFixed(1);}
          recOf.set(el,rec.i); out.push(rec);
        });
      });
      document.body.innerHTML='<pre id="geo"></pre>';
      document.getElementById('geo').textContent=JSON.stringify(out);
    }catch(e){
      document.body.innerHTML='<pre id="geo-err"></pre>';
      document.getElementById('geo-err').textContent=String(e&&e.stack||e);
    }
  }
  if(document.readyState==='complete'){document.fonts.ready.then(run);}
  else{window.addEventListener('load',function(){document.fonts.ready.then(run);});}
})();
</script>
"""

FURNITURE = {"footer-brand", "pageno", "confidential", "source"}
CONTRAST_FAIL, CONTRAST_WARN = 2.0, 3.0   # WCAG ratio thresholds for furniture


def _locked_slide(sid):
    """Locked-by-construction slides (build_shell owns their geometry)."""
    return sid in ("cover", "agenda", "thankyou") or sid.startswith("divider-")


def _content_edge(text, default=40.0):
    """The deck's own --m-edge. One source of truth: the built file."""
    m = re.search(r"--m-edge:\s*(\d+(?:\.\d+)?)px", text)
    return float(m.group(1)) if m else default


def _geo_capture(deck_path):
    """Run the probe once over the whole deck. -> (records, None) or (None, why)."""
    if not CHROME:
        return None, CHROME_HELP
    try:
        with open(deck_path, encoding="utf-8") as f:
            src = f.read()
    except OSError as e:
        return None, str(e)
    instr = (src.replace("</body>", GEO_PROBE_JS + "\n</body>", 1)
             if "</body>" in src else src + GEO_PROBE_JS)
    tmpdir = tempfile.mkdtemp(prefix="geomprobe-")
    tmp = os.path.join(tmpdir, "probe.html")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(instr)
        proc = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             "--window-size=1920,1080", "--virtual-time-budget=15000",
             "--dump-dom", "file://" + tmp + "?motion=off"],
            capture_output=True, text=True, timeout=120)
        dom = proc.stdout
    except (subprocess.TimeoutExpired, OSError) as e:
        return None, f"Chrome probe run failed ({e})"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    m = re.search(r'<pre id="geo">(.*?)</pre>', dom, re.S)
    if not m:
        err = re.search(r'<pre id="geo-err">(.*?)</pre>', dom, re.S)
        if err:
            return None, "probe JS error: " + html.unescape(err.group(1))[:300]
        return None, (f"no probe output in dumped DOM ({len(dom)} bytes); "
                      f"Chrome stderr tail: {proc.stderr[-300:]!r}")
    try:
        return json.loads(html.unescape(m.group(1))), None
    except ValueError as e:
        return None, f"probe JSON unparsable ({e})"


def _geo_classes(sel):
    return set(sel.split(".")[1:])


def _geo_is_ancestor(by_i, a, b):
    p = b["parent"]
    while p != -1:
        if p == a["i"]:
            return True
        p = by_i[p]["parent"]
    return False


def _geo_trect(r):
    """Glyph rect if available, else element box."""
    if "tx" in r:
        return r["tx"], r["ty"], r["tw"], r["th"]
    return r["x"], r["y"], r["w"], r["h"]


def _geo_ix(ax, ay, aw, ah, bx, by, bw, bh):
    ox = min(ax + aw, bx + bw) - max(ax, bx)
    oy = min(ay + ah, by + bh) - max(ay, by)
    return ox, oy


def _geo_fmt(r):
    x, y, w, h = _geo_trect(r)
    return "%s [%g,%g %gx%g] '%s'" % (r["sel"], x, y, w, h, r["text"])


def _geo_aligned(vals, tol):
    return max(vals) - min(vals) <= tol


def _geo_clusters(vals, tol):
    """Number of alignment clusters (values within tol of a cluster seed)."""
    out = []
    for v in sorted(vals):
        for c in out:
            if abs(v - c[0]) <= tol:
                c.append(v)
                break
        else:
            out.append([v])
    return len(out)


# §15.10 type-size floors (v4.1). Two levels, and the gap between them is a
# CLOSED LIST, not a judgement call.
#
# The bank runs 36% of its text runs under 20px and 15.5% under 15px, so a flat
# 20px floor would fail the source material it is supposed to model. But the
# reading that says "the real p10 is 14px, so allow 14px" gets it backwards:
# those slides were never legible projected. Slide 203 sets 47 of its 54 runs at
# 16px; the answer is that 16px is the second-level reference size for a named
# set of label roles, and that free prose can never reach it.
#
# So: nothing below MIN_FINE at all, and between MIN_FINE and MIN_TEXT only the
# roles below. A .body at 17px is a FAIL, not a warning — that is the whole point.
MIN_FINE = 16.0                          # declared second level, closed list only
MIN_TEXT = 20.0                          # everything else
MIN_FONT, MIN_BODY_FONT = MIN_FINE, MIN_TEXT   # back-compat for existing callers

# The closed list. Adding to it is a design decision that belongs in CORE §4.5,
# not a convenience. Roles measured in the kit today, plus the canon roles the
# second-level tier exists to serve.
FINE_PRINT_ROLES = frozenset({
    "col-sub", "pill", "bio", "l",                    # in the kit today
    "ramp-l1", "ramp-l2", "ramp-l3", "ramp-l4",       # intensity-ramp leaders
    "cell-label", "tax-leaf", "band-label",           # canon: matrix, taxonomy, stack
    "logo-cat", "sub-item",                           # canon: logo wall, second-level
})
MEDIA_MIN = 200.0                        # §15.9.2 media-anchoring size gate (v4)
# Media hosts the anchoring law applies to; ancestors/classes that exempt a
# rect (tiles/portraits/centrepieces whose inset placement IS the composition).
_MEDIA_HOSTS = {"motif", "duo", "media", "img-right-media", "img-half-media"}
_MEDIA_EXEMPT = {"card", "cell", "person", "ph", "logo-row", "compare-art",
                 "screenshot", "motif--backdrop", "cover-art", "card-img"}


def _geo_anc_classes(by_i, r):
    """Union of ancestor class sets for a probe record."""
    seen, p = set(), r["parent"]
    while p != -1:
        seen |= _geo_classes(by_i[p]["sel"])
        p = by_i[p]["parent"]
    return seen


def _geo_violations(rs, locked, edge=40.0):
    """(status, detail) §15 findings for one slide's probe records. Locked
    slides skip the margin/footer laws (their geometry deliberately rides the
    canvas edges) but keep the overlap laws."""
    by_i = {r["i"]: r for r in rs}
    out = []
    text_leaves = [r for r in rs if r["hasText"] and not r["decor"]
                   and not (_geo_classes(r["sel"]) & FURNITURE)]

    # ---- §15.10 type-size floor (v4) — measured computed sizes ----
    for t in text_leaves:
        try:
            fs = float(str(t.get("fs", "")).replace("px", "") or 0)
        except ValueError:
            continue
        cls = _geo_classes(t["sel"])
        if 0 < fs < MIN_FINE:
            out.append(("FAIL", "type floor (§15.10): %s at %.1fpx — nothing is set "
                        "below %gpx, whatever role it plays"
                        % (_geo_fmt(t), fs, MIN_FINE)))
        elif fs < MIN_TEXT and not (cls & FINE_PRINT_ROLES):
            out.append(("FAIL", "type floor (§15.10): %s at %.1fpx. Between %gpx and "
                        "%gpx only the declared second-level roles are allowed (%s); "
                        "this carries none of them. Raise the size or give it the role "
                        "it actually plays — do not shrink prose to make it fit (§4.5)."
                        % (_geo_fmt(t), fs, MIN_FINE, MIN_TEXT,
                           ", ".join(sorted(FINE_PRINT_ROLES)[:5]) + ", …")))

    # ---- §13.4/§12.14 card grid (v4) — cards must expand individually ----
    for r in rs:
        cg = r.get("cardgrid") or ""
        if not cg:
            continue
        gar, _, ai = cg.partition("|")
        # stretch-aligned rows (the default) or 1fr auto-rows both make an
        # opened .card-detail resize the SIBLING cards — the §13.4 violation.
        if ai.strip() not in ("start", "flex-start") or "fr" in gar:
            out.append(("FAIL", "card grid (§12.14): %s sits in a grid with "
                        "grid-auto-rows:%s / align-items:%s — an opened card "
                        "stretches its siblings; use .canvas-grid--cards"
                        % (r["sel"], gar.strip() or "auto", ai.strip() or "stretch")))
            break  # one finding per slide is enough

    # ---- §10.1 semantic colour sanity (v4) — orange minus without .stat--pos ----
    for t in text_leaves:
        txt = (t.get("text") or "").lstrip()
        if not txt or txt[0] not in "-−–":
            continue
        col = (t.get("color") or "").replace(" ", "")
        if col in ("rgb(255,120,0)", "rgb(217,78,14)") \
                and "stat--pos" not in _geo_classes(t["sel"]):
            out.append(("WARN", "data semantics (§10.1): negative-looking numeral "
                        "%s is orange without a declared .stat--pos — if the "
                        "decline is a win, declare it; otherwise it takes Navy"
                        % _geo_fmt(t)))

    # ---- text x text overlap (different components) -> FAIL ----
    for i in range(len(text_leaves)):
        for j in range(i + 1, len(text_leaves)):
            a, b = text_leaves[i], text_leaves[j]
            if _geo_is_ancestor(by_i, a, b) or _geo_is_ancestor(by_i, b, a):
                continue
            ax, ay, aw, ah = _geo_trect(a)
            bx, by, bw, bh = _geo_trect(b)
            ox, oy = _geo_ix(ax, ay, aw, ah, bx, by, bw, bh)
            if ox > 4 and oy > 4:
                out.append(("FAIL", "text x text: %s x %s (ix %.0fx%.0fpx)"
                            % (_geo_fmt(a), _geo_fmt(b), ox, oy)))

    # ---- decor covering >30% of a text rect -> FAIL ----
    decos = [r for r in rs if r["decor"] or
             (not r["hasText"] and r["sel"].split(".")[0] in ("img", "svg"))]
    for t in text_leaves:
        tx, ty, tw, th = _geo_trect(t)
        for d in decos:
            if d["i"] == t["i"]:
                continue
            if _geo_is_ancestor(by_i, d, t) or _geo_is_ancestor(by_i, t, d):
                continue
            if d["w"] >= 1900 and d["h"] >= 1060:
                continue  # full-bleed background art: text-over-art by design
            ox, oy = _geo_ix(tx, ty, tw, th, d["x"], d["y"], d["w"], d["h"])
            if ox > 0 and oy > 0 and tw * th > 0:
                cover = (ox * oy) / (tw * th)
                if cover > 0.30:
                    detail = ("decor %s [%g,%g %gx%g] covers %.0f%% of %s"
                              % (d["sel"], d["x"], d["y"], d["w"], d["h"],
                                 cover * 100, _geo_fmt(t)))
                    if d.get("safe"):
                        out.append(("WARN", detail + ' — data-text-safe="true" '
                                    "declared; art pass must re-check by eye"))
                    else:
                        out.append(("FAIL", detail))

    if not locked:
        # ---- safe area (glyph rects) -> FAIL ----
        # The safe area is the content edge with 8px of glyph tolerance, derived
        # from THIS deck's --m-edge. It was written as a literal 72/1848 pair,
        # which is edge 80 minus/plus that tolerance — the fifth place the edge
        # constant lived. Moving the frame to 40 made every correct headline a
        # FAIL until this followed it.
        safe_l = edge - 8
        safe_r = (1920 - edge) + 8
        for t in text_leaves:
            tx, ty, tw, th = _geo_trect(t)
            probs = []
            if tx < safe_l:
                probs.append("x=%g < %g" % (tx, safe_l))
            if tx + tw > safe_r:
                probs.append("right=%g > %g" % (tx + tw, safe_r))
            if ty < 20:
                probs.append("y=%g < 20" % ty)
            if probs:
                out.append(("FAIL", "outside safe area: %s: %s"
                            % (_geo_fmt(t), "; ".join(probs))))

        # ---- footer band intrusion (y>985, non-furniture) -> FAIL ----
        for t in text_leaves:
            tx, ty, tw, th = _geo_trect(t)
            if ty + th > 985 and ty < 1080:
                out.append(("FAIL", "footer band: %s extends to y=%g (>985)"
                            % (_geo_fmt(t), ty + th)))

        # ---- §15.9.1 content-edge conformance (v4) -> WARN ----
        # Skip slides whose left half is structurally owned by a panel/bleed.
        left_owned = any(
            ("panel--left" in _geo_classes(r["sel"]))
            or ("media--bleed-l" in _geo_classes(r["sel"]))
            or (r["pos"] and r["x"] <= 2 and r["w"] >= 700)
            for r in rs)
        if not left_owned:
            for t in text_leaves:
                if "headline" not in _geo_classes(t["sel"]):
                    continue
                tx = _geo_trect(t)[0]
                # Read the edge off the deck rather than restating it. This
                # check hardcoded 80 while the shell moved to 40, which would
                # have warned on every correctly-built slide.
                if abs(tx - edge) > 6:
                    out.append(("WARN", "content edge (§15.9): headline starts at "
                                "x=%g — this deck's content edge is x=%g" % (tx, edge)))
                break

        # ---- §15.9.2 media anchoring (v4) -> FAIL ----
        # A media rect >= 200x200 must bleed to a canvas edge / sit in a corner,
        # unless declared inset (data-inset-ok, .screenshot) or exempt by role.
        for r in rs:
            cls = _geo_classes(r["sel"])
            base = r["sel"].split(".")[0]
            anc = _geo_anc_classes(by_i, r)
            is_host = bool(cls & _MEDIA_HOSTS)
            is_img = base == "img" and not (anc & (_MEDIA_HOSTS | _MEDIA_EXEMPT))
            if not (is_host or is_img):
                continue
            if r.get("insetok") or (cls & _MEDIA_EXEMPT) or (anc & _MEDIA_EXEMPT):
                continue
            if r["w"] < MEDIA_MIN or r["h"] < MEDIA_MIN:
                continue
            touches = (r["x"] <= 2 or r["y"] <= 2
                       or r["x"] + r["w"] >= 1918 or r["y"] + r["h"] >= 1078)
            if not touches:
                out.append(("FAIL", "media anchoring (§15.9): %s [%g,%g %gx%g] "
                            "floats inside the margins on all four sides — "
                            "bleed it to an edge, corner it, or declare "
                            "data-inset-ok" % (r["sel"], r["x"], r["y"],
                                               r["w"], r["h"])))

    # ---- grid drift (sibling groups, same selector, count>=2) -> WARN ----
    groups = {}
    for r in rs:
        if r["decor"]:
            continue  # scattered decorative dots/motifs are not a grid
        groups.setdefault((r["parent"], r["sel"]), []).append(r)
    for (_parent, sel), g in groups.items():
        if len(g) < 2:
            continue
        xs = sorted(g, key=lambda r: (r["x"], r["y"]))
        horiz = all(xs[k]["x"] + xs[k]["w"] <= xs[k + 1]["x"] + 8
                    for k in range(len(xs) - 1))
        if horiz:
            tops = [r["y"] for r in xs]
            mids = [r["y"] + r["h"] / 2 for r in xs]
            bots = [r["y"] + r["h"] for r in xs]
            # two clean lanes (alternating timeline above/below) is a
            # deliberate pattern; >2 clusters on every edge = drift
            if not (_geo_aligned(tops, 6) or _geo_aligned(mids, 6)
                    or _geo_aligned(bots, 6)
                    or min(_geo_clusters(tops, 6), _geo_clusters(mids, 6),
                           _geo_clusters(bots, 6)) <= 2):
                out.append(("WARN",
                            "off-grid: %d x %s no common horizontal alignment "
                            "(tops: %s | mids: %s)"
                            % (len(g), sel, ", ".join("%g" % v for v in tops),
                               ", ".join("%g" % v for v in mids))))
            gaps = [xs[k + 1]["x"] - (xs[k]["x"] + xs[k]["w"])
                    for k in range(len(xs) - 1)]
            if len(gaps) >= 2 and max(gaps) - min(gaps) > 8:
                out.append(("WARN", "off-grid: %d x %s gaps uneven (%s)"
                            % (len(g), sel, ", ".join("%.0f" % v for v in gaps))))
        else:
            ys = sorted(g, key=lambda r: (r["y"], r["x"]))
            vert = all(ys[k]["y"] + ys[k]["h"] <= ys[k + 1]["y"] + 8
                       for k in range(len(ys) - 1))
            if vert:
                lefts = [r["x"] for r in ys]
                mids = [r["x"] + r["w"] / 2 for r in ys]
                rights = [r["x"] + r["w"] for r in ys]
                if not (_geo_aligned(lefts, 6) or _geo_aligned(mids, 6)
                        or _geo_aligned(rights, 6)):
                    out.append(("WARN",
                                "off-grid: %d x %s no common vertical alignment "
                                "(lefts: %s)"
                                % (len(g), sel, ", ".join("%g" % v for v in lefts))))
                gaps = [ys[k + 1]["y"] - (ys[k]["y"] + ys[k]["h"])
                        for k in range(len(ys) - 1)]
                if len(gaps) >= 2 and max(gaps) - min(gaps) > 8:
                    out.append(("WARN", "off-grid: %d x %s v-gaps uneven (%s)"
                                % (len(g), sel,
                                   ", ".join("%.0f" % v for v in gaps))))
    return out


def check_geometry(deck_path, slides, shots):
    """§15 layout laws — mechanical geometry pass over every captured slide.
    Runs the Chrome probe ONCE for the whole deck; returns
    {slide_number: [probe records]} so check_furniture_contrast can reuse the
    same JSON (None when the probe failed)."""
    try:
        edge = _content_edge(open(deck_path, encoding="utf-8", errors="replace").read())
    except OSError:
        edge = 40.0
    recs, err = _geo_capture(deck_path)
    if recs is None:
        report("WARN", "geometry", f"probe failed — {err}; §15 laws not checked this run")
        return None
    order, groups = [], {}
    for r in recs:                       # records arrive in document order
        if r["slide"] not in groups:
            order.append(r["slide"])
            groups[r["slide"]] = []
        groups[r["slide"]].append(r)
    id2num = {slide_id(s): n for n, s in enumerate(slides, 1) if slide_id(s)}
    geo = {id2num.get(key, pos): groups[key] for pos, key in enumerate(order, 1)}

    clean, checked = [], 0
    for n in sorted(shots):
        rs = geo.get(n)
        if not rs:
            continue
        checked += 1
        sid = (slide_id(slides[n - 1]) if n <= len(slides) else None) or rs[0]["slide"]
        vios = _geo_violations(rs, _locked_slide(sid), edge)
        for status, detail in vios:
            report(status, f"geometry s{n} ({sid})", detail)
        if not vios:
            clean.append(f"s{n}")
    if clean:
        report("PASS", "geometry", ", ".join(clean) + " clean "
               f"({checked} slide(s) checked against the §15 laws)")
    elif checked:
        print(f"NOTE geometry — every one of the {checked} checked slide(s) "
              "has findings above")
    else:
        print("SKIP geometry — no captured slides to check")
    return geo


def _parse_rgb(s):
    """'rgb(250, 250, 240)' / 'rgba(...)' -> (r, g, b), else None."""
    nums = re.findall(r"-?\d+(?:\.\d+)?", s or "")
    if len(nums) >= 3:
        return tuple(min(255, max(0, int(float(v)))) for v in nums[:3])
    return None


def _rel_lum(rgb):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _wcag(c1, c2):
    l1, l2 = _rel_lum(c1), _rel_lum(c2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def _median_rgb(pixels):
    n = len(pixels)
    return tuple(sorted(p[c] for p in pixels)[n // 2] for c in range(3))


def check_furniture_contrast(slides, shots, geo):
    """Furniture legibility — for each captured slide, sample the screenshot
    inside each furniture glyph rect (.footer-brand/.pageno/.confidential/
    .source from the geometry JSON), take the median colour of the pixels far
    from the computed text colour (the background under the glyphs — falls
    back to all pixels when nearly everything is text-coloured, i.e. text on
    a same-colour surface), and check the WCAG ratio against the computed
    text colour. Catches cream-on-cream furniture over decorative circles."""
    if not geo:
        print("SKIP furniture contrast — no geometry data (probe failed or "
              "nothing captured)")
        return
    try:
        from PIL import Image
    except ImportError:
        print("SKIP furniture contrast — Pillow not installed (pip install "
              "pillow); furniture legibility unmeasured")
        return
    ok, bad, slides_seen = 0, 0, set()
    for n in sorted(shots):
        rs = geo.get(n)
        if not rs:
            continue
        furn = [r for r in rs if (_geo_classes(r["sel"]) & FURNITURE)
                and r["hasText"] and "tx" in r]
        if not furn:
            continue
        sid = (slide_id(slides[n - 1]) if n <= len(slides) else None) or rs[0]["slide"]
        img = Image.open(shots[n]).convert("RGB")
        scale = img.size[0] / 1920.0
        for r in furn:
            if r["tw"] < 8 or r["th"] < 4:
                continue                       # too small to sample honestly
            fg = _parse_rgb(r["color"])
            if not fg:
                continue
            box = (max(0, int(r["tx"] * scale)),
                   max(0, int(r["ty"] * scale)),
                   min(img.size[0], int((r["tx"] + r["tw"]) * scale) + 1),
                   min(img.size[1], int((r["ty"] + r["th"]) * scale) + 1))
            if box[2] - box[0] < 2 or box[3] - box[1] < 2:
                continue
            px = list(img.crop(box).getdata())
            far = [p for p in px
                   if (p[0] - fg[0]) ** 2 + (p[1] - fg[1]) ** 2
                   + (p[2] - fg[2]) ** 2 > 60 ** 2]
            bg = _median_rgb(far if len(far) >= max(8, len(px) // 4) else px)
            ratio = _wcag(fg, bg)
            slides_seen.add(n)
            if ratio >= CONTRAST_WARN:
                ok += 1
                continue
            bad += 1
            report("FAIL" if ratio < CONTRAST_FAIL else "WARN",
                   f"furniture-contrast s{n} ({sid})",
                   "%s '%s' colour rgb%s on sampled bg rgb%s — ratio %.2f:1 "
                   "(min %.1f) — furniture must stay legible over decor"
                   % (r["sel"], r["text"], fg, bg, ratio, CONTRAST_WARN))
    if ok:
        report("PASS", "furniture contrast",
               f"{ok} furniture element(s) across {len(slides_seen)} slide(s) "
               f"at >= {CONTRAST_WARN}:1" + (f" ({bad} flagged above)" if bad else ""))
    elif not slides_seen:
        print("SKIP furniture contrast — no furniture glyph rects big enough "
              "to sample on the captured slides")


# --- main --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Verify a WPP ES | MAP deck .html.")
    ap.add_argument("deck", help="Path to the deck .html file.")
    ap.add_argument("--demo", action="store_true",
                    help="Allow the demo-deck banner (development only).")
    ap.add_argument("--screenshots", metavar="DIR",
                    help="Render every slide with headless Chrome into DIR, check "
                         "them, and run the composition tripwire.")
    ap.add_argument("--quick", action="store_true",
                    help="With --screenshots: old fast subset (all slides when "
                         "<=12, else just 1, 2 and the last).")
    ap.add_argument("--slides", metavar="N,N,...",
                    help="With --screenshots: shoot only these slide numbers "
                         "(e.g. 4,7,9) — art-direction re-shoot loop. "
                         "Overrides --quick.")
    ap.add_argument("--contact-sheet", metavar="PNG", nargs="?", const="",
                    help="With --screenshots: also tile every captured slide into "
                         "ONE image (default DIR/contact-sheet.png). Read this for "
                         "the art-direction rhythm pass instead of every slide; "
                         "slides the verifier flagged are outlined and must still "
                         "be read at full resolution.")
    ap.add_argument("--max-size-mb", type=float, default=5,
                    help="Max total file size in MB (default 5).")
    args = ap.parse_args()

    only = None
    if args.slides:
        if not args.screenshots:
            ap.error("--slides requires --screenshots DIR")
        try:
            only = sorted({int(x) for x in args.slides.split(",") if x.strip()})
        except ValueError:
            ap.error(f"--slides wants comma-separated slide numbers, got {args.slides!r}")
        if not only:
            ap.error("--slides given but no slide numbers in it")

    try:
        with open(args.deck, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"FAIL read — {e}")
        sys.exit(1)

    slides = parse_slides(text)

    check_self_contained(text)
    check_banned(text, args.demo)
    check_structure(text, slides)
    check_cover_title(text)
    check_brand(text)
    check_palette(text, slides)
    check_sizes(args.deck, text, args.max_size_mb)
    check_notes(text)
    check_motif_templates(text)
    check_motif_routing(text)
    check_duplicate_payloads(text)
    check_photography(slides)
    check_rhythm(slides)
    if args.screenshots:
        shots = check_screenshots(args.deck, len(slides), args.screenshots,
                                  quick=args.quick, only=only)
        check_composition(slides, shots)
        geo = check_geometry(args.deck, slides, shots)
        check_furniture_contrast(slides, shots, geo)
        # built last, so it can outline whatever the checks above flagged
        if args.contact_sheet is not None:
            out = args.contact_sheet or os.path.join(args.screenshots, "contact-sheet.png")
            build_contact_sheet(shots, len(slides), out, flagged=flagged_slides())

    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
