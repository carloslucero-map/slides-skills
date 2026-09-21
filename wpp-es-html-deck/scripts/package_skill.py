#!/usr/bin/env python3
"""Build the uploadable skill bundle.

claude.ai caps an uploaded skill at 30 MB. The checkout is ~55 MB, and the
overflow is entirely authoring material: the contact sheets the snippets were
shot against, the renders of the source deck the canon was traced from, and
25 pairs of 1920x1080 PNGs kept at print weight. None of that is read while a
deck is being built.

So the repo stays whole — it is the source the canon is re-derived from, and
the copy handed to design work — and this script stages a second, lean tree
for upload:

  1. drops the authoring-only directories (canon/_shots, canon/_ref) and junk
  2. re-encodes canon/<id>/ref.png and preview.png at 1568 px wide,
     256-colour palette, SAME FILENAME — the docs and meta.json keep pointing
     at a file that exists. 1568 px is what an image is downsampled to before
     a model sees it, so nothing is lost for the one job these images have:
     being looked at when a fill comes out wrong.
  3. refuses to produce a bundle over the limit

Usage:
  python3 scripts/package_skill.py                 # stage + zip into dist/
  python3 scripts/package_skill.py --check         # report only, write nothing
  python3 scripts/package_skill.py --limit 25      # tighter budget, in MB
  python3 scripts/package_skill.py --no-zip        # leave the staged tree only
"""

import argparse
import os
import shutil
import subprocess
import sys
import zipfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = os.path.basename(SKILL)
MB = 1024 * 1024

# Authoring inputs and outputs. Nothing under these is read at deck-build time;
# every reference to them lives in the tool that writes them.
EXCLUDE_DIRS = {
    "canon/_shots",     # contact sheets from shoot_snippets.py
    "canon/_ref",       # renders + measurements of the source deck
    "dist",             # this script's own output
}
EXCLUDE_NAMES = {"__pycache__", ".git", ".venv", "venv", "node_modules",
                 ".mypy_cache", ".pytest_cache", ".DS_Store"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".swp")

# Re-encoded on the way into the bundle. Only the canon reference imagery:
# assets/ ships pixels that end up inside a delivered deck and must stay exact.
SHRINK = {"ref.png", "preview.png"}
SHRINK_WIDTH = 1568
SHRINK_COLORS = 256

GENERATED = os.path.join("build", "WPP-ES-DESIGN-GUIDELINE.md")


def skipped(rel, name):
    if name in EXCLUDE_NAMES or name.startswith("._"):
        return True
    if name.endswith(EXCLUDE_SUFFIXES):
        return True
    return rel in EXCLUDE_DIRS or any(
        rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


def walk_kept():
    """Every file that belongs in the bundle, as paths relative to SKILL."""
    for root, dirs, files in os.walk(SKILL):
        rel_root = os.path.relpath(root, SKILL)
        rel_root = "" if rel_root == "." else rel_root
        dirs[:] = sorted(d for d in dirs
                         if not skipped(os.path.join(rel_root, d) if rel_root else d, d))
        for f in sorted(files):
            rel = os.path.join(rel_root, f) if rel_root else f
            if not skipped(rel, f):
                yield rel


def shrink_to(src, dst):
    """Palette-quantised copy at SHRINK_WIDTH. Returns bytes written.

    Falls back to a plain copy if Pillow is missing or the re-encode comes out
    bigger than the original — a bundle with an untouched PNG is correct, one
    with a bloated PNG is not.
    """
    try:
        from PIL import Image
    except ImportError:
        shutil.copy2(src, dst)
        return os.path.getsize(dst)
    im = Image.open(src).convert("RGB")
    if im.width > SHRINK_WIDTH:
        im = im.resize((SHRINK_WIDTH, round(im.height * SHRINK_WIDTH / im.width)),
                       Image.LANCZOS)
    im.quantize(colors=SHRINK_COLORS, method=Image.MEDIANCUT,
                dither=Image.FLOYDSTEINBERG).save(dst, format="PNG", optimize=True)
    if os.path.getsize(dst) >= os.path.getsize(src):
        shutil.copy2(src, dst)
    return os.path.getsize(dst)


def ensure_generated():
    """build/ is gitignored, so a fresh clone has no master guideline."""
    if os.path.isfile(os.path.join(SKILL, GENERATED)):
        return
    script = os.path.join(SKILL, "scripts", "build_docs.py")
    print(f"  {GENERATED} missing — running build_docs.py --write")
    subprocess.run([sys.executable, script, "--write"], cwd=SKILL, check=True)


def bucket(rel):
    head = rel.split("/")[0]
    if head == "canon":
        return "canon/*/ref.png" if rel.endswith("/ref.png") else (
            "canon/*/preview.png" if rel.endswith("/preview.png") else "canon (text)")
    return head if os.path.isdir(os.path.join(SKILL, head)) else "(root files)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(SKILL, "dist"))
    ap.add_argument("--limit", type=float, default=30.0, help="budget in MB")
    ap.add_argument("--check", action="store_true", help="report only")
    ap.add_argument("--no-zip", action="store_true")
    ap.add_argument("--flat", action="store_true",
                    help="zip with SKILL.md at the archive root, not under %s/" % NAME)
    args = ap.parse_args()

    ensure_generated()
    files = list(walk_kept())

    stage = os.path.join(args.out, NAME)
    if not args.check:
        if os.path.isdir(stage):
            shutil.rmtree(stage)
        os.makedirs(stage)

    before = {}
    after = {}
    for rel in files:
        src = os.path.join(SKILL, rel)
        b = bucket(rel)
        before[b] = before.get(b, 0) + os.path.getsize(src)
        if args.check:
            continue
        dst = os.path.join(stage, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = (shrink_to(src, dst) if os.path.basename(rel) in SHRINK
             else (shutil.copy2(src, dst), os.path.getsize(dst))[1])
        after[b] = after.get(b, 0) + n

    checkout = sum(os.path.getsize(os.path.join(r, f))
                   for r, _, fs in os.walk(SKILL) for f in fs
                   if not os.path.join(r, f).startswith(args.out))
    total = sum(after.values()) if after else sum(before.values())

    print(f"\n  {NAME} bundle\n")
    print(f"  {'bucket':<22}{'checkout':>12}{'bundle':>12}")
    print("  " + "-" * 46)
    for b in sorted(before, key=lambda k: -before[k]):
        got = after.get(b, before[b])
        print(f"  {b:<22}{before[b]/MB:>9.2f} MB{got/MB:>9.2f} MB")
    print("  " + "-" * 46)
    print(f"  {'TOTAL':<22}{checkout/MB:>9.2f} MB{total/MB:>9.2f} MB")
    print(f"\n  {len(files)} files · limit {args.limit:.0f} MB · "
          f"headroom {(args.limit * MB - total)/MB:.2f} MB")

    if total > args.limit * MB:
        print(f"\n  OVER BUDGET by {(total - args.limit*MB)/MB:.2f} MB\n", file=sys.stderr)
        return 1
    if args.check:
        print("  --check: nothing written (bundle figures are pre-shrink estimates)\n")
        return 0

    if not args.no_zip:
        zpath = os.path.join(args.out, NAME + ".zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for root, _, fs in os.walk(stage):
                for f in sorted(fs):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, stage)
                    z.write(p, rel if args.flat else os.path.join(NAME, rel))
        print(f"  zip  {os.path.relpath(zpath, SKILL)}  "
              f"{os.path.getsize(zpath)/MB:.2f} MB\n")
    else:
        print(f"  tree {os.path.relpath(stage, SKILL)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
