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
- **Title + subheader + meta, top-left:** deck **title** at (40, 88) in WPP Light 81 px Navy, ALL CAPS — kept **short (2–4 words)**; directly beneath it a **longer subheader** in WPP Light 31 px Navy (one plain-sentence line, max-width 900 px, line-height 1.16); then the **month/year** in WPP Regular 24 px ALL CAPS **Orange 700** and the **presenter name** in WPP Regular 24 px Navy (omitted cleanly when `presenter` is `""`).
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

- Background: flat **WPP Cream**. "Agenda" headline top-left in WPP Light 54 px Navy at (40, 112).
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

- Section number `05.` top-left at (40, 56): WPP Thin **104 px**.
- Section title bottom-left, pinned LOW (bottom inset 96): WPP Thin **136 px** ALL CAPS, line-height 0.88, max-width 1560 px, `text-wrap:balance`. The title may overlap the circles (display type over flat dots is playbook-sanctioned); locked dividers are exempt from the §15.1 footer-band law, but the brand line/pageno must stay legible (§15.1 contrast sampling still applies).
- Sub-label ABOVE the title, in the same bottom-left block (`.dv-block`, x 40), 26 px above it: WPP Medium 22 px ALL CAPS, +0.14em — **Orange 800** (Orange 600 on `navy-full`).
- **The scatter:** 5–7 macro/mid circles in the deck's ONE divider hue (via `dividerColourway`, §11) scattered across the top and right of the canvas — at least two bleeding off different edges, exactly one fused pair, none entering the title's clear zone (left/bottom quadrant) and none making the footer illegible. Drawn by the `divider-playbook` `data-dots` preset — geometry verbatim, never hand-edited.
- **Identical on every section** — same composition, same geometry; only the numeral, title and sub-label change.
- Footer brand line + page number as §7.3, contrast auto-handled per colourway.

**The classic v3 geometry survives as `dividerStyle:"classic"`** (registered variant, not a deviation): number top-left, title at bottom inset 214 at 104 px, sub-label below it (x 84, bottom inset 150), the four right-anchored macro dots (Ø 760/560/180/90). Same colourway system either way.

