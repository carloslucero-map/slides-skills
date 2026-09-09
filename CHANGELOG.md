# Changelog

All notable changes to these skills are recorded here.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
