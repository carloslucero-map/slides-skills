#!/usr/bin/env python3
"""Brand dot-halftone generator for the wpp-es-html-deck skill (v4).

Mirrors the canonical generator defaults printed in WPP ES Brand Playbook
v0.2 p.33: Min 2.0 / Max 8.0 / Square grid / Spacing 10.0 / Contrast 1.00 /
Jitter 0.00 / Size Variation 0.00. Min/Max are dot DIAMETER bounds in output
pixels on a 10.0px square grid: darkest cell -> max dot, light or transparent
cell -> no dot (the "subject-only, clean background" rule falls out of the
cutoff when the source has a light/transparent ground). Dots are FLAT
single-colour fills — no gradients, no strokes.

Two modes:
  photo mode    halftone.py INPUT [-o BASE] [--fg navy] [--bg none] ...
                samples INPUT on a square grid, emits BASE.svg + BASE.png
  overlay mode  halftone.py --overlay W H [--fg orange-800] [--seed 7] ...
                website-style cluster: 2-4 large flat circles (some fused),
                each bleeding off a canvas edge, plus sparse satellite dots
                that fade toward the centre; deterministic per --seed

PNG output follows the tools/process_assets.py conventions: 2x supersample,
LANCZOS downscale, 4-level alpha posterize, palette quantize, optimized PNG,
hard 300KB budget (photo mode auto-raises spacing and retries once).
"""

import argparse
import math
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw

MAX_BYTES = 300 * 1024
SUPERSAMPLE = 2

FG = {
    "navy": "#000050",
    "orange": "#FF7800",
    "orange-800": "#D94E0E",
    "white": "#FFFFFF",
    "cream": "#FAFAF0",
}
BG = {"none": None, "white": "#FFFFFF", "cream": "#FAFAF0"}

# Playbook p.33 printed defaults.
SPACING = 10.0
MIN_DOT = 2.0   # diameter, px
MAX_DOT = 8.0   # diameter, px
CUTOFF = 0.92   # cells lighter than this luminance get no dot
ALPHA_CUT = 0.1


def hex_rgb(h):
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def fmt(v):
    # 1-decimal, trailing-zero-free coordinates keep the SVG compact.
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def posterize_alpha(alpha):
    # 4 levels: 0 / 85 / 170 / 255 — enough for halftone edge softness.
    return alpha.point(lambda v: 255 if v >= 192 else 170 if v >= 106 else 85 if v >= 43 else 0)


def sample_grid(im, out_w, out_h, spacing):
    """Average the source per grid cell, alpha-weighted (premultiplied BOX
    downscale so transparent-pixel RGB never pollutes the cell tone)."""
    cols = max(1, round(out_w / spacing))
    rows = max(1, round(out_h / spacing))
    r, g, b, a = im.split()
    pre = Image.merge("RGBA", (ImageChops.multiply(r, a),
                               ImageChops.multiply(g, a),
                               ImageChops.multiply(b, a), a))
    grid = pre.resize((cols, rows), Image.BOX)
    return cols, rows, list(grid.getdata())


