## 12.14–12.15a — Composition

<!-- Split out of 12-slide-archetype-library.md. These three subsections are
     hoisted verbatim into CORE.md because verify_deck.py enforces them on
     every deck — so opening the archetype library used to reload ~2,861
     tokens the model already had in context. -->

### 12.14 Composition guardrails (verified in render QA)

Constraints the kit's geometry imposes — respect them instead of rediscovering them:

- **Lead paragraphs vs grid archetypes:** a `.content-band` lead line fits above `.timeline` (top 540; ≤2 lines) and `.kpi-row` (top 340; exactly 1 line). It collides with `.proc` (top 300) — never combine.
- **Timeline positioning:** nodes are 16 px, so centre with `left:calc(P% − 8px)`; labels take the bare `left:P%` (the class self-centres). Keep nodes within ~5–95% or `nowrap` labels escape the 80 px margins.
- **Stat circles below Ø ~340 px** need inline font downscales (e.g. 68/16 px at Ø 330, 46/12 px at Ø 220) or the value/label overflow the circle.
- **`.img-half-media`** puts the footer furniture ON the image and the headline can run under it: cap the headline with an inline `max-width:820px` and keep the image's bottom-right corner visually light — otherwise use the framed `img-right` layout.
- **`lift-corner` dots** overlap the footer zone by design; their colours are White/Cream so the Navy footer stays readable — do not recolour them darker.
- **Card grids use the `.canvas-grid--cards` modifier** (`grid-auto-rows:auto; align-items:start; align-content:start`) — never the bento's default `grid-auto-rows:1fr`. With `1fr` rows, one opened `.card-detail` stretches every sibling in the row; with the modifier, **each card expands individually: the opened `.card-detail` renders as a flat white overlay dropping over whatever sits below, and no sibling ever moves or stretches** (§13.4). The verifier fails a `.card` inside a `1fr`-rows grid.
- **`.col-sub` carries `margin-bottom:18px`** — zero it inline when reusing it as a row label inside a centred grid (e.g. bar-chart rows).
- **Panel headline cap:** when a right-side `.panel` is ≥ 768 px wide (`--w768`/`--w960`), cap the headline with an inline `max-width:1040px` or it runs under the panel.
- **Motif text-safe zones:** `.motif--right` keeps text left of x = 1200; `.motif--bottom` keeps text above y = 560; `.motif--backdrop` sits behind stat compositions only; `.motif--panel` lives inside panels; `.motif--bleed` is only for R11 posters (§12.16 (b)).
- **`field-navy` dots never sit behind text** — place them only where the composition leaves that zone empty (§5, §3.4).
- **`.takeaway` holds ONE line, ≤ 90 characters** — a second line collides with the footer furniture.
- **`.num-ghost` uses flat sanctioned tones only:** Orange 500 on Cream, White/Cream on Navy — never opacity tricks, never other colours.
- **`.canvas-grid` cells need explicit `grid-column`/`grid-row` spans inline** — auto-placement produces even boxes, not the asymmetric bento the recipes call for (R2).

### 12.15 Composition recipes (mined from the template)

These 17 recipes are the template's own full-canvas compositions, translated to the kit (all coordinates re-extracted from the source slides; 1920 × 1080 canvas). **Content slides are ASSEMBLED FROM RECIPES, never from bare text bands** — a headline over a `.content-band` of copy is a draft, not a slide. **The first variant of every snippet file is a full-canvas recipe — pasting it unmodified must pass §12.15a.** Registry format: name · template source · geometry (px) · kit classes · snippet file · direction affinity.

