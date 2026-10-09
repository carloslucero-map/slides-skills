# Slides Skills — WPP Enterprise Solutions | MAP

Two Claude [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
that together turn raw context into a finished, on-brand presentation. They are
designed as a chain, and the recommended route is script first: one writes the
script, the other builds the slides from it.

```
raw notes / brief
      │
      ▼
┌─────────────────────┐   approved .md    ┌─────────────────────┐
│ deck-content-builder│ ────────────────► │  wpp-es-html-deck   │
│  (script-builder)   │  HANDOFF-CONTRACT │  (slides-builder)   │
│  writes the script  │                   │  renders the deck   │
└─────────────────────┘                   └─────────────────────┘
      │                                             │
      ▼                                             ▼
 slide-by-slide Markdown            a Claude Slides deck wherever it is on
 (also pastes into PowerPoint       (chat, Claude Design, Claude Code); else
  or Google Slides)                 one self-contained .html (16:9, offline)
```

Either skill can be used on its own. The handoff format between them is
specified in [`wpp-es-html-deck/references/HANDOFF-CONTRACT.md`](wpp-es-html-deck/references/HANDOFF-CONTRACT.md).

## Who owns what

**The design system owns what a deck looks like. The skills own how a deck gets
made.** The design system is "WPP Enterprise Solutions | MAP", a Design System
artifact in Claude Design (namespace `WppEsMap`): colour, type, the dot system,
the elements, the four fixed slides and the 76 layouts. It is edited there, and
only there.

It is the default, not the only one: a deck can be built in a MAP client's
design system instead, another Design System artifact in Claude Design, which
then owns that deck's look the same way (see [Client design systems](#client-design-systems)).
No other system is used or offered.

The skills hold the process: the gates, the plan, the content method, the copy
rules, the generator and the verifier. `wpp-es-html-deck` carries a **generated
copy** of the design system in `design-system/`, because its scripts cannot
reach Claude Design (see [The design system's copy](#the-design-systems-copy)).
The copy runs one way. Nothing in this repository writes to the design system,
and it is never re-synced from here.

## The skills

In the organisation they ship together as one plugin, **map-decks** (shown as
MAP Decks), where they are named **script-builder** and **slides-builder**,
and the two skills call each other by those names. slides-builder's first
question on raw notes recommends starting with script-builder. Here each SKILL.md's `name`
stays its folder's name; `authoring/build_plugin.py` gives them their
organisation names when it builds the plugin (see
[Uploading to claude.ai](#uploading-to-claudeai)).

### `deck-content-builder` (script-builder)
Writes the deck's **script**, its text content — action titles, bullets,
callouts, speaker notes — using consultant-grade methods (Pyramid Principle,
SCR). The recommended first step of every deck. Output is a single Markdown
script. It does not design or render anything.

Single file, no dependencies: [`deck-content-builder/SKILL.md`](deck-content-builder/SKILL.md).

### `wpp-es-html-deck` (slides-builder)
Renders a deck in the WPP ES | MAP visual language — Navy + Cream + Orange,
WPP Sans, the dot system, 16:9 — or in a MAP client's design system. **Wherever
Claude can make a Claude Slides deck (a chat, Claude Design, Claude Code) it
builds straight into one, from the design system itself, and on request makes
an animated HTML file from it, in any design system; only where Claude Slides
is not available does it write one self-contained HTML file from its copy of
the design system.** Ships 25 canon
templates, a 51-template snippet library, a per-slot capacity model, and a
verifier that enforces the design system's rules.

| Path | What it holds |
|---|---|
| `SKILL.md` | The skill itself — the operating instructions |
| `design-system/` | The generated copy of the design system: its `README.md`, the eleven `guidelines/`, every card in `cards/` (one file per group), the asset groups' notes, `tokens.json`, `bundle.css`, `fixed-slides.json`, `elements.json`, fonts, logos, icons, illustrations, photos, textures, exemplars, and `SOURCE.json` (version and a sha256 per file) |
| `references/HTML-BUILD.md` | The skill's own: how the HTML file is built, filled and checked, with the layout laws the verifier enforces |
| `references/SLIDES.md` | How to build in a Claude Slides deck, wherever one is available: the question card, the reading order, the install, the animated file |
| `references/DESIGN-SYSTEMS.md` | MAP's clients' design systems beside WPP ES \| MAP: which systems count, how one is picked, the four directions in any system, what the skill needs from it, how to fill what it lacks, what stays WPP-only, and the prompt that makes a client's system deck-ready |
| `scripts/animate_slides.py` | The animated HTML file: one self-contained file made from a finished Claude Slides deck, in any design system, with its transitions and builds plus the extras Slides cannot do |
| `references/MOTION.md` | Motion in Claude Slides for any design system: what Slides can do, the roles, and the quiet default for whatever a design system leaves unsaid |
| `references/SNIPPET-INDEX.md` | All 51 kit layouts, one line each |
| `references/capacity.json` | Per-slot min/ideal/max character counts |
| `references/HANDOFF-CONTRACT.md` | The content → render contract |
| `canon/` | The 25 traced templates and their catalogue |
| `assets/snippets/variants/` | The 51 kit layouts, one per file: the design system's slide under a measured capacity block |
| `scripts/` | Shell generator, capacity tooling, halftone generator, verifier, shared-block check, packager |

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

# Verify a deck against the design system's rules
python wpp-es-html-deck/scripts/verify_deck.py deck.html
python wpp-es-html-deck/scripts/verify_deck.py deck.html --screenshots shots/

# Check content against the per-slot capacity model (run from the skill folder)
cd wpp-es-html-deck && python3 scripts/check_capacity.py deck.html --skill .

# Remeasure capacity.json, the variants' capacity blocks and the snippet index (needs a built shell)
python3 scripts/build_shell.py --out /tmp/demo.html
python3 scripts/derive_capacity.py --skill . --demo /tmp/demo.html --write --index
python3 ../authoring/canon-tools/derive_canon_capacity.py --demo /tmp/demo.html --write

# Check that the blocks the two skills share still match (every verify runs it)
python3 scripts/check_shared_blocks.py
```

`verify_deck.py` exits 0 when every check passes (warnings allowed) and 1 on
any failure, so it drops into CI as-is.

## In a Claude Slides deck (a chat, Claude Design, Claude Code)

Slides is an Artifact **type**, available in a chat, in Claude Design and in
Claude Code: a deck is created from it and
written as `project/deck.json` plus one `project/slides/<id>.html` per slide, in
a closed inline-style subset — no classes, no `<style>`, no `var()`, images
uploaded rather than embedded. A self-contained HTML file is the opposite of
that, which is why decks used to land beside the Claude Slides deck instead of in
it.

The skill decides the surface before it builds. Where a Slides type is
available it skips `build_shell.py`, `check_capacity.py` and `verify_deck.py`
and builds from the design system itself:
[`references/SLIDES.md`](wpp-es-html-deck/references/SLIDES.md)
gives the order to read it in (the README, the guidelines, then the Elements
cards, each with its inline-style recipe for Slides, then the Fixed slides
cards, then the layout catalogue and the chosen layout's card) and how to
install it in the deck. It holds no brand values of its own.

Two things are specific to this path. **The plan gate is a question card**
(`AskUserQuestion`) wherever the session has one, because a question typed as
prose cannot be clicked there; without it, the same questions go in one short
message.
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

**Motion is Slides' own, and the design system's.** A Claude Slides deck
moves with the type's transitions (`fade`, `push`, `magic`) and builds
(`rise`, `fade`, `pop`, `left`, `right`), which play when the deck is
presented. The design system in use decides how they are used: WPP ES | MAP
does it in guideline 10, *In Claude Slides*, which maps the HTML deck's five
motion hooks onto them per motion level. The skill keeps only the part that
holds for any design system, in
[`references/MOTION.md`](wpp-es-html-deck/references/MOTION.md): what Slides
can do, the roles every slide's elements play, and a quiet default for
whatever a system leaves unsaid, so a client's design system with no motion
rules still gets a deck that moves well, and one with its own rules gets
those. A build works only on an element pinned directly on the slide, so
whatever moves is pinned.

## The animated HTML file

Every deck's question card asks whether the Claude Slides deck should come with
an animated HTML file, in every design system. The file is made from the
finished Claude Slides deck by
[`scripts/animate_slides.py`](wpp-es-html-deck/scripts/animate_slides.py): the
deck's own slides, pixel for pixel, with their transitions and builds played in
the browser (magic move as a real morph), plus extras Claude Slides cannot do:
units arriving one after another, figures counting up, and where the brand's
motion rules allow more than rise and fade, rules drawing on, titles rising
word by word and art drifting. Every picture and font is embedded, so the file
works offline. The Claude Slides deck stays the deck to edit, share and export;
after a change, the file is made again. (Where Claude Slides is not available,
the WPP HTML path's own runtime, `HTML-BUILD.md` §14, does the motion.)

## Client design systems

WPP ES | MAP is the default design system, and a MAP client's Design System
artifact in Claude Design can take its place. No other system is used or
offered (not MAP's own product or team systems, nor untitled ones).
[`references/DESIGN-SYSTEMS.md`](wpp-es-html-deck/references/DESIGN-SYSTEMS.md)
holds the rules:

- **Which system:** the open deck's own (a revision stays on its brand), else
  the brand the user names ("a deck in Acme's brand", "a MAP deck"); with no
  brand named, the question card asks, WPP ES | MAP first, then each client
  system. It also asks when the name fits two client systems, or a client has
  none.
- **The four directions** (Editorial quiet, Statement-led, Data-forward,
  High-impact) are asked for every deck: in a client's system each one picks
  among that system's own grounds, layouts and type.
- **What the skill needs from it:** a README, colour tokens by role, at most
  four font faces, a logo; ideally also a section for Claude Slides, element
  recipes, the four fixed slides, a layout catalogue and motion rules. Where
  a part is missing the skill fills it from the system's own colours, type and
  logo, never from WPP's, and says so at delivery.
- **What stays WPP-only:** WPP's non-negotiables 2 to 8, the canon and kit,
  and the HTML path. A client's deck is always a Claude Slides deck (with its
  animated file when asked for), following that client's own rules.
- **Making a client's system deck-ready:** the prompt at the end of that page,
  pasted into the system in Claude Design, adds what decks need (including
  its motion rules for Claude Slides) and lists what is missing.

## The design system's copy

The HTML path's scripts run in Claude Code, in a claude.ai sandbox or from an
uploaded zip, and none of them can reach Claude Design. So `wpp-es-html-deck`
ships a copy of the design system in `design-system/`, and the rule for it is
strict: **generated by a script, stamped with the version, never edited by
hand, and checked.**

- [`authoring/refresh_design_system.py`](authoring/refresh_design_system.py)
  is the only writer. An agent that can read the design system saves its files
  and assets with the Artifact tool, then runs the script with `--write`. It
  writes the README, the guidelines, every card (one file per group) and the
  asset groups' notes, which are what the model reads; the tokens, the
  stylesheet, the fonts and asset groups, the icon family files,
  `fixed-slides.json` (colourways, both outros, the covers, the agenda's row
  placement, the dot presets and each direction's default colourway and
  motion, read from the Fixed slides and DotField cards, the previews and the
  README), `elements.json` (the closed list of fine-print roles, from
  the BodyCopy card), every layout's `<section>`, and the canon catalogue's
  text; and it records the version and a sha256 per file in `SOURCE.json`.
  `--check` exits 1 when the copy has drifted, and both modes warn when the
  design system's catalogue stops quoting a layout card.
- `build_shell.py` builds every deck from the copy: `:root` from the tokens, the
  whole stylesheet from `bundle.css`, the fixed slides from `fixed-slides.json`.
- `verify_deck.py` fails the deck when any file in `design-system/`, or any
  layout's `<section>`, no longer matches `SOURCE.json`, and takes the palette,
  the grounds and the fine-print roles from the copy.

Everything a deck shows comes from the copy: `build_shell.py` holds no colour,
size, position, dot or per-direction default of its own, only the fixed
slides' words in each language (Agenda, Thank you., Section N, the
confidential line). And the model reads the brand from the copy too, so there
is no second, hand-kept version of the rules in the skill: its own
`references/HTML-BUILD.md` says only how the HTML file is built and checked.

## Uploading to claude.ai

### The organisation installs one plugin, map-decks

Build it from the latest commit:

```bash
python3 authoring/build_plugin.py --out ~/Downloads
# writes ~/Downloads/map-decks-<version>.zip
```

It holds both skills under the names people use, `skills/slides-builder/` and
`skills/script-builder/`, beside `.claude-plugin/plugin.json` and a short
README. It is built from a commit (`git archive`), never the working copy, and
takes its version from the newest release in this CHANGELOG. It checks
claude.ai's plugin limits, **5,000 files and 200 MB** (now 172 files, 4.9 MB),
and runs `claude plugin validate` when the Claude Code CLI is installed.

An Owner uploads it in **Organization settings > Plugins & skills**: **Add >
Upload a plugin** the first time, then **Upload new version** from the
plugin's menu for each release. **Default access** decides who gets it:
**Installed by default** or **Required** puts it in front of everyone. Every
upload stays in the plugin's **Version history**, and **Revert to this
version** rolls back. To try a build before the organisation sees it, upload it
to your own account from **Customize > Plugins > Add > Upload plugin**.

### One skill on its own

claude.ai caps an uploaded skill at **200 entries and 30 MB**. The error reads
*"Zip contains too many files (maximum 200)"*, but it counts **files AND
directories** — 199 files in 41 directories is 240 entries and is refused.

**`wpp-es-html-deck/` is the skill.** It is kept under the cap by where things
live, not by a build step, so zipping the folder is a valid upload:

| | cap | now |
|---|---|---|
| entries (files + directories) | 200 | **187** — 169 files + 18 directories |
| size | 30 MB | **4.84 MB** |

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
file the most expensive thing in a tree. Three layouts follow from that:

- **`canon/templates/<id>.html`** — one directory for 25 templates, not 25
  directories holding one file each. 50 entries down to 26.
- **`design-system/icons/<family>.md`** — the 32 icons grouped into four files by
  the design system's own weight families, each icon under its own `##` heading.
  33 entries down to 5. The hard rule is one weight family per slide, so the agent reads
  exactly the family it already has to pick: ~8k tokens for the largest, against
  ~18k if all 32 were merged into a single file.
- **`design-system/cards/<group>.md`** — the design system's 98 cards in ten
  files, one per group (the elements, the fixed slides, each layout family),
  each card under its own `#` heading. 196 entries down to 11.

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

**The skill keeps no copy of the brand rules of its own.** It reads the design
system's README, guidelines and cards from `design-system/`, and
`references/HTML-BUILD.md` holds only the HTML mechanics: the self-contained
file, the kit's composition recipes and checklist, the runtime, and the layout
laws as the verifier measures them. It keeps the old guideline's section
numbers, which the verifier's messages and the layouts' comments cite, and a
table of where every other number went. The old downstream guideline
(`references/sections/`, `CORE.md` and the whole guideline in `build/`) was
retired in 4.2.0.

**Two blocks are shared between the skills**, the house copy rules and the
handoff contract, each written once per skill.
`scripts/check_shared_blocks.py`, which every verify runs, fails when the two
copies of either differ.

**Assets are proprietary.** See [`NOTICE.md`](NOTICE.md). This repository is
private and must stay private.

## Licence

Proprietary and internal to WPP Enterprise Solutions | MAP. Not for
distribution. See [`NOTICE.md`](NOTICE.md).
