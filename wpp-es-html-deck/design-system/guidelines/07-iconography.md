# Iconography

Icons are **built from dots** on a rounded-square grid: the glyph outline is drawn as a string of solid Navy
circles of varying diameter, with a loose scatter of tiny satellite dots around it. One colour per icon —
Navy on light, Cream on Navy. Never multicolour.

**32 icons ship** in the **Icons** asset group, normalized to `currentColor` so they recolour in CSS, 0.5–11 KB
each. Paste the SVG inline inside an icon host: `<div class="icon"><svg …></svg></div>` — 44px Navy by
default, `.icon--lg` at 64px, `.icon--orange` for the one sanctioned orange moment, auto-flipping to Cream on
navy slides and panels.

## The suite, by weight family

**line** (monoline, 96px) — `brain` (gears in a head) · `chart-decline` (bars with a *downward* arrow: cost and
risk reduction only, never growth) · `checklist` · `flow` · `mind` (**the AI icon** — circuit head) ·
`network` (three linked user nodes, the same drawing as `segments`) · `reach` (person in radar arcs) · `segments` (three linked user nodes) · `strength`
(weightlifter — capability slides only, if the tone can take it)

**solid** (96px) — `audience` · `clipboard` · `cycle` · `energy` (charging battery) · `globe` · `globe-grid`
(a thinner near-duplicate of globe) · `globe-hands` (Americas globe — no hands, despite the name) · `growth` ·
`idea` · `loop` (nodes cycling — test and learn) · `puzzle` · `report` · `rocket` · `team` · `thought` ·
`workflow` (the same glyph as `flow`, solid style)

**bold** (rounded, 24px, chunkier) — `face-sad` · `gift` · `hands-care` (hands holding a gem) · `heart-mail` ·
`trophy`

**accents** — `spark` · `spark-bold`

Four pairs of files are the same drawing: `audience` and `team`, `clipboard` and `report`, `network` and
`segments`, `cycle` and `loop`. Either name renders the same glyph.

**Six pillar icons** exist in the wider WPP brand system but do not ship here: Commerce, Customer Experience,
Content Transformation, Consulting, Engineering & Platforms / Technology & Data, and 1PD, CRM & Loyalty.

## The pairing rule is hard

**One weight family per icon row, per slide.** A monoline icon beside a solid one in the same row reads as two
different icon sets — the most visible amateur tell in the system.

Deck-wide default is **solid**. Use **line** only when every icon on the slide is line; **bold** only in hosts
of 44px or more. Where both styles of a glyph exist (`flow` / `workflow`), the family decides for you.

## When an icon is the wrong answer

Icon-led columns replace dot headers **when the point is a verb or a capability**; dot headers stay the default
for parallel nouns. Never mix both header styles on one slide.

`spark` and `spark-bold` are accents, not bullets: absolutely positioned at 34px or 56px, orange-700 or navy,
**maximum two per deck**, in statement-adjacent air only.

**Never substitute a generic icon library.** If no suite icon fits, fall back to the dot bullet — always safe.
Known gaps with no suite icon, which degrade to dot bullets by design because they do not exist in the brand
source: calendar/timeline, money/ROI, shield/security, target/goal, search, gear alone, lone user, warning,
integration/API, database, commerce/cart.
