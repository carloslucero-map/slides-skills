# Building the HTML deck: the mechanics and the checks

This file is the skill's own. It says how the one self-contained HTML file is
generated, filled, run and checked. What a deck looks like is the design
system's, and on this path its copy in `design-system/`: `README.md` first,
then the guidelines and cards `SKILL.md` names (Step 0). Where this file and
the design system disagree, the design system is right; follow it and say so
at delivery.

The section numbers are the old guideline's, kept so that the verifier's
messages, the templates' comments and older notes still point somewhere: §2a,
§12.14 to §12.15a, §13, §13.4, §14 and §15. Every other old number (the brand
sections §1 to §11 and the archetype library §12.0 to §12.13) now belongs to
the design system; the table at the end says where each one went.

**Read before building:** §2a, §12.14 to §12.15a, §13 and §15. **Only when it
applies:** §13.4 when the deck has expandable cards, §14 when motion is full or
subtle, and the table at the end when a comment cites an old number.

---

## 2a. Self-contained file rule (non-negotiable)

**Scope: the standalone HTML file.** In Claude Design the deck is an Artifact
made from the Slides type, and the opposite holds there: images and fonts are
*uploaded* and referenced by the URL the upload returns (a `data:` URI is
refused), so this section does not apply. `references/CLAUDE-DESIGN.md` governs
that surface.

**Every deck ships as a single, standalone `.html` file that opens correctly by
double-clicking it in any browser, with no other files present, no folder
structure, and no internet connection.** Decks are shared with colleagues who
just open them locally, so a deck that relies on an external path is broken on
arrival.

Concretely, **all** of the following are embedded inline, never linked out to:

- **Fonts**: the five WPP Sans weights embedded as base64 inside
  `@font-face { src: url("data:font/woff2;base64,…") }`. The generator does this.
- **Logos**: the MAP lockup pasted in as an **inline `<svg>…</svg>`** element
  (preferred) or a base64 data URI, never an `<img src>` file path.
- **Icons**: inline SVG, never an external reference.
- **Illustrations, textures and library photos**: a base64 `data:image/…` URI,
  never a file path. The generator inlines each one the spec lists (§13.3).
- **Anything else raster or vector**: a base64 data URI in the `src` or
  `background-image`, never a file path.

Rules of thumb:

- **No relative or absolute file paths, and no external URLs**, anywhere in the
  final HTML: not in `<img src>`, `background-image`, `@font-face src`,
  `<link>`, `<script src>`, `<use href>`, or CSS `url()`. The only sanctioned
  "external" thing is an inline SVG referencing its own internal `#id`.
- **No CDN links either** (fonts, CSS resets, JS libraries): pull the content
  in and inline it. The file must render fully offline.
- The files in `design-system/` are **build-time sources**: the generator (and
  you, during the fill step) read an asset from there, then **inline its
  contents** into the HTML. They are never left as live references in the
  shipped file.

**Payload budget.** Base64 makes files about a third bigger, so keep sources
lean: **every raster asset ≤ 300 KB before base64**, and treat **5 MB total
deck size as the warn threshold** (`verify_deck.py` checks both). The shipped
motifs are pre-optimised for this budget (the mountain is about 150 KB against
the 2.4 MB original), so preferring the shipped assets keeps you inside it.

**Verification before sharing:** move the finished `.html` to an empty folder
on its own (or disconnect from the network) and open it in a browser. If any
font falls back, any logo, icon, illustration or image fails to appear, or
anything 404s, the file is not self-contained: fix it before it goes out. Then
run `scripts/verify_deck.py`.

---

## 12.14–12.15a — Composition

These three are the kit's side of composition: the geometry it imposes, the
recipes it was built from, and the art-direction pass. `verify_deck.py`
enforces them on every deck. The design system's rules for composition are in
guideline 03 (the layout laws, archetypes and deck rhythm).

### 12.14 Composition guardrails (verified in render QA)

Constraints the kit's geometry imposes; respect them instead of rediscovering
them:

- **Lead paragraphs vs grid archetypes:** a `.content-band` lead line fits above
  `.timeline` (top 540; ≤ 2 lines) and `.kpi-row` (top 340; exactly 1 line). It
  collides with `.proc` (top 300): never combine.
- **Timeline positioning:** nodes are 16 px, so centre with
  `left:calc(P% − 8px)`; labels take the bare `left:P%` (the class
  self-centres). Keep nodes within about 5–95 %, or `nowrap` labels escape the
  content edge.
- **Stat circles below Ø ~340 px** need inline font downscales (e.g. 68/16 px at
  Ø 330, 46/16 px at Ø 220) or the value and label overflow the circle. Never
  below the type floors (§15.10).
- **`.img-half-media`** puts the footer furniture ON the image and the headline
  can run under it: cap the headline with an inline `max-width:820px` and keep
  the image's bottom-right corner visually light, or use the framed `img-right`
  layout.
- **`lift-corner` dots** overlap the footer zone by design; their colours are
  White and Cream so the Navy footer stays readable. Do not recolour them
  darker.
- **Card grids use the `.canvas-grid--cards` modifier**
  (`grid-auto-rows:auto; align-items:start; align-content:start`), never the
  bento's default `grid-auto-rows:1fr`. With `1fr` rows, one opened
  `.card-detail` stretches every sibling in the row; with the modifier, **each
  card expands individually: the opened `.card-detail` renders as a flat white
  overlay dropping over whatever sits below, and no sibling ever moves or
  stretches** (§13.4). The verifier fails a `.card` inside a `1fr`-rows grid.
- **`.col-sub` carries `margin-bottom:18px`**: zero it inline when reusing it as
  a row label inside a centred grid (e.g. bar-chart rows).
- **Panel headline cap:** when a right-side `.panel` is ≥ 768 px wide
  (`--w768`/`--w960`), cap the headline with an inline `max-width:1040px` or it
  runs under the panel (the Headline card).
