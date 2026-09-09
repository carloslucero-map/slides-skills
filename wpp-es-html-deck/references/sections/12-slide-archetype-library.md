## 12. Slide archetype library

The source template ships 95 layouts. They reduce to these archetypes — when converting an outline, pick the closest archetype per slide. All coordinates are for the 1920 × 1080 canvas and match the generator/snippets.

### 12.0 Locked deck defaults (non-negotiable)

Five things about a deck are **fixed** and must be applied every time an outline is turned into an HTML deck — no re-designing, no per-deck variation. They exist so the output is consistent from deck to deck. Deviate only when **the deck owner / the user** explicitly asks. **Choices the skill explicitly offers at its checkpoint (design direction, per-deck divider colourway, registered cover, outro) are sanctioned user decisions, not deviations.**

1. **Content background is always Cream `#FAFAF0`.** Every content slide sits on the one warm Cream field — never pure White, never alternating (§3.3a, §11). Navy is only for the occasional deliberate dark moment; the default `.slide` is Cream.
2. **Title slide = short title + longer subheader** inside the locked cover frame (§12.1a): a **short title (2–4 words, ALL CAPS)** with a **longer plain-sentence subheader** beneath it. Cover art comes from the registry (`mountain` default). Only drop the subheader if the deck owner asks for a title-only cover.
3. **One locked agenda.** The agenda is always the single approved layout (§12.2): "Agenda" headline + a numbered **vertical list** (Thin Orange numerals, Light Navy titles) + the Orange dot cluster off the top-right. No per-item descriptions unless the brief asks.
4. **One locked divider, identical every time.** Every section divider uses the same geometry (§12.3) in the deck's one chosen colourway (§11); only the number, title and sub-label change. Never rotate the colourway between dividers.
5. **Every deck ends with the locked Thank-you slide** (§12.13) — light by default, dark via `outro:"dark"` — whatever the deck is about.

The locked compositions are emitted by the generator's slide builders (scripts/build_shell.py). Never hand-build them and never edit their geometry — change only the spec keys and the content placeholders.

### 12.1a Cover — the locked frame + the registered art (`cover` spec key)

*(This section absorbs the old §12.1 "variants A/B/C" anatomy — the frame below is the only cover spec.)*

**Every internal deck opens with the one locked cover frame. It is emitted by the generator — never designed from scratch.** Only the title slide is locked; body/content slides are still built from the archetypes in this document.

**The locked frame (identical on every registered cover):**

- **Background:** flat **WPP Cream `#FAFAF0`**.
- **Title + subheader + meta, top-left:** deck **title** at (80, 88) in WPP Light 81 px Navy, ALL CAPS — kept **short (2–4 words)**; directly beneath it a **longer subheader** in WPP Light 31 px Navy (one plain-sentence line, max-width 900 px, line-height 1.16); then the **month/year** in WPP Regular 24 px ALL CAPS **Orange 700** and the **presenter name** in WPP Regular 24 px Navy (omitted cleanly when `presenter` is `""`).
- **Logo, bottom-right — WHITE lockup on a solid NAVY BADGE (mandatory, non-negotiable):** the white MAP lockup, 300 px wide, sits **inside a solid WPP Navy rectangular badge flush to the bottom-right corner** (`right:0; bottom:0`, padding `46px 80px 60px 64px`). **Never float the bare white lockup directly over the artwork** — halftone art has light and transparent passages that wash a white logo out. The badge guarantees the full `WPP Enterprise Solutions | MAP` lockup always reads, whatever falls behind it (§6.3).
- Covers carry no footer strip (§7.3).

**The cover registry** — all registered covers are art-swaps inside the SAME locked frame (type block, meta, navy badge untouched), selected via the `cover` spec key:

| Key | Art | Treatment |
|---|---|---|
| **`mountain`** | `WPPOpen_Mountain-01.png` | **THE LOCKED DEFAULT.** Full-bleed (`object-fit:cover`) — navy halftone peaks on the right, Cream carries the type top-left. |
| `crystal` | `WPPOpen_Crystal-01.png` | Right-anchored motif: 1440 px wide, vertically centred, bleeding off the right edge. |
| `coral` | `WPPOpen_Coral-01.png` | Right-anchored motif, same treatment as `crystal`. |
| `dots` | none (pure CSS) | Tone-on-tone composition of white macro circles (Ø 900/560/300) with an Orange 500 mid dot and a small Orange 600 accent, anchored to the right — no raster payload. |
| `playbook` (v4) | none (pure CSS) | The playbook's own cover language (p.1): pure type on Cream — the title block set in hairline caps with the meta lines in Orange 700, plus a sparse Orange 600 mid-dot scatter drifting off the top-right (one fused pair). Zero raster payload; the quietest, most parent-brand cover. |

