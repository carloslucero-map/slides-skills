# Notice — proprietary and third-party assets

This repository is **private and internal to WPP Enterprise Solutions | MAP**.
It is not licensed for distribution, and it must not be made public.

## Why this repository cannot be public

`wpp-es-html-deck/design-system/` ships brand and media assets that are not
ours to redistribute. They are a copy of the WPP Enterprise Solutions | MAP
design system's, written by `authoring/refresh_design_system.py`:

| Asset set | Files | Status |
|---|---|---|
| `design-system/fonts/` | 5 × WPP Sans `.woff2` (Thin, Light, Regular, Medium, Bold) | **Proprietary WPP corporate typeface.** Licensed for WPP use only. Never redistribute, never embed in anything leaving WPP. |
| `design-system/logos/` | WPP ES \| MAP lockups (Navy, White) | **Proprietary WPP trademark.** Use is governed by the brand guideline; see §6 of the design guideline. |
| `design-system/illustrations/` | WPP Open and MAP motif artwork | **Proprietary WPP artwork.** |
| `design-system/photos/` | 13 photographs | **Provenance not recorded at import.** Verify licensing before any external or client-facing use. See below. |
| `design-system/textures/`, `design-system/icons/`, `design-system/exemplars/` | Generated or derived from the brand guideline | Internal. |

## Photography — action required

The 13 files in `design-system/photos/` were carried over without a recorded source or
licence. Before any of them appears in a **client-facing or externally published**
deck, confirm the licence for that specific image and record it here.

Internal decks may use them under the same assumption they were used before this
repository existed. This is a documentation gap, not a known infringement.

| File | Source | Licence | Verified |
|---|---|---|---|
| `photo-chess.png` | — | — | ☐ |
| `photo-confetti.png` | — | — | ☐ |
| `photo-dancers.png` | — | — | ☐ |
| `photo-diver.jpg` | — | — | ☐ |
| `photo-fibers.png` | — | — | ☐ |
| `photo-fjord.jpg` | — | — | ☐ |
| `photo-gears.png` | — | — | ☐ |
| `photo-globe.png` | — | — | ☐ |
| `photo-handoff.webp` | — | — | ☐ |
| `photo-lighthouse.png` | — | — | ☐ |
| `photo-pencils.png` | — | — | ☐ |
| `photo-ridge.jpg` | — | — | ☐ |
| `photo-team.webp` | — | — | ☐ |

## Internal contacts in the repository's history

The skill's old downstream guideline named an internal contact for sub-brand
and partner logo creation. That guideline was retired in 4.2.0 and the design
system does not carry the contact, so no current file names it, but the
repository's history still does: another reason this repository stays
private.

## If this repository is ever opened up

Removing `design-system/fonts/`, `design-system/logos/`,
`design-system/illustrations/` and `design-system/photos/`, and publishing from
a history that no longer holds the internal contact above, is the minimum. The skills would then need a
documented way for users to supply their own brand assets.