- **Motif text-safe zones:** `.motif--right` keeps text left of x = 1200;
  `.motif--bottom` keeps text above y = 560; `.motif--backdrop` sits behind stat
  compositions only; `.motif--panel` lives inside panels; `.motif--bleed` is for
  posters, and on any slide of a high-impact deck (guideline 08).
- **`field-navy` dots never sit behind text**: place them only where the
  composition leaves that zone empty (guideline 04).
- **`.takeaway` holds ONE line, ≤ 90 characters**: a second line collides with
  the footer furniture.
- **`.num-ghost` uses flat sanctioned tones only:** Orange 500 on Cream, White or
  Cream on Navy; never opacity tricks, never other colours.
- **`.canvas-grid` cells need explicit `grid-column`/`grid-row` spans inline**:
  auto-placement produces even boxes, not the asymmetric bento the recipes call
  for (R2).

### 12.15 Composition recipes (mined from the template)

These 17 recipes are the template's own full-canvas compositions, translated to
the kit (coordinates extracted from the source slides; 1920 × 1080 canvas).
**Content slides are ASSEMBLED FROM RECIPES, never from bare text bands**: a
headline over a `.content-band` of copy is a draft, not a slide. **The first
variant of every kit family (`<family>-v1.html`) is a full-canvas recipe; pasted
unmodified, it must pass §12.15a.** Registry format: name · template source ·
geometry (px) · kit classes · variant file in `assets/snippets/variants/` ·
direction affinity.

- **R1 · Split rail dashboard** — slide 95 (halves variant: 97). Full-height
  440 px rail `.panel .panel--w440 .panel--tint|--nav` carrying 4 stat rows via
  `.panel-inner` (~y 162/377/589/806; values 60–72 px, labels 20 px); main
  field: lead paragraph ~(80, 124) 1170 × 170 + KPI row anchored LOW,
  `.kpi-row .kpi-row--low` (y 747–930). → `splits-v1` · data-forward/editorial.
- **R2 · Stat mosaic bento** — slide 96. `.canvas .canvas-grid` 12-col bento: 5
  asymmetric `.cell` zones filling the whole band, one hero stat, 2 × 2 stat
  quads at 60 px. → `charts-v1` · data-forward.
- **R3 · Hero numeral quartet + ruler** — slide 94. 3–4 `.hero-row` numerals
  (`.n` 144 px) in ~244 × 164 boxes at y ≈ 234, CAPS labels y ≈ 361, 380 px
  bodies y ≈ 440; `.vrule` hairlines x ≈ 520/960/1400, h ≈ 120; bottom `.ruler`
  y ≈ 881 + `.ruler-ticks` (majors every ~360 px) + `.ruler-label` CAPS
  y ≈ 931. → `stats-v1` · data-forward.
- **R4 · Hub & spokes** — slide 100. Centre circle Ø 460–500 at ~(747, 333),
  a flat navy `.stat-circle` or `.motif--backdrop`, ringed by 6 × 19 px
  satellite `.dot`s; flanking 475 px columns (`.col-dot` + subhead + body) at
  x ≈ 81/1399, rows y ≈ 277/516/756. → `stats-v2` (and `stats-v1`) ·
  data-forward.
- **R5 · Cluster diagram + index row** — slide 102. Two Ø 465 navy circles
  overlapping at (380, 311)/(767, 308), knockout labels, white-text lists
  inside; Ø 187 satellites; 1 px orange connector lines; bottom row of
  6 × (dot + subhead + body) 278 px wide, y 806–959. 100 % active canvas.
  → `stats-v6` · data-forward.
- **R6 · Gantt swimlanes** — slides 90/91. `.gantt` band; `.lane-dot`s x ≈ 42,
  y ≈ 221/394/567; `.bar`s 6 px flat orange-ramp fills y ≈ 281–532, widths
  197–750; `.vrule` guides x ≈ 982/1102/1550/1763; bottom `.flag` chips
  206 × 46 at y ≈ 834/914. → `process-timeline-v3` · data-forward.
- **R7 · Milestone ruler timeline** — slide 93. Full-width `.ruler` y ≈ 569,
  alternating year `.ruler-label`s y ≈ 528/600; up to 12 `.stem`s (h 43–183) to
  `.milestone` blocks ABOVE AND BELOW the line (y range 226–954).
  → `process-timeline-v2` · all directions.
- **R8 · Phase board** — slide 117. Centre `.cell--tint` panel (480, 200)
  960 × 680; step headers on the top rule (14 px dots, STEP CAPS labels, `.pill`
  time chips); 4 body columns 402 × 399; full-width bottom band (40, 880)
  1839 × 120 split by white rules. → `process-timeline-v6` ·
  editorial/data-forward.
- **R9 · Full-height card row + takeaway bracket** — slides 110/115. 4 white
  cards 360 × 560 at y = 200 via `.tbx-row .tbx-row--fill` (pill chip + 36 px
  title + rule + body per card); closer variant: `.takeaway` bracketed 48 px
  Light line (template bracket arms 23 × 120 at x ≈ 160/1737, band
  ~(201, 805) 1515 × 115). → `boxes-v1` · all directions.
- **R10 · Motif-side statement** — layouts 44/46. `.big-statement` 150–180 px
  at ~(109, 245), max-width 1500; art side = `.lift`
  `data-dots="field-right|field-accent"` or `.motif--right` `data-motif`;
  layout-46 art zone ~(1071, 399) 849 × 681 (text-safe left).
  → `statement-quote-v1` (`-v2b` with a halftone motif) · statement-led.
- **R11 · Full-bleed motif title** — layout 82. `.motif--bleed` `data-motif`
  full-canvas + ALL-CAPS Thin 108 px title at ~(45, 25). The "chapter poster"
  moment. → `image-content-v0` · statement-led/high-impact.
