# Changelog

All notable changes to these skills are recorded here.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [4.4.0] — 2026-10-07

Claude Slides first, wherever it is available. The skills used to say "in
Claude Design" where they meant "wherever Claude can make a Claude Slides
deck", and the rule that picks the deliverable listed Claude Code as an
HTML-only surface. A chat with Claude Slides on, Claude Design and Claude Code
all get a Claude Slides deck now; the self-contained HTML file is only for where
Claude Slides is not available.

### Changed
- slides-builder decides between the **Claude Slides path** (the default:
  any session whose Artifact tool offers a Slides type, checked with
  `quickstart` when unsure) and the **HTML path** (only where there is none).
  The description, the gates, delivery, revising and the edge cases say so.
- `references/CLAUDE-DESIGN.md` is now **`references/SLIDES.md`**. Asking
  uses the question card where the session has `AskUserQuestion`; where it
  does not, the same questions go in one short message, still with no slide
  table.
- deck-builder keeps its approved content in the conversation and asks with
  the card on the same terms, wherever Claude Slides is available.
- The plugin's description and README say Claude Slides first, HTML otherwise.

### Changed, in the design system (now version `1791385252-da14`)
- Rule 8 of the README: wherever Claude can make a Claude Slides deck (a
  chat, Claude Design or Claude Code), the deck is built in Claude Slides;
  only where Claude Slides is not available does the slides-builder skill in
  the MAP Decks plugin write one self-contained HTML file. It used to send
  everything outside Claude Design to HTML.
- "Claude Design Slides" is now "Claude Slides", the product's name, in 105
  places: every card's recipe heading, the README's *Building in Claude
  Slides*, guidelines 03, 08 and 10, the logo notes and one token note.

The skill's copy is refreshed to that version; no layout, fixed slide or
value changed, and decks build exactly as before.

## [4.3.0] — 2026-10-07

### Added
- **map-decks**, one plugin holding both skills, for the organisation to
  install in place of two separate skills. Inside it they carry the names
  people use, slides-builder and deck-builder, so nothing has to be renamed at
  upload, and the two always ship at the same version. An Owner uploads it once
  in Organization settings > Plugins & skills and can set it to Installed by
  default or Required, so everyone has it without turning anything on.
- `authoring/build_plugin.py` builds it: `map-decks-<version>.zip`, from a
  commit, checked against claude.ai's plugin limits (5,000 files, 200 MB; it is
  169 files, 4.9 MB) and by `claude plugin validate`.

The skills themselves are unchanged. Anthropic's plugin pages list chat, Cowork
and Claude Code and do not mention Claude Design, so try the plugin on your own
account in a chat and in a Claude Design deck before the organisation gets it,
and remove the two separate skills only after that.

## [4.2.3] — 2026-10-07

### Changed, in the design system (now version `1791378973-10da`)
- The README's rule 8 names the HTML skill **slides-builder**, its name in
  the organisation, where it said `wpp-es-html-deck`. Guideline 11 still says
  `wpp-es-html-deck` where it means the repository folder, which is right.

The skill's copy of the design system is refreshed to that version: its
README and `SOURCE.json` are the only files that changed. Decks build exactly
as before.

## [4.2.2] — 2026-10-07

### Fixed
- The two skills call each other by the names they have in the
  organisation, **slides-builder** and **deck-builder**. deck-builder used to
  tell Claude to hand its content to `wpp-es-html-deck`, a skill nobody in the
  organisation has under that name, so the hand-off after "now make the
  slides" depended on Claude guessing.

The `name` in each SKILL.md stays the folder's name (`wpp-es-html-deck`,
`deck-content-builder`): a skill's name has to match the folder it is uploaded
in, so a folder downloaded from GitHub still uploads as before. Decks build
exactly as before.

## [4.2.1] — 2026-09-27

The six leftovers 4.2.0 listed, fixed in the design system, and the skill
following them.