### 12.4 Big Statement
- One sentence, WPP Thin **150 px default** (81–180 range for shorter/longer statements), Navy, left-aligned at x = 40 and vertically centred, line-height 0.82, max-width 1640 px, on an otherwise empty cream canvas.
- Variants: with supporting paragraph (24–26 px Light below), with halftone motif side, with a lift dot cluster, vertical composition.
- Assemble from the `statement-quote-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.5 Big Quote
- Quote in WPP Thin 120 px with typographic quotation marks at (120, 170), max-width 1620 px, line-height 1.04, max ~4 lines.
- Attribution in Medium ALL CAPS 30 px at left 120 / bottom 190.
- Assemble from the `statement-quote-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.6 Title + Content (1/2/3/4 columns)
- Furniture per §7. Column grid starts at (40, 260), right inset 80; gaps 80 px (56 px for 4-col); widths per §2 (860 / ≈547 / 408).
- Each column: optional **Medium ALL-CAPS subheader** (24 px) or a 16 px dot bullet, then Light body (24 px; 22 px in 4-col).
- **4-col with Dot Header**: each column headed by a dotted icon (§8.1 fallback) + subheader.
- **4-col with Pills**: navy pill labels (§5) beneath columns.
- Assemble from the `columns-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.7 Text boxes ×3–×8 (with Dots or Arrows)
- Title as usual; a row of equal flat White boxes starting at (40, 280), gap 28, padding 32 × 36, body 22 px (or two rows of 3/4 for ×6/×8).
- Between boxes: a **16 px navy dot** (relationship) or the **navy triangle arrow** (sequence/flow) vertically centred in the gutter.
- Assemble from the `boxes-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.8 Comparative (rocks / ribbon)
- Two-sided comparison: a shipped accent motif (rocks or ribbon, §9.1a — pick the colourway that matches the deck's family: `rocks`/`ribbon-navy` for navy decks, `rocks-orange`/`ribbon-orange` for orange) centred at 964 px wide; 420 px label columns left and right at top 420, 24 px Light.
- **Family exemption:** the `.compare-art` centrepiece is furniture of this archetype — it does NOT count against the deck's one-motif-family rule (SKILL.md). Prefer the colourway variant closest to the deck's family.
- Assemble from the `comparison-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.9 Image layouts — v4: media anchors to edges (the anchoring law, §15.9)

**A rectangular media block never floats in the middle of the canvas.** A photo/motif crop that ends in naked rectangular cuts on all four sides, surrounded by margin, reads as a placed thumbnail, not a composition. Every media block ≥ ~200 × 200 px does ONE of:

1. **Bleeds to at least one canvas edge** (`.media--bleed-r/-l/-b/-t` or the half/panel layouts) — the sanctioned exception to the 40 px margin: edge-bled media runs to x = 0 / 1920, y = 0 / 1080.
2. **Sits in a canvas corner** (two of its sides ON the edges — `.media--corner-br` etc.).
3. **Is declared inset** (`data-inset-ok`) — reserved for `.screenshot` (whose keyline frame IS the treatment and which must never bleed) and for grid-mosaic tiles whose gutters are the composition.

The layouts:

- **Title + Content with Image (v4)**: text column left (640 px at (40, 260)), media right **bled to the right edge** (from x 880 to 1920, top 240 to bottom 140, `object-fit:cover`) — the outer margin opens for the image, the inner edge holds the grid.
- **Half Image**: image fills the right 960 px, full height (edges top/right/bottom).
- **Image with Title**: full-bleed halftone/photo + big ALL-CAPS Thin title.
- **Dot hero (v4)**: a `halftone.py` conversion as the art half of a split — the "pixelated" website look (§9.1c).
- **Screenshots**: 1 px Navy outline (`.screenshot`), never a drop shadow, never full-bleed — the one sanctioned inset (`data-inset-ok` is implied by the class).
- Assemble from the `image-content-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.10 Team slides
- Grid of 3 or 4 per row at (40, 280), right inset 80, gap 64: circular portrait (Ø 180 px, navy placeholder) + `Firstname Lastname` (Medium 24), role/department/city (Light 20), short bio (Light 16).
- Assemble from the `team-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.11 Process (×5) & Timelines
- **Process boxes ×5**: five numbered columns at (40, 300), gap 40 — Thin **Orange 700** numeral (64 px), Medium ALL-CAPS step label (16 px), Light body (20 px).
- **Timeline**: a 1 px navy axis at y = 540, 16 px dot nodes (Orange 700 for accents), Medium ALL-CAPS 16 px labels below.
- **Roadmap / horizontal steps**: `START → …` with stat blocks; phases labelled `PHASE 1…` with dot markers on the thin line.
- Assemble from the `process-timeline-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.12 Data-viz slides
- **Bubble pipeline**: big Thin ALL-CAPS title left, composition of flat circles right (§10) — `.stat-circle` (Navy fill, White Thin 90 px value, Medium 18 px label; `--orange` variant flips to Orange 700 / Navy).
- **Impact stats**: diagonal chain of circles + external stat callouts with thin connector lines + short narrative paragraph right.
- **Dashboard**: KPI row (Thin 110 px values) + description + percentage circles.
- **Charts**: bar/line charts flat navy/orange, Light labels; headline + eyebrow furniture unchanged.
- **Data honesty (hard rule): bubble/circle AREA is proportional to value — diameter ∝ √value.** Diameter-proportional bubbles exaggerate ratios quadratically and are a distortion; they are **banned**. When two circles represent 4× the value, the bigger one is 2× the diameter, never 4×.
- Assemble from the `stats-v*` and `charts-v*` variants in `assets/snippets/variants/` — don't re-derive.

### 12.13 Outro / Thank-you — the locked, mandatory close

**Every deck ends with the locked Thank-you slide — no exceptions.** It is always the last slide, whatever the deck is about.

- **Light (default):** flat WPP Cream, `Thank you.` in WPP Light 99 px Navy, left-aligned at (40, 430); Orange dot composition anchored bottom-right, bleeding off-canvas — a large Orange 700 dot (Ø 760, bottom-right), an Orange 600 dot (Ø 300, top-right) and a small Orange 800 accent (Ø 150).
- **Dark (`outro:"dark"`, sanctioned for statement-led decks):** Navy field, White text, the same geometry with Cream/White macro dots + an Orange 700 accent; footer contrast auto-handled (§11).
- Footer brand line + page number as §7.3.
- **Optional contact block** (via the `contact` spec key): name / role / email at (40, 580), 24 px Light. Otherwise the clean word-only close.
- Localized automatically: `lang:"es"` renders `Gracias.` (or override via `strings`).

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
