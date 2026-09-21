#!/usr/bin/env python3
"""Build the uploadable skill bundle.

claude.ai enforces TWO limits on an uploaded skill and the tight one is not the
obvious one:

    max 200 files          <- this is what rejects the upload
    max 30 MB

The checkout is 329 files and 26.95 MB. Size was never the problem.

So the bundle is cut to what a deck build actually reads. Everything dropped
here is authoring or provenance material, and the repo keeps all of it:

  canon/<id>/meta.json, spec.json     read only by canon/_tools/build_catalog.py,
  canon/<id>/measure.json             which regenerates CATALOG.md and
  canon/_tools/                       catalog.json. The agent reads the
                                      generated pair, never the sources. 104 files.

  canon/<id>/ref.png                  the source slide each template was traced
                                      from. Provenance, not instruction. 25 files.

  canon/<id>/preview.png              collapsed into ONE contact sheet,
                                      canon/PREVIEWS.png. 25 files -> 1.

  assets/snippets/*.html              the 13 authoring sources. SKILL.md forbids
                                      opening them at fill time; the deck reads
                                      assets/snippets/variants/ only.

  assets/exemplars/                   SKILL.md: never read into context.

  scripts/shoot_snippets.py           repo-side tooling. Nothing in the bundle
  scripts/package_skill.py            invokes either.

What survives is load-bearing: CATALOG.md and catalog.json carry every field the
agent chooses on, capacity.json already holds the canon's measured limits, and
verify_deck.py degrades by design when canon/_tools is absent ("no canon in this
checkout; not an error").

Usage:
  python3 scripts/package_skill.py                 # stage + zip into ../dist/
  python3 scripts/package_skill.py --check         # report only, write nothing
  python3 scripts/package_skill.py --no-zip        # leave the staged tree only
"""

import argparse
import os
import shutil
import subprocess
import sys
import zipfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(SKILL)
NAME = os.path.basename(SKILL)
MB = 1024 * 1024

FILE_LIMIT = 200
SIZE_LIMIT_MB = 30.0

# Directories that do not ship. canon/_shots and canon/_ref live in authoring/
# now; they stay listed because an old `--out canon/_shots` invocation can still
# put 14 MB back and it must not reach a bundle.
# assets/exemplars/ is NOT here: SKILL.md attaches those four PNGs for the
# design-direction question and re-reads one as the review bar. "Never read
# into context" means do not parse them as text, not that they are optional.
EXCLUDE_DIRS = {"canon/_shots", "canon/_ref", "canon/_tools", "dist"}
EXCLUDE_FILES = {"scripts/shoot_snippets.py", "scripts/package_skill.py"}
# Per-template sources for the generated catalogue. Dropped with canon/_tools.
EXCLUDE_IN_CANON = {"meta.json", "spec.json", "measure.json", "ref.png"}
EXCLUDE_NAMES = {"__pycache__", ".git", ".venv", "venv", "node_modules",
                 ".mypy_cache", ".pytest_cache", ".DS_Store"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".swp")

SHEET = "canon/PREVIEWS.png"
SHEET_COLS = 5
SHEET_CELL_W = 480
SHEET_LABEL_H = 26
GENERATED = os.path.join("build", "WPP-ES-DESIGN-GUIDELINE.md")


def skipped(rel, name):
    if name in EXCLUDE_NAMES or name.startswith("._"):
        return True
    if name.endswith(EXCLUDE_SUFFIXES) or rel in EXCLUDE_FILES:
        return True
    if any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS):
        return True
    parts = rel.split("/")
    # canon/<id>/<file> — the catalogue's sources, not the catalogue.
    if len(parts) == 3 and parts[0] == "canon" and parts[2] in EXCLUDE_IN_CANON:
        return True
    return False


def walk_kept():
    for root, dirs, files in os.walk(SKILL):
        rel_root = os.path.relpath(root, SKILL)
        rel_root = "" if rel_root == "." else rel_root
        dirs[:] = sorted(d for d in dirs
                         if not skipped(os.path.join(rel_root, d) if rel_root else d, d))
        for f in sorted(files):
            rel = os.path.join(rel_root, f) if rel_root else f
            if not skipped(rel, f):
                yield rel