### Fixed, in the design system (now version `1790526555-cad0`)
- Two traced layouts set labels in Orange 600, which is on no list of orange
  text. Both now follow their source slides: SeqPhasePanels3's phase labels
  are Orange 700 (the traced layouts' measured orange), SeqStepsPanels5's
  "Activities" and "Deliverables" labels are White. The rule's wording is
  clearer too: Orange 600 is never a ground for text.
- ProcessTimelineV4, rebuilt. Its nodes sat outside the line, so they rendered
  at the slide's top edge; a dot of its field covered the last label; and its
  lower half was empty. The nodes and labels now sit inside the line, the line
  runs through the middle of the band, a takeaway anchors the bottom, and the
  example dates are four even quarters. Like the other two timelines it
  declares its air. It passes the verifier; its copy grows to 158 characters,
  213 at most (was 126 and 170).
- EntTeamRow6's preview no longer calls its headline orange.
- The README carries the chart-label rule for Slides (a chart's labels are
  `<p>` elements pinned over its svg) and a new *Four deck directions* table:
  what each direction changes, with its default divider colourway, motion and
  outro. Its poster statements run to 220 px, as the type scale says; the
  skill's table had said 260.
- No old guideline section number is left in the design system: 137 citations
  in the stylesheet, the 76 layout previews and seven cards now name the
  guideline or card that holds the rule.

### Changed, in the skill
- `build_shell.py` takes the four directions and each one's default colourway
  and motion from the copy (the refresh reads the README's table into
  `fixed-slides.json`). 4.2.0 said the generator wrote no brand value; it
  still held those defaults. What it writes itself now is only the fixed
  slides' words in each language.
- `SKILL.md` points at the design system's directions table instead of keeping
  its own, and `CLAUDE-DESIGN.md` drops its last Slides note.
- Five kit capacity labels lose their section numbers, in step with their
  cards.

Decks build as before: across the 1,449 spec combinations the output differs
from 4.2.0 only in the stylesheet's comments.

## [4.2.0] — 2026-09-25

The skill stops keeping a copy of the brand of its own. It reads the design
system's README, guidelines and cards from its copy of the design system, and
the guideline it used to keep in step by hand is gone.

### Added, in the design system (now version `1790341061-1a78`)
- The 56 rules the skill's old guideline held and the design system did not,
  approved as listed on the coverage review: print values for the palette;
  dark slides and ghost numerals on Navy; contrast measured against what is
  behind the text; a section of layout laws in guideline 03 (the content
  edge, the headline and footer bands, overlaps, clearances, alignment,
  balance, deck rhythm); when a slide may carry dots or a motif, and which
  one; the motion details (defaults by direction, ambient motion, word by word,
  step-by-step reveals, no invented animation); the fixed slides' limits (six
  chapters of about 45 characters, a cover title of two to four words, the
  optional contact, "Gracias."); the classic divider's second and third dot
  colours; and the `field-mid` and `field-macro` dot fields.
- Eleven decisions, as recommended. Dark slides by direction, stated once. A
  full-bleed motif on posters and stat backdrops, and on any slide of a
  high-impact deck. No dots over photos. The stricter rule for body copy over
  halftones. The composition checklist stays the HTML deck's art pass. The
  progress line as the one exception to "no accent bars". EntTeamRow6's
  headline in Navy, QuantStatGrid5's highlight by weight only, and the traced
  layouts' measured orange labels listed as an exception. The Venn redrawn
  flat. The four identical icon pairs noted. Orange 700 for the halftones.
  Two layout forms that never shipped dropped.
- Eleven corrections where the design system contradicted itself or the
  stylesheet: the divider title is 136 px, Big Statements run to 220 px, one
  hue per register field (the corner presets mix up to three), the agenda's
  scatter, Cream icons on Navy, the KPI label, the pinned card link, circles
  first and bars when needed, hover and the motion durations, the takeaway's
  brackets, and the token notes.

### Changed, in the skill
- **The model reads the design system's own words.** The refresh copies the
  README, the eleven guidelines, every card (one file per group in
  `design-system/cards/`) and the asset groups' notes
  (`design-system/asset-notes.md`), verbatim and hash-checked like the rest of
  the copy. `SKILL.md` has the model read the README, guidelines 01 to 04 and
  06 and the new `references/HTML-BUILD.md` before building, and another
  guideline or a card only when its trigger fires. A layout's card, with what
  it deviates from on purpose, is now at hand on the HTML path too.