- **R12 · Tile grid** — layouts 69/70/73/74. 3 × 2 grid of 560 × 319 tiles:
  flat `.cell`/`.cell--nav`/`.cell--tint` panels, stat blocks, or
  `.motif--panel` crops. → `cards-v4` · all.
- **R13 · Split colour-block 40/60** — synthesised from slide 95 + layout 83.
  `.panel--w768` (40 %) or `.panel--w960` (50 %), `--nav`/`--tint` (`--orange`
  high-impact only), carrying display type (`.hero-num--l/--xl` or a short
  statement) or a `.motif--panel`; content columns on the other side; headline
  capped inline at max-width 1040 px when the right panel is ≥ 768 px (§12.14).
  → `splits-v2` · high-impact/statement-led.
- **R14 · Orbit hub** — inspired by pptx slide 27. 3 concentric `.orbit` rings
  (dotted circle borders) centred right of the headline, 4 `.orbit-node` labels
  on the middle ring, `.orbit-hub` centre with navy fill and label. Headline and
  body text left of centre. → `orbit-v1` · editorial/statement-led.
- **R15 · Scorecard bento** — inspired by pptx measurement frameworks.
  `.canvas .canvas-grid` 3 × 2 with `.cell` blocks, each carrying a category
  header (`.col-sub`), hero number (Thin 72 px), and label; one `.cell--nav`
  contrast moment, one `.cell--tint` highlight max. → `stats-v5` ·
  data-forward.
- **R16 · Venn diagram** — inspired by pptx slide 77. `.venn` container with 2–3
  `.venn-set` circles, flat tone-on-tone fills and no outlines, overlapping;
  `.venn-label` inside each set and a Medium label at the intersection. No
  motif: the diagram IS the composition. → `comparison-v2` · editorial.
- **R17 · Ecosystem map** — inspired by pptx slides 63-64. Centre `.orbit` ring
  + navy hub; 4 zones (positioned absolutely, top-left / top-right /
  bottom-left / bottom-right) with dot + `.col-sub` + `.body`; dotted
  connecting lines between zones and hub. → `process-timeline-v5` ·
  editorial/data-forward.

### 12.15a Composition checklist (the art-direction pass)

Seven criteria, each checkable on a screenshot. Every content slide must pass
all seven **by looking at its render**: this pass is visual, not textual. It is
the HTML deck's art pass, not a design-system rule: several traced layouts
depart from it on purpose, and their cards say where.

- **C1 — Focal element.** The slide has one: display type ≥ 100 px, a motif, a
  dot field, a panel, or a chart/stat composition ≥ 300 px tall. A headline
  alone never qualifies.
- **C2 — No dead lower half.** Composed elements extend below y = 700, and the
  background fraction in the band y 432–990 is < 0.83 (the verifier WARNs at
  ≥ 0.83 and FAILs at ≥ 0.92). Exception: registered statement/quote slides
  with deliberately asymmetric air.
- **C3 — Edge anchor.** At least one element touches or bleeds off an edge, or
  the slide is a deliberate centred statement.
- **C4 — Type discipline.** ≤ 3 text scales + ≤ 1 display moment; body ≥ 20 px;
  headline ≤ 2 lines. (Raised from ≤ 2 in v4.1: the curated selection's real
  median is 4 distinct sizes per slide, and at ≤ 2 an honestly traced canon
  fails its own criterion on 21 of 24 measurable slides. ≤ 3 still forbids the
  size-soup this rule exists to stop.)
- **C5 — Collisions.** Nothing under the footer zone (bottom-right 500 × 90);
  headline clear of art; text never over navy dots or dense halftone.
- **C6 — Deck rhythm.** No two adjacent content slides share archetype +
  treatment; decks of 8+ content slides use ≥ 2 density variants and ≥ 3
  recipes.
- **C7 — Colour quota.** The slide respects its direction's quota of dark and
  tint moments (the direction table in `SKILL.md`; guideline 01).

`verify_deck.py` enforces C2 numerically as a tripwire; the pass itself is done
BY LOOKING at each slide's screenshot.

**Declared air:** thin display type is pixel-light, so a template-faithful
display slide (an R3 quartet over a hairline ruler) can trip the tripwire while
being perfectly composed. When, and only when, the air is shaped (hairlines,
rulers or counterweights carry the eye through it), declare
`data-composition="intentional-air"` on the section: the verifier downgrades its
FAILs to WARNs and always prints the declaration, and the G2 seen-report must
name it. Never declare air on an undesigned slide.

**The thresholds are calibrated against the KIT, not the bank.** Measured
2026-09-11 across the canon: five traced templates fail the 0.92 tripwire, and
four of their SOURCE SLIDES measure 0.92–0.94 on the identical metric
(`ent-logo-rows-6` 0.94, `enum-intro-grid-5` 0.93, `ent-partner-credentials-3`
and `quant-stat-grid-5` 0.92). MAP's own index, roster and stat-grid slides are
built airier than this check allows, so a faithful trace inherits the failure.
That is what the declaration is for, but declare it against a MEASUREMENT of the
source, never against a preference.

