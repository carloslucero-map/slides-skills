# WPP ES | MAP — design guideline (moved)

This file is no longer the master. It was maintained by hand alongside
`references/sections/` and `references/CORE.md`, and nothing kept the three in
step — the drift was silent, and the copy that used to live here was already
behind on §2 and §12.15a when it was retired.

**The source is `references/sections/`.** Edit there, and nowhere else.

- **`references/CORE.md`** — the always-loaded subset. Generated.
- **`build/WPP-ES-DESIGN-GUIDELINE.md`** — the whole guideline in one file, for
  a human reading it end to end or diffing it against a future playbook.
  Generated, gitignored, and rebuilt by:

```bash
python3 scripts/build_docs.py --write
```

`build_docs.py --check` fails if either output has drifted from `sections/`,
and `verify_deck.py` runs that check on every deck.

**Do not read this path to settle a question.** CORE.md holds the numbers the
verifier enforces; a section file behind its trigger holds the rest. Reaching
for the whole guideline costs ~28,600 tokens to answer something CORE has
already answered.