- **`references/HTML-BUILD.md`** is the skill's own file: how the HTML deck is
  built, filled, run and checked. It keeps the old guideline's section numbers
  for those parts (§2a, §12.14 to §12.15a, §13, §13.4, §14, §15), which the
  verifier and the layouts cite, and says where every other number went. Lines
  the design system or the code had overtaken are corrected on the way: the
  type floor as the verifier measures it, the card link as the kit ships it (a
  text link, not a pill), the flat Venn, the motion durations and hover, the
  recipes' files in `variants/`.
- `build_shell.py` takes the classic divider's dot colours and the mid and
  macro fields from the copy, so no brand value is written in the generator.
- `build_docs.py` is now `check_shared_blocks.py`. It only checks that the
  house copy rules and the handoff contract still match `deck-content-builder`,
  and every verify still runs it.
- The verifier's messages, the generator's comments, the capacity scripts and
  the templates' own headers cite the design system (guideline 02, the
  Headline card) instead of retired section numbers. The design system's own
  previews still cite some; `HTML-BUILD.md` resolves them.
- `CLAUDE-DESIGN.md` adds the guidelines to the reading order in Claude Design,
  and falls back on `design-system/` when the design system cannot be found.
- QuantStatGrid5's capacity loses the orange accent slot the design system
  removed.

### Removed
- The skill's downstream guideline: `references/sections/` (20 files),
  `references/CORE.md`, `build/WPP-ES-DESIGN-GUIDELINE.md` and the stub at
  `references/WPP-ES-DESIGN-GUIDELINE.md`. With the copy's new files the skill
  is 184 entries and 4.84 MB (183 and 4.85 MB before).

### Known issues, all in the design system
- Two traced layouts set labels in Orange 600, which the design system says
  never carries text: SeqPhasePanels3's phase arcs and SeqStepsPanels5's step
  labels. The measured-orange exception covers Orange 700 only.
- ProcessTimelineV4 still fails two verifier checks as it is (see 4.1.3).
- EntTeamRow6's preview still calls its headline orange in a CSS comment.
- The chart-label rule for Slides is still only in `CLAUDE-DESIGN.md`.

Decks build as before: across the 1,449 spec combinations the output differs
only in the flat Venn's two rules and in comments and the placeholder slide's
hint that named retired sections. The demo deck's verifier transcript is
unchanged apart from the same wording.

## [4.1.3] — 2026-09-25

The remaining design-system items from the alignment audit, and the kit's
authoring sources retired.

### Added, in the design system (now version `1790337247-f9ce`)
- A **Photo** element. It gives the navy duotone as a Slides recipe (a Navy
  box, the image inside with a grayscale filter and a screen blend), says which
  photos take it (a brief's photos do; the thirteen library photos are already
  duotone and go in as they are), and states the anchoring rule for photos of
  200 × 200 px or more.
- The Motion guideline's Slides rules: fade on every slide, push between
  chapters, build-ins on pinned children only, none with motion off.
- BodyCopy's closed list of fine-print roles, the only text allowed between 16
  and 20 px. Besides the fourteen roles the verifier knew, it names the four
  the design system already set that small: the table header, the card link,
  the timeline label and the milestone note.

### Changed, in the design system
- The README catalogue quotes each layout card's *When to use it* word for
  word, and the sentence the 51 kit cards repeated moves into the README once.

### Changed, in the skill
- The verifier reads the fine-print roles from the copy
  (`design-system/elements.json`, written by the refresh) instead of its own
  list. CardsV1 and V2, ChartsV3 and ProcessTimelineV2 and V4 no longer fail
  the type floor on text the design system allows.
- `CLAUDE-DESIGN.md` drops its duotone and motion notes. Only the chart-label
  note is left for the design system to take.
- The 13 kit authoring sources (`assets/snippets/*.html`) are gone.
  `derive_capacity.py` measures the 51 variants themselves (`--split` is
  retired), and the notes the files carried are kept verbatim in
  `authoring/kit-notes.md`, outside the skill. The skill is 182 entries, down
  from 194.
- The refresh warns when the design system's catalogue stops quoting a layout
  card.

### Known issues
- ProcessTimelineV4, used as it is, fails two verifier checks: one of its own
  dots covers its last timeline label, and it leaves the lower half of the
  slide empty. The fix is a change to its preview in the design system.

Decks build as before: all 1,449 spec combinations build byte-identical, and
the demo deck's verifier transcript is unchanged.

## [4.1.2] — 2026-09-25

The last design-system notes from the alignment audit, and the skill following
them.