Unless the deck owner picks an alternate at the checkpoint, always open with `mountain`. Never ship a hand-designed cover.

**Adding a new variant (the extract-and-verify workflow)** — applies to any new cover *or* slide variant, and only when the deck owner explicitly wants one:

1. **Extract** the approved design from source (slide XML or the owner's spec) — exact placeholders, x/y/size geometry (pt → px × 1.5), fills, and assets.
2. **Verify by screenshot.** Render it and compare 1:1 against the supplied reference; correct until the render matches.
3. **Register it in the generator** (a new registry entry / snippet) before first use. Unregistered variants never ship.

### 12.2 Table of Contents / Agenda — the locked default

**The agenda is a single locked layout — the generator emits it every time.** Do not switch between a list and a grid deck-to-deck.

- Background: flat **WPP Cream**. "Agenda" headline top-left in WPP Light 54 px Navy at (80, 112).
- Chapters as a **numbered vertical list**: each row = a WPP Thin **Orange 700** numeral (`1.` 88 px, in a 118 px column, gap 44) + a WPP Light Navy chapter title (50 px).
- Two geometries, switched automatically by chapter count:
  - **≤ 5 chapters:** rows start at top **266**, stepping **148** px per row; numeral **88** px.
  - **Exactly 6 chapters (dense mode):** rows start at top **224**, stepping **128** px; numeral **72** px (98 px column), titles 42 px.
- **Hard max: 6 chapters.** The generator refuses more — split the deck into parts. Chapter titles ≤ **45 characters**, or the row runs under the dot cluster.
- One fixed **Orange dot cluster** bleeding off the top-right corner: a large Orange 700 dot (Ø 360), an Orange 600 mid dot (Ø 150) and a small Orange 800 accent (Ø 80). The agenda cluster is **always this Orange trio**, independent of the deck's divider colourway.
- **No subtitle / no per-item descriptions unless explicitly requested.** By default a row is just the numeral + chapter title — clean and airy.
- Footer brand line + page number as §7.3.

### 12.3 Divider (section header) — v4: the playbook composition is the locked default

The playbook's own section dividers (pp. 14, 19, 27, 30, 42, 44) are the model: **full-bleed field + macro circles in ONE hue bleeding off ≥ 2 edges + a giant hairline title pinned to the bottom-left, allowed to overlap the circles.**

**The locked v4 geometry (`dividerStyle:"playbook"`, the default):**

- Section number `05.` top-left at (80, 56): WPP Thin **104 px**.
- Section title bottom-left, pinned LOW (bottom inset 96): WPP Thin **136 px** ALL CAPS, line-height 0.88, max-width 1560 px, `text-wrap:balance`. The title may overlap the circles (display type over flat dots is playbook-sanctioned); locked dividers are exempt from the §15.1 footer-band law, but the brand line/pageno must stay legible (§15.1 contrast sampling still applies).
- Sub-label ABOVE the title (left 84, anchored to the title's top): WPP Medium 22 px ALL CAPS — **Orange 800** (Orange 600 on `navy-full`).
- **The scatter:** 5–7 macro/mid circles in the deck's ONE divider hue (via `dividerColourway`, §11) scattered across the top and right of the canvas — at least two bleeding off different edges, exactly one fused pair, none entering the title's clear zone (left/bottom quadrant) and none making the footer illegible. Drawn by the `divider-playbook` `data-dots` preset — geometry verbatim, never hand-edited.
- **Identical on every section** — same composition, same geometry; only the numeral, title and sub-label change.
- Footer brand line + page number as §7.3, contrast auto-handled per colourway.

**The classic v3 geometry survives as `dividerStyle:"classic"`** (registered variant, not a deviation): number top-left, title at bottom inset 214 at 104 px, sub-label below, the four right-anchored macro dots (Ø 760/560/180/90). Same colourway system either way.

### 12.4 Big Statement
- One sentence, WPP Thin **150 px default** (81–180 range for shorter/longer statements), Navy, left-aligned at x = 80 and vertically centred, line-height 0.82, max-width 1640 px, on an otherwise empty cream canvas.
- Variants: with supporting paragraph (24–26 px Light below), with halftone motif side, with a lift dot cluster, vertical composition.
- Assemble from `assets/snippets/statement-quote.html` — don't re-derive.

### 12.5 Big Quote
- Quote in WPP Thin 120 px with typographic quotation marks at (120, 170), max-width 1620 px, line-height 1.04, max ~4 lines.
- Attribution in Medium ALL CAPS 30 px at left 120 / bottom 190.
- Assemble from `assets/snippets/statement-quote.html` — don't re-derive.

### 12.6 Title + Content (1/2/3/4 columns)
- Furniture per §7. Column grid starts at (80, 260); gaps 80 px (56 px for 4-col); widths per §2 (840 / ≈533 / 398).
- Each column: optional **Medium ALL-CAPS subheader** (24 px) or a 16 px dot bullet, then Light body (24 px; 22 px in 4-col).
- **4-col with Dot Header**: each column headed by a dotted icon (§8.1 fallback) + subheader.
- **4-col with Pills**: navy pill labels (§5) beneath columns.
- Assemble from `assets/snippets/columns.html` — don't re-derive.

### 12.7 Text boxes ×3–×8 (with Dots or Arrows)
- Title as usual; a row of equal flat White boxes starting at (80, 280), gap 28, padding 32 × 36, body 22 px (or two rows of 3/4 for ×6/×8).
- Between boxes: a **16 px navy dot** (relationship) or the **navy triangle arrow** (sequence/flow) vertically centred in the gutter.
- Assemble from `assets/snippets/boxes.html` — don't re-derive.

### 12.8 Comparative (rocks / ribbon)
- Two-sided comparison: a shipped accent motif (rocks or ribbon, §9.1a — pick the colourway that matches the deck's family: `rocks`/`ribbon-navy` for navy decks, `rocks-orange`/`ribbon-orange` for orange) centred at 964 px wide; 420 px label columns left and right at top 420, 24 px Light.
- **Family exemption:** the `.compare-art` centrepiece is furniture of this archetype — it does NOT count against the deck's one-motif-family rule (SKILL.md). Prefer the colourway variant closest to the deck's family.
- Assemble from `assets/snippets/comparison.html` — don't re-derive.

### 12.9 Image layouts — v4: media anchors to edges (the anchoring law, §15.9)

**A rectangular media block never floats in the middle of the canvas.** A photo/motif crop that ends in naked rectangular cuts on all four sides, surrounded by margin, reads as a placed thumbnail, not a composition. Every media block ≥ ~200 × 200 px does ONE of:

1. **Bleeds to at least one canvas edge** (`.media--bleed-r/-l/-b/-t` or the half/panel layouts) — the sanctioned exception to the 80 px margin: edge-bled media runs to x = 0 / 1920, y = 0 / 1080.
2. **Sits in a canvas corner** (two of its sides ON the edges — `.media--corner-br` etc.).
3. **Is declared inset** (`data-inset-ok`) — reserved for `.screenshot` (whose keyline frame IS the treatment and which must never bleed) and for grid-mosaic tiles whose gutters are the composition.

The layouts:

- **Title + Content with Image (v4)**: text column left (640 px at (80, 260)), media right **bled to the right edge** (from x 880 to 1920, top 240 to bottom 140, `object-fit:cover`) — the outer margin opens for the image, the inner edge holds the grid.
- **Half Image**: image fills the right 960 px, full height (edges top/right/bottom).
- **Image with Title**: full-bleed halftone/photo + big ALL-CAPS Thin title.
- **Dot hero (v4)**: a `halftone.py` conversion as the art half of a split — the "pixelated" website look (§9.1c).
- **Screenshots**: 1 px Navy outline (`.screenshot`), never a drop shadow, never full-bleed — the one sanctioned inset (`data-inset-ok` is implied by the class).
- Assemble from `assets/snippets/image-content.html` — don't re-derive.

### 12.10 Team slides
- Grid of 3 or 4 per row at (80, 280), gap 64: circular portrait (Ø 180 px, navy placeholder) + `Firstname Lastname` (Medium 24), role/department/city (Light 20), short bio (Light 16).
- Assemble from `assets/snippets/team.html` — don't re-derive.

### 12.11 Process (×5) & Timelines
- **Process boxes ×5**: five numbered columns at (80, 300), gap 40 — Thin **Orange 700** numeral (64 px), Medium ALL-CAPS step label (15 px), Light body (20 px).
- **Timeline**: a 1 px navy axis at y = 540, 16 px dot nodes (Orange 700 for accents), Medium ALL-CAPS 16 px labels below.
- **Roadmap / horizontal steps**: `START → …` with stat blocks; phases labelled `PHASE 1…` with dot markers on the thin line.
- Assemble from `assets/snippets/process-timeline.html` — don't re-derive.

### 12.12 Data-viz slides
- **Bubble pipeline**: big Thin ALL-CAPS title left, composition of flat circles right (§10) — `.stat-circle` (Navy fill, White Thin 90 px value, Medium 18 px label; `--orange` variant flips to Orange 700 / Navy).
- **Impact stats**: diagonal chain of circles + external stat callouts with thin connector lines + short narrative paragraph right.
- **Dashboard**: KPI row (Thin 110 px values) + description + percentage circles.
- **Charts**: bar/line charts flat navy/orange, Light labels; headline + eyebrow furniture unchanged.
- **Data honesty (hard rule): bubble/circle AREA is proportional to value — diameter ∝ √value.** Diameter-proportional bubbles exaggerate ratios quadratically and are a distortion; they are **banned**. When two circles represent 4× the value, the bigger one is 2× the diameter, never 4×.
- Assemble from `assets/snippets/stats.html` + `assets/snippets/charts.html` — don't re-derive.

### 12.13 Outro / Thank-you — the locked, mandatory close

**Every deck ends with the locked Thank-you slide — no exceptions.** It is always the last slide, whatever the deck is about.

- **Light (default):** flat WPP Cream, `Thank you.` in WPP Light 99 px Navy, left-aligned at (80, 430); Orange dot composition anchored bottom-right, bleeding off-canvas — a large Orange 700 dot (Ø 760, bottom-right), an Orange 600 dot (Ø 300, top-right) and a small Orange 800 accent (Ø 150).
- **Dark (`outro:"dark"`, sanctioned for statement-led decks):** Navy field, White text, the same geometry with Cream/White macro dots + an Orange 700 accent; footer contrast auto-handled (§11).
- Footer brand line + page number as §7.3.
- **Optional contact block** (via the `contact` spec key): name / role / email at (80, 580), 24 px Light. Otherwise the clean word-only close.
- Localized automatically: `lang:"es"` renders `Gracias.` (or override via `strings`).

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
- **C4 — Type discipline.** ≤ 2 text scales + ≤ 1 display moment; body ≥ 20 px; headline ≤ 2 lines.
- **C5 — Collisions.** Nothing under the footer zone (bottom-right 500 × 90); headline clear of art; text never over navy dots or dense halftone.
- **C6 — Deck rhythm.** No two adjacent content slides share archetype + treatment; decks of 8+ content slides use ≥ 2 density variants and ≥ 3 recipes.
- **C7 — Colour quota.** The slide respects its direction's colour quota per §11.

Note: `verify_deck.py` enforces C2 numerically as a tripwire; the pass itself is done BY LOOKING at each slide's screenshot.

**Declared air:** thin display type is pixel-light, so a template-faithful display slide (an R3 quartet over a hairline ruler) can trip the tripwire while being perfectly composed. When — and only when — the air is shaped (hairlines, rulers or counterweights carry the eye through it), declare `data-composition="intentional-air"` on the section: the verifier downgrades its FAILs to WARNs and always prints the declaration, and the G2 seen-report must name it. Never declare air on an undesigned slide.

### 12.16 Sanctioned flexibilities (v3)

Four registered liberties — sanctioned composition, not deviation (§12.0):

- **(a) Full-bleed navy/tint content moments**, per the design direction's quota (high-impact: up to 1-in-3; others per their row in SKILL.md).
- **(b) Halftone motifs as art on any content slide** via the placement utilities, respecting the text-safe zones: `--right` keeps text left of x = 1200 · `--bottom` keeps text above y = 560 · `--backdrop` behind stat compositions only · `--panel` inside panels · `--bleed` only for R11 posters. One motif family per deck, repeated — never rotated slide-to-slide.
- **(c) Giant numerals 200–320 px** — `.hero-num--l/--xl`, and `.num-ghost` in flat sanctioned tones only (§12.14).
- **(d) Split colour-blocks** — recipe R13.
- **(e) Duotone photography (v3.3)** — `.duo` navy-duotone photo moments per
  §9.2: hero splits, panel fills, R11 posters (high-impact). Counts against
  the direction's dark-moment quota.
- **(f) Dot-halftone conversions (v4)** — brief imagery converted with
  `scripts/halftone.py` (§9.1c) used as hero art: split halves, statement
  counterweights, R11 posters. One conversion colourway per deck (it joins
  the one-motif-family rule).
- **(g) Dot register fields (v4)** — the `field-micro` / `field-mid` /
  `field-macro` presets (§5) as content-slide counterweights, one hue,
  respecting the §3.4 combos and the navy-dots-never-near-text law.

**Still locked (unchanged by v4):** cover frame · agenda · divider geometry (now the §12.3 playbook composition) · thank-you · Cream default background · palette · WPP Sans weights · flat fills (no gradients/shadows) · footer furniture · area-true bubbles · no full-colour photography outside the `.screenshot` keyline.

Flexibility means more sanctioned composition, never new colours, fonts, or effects.

---