- **R1 · Split rail dashboard** — slide 95 (halves variant: 97). Full-height 440 px rail `.panel .panel--w440 .panel--tint|--nav` carrying 4 stat rows via `.panel-inner` (~y 162/377/589/806; values 60–72 px, labels 20 px); main field: lead paragraph ~(80, 124) 1170 × 170 + KPI row anchored LOW — `.kpi-row .kpi-row--low` (y 747–930). → `splits.html` · data-forward/editorial.
- **R2 · Stat mosaic bento** — slide 96. `.canvas .canvas-grid` 12-col bento: 5 asymmetric `.cell` zones filling the whole band, one hero stat, 2 × 2 stat quads at 60 px. → `charts.html` · data-forward.
- **R3 · Hero numeral quartet + ruler** — slide 94. 3–4 `.hero-row` numerals (`.n` 144 px) in ~244 × 164 boxes at y ≈ 234, CAPS labels y ≈ 361, 380 px bodies y ≈ 440; `.vrule` hairlines x ≈ 520/960/1400, h ≈ 120; bottom `.ruler` y ≈ 881 + `.ruler-ticks` (majors every ~360 px) + `.ruler-label` CAPS y ≈ 931. → `stats.html` · data-forward.
- **R4 · Hub & spokes** — slides 100/103. Centre circle Ø 460–500 at ~(747, 333) — flat navy `.stat-circle` or `.motif--backdrop` — ringed by 6 × 19 px satellite `.dot`s; flanking 475 px columns (`.col-dot` + subhead + body) at x ≈ 81/1399, rows y ≈ 277/516/756. Slide-103 variant: overlapping Ø 501/Ø 423 triptych + bottom index row of 3. → `stats.html` · data-forward.
- **R5 · Cluster diagram + index row** — slide 102. Two Ø 465 navy circles overlapping at (380, 311)/(767, 308), knockout labels, white-text lists inside; Ø 187 satellites; 1 px orange connector lines; bottom row of 6 × (dot + subhead + body) 278 px wide, y 806–959. 100 % active canvas. → `stats.html` **V6 (paste-ready)** · data-forward.
- **R6 · Gantt swimlanes** — slides 90/91. `.gantt` band; `.lane-dot`s x ≈ 42, y ≈ 221/394/567; `.bar`s 6 px flat orange-ramp fills y ≈ 281–532, widths 197–750; `.vrule` guides x ≈ 982/1102/1550/1763; bottom `.flag` chips 206 × 46 at y ≈ 834/914. → `process-timeline.html` · data-forward.
- **R7 · Milestone ruler timeline** — slide 93. Full-width `.ruler` y ≈ 569, alternating year `.ruler-label`s y ≈ 528/600; up to 12 `.stem`s (h 43–183) to `.milestone` blocks ABOVE AND BELOW the line (y range 226–954). → `process-timeline.html` · all directions.
- **R8 · Phase board** — slide 117. Centre `.cell--tint` panel (480, 200) 960 × 680; step headers on the top rule (14 px dots, STEP CAPS labels, `.pill` time chips); 4 body columns 402 × 399; full-width bottom band (40, 880) 1839 × 120 split by white rules. → `process-timeline.html` **V6 (paste-ready)** · editorial/data-forward.
- **R9 · Full-height card row + takeaway bracket** — slides 110/115. 4 white cards 360 × 560 at y = 200 via `.tbx-row .tbx-row--fill` (pill chip + 36 px title + rule + body per card); closer variant: `.takeaway` bracketed 48 px Light line (template bracket arms 23 × 120 at x ≈ 160/1737, band ~(201, 805) 1515 × 115). → `boxes.html` · all directions.
- **R10 · Motif-side statement** — layouts 44/46. `.big-statement` 150–180 px at ~(109, 245), max-width 1500; art side = `.lift` `data-dots="field-right|field-accent"` or `.motif--right` `data-motif`; layout-46 art zone ~(1071, 399) 849 × 681 (text-safe left). → `statement-quote.html` · statement-led.
- **R11 · Full-bleed motif title** — layout 82. `.motif--bleed` `data-motif` full-canvas + ALL-CAPS Thin 108 px title at ~(45, 25). The "chapter poster" moment. → `image-content.html` · statement-led/high-impact.
- **R12 · Tile rail grids** — layouts 69/70/73/74. ×5 portrait rail: 320 × 680 tiles at y = 160 + SUBHEAD rows y ≈ 874; 3 × 2 grid: 560 × 319 tiles; 2 × 2 offset: 639 × 359. Tiles are flat `.cell`/`.cell--nav`/`.cell--tint` panels, stat blocks, or `.motif--panel` crops. → `cards.html` **V4 (paste-ready, 3×2 form)**; ×5 portrait rail hand-built from these coordinates · all.
- **R13 · Split colour-block 40/60** — synthesized from slide 95 + layout 83. `.panel--w768` (40 %) or `.panel--w960` (50 %), `--nav`/`--tint` (`--orange` high-impact only), carrying display type (`.hero-num--l/--xl` or a short statement) or a `.motif--panel`; content columns on the other side; headline capped inline at max-width 1040 px when the right panel is ≥ 768 px (§12.14). → `splits.html` · high-impact/statement-led.
- **R14 · Orbit hub** — inspired by pptx slide 27. 3 concentric `.orbit` rings (dotted circle borders) centred right of the headline, 4 `.orbit-node` labels on the middle ring, `.orbit-hub` centre with navy fill and label. Headline and body text left of centre. → `orbit.html` · editorial/statement-led.
- **R15 · Scorecard bento** — inspired by pptx measurement frameworks. `.canvas .canvas-grid` 3 × 2 with `.cell` blocks, each carrying a category header (`.col-sub` 14 px), hero number (Thin 72 px), and label; one `.cell--nav` contrast moment, one `.cell--tint` highlight max. → `stats.html` V5 · data-forward.
- **R16 · Venn diagram** — inspired by pptx slide 77. `.venn` container with 2–3 `.venn-set` circles (dotted border, translucent fill) overlapping; `.venn-label` inside each set and at the intersection. No motif — the diagram IS the composition. → `comparison.html` V2 · editorial.
- **R17 · Ecosystem map** — inspired by pptx slides 63-64. Centre `.orbit` ring + navy hub; 4 zones (positioned absolutely, top-left / top-right / bottom-left / bottom-right) with dot + `.col-sub` + `.body`; dotted connecting lines between zones and hub. → `process-timeline.html` V5 · editorial/data-forward.

