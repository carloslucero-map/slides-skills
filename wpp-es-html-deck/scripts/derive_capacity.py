#!/usr/bin/env python3
"""
derive_capacity.py — WPP ES | MAP HTML Deck Builder

Derives per-template text capacity (min / ideal / max) for every kit layout in
assets/snippets/variants/, one file per layout, and writes:

  1. references/capacity.json     — machine-readable catalogue
  2. an inline <!-- capacity: --> block above each variant's <section class="slide">
  3. references/SNIPPET-INDEX.md  — one line per layout (--index)

The <section> itself is the design system's: authoring/refresh_design_system.py
copies it into the variant, and this script never touches it.

Capacity is MEASURED, never invented. Three independent sources:

  A. The layout's own example copy. Each is a calibrated §12.15 recipe that
     already passes the composition laws, so its measured length IS the ideal.
  B. Geometry. chars-per-line = container_width / (font_size * char_width_em),
     read from the shell CSS; lines capped per class by the guideline.
  C. The master-PPT empirical distribution (optional --ppt-stats), used to
     sanity-check the ceiling against slides that shipped.

The tightest of the three wins for `max`. Nothing here touches build_shell.py
or verify_deck.py — this script only reads the variants and writes comments.

Usage:
  python3 derive_capacity.py --skill /path/to/wpp-es-html-deck --demo <deck>.html [--write] [--index] [--ppt-stats stats.json]
"""

import argparse, json, os, re, sys
from html.parser import HTMLParser

# ─────────────────────────────────────────────────────────────────────────────
# Canvas + layout constants (guideline §2 / §15.1)
# ─────────────────────────────────────────────────────────────────────────────
CANVAS_W, CANVAS_H = 1920, 1080
# §15.1 text glyph bounds. These are READ FROM THE SHELL, not stated here — the
# content edge lived in four places (build_shell's --m-edge, CORE §2,
# verify_deck's §15.9 check and this file) and moving it in one silently left
# the other three behind. Widening the frame from 80 to 40 changed nothing in
# capacity.json until this stopped being a literal.
CANVAS_W = 1920
CONTENT_X0, CONTENT_X1 = 80, 1840          # fallback only; overwritten by read_frame()
CONTENT_W = CONTENT_X1 - CONTENT_X0


def read_frame(demo_html):
    """--m-edge out of the generated shell -> (x0, x1, width)."""
    if not os.path.exists(demo_html):
        return CONTENT_X0, CONTENT_X1, CONTENT_W
    html = open(demo_html, encoding="utf-8", errors="replace").read()
    m = re.search(r"--m-edge:\s*(\d+(?:\.\d+)?)px", html)
    if not m:
        return CONTENT_X0, CONTENT_X1, CONTENT_W
    edge = float(m.group(1))
    return edge, CANVAS_W - edge, CANVAS_W - 2 * edge
FOOTER_Y = 985                             # §15.1 footer band
GRID_TOP = 260                             # the columns variants: grid sits at y=260
COL_GAP = 64

# Average glyph advance as a fraction of font-size, for a grotesque like
# WPP Sans. Mixed case ≈ .50 em; ALL CAPS runs wider.
EM_MIXED, EM_CAPS = 0.50, 0.60

# Per-class line ceilings. Sources noted; these are hard stops, not guesses.
LINE_CAP = {
    "headline":    2,    # §4.5 "sentence-case headlines, max two lines"
    "subtitle":    1,    # locked eyebrow at y=132
    "col-sub":     1,
    "body":        4,    # the columns family notes: "2-4 short lines per column"
    "takeaway":    2,
    "tbx":         4,
    "bio":         4,
    "nm":          1,
    "pill":        1,
    "cell":        3,
    "card":        4,
    "source":      1,
    "ruler-label": 1,
    "kpi":         1,
    "stat":        1,
    "hero-num":    1,
    "milestone":   2,
    "orbit-node":  2,
}

# Classes rendered in caps (wider glyphs)
CAPS_CLASSES = {"subtitle", "pill", "ruler-label", "eyebrow"}

# Classes that are furniture, not author-supplied content — skip them.
SKIP_CLASSES = {
    "slide", "pageno", "footer-brand", "lift", "motif", "notes",
    "content-band", "cols", "dot", "col-dot", "arrow", "stem", "vrule",
    "orbit", "confidential", "ph", "ph-init",
}