def build_sheet(stage):
    """One labelled contact sheet in place of 25 preview.png. Returns bytes.

    Choosing a template is meant to happen on CATALOG.md's `use when` column;
    the sheet is the second opinion, and a second opinion does not need 25
    files. Every cell is labelled with the id so a shape maps back to a row.
    """
    from PIL import Image, ImageDraw
    ids = sorted(d for d in os.listdir(os.path.join(SKILL, "canon"))
                 if os.path.isfile(os.path.join(SKILL, "canon", d, "preview.png")))
    cell_h = round(SHEET_CELL_W * 9 / 16)
    rows = (len(ids) + SHEET_COLS - 1) // SHEET_COLS
    pad = 8
    sheet = Image.new("RGB",
                      (SHEET_COLS * (SHEET_CELL_W + pad) + pad,
                       rows * (cell_h + SHEET_LABEL_H + pad) + pad),
                      (250, 248, 240))
    draw = ImageDraw.Draw(sheet)
    for i, tid in enumerate(ids):
        x = pad + (i % SHEET_COLS) * (SHEET_CELL_W + pad)
        y = pad + (i // SHEET_COLS) * (cell_h + SHEET_LABEL_H + pad)
        im = Image.open(os.path.join(SKILL, "canon", tid, "preview.png")).convert("RGB")
        sheet.paste(im.resize((SHEET_CELL_W, cell_h), Image.LANCZOS), (x, y))
        draw.text((x + 2, y + cell_h + 6), tid, fill=(26, 26, 74))
    dst = os.path.join(stage, SHEET)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    sheet.quantize(colors=256, method=Image.MEDIANCUT).save(dst, optimize=True)
    return os.path.getsize(dst), len(ids)


def patch_catalog(stage):
    """CATALOG.md is generated and tells the reader to open files the bundle
    does not carry. Correct it here rather than shipping a dead instruction."""
    p = os.path.join(stage, "canon", "CATALOG.md")
    if not os.path.isfile(p):
        return
    s = open(p, encoding="utf-8").read()
    old = ("Choose on `use when` — the rest is filtering. If a fill looks wrong, compare\n"
           "the template's `ref.png` (the source slide) with its `preview.png` before\n"
           "changing anything.")
    new = ("Choose on `use when` — the rest is filtering. If a fill looks wrong, find the\n"
           "template on `PREVIEWS.png` (all 25, labelled) and compare before changing\n"
           "anything. The full-size renders and the source slide each was traced from\n"
           "are in the repo, not in this upload.")
    if old in s:
        open(p, "w", encoding="utf-8").write(s.replace(old, new))


def shrink_to(src, dst):
    try:
        from PIL import Image
    except ImportError:
        shutil.copy2(src, dst)
        return os.path.getsize(dst)
    im = Image.open(src).convert("RGB")
    if im.width > 1568:
        im = im.resize((1568, round(im.height * 1568 / im.width)), Image.LANCZOS)
    im.quantize(colors=256, method=Image.MEDIANCUT,
                dither=Image.FLOYDSTEINBERG).save(dst, format="PNG", optimize=True)
    if os.path.getsize(dst) >= os.path.getsize(src):
        shutil.copy2(src, dst)
    return os.path.getsize(dst)


def ensure_generated():
    if os.path.isfile(os.path.join(SKILL, GENERATED)):
        return
    print(f"  {GENERATED} missing — running build_docs.py --write")
    subprocess.run([sys.executable, os.path.join(SKILL, "scripts", "build_docs.py"),
                    "--write"], cwd=SKILL, check=True)


def area(rel):
    parts = rel.split("/")
    if parts[0] == "canon":
        return "canon" if len(parts) <= 2 else "canon/<templates>"
    if parts[0] == "assets":
        return "assets/" + parts[1] if len(parts) > 1 else "assets"
    if parts[0] == "references":
        return "references/sections" if len(parts) > 2 else "references"
    return parts[0] if os.path.isdir(os.path.join(SKILL, parts[0])) else "(root)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "dist"))
    ap.add_argument("--max-files", type=int, default=FILE_LIMIT)
    ap.add_argument("--limit", type=float, default=SIZE_LIMIT_MB, help="MB")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-zip", action="store_true")
    ap.add_argument("--flat", action="store_true")
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    if out == SKILL or out.startswith(SKILL + os.sep):
        print("  --out is inside the skill directory; that is what gets measured.",
              file=sys.stderr)
        return 2

    ensure_generated()
    # preview.png is staged as the contact sheet, not as itself.
    files = [f for f in walk_kept() if os.path.basename(f) != "preview.png"]

    stage = os.path.join(out, NAME)
    if not args.check:
        if os.path.isdir(stage):
            shutil.rmtree(stage)
        os.makedirs(stage)

    counts, sizes = {}, {}
    for rel in files:
        src = os.path.join(SKILL, rel)
        a = area(rel)
        counts[a] = counts.get(a, 0) + 1
        if args.check:
            sizes[a] = sizes.get(a, 0) + os.path.getsize(src)
            continue
        dst = os.path.join(stage, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = (shrink_to(src, dst) if os.path.basename(rel) == "ref.png"
             else (shutil.copy2(src, dst), os.path.getsize(dst))[1])
        sizes[a] = sizes.get(a, 0) + n

    n_files = len(files)
    if not args.check:
        sheet_bytes, n_prev = build_sheet(stage)
        patch_catalog(stage)
        counts["canon"] = counts.get("canon", 0) + 1
        sizes["canon"] = sizes.get("canon", 0) + sheet_bytes
        n_files += 1
        print(f"\n  PREVIEWS.png — {n_prev} previews on one sheet, "
              f"{sheet_bytes/MB:.2f} MB")
    else:
        # --check must count the sheet too, or it reports one file fewer than
        # a real run and a bundle at the limit reads as having room.
        counts["canon"] = counts.get("canon", 0) + 1
        n_files += 1

    total = sum(sizes.values())
    print(f"\n  {NAME} bundle\n")
    print(f"  {'area':<22}{'files':>8}{'size':>12}")
    print("  " + "-" * 42)
    for a in sorted(counts, key=lambda k: -counts[k]):
        print(f"  {a:<22}{counts[a]:>8}{sizes.get(a,0)/MB:>9.2f} MB")
    print("  " + "-" * 42)
    print(f"  {'TOTAL':<22}{n_files:>8}{total/MB:>9.2f} MB")
    print(f"\n  limits: {n_files}/{args.max_files} files · "
          f"{total/MB:.2f}/{args.limit:.0f} MB "
          f"(spare: {args.max_files - n_files} files, "
          f"{(args.limit*MB - total)/MB:.2f} MB)")

    over = []
    if n_files > args.max_files:
        over.append(f"{n_files - args.max_files} files too many")
    if total > args.limit * MB:
        over.append(f"{(total - args.limit*MB)/MB:.2f} MB too big")
    if over:
        print(f"\n  OVER: {'; '.join(over)}\n", file=sys.stderr)
        if n_files > args.max_files:
            print("  Nothing else is safe to drop — what is left is cited by SKILL.md\n"
                  "  or the guideline. To make room, consolidate rather than delete:\n"
                  "    assets/icons/       32 files, 71 KB. One file costs ~18k tokens\n"
                  "                        to read whole vs ~2k for the icons a deck\n"
                  "                        uses, so split by weight family, not into one.\n"
                  "    assets/snippets/    51 variants + 13 authoring sources. SKILL.md\n"
                  "                        forbids the sources at fill time but §12 says\n"
                  "                        'assemble from' them — resolve that first.\n"
                  "    build/ + build_docs.py  drops the guideline-drift gate. 2 files.\n",
                  file=sys.stderr)
        return 1
    if args.check:
        print("  --check: nothing written\n")
        return 0

    if not args.no_zip:
        zpath = os.path.join(out, NAME + ".zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for root, _, fs in os.walk(stage):
                for f in sorted(fs):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, stage)
                    z.write(p, rel if args.flat else os.path.join(NAME, rel))
        print(f"  zip  {os.path.relpath(zpath, REPO)}  "
              f"{os.path.getsize(zpath)/MB:.2f} MB\n")
    else:
        print(f"  tree {os.path.relpath(stage, REPO)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
