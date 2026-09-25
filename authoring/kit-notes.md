# Kit authoring notes

The 51 kit layouts live in the design system, and the skill keeps each one as
`wpp-es-html-deck/assets/snippets/variants/<name>.html`. Until release 4.1.3 they
were authored in 13 files, `assets/snippets/<family>.html`. Those files left the
skill once the variants came from the design system, and these are the notes
they carried, verbatim: each family's header, then each layout's own notes.

They are history, not rules. Several predate v4 (the 80px content edge, a 15px
type floor), and where one disagrees with the design system, the design system
wins. A note still worth following belongs on the layout's card there.

## boxes

```text
  boxes.html — R9 full-height card row + takeaway bracket · compact dot/arrow strips (§12.7, §12.15)
  v3 RULE: variant 1 is a FULL-CANVAS composition — pasting it unmodified passes §12.15a.
  JOINERS carry meaning: .sep-dot → related set · .sep-arrow → sequence.
  .tbx is the ONE sanctioned white surface on Cream — flat, square, no borders/shadows.
  .takeaway holds ONE line (<=90 chars) — the house closer, bracket arms included.
```

### `boxes-v1.html`

```text
 V1 · R9 FULL-HEIGHT CARD ROW + TAKEAWAY BRACKET
```

### `boxes-v2.html`

```text
 V2 · COMPACT — related items joined by dots (pair with a lift or takeaway on sparse decks)
```

### `boxes-v3.html`

```text
 V3 · COMPACT — sequence joined by arrows
```

## cards

```text
  cards.html — house expandable card (§13.4): grid of .card with progressive detail
  WHEN
    3-6 topics where the room gets the one-liner and readers can expand for depth
    (FAQ, service catalogue, workstream detail).
  INTERACTION (already wired in the shell's NAV_JS — add NO script here)
    - Click, Enter or Space on a focused .card toggles .is-open, which reveals
      .card-detail — and syncs aria-expanded (v4). Cards do NOT trigger slide
      navigation (nav ignores .card targets).
    - Rest state is flat white; hover draws the Orange 600 outline, the CTA flips
      Navy→Orange 700 and the arrow nudges 4px right — all from the base CSS.
  RULES
    - Every card carries tabindex="0" role="button" aria-expanded="false" exactly as
      below (keyboard reachable; NAV_JS toggles the class — the attribute is static).
    - The grid is the .content-band with an inline grid: 3 columns for 3 cards,
      repeat(2,1fr) for a 2×2 of four. v4 INDIVIDUAL-EXPANSION LAW: V1 uses
      .canvas-grid--cards (auto rows + start alignment); V2's inline grid carries
      align-content:start + align-items:start. Either way each card opens ALONE —
      siblings keep their closed height and the row alignment intentionally breaks
      while a card is open. An opened card grows downward; keep detail copy ≤4 lines
      so it stays inside the band (bottom y=960).
    - .card is a white surface like .tbx — flat, no borders, no shadows.
    - Keep the .slide wrapper, .headline, .footer-brand and the EMPTY .pageno.
      Swap data-slide-id="cX-sY" for the shell placeholder's real id, and keep the
      placeholder's .confidential line if the deck has one.
  v3 RULE: variant 1 is the FULL-CANVAS 2×2 bento — cards fill the band top to bottom.
```

### `cards-v1.html`

```text
 Variant 1 — 2×2 full-height card bento (.canvas-grid--cards: one card expands alone;
     siblings hold their closed height — the broken row while open is the v4 law, not a bug)
```

### `cards-v2.html`

```text
 Variant 2 — three across (compact). §15.3: cards are flex columns with the CTA
     pinned via margin-top:auto so every "More" link shares ONE baseline regardless of
     body length — flowed CTAs go ragged the moment copy lengths differ.
     v4: align-items:start lets one card open without stretching its siblings — each
     card expands alone (the toggle also syncs aria-expanded).
```

### `cards-v3.html`

```text
 Variant 3 · IMAGE-TOP CARDS — 3 cards with photo/image above + title + body (case studies,
     partner showcases, reward types). Defaults use §9.2a pack photos via data-motif
     (list photo-chess/photo-gears/photo-dancers in spec.illustrations); swap for
     base64 screenshots or .duo-treated brief photos when the content supplies them.
     Cards do NOT expand (no .card-cta / .card-detail) — they are static display cards.
```

