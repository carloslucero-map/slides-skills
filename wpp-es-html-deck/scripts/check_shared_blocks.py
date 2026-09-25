#!/usr/bin/env python3
"""
check_shared_blocks.py — the two blocks the skills share must stay identical.

The house copy rules and the handoff contract are each written twice, once in
this skill and once in deck-content-builder, because each skill is uploaded on
its own and must read complete. Nothing but this check keeps the two copies in
step, and the drift is silent: each copy reads plausibly on its own.

  python3 scripts/check_shared_blocks.py     # exit 1 when a pair differs

verify_deck.py runs it on every deck. It needs deck-content-builder/ beside
this skill, as in the repository; an uploaded skill has no sibling, and the
check says it was skipped rather than failing.

(Until 4.2.0 this was build_docs.py, which also generated the skill's own copy
of the brand guideline, references/CORE.md and the whole guideline in build/,
from references/sections/. That copy is gone: the design system owns the
brand, and the skill reads its copy in design-system/.)
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REPO = os.path.dirname(SKILL)

# (block, this skill's copy, deck-content-builder's copy), paths from the repo root
SHARED_BLOCKS = [
    ("HOUSE-COPY-RULES", "wpp-es-html-deck/SKILL.md", "deck-content-builder/SKILL.md"),
    ("HANDOFF-CONTRACT", "wpp-es-html-deck/references/HANDOFF-CONTRACT.md",
     "deck-content-builder/SKILL.md"),
]


def shared_block(path, name):
    """(version, body, twin named in the marker) of <!-- NAME vN … --> … <!-- /NAME -->."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"<!-- " + name + r" v(\d+) — keep byte-identical with the block in "
                  r"(\S+) -->\n(.*?)<!-- /" + name + r" -->", text, re.S)
    return (m.group(1), m.group(3), m.group(2)) if m else None


def check_shared_blocks():
    """(problems, summary). Skipped when deck-content-builder is not beside the skill."""
    if not os.path.isdir(os.path.join(REPO, "deck-content-builder")):
        return [], "shared blocks not checked (deck-content-builder is not beside this skill)"
    problems = []
    for name, ours, theirs in SHARED_BLOCKS:
        a, b = (shared_block(os.path.join(REPO, p), name) for p in (ours, theirs))
        if not (a and b):
            problems.append(f"{name}: no block in {ours if not a else theirs}")
            continue
        if a[2] != theirs or b[2] != ours:
            problems.append(f"{name}: a marker names the wrong twin "
                            f"({ours} names {a[2]}, {theirs} names {b[2]})")
        if a[0] != b[0]:
            problems.append(f"{name}: v{a[0]} in {ours}, v{b[0]} in {theirs}")
        elif a[1] != b[1]:
            problems.append(f"{name}: the text differs between {ours} and {theirs}")
    return problems, "both shared blocks match deck-content-builder"


def main():
    problems, summary = check_shared_blocks()
    if problems:
        print("SHARED BLOCK DRIFT — a block the two skills share differs:", file=sys.stderr)
        for pr in problems:
            print(f"  {pr}", file=sys.stderr)
        print("\nEdit both copies together; they must stay byte-identical.", file=sys.stderr)
        sys.exit(1)
    print(f"SHARED BLOCKS OK — {summary}")


if __name__ == "__main__":
    main()