**One trap when you measure a source.** `_bg_fraction` compares against the
brand cream #FAFAF0 with a tolerance of 12 per channel. Some bank slides are set
on a near-white ground (#FEFEFC) instead, which sits at the very edge of that
window: around a tenth of a visually EMPTY region then reads as foreground, and
the slide scores as far better composed than it is. `enum-index-2col`'s source
measures 0.84 for exactly this reason and it means nothing. Check the source's
dominant background colour before trusting a cross-render comparison.

---

## 13. Building the HTML deck — conventions & checklist

### 13.1 Skeleton

The generator writes the stylesheet from `design-system/bundle.css` and `:root`
from `tokens.json`; this is the frame it relies on.

```css
.slide {
  position: absolute; top: 0; left: 0;
  width: 1920px; height: 1080px; overflow: hidden;
  background: var(--bg);            /* Cream, the one content background */
  color: var(--text);
  font-family: 'WPP', 'Poppins', 'Century Gothic', system-ui, sans-serif;
  font-weight: 300;                 /* Light is the display voice; .body/.tbx set Regular 400 */
  font-feature-settings: "salt" 1;
  display: none;                    /* nav script reveals the active slide */
}
body:not(.js) #frame .slide:first-of-type { display: block; }  /* no-JS fallback */
body.js .slide.is-active            { display: block; }         /* script adds .js */
.slide--navy  { background: var(--bg-dark); color: var(--text-inv); }
.slide--tint  { background: var(--bg-tint); }
.slide--white { background: var(--bg-alt); }  /* rare only; guideline 01 */
```

- One `<section class="slide" data-slide-id="…">` per slide, `class` written
  first; keyboard ←/→ navigation; slide counter. The nav script stamps
  `body.js` on load (a `<noscript>` banner explains the single-slide fallback)
  and **fills every empty `.pageno` at runtime from the live slide count**:
  never bake page numbers into the markup.
- **Scaling: avoid the flex-shrink trap.** Do **not** put the fixed
  1920 × 1080 `#frame` inside a `display:flex` centring container: a flex child
  with an explicit width still shrinks (default `flex-shrink:1`), which
  silently squashes the frame and pushes content off the right edge. Scale it
  absolutely and centre by translate instead:

```css
#stage { position: fixed; inset: 0; overflow: hidden; background: #0a0a1a; }
#frame { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; transform-origin: top left; }
```
```js
function fit(){
  var vw=innerWidth, vh=innerHeight, s=Math.min(vw/1920, vh/1080);
  frame.style.transform='translate('+(vw-1920*s)/2+'px,'+(vh-1080*s)/2+'px) scale('+s+')';
}
addEventListener('resize', fit); fit();
```
  (If you prefer flex centring, you must add `flex-shrink:0` to `#frame`.)
  Always verify in the browser that `#frame`'s bounding rect fills the viewport
  with no side gutter before shipping.
- **Decorative dots** are absolutely positioned `div`s with
  `border-radius: 50%`, flat `background`, no opacity, `z-index` below content,
  cropped by `overflow: hidden`. The fixed slides' compositions are drawn by the
  shell's `[data-dots]` presets: their geometry is the design system's and
  their colours resolve through the deck's colourway; never hand-edit them.
- **The verifier's closed sets.** `border-radius` takes `50%` (dots and circles)
  or `999px` (pills) and nothing else, and any shadow (`box-shadow`,
  `text-shadow`, `drop-shadow`) FAILs the deck. Every colour literal should be
  in the palette `tokens.json` defines (plus `#0a0a1a`, the stage behind the
  frame); one outside it WARNs, naming the slide it sits on.

### 13.2 Mapping an outline to slides

1. Generate the shell: `python3 scripts/build_shell.py --spec spec.json --out
   deck.html`. The spec's five required keys (`title`, `subtitle`, `month`,
   `presenter`, `chapters`) plus the registered choices (`direction`,
   `dividerColourway`, `dividerStyle`, `cover`, `outro`, `motion`) and the
   rest (`confidential`, `lang`, `strings`, `contact`, `microDeck`,
   `illustrations`) produce the cover, agenda, dividers and thank-you slide, and
   one placeholder per planned content slide. A single-chapter micro-deck omits
   the agenda and the dividers automatically.
2. **When the input is a deck-content-builder Markdown file, follow the
   input-mode mapping in `references/HANDOFF-CONTRACT.md`: approved titles are
   carried verbatim.**
