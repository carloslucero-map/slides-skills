#!/usr/bin/env python3
"""
measure.py — pull one source slide's geometry out of the PPTX inventory.

The measuring tape for the canon. Every template in canon/ is built against a
real slide, and this is what says where that slide's parts actually are —
instead of a human retyping a layout by eye, which is the error that produced
the current kit.

The inventory is NOT in this repo: it is derived from the 640 MB source deck and
lives beside it. Point --inventory at it, or set WPP_DECK_INVENTORY.

  python3 canon/_tools/measure.py 86 --out canon/enum-numbered-4/measure.json

Two things this deliberately does NOT do:

  It does not average across "sibling" slides. Slides 86 and 103 are the same
  family, form and near-arity, and compositionally opposite — 86 runs a 192px
  numeral over a left-aligned headline, 103 uses a 32px numeral as a label under
  a centred one. A median of the two matches neither and averages the focal
  element away. One slide, one measurement.

  It does not emit CSS. Geometry here is evidence about the source, not the
  template's implementation. The template consumes shell tokens; where the
  source needs something the tokens cannot express, that is a contract gap and
  the shell gets a new token (see .slide--ground in build_shell.py).
"""
import argparse, json, os, sys

# 12192000 EMU / 1920 px = 6350 EMU/px; 13.333in = 960pt over 1920px, so the
# pt -> px factor for this canvas is exactly 2.0. CORE.md said 1.5, which is
# why every type and spacing translation ran 25% short.
PT_TO_PX = 2.0
CANVAS = (1920, 1080)

DEFAULT_INVENTORY = os.environ.get(
    "WPP_DECK_INVENTORY",
    os.path.expanduser("~/Desktop/slides_map/_audit/inventory2.json"))


def measure(inv_path, n):
    with open(inv_path, encoding="utf-8") as f:
        inv = json.load(f)
    slide = next((s for s in inv["slides"] if s["n"] == n), None)
    if slide is None:
        sys.exit(f"slide {n} not in {inv_path}")

    shapes, offstage = [], 0
    for sh in slide["shapes"]:
        x, y, w, h = sh["box"]
        if x >= CANVAS[0] or y >= CANVAS[1]:
            offstage += 1          # PowerPoint scratch space beside the canvas
            continue
        runs = sh.get("p") or []
        sizes = sorted({p["sz"] for p in runs if p.get("sz")})
        text = " ".join((p.get("t") or "") for p in runs).strip()
        shapes.append({
            "kind": sh["k"],
            "name": sh.get("nm"),
            "box": [x, y, w, h],
            "right": x + w,
            "bottom": y + h,
            "placeholder": sh.get("ph"),
            "geom": sh.get("g"),
            "rot": sh.get("rot") or 0,
            "pt": sizes,
            "px": [round(s * PT_TO_PX) for s in sizes],
            "chars": len(text),
            "text": text[:180],
        })

    xs = sorted({s["box"][0] for s in shapes})
    ys = sorted({s["box"][1] for s in shapes})
    return {
        "source": f"bank:{n}",
        "inventory": os.path.basename(inv_path),
        "canvas": list(CANVAS),
        "ptToPx": PT_TO_PX,
        "shapeCount": len(shapes),
        "offstageDropped": offstage,
        "leftEdges": xs,
        "topEdges": ys,
        "typePx": sorted({p for s in shapes for p in s["px"]}),
        "shapes": shapes,
        "_note": "Evidence about the source slide. Not CSS, not a spec, "
                 "never averaged with another slide.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slide", type=int, help="source slide number in the bank")
    ap.add_argument("--inventory", default=DEFAULT_INVENTORY)
    ap.add_argument("--out", help="write JSON here (default: stdout)")
    args = ap.parse_args()

    if not os.path.isfile(args.inventory):
        sys.exit(f"no inventory at {args.inventory}\n"
                 f"Pass --inventory or set WPP_DECK_INVENTORY. It is generated "
                 f"from the source deck and is not committed here.")

    rec = measure(args.inventory, args.slide)
    text = json.dumps(rec, indent=1, ensure_ascii=False)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"slide {args.slide}: {rec['shapeCount']} shapes on canvas"
              + (f", {rec['offstageDropped']} offstage dropped" if rec["offstageDropped"] else "")
              + f"\nleft edges: {rec['leftEdges']}"
              + f"\ntype (px):  {rec['typePx']}"
              + f"\n-> {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