### `cards-v4.html`

```text
 V4 · R12 TILE GRID 3×2 — 560×319 flat tiles mixing .cell / .cell--nav stat /
     .cell--tint stat / one .motif--panel crop (registry R12, layouts 69/70/73/74).
     The motif tile needs its name in spec.illustrations (e.g. "coral").
```

## charts

```text
  charts.html — R2 stat mosaic bento · flat bars · .datatable (§12.12, §12.15)
  v3 RULE: variant 1 is a FULL-CANVAS composition — pasting it unmodified passes §12.15a.
  Numbers become a CHART ARCHETYPE — never prose bullets, never a raw <table>.
  Check stats.html FIRST: the brand prefers circles; bars only for genuinely linear/ranked
  comparisons. Bar fills: flat Navy with ONE Orange 700 highlight — or a single-hue orange
  ramp (800→700→600) for ordered stages. Never mix both. .canvas-grid cells need explicit
  inline grid-column/grid-row spans.
```

### `charts-v1.html`

```text
 V1 · R2 STAT MOSAIC BENTO (5 cells fill the whole band; one navy hero)
```

### `charts-v2.html`

```text
 V2 · COMPACT — horizontal bars from plain divs (widths ∝ value on one shared scale).
     Direction-meaningful figures take .stat--pos / .stat--neg (§10.1) — meaning, not sign.
```

### `charts-v3.html`

```text
 V3 · COMPACT — .datatable (<=5 cols, <=6 rows; larger data goes to an appendix)
```

## columns

```text
  columns.html — column archetype (.cols + .cols-2 / .cols-3 / .cols-4)
  WHEN
    2-4 parallel ideas of equal weight: pillars, principles, offers, benefits.
  v3 RULE: variant 1 is a FULL-CANVAS composition (spacious grid + dot field + takeaway) —
  pasting it unmodified passes §12.15a. Bare column strips are the rejected v2 look.
  VARIANTS
    1. .cols-3 .cols--spacious + field-right lift + .takeaway — the workhorse, composed.
    2. .cols-4 .cols--compact with .col-dot dot headers — denser; pair with a lift.
    3. .cols-2 with a .pill row underneath — two ideas plus a tag row.
  RULES
    - Optional orange eyebrow under the headline: <div class="subtitle">FEW CAPS WORDS</div>
      (locked at y=132 — see variant 1). Never restyle it.
    - Text Navy on Cream only; 2-4 short lines per column. The grid sits at y=260 —
      don't stack anything above it except headline/subtitle.
    - Markup only: no <style>, no new classes. Inline style only for per-instance
      sizing/positioning (the pill row in variant 3).
    - Keep the .slide wrapper, .headline, .footer-brand and the EMPTY .pageno
      (runtime-filled). Swap data-slide-id="cX-sY" for the shell placeholder's real id,
      and keep the placeholder's .confidential line if the deck has one.
```

### `columns-v1.html`

```text
 Variant 1 — three spacious columns + dot field + takeaway (full canvas)
```

### `columns-v2.html`

```text
 Variant 2 — four compact columns, dot headers (pair with a lift on sparse decks)
```

### `columns-v3.html`

```text
 Variant 3 — two columns + pill row (tags, markets, workstreams…)
```

### `columns-v4.html`

```text
 Variant 4 · ICON-LED TRIO (v3.3) — suite icons head the columns when the point
     is a verb/capability (§8.1). Paste each SVG inline from design-system/icons/<family>.md; at most
     one .icon--orange moment per slide. Pairs well with a .duo half or a lift.
```

### `columns-v5.html`

```text
 Variant 5 · NUMBERED STEPS — 3-4 columns headed by a giant step number (.hero-num--s)
     + label + body. For visual agendas, phased approaches, or sequential flows where the
     number IS the focal anchor. Like the pptx "strategy briefing" agenda (slide 5).
```

## comparison