3. Fill each placeholder from a canon template or a kit variant (`SKILL.md`,
   step 4): key messages and transitions become a Big Statement, quotes a Big
   Quote (the catalogue's Narrative family).
4. Body content: choose the column count by the number of parallel points
   (1–4); sequences get **arrows**, parallel relations get **dots**, categories
   get **pills**.
5. Numbers become a data-viz layout (guideline 09): circles first, sized by
   area, never by diameter; bars only when circles cannot carry it.
6. Rhythm check: every content slide on the one Cream ground, orange as
   seasoning, dark slides only as often as the direction allows; no two
   adjacent slides with the same heavy dot treatment (guidelines 01 and 04).
7. Verify: self-containment (§2a), the payload budget, then
   `scripts/verify_deck.py`.

**Never hand-build, hand-edit or skip the four fixed slides.** The generator
emits them from `design-system/fixed-slides.json`; the spec keys are the only
sanctioned variation. Never reference or promise an asset that is not in
`design-system/`.

### 13.3 The kit's vocabulary: where each rule meets the file

The design system names the rule; this is how the HTML deck spells it. Each
card's *In the HTML deck* section lists the same classes.

| Topic | In the file | The rule |
|---|---|---|
| Grounds | `.slide` (Cream), `.slide--navy`, `.slide--tint`; `.slide--white` rarely | guideline 01 |
| Headline, eyebrow, highlight | `.headline`, `.headline--lg`, `.headline--caps`; `.subtitle`; one `<span class="hl">` per title | Headline card |
| Running text and labels | `.body`, `.subhead`, `.col-sub`; text between 16 and 20 px carries a fine-print role from `design-system/elements.json` | BodyCopy, Subhead and ColumnLabel cards |
| Numbers with a direction | `.stat--pos` (favourable), `.stat--neg` (unfavourable); weight 300 or more below 90 px, one `.stat--pos` per slide | guideline 09, KpiRow card |
| Dot fields | `data-dots="<preset>"`: `lift-corner`, `lift-orange-soft`, `lift-navy-corner`, `field-right`, `field-bottom`, `field-tl`, `field-accent`, `field-navy`, `field-micro`, `field-mid`, `field-macro` | guideline 04, DotField card; which preset per direction: `SKILL.md` |
| Motifs, textures, library photos | list the keys in `spec.illustrations`; the shell inlines each once as a `<template data-asset>`; place with `<div class="motif motif--right" data-motif="coral">`, utilities `--right`, `--bottom`, `--backdrop`, `--panel`, `--bleed` (§12.14) | guideline 08, `design-system/asset-notes.md` |
| A brief's photo | `<div class="duo" style="…geometry…"><img src="data:…" alt="…"></div>`; a library photo is never wrapped in `.duo` | Photo card |
| A brief's photo as dot art | `scripts/halftone.py`, below | guideline 08 |
| Screenshots | `.screenshot`, the keyline frame; never full-bleed | ScreenshotFrame card |
| Edge-bled media | `.media--bleed-r`, `-l`, `-b`, `-t`, `.media--corner-br`, `-tr`; `data-inset-ok` for a declared inset (§15.9) | Photo card |
| Icons | `<div class="icon"><svg …></svg></div>`, `.icon--lg`, `.icon--orange`, pasted from `design-system/icons/<family>.md`; accents `.spark`, `.spark--lg`, `.spark--navy`, two per deck at most | guideline 07, Icon card |
| Takeaway | `.takeaway`: one line, ≤ 90 characters, the same geometry on every slide (§15.3) | Takeaway card |
| Cards that open | `.card`, `.card-cta` with `.arrow`, `.card-detail` (§13.4) | CardBox and CardLink cards |
| Ghost numerals | `.num-ghost`, flat sanctioned tones (§12.14) | README, the orange text moments |
| Furniture | `.footer-brand`, `.pageno` (left empty), `.confidential` (the `confidential` key), `.source` | FooterFurniture card |
| Speaker notes | `<aside class="notes" hidden>`, shown with the `N` key | — |
| Step-by-step reveals | `data-build` on parallel blocks (§14) | guideline 10 |

**The halftone converter, `scripts/halftone.py`** (the old §9.1c). It turns any
raster image into a brand dot illustration at the design system's canonical
settings (guideline 08). It is a build-time tool: its outputs are optimised
PNGs or SVGs that get base64-inlined like any motif; the script never ships
inside a deck.

```
python3 scripts/halftone.py photo.jpg --fg navy --bg none --width 1600   # subject-only dot art
python3 scripts/halftone.py photo.jpg --fg orange --invert               # flip tone mapping when the subject is light
python3 scripts/halftone.py --overlay 1920 1080 --fg orange-800 --seed 7 # halftone-circle cluster overlay
```

- Colourways: `navy` (default) · `orange` (700) · `orange-800` · `white` ·
  `cream`: flat single-colour dots, transparent ground by default.
- A brief's photo on a slide that wants the "pixelated" hero look: convert it
  (subject only) and inline the result. The other rendering is the `.duo`
  duotone; those two are the only photo treatments.
- `--overlay` produces a cluster of two to four flat macro circles bleeding off
  the canvas, one colourway, as a transparent PNG.
- Outputs obey the §2a payload budget (≤ 300 KB before base64; the script
  enforces it).

---

## 15. Layout & UX laws (v3.6) — enforced geometry

The design system states these as layout laws (guideline 03); this section says
how the HTML deck is **measured against them**. `verify_deck.py --screenshots`
measures every one from the rendered DOM (glyph-accurate rects, headless
Chrome) and **FAILs the build** on violations. A slide that looks right but
breaks a law is broken: fix the geometry, don't argue with the ruler.

### 15.1 Safe areas & reserved bands

| Zone | Reserved for | Law |
|---|---|---|
| x < 32 · x > 1888 | margins | No text glyph starts left of x 32 or ends past x 1888: the content edge (`--m-edge`, 40 px) with 8 px of glyph tolerance, read from the deck itself. Decorative art bleeds freely; text never does. |
| y 73–201 | headline block | Only `.headline` (+ `.subtitle` at 177). Content never rises above y 240 except panel/canvas compositions that own the full height. |
| y 985–1080 | footer furniture | Only `.footer-brand`, `.pageno`, `.confidential`, `.source`. No other TEXT enters this band, ever. |
| Furniture anchor corners: bottom-left (0–420, 1000–1080) and bottom-right (1500–1920, 1000–1080) | furniture legibility | Decorative fills entering these corners must leave the furniture readable: the verifier samples the pixels under each furniture line and fails contrast < 2:1 (warns < 3:1). White/Cream shapes under Navy text pass; same-tone shapes under same-tone text are the classic failure (a cream dot under the cream `PRIVATE & CONFIDENTIAL` line on a navy slide). |

### 15.2 Overlap laws (the collision register)

1. **Text never intersects text.** Two text-bearing elements from different
   components may not overlap by more than 4 px in both axes. This includes
   display numerals vs their own captions (a 280 px `.hero-num--l` line box
   WILL collide with a `.col-sub` below it inside a 768 px panel: size down).
2. **Decoration never covers more than 30 % of a text block.** Dots, motifs,
   ghost numerals, rules and panels either stay clear of text boxes or the text
   moves. The sanctioned escape hatch for a deliberate composition is
   `data-text-safe="true"` on the decor element: the verifier downgrades to a
   printed WARN and the art pass must confirm legibility by eye.
3. **Body copy never sits on halftone or texture art.** Statements and
   headlines may cross *sparse* texture only when the art-direction pass
   confirms contrast by eye; paragraphs (< 28 px) never do. The comparative
   layout's `.compare-art` centrepiece (`comparison-v1`) is sized by CSS
   (`width:100%` on its img; never remove it); its text zones at x 40–410 /
   1470–1840 exist because the art stays inside x 478–1442.
4. **Ghost numerals (`.num-ghost`) live in text-free zones.** Same-colour ghost
   + statement = both illegible. Differentiate by POSITION (right of or below
   the text box), never by opacity (§12.14).
5. **Diagram hairlines keep 24 px clearance from glyphs.** A vrule crossing a
   `−` sign turns "−50%" into "+50%": rules, stems and ticks sit ≥ 24 px from
   any glyph edge (40 px for display-size numerals), and identical siblings use
   identical clearance.
6. **One art layer per canvas zone.** A dot field and a motif or texture never
   occupy the same region of a slide: the later one paints over the circles and
   reads as a rendering error, not a composition. Statement recipes take the
   accent field (`statement-quote-v1`) **or** the motif (`-v2b`), never both;
   when two art devices genuinely coexist on one slide they live in separate
   zones (e.g. `field-tl` + `motif--bottom`).

### 15.3 Alignment laws (the grid is not a suggestion)

- **Siblings share edges.** Same-component siblings (columns, cards, KPIs,
  milestones, links inside cards) align their tops within 6 px and their gaps
  within 8 px. Auto-sized (`max-content`) grid tracks drift when content
  lengths differ; the kit's `.hero-row`/`.kpi-row` are `grid-auto-columns:1fr`
  for exactly this reason. Don't override to auto.
- **Timelines run on two lanes.** Above-axis milestones share ONE top edge,
  below-axis milestones share ONE top edge; stem length absorbs copy-length
  differences. One milestone width per slide.
- **Pinned, not flowed.** Anything that must share a baseline across sibling
  containers (card links, panel captions) is pinned (`margin-top:auto` or
  absolute), never flowed after variable-length copy.
- **Centre-anchored nodes.** Radial and orbit nodes anchor by their centre
  (`translate(-50%,-50%)`) at exact clock positions: top-left anchoring skews
  every label by half its own width.
- **Diagrams centre on the slide midline (x 960)** unless a content column
  justifies the offset; an unexplained 100 px skew reads as an accident.
- **One geometry per furniture element per deck.** The `.takeaway` bracket band
  lives at x 160 / y ≈ 877 everywhere; in split layouts adjust `right`, never
  `left`. Source lines, subtitles and takeaways sit at the same y on every slide
  that carries them.

### 15.4 Spacing & fit laws

- **Containers fit their content and content fits its container.** Display
  numerals must fit their panel's inner width (768 px navy panel − 2 × 56
  padding = 656 px: ≈ 4 thin glyphs at 240 px; measure, then size). Text inside
  circles stays within 70 % of the diameter. Cards hug content height
  (`.proc--cards` is 260→700 + takeaway): a card whose bottom half is empty
  white is a composition failure, not whitespace.