### Fixed, in the design system (now version `1790335932-06d5`)
- The Headline card gives the Slides highlight its numbers. The gap between
  the flex row's blocks is one word space, measured in the WPP faces: 15 px at
  54 px, 18 px at 64 px, 14 px for the 48 px capitals. Only a headline of at
  most 60 characters (50 at 64 px, 55 in capitals) is split; a longer one, or
  one an edit takes past its limit, stays one `<h2>` and drops the highlight.
- The Headline card says to drop the eyebrow when the headline runs to two
  lines, as guideline 06 already did.
- Provenance. Guideline 11, the README and the `tokens.json` `meta` say the
  system is edited in Claude Design, the repository copies it one way, and it
  is never re-synced from the repository. Gone: the note that treated the
  repository as the source, and the old repository paths in `meta`.
- The 25 traced layouts' Origin lines point at `canon/templates/<id>.html` and
  `authoring/canon-src/<id>/`, where those files now live.

### Changed, in the skill
- `CLAUDE-DESIGN.md` drops the highlight and eyebrow notes, which the Headline
  card now carries. Saying which highlights were dropped moves into the
  delivery step.
- The design-system copy is refreshed. Only `tokens.json` (its `meta`) and
  `SOURCE.json` change.

## [4.1.1] — 2026-09-25

The design-system fixes approved after 4.1.0, and the skill following them.

### Fixed, in the design system (now version `1790334182-5d6d`)
- The two logos, re-uploaded with their fill on each shape. The first uploads
  had lost it with their `<style>` block and rendered black, so a cover built
  in Claude Design carried a black logo on its navy badge.
- AgendaSlide places its rows where the generator does: the first at y 266,
  148 px apart (for six chapters, 224 and 128), not 300 and 140.
- ThankYouSlide has the dark outro beside the light one. CoverSlide has the
  dots and playbook covers, and says how crystal and coral are anchored.
- The 80 px leftovers: the README's canvas note, the grid guideline's column
  widths (860 / ~547 / 408 on the 1800 px grid), the furniture guideline's
  headline width, the open question in guideline 11, the gutter token notes and
  the stylesheet's `:root` comment.
- `bundle.css` no longer ends with the logo rule that had leaked into it.

### Changed, in the skill
- The refresh reads the outros, the covers, the agenda's row placement and the
  playbook cover's dots from the cards, and takes the logos like any other asset
  group: `SOURCE.json` lists no exceptions.
- `build_shell.py` takes all of those from the copy. Only the classic divider's
  second and third dot colours and two content-slide dot fields are still
  written there. The full-bleed cover uses its own art file, not always the
  mountain.
- `CLAUDE-DESIGN.md` drops the logo workaround.

Decks build as before: across all 1,449 spec combinations the output differs
only in the logo's markup and the removed rule, and renders pixel-identical.

## [4.1.0] — 2026-09-25

One entry for everything since 4.0.0, which this file had not followed. The
last part moves the brand into the design system in Claude Design; the decks
the renderer builds are unchanged by it, pixel for pixel.

### Changed: the design system owns the brand
- The "WPP Enterprise Solutions | MAP" design system in Claude Design decides
  what a deck looks like; the skills decide how a deck gets made. Where they
  disagree, the design system wins. `SKILL.md` says so and no longer restates
  brand values in its non-negotiables.
- `wpp-es-html-deck/design-system/` is a generated copy of the design system
  (tokens, stylesheet, fixed-slide data, fonts, logos, icons, illustrations,
  photos, textures, exemplars), written only by
  `authoring/refresh_design_system.py`, one way, and stamped in `SOURCE.json`
  with the version (`1790326528-fd00`) and a sha256 per file. It replaces the
  asset folders under `assets/`.
- `build_shell.py` builds every deck from the copy: the whole stylesheet from
  `bundle.css` (about 450 lines of CSS removed from the generator), `:root` and
  the fonts from `tokens.json`, the colourways, light outro, cover art and dot
  presets from `fixed-slides.json`.
- `verify_deck.py` fails a deck when any cached file or layout section differs
  from `SOURCE.json`, and reads its closed palette from the tokens;
  `halftone.py` reads its inks and grounds from them.
- Every layout's `<section>` comes from the design system's preview, and the
  canon catalogue's text from its cards.
