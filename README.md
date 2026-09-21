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

## Size, and uploading to claude.ai

claude.ai takes a skill at **30 MB**. Two numbers have to stay under that, and
they are not the same number:

| | | |
|---|---|---|
| the skill directory | 26.95 MB | what you get zipping `wpp-es-html-deck/` by hand |
| the bundle | 14.83 MB | what `package_skill.py` writes to `dist/` |

The directory is the one that bites — it is the obvious thing to zip, and it was
55 MB until the authoring material moved to [`authoring/`](authoring/README.md)
at the repo root. Nothing under `authoring/` is read while a deck is being
built; it is what the canon is re-derived from and what design work reads, so it
stays in the repo, just not inside the skill.

Build the bundle for upload:

```bash
python wpp-es-html-deck/scripts/package_skill.py
# -> dist/wpp-es-html-deck.zip   (one top-level folder, SKILL.md at its root)
```

It reports **both** sizes against the cap on every run and exits non-zero if
either is over, so a regression surfaces at packaging time rather than at upload
time. It refuses `--out` anywhere inside the skill directory, for the obvious
reason. `--check` reports without writing, `--limit` tightens the budget,
`--no-zip` leaves the staged tree.

The extra 12 MB of headroom comes from re-encoding `canon/<id>/ref.png` and
`preview.png` at 1568 px wide with a 256-colour palette, **keeping the
filename** — `CATALOG.md`, `meta.json` and `spec.json` all name `ref.png`, and
renaming to `.jpg` would point 25 templates' provenance at a file that does not
exist. 1568 px is the width an image is downsampled to before a model sees it,
and the palette is generous for a deck drawn in three brand colours plus duotone
photography, so the one job those images have — being compared against a fill
that came out wrong — is unaffected. `assets/` is copied byte-for-byte: those
pixels ship inside delivered decks.

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