### 12.15a Composition checklist (the art-direction pass)


Seven criteria, each checkable on a screenshot. Every content slide must pass all seven **by looking at its render** — this pass is visual, not textual:

- **C1 — Focal element.** The slide has one: display type ≥ 100 px, a motif, a dot field, a panel, or a chart/stat composition ≥ 300 px tall. A headline alone never qualifies.
- **C2 — No dead lower half.** Composed elements extend below y = 700, and the background fraction in the band y 432–990 is < 0.83 (v4 tightened; the verifier WARNs ≥ 0.83 and FAILs ≥ 0.92). Exception: registered statement/quote slides with deliberately asymmetric air.
- **C3 — Edge anchor.** At least one element touches or bleeds off an edge — or the slide is a deliberate centred statement.
- **C4 — Type discipline.** ≤ 3 text scales + ≤ 1 display moment; body ≥ 20 px; headline ≤ 2 lines. (v4.1: raised from ≤2. The curated selection's real median is 4 distinct sizes per slide; at ≤2 an honestly traced canon fails its own criterion on 21 of 24 measurable slides. ≤3 still forbids the size-soup this rule exists to stop.)
- **C5 — Collisions.** Nothing under the footer zone (bottom-right 500 × 90); headline clear of art; text never over navy dots or dense halftone.
- **C6 — Deck rhythm.** No two adjacent content slides share archetype + treatment; decks of 8+ content slides use ≥ 2 density variants and ≥ 3 recipes.
- **C7 — Colour quota.** The slide respects its direction's colour quota per §11.

Note: `verify_deck.py` enforces C2 numerically as a tripwire; the pass itself is done BY LOOKING at each slide's screenshot.

**Declared air:** thin display type is pixel-light, so a template-faithful display slide (an R3 quartet over a hairline ruler) can trip the tripwire while being perfectly composed. When — and only when — the air is shaped (hairlines, rulers or counterweights carry the eye through it), declare `data-composition="intentional-air"` on the section: the verifier downgrades its FAILs to WARNs and always prints the declaration, and the G2 seen-report must name it. Never declare air on an undesigned slide.