```text
  comparison.html — comparative archetype (.compare-art + .compare-left / .compare-right)
  WHEN
    Two states or options framed around ONE centrepiece motif: before/after,
    today/tomorrow, us/them. The art carries the middle; text stays at the edges.
  v3 RULE: variant 1 is a FULL-CANVAS composition — motif centrepiece + edge text zones
  + takeaway closer. For a 50/50 colour-block face-off see splits.html V3.
  CENTREPIECE
    .compare-art is a fixed 964px-wide, dead-centre host. Give it data-motif="rocks"
    (or "ribbon-orange") with the motif listed in spec.illustrations — the shell clones
    the art from its <template data-asset> at load. Never paste base64 into the slide.
    Rocks (two masses) and Ribbon (one flowing form) are the natural comparison motifs.
  RULES
    - Pills act as the two state labels; text zones are 420px wide at y=420 —
      roughly 4 short lines each. Use plain <p> inside them (the zone sets 24px/1.35).
    - Text Navy on Cream only; nothing else in the middle of the slide.
    - Keep the .slide wrapper, .headline, .footer-brand and the EMPTY .pageno.
      Swap data-slide-id="cX-sY" for the shell placeholder's real id, and keep the
      placeholder's .confidential line if the deck has one.
```

### `comparison-v1.html`

No notes of its own.

### `comparison-v2.html`

```text
 V2 · VENN DIAGRAM — 2-3 overlapping circles with labels inside and at the intersection.
     Use for converging disciplines, overlapping audiences, or shared-value propositions.
     Max 3 sets; the intersection label carries the slide's key insight.
     Uses .venn, .venn-set, .venn-label (v3.4 CSS). No motif — the diagram IS the composition.
```

## image-content

```text
  image-content.html — image + text layouts (.img-right-text / .img-right-media /
  .img-half-media) and the .screenshot treatment
  WHEN
    A photo, illustration or product screenshot needs to share the slide with copy —
    or a chapter needs its R11 motif poster moment.
  v3 RULE: variant 1 is a FULL-CANVAS composition (the R11 poster).
  VARIANTS
    0. R11 MOTIF POSTER — full-bleed halftone + 108px ALL-CAPS Thin title. The shipped
       motifs keep their upper-left zone sparse, so the title stays legible there.
    1. .img-right-text + .img-right-media — text 640px left; media bleeds to the RIGHT
       CANVAS EDGE (x880→1920, y 240-940) per §15.9 — the outer margin opens for the
       image, the inner edge holds the grid. The media <img> is object-fit:cover.
    2. .img-half-media — media bleeds to the top/right/bottom EDGES (960px wide).
       The headline runs under it unless you clamp it: keep it short or add an inline
       max-width (see example). The footer/pageno sit ON the image bottom-right —
       only use imagery that stays light/quiet in that corner, else use variant 1.
    3. .screenshot — for user-supplied product screenshots ONLY:
       base64-inline it, downscale to ≤1920px wide first, keep the navy keyline the
       class draws, and NEVER full-bleed a screenshot (it must sit inside margins).
    4. DUOTONE HERO (v3.3, §9.2) — half photo, half argument; counts as a dark
       moment. Default photo comes from the §9.2a pack (pre-duotoned, via
       data-motif). A brief-supplied colour PHOTO (never UI) goes inside .duo
       instead and duotones at runtime.
    5. DOT HERO (v4, §9.1c) — brand dot art right, .subhead lead-in + body left.
  RULES
    - All imagery is base64-inlined data-URIs — never external file paths (§2a).
    - Until the real image is pasted, keep the flat navy stand-in div — never a grey
      box, stock photo or icon.
    - Keep the .slide wrapper, .headline, .footer-brand and the EMPTY .pageno.
      Swap data-slide-id="cX-sY" for the shell placeholder's real id, and keep the
      placeholder's .confidential line if the deck has one.
```

### `image-content-v0.html`

```text
 Variant 0 · R11 MOTIF POSTER (full-bleed halftone, chapter-poster moment)
```

### `image-content-v1.html`

```text
 Variant 1 — text left, media right. v4 §15.9: .img-right-media bleeds to the right
     canvas edge (x880→1920) — floating mid-canvas rectangles now FAIL verification.
```

### `image-content-v2.html`

```text
 Variant 2 — full-bleed-right media (edges top/right/bottom); clamp the headline
```

### `image-content-v3.html`

```text
 Variant 3 — user screenshot with the sanctioned .screenshot treatment
```

### `image-content-v4.html`

```text
 Variant 4 · DUOTONE HERO SPLIT (v3.3) — the proven composition: photo one half,
     statement or content the other. DEFAULT: a §9.2a pack photo via the motif
     mechanism (already navy-duotone — list e.g. "photo-diver" in spec.illustrations;
     alternatives: photo-fjord, photo-ridge). BRIEF-SUPPLIED colour photo instead?
     Swap the motif div for `.duo` + a base64 <img> with a short descriptive alt —
     the .duo treatment duotones it at runtime. Never leave an unfilled stub.
```

