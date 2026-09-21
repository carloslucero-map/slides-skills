#!/usr/bin/env python3
"""Build the uploadable skill bundle.

claude.ai enforces TWO limits on an uploaded skill and the tight one is not the
obvious one:

    max 200 ENTRIES        <- files AND directories. This is what rejects it.
    max 30 MB

The error reads "Zip contains too many files (maximum 200)", but a bundle of 199
files is still refused: it carries 41 directories, so an extractor sees 240
entries. Every directory costs the same as a file, which makes a directory
holding one file the most expensive thing in the tree.

Two layout changes follow from that, and they are why this is not just a filter:

  canon/<id>/template.html   -> canon/templates/<id>.html
      25 directories holding one file each cost 50 entries. Flat: 26.
      check_capacity.py accepts either layout; SKILL.md is patched to match.

  assets/icons/<name>.svg    -> assets/icons/<family>.md
      32 files + 1 directory -> 4 + 1. The families are §8.1\'s own, parsed
      from the guideline rather than hardcoded, and §8.1\'s hard rule is one
      weight family per slide — so the agent reads exactly the family it is
      already required to pick. One merged file would have cost ~18k tokens
      a read; the largest family costs ~8k.

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
import re
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

ICON_SECTION = "references/sections/8-iconography.md"
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


def icon_families():
    """{family: [icon, ...]} parsed from §8.1, first family wins.

    Parsed, not hardcoded: the suite has changed twice (v3.3, v3.5) and a
    hardcoded list would ship icons under the wrong weight, which §8.1 calls
    "the most visible amateur tell". Returns {} if the section stops matching,
    and the caller then ships the icons unchanged and fails on the entry count
    rather than silently mis-grouping them.
    """
    path = os.path.join(SKILL, ICON_SECTION)
    if not os.path.isfile(path):
        return {}
    txt = open(path, encoding="utf-8").read()
    if "by weight family" not in txt:
        return {}
    body = txt[txt.index("by weight family"):]
    have = {f[:-len(".svg")] for f in os.listdir(os.path.join(SKILL, "assets", "icons"))
            if f.endswith(".svg")}
    fams, claimed = {}, set()
    for m in re.finditer(r"^- \*\*([a-z]+)\*\*[^:]*:(.*?)(?=^- \*\*|\Z)", body, re.M | re.S):
        # Dedup WITHIN a family as well as across them: the last bullet has no
        # bullet after it, so its capture runs to end-of-section and re-matches
        # the names in the pairing-rule prose below. That shipped `spark` twice.
        picked = []
        for i in re.findall(r"`([a-z0-9-]+)`", m.group(2)):
            if i in have and i not in claimed and i not in picked:
                picked.append(i)
        if picked:
            fams[m.group(1)] = picked
            claimed |= set(picked)
    # Every icon placed exactly once, or ship them ungrouped and fail on count.
    if claimed != have or sum(len(v) for v in fams.values()) != len(have):
        return {}
    return fams


def write_icon_families(stage, fams):
    """One Markdown file per weight family, each icon under its own heading."""
    total = 0
    for fam, icons in fams.items():
        dst = os.path.join(stage, "assets", "icons", fam + ".md")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(f"# Icon suite — {fam} family ({len(icons)})\n\n"
                     "§8.1: ONE weight family per icon row / per slide. Paste the `<svg>`\n"
                     "inline into `<div class=\"icon\">…</div>` — do not link to it.\n")
            for i in icons:
                svg = open(os.path.join(SKILL, "assets", "icons", i + ".svg"),
                           encoding="utf-8").read().strip()
                fh.write(f"\n## {i}\n\n{svg}\n")
        total += os.path.getsize(dst)
    return total


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


def patch_skill_md(stage, fams):
    """SKILL.md names both layouts it is about to stop matching. It is
    hand-written (not generated from references/sections/), so patching it here
    does not put build_docs.py --check into drift."""
    p = os.path.join(stage, "SKILL.md")
    s = open(p, encoding="utf-8").read()
    before = s
    s = s.replace("`canon/<id>/template.html` and paste its `<section>`.",
                  "`canon/templates/<id>.html` and paste its `<section>`.")
    if fams:
        roster = " · ".join(f"`{f}.md` ({len(i)})" for f, i in fams.items())
        s = s.replace(
            "Icons come from `assets/icons/` (32 suite SVGs, §8.1 — ONE weight family per",
            f"Icons come from `assets/icons/`, one Markdown file per weight family —\n"
            f"{roster} — each icon under its own `##` heading (§8.1 — ONE weight family per")
    if s != before:
        open(p, "w", encoding="utf-8").write(s)


def patch_icon_refs(stage, fams):
    """Snippets tell the agent to paste `assets/icons/<name>.svg`. Once icons
    ship grouped by family that file does not exist, and the instruction is in
    columns-v4.html — a variant the deck actually reads, not just an authoring
    source. Repoint it at the family file and the heading inside it."""
    home = {i: f for f, icons in fams.items() for i in icons}
    if not home:
        return 0
    pat = re.compile(r"assets/icons/([a-z0-9-]+)\.svg")
    n = 0
    for root, dirs, files in os.walk(stage):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if not f.endswith((".html", ".md")):
                continue
            fp = os.path.join(root, f)
            txt = open(fp, encoding="utf-8").read()
            new = pat.sub(lambda m: (f"assets/icons/{home[m.group(1)]}.md (## {m.group(1)})"
                                     if m.group(1) in home else m.group(0)), txt)
            if new != txt:
                open(fp, "w", encoding="utf-8").write(new)
                n += len(pat.findall(txt))
    return n


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
    ap.add_argument("--max-files", type=int, default=FILE_LIMIT,
                    help="entry cap: files PLUS directories")
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
    fams = icon_families()
    if not fams:
        print("  §8.1 did not parse — shipping icons unchanged (entry count will "
              "say so rather than mis-grouping them)", file=sys.stderr)

    def dest_for(rel):
        """Where a source file lands in the bundle. See the module docstring:
        directories cost an entry each, so canon loses 24 of them here."""
        parts = rel.split("/")
        if len(parts) == 3 and parts[0] == "canon" and parts[2] == "template.html":
            return f"canon/templates/{parts[1]}.html"
        return rel

    files = [f for f in walk_kept() if os.path.basename(f) != "preview.png"]
    if fams:                      # emitted as <family>.md instead
        files = [f for f in files if not f.startswith("assets/icons/")]

    stage = os.path.join(out, NAME)
    if not args.check:
        if os.path.isdir(stage):
            shutil.rmtree(stage)
        os.makedirs(stage)

    counts, sizes, staged = {}, {}, []
    for rel in files:
        src = os.path.join(SKILL, rel)
        dest = dest_for(rel)
        staged.append(dest)
        a = area(dest)
        counts[a] = counts.get(a, 0) + 1
        if args.check:
            sizes[a] = sizes.get(a, 0) + os.path.getsize(src)
            continue
        dst = os.path.join(stage, dest)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = (shrink_to(src, dst) if os.path.basename(rel) == "ref.png"
             else (shutil.copy2(src, dst), os.path.getsize(dst))[1])
        sizes[a] = sizes.get(a, 0) + n

    for fam in fams:
        staged.append(f"assets/icons/{fam}.md")
        counts["assets/icons"] = counts.get("assets/icons", 0) + 1
    staged.append(SHEET)
    counts["canon"] = counts.get("canon", 0) + 1

    if not args.check:
        if fams:
            sizes["assets/icons"] = write_icon_families(stage, fams)
        sheet_bytes, n_prev = build_sheet(stage)
        patch_catalog(stage)
        patch_skill_md(stage, fams)
        n_ref = patch_icon_refs(stage, fams)
        if n_ref:
            print(f"  icon refs — {n_ref} `<name>.svg` pointers repointed at family files")
        sizes["canon"] = sizes.get("canon", 0) + sheet_bytes
        print(f"\n  PREVIEWS.png — {n_prev} previews on one sheet, {sheet_bytes/MB:.2f} MB")
        if fams:
            print("  icons — " + ", ".join(f"{f}.md ({len(i)})" for f, i in fams.items()))

    # What the platform counts: every file AND every directory an extractor makes.
    dirs = set()
    for rel in staged:
        parts = rel.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    dirs.add("")                                  # the top-level folder itself
    n_files, n_dirs = len(staged), len(dirs)
    n_entries = n_files + n_dirs
    total = sum(sizes.values())

    print(f"\n  {NAME} bundle\n")
    print(f"  {'area':<22}{'files':>8}{'size':>12}")
    print("  " + "-" * 42)
    for a in sorted(counts, key=lambda k: -counts[k]):
        print(f"  {a:<22}{counts[a]:>8}{sizes.get(a,0)/MB:>9.2f} MB")
    print("  " + "-" * 42)
    print(f"  {'':<22}{n_files:>8}{total/MB:>9.2f} MB")
    print(f"  {'+ directories':<22}{n_dirs:>8}")
    print(f"  {'= ENTRIES':<22}{n_entries:>8}")
    print(f"\n  limits: {n_entries}/{args.max_files} entries · "
          f"{total/MB:.2f}/{args.limit:.0f} MB "
          f"(spare: {args.max_files - n_entries} entries, "
          f"{(args.limit*MB - total)/MB:.2f} MB)")

    over = []
    if n_entries > args.max_files:
        over.append(f"{n_entries - args.max_files} entries too many")
    if total > args.limit * MB:
        over.append(f"{(total - args.limit*MB)/MB:.2f} MB too big")
    if over:
        print(f"\n  OVER: {'; '.join(over)}\n", file=sys.stderr)
        if n_entries > args.max_files:
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
