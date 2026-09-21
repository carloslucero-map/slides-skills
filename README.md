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

claude.ai caps an uploaded skill at **30 MB**. The checkout is ~55 MB, so build
the bundle rather than zipping the directory:

```bash
python wpp-es-html-deck/scripts/package_skill.py
# -> wpp-es-html-deck/dist/wpp-es-html-deck.zip  (~15 MB)
```

The repo is not modified. The script stages a second tree that drops the two
authoring-only directories and re-encodes the canon reference imagery, then
refuses to write a bundle over the limit (`--limit`, `--check`, `--no-zip`).

| Left out of the bundle | Why |
|---|---|
| `canon/_shots/` (14 MB) | Contact sheets `shoot_snippets.py` writes. Never read while building a deck. |
| `canon/_ref/` (14 MB) | Renders and measurements of the source deck the canon was traced from. Authoring input. |
| `__pycache__/`, `.DS_Store` | Junk. |

`canon/<id>/ref.png` and `preview.png` are re-encoded at 1568 px wide with a
256-colour palette — 21 MB down to 11 MB, **same filenames**, so `CATALOG.md`,
`meta.json` and `spec.json` keep pointing at files that exist. 1568 px is the
width an image is downsampled to before a model sees it, and the palette is
generous for a deck drawn in three brand colours plus duotone photography, so
the one job these images have — being compared against a fill that came out
wrong — is unaffected. `assets/` is copied byte-for-byte: those pixels ship
inside delivered decks.

Keep the full checkout for anything that re-derives the canon or feeds design
work. The bundle is for upload only.

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
