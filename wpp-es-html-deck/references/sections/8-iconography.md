## 8. Iconography

- Icons are **built from dots** on a rounded-square grid: the glyph outline is drawn as a string of solid Navy circles of varying diameter, with a loose scatter of tiny satellite dots around it.
- One colour per icon: **Navy** on light backgrounds (White on Navy). Never multicolour.
- Six pillar icons exist in the brand system: **Commerce** (overlapping circles), **Customer Experience** (person), **Content Transformation** (stacked frames), **Consulting** (key), **Engineering & Platforms / Technology & Data** (bolt), **1PD, CRM & Loyalty** (chain links).

### 8.1 Icon suite (v3.3 — ships in `design-system/icons/<family>.md`, mined from the MAP deck)

**32 brand icons ship**, normalized to `currentColor` (mono, CSS-recolourable),
0.5–11 KB each. Paste the SVG **inline** at fill time inside an icon host:
`<div class="icon"><svg …></svg></div>` — 44px navy by default; `.icon--orange`
for the one sanctioned orange moment; `.icon--lg` 64px; auto-flips to Cream on
navy slides/panels. The suite:

The suite, by weight family (subject gloss where the filename misleads):

- **line** (monoline 96px): `brain` (gears-in-brain) · `chart-decline` (bars
  with DOWNWARD arrow — cost/risk reduction only, never growth) · `checklist` ·
  `flow` (workflow, line style) · `mind` (**the AI icon** — circuit-head) ·
  `network` (people cycle) · `reach` (person in radar arcs — audience/reach,
  v3.5) · `segments` (three linked user nodes — segmentation, v3.5) ·
  `strength` (weightlifter — capability slides only if the tone can take it)
- **solid** (96px): `audience` (group under speech panel — comms/engagement,
  v3.5) · `clipboard` · `cycle` · `energy` (charging battery) · `globe` ·
  `globe-grid` (near-duplicate of globe, thinner) · `globe-hands`
  (Americas globe — no hands) · `growth` (upward curve) · `idea` · `loop`
  (nodes cycling — test-and-learn, v3.5) · `puzzle` · `report` (sheet +
  pencil — document/report, v3.5) · `rocket` · `team` (review panel over
  people) · `thought` · `workflow` (same glyph as flow, solid style)
- **bold** (rounded 24px, chunkier weight): `face-sad` · `gift` · `hands-care`
  (hands holding a gem — value/premium) · `heart-mail` · `trophy`
- **accents**: `spark` / `spark-bold`

**Pairing rule (hard):** one weight family per icon row / per slide. A monoline
icon beside a solid one in the same row reads as two different icon sets — the
most visible amateur tell. Deck-wide default is **solid**; use **line** only
when the whole slide's icons are line; **bold** only in hosts ≥44px. When both
styles of a glyph exist (`flow`/`workflow`), the family decides for you.

- Icon-led columns replace dot headers **when the point is a verb or a
  capability**; dot headers stay the default for parallel nouns. Never mix
  both header styles on one slide.
- `spark` / `spark-bold` are ACCENTS, not bullets: absolutely-positioned
  `.spark` (34px) or `.spark--lg` (56px), orange-700 or `.spark--navy`,
  **max 2 per deck**, statement-adjacent air only.
- **Never** substitute a generic icon library; if no suite icon fits, fall
  back to the dot bullet — always safe. Known gaps with NO suite icon (they
  degrade to dot bullets by design; the brand pptx was swept in full — these
  simply don't exist in brand source): calendar/timeline, money/ROI,
  shield/security, target/goal, search, gear alone, lone user, warning,
  integration/API, database, commerce/cart.

---