### `image-content-v5.html`

```text
 V5 · DOT HERO (v4, §9.1c) — the 'pixelated' website look: navy square-grid dot art
     right, copy left. Brief-supplied images convert to brand dot art with
     `python3 scripts/halftone.py photo.jpg --fg navy --bg none` (§9.1c); ONE conversion
     colourway per deck (dot-dancers-orange is the orange sibling). List the motif key
     in spec.illustrations. Text stays left of x=1200.
```

## logo-wall

```text
  logo-wall.html — partner / technology / capability logo grids
  WHEN
    Showcasing partnerships, technology stack, certifications, or award logos.
    "We work with", "Our partners", "Technology ecosystem", "Awards".
  CSS DEPS
    .logo-row (new v3.4), .col-sub, .hero-num, .content-band, .headline, .body, .takeaway
  VARIANTS
    1. CATEGORISED GRID — rows grouped by category label (left) + logos (right),
       separated by horizontal rules. Like the pptx partner grid (slide 36).
    2. HERO COUNT MOSAIC — giant number left ("1300+"), supporting line, full-height
       logo grid right. Like the pptx awards wall (slide 37).
  RULES
    - Tiles default to TYPOGRAPHIC WORDMARKS (WPP Sans Medium, navy on white) —
      swap the real names in and the wall reads designed even with zero logo files.
      When the brief supplies logos, paste inline <svg> or <img src="data:..."> (base64)
      into the tile in place of the span. Never external URLs, never third-party
      logos pulled from the web.
    - Max 6 logos per row, max 5 rows (30 logos total).
    - Navy on Cream only. Logos keep their original colours.
    - Logo tiles are sized for presence (>=180x72) — a wall of stamps reads as
      dead canvas; fewer, larger tiles beat many small ones.
    - Keep .slide wrapper, .headline, .footer-brand, EMPTY .pageno.
```

### `logo-wall-v1.html`

```text
 V1 · CATEGORISED GRID — rows with category labels + partner logos
```

### `logo-wall-v2.html`

```text
 V2 · HERO COUNT MOSAIC — giant number + full-height logo grid (awards / certifications)
```

## orbit

```text
  orbit.html — hub-and-spoke / concentric / radial diagrams
  WHEN
    A central concept radiates outward: capabilities around a core platform,
    data types feeding an engine, services orbiting a hub.
  CSS DEPS
    .orbit (dotted circle), .orbit-hub, .orbit-node (new v3.4),
    .stat-circle, .pill, .headline, .col-sub, .body, .lift
  VARIANTS
    1. HUB CLASSIC — 3 concentric dotted rings + 4 labelled nodes on the middle ring.
       Headline left of centre; ideal for "X is the connecting tissue" strategy slides.
    2. RADIAL SPOKES — large centre circle + 6 labelled spokes radiating outward.
       Ideal for data ecosystems, capability wheels, or "what we bring" inventories.
    3. FLOATING BUBBLES — 3-4 overlapping circles with text inside each.
       Ideal for value propositions, strategic pillars, or "we design / build / operate".
  RULES
    - Navy on Cream. ONE filled anchor per slide (the navy hub, or one Orange 500
      tint circle); every other circle stays an outline or dotted stroke. A soft
      --bg-alt disc behind the hub is sanctioned tone-on-tone counterweight.
    - 4 orbit nodes max per ring; 8 spokes max in radial mode.
    - Text inside circles: keep <=3 short lines; use .col-sub + .body.
    - Markup only: no <style>, no new classes. Inline style for per-instance positions.
    - Keep .slide wrapper, .headline, .footer-brand, EMPTY .pageno.
```

### `orbit-v1.html`

```text
 V1 · HUB CLASSIC — 3 rings, 4 labelled nodes, headline left (full canvas)
     §15.3 ALIGNMENT LAWS: the ring group is centred on the slide midline (hub centre
     x=960) unless a left context column justifies an offset. Every node anchors by its
     CENTRE (inline translate(-50%,-50%)) at an exact clock position on the middle ring —
     never by its top-left corner, which skews each label by half its own width.
```

