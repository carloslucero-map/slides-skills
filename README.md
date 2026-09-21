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
directories** — 199 files in 41 directories is 240 entries and is refused.

**`wpp-es-html-deck/` is the skill.** It is kept under the cap by where things
live, not by a build step, so zipping the folder is a valid upload:

| | cap | now |
|---|---|---|
| entries (files + directories) | 200 | **190** — 173 files + 17 directories |
| size | 30 MB | **5.54 MB** |

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
- **`assets/icons/<family>.md`** — the 32 icons grouped into four files by
  §8.1's own weight families, each icon under its own `##` heading. 33 entries
  down to 5. §8.1's hard rule is one weight family per slide, so the agent reads
  exactly the family it already has to pick: ~8k tokens for the largest, against
  ~18k if all 32 were merged into a single file.

Everything the skill was *made from* lives in [`authoring/`](authoring/README.md)
at the repo root — the canon sources, the tools that generate `CATALOG.md`, the
individual icon SVGs, the contact sheets. Nothing there is read while a deck is
being built, and `verify_deck.py` skips its canon checks when it is absent,
which is the normal state of an installed skill.

`package_skill.py` reports files, directories and the entry total on every run
and exits non-zero above either cap, so a regression surfaces here rather than
at upload time.

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