- `references/CLAUDE-DESIGN.md` holds process only: a reading order through the
  design system, the install, and the few Slides rules the design system does
  not carry yet.
- The guideline (`references/sections/`, `CORE.md`, the whole guideline in
  `build/`) is the skill's downstream copy; about thirty stale positions (the
  80 px content edge, headline at (80, 28), eyebrow at y 132, 1760 px column
  maths) now match the generator.

### Added
- Claude Design Slides as a surface: the deck is built in the Slides artifact
  with the design system installed (four faces, so the weights survive), the
  plan gate is a question card, no slide is posted as an image, and revising,
  PPTX and PDF have answers there.
- The canon: 25 templates traced from the MAP slide bank across eight
  families, with a catalogue, capacity limits and motion.
- Packaging for claude.ai: the skill folder fits the 200-entry, 30 MB cap as it
  stands (195 entries, 4.98 MB); `scripts/package_skill.py` checks it and zips
  without Finder's `__MACOSX` entries.
- Four `**Visual:**` hints in the handoff contract: `relational`, `logos`,
  `chart`, `split` (additive; existing content files read the same).
- A check, run by `build_docs.py` and so by every verify, that the two blocks
  shared between the skills (house copy rules, handoff contract) stay
  byte-identical.
- The guideline is generated from `references/sections/` by `build_docs.py`,
  and checked on every deck.

### Changed
- The frame sits on the playbook's 40 px grid (`--m-edge`), and the verifier
  reads the edge from the deck instead of assuming 80.
- The two logos are coloured by attribute, not by a `<style>` class, so an
  upload keeps their colour.
- `deck-content-builder` describes the favourable and unfavourable number cues
  without naming colours.

### Removed
- `canon/PREVIEWS.png`, a contact sheet nothing could rebuild; each layout's
  card in the design system renders it.
- `assets/fonts`, `logos`, `illustrations`, `photos`, `textures`, `exemplars`
  and `icons`, moved into `design-system/`.

### Fixed
- `references/capacity.json` recorded a stale font size on six canon slots;
  regenerating it (on `main` too) gives `null`. Limits are unchanged.
- `deck-content-builder`'s handoff marker named the wrong twin file.
- `SKILL.md` no longer points at files the uploaded skill does not have (a
  template's `ref.png` and `spec.json`).

### Known issues
- The design system does not hold yet: the dark outro, the dots and playbook
  covers, how crystal and coral are anchored, the classic divider's second and
  third dot colours, three dot presets. They stay in `build_shell.py`, marked.
- In the design system, AgendaSlide's row spacing (300/140) is wrong (the
  generator's is 266/148, dense 224/128), and both logo uploads render black.
- The guideline is still a hand-kept copy downstream of the design system.
- The 13 kit authoring sources in `assets/snippets/*.html` now only mirror the
  design system's layouts; removing them would free 13 entries.
- Photography licensing is unrecorded. See `NOTICE.md`.

## [4.0.0] — 2026-09-09

First commit under version control. The skills themselves already carried
internal version markers (`wpp-es-html-deck` v4, `deck-content-builder` v4,
HANDOFF-CONTRACT v3); this release records that state as the baseline.

### Added
- `wpp-es-html-deck` v4 — SKILL.md, the design guideline in three forms
  (master, section split, CORE subset), 51-template snippet library,
  per-slot capacity model, brand assets, and five scripts
  (`build_shell.py`, `verify_deck.py`, `check_capacity.py`,
  `derive_capacity.py`, `halftone.py`).
- `deck-content-builder` v4 — SKILL.md, emitting HANDOFF-CONTRACT v3 Markdown.
- Repository scaffolding: `README.md`, `NOTICE.md`, `.gitignore`,
  `wpp-es-html-deck/requirements.txt`.

### Fixed
- `verify_deck.py` no longer hardcodes the macOS Chrome path. It now resolves
  Chrome from `$WPP_DECK_CHROME`, then the standard install locations on
  macOS, Linux and Windows, then `PATH` — so `--screenshots` and the geometry
  probe work off a Mac and in CI. When no Chrome is found the failure message
  says how to fix it instead of naming a path that never existed.

### Known issues
- The design guideline is duplicated three ways by design; edits must be
  propagated by hand. See "Maintenance notes" in `README.md`.
- Photography licensing is unrecorded. See `NOTICE.md`.