def photo_dots(im, out_w, out_h, args):
    """Map per-cell tone to dot diameter. Returns [(cx, cy, radius)]."""
    cols, rows, cells = sample_grid(im, out_w, out_h, args.spacing)
    sx, sy = out_w / cols, out_h / rows  # effective spacing (~= --spacing)
    rng = random.Random(args.seed)
    tone_cut = 1.0 - args.cutoff
    dots = []
    for i, (rp, gp, bp, av) in enumerate(cells):
        a = av / 255.0
        if a < ALPHA_CUT:
            continue
        # Un-premultiply, Rec.709 luminance, 0..1.
        lum = min(1.0, (0.2126 * rp + 0.7152 * gp + 0.0722 * bp) / (255.0 * a))
        tone = (lum if args.invert else 1.0 - lum) * a
        tone = min(1.0, max(0.0, 0.5 + (tone - 0.5) * args.contrast))
        if tone < tone_cut:
            continue
        d = args.min_dot + tone * (args.max_dot - args.min_dot)
        if args.size_variation:
            d *= 1.0 + rng.uniform(-1.0, 1.0) * args.size_variation
        cx = (i % cols + 0.5) * sx
        cy = (i // cols + 0.5) * sy
        if args.jitter:
            cx += rng.uniform(-1.0, 1.0) * args.jitter * sx
            cy += rng.uniform(-1.0, 1.0) * args.jitter * sy
        dots.append((cx, cy, d / 2.0))
    return dots


def ensure_bleed(x, y, r, w, h, rng):
    """Shift a circle so it crosses its nearest canvas edge."""
    edges = [(x, "x", 0), (w - x, "x", w), (y, "y", 0), (h - y, "y", h)]
    dist, axis, edge = min(edges)
    if dist < r:
        return x, y  # already bleeds
    inset = r * rng.uniform(0.2, 0.8)  # centre this far inside the edge
    if axis == "x":
        x = inset if edge == 0 else w - inset
    else:
        y = inset if edge == 0 else h - inset
    return x, y


def overlay_dots(w, h, args):
    """Website-style cluster: 2-4 large circles (1-2 fused pairs allowed),
    every circle bleeding off an edge, plus satellites fading centre-ward."""
    rng = random.Random(args.seed)
    m = min(w, h)
    n = rng.randint(2, 4)
    partners = min(rng.randint(1, 2), n - 1) if n >= 3 else 0
    circles = []
    edges = ["left", "right", "top", "bottom"]
    rng.shuffle(edges)
    for i in range(n - partners):
        r = m * rng.uniform(0.15, 0.30)  # 30-60% of min(W,H) diameter
        along = rng.uniform(0.15, 0.85)
        inset = r * rng.uniform(-0.25, 0.7)  # <r: crosses the edge
        edge = edges[i % 4]
        if edge == "left":
            x, y = inset, along * h
        elif edge == "right":
            x, y = w - inset, along * h
        elif edge == "top":
            x, y = along * w, inset
        else:
            x, y = along * w, h - inset
        circles.append((x, y, r))
    for j in range(partners):  # fused pair: overlap an anchor circle
        ax, ay, ar = circles[j]
        r = m * rng.uniform(0.15, 0.30)
        ang = rng.uniform(0.0, 2.0 * math.pi)
        dist = (ar + r) * rng.uniform(0.55, 0.85)
        x, y = ax + math.cos(ang) * dist, ay + math.sin(ang) * dist
        x, y = ensure_bleed(x, y, r, w, h, rng)
        circles.append((x, y, r))
    dots = list(circles)
    cx0, cy0, half_diag = w / 2.0, h / 2.0, math.hypot(w, h) / 2.0
    placed = 0
    for _ in range(args.satellites * 40):
        if placed >= args.satellites:
            break
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        d_norm = math.hypot(x - cx0, y - cy0) / half_diag
        if rng.random() > d_norm ** 2:  # sparse toward the centre
            continue
        if any(math.hypot(x - cx, y - cy) < cr for cx, cy, cr in circles):
            continue  # invisible inside a flat circle of the same colour
        dots.append((x, y, m * rng.uniform(0.004, 0.011)))
        placed += 1
    return dots


def write_svg(path, dots, w, h, fg_hex, bg_hex):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
             f'width="{w}" height="{h}">']
    if bg_hex:
        parts.append(f'<rect width="{w}" height="{h}" fill="{bg_hex}"/>')
    parts.append(f'<g fill="{fg_hex}">')
    parts.extend(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}"/>'
                 for x, y, r in dots)
    parts.append("</g></svg>")
    with open(path, "w") as f:
        f.write("".join(parts))
    return os.path.getsize(path)


def write_png(path, dots, w, h, fg_hex, bg_hex):
    s = SUPERSAMPLE
    bg = hex_rgb(bg_hex) + (255,) if bg_hex else (0, 0, 0, 0)
    canvas = Image.new("RGBA", (w * s, h * s), bg)
    draw = ImageDraw.Draw(canvas)
    fill = hex_rgb(fg_hex) + (255,)
    for x, y, r in dots:
        draw.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s],
                     fill=fill)
    im = canvas.resize((w, h), Image.LANCZOS)
    r, g, b, a = im.split()
    im = Image.merge("RGBA", (r, g, b, posterize_alpha(a)))
    im.quantize(colors=8, method=Image.FASTOCTREE).save(path, "PNG",
                                                        optimize=True)
    return os.path.getsize(path)