### `orbit-v2.html`

```text
 V2 · RADIAL SPOKES — context column left, ring right: filled navy hub + 6 pill nodes
```

### `orbit-v3.html`

```text
 V3 · FLOATING BUBBLES — 3-4 overlapping text circles (value props / strategic pillars)
```

## process-timeline

```text
  process-timeline.html — proc cards · R7 milestone ruler · R6 gantt · compact timeline (§12.11, §12.15)
  v3 RULE: variant 1 is a FULL-CANVAS composition — pasting it unmodified passes §12.15a.
  .proc for HOW (numbered steps, no dates) · R7/timeline for WHEN · R6 for WHO-WHEN (workstreams).
  Timeline maths: nodes are 16px → centre with left:calc(P% - 8px); labels take bare left:P%
  (the class self-centres). Keep nodes within ~5-95%. Never add a content-band lead above .proc.
```

### `process-timeline-v1.html`

```text
 V1 · PROCESS CARDS + TAKEAWAY (5 numbered white cards). §15.4: cards hug their
     content (.proc--cards is 260→700) and the takeaway anchors the freed bottom band —
     never ship a card whose bottom half is blank white.
```

### `process-timeline-v2.html`

```text
 V2 · R7 MILESTONE RULER (stems above AND below fill the canvas vertically).
     Hairline composition: stems/dots/labels are pixel-light, so the tripwire cannot see it —
     the declaration below downgrades it to a surfaced WARN and the art pass confirms BY EYE.
     §15.3 LANE LAWS (the audit's most-repeated timeline defects — respect all four):
     - TWO lanes only: every above-axis milestone starts at the SAME top (240), every
       below-axis one at the SAME top (744). Stem length absorbs copy-length differences —
       never nudge a milestone block vertically to fit its text.
     - Stems keep ≥24px clearance from the text block they leave (above-axis: stem top =
       lane text bottom + 24; below-axis: stem runs axis → lane top − 24).
     - Axis labels never touch a stem: keep every label's left edge ≥24px from any stem x.
     - One milestone width per slide (280px here, inline) so line-wrap depth matches.
```

### `process-timeline-v3.html`

```text
 V3 · R6 GANTT SWIMLANES (flat 6px bars in the orange ramp, two segments per lane,
     bottom event flags). Hairline composition — declared, and confirmed by eye in the art pass.
```

### `process-timeline-v4.html`

```text
 V4 · COMPACT — classic node timeline (pair with a field lift so the canvas stays alive)
```

### `process-timeline-v5.html`

```text
 V5 · ECOSYSTEM MAP — nodes distributed across zones with connecting lines.
     For capability maps, technology ecosystems, or operating model diagrams.
     Uses .orbit (dotted circle), .stat-circle for centre, positioned text/pills for nodes,
     and border-based connecting lines. Like the pptx ecosystem slides (13, 63-64).
```

### `process-timeline-v6.html`

```text
 V6 · R8 PHASE BOARD — centre tint panel as the board, step headers on a top rule
     (14px dots + STEP CAPS + pill time chips), 4 body columns, full-width KPI band at
     the bottom split by rules (registry R8, slide 117). No motif needed.
```

## splits

```text
  SPLIT PANELS — R1 split rail dashboard · R13 colour-block 40/60 · 50/50 motif panel (§12.15).
  v3 rule: variant 1 is a FULL-CANVAS composition; pasting it unmodified must pass §12.15a.
  Rules: with a right panel >=768px the headline needs inline max-width:1040px (>=440px: 1240px).
  Footer contrast flips automatically under a right navy panel. Panels paint at z-index 0 and are
  emitted BEFORE the furniture. Motifs are never inlined — use data-motif (cloned from the shell's
  <template data-asset>, listed in spec.illustrations). Do not use .panel--left in these variants:
  the headline sits at x=80 and would collide; left panels need a bespoke headline treatment.
```

### `splits-v1.html`

```text
 V1 · R1 SPLIT RAIL DASHBOARD (full canvas): lead + low KPI row, tint rail with 4 stats
```

### `splits-v2.html`

```text
 V2 · R13 COLOUR-BLOCK 40% (right navy panel carries the display numeral)
     §15.4 FIT LAW: the panel-inner is 656px wide (768 − 2×56 padding). Display numerals
     must FIT it: at 240px Thin, ~4 glyphs max (incl. sign/%). "+35%" at 280px (--l)
     already overflows the panel and collides with the label below — size DOWN, never
     let a numeral cross the panel edge or its own caption.
```

