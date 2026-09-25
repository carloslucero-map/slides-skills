# Changelog

All notable changes to these skills are recorded here.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