def emit(dots, w, h, fg_hex, bg_hex, base):
    svg_size = write_svg(base + ".svg", dots, w, h, fg_hex, bg_hex)
    png_size = write_png(base + ".png", dots, w, h, fg_hex, bg_hex)
    print(f"{os.path.basename(base)}: {len(dots)} dots {w}x{h}  "
          f"svg {svg_size // 1024}KB  png {png_size // 1024}KB")
    return png_size


def main():
    p = argparse.ArgumentParser(
        description="WPP ES brand dot-halftone generator (playbook v0.2 p.33 "
                    "defaults: square grid, spacing 10, dot diameter 2-8px, "
                    "contrast 1, jitter 0, size variation 0). Emits .svg + "
                    ".png; flat single-colour dots only.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("input", nargs="?",
                   help="source raster (PNG/JPEG/WebP, RGB or RGBA); "
                        "omit when using --overlay")
    p.add_argument("-o", "--out",
                   help="output base path, no extension (default: derived "
                        "from input/mode, written to cwd)")
    p.add_argument("--fg", choices=sorted(FG), default="navy",
                   help="dot colourway")
    p.add_argument("--bg", choices=sorted(BG), default="none",
                   help="background (none = transparent)")
    p.add_argument("--width", type=int, default=1920,
                   help="output width px; height keeps source aspect")
    p.add_argument("--spacing", type=float, default=SPACING,
                   help="square grid spacing, output px")
    p.add_argument("--min-dot", type=float, default=MIN_DOT,
                   help="min dot diameter px (lightest kept cell)")
    p.add_argument("--max-dot", type=float, default=MAX_DOT,
                   help="max dot diameter px (darkest cell)")
    p.add_argument("--cutoff", type=float, default=CUTOFF,
                   help="cells lighter than this luminance get no dot")
    p.add_argument("--contrast", type=float, default=1.0,
                   help="tone curve steepness around midtone")
    p.add_argument("--invert", action="store_true",
                   help="light areas get dots (for dark-ground sources)")
    p.add_argument("--jitter", type=float, default=0.0,
                   help="dot position jitter, fraction of spacing (playbook: 0)")
    p.add_argument("--size-variation", type=float, default=0.0,
                   help="random dot size variation 0-1 (playbook: 0)")
    p.add_argument("--overlay", nargs=2, type=int, metavar=("W", "H"),
                   help="overlay mode: large-circle cluster on a WxH canvas "
                        "instead of sampling an input image")
    p.add_argument("--satellites", type=int, default=16,
                   help="overlay mode: max small scatter dots (0 disables)")
    p.add_argument("--seed", type=int, default=0,
                   help="RNG seed (overlay layout, jitter, size variation)")
    args = p.parse_args()

    fg_hex, bg_hex = FG[args.fg], BG[args.bg]

    if args.overlay:
        w, h = args.overlay
        base = args.out or f"halftone-overlay-{w}x{h}-{args.fg}-s{args.seed}"
        dots = overlay_dots(w, h, args)
        png_size = emit(dots, w, h, fg_hex, bg_hex, base)
        if png_size > MAX_BYTES:
            print(f"ERROR: {base}.png is {png_size // 1024}KB > 300KB budget",
                  file=sys.stderr)
            sys.exit(1)
        return

    if not args.input:
        p.error("INPUT is required unless --overlay is given")
    im = Image.open(args.input).convert("RGBA")
    w = args.width
    h = max(1, round(im.height * w / im.width))
    stem = os.path.splitext(os.path.basename(args.input))[0]
    base = args.out or f"{stem}-halftone-{args.fg}"
    png_size = emit(photo_dots(im, w, h, args), w, h, fg_hex, bg_hex, base)
    if png_size > MAX_BYTES:
        # One retry at coarser spacing, per the 300KB asset budget.
        args.spacing *= 1.5
        print(f"WARNING: {base}.png over 300KB budget; retrying with "
              f"spacing {args.spacing:g}", file=sys.stderr)
        png_size = emit(photo_dots(im, w, h, args), w, h, fg_hex, bg_hex, base)
        if png_size > MAX_BYTES:
            print(f"ERROR: {base}.png still {png_size // 1024}KB > 300KB "
                  f"budget", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