### `splits-v3.html`

```text
 V3 · 50/50 MOTIF PANEL (navy panel filled by a halftone crop; statement-led / high-impact)
```

### `splits-v4.html`

```text
 V4 · IMAGE BLEED + SIDEBAR — full-bleed photo left (50%), structured text right.
     For case studies, location spotlights, product showcases. DEFAULT: a §9.2a pack
     scene via data-motif (list "photo-fjord" in spec.illustrations; alternatives:
     photo-diver, photo-ridge). Brief-supplied colour photo? Swap the motif div for
     .duo + base64 <img>. Like the pptx "INTERIOR 50/50 Image Bleed Left" layout.
```

## statement-quote

```text
  statement-quote.html — R10 motif-side statement · big quote · poster (§12.4, §12.5, §12.15)
  v3 RULE: variant 1 is a full composition — the statement's air is SHAPED by an art
  counterweight (accent field or motif), never leftover. Statement/quote slides are the
  only sanctioned "intentional air" slides, and only when the air is asymmetric like these.
  .big-statement: ~6 words / 2 lines max. .big-quote: CURLY quotes (“ ”) in the copy,
  attribution in Medium CAPS. Use at most one or two statements per deck outside high-impact.
  §15.2(6) — ONE art layer per zone: V1's accent field and V1b's motif are ALTERNATIVES.
  Never stack a dot field and a motif/texture in the same region — the later layer paints
  over the circles and reads as a rendering error.
  v4: data-dots="field-micro" / "field-mid" are sanctioned alternatives to "field-accent"
  for the statement counterweight — one hue per field (§5).
```

### `statement-quote-v1.html`

```text
 V1 · R10 MOTIF-SIDE STATEMENT (accent dot field as the counterweight)
```

### `statement-quote-v2b.html`

```text
 V1b · R10 with a halftone motif (list the motif in spec.illustrations; text stays left of x=1200)
```

### `statement-quote-v2.html`

```text
 V2 · BIG QUOTE
```

### `statement-quote-v3.html`

```text
 V3 · POSTER STATEMENT — high-impact direction ONLY (navy moment, ghost numeral low-right,
     cream corner dots as counterweight; diagonal tension fills the canvas)
     §15 LAWS for this recipe:
     - Poster statement is ≤3 words / ≤2 lines at 220px. A full sentence at poster scale
       overflows the canvas top (translateY(-50%) centring) — longer copy drops to the
       default 150px .big-statement instead.
     - THE CHARACTER LIMIT IS NOT THE BINDING CONSTRAINT HERE. capacity.json allows 50
       chars for this slot and cannot count words, so it green-lights copy this recipe
       forbids: "Loyalty is an enterprise decision." is 33 chars and passes the capacity
       gate, but it is 5 words and sets FOUR lines, which grows down into the cream
       corner dot — white type on a cream fill measures 1.05:1, i.e. invisible, and no
       gate reports it because .dot is decor-exempt from the overlap laws. Count the
       WORDS before trusting the char count.
     - The .num-ghost NEVER intersects the statement's text box: keep the ghost's left
       edge right of the statement's max-width, or below its last line. Ghost tones are
       flat sanctioned colours — differentiate from the statement by POSITION, not opacity.
     - The corner dot stays clear of the footer furniture zone: on confidential decks the
       bottom-left line sits at (80,1048) — dots in that corner must end above y≈1000.
```

## stats

```text
  stats.html — R3 hero numeral quartet + ruler · R4 hub & spokes · √-scaled bubbles (§12.12, §12.15)
  v3 RULE: variant 1 is a FULL-CANVAS composition — pasting it unmodified passes §12.15a.
  WHEN: any slide whose payload is numbers. Circles come FIRST in the brand doctrine —
  reach for bars (charts.html) only when circles genuinely can't carry it.
  SIZING RULE (non-negotiable): circle AREA ∝ value, so DIAMETER ∝ √value.
    100 vs 25 → Ø400 vs Ø200 (never 400 vs 100). Below: 64/36/16 → k=55 → Ø440/330/220.
    Circles under Ø340 need inline font downscales (68/15 at Ø330, 46/15 at Ø220 —
    15px is the v4 floor for ANY informational text).
  For the split-rail stat dashboard see splits.html V1. Motifs: data-motif placeholders only
  (list the motif in spec.illustrations; the shell clones it from its <template> at load).
```