- **Minimum clearances:** 24 px text↔hairline, 40 px text↔display-rule, 40 px
  text↔unrelated art edge, 36 px padding inside white surfaces (`.tbx`,
  `.card`, `.cell`).
- **No accidental dead bands.** A full-width empty strip > 280 px inside
  y 240–880 must be either declared (`data-composition="intentional-air"` on
  statement-class slides) or filled by the recipe's anchor (ruler, takeaway,
  field). The `stats-v1` quartet keeps its bottom ruler for exactly this reason.

### 15.5 Contrast floor (measured, not assumed)

- Body copy ≥ 4.5:1, display type ≥ 3:1 against its EFFECTIVE background: the
  pixels actually behind it, not the slide colour.
- Footer furniture ≥ 3:1 always (the verifier samples it; < 2:1 fails the
  build).
- Thin (weight 100) orange numerals: Orange 700 on Cream measures about 2.5:1,
  sanctioned ONLY as ≥ 64 px wayfinding numerals inside the fixed slides (the
  agenda). Content-slide numerals default to **Orange 800** (`.proc .n` ships
  that way) or Navy.
- Guideline 01's contrast table governs colour pairs; this law extends it to
  text over art: when text must cross art, the art under the glyphs is what
  counts.

### 15.6 Vertical balance

Content bands centre between the headline block's bottom (y ≈ 201 with the
eyebrow, ≈ 122 for a one-line headline without it) and their anchor (takeaway
top y ≈ 877, or the footer band). Top-heavy compositions with all mass above the
fold and 40 %+ empty below read as unfinished: anchor the bottom (takeaway,
ruler, KPI band, field) or centre the mass.

### 15.7 Motion UX laws (why the deck never "teleports")

§14 says what may move; these laws say what must NEVER happen. Each one is wired
into the shell and listed here so nobody undoes it:

1. **Choreography ends exactly at static layout.** Every entrance keyframe's end
   state equals the element's resting geometry; captures with `?motion=off` are
   the reference the animated deck must settle into.
2. **No property is contested.** Entrances own `translate`/`scale`/`opacity`;
   the pointer parallax owns `transform`; hover states own `transform` (lifts,
   buttons) or `scale` where no entrance animates it. A hover transition on a
   property an entrance keyframe animates completes invisibly under the
   animation, then SNAPS on release: the #1 teleport cause.
3. **Count-ups never reflow.** Counting numerals pin their final width
   (`min-width` for the duration + `tabular-nums` + `1fr` tracks) so ticking
   digits can't resize columns or re-wrap neighbours. Numerals with word
   suffixes ('1 Sep', '12 weeks') never count.
4. **Kinetic type splits before first paint.** Word-span splitting after display
   re-runs text-wrap balancing and can visibly re-break lines (Safari); the shell
   splits at load.
5. **Re-showing the current slide is a no-op.** Boundary keys and same-hash
   navigation must not replay choreography on a visible slide.
6. **Parallax variables are seeded** (0,0) so the first pointer event eases from
   rest instead of lurching from an unset state.

### 15.9 Placement laws (v4): the content edge and media anchoring

