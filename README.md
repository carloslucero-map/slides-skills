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

claude.ai enforces two limits on an uploaded skill, and **the binding one is
file count, not size**:

| | limit | bundle |
|---|---|---|
| files | 200 | **199** |
| size | 30 MB | **4.77 MB** |

```bash
python wpp-es-html-deck/scripts/package_skill.py
# -> dist/wpp-es-html-deck.zip   (one top-level folder, SKILL.md at its root)
```

The checkout is 329 files, so the folder cannot be zipped by hand — it is
rejected on count long before size matters. The packager drops only what a deck
build never reads, and the repo keeps all of it:

| dropped | files | why it is safe |
|---|---|---|
| `canon/<id>/{meta,spec,measure}.json` + `canon/_tools/` | 104 | Sources for the generated `CATALOG.md` / `catalog.json`, which is what the agent actually reads. `verify_deck.py` skips its canon checks by design when `_tools` is absent. |
| `canon/<id>/ref.png` | 25 | The source slide each template was traced from. Provenance, not instruction. |
| `canon/<id>/preview.png` → `canon/PREVIEWS.png` | 25 → 1 | One labelled contact sheet of all 25. Choosing happens on the catalogue's `use when` column; the sheet is the second opinion. |
| `scripts/{shoot_snippets,package_skill}.py` | 2 | Repo-side tooling; nothing in the bundle invokes either. |

**What is deliberately kept**, having been cut once and put back:
`assets/exemplars/` (SKILL.md attaches those four PNGs for the design-direction
checkpoint and re-reads one as the review bar — "never read into context" means
do not parse them as text, not that they are optional) and the 13
`assets/snippets/*.html` authoring sources (`references/sections/12-archetypes.md`
says *"assemble from"* them, which contradicts SKILL.md's ban on opening them at
fill time — a contradiction to resolve in the source, not by deletion).

Verified on every build: `check_capacity.py` canon and kit integrity,
`build_docs.py --check`, and a sweep for paths cited by a bundled file but not
present.

**One file of headroom.** The 26th canon template breaks the upload, and the
catalogue already names families the canon does not cover. `package_skill.py`
exits non-zero above the cap and prints the consolidation levers — the useful
one is `assets/icons/`, 32 files, but note that merging all 32 into one costs
~18k tokens to read against ~2k for the icons a deck uses, so split by weight
family rather than into a single file.

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
