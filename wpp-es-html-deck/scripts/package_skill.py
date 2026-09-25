#!/usr/bin/env python3
"""Check this skill against claude.ai's upload limits, and zip it cleanly.

claude.ai caps an uploaded skill at:

    200 ENTRIES        files AND directories, both counted
     30 MB

The error says only "Zip contains too many files (maximum 200)", which is why
this took four attempts to pin down. A folder of 199 files carrying 41
directories is 240 entries and is refused.

THIS FOLDER IS THE SKILL. It is kept under the cap by where things live, not by
a build step, so `zip -rX` on it is a valid upload and so is this script's
output. Authoring material sits in authoring/ at the repo root, outside the
skill: the canon sources each template was traced from, the tools that generate
CATALOG.md and catalog.json and the design-system copy, the individual icon SVGs,
the contact sheets. None of it is read while a deck is being built.

Two layouts exist because a directory costs an entry, so a directory holding one
file is the most expensive thing in a tree:

    canon/templates/<id>.html      one directory, not 25
    design-system/icons/<family>.md
                                   four files, not 32 — grouped by the design
                                   system's own weight families, which is the
                                   unit the agent has to pick anyway

DO NOT COMPRESS THIS FOLDER WITH FINDER. macOS writes a __MACOSX/._name shadow
entry for every file carrying an extended attribute, and every file in a folder
extracted from an internet download carries com.apple.quarantine. Measured on
this skill: 410 extra entries, and `xattr -cr` first does not prevent it. Use
this script, or `zip -rX`.

Usage:
  python3 scripts/package_skill.py          # check, then write ../dist/<name>.zip
  python3 scripts/package_skill.py --check  # check only, write nothing
"""

import argparse
import os
import sys
import zipfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(SKILL)
NAME = os.path.basename(SKILL)
MB = 1024 * 1024

ENTRY_LIMIT = 200
SIZE_LIMIT_MB = 30.0

SKIP_DIRS = {"__pycache__", ".git", ".venv", "venv", "node_modules",
             ".mypy_cache", ".pytest_cache", "dist"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".swp")
SKIP_NAMES = {".DS_Store"}


def walk():
    """Files that belong in the upload, relative to SKILL."""
    for root, dirs, files in os.walk(SKILL):
        rel_root = os.path.relpath(root, SKILL)
        rel_root = "" if rel_root == "." else rel_root
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if f in SKIP_NAMES or f.endswith(SKIP_SUFFIXES) or f.startswith("._"):
                continue
            yield os.path.join(rel_root, f) if rel_root else f


def area(rel):
    p = rel.split("/")
    if len(p) == 1:
        return "(root)"
    if p[0] in ("assets", "references", "canon", "design-system") and len(p) > 2:
        return f"{p[0]}/{p[1]}"
    return p[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "dist"))
    ap.add_argument("--max-entries", type=int, default=ENTRY_LIMIT)
    ap.add_argument("--limit", type=float, default=SIZE_LIMIT_MB, help="MB")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    files = list(walk())
    dirs = set()
    for rel in files:
        p = rel.split("/")[:-1]
        for i in range(1, len(p) + 1):
            dirs.add("/".join(p[:i]))
    dirs.add("")                               # the top-level folder itself

    counts, sizes = {}, {}
    for rel in files:
        a = area(rel)
        counts[a] = counts.get(a, 0) + 1
        sizes[a] = sizes.get(a, 0) + os.path.getsize(os.path.join(SKILL, rel))

    entries = len(files) + len(dirs)
    total = sum(sizes.values())

    print(f"\n  {NAME}\n")
    print(f"  {'area':<26}{'files':>7}{'size':>11}")
    print("  " + "-" * 44)
    for a in sorted(counts, key=lambda k: -counts[k]):
        print(f"  {a:<26}{counts[a]:>7}{sizes[a]/MB:>8.2f} MB")
    print("  " + "-" * 44)
    print(f"  {'':<26}{len(files):>7}{total/MB:>8.2f} MB")
    print(f"  {'+ directories':<26}{len(dirs):>7}")
    print(f"  {'= ENTRIES':<26}{entries:>7}")
    print(f"\n  {entries}/{args.max_entries} entries · {total/MB:.2f}/{args.limit:.0f} MB"
          f"   (spare: {args.max_entries - entries} entries, "
          f"{(args.limit*MB - total)/MB:.2f} MB)")

    over = []
    if entries > args.max_entries:
        over.append(f"{entries - args.max_entries} entries too many")
    if total > args.limit * MB:
        over.append(f"{(total - args.limit*MB)/MB:.2f} MB too big")
    if over:
        print(f"\n  OVER: {'; '.join(over)}\n", file=sys.stderr)
        print("  A directory costs an entry, same as a file. Before deleting\n"
              "  anything, look for a directory holding one or two files, and\n"
              "  move authoring-only material to authoring/ at the repo root.\n",
              file=sys.stderr)
        return 1
    if args.check:
        print("  --check: nothing written\n")
        return 0

    os.makedirs(args.out, exist_ok=True)
    zpath = os.path.join(args.out, NAME + ".zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in files:
            z.write(os.path.join(SKILL, rel), os.path.join(NAME, rel))
    print(f"  zip  {os.path.relpath(zpath, REPO)}  "
          f"{os.path.getsize(zpath)/MB:.2f} MB   (no __MACOSX entries)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