1. **Content-edge conformance.** On every non-bleed content slide the leftmost
   text block starts at the deck's content edge, x = 40 (`--m-edge`), or its
   text edge, x = 56 (`--m-text`), ± 6. The verifier reads both edges from the
   deck and WARNs when the `.headline` sits at neither (guideline 03, the
   margin-consistency law). A slide whose left side a panel or edge-bled media
   owns, and the fixed slides, are exempt.
2. **Media anchoring.** Any rendered media block ≥ 200 × 200 px (`<img>`, motif
   host, `.duo`, photo panel) must touch at least one canvas edge (bleed), sit
   in a canvas corner, or carry `data-inset-ok` (implied by `.screenshot`;
   granted to tiles, portraits and centrepieces whose inset placement is the
   composition: inside `.card`, `.cell`, `.person`, a placeholder, a logo row,
   `.compare-art`, a backdrop motif or the cover art). Three or more media of
   the same size are a set (a team row, a card row, a logo grid) and exempt
   too. One rectangle floating inside the margins on all four sides is a FAIL:
   corner it or bleed it (the Photo card). Decorative dots and icons are not
   media; they are exempt.

### 15.10 Type-size floor (v4)

Measured on the rendered DOM against guideline 02's floors: **nothing is set
below 16 px**, whatever role it plays (FAIL); **between 16 and 20 px only the
fine-print roles the BodyCopy card lists** are allowed, read from
`design-system/elements.json`, and anything else there FAILs. A role counts on
the element or on any of its four nearest ancestors, so emphasis inside fine
print keeps the tier. The four furniture elements (`.pageno`, `.confidential`,
`.source`, `.footer-brand`) are frozen at their shipped sizes (11 px and up) and
exempt; no new text may join them at that scale. A template that needs the
fine-print tier adds the role class beside its own (`class="fine-label
ssp-label"`) rather than its own class to the card, or the list stops being
closed. If copy does not fit at its floor, the slide has too much content:
split it or cut, never shrink the type.

### 15.8 Enforcement

`python3 scripts/verify_deck.py deck.html --screenshots shots/` runs, on top of
the brand checks: glyph-accurate **overlap / margin / footer-band / grid-drift
geometry** (15.1–15.3), **furniture contrast sampling** (15.1/15.5), and the v4
probes: **type-size floor** (15.10), **content-edge conformance** (15.9.1),
**media anchoring** (15.9.2), and the **card-grid static check** (§12.14).
FAILs block delivery; WARNs (including every `data-text-safe` and
`intentional-air` declaration) are re-checked by eye in the §12.15a art pass.
The art pass judges what the ruler can't (balance, rhythm, legibility over
art); the ruler catches what eyes skim past (a 4 px overlap, a 1.04:1 footer).
A deck ships only when both agree.

**Write `class` first on every `<section>`, and never trust a green run that did
not say how many slides it parsed.** Both `verify_deck.parse_slides` and
`check_capacity.slides_of` used to require `class` to be the FIRST attribute in
the tag. A perfectly valid `<section data-x="…" class="slide">` was therefore
not a slide to them, while the browser still rendered it and the screenshot
pass still shot it. The two lists then drifted out of step, and every geometry
and composition finding after the first such section was reported against the
WRONG slide id, with the skipped slides never checked at all. The run stays
green throughout, which is the worst way for a checker to be wrong.

Found 2026-09-11 by building a real client deck; both parsers now accept `class`
anywhere in the tag, and `check_slide_parse` FAILs when any section carrying a
`data-slide-id` did not parse as a slide. If you add a third consumer of the
slide list, give it the same gate: the failure is silent by construction.

---

# Only when it applies

## 13.4 Interaction patterns (interactive HTML decks)

Slides that are read on screen (not printed) can carry lightweight interaction.
**Anything that expands, opens a detail view or is otherwise clickable uses the
one house pattern, the CardLink card's**: do not invent a different hover or
affordance per deck. It keeps interactive decks feeling like one system and
makes it obvious to a viewer that something *can* be opened.

**The deck runtime already wires the behaviour:** a single click (or Enter or
Space when focused) toggles a card's detail view, and the click-to-advance
handler explicitly ignores cards and other interactive elements: **a click on a
card never advances the slide**.

**Individual expansion (v4 law):** every expandable element opens and closes
**on its own**: opening one card never opens, moves, or resizes anything else on
the slide. The opened card's detail drops OVER the content below as a flat white
panel (an overlay, not a reflow); closed siblings keep their exact position and
height. Mechanically: card grids use `.canvas-grid--cards` (§12.14), and the
toggle syncs `aria-expanded` per card. Never build an "accordion" where opening
one item closes another; each is independent.

**The pattern, as the kit ships it** (`bundle.css`; the look is the CardBox and
CardLink cards'):

1. **Card at rest**: `.card`, flat, borderless, square-cornered, no shadow. The
   affordance lives in the hover state and the link, so the resting slide stays
   quiet.
2. **Hover on the card**: a 2 px Orange 600 `outline` (never `border`, so
   nothing reflows), and the card's link turns from Navy to Orange 700, its
   arrow nudging right. Focus shows a 2 px Navy outline.
3. **The link**: `<span class="card-cta">More <span class="arrow">→</span></span>`,
   a word or two and an arrow, pinned to the card's foot (`margin-top:auto` in a
   flex column) so the links line up across a row. `.card-detail` holds what
   the card opens.

**Behaviour & accessibility.** The whole card opens on a click and on Enter or
Space when focused, and carries `tabindex="0"`, `role="button"` and an
`aria-label` ("Open full story: …"), so mouse, trackpad and keyboard users all
have a way in. `prefers-reduced-motion` drops the transitions (the shell's print
and reduced-motion rules already cover this). Static and print decks show no
hover affordance.

Assemble from the `cards-v*` variants in `assets/snippets/variants/`; don't
re-derive.