### `stats-v1.html`

```text
 V1 · R3 HERO NUMERAL QUARTET + TICK RULER (display top, ruler anchors the bottom)
```

```text
 intentional-air: sanctioned by §12.15a for exactly this silhouette (display
     quartet over a hairline ruler reads as air to the tripwire, not to the eye).
     §15.6: the ruler IS the composition's bottom anchor — dropping it without an
     equivalent bottom element (takeaway at the standard y877 band) leaves a ~340px
     dead band and fails the balance law. If the stats aren't time-based, swap the
     ruler for the takeaway; never ship the quartet alone. The 1fr grid tracks (§15.3)
     keep the four columns and their divider vrules on one pitch: place vrules at
     track boundaries minus half the gap.
```

### `stats-v2.html`

```text
 V2 · R4 HUB & SPOKES (motif backdrop behind the hero stat, flanking proof columns)
```

### `stats-v3.html`

```text
 V3 · √-SCALED BUBBLE ROW (area ∝ value) + bottom dot field. NEVER one dominant centred circle.
```

### `stats-v4.html`

```text
 V4 · COMPACT — .kpi-row value/label pairs when the numbers don't need weighting.
     Anchor it LOW (.kpi-row--low) or pair it with a lead line + field; never leave it
     floating alone mid-canvas (that is the rejected v2 look).
```

### `stats-v5.html`

```text
 V5 · SCORECARD GRID — KPIs grouped by category in a 2×3 or 3×2 bento. Each cell has
     a category header, hero number, label, and optional trend. For performance dashboards,
     quarterly reviews, or multi-dimensional measurement frameworks.
```

### `stats-v6.html`

```text
 V6 · R5 CLUSTER DIAGRAM + INDEX ROW — two overlapping navy sets (knockout labels,
     white lists), outline satellites, 1px orange connectors, and a 6-item index rail
     at the bottom (registry R5, slide 102 — 100% active canvas). No motif needed.
```

### `stats-v7.html`

```text
 V7 · INTENSITY RAMP + LEADER LINES (v4, playbook p.46) — four flat circles step up
     in size along a diagonal AND through the warm ramp #FFF5CD → #F9BD5D → #FF7800 →
     #D94E0E. Colour here encodes INTENSITY/SEQUENCE, never good/bad (§10). Area-true:
     diameter ∝ √value (9/16/36/64 → k=45 → Ø135/180/270/360). Each circle takes a thin
     1px navy leader line to an external callout on the cream — Thin numeral 90px+ with
     the % as a superscript span, Medium CAPS 18px label beneath. The dotted-hairline
     guide circles are optional counterweight (border:1px dotted navy, no fill).
     Keep everything inside x 80-1840; no text below y 985.
```

## team

```text
  team.html — people grid (.team-grid / .team-grid--3 with .person cards)
  WHEN
    Introducing 3-8 people: team slide, speakers, points of contact.
  v3 RULE: variant 1 is the FULL-CANVAS wide grid (260px portraits + bios fill the band).
  VARIANTS
    1. .team-grid.team-grid--wide — three across, 260px portraits, full-height bios.
    2. .team-grid — four across, 180px portraits (compact; pair with a lift).
  RULES
    - .ph is a 180px navy CIRCLE photo holder. Photos go INSIDE it as base64-inlined
      <img> (object-fit:cover crops to the circle automatically; delete the .ph-init).
      No photo? The default .ph-init initials monogram (WPP Thin, cream) stays —
      never a grey placeholder, a stock face, or an icon. Match initials to the name.
    - .nm name (Medium 24), .rl role (Light 20), .bio 1-3 short lines (16px).
      Keep bios parallel in length so the row reads level.
    - Text Navy on Cream; the circles are the only dark fills on the slide.
    - Keep the .slide wrapper, .headline, .footer-brand and the EMPTY .pageno.
      Swap data-slide-id="cX-sY" for the shell placeholder's real id, and keep the
      placeholder's .confidential line if the deck has one.
```

### `team-v1.html`

```text
 Variant 1 — three across, wide portraits, full-height bios
```

### `team-v2.html`

```text
 Variant 2 — four across (compact)
```
