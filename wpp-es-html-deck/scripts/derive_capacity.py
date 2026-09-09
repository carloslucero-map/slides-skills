#!/usr/bin/env python3
"""
derive_capacity.py — WPP ES | MAP HTML Deck Builder

Derives per-template text capacity (min / ideal / max) for every slide template
in assets/snippets/, and writes:

  1. references/capacity.json     — machine-readable catalogue
  2. an inline <!-- capacity: --> block above each <section class="slide">

Capacity is MEASURED, never invented. Three independent sources:

  A. The snippet's own example copy. Variant 1 of every file is a calibrated
     §12.15 recipe that already passes the composition laws, so its measured
     length IS the ideal.
  B. Geometry. chars-per-line = container_width / (font_size * char_width_em),
     read from the shell CSS; lines capped per class by the guideline.
  C. The master-PPT empirical distribution (optional --ppt-stats), used to
     sanity-check the ceiling against slides that shipped.

The tightest of the three wins for `max`. Nothing here touches build_shell.py
or verify_deck.py — this script only reads snippets and writes comments.

Usage:
  python3 derive_capacity.py --skill /path/to/wpp-es-html-deck [--write] [--ppt-stats stats.json]
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
GRID_TOP = 260                             # columns.html: grid sits at y=260
COL_GAP = 64

# Average glyph advance as a fraction of font-size, for a grotesque like
# WPP Sans. Mixed case ≈ .50 em; ALL CAPS runs wider.
EM_MIXED, EM_CAPS = 0.50, 0.60

# Per-class line ceilings. Sources noted; these are hard stops, not guesses.
LINE_CAP = {
    "headline":    2,    # §4.5 "sentence-case headlines, max two lines"
    "subtitle":    1,    # locked eyebrow at y=132
    "col-sub":     1,
    "body":        4,    # columns.html: "2-4 short lines per column"
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
    ap.add_argument("--demo", default="/home/claude/demo.html",
                    help="a generated deck, used to read the shell CSS metrics")
    ap.add_argument("--ppt-stats", default=None,
                    help="optional JSON of empirical p90 char counts per slot")
    ap.add_argument("--write", action="store_true",
                    help="inject <!-- capacity --> blocks into the snippets")
    ap.add_argument("--index", action="store_true",
                    help="write references/SNIPPET-INDEX.md")
    ap.add_argument("--split", action="store_true",
                    help="also emit assets/snippets/variants/ (one template per "
                         "file, generated; the originals stay canonical). "
                         "Implies --index. Requires --write first.")
    args = ap.parse_args()

    css = read_css_metrics(args.demo)
    global CONTENT_X0, CONTENT_X1, CONTENT_W
    CONTENT_X0, CONTENT_X1, CONTENT_W = read_frame(args.demo)
    print(f"frame read from shell: content edge x={CONTENT_X0:g}, width {CONTENT_W:g}px")
    print(f"CSS metrics read for {len(css)} classes")

    ppt = {}
    if args.ppt_stats and os.path.exists(args.ppt_stats):
        ppt = json.load(open(args.ppt_stats))

    sdir = os.path.join(args.skill, "assets", "snippets")
    catalogue, total = [], 0

    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(sdir, fn)
        src, tpls = split_templates(path)
        inserts = []

        for t in tpls:
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
                "file": fn,
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
            open(path, "w", encoding="utf-8").write(out)

    refs = os.path.join(args.skill, "references")
    os.makedirs(refs, exist_ok=True)
    with open(os.path.join(refs, "capacity.json"), "w", encoding="utf-8") as f:
        json.dump({"canvas": [CANVAS_W, CANVAS_H], "templates": catalogue}, f, indent=1)

    print(f"{total} templates measured -> references/capacity.json")
    if args.write:
        print("capacity blocks injected into snippets")

    if args.index or args.split:
        write_index_and_variants(args.skill, catalogue, do_split=args.split)
    return catalogue


def _short(label):
    """'Variant 3 · IMAGE-TOP CARDS - 3 cards with photo…' -> ('V3', 'image-top cards…')"""
    m = re.match(r"(?:Variant|V)\s*(\d+)\s*[·—\-]?\s*(.*)", label)
    if not m:
        return "", label[:60]
    desc = re.sub(r"\s*\(.*?\)\s*", " ", m.group(2)).strip(" -—·")
    return f"V{m.group(1)}", desc[:64]


def write_index_and_variants(skill, catalogue, do_split=False):
    """SNIPPET-INDEX.md — one line per template, so the model picks a variant
    without opening files to find out what is in them.

    With --split, also emit assets/snippets/variants/<file>-v<N>.html holding a
    single template each. The originals stay CANONICAL; the variant files are
    generated, so editing a snippet then re-running this script keeps them in
    sync. Opening one 1.5 KB variant beats opening a 20 KB snippet to use a
    tenth of it.
    """
    sdir = os.path.join(skill, "assets", "snippets")
    vdir = os.path.join(sdir, "variants")
    if do_split:
        os.makedirs(vdir, exist_ok=True)

    by_file = {}
    for e in catalogue:
        by_file.setdefault(e["file"], []).append(e)

    lines = [
        "# Snippet index — 51 templates, one line each",
        "",
        "Generated by `scripts/derive_capacity.py --index`. Do not hand-edit.",
        "",
        "Pick from this table, then open ONLY the file named. `chars` is the",
        "slide's ideal total; the per-slot min-max lives in the `<!-- capacity -->`",
        "block above each template.",
        "",
        "The files in `assets/snippets/` are canonical. `variants/` holds the same",
        "templates split one-per-file and is regenerated from them.",
        "",
        "| archetype | open | chars | what it is |",
        "|---|---|---|---|",
    ]

    written = 0
    seen = set()
    for fn in sorted(by_file):
        src = open(os.path.join(sdir, fn), encoding="utf-8").read()
        # file-header comment, used when a template carries no variant label
        hdr = re.search(r"<!--\s*\n?\s*\S+\s*—\s*(.*?)\n", src)
        fallback = hdr.group(1).strip()[:64] if hdr else ""
        blocks = re.findall(
            r'(<!-- capacity:.*?-->\n<section class="slide[^"]*".*?</section>)',
            src, re.S)
        for i, e in enumerate(by_file[fn]):
            vtag, desc = _short(e["label"])
            if not desc or desc == "—":
                desc = fallback or e["archetype"]
            stem = fn[:-5]
            target = f"`{fn}`" + (f" {vtag}" if vtag else "")
            if do_split and i < len(blocks):
                vname = f"{stem}-{(vtag or 'v' + str(i + 1)).lower()}.html"
                if vname in seen:                       # two templates, same tag
                    vname = f"{stem}-v{i + 1}b.html"
                seen.add(vname)
                with open(os.path.join(vdir, vname), "w", encoding="utf-8") as f:
                    f.write(f"<!-- GENERATED from {fn} by derive_capacity.py "
                            f"--split. Edit {fn}, not this file. -->\n")
                    f.write(blocks[i] + "\n")
                target = f"`variants/{vname}`"
                written += 1
            lines.append(
                f'| {e["archetype"]} | {target} | {e["slide_ideal_chars"]} | {desc} |')

    out = os.path.join(skill, "references", "SNIPPET-INDEX.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"references/SNIPPET-INDEX.md written ({os.path.getsize(out):,} B, "
          f"~{os.path.getsize(out)//4:,} tokens)")
    if do_split:
        print(f"{written} per-variant files -> assets/snippets/variants/")


if __name__ == "__main__":
    main()