# Countable item classes: how many repeats the layout expects.
ITEM_CLASSES = {
    "col-sub", "body", "pill", "cell", "tbx", "card", "kpi", "stat",
    "person", "milestone", "orbit-node", "bio", "nm",
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS metrics
# ─────────────────────────────────────────────────────────────────────────────
def read_css_metrics(demo_html):
    """Pull font-size / line-height / width per class from the generated shell."""
    if not os.path.exists(demo_html):
        return {}
    html = open(demo_html, encoding="utf-8", errors="replace").read()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    out = {}
    for m in re.finditer(r"([^{}]+)\{([^}]*)\}", css):
        sel, blk = m.group(1), m.group(2)
        sel = sel.split(",")[-1].strip()          # last selector in a group
        classes = re.findall(r"\.([a-z0-9_-]+)", sel)
        if not classes:
            continue
        cls = classes[-1]                          # subject of the selector
        fs = re.search(r"font-size:\s*(\d+(?:\.\d+)?)px", blk)
        lh = re.search(r"line-height:\s*([\d.]+)", blk)
        wd = re.search(r"(?:^|;)\s*(?:max-)?width:\s*(\d+(?:\.\d+)?)px", blk)
        if not (fs or wd):
            continue
        e = out.setdefault(cls, {"font_px": None, "line_height": 1.3, "width_px": None})
        if fs and e["font_px"] is None:
            e["font_px"] = float(fs.group(1))
        if lh and e["line_height"] == 1.3:
            e["line_height"] = float(lh.group(1))
        if wd and e["width_px"] is None:
            e["width_px"] = float(wd.group(1))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Snippet parsing
# ─────────────────────────────────────────────────────────────────────────────
class SlotExtractor(HTMLParser):
    """Collect direct text per element carrying a known slot class."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # (classes, depth)
        self.slots = []      # (class, text)
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        d = dict(attrs)
        classes = (d.get("class") or "").split()
        keep = [c for c in classes if c not in SKIP_CLASSES]
        if keep:
            self.stack.append({"cls": keep, "depth": self.depth, "text": []})

    def handle_endtag(self, tag):
        while self.stack and self.stack[-1]["depth"] >= self.depth:
            e = self.stack.pop()
            txt = re.sub(r"\s+", " ", "".join(e["text"])).strip()
            if txt:
                for c in e["cls"]:
                    self.slots.append((c, txt))
        self.depth -= 1

    def handle_data(self, data):
        if self.stack:
            self.stack[-1]["text"].append(data)


def split_templates(path):
    """Split a snippet file into (label, archetype, html) per <section class="slide">."""
    src = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r'<section class="slide[^"]*"[^>]*>', src):
        start = m.start()
        # nearest preceding comment = the variant label
        pre = src[:start]
        cm = None
        for c in re.finditer(r"<!--(.*?)-->", pre, re.S):
            # skip our own injected capacity blocks — they sit between the
            # variant comment and the <section>, and would shadow the label
            if c.group(1).lstrip().startswith("capacity:"):
                continue
            cm = c
        label = "—"
        if cm:
            first = cm.group(1).strip().splitlines()[0].strip()
            if re.match(r"^(V\d|Variant)", first):
                label = re.sub(r"\s+", " ", first)[:90]
        arch = re.search(r'data-archetype="([^"]+)"', m.group(0))
        end = src.find("</section>", start)
        end = end + len("</section>") if end != -1 else len(src)
        out.append({
            "label": label,
            "archetype": arch.group(1) if arch else "unknown",
            "html": src[start:end],
            "offset": start,
        })
    return src, out


# ─────────────────────────────────────────────────────────────────────────────
# Capacity maths
# ─────────────────────────────────────────────────────────────────────────────
def container_width(cls, n_items, css):
    """Resolve the pixel width one instance of this slot gets."""
    meta = css.get(cls) or {}
    if meta.get("width_px"):
        base = meta["width_px"]
    else:
        base = CONTENT_W
    if n_items > 1 and cls in ITEM_CLASSES:
        base = (CONTENT_W - (n_items - 1) * COL_GAP) / n_items
    return max(base, 120.0)


def geometric_max(cls, n_items, css):
    meta = css.get(cls) or {}
    fpx = meta.get("font_px")
    if not fpx:
        return None
    em = EM_CAPS if cls in CAPS_CLASSES else EM_MIXED
    cpl = container_width(cls, n_items, css) / (fpx * em)
    lines = LINE_CAP.get(cls, 3)
    return int(cpl * lines)


def derive(measured, geo, ppt_p90=None):
    """Blend the three sources. Tightest ceiling wins."""
    ideal = measured
    caps = [c for c in (geo, ppt_p90) if c]
    if caps:
        # geometry IS the constraint — the snippet example may simply be short
        mx = max(int(measured * 1.15), min(caps))
    else:
        mx = int(measured * 1.4)
    # FIX 3 — min can never exceed ideal, and never collapse onto max
    mn = min(max(4, int(measured * 0.45)), ideal)
    if mx <= ideal:
        mx = max(ideal + 1, int(ideal * 1.15))
    return mn, ideal, mx


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True)
    ap.add_argument("--demo", default="build/demo.html",
                    help="a generated deck, used to read the shell CSS metrics")
    ap.add_argument("--ppt-stats", default=None,
                    help="optional JSON of empirical p90 char counts per slot")
    ap.add_argument("--write", action="store_true",
                    help="write each variant's <!-- capacity --> block")
    ap.add_argument("--index", action="store_true",
                    help="write references/SNIPPET-INDEX.md")
    args = ap.parse_args()

    # A missing --demo used to degrade in SILENCE: read_css_metrics returned {}
    # and read_frame fell back to the 80px literal, so every limit in
    # capacity.json was derived from constants that had not been true since the
    # frame moved to 40px. The default even pointed at /home/claude/demo.html, a
    # path from another machine. Silence is the wrong failure mode for a tool
    # whose whole job is to be the measurement.
    if not os.path.exists(args.demo):
        sys.exit(f"--demo {args.demo!r} does not exist.\n"
                 f"Without a generated shell this reads NO CSS metrics and falls "
                 f"back to a stale content edge, and every number it writes is "
                 f"wrong but plausible. Build one first:\n"
                 f"  python3 scripts/build_shell.py --out /tmp/demo.html\n"
                 f"  python3 scripts/derive_capacity.py --skill . --demo /tmp/demo.html --write")
    css = read_css_metrics(args.demo)
    global CONTENT_X0, CONTENT_X1, CONTENT_W
    CONTENT_X0, CONTENT_X1, CONTENT_W = read_frame(args.demo)
    print(f"frame read from shell: content edge x={CONTENT_X0:g}, width {CONTENT_W:g}px")
    print(f"CSS metrics read for {len(css)} classes")

    ppt = {}
    if args.ppt_stats and os.path.exists(args.ppt_stats):
        ppt = json.load(open(args.ppt_stats))

    vdir = os.path.join(args.skill, "assets", "snippets", "variants")
    catalogue, total = [], 0

    for fn in sorted(os.listdir(vdir)):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(vdir, fn)
        src, tpls = split_templates(path)
        if len(tpls) != 1:
            sys.exit(f"variants/{fn}: expected one <section class=\"slide\">, found {len(tpls)}")
        inserts = []

        for t in tpls:
            if t["label"] == "—":
                t["label"] = block_label(src)
            p = SlotExtractor()
            p.feed(t["html"])
            try:
                p.close()
            except Exception:
                pass

            grouped = {}
            for cls, txt in p.slots:
                grouped.setdefault(cls, []).append(txt)

            slots = {}
            for cls, texts in sorted(grouped.items()):
                if cls in SKIP_CLASSES or not texts:
                    continue
                n = len(texts)
                measured = int(sum(len(x) for x in texts) / n)
                if measured < 3:
                    continue
                geo = geometric_max(cls, n, css)
                mn, ideal, mx = derive(measured, geo, ppt.get(cls))
                slots[cls] = {
                    "items": n,
                    "min_chars": mn,
                    "ideal_chars": ideal,
                    "max_chars": mx,
                    "font_px": (css.get(cls) or {}).get("font_px"),
                    "basis": "geometry" if geo and geo < measured * 1.8 else "measured",
                }

            slide_total = sum(s["ideal_chars"] * s["items"] for s in slots.values())
            entry = {
                "file": f"variants/{fn}",
                "archetype": t["archetype"],
                "label": t["label"],
                "slots": slots,
                "slide_ideal_chars": slide_total,
                "slide_max_chars": int(slide_total * 1.35),   # practical ceiling, not sum-of-maxes
            }
            catalogue.append(entry)
            total += 1

            # build the inline block
            lines = [f'<!-- capacity: {t["archetype"]} — {t["label"]}']
            for cls, s in slots.items():
                it = f'×{s["items"]}' if s["items"] > 1 else "  "
                fp = f'{int(s["font_px"])}px' if s["font_px"] else "—"
                lines.append(
                    f'     .{cls:<14}{it}  {s["min_chars"]:>4}–{s["max_chars"]:<4} chars'
                    f'  (ideal {s["ideal_chars"]}, {fp})'
                )
            lines.append(f'     SLIDE TOTAL      ideal {slide_total} · max {entry["slide_max_chars"]} chars')
            lines.append("     Over max: pick a lower-density variant, do not shrink type (§4.5). -->")
            inserts.append((t["offset"], "\n".join(lines) + "\n"))

        if args.write and inserts:
            out = src
            for off, block in sorted(inserts, reverse=True):
                out = out[:off] + block + out[off:]
            # Insertion alone only ever ADDED. Every --write run stacked one more
            # block on each section and none of the stale ones were removed, so
            # the snippets carried several contradictory measurements at once and
            # a reader had no way to tell which was current. Collapse each run to
            # the block just written — it sits closest to its <section>.
            out = _collapse_capacity(out)
            open(path, "w", encoding="utf-8").write(out)

    refs = os.path.join(args.skill, "references")
    os.makedirs(refs, exist_ok=True)
    with open(os.path.join(refs, "capacity.json"), "w", encoding="utf-8") as f:
        json.dump({"canvas": [CANVAS_W, CANVAS_H], "templates": catalogue}, f, indent=1)

    print(f"{total} templates measured -> references/capacity.json")
    if args.write:
        print("capacity blocks written into the variants")

    if args.index:
        write_index(args.skill, catalogue)
    return catalogue


def block_label(src):
    """The label the last run wrote into the variant's capacity block.

    A variant holds no label comment of its own: the kit's authoring sources did,
    and they are gone (their notes are in authoring/kit-notes.md). The label
    survives on the first line of the capacity block, `capacity: <arch> — <label>`,
    and this script writes it back unchanged."""
    m = re.search(r"<!--\s*capacity:\s*\S+ — (.*)", src)
    return m.group(1) if m else "—"          # verbatim: a label cut at 90 can end in a space


def _collapse_capacity(text):
    """Keep only the LAST capacity block in any run sitting above a <section>."""
    run = re.compile(r'(?:<!--\s*capacity:.*?-->\n)+(?=<section\b)', re.S)
    one = re.compile(r'<!--\s*capacity:.*?-->\n', re.S)
    return run.sub(lambda m: one.findall(m.group(0))[-1], text)


def _short(label):
    """'Variant 3 · IMAGE-TOP CARDS - 3 cards with photo…' -> ('V3', 'image-top cards…')"""
    m = re.match(r"(?:Variant|V)\s*(\d+)\s*[·—\-]?\s*(.*)", label)
    if not m:
        return "", label[:60]
    desc = re.sub(r"\s*\(.*?\)\s*", " ", m.group(2)).strip(" -—·")
    return f"V{m.group(1)}", desc[:64]


def write_index(skill, catalogue):
    """SNIPPET-INDEX.md — one line per layout, so the model picks a variant
    without opening files to find out what is in them. Opening one 1.5 KB
    variant beats opening every file to use a tenth of it."""
    lines = [
        f"# Snippet index — {len(catalogue)} templates, one line each",
        "",
        "Generated by `scripts/derive_capacity.py --index`. Do not hand-edit.",
        "",
        "Pick from this table, then open ONLY the file named. `chars` is the",
        "slide's ideal total; the per-slot min-max lives in the `<!-- capacity -->`",
        "block above each template.",
        "",
        "Each file in `variants/` is one layout from the design system: its slide is",
        "copied by `authoring/refresh_design_system.py`, its capacity block written",
        "by `scripts/derive_capacity.py`.",
        "",
        "| archetype | open | chars | what it is |",
        "|---|---|---|---|",
    ]
    for e in catalogue:
        vtag, desc = _short(e["label"])
        if not desc or desc == "—":
            # an unlabelled layout keeps a one-line description in its header
            src = open(os.path.join(skill, "assets", "snippets", e["file"]), encoding="utf-8").read()
            hdr = re.search(r"<!--\s*\n?\s*\S+\s*—\s*(.*?)\n", src)
            desc = hdr.group(1).strip()[:64] if hdr else e["archetype"]
        lines.append(
            f'| {e["archetype"]} | `{e["file"]}` | {e["slide_ideal_chars"]} | {desc} |')

    out = os.path.join(skill, "references", "SNIPPET-INDEX.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"references/SNIPPET-INDEX.md written ({os.path.getsize(out):,} B, "
          f"~{os.path.getsize(out)//4:,} tokens)")


if __name__ == "__main__":
    main()
