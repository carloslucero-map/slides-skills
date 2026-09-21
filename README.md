# Slides Skills — WPP Enterprise Solutions | MAP

Two Claude [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
that together turn raw context into a finished, on-brand presentation. They are
designed as a chain: one writes the words, the other renders them.

```
raw notes / brief
      │
      ▼
┌─────────────────────┐   approved .md    ┌─────────────────────┐
│ deck-content-builder│ ────────────────► │  wpp-es-html-deck   │
│  writes the content │  HANDOFF-CONTRACT │  renders the deck   │
└─────────────────────┘                   └─────────────────────┘
      │                                             │
      ▼                                             ▼
 slide-by-slide Markdown                   self-contained .html
 (also pastes into PowerPoint               (16:9, keyboard-navigable,
  or Google Slides)                          no external assets)
```

Either skill can be used on its own. The handoff format between them is
specified in [`wpp-es-html-deck/references/HANDOFF-CONTRACT.md`](wpp-es-html-deck/references/HANDOFF-CONTRACT.md).

## The skills

### `deck-content-builder`
Writes the **text content** of a deck — action titles, bullets, callouts,
speaker notes — using consultant-grade methods (Pyramid Principle, SCR).
Output is a single Markdown file. It does not design or render anything.

Single file, no dependencies: [`deck-content-builder/SKILL.md`](deck-content-builder/SKILL.md).

### `wpp-es-html-deck`
Renders a **self-contained HTML deck** in the WPP ES | MAP visual language —
Navy + Cream + Orange, WPP Sans, the dot system, 16:9, keyboard-navigable.
Ships the brand assets, a 51-template snippet library, a per-slot capacity
model, and a verifier that enforces the design guideline.

| Path | What it holds |
|---|---|
| `SKILL.md` | The skill itself — the operating instructions |
| `references/CORE.md` | The always-loaded subset of the design guideline |
| `references/WPP-ES-DESIGN-GUIDELINE.md` | The master guideline (source of truth) |
| `references/sections/` | The master guideline split by section, loaded on demand |
| `references/SNIPPET-INDEX.md` | All 51 layout templates, one line each |
| `references/capacity.json` | Per-slot min/ideal/max character counts |
| `references/HANDOFF-CONTRACT.md` | The content → render contract |
| `assets/` | Fonts, logos, icons, illustrations, photos, textures, snippets |
| `scripts/` | Shell generator, capacity tooling, halftone generator, verifier |

## Installation

Copy (or symlink) each skill directory into your Claude skills folder:

```bash
git clone https://github.com/carloslucero-map/slides-skills.git
ln -s "$PWD/slides-skills/wpp-es-html-deck"     ~/.claude/skills/wpp-es-html-deck
ln -s "$PWD/slides-skills/deck-content-builder" ~/.claude/skills/deck-content-builder
```

## Requirements

`deck-content-builder` has none. `wpp-es-html-deck` needs them only for its
scripts — the skill itself renders decks without either.

```bash
pip install -r wpp-es-html-deck/requirements.txt
```

- **Pillow** — required by `scripts/halftone.py`; optional for
  `verify_deck.py --contact-sheet`, which warns and skips without it.
- **Google Chrome (headless)** — required by `verify_deck.py` for
  `--screenshots` and the geometry probe. Auto-detected on macOS, Linux and
  Windows; override the binary with `WPP_DECK_CHROME=/path/to/chrome`.

## Scripts

```bash
# Generate a deck shell
python wpp-es-html-deck/scripts/build_shell.py --out deck.html

# Verify a deck against the design guideline
python wpp-es-html-deck/scripts/verify_deck.py deck.html
python wpp-es-html-deck/scripts/verify_deck.py deck.html --screenshots shots/

# Check content against the per-slot capacity model
python wpp-es-html-deck/scripts/check_capacity.py

# Regenerate capacity.json and the snippet index from the snippet library
python wpp-es-html-deck/scripts/derive_capacity.py
```

`verify_deck.py` exits 0 when every check passes (warnings allowed) and 1 on
any failure, so it drops into CI as-is.

## Uploading to claude.ai

claude.ai caps an uploaded skill at **200 entries and 30 MB**. The error reads
*"Zip contains too many files (maximum 200)"*, but it counts **files AND
directories** — a bundle of 199 files carrying 41 directories is 240 entries and
is refused. Size is not the constraint and never was.

| | cap | bundle |
|---|---|---|
| entries (files + directories) | 200 | **188** — 171 files + 17 directories |
| size | 30 MB | **4.76 MB** |

```bash
python wpp-es-html-deck/scripts/package_skill.py
# -> dist/wpp-es-html-deck.zip
```

The checkout is 329 files in 41 directories, so **the folder cannot be zipped by
hand**. The packager reports files, directories and the entry total on every run
and exits non-zero above either cap.

### What it drops

Authoring and provenance only; the repo keeps all of it.

| dropped | entries | why it is safe |
|---|---|---|
| `canon/<id>/{meta,spec,measure}.json` + `canon/_tools/` | 104 | Sources for the generated `CATALOG.md` / `catalog.json`, which is what the agent reads. `verify_deck.py` skips its canon checks by design when `_tools` is absent. |
| `canon/<id>/ref.png` | 25 | The source slide each template was traced from. |
| `canon/<id>/preview.png` → `canon/PREVIEWS.png` | 24 | One labelled contact sheet of all 25. |
| `scripts/{shoot_snippets,package_skill}.py` | 2 | Repo-side tooling. |

### What it restructures

Because a directory costs an entry, a directory holding one file is the most
expensive thing in the tree.

- **`canon/<id>/template.html` → `canon/templates/<id>.html`** — 25 directories
  holding one file each cost 50 entries; flat costs 26. `check_capacity.py`
  accepts both layouts, and the bundle's `SKILL.md` is patched to match.
- **`assets/icons/<name>.svg` → `assets/icons/<family>.md`** — 33 entries to 5.
  The families are §8.1's own, **parsed from the guideline rather than
  hardcoded** (the suite changed in v3.3 and v3.5, and shipping an icon under
  the wrong weight is what §8.1 calls "the most visible amateur tell"). §8.1's
  hard rule is one weight family per slide, so the agent reads exactly the
  family it already has to pick: ~8k tokens for the largest, against ~18k for
  one merged file. If the section stops parsing, icons ship ungrouped and the
  entry count fails loudly rather than mis-grouping them.

Snippets that said *"paste `assets/icons/rocket.svg`"* are repointed at
`assets/icons/solid.md (## rocket)` — one of those is `columns-v4.html`, a
variant the deck actually reads.

### Kept, having been cut once and put back

`assets/exemplars/` — SKILL.md attaches those four PNGs for the design-direction
checkpoint and re-reads one as the review bar; "never read into context" means
do not parse them as text. And the 13 `assets/snippets/*.html` —
`references/sections/12-archetypes.md` says *"assemble from"* them in nine
places, contradicting SKILL.md's ban on opening them at fill time. That is a
contradiction to resolve in the source, not by deletion.

Verified on every build: `check_capacity.py` canon and kit integrity,
`build_docs.py --check`, zip integrity, and a sweep for paths cited by a bundled
file but not present in it.

## Maintenance notes

**The design guideline exists in three forms.**
`WPP-ES-DESIGN-GUIDELINE.md` is the master; `references/sections/` is that same
file split by section for on-demand loading; `CORE.md` is the always-loaded
subset. This is deliberate — it keeps the token cost of a routine deck low —
but it means **an edit to the guideline must be applied to all three**. Always
edit the master first, then propagate. They are in sync as of the initial
commit.

**Assets are proprietary.** See [`NOTICE.md`](NOTICE.md). This repository is
private and must stay private.

## Licence

Proprietary and internal to WPP Enterprise Solutions | MAP. Not for
distribution. See [`NOTICE.md`](NOTICE.md).
