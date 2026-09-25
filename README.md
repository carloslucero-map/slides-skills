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
 slide-by-slide Markdown            in Claude Design: the Slides artifact
 (also pastes into PowerPoint       elsewhere: one self-contained .html
  or Google Slides)                 (16:9, keyboard-navigable, no external assets)
```

Either skill can be used on its own. The handoff format between them is
specified in [`wpp-es-html-deck/references/HANDOFF-CONTRACT.md`](wpp-es-html-deck/references/HANDOFF-CONTRACT.md).

## Who owns what

**The design system owns what a deck looks like. The skills own how a deck gets
made.** The design system is "WPP Enterprise Solutions | MAP", a Design System
artifact in Claude Design (namespace `WppEsMap`): colour, type, the dot system,
the elements, the four fixed slides and the 76 layouts. It is edited there, and
only there.

The skills hold the process: the gates, the plan, the content method, the copy
rules, the generator and the verifier. `wpp-es-html-deck` carries a **generated
copy** of the design system in `design-system/`, because its scripts cannot
reach Claude Design (see [The design system's copy](#the-design-systems-copy)).
The copy runs one way. Nothing in this repository writes to the design system,
and it is never re-synced from here.

## The skills

### `deck-content-builder`
Writes the **text content** of a deck — action titles, bullets, callouts,
speaker notes — using consultant-grade methods (Pyramid Principle, SCR).
Output is a single Markdown file. It does not design or render anything.

Single file, no dependencies: [`deck-content-builder/SKILL.md`](deck-content-builder/SKILL.md).

### `wpp-es-html-deck`
Renders a deck in the WPP ES | MAP visual language — Navy + Cream + Orange,
WPP Sans, the dot system, 16:9. **In Claude Design it builds straight into the
Slides artifact, from the design system itself; everywhere else it writes one
self-contained HTML file from its copy of the design system.** Ships 25 canon
templates, a 51-template snippet library, a per-slot capacity model, and a
verifier that enforces the design guideline.

| Path | What it holds |
|---|---|
| `SKILL.md` | The skill itself — the operating instructions |
| `design-system/` | The generated copy of the design system: `tokens.json`, `bundle.css`, `fixed-slides.json`, fonts, logos, icons, illustrations, photos, textures, exemplars, and `SOURCE.json` (version and a sha256 per file) |
| `references/CLAUDE-DESIGN.md` | How to build in Claude Design: the question card, the reading order, the install |
| `references/CORE.md` | The always-loaded subset of the design guideline, the skill's downstream copy of the brand rules |
| `references/sections/` | That guideline split by section, loaded on demand; the one place to edit it |
| `build/WPP-ES-DESIGN-GUIDELINE.md` | The whole guideline in one file, generated like `CORE.md` |
| `references/SNIPPET-INDEX.md` | All 51 kit layouts, one line each |
| `references/capacity.json` | Per-slot min/ideal/max character counts |
| `references/HANDOFF-CONTRACT.md` | The content → render contract |
| `canon/` | The 25 traced templates and their catalogue |
| `assets/snippets/` | The 51 kit layouts, one per file in `variants/`, and their 13 authoring sources |
| `scripts/` | Shell generator, capacity tooling, halftone generator, guideline builder, verifier, packager |

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

# Check content against the per-slot capacity model (run from the skill folder)
cd wpp-es-html-deck && python3 scripts/check_capacity.py deck.html --skill .

# Regenerate capacity.json, the snippet index and the variants (needs a built shell)
python3 scripts/build_shell.py --out /tmp/demo.html
python3 scripts/derive_capacity.py --skill . --demo /tmp/demo.html --write --index --split
python3 ../authoring/canon-tools/derive_canon_capacity.py --demo /tmp/demo.html --write

# Regenerate CORE.md and the whole guideline from references/sections/
python3 scripts/build_docs.py --write
```

`verify_deck.py` exits 0 when every check passes (warnings allowed) and 1 on
any failure, so it drops into CI as-is.

## In Claude Design

Claude Design's slides are an Artifact **type**: a deck is created from it and
written as `project/deck.json` plus one `project/slides/<id>.html` per slide, in
a closed inline-style subset — no classes, no `<style>`, no `var()`, images
uploaded rather than embedded. A self-contained HTML file is the opposite of
that, which is why decks used to land beside the Slides artifact instead of in
it.

