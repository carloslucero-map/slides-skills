# WPP Enterprise Solutions — Design Guideline for Slide & HTML Decks

**Version 4.0 · July 2026** — aligns the system to the parent-brand **WPP Enterprise Solutions Brand Playbook v0.2 (July 2026)**, which is now the design master. v4 adds: the playbook typography roles (Regular body — real headline/body weight contrast), the sub-headline tier, the title-highlight rule, minimum font sizes, semantic data colours (`.stat--pos`/`.stat--neg`), the dot scale registers (micro/mid/macro + fused metaballs), the playbook divider composition, media edge-anchoring laws, the content-edge consistency law, and the dot-halftone conversion pipeline (`scripts/halftone.py`). The generator (scripts/build_shell.py) and this document are the single source of truth; where they ever disagree, the generator wins.

Compiled from: the **WPP ES Brand Playbook v0.2** (`WPP Enterprise Solutions Guidelines_0.2JULY2026.pdf`, 46 pages — the design master), the WPP ES website (enterprisesolutions.wpp.com — stipple/halftone image language), the WPP Enterprise Theme 2026 PowerPoint template (95 layouts + 131 example slides), the official colour palette exports, the WPP Sans font family, the MAP logo pack, and the WPP Open dot-illustration library. Those are provenance documents — everything a deck actually needs ships inside this skill package.

**Purpose.** This document encodes the complete WPP Enterprise Solutions (WPP ES) visual identity so that a text-only presentation outline (agenda, slide titles, content, narrative) can be turned into an on-brand HTML presentation without consulting any other source. Every colour, font, spacing value, shape and slide archetype needed is specified here.

**What ships with this skill** (the complete asset inventory):

| Kind | Files |
|---|---|
| **Fonts** (`assets/fonts/`) | 5 woff2: `WPP-Thin` (100) · `WPP-Light` (300) · `WPP-Regular` (400) · `WPP-Medium` (500) · **`WPP-Bold` (700)** |
| **Logos** (`assets/logos/`) | `WPP_ES_MAP_logo_NAVY.svg` · `WPP_ES_MAP_logo_WHITE.svg` (the full lockup, both colourways) |
| **Illustrations** (`assets/illustrations/`, see §9.1a for the full v4 inventory) | `WPPOpen_Mountain-01.png` 1920×1072 navy · `WPPOpen_Crystal-01.png` 1920×1072 navy · `WPPOpen_Crystal-01_Orange.png` 1920×1072 orange · `WPPOpen_Coral-01.png` 1920×1072 navy · `WPPOpen_Coral-01_Orange.png` 1920×1072 orange · `WPPOpen_Rocks-01.png` 964×540 navy+cream · `WPPOpen_Bee-01.png` 560×581 navy multi · `WPPOpen_Ribbon-01_Orange.png` 964×540 orange+cream |
| **Snippets** (`assets/snippets/*.html`, 13) | `statement-quote` · `columns` · `boxes` · `comparison` · `image-content` · `team` · `process-timeline` · `stats` · `charts` · `cards` · `splits` · `orbit` · `logo-wall` — variant 1 of each is a full-canvas §12.15 recipe |
| **Icons** (`assets/icons/`, 27 SVG) | the §8.1 suite, mono `currentColor`, pasted inline (incl. `spark`/`spark-bold` accents) |
| **Exemplars** (`assets/exemplars/`, 4) | one exemplar slide PNG per design direction — the visual bar for the §12.15a art-direction pass |
| **Scripts** (`scripts/`) | `build_shell.py` (deck-shell generator) · `verify_deck.py` (delivery checks + composition tripwire) · `halftone.py` (dot-illustration converter, §9.1c — authoring-time tool) |

Anything not listed here does not ship in this package — never reference or promise it; use the fallbacks in §13.1.

---