## 14. Motion system (v3.2) — the deck feels alive, the brand stays flat

Guideline 10 is the design system's record of what moves and how: the doctrine,
the entrance choreography, the durations, the progress line and the five motion
hooks (`m-lead`, `m-art`, `m-unit`, `m-mark`, `m-bar`) a canon template declares
beside its own classes, on the outermost repeated element. This section is the
HTML runtime that carries it out.

- **The spec key.** `"motion": "full" | "subtle" | "off"`; left out, the
  direction decides (high-impact and statement-led `full`, the others
  `subtle`). The shell applies it at runtime: layouts need no markup changes.
- **The hooks are a closed list.** The choreography is driven by `M_ROLES`, a
  closed list of selectors in `build_shell.py`: the kit's classes plus the five
  hooks at its head, whose order sets the reading order. A canon template that
  declares no hook animates nothing but the slide fade.
- **Data counts up** (both levels): `.hero-num`, `.hero-row .n`, `.kpi .v`,
  `.stat-circle .v`, `.proc .n` animate 0 → value (~950 ms) on first reveal,
  preserving comma decimals, dot thousands, prefixes and suffixes and
  zero-padding. Any other numeral opts in with a bare `data-count` attribute.
- **Ambient life** (`full` only): dots breathe (scale ≤ 1.055, 7.5 s alternate,
  desynced), motif art floats ±14 px (9 s), `.duo` photos take a slow Ken Burns
  (scale ≤ 1.07 over 16 s), sparks twinkle. Never on text.
- **Pointer parallax** (`full` only): art layers only (dot fields ≤ 14 px,
  motifs ≤ 24 px, ghost numerals ≤ 34 px); text never moves.
- **Hover states** (hover-capable screens, any level except `off`): cards and
  process steps lift 8 px, columns, KPIs and milestones 6 px, stat circles and
  hero numerals swell about 5 % on the sanctioned spring, the takeaway's bracket
  arms stretch, agenda rows nudge right. Movement only: hover never changes a
  colour outside the §13.4 card pattern.
- **The progress line** (any level except `off`): the 3 px Orange 700 line along
  the bottom edge, growing with deck position. Hidden in print.
- **Kinetic type** (both levels): Big Statements, Big Quotes, divider titles and
  the cover title split into word spans at load and rise word by word. Plain
  text elements only; the shell handles it, never hand-split.
- **Fragments** (`data-build`, opt-in per element): blocks marked `data-build`
  hide on slide entry and reveal one per forward step (→, Space or click) before
  the deck advances. Use on parallel blocks (cards, steps, columns), 3–5 per
  slide at most, on one or two slides of a deck; print and motion off show
  everything.
- **Deterministic capture:** the verifier and any headless or PDF path pin
  `?motion=off` in the URL, so screenshots and prints always see the finished
  layout, never a mid-entrance frame.
- **Always static:** `prefers-reduced-motion`, print and PDF, and headless
  capture (`navigator.webdriver`) force `off`. URL override for testing:
  `?motion=off|subtle|full` (`?motion=force` keeps full even headless, for
  motion smoke tests).

Never add per-deck keyframes, easing, or a motion library (no React, no GSAP:
the deck stays ONE dependency-free file). A new motion behaviour is a change to
the design system's guideline 10 first, then to `build_shell.py`.

---

# Where the other section numbers went

The old guideline's brand sections now live in the design system, and on this
path in its copy under `design-system/`. Comments in the layouts (including the
design system's own previews) still cite some of the old numbers; this is where
each one went.

| Old § | Now |
|---|---|
| §1 Brand essence | `README.md`, *The eight things that matter*; §1.4, the orange text moments: `README.md`, *Colour, in one page* |
| §2 Canvas, grid & spacing | `README.md`, *The canvas*; guideline 03 |
| §3 Colour | guideline 01: §3.1 *Primary*, §3.2 *Secondary*, §3.3 *The role mapping*, §3.3a *Do not mix warm and cold whites*, §3.4 *Sanctioned background × dot pairings*, §3.5 *Contrast*, §3.6 *Tertiary*; §3.7 the tokens, `tokens.json`; §3.8 semantic data colours, guideline 09 *Direction semantics* and the KpiRow card |
| §4 Typography | guideline 02; §4.4 the title highlight, the Headline card; §4.5 the minimum sizes, guideline 02 *Floors* and the BodyCopy card (measured: §15.10 here) |
| §5 The dot system | guideline 04 and the DotField card |
| §6 Logo | guideline 05 and the Logos notes in `asset-notes.md` |
| §7 Slide furniture | guideline 06, the Headline and FooterFurniture cards |
| §8 Iconography | guideline 07, the Icon card and the Icons notes |
| §9 Illustration & photography | guideline 08; §9.1a, §9.1b and §9.2a the Illustrations, Textures and Photography notes in `asset-notes.md`; §9.1c the halftone converter, §13.3 here; §9.2 the Photo card |
| §10 Data visualisation | guideline 09, the StatCircle and KpiRow cards |
| §11 Backgrounds by moment | `README.md`, *Colour, in one page*; guideline 01 (dark slides by direction, the per-deck colourways); guideline 04 (dots by slide density); the DividerSlide and ThankYouSlide cards |
| §12 (§12.0–§12.13) Slide archetype library | the fixed slides: `README.md`, *Components*, and the cards in `cards/fixed-slides.md` (§12.1a CoverSlide, §12.2 AgendaSlide, §12.3 DividerSlide, §12.13 ThankYouSlide); §12.4–§12.12, guideline 03 *Archetypes* and the layout cards in `cards/layouts-*.md` |
| §12.16 Sanctioned flexibilities | the direction table in `SKILL.md`; guidelines 03, 04 and 08 |
| §14.5 Revising a delivered deck | `references/REVISING.md` |
