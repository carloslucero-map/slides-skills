#!/usr/bin/env python3
"""Build the uploadable skill bundle, and hold the skill under its size cap.

claude.ai takes a skill at 30 MB. Two numbers have to stay under that and they
are not the same number:

  the skill directory   what you get zipping wpp-es-html-deck/ yourself
  the bundle            what this script writes to dist/

The directory is the one that bites, because it is the obvious thing to zip and
nothing in the repo used to stop it growing. It is kept under the cap by where
things live: authoring material — the contact sheets shoot_snippets.py writes,
the renders and measurements of the source deck the canon was traced from —
sits in authoring/ at the repo root, outside the skill. Nothing under authoring/
is read while a deck is being built. This script REPORTS the directory size on
every run so a regression shows up the next time anyone packages.

The bundle then buys headroom on top, by re-encoding the canon reference
imagery. canon/<id>/ref.png and preview.png are 1920x1080 for a job that does
not need it: being looked at, by a model, when a fill comes out wrong. 1568 px
is the width an image is downsampled to before a model sees it. They are
re-encoded at that width with a 256-colour palette and THE SAME FILENAME —
CATALOG.md, meta.json's sourceRender and spec.json's referenceRender all name
ref.png, and renaming to .jpg would point 25 templates' provenance at a file
that does not exist.

assets/ is copied byte-for-byte. Those pixels end up inside a delivered deck.

Usage:
  python3 scripts/package_skill.py                 # stage + zip into ../dist/
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
REPO = os.path.dirname(SKILL)
NAME = os.path.basename(SKILL)
MB = 1024 * 1024

# Legacy locations. authoring/ is outside the skill now, but an old invocation
# (`shoot_snippets.py --out canon/_shots`) can still drop 14 MB back in here,
# and it must not reach a bundle.
EXCLUDE_DIRS = {"canon/_shots", "canon/_ref", "dist"}
EXCLUDE_NAMES = {"__pycache__", ".git", ".venv", "venv", "node_modules",
                 ".mypy_cache", ".pytest_cache", ".DS_Store"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".swp")

SHRINK = {"ref.png", "preview.png"}
SHRINK_WIDTH = 1568
SHRINK_COLORS = 256

GENERATED = os.path.join("build", "WPP-ES-DESIGN-GUIDELINE.md")


def skipped(rel, name):
    if name in EXCLUDE_NAMES or name.startswith("._"):
        return True
    if name.endswith(EXCLUDE_SUFFIXES):
        return True
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


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


def dir_size(path):
    return sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(path) for f in fs)


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
    ap.add_argument("--out", default=os.path.join(REPO, "dist"),
                    help="where the bundle is written (default: <repo>/dist, "
                         "OUTSIDE the skill directory — writing it inside would "
                         "push the directory itself over the cap)")
    ap.add_argument("--limit", type=float, default=30.0, help="budget in MB")
    ap.add_argument("--check", action="store_true", help="report only")
    ap.add_argument("--no-zip", action="store_true")
    ap.add_argument("--flat", action="store_true",
                    help="zip with SKILL.md at the archive root, not under %s/" % NAME)
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    if out == SKILL or out.startswith(SKILL + os.sep):
        print(f"  --out is inside the skill directory ({os.path.relpath(out, SKILL)}); "
              f"that is what the cap is measured on.", file=sys.stderr)
        return 2

    ensure_generated()
    files = list(walk_kept())

    stage = os.path.join(out, NAME)
    if not args.check:
        if os.path.isdir(stage):
            shutil.rmtree(stage)
        os.makedirs(stage)

    before, after = {}, {}
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

    on_disk = dir_size(SKILL)
    total = sum(after.values()) if after else sum(before.values())

    print(f"\n  {NAME}\n")
    print(f"  {'bucket':<22}{'directory':>12}{'bundle':>12}")
    print("  " + "-" * 46)
    for b in sorted(before, key=lambda k: -before[k]):
        print(f"  {b:<22}{before[b]/MB:>9.2f} MB{after.get(b, before[b])/MB:>9.2f} MB")
    print("  " + "-" * 46)
    print(f"  {'TOTAL':<22}{on_disk/MB:>9.2f} MB{total/MB:>9.2f} MB")

    over = [n for n, v in (("directory", on_disk), ("bundle", total))
            if v > args.limit * MB]
    print(f"\n  {len(files)} files · cap {args.limit:.0f} MB · "
          f"directory {(args.limit*MB - on_disk)/MB:+.2f} MB · "
          f"bundle {(args.limit*MB - total)/MB:+.2f} MB")

    if over:
        print(f"\n  OVER THE CAP: {', '.join(over)}\n", file=sys.stderr)
        if "directory" in over:
            print("  The directory is what you get zipping the folder by hand. "
                  "Move authoring output to authoring/ at the repo root.\n",
                  file=sys.stderr)
        return 1
    if args.check:
        print("  --check: nothing written (bundle column is a pre-shrink estimate)\n")
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