The skill decides the surface before it builds. Where a Slides type is
available it skips `build_shell.py`, `check_capacity.py` and `verify_deck.py`
and builds from the design system itself:
[`references/CLAUDE-DESIGN.md`](wpp-es-html-deck/references/CLAUDE-DESIGN.md)
gives the order to read it in (the README, then the Elements cards, each with
its inline-style recipe for Slides, then the Fixed slides cards, then the layout
catalogue and the chosen layout's card), how to install it in the deck, and the
few Slides rules the design system does not carry yet. It holds no brand values
of its own.

Two things are specific to this surface. **The plan gate is a question card**
(`AskUserQuestion`), because a question typed as prose cannot be clicked there.
**No slide is ever posted as an image**: the draft is the deck in the editor.
`deck-content-builder` keeps its approved content in the conversation rather
than saving a stray `.md`.

**Fonts are the subtle part.** The Slides format loads one file per face, at
most four, and renders a one-weight file at that weight whatever `font-weight`
asks for. WPP is five static files under one name, so installed naively every
tier — Thin display, Light headline, Regular body, Medium label — comes out the
same. The design system registers four faces instead (`WPP` for Regular,
`WPP Thin`, `WPP Light`, `WPP Medium`) with `font-weight:400` everywhere; Bold,
a fifth face, does not load, and the footer brand line moves to Medium.

## The design system's copy

The HTML path's scripts run in Claude Code, in a claude.ai sandbox or from an
uploaded zip, and none of them can reach Claude Design. So `wpp-es-html-deck`
ships a copy of the design system in `design-system/`, and the rule for it is
strict: **generated by a script, stamped with the version, never edited by
hand, and checked.**

- [`authoring/refresh_design_system.py`](authoring/refresh_design_system.py)
  is the only writer. An agent that can read the design system saves its files
  and assets with the Artifact tool, then runs the script with `--write`. It
  writes the tokens, the stylesheet, the fonts and asset groups, the icon family
  files, `fixed-slides.json` (colourways, the light outro, cover art and dot
  presets, read from the Fixed slides cards and previews), every layout's
  `<section>`, and the canon catalogue's text, and records the version and a
  sha256 per file in `SOURCE.json`. `--check` exits 1 when the copy has drifted.
- `build_shell.py` builds every deck from the copy: `:root` from the tokens, the
  whole stylesheet from `bundle.css`, the fixed slides from `fixed-slides.json`.
- `verify_deck.py` fails the deck when any file in `design-system/`, or any
  layout's `<section>`, no longer matches `SOURCE.json`.

Almost everything a deck shows now comes from the copy, the logos, both outros,
all five covers and the agenda's row placement included. What the design system
does not hold yet stays in `build_shell.py`, marked "not in the design system
yet": the classic divider's second and third dot colours and two content-slide
dot fields (`field-mid`, `field-macro`).

## Uploading to claude.ai

claude.ai caps an uploaded skill at **200 entries and 30 MB**. The error reads
*"Zip contains too many files (maximum 200)"*, but it counts **files AND
directories** — 199 files in 41 directories is 240 entries and is refused.

**`wpp-es-html-deck/` is the skill.** It is kept under the cap by where things
live, not by a build step, so zipping the folder is a valid upload:

| | cap | now |
|---|---|---|
| entries (files + directories) | 200 | **195** — 177 files + 18 directories |
| size | 30 MB | **4.98 MB** |

```bash
python wpp-es-html-deck/scripts/package_skill.py
# checks both caps, then writes dist/wpp-es-html-deck.zip
```

Or zip it yourself — **from a terminal, not from Finder**:

```bash
zip -rX wpp-es-html-deck.zip wpp-es-html-deck -x '*.DS_Store'
```

### Do not use Finder's right-click → Compress

macOS writes a `__MACOSX/._name` shadow entry for every file carrying an
extended attribute, and **every file in a folder extracted from an internet
download carries `com.apple.quarantine`** — so a GitHub source download,
unzipped and re-compressed in Finder, is the worst case. Measured on this skill:
**410 extra entries**, and running `xattr -cr` first does not prevent it. Only
`zip -X` (or `package_skill.py`, which writes the archive with Python's
`zipfile`) avoids it.

Check any zip before uploading:

```bash
python3 -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); f=[n for n in z.namelist() if not n.endswith('/')]; d={'/'.join(n.split('/')[:i+1]) for n in f for i in range(len(n.split('/'))-1)}; c=[n for n in z.namelist() if '__MACOSX' in n or n.rsplit('/',1)[-1].startswith('._')]; print(f'{len(f)} files + {len(d)} dirs = {len(f)+len(d)} entries (cap 200), {len(c)} mac cruft')" wpp-es-html-deck.zip
```

### What keeps it under the cap

A directory costs an entry, same as a file, which makes a directory holding one
file the most expensive thing in a tree. Two layouts follow from that:

- **`canon/templates/<id>.html`** — one directory for 25 templates, not 25
  directories holding one file each. 50 entries down to 26.
- **`design-system/icons/<family>.md`** — the 32 icons grouped into four files by
  the design system's own weight families, each icon under its own `##` heading.
  33 entries down to 5. The hard rule is one weight family per slide, so the agent reads
  exactly the family it already has to pick: ~8k tokens for the largest, against
  ~18k if all 32 were merged into a single file.

Everything the skill was *made from* lives in [`authoring/`](authoring/README.md)
at the repo root — the canon sources, the tools that generate `CATALOG.md` and
the design-system copy, the individual icon SVGs, the contact sheets. Nothing there is read while a deck is
being built, and `verify_deck.py` skips its canon checks when it is absent,
which is the normal state of an installed skill.

`package_skill.py` reports files, directories and the entry total on every run
and exits non-zero above either cap, so a regression surfaces here rather than
at upload time.

## Maintenance notes

**A brand change starts in the design system.** Edit it in Claude Design, then
refresh the copy (`authoring/refresh_design_system.py --write`) and commit. Never
edit `design-system/` or a layout's `<section>` in the repo: `verify_deck.py`
fails the deck, and the next refresh would undo it.

**The design guideline is the skill's downstream copy, in three forms.**
`references/sections/` is the one place to edit it; `references/CORE.md` (the
always-loaded subset) and `build/WPP-ES-DESIGN-GUIDELINE.md` (the whole of it)
are generated from it by `scripts/build_docs.py --write`, and `--check` fails
when either has drifted. When the design system changes a rule, change
`sections/` to match. Retiring this copy in favour of one generated from the
design system is planned separately.

**Two blocks are shared between the skills**, the house copy rules and the
handoff contract, each written once per skill. `build_docs.py --check` fails
when the two copies of either differ.

**Assets are proprietary.** See [`NOTICE.md`](NOTICE.md). This repository is
private and must stay private.

## Licence

Proprietary and internal to WPP Enterprise Solutions | MAP. Not for
distribution. See [`NOTICE.md`](NOTICE.md).
