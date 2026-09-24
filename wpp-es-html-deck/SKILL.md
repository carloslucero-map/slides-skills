---
name: wpp-es-html-deck
description: >-
  Turn any raw input — narrative, outline, brief, bullet dump, or an approved
  deck-content-builder Markdown file — into a polished slide deck in the WPP
  Enterprise Solutions | MAP visual language (Navy + Cream + Orange, WPP
  Sans, dot system, 16:9). In Claude Design the deck is built inside the
  Slides artifact, never as a separate file; elsewhere it is one
  self-contained HTML file. Trigger: "build a deck", "turn this into
  slides", "make a presentation", "WPP deck", "MAP deck", "put this in the
  WPP template", "make this on-brand", or pasting notes to be rendered as a
  deck — even if messy, structuring is the job. House standard for WPP ES |
  MAP decks. Do NOT use to edit .pptx files or for the older VML MAP
  espresso/gold style. Two-turn by design: first reply is a slide plan +
  design-direction question (blocking checkpoint); the deck is built only
  after approval or an explicit review waiver.
---

# WPP Enterprise Solutions | MAP — HTML Deck Builder v4

You convert loose text — or an approved `deck-content-builder` content file —
into one on-brand slide deck. The user brings the thinking, you bring the
structure and the brand. Version history is in `CHANGELOG.md`; everything
this file states is current.

## STOP — checkpoint discipline (this rule outranks everything below)

**Your first substantive reply to a new deck request is the G1 plan, never
the deck** (if G0 fires, that intake question comes first — and is also never
the deck). Present the plan artifact (slide table, narrative, cover block,
the design-direction question), then **end your turn and wait**. Do not run
`build_shell.py`, do not write any deck HTML, in that turn. This applies at
every size (a micro-deck or single slide still gets a short plan and the
direction question), in every language (run the gates in the user's
language), and separately to EACH new deck in a conversation.

Only three inputs waive the full gate:
1. **An explicit review waiver in the user's own message** — "just build it,
   no questions", "skip the plan", "don't ask me", or equivalent words that
   waive *review*. A deck request, however imperative ("build a deck", "arma
   un deck", "renderiza esto", "ASAP"), is the normal trigger, NOT a waiver.
   → Build with defaults, list your assumptions at delivery, ask nothing.
2. **An approved `deck-content-builder` Markdown file** — approved means the
   user says so, or it passed that skill's gate in this conversation; a
   contract-shaped file alone is just input (full G1 applies). → One-line
   notice + the design-direction question, then **end your turn** and wait
   for that one answer.
3. **A user-supplied complete `spec.json`** — it encodes every registered
   choice, so it IS the approved plan; build from it. If it omits
   direction / cover / colourway, ask the direction question first.

Building in the same turn as receiving content that has not been
plan-approved — raw or polished — is this skill's #1 failure mode: it
silently produces the all-defaults deck (the old v1 look), asks the user
nothing, and offers no variants. About to generate with no approved plan for
THIS deck? Stop and present G1 instead.

## Where the deck goes — decide once, before building

The gates above hold on every surface. What differs is the deliverable, and
getting it wrong puts the deck in a separate file the user cannot present
from.

- **Claude Design, or any session whose Artifact tool offers a Slides type**
  (a deck is open, or `quickstart` with intent `slides` returns one): **the
  deck is an Artifact made from that type.** Read
  **`references/CLAUDE-DESIGN.md`** and follow it for steps 3–6. Never write
  a standalone `.html` file, never run `build_shell.py`, `check_capacity.py`
  or `verify_deck.py`, never screenshot. The artifact exports HTML, PDF and
  PPTX itself, so a request for "an HTML file" there means its export.
- **Everywhere else** (Claude Code, a chat with no Slides type): **one
  self-contained `.html` file**, built by steps 3–6 below.

## Step 0 — read the brand system first (once per deck)

Before building, read **`references/CORE.md`** — everything needed to lay out
ANY slide (canvas, colour, typography, dots, logo, furniture, rhythm, HTML
conventions, and the §15 layout laws the verifier enforces). It is a verbatim
subset of the master guideline, so its numbers ARE the enforced numbers.
Don't build from memory — open it.

**Then open a `references/sections/` file only when its trigger fires:**

| Open | Only when |
|---|---|
| `sections/8-iconography.md` | the slide uses icons |
| `sections/9-illustration-photography.md` | the slide uses a photo, motif, duotone or halftone |
| `sections/10-data-visualisation.md` | the slide carries a chart, stat circles or bubbles |
| `sections/12-archetypes.md` | you need an archetype's detail and the quick-map plus SNIPPET-INDEX did not settle it. **§12.14 / §12.15 / §12.15a are already in CORE** — the composition guardrails, recipes and the C1-C7 checklist load every deck, because the verifier enforces them every deck |
| `sections/13-4-interaction-patterns-interactive-html-de.md` | the deck needs expandable cards or interaction |
| `sections/14-motion-system-v3-2-the-deck-feels-alive-.md` | motion is full or subtle (skip when off) |
| `sections/14-5-revising-a-delivered-deck.md` | you are revising a delivered deck |

Loading the whole guideline when only CORE is needed costs ~14k tokens per
deck for nothing. **`references/WPP-ES-DESIGN-GUIDELINE.md` remains the master**
— `sections/` is that same file split, CORE.md a subset of it. If anything
disagrees, the generator wins, then the master.

## The non-negotiables (every deck, no exceptions)

1. **One deliverable, in the surface's own form** (see "Where the deck
   goes"). In Claude Design: the Slides artifact, with assets uploaded, never
   inlined. Everywhere else: **one self-contained `.html` file** — every
   asset embedded inline (base64 / inline SVG), never an external path or CDN
   link, so a colleague double-clicks it offline and it renders fully. The
   generator handles this; if you add assets, inline them too (raster ≤300KB
   before base64).
2. **Five locked defaults — never redesigned per deck:** Cream `#FAFAF0`
   content background (never pure White, never alternating); the locked cover
   frame (2–4 word ALL-CAPS title + sentence subheader + month + presenter +
   navy logo badge — the art layer is a registered choice, the frame is not);
   the one locked agenda; one divider composition identical on every section
   (its colourway is a once-per-deck registered choice); the locked Thank-you
   close. Registered choices are sanctioned user decisions, not deviations.
3. **Colour discipline.** Navy `#000050` carries text; Cream + White dominate;
   the Orange ramp is an accent only. Text is Navy or White except the
   sanctioned orange moments enumerated in the guideline (§1.4).
4. **The dot is the primary device** — circles at micro / mid / macro scale,
   anchored to edges, bleeding off-canvas; flat fills; Navy dots never behind
   text. Charts are circle-first; **bubble area ∝ value (diameter ∝ √value)**.
5. **Type is WPP Sans in the v4 playbook roles** — Thin (large display ONLY) /
   Light (titles + headlines; `.headline--caps` for strong emphasis) /
   **Regular (sub-headlines in caps, body copy, footers — the weight step
   below the Light headline IS the hierarchy)** / Medium (labels, and the
   single-token `.hl` title highlight) / Bold (footer brand line only).
   Sentence-case headlines, max two lines. No bold-in-body, no italics except
   sparse quotes, no underlines. **No informational text below 16px; body
   ≥ 20px** (§4.5 — the verifier measures it, and between 16 and 20 only the
   declared fine-print roles are allowed).
6. **No gradients, no shadows, no rounded cards (pills only), no accent bars.**
7. **The name is "WPP Enterprise Solutions | MAP".** Never "VML MAP".
8. **Media anchors to edges (§15.9).** A photo/motif block ≥200×200 bleeds to
   a canvas edge or sits in a corner — never floats inside the margins
   (`.screenshot` and mosaic tiles are the declared-inset exceptions).

## Design directions (the one design question you ask)

**Every direction requires full-canvas composition (§12.15) — the difference
between them is voice, never effort.** A bare text band on cream is a defect
in all four.

| Axis | **1 · Editorial quiet** (default) | **2 · Statement-led** | **3 · Data-forward** | **4 · High-impact** |
|---|---|---|---|---|
| Dark / tint moments | 0 dark; tint panels ok | ≤1-in-6 dark | 0–1, on the hero number | up to 1-in-3, evenly spread; colour-block splits count half |
| Big Statements | ≤1, motif-side (R10) | opens each chapter (R10/R11) | open + close only | poster scale 200–260px; R11 full-bleed per chapter sanctioned |
| Motifs on content slides | ≤2, navy, `--right/--bottom` | statement-adjacent slides | `--backdrop` behind stat hubs | any slide, incl. `--bleed` and `--panel` |
| Dot fields | `field-*` tone-on-tone on non-dense slides; `field-micro` as quiet energy | `field-accent`/`field-micro` on statements, `field-right` elsewhere | `field-bottom` on non-chart slides | any preset incl. `field-navy` (text-safe), `field-mid`, `field-macro` |
| Numbers | inline Thin callouts, R1 halves | one hero stat per chapter (`.hero-num--s`) | R3 quartets, R4 hubs, R2 mosaics; `.hero-num` 240–320px | numerals as art (`.num-ghost`, panel numerals) |
| Density | spacious | mixed | compact-leaning; R6/R7/R8 | mixed + sanctioned collage layering |
| Divider default | `orange` | `navy-dots` | `orange` | `navy-full` (dark outro suggested) |

A gate reply that picks no direction → Editorial quiet. **"You choose" means
pick by content signal** — numbers-heavy input → Data-forward, message- or
manifesto-led → Statement-led, a launch / rallying moment → High-impact, an
exec readout (or any doubt) → Editorial quiet — and name your pick at
delivery. **No further design questions during the build.** If the user
already named a direction or any registered choice in their request, record
it and drop that question from G1
— pre-answering questions never waives the plan half of the gate; only an
explicit review waiver does.

## Gates

**G0 — Intake (conditional, at most once).** Fires only if deck type /
audience / cover meta are missing *and* uninferable. One batched message:
*"Before I draft: (a) audience and the decision they need to make? (b) deck
type — MT / sales / discovery / other? (c) cover meta — presenter + month?
Reply 'defaults' for: internal MT deck, current month, no presenter line."*
Otherwise infer, and print assumptions as the first line of G1 ("Assumed: MT
deck, exec sponsors deciding budget — correct me if wrong"). Never ask serial
questions; never let demo metadata reach a real cover (the generator errors on
it anyway). A reply to G0 — including "defaults" — answers intake only; G1
still follows as its own turn.

**G1 — Plan gate (the single blocking gate).** Present one compact artifact:
- table: *slide # · chapter · action title · archetype · confidence*, with
  **▲ marking titles under 70%**;
- a 3-sentence narrative read-through;
- the cover block (ALL-CAPS short title / subheader / month / presenter)
  **plus the resolved registered set**, so the sanctioned per-deck choices are
  actually on the table: *"Cover: mountain · dividers: orange · outro: light ·
  motion: subtle — say so to swap any of these"* (resolve from the chosen or
  default direction before printing);
- the design-direction question — **show, don't tell: attach or link the four
  exemplar slides** (`assets/exemplars/editorial-quiet.png` ·
  `statement-led.png` · `data-forward.png` · `high-impact.png`) so the user
  picks from pictures, not names: *"The plan is N slides in M chapters. Which
  design direction should I build? 1 Editorial quiet (default) ·
  2 Statement-led · 3 Data-forward · 4 High-impact — exemplars attached.
  Reply 1/2/3/4, adjust the plan, or say 'you choose'."*
- enumerated replies: *"(1) 'build' to render as-is, (2) slide numbers +
  changes ('5: make this a comparison'), (3) 'alt storyline', (4)
  'shorter'/'longer'."*

**Skip G1 when** the input is an already-approved deck-content-builder file —
collapse to a one-line notice ("Using your approved titles verbatim;
chapters: X / Y / Z") **plus the design-direction question**, and wait for
that one answer — or when the user said "just build it" (default direction,
assumptions noted at delivery, no questions at all).

**G2 — Delivery (never blocking).** The file — in Claude Design, the Slides
artifact's link, with no seen-report (`CLAUDE-DESIGN.md`) — + a 2–4-line summary + *which two
slides to eyeball first* (cover badge legibility, the main data-viz slide) +
the revision invitation, always including the variant offer: *"Name any slide
by number to change it — I patch in place; numbering and self-containment are
preserved automatically. I can also render an A/B alternative of any slide
(or an A/B thumbnail sheet of the 2–3 highest-stakes slides) so you can pick."*

## Workflow

### 1. Structure the input into a slide plan

Find the **spine**; group into **1–6 chapters** (3–6 for standard decks; a
single chapter renders as a micro-deck — cover + content + thank-you). One
idea per slide, sentence-case action headline, archetype from the quick-map.
On raw input, action titles meet the deck-content-builder bar: a full
sentence that lands a so-what, ≤15 words, active voice, specific numbers —
never a label ("Background", "Next steps"). Decide the cover.

**Anti-sameness self-review before presenting the plan:** if more than half
the content slides share one archetype, redistribute using the quick-map — an
8+ slide deck should use **at least 4 distinct archetypes, ≥3 §12.15 recipes
and ≥2 density variants**, no two adjacent slides sharing archetype +
treatment (checklist C6), and any run of numbers must land on a stats/chart
recipe, never bullets. A plan that would render as wall-to-wall bullet
columns fails this review.

### 2. Hold the G1 gate — then STOP

Present the G1 artifact and **end your turn**. Do not continue to step 3 in
the same turn unless one of the three waivers in the STOP section applies.

### 3. Write the spec and generate the shell

**In Claude Design, stop here:** steps 3–6 are replaced by
`references/CLAUDE-DESIGN.md`. Everything below builds the standalone file.

```bash
python scripts/build_shell.py --spec spec.json --out deck.html
```

`spec.json` v2 (title/subtitle/month/presenter/chapters required; the
generator validates and errors on demo values, >6 chapters, bad enums):

```json
{
  "title": "AI NATIVE",
  "subtitle": "How WPP Enterprise Solutions | MAP moves to an AI-native way of working",
  "month": "July 2026",
  "presenter": "Alex Humpert",
  "chapters": [
    {"title": "Why this matters", "slides": [
      {"headline": "Approved action title, kept verbatim", "archetype": "cols-3",
       "notes": "…", "source": "…"}
    ]}
  ],
  "direction": "editorial-quiet",
  "dividerColourway": "orange",
  "dividerStyle": "playbook",
  "cover": "mountain",
  "outro": "light",
  "confidential": false,
  "lang": "en",
  "contact": {"name": "…", "role": "…", "email": "…"},
  "illustrations": ["rocks"]
}
```

Registered choices: `cover` mountain · crystal · coral · dots · playbook
(pure-type cream cover, the parent-brand look);
`dividerColourway` orange · orange-600 · orange-500 · white · navy-dots ·
navy-full; `dividerStyle` playbook (default — one-hue macro scatter, title
pinned bottom, §12.3) · classic (the v3 geometry);
`outro` light · dark; `motion` full · subtle · off (defaults:
high-impact / statement-led → full, others → subtle; the shell choreographs
the kit automatically — no markup work, see guideline §14). Flat string chapters (v1 style) still work.
Set `"microDeck": true` when the final deck has ≤4 content slides. For
Spanish decks set `"lang": "es"` (Agenda / Gracias. / Sección N / PRIVADO Y
CONFIDENCIAL are built in; other languages via `"strings"`).

### 4. Fill in the content slides

**Read `canon/CATALOG.md` FIRST, then fall back to the snippet kit.**

`canon/` holds templates traced from the real MAP slide bank: each one measured
off a source slide, rendered against it, and shipped with that original as
`ref.png`. The 51 snippets in `assets/snippets/` were authored from the brand
guideline in the abstract, not from the deck bank — which is the reason decks
built from them have never quite looked like MAP's own slides.

So the order is not a preference, it is a fidelity rule:

1. **`canon/CATALOG.md`** (~950 tokens, loaded once). Choose on the `use when`
   column — it names the problem the template solves. Then open exactly one
   `canon/templates/<id>.html` and paste its `<section>`.
2. **`references/SNIPPET-INDEX.md`** only when no canon template fits. The
   catalogue's last line names the families the canon does not cover yet; for
   those the kit is the answer and there is nothing wrong with saying so.
3. When you fall back, **say which slide fell back and why** in the G2 delivery
   note. That list is what tells the next canon template which slide to trace.

Never open `assets/snippets/*.html` at fill time — those 13 files are the
authoring source (up to 6,326 tokens each); the deck reads `variants/` only.
Edit a canonical file and re-run the full regeneration to rebuild them — `--split` alone does not remeasure:

```bash
python3 scripts/build_shell.py --out build/demo.html
python3 scripts/derive_capacity.py --skill . --demo build/demo.html --write --index --split
```

**`--demo` is not optional.** Without a generated shell the tool reads no CSS metrics at all and falls back to a content edge that stopped being true when the frame moved to 40px — every number it writes is then wrong but plausible. It now refuses to run rather than degrade quietly. Note that `--write` also rewrites `references/capacity.json` wholesale, which drops the canon entries: re-run `authoring/canon-tools/derive_canon_capacity.py --demo <canon-deck> --write` afterwards to merge them back, or `check_capacity.py` reports every canon slide UNCHECKED.

A canon template carries no `<!-- capacity -->` block, but it IS capacity-checked:
`authoring/canon-tools/derive_canon_capacity.py` merges per-slot limits into the same
`references/capacity.json`, so `check_capacity.py` covers canon and kit slides
alike. Its `spec.json` `invariants` say what must not be changed when you fill
it — read those before you touch geometry.

Those maxima are marked `basis: "placeholder"`: they are derived from the copy
the template shipped with, which is evidence of what fits rather than proof of
what the slot holds. Treat a small overage as a question, not a verdict; treat a
large one as a real overflow.

**Check capacity before you write.** Every template carries a
`<!-- capacity: -->` block above its `<section>`: per-slot min–max character
counts and a slide total, derived from the shell's real type sizes and
container widths. Match the
content to a template that fits. `max` is a hard stop, not a target — over it,
pick a lower-density variant or cut copy. **Never shrink type to make copy fit
(§4.5).** `ideal` carries the editorial truth; a geometric `max` of 122 chars
on a `.subtitle` is physically true and editorially wrong.

Replace each placeholder's `.content-band` with a **composition recipe**
(§12.15) — **variant 1 of every snippet file is a full-canvas recipe; start
there, never from a bare text band.** Keep the `.slide` wrapper, headline,
footer brand line and the **empty `.pageno`** (page numbers are computed at
runtime — never hand-number, never renumber). Add/remove slides freely; copy
a divider block for a new section and keep its `data-slide-id` pattern.
Motifs go in as `<div class="motif motif--right" data-motif="coral">`
placeholders (list the motifs in `spec.illustrations`; the shell inlines each
payload once and clones it at load — never paste base64 into slides). Pick
**one motif family per deck** and repeat it — never rotate motifs
(the §12.8 `.compare-art` centrepiece is archetype furniture and is exempt —
pick its colourway variant closest to the deck's family)
slide-to-slide; the divider rule's chosen-once ethos applies to art too.

| Content signal (`**Visual:**` hint) | Archetype | Snippet |
|---|---|---|
| Single key message / transition | Big Statement | `variants/statement-quote-v1.html` |
| A quote | Big Quote | `variants/statement-quote-v2.html` |
| 1–4 parallel points | Columns (2/3/4, dot headers, pills) | `variants/columns-v1.html` |
| Numbered agenda / phased approach | Numbered step columns (giant 01-04 headers) | `variants/columns-v5.html` |
| Steps / sequence | Text boxes with arrows | `variants/boxes-v3.html` |
| Parallel / related items | Text boxes with dots | `variants/boxes-v2.html` |
| This vs that | Comparative (Rocks / Ribbon centrepiece) | `variants/comparison-v1.html` |
| Converging disciplines / overlap | Venn diagram (2-3 sets + intersection) | `variants/comparison-v2.html` |
| Numbers, stats, KPIs | Stat circles / bubbles / orbits / KPI row | `variants/stats-v1.html` · `v3` · `v4` |
| Multi-KPI dashboard / scorecard | Scorecard grid (2×3 bento, category headers) | `variants/stats-v5.html` |
| Data series / table | Flat chart / data table | `variants/charts-v2.html` · `v3` |
| Process / timeline / roadmap | Process ×5 / timeline | `variants/process-timeline-v1.html` |
| Capability map / ecosystem | Ecosystem map (zones + centre hub) | `variants/process-timeline-v5.html` |
| People | Team grid | `variants/team-v1.html` |
| Screenshot / image | Image + text layouts / motif poster | `variants/image-content-v1.html` |
| Photo / mood image | **Duotone hero** — `.duo` renders any photo navy-duotone at runtime (§9.2) | `variants/image-content-v4.html` |
| Hero image, "pixelated" website look | **Dot hero** — convert with `scripts/halftone.py` (§9.1c), or the shipped `dot-lighthouse` / `dot-dancers-orange` motifs | `variants/image-content-v5.html` |
| Clickable detail | Expandable cards | `variants/cards-v1.html` |
| Case study / partner showcase | Image-top cards (photo + title + body ×3) | `variants/cards-v3.html` |
| Hero message + proof / colour-block moment | Split panels (R1 / R13) | `variants/splits-v1.html` · `v2` |
| Case study with photo | 50/50 image bleed + text sidebar | `variants/splits-v4.html` |
| Hub / capabilities around a core | Orbit diagram (rings + nodes) | `variants/orbit-v1.html` |
| Data ecosystem / radial signals | Radial spokes (centre + 6-8 labelled items) | `variants/orbit-v2.html` |
| Value props / strategic pillars | Floating bubbles (overlapping text circles) | `variants/orbit-v3.html` |
| Partner / tech ecosystem | Logo wall (categorised grid or hero count) | `variants/logo-wall-v1.html` |
| Two engines / overlapping systems + funnel | Cluster diagram + index row (R5) | `variants/stats-v6.html` |
| Phased plan on one board | Phase board — tint panel + step rule + KPI band (R8) | `variants/process-timeline-v6.html` |
| Capability tiles / mixed bento | 3×2 tile grid — cells + stats + one motif crop (R12) | `variants/cards-v4.html` |

**Photo slots:** brief supplies a photo → hero moment: convert to brand dot
art with `python3 scripts/halftone.py photo.jpg --fg navy --bg none` (§9.1c);
photographic moment: `.duo`. No photo → pick from the §9.2a pack by metaphor
(13 pre-duotoned brand photos, via `data-motif` — never wrap pack photos in
`.duo`, never generate photography, never leave a grey box). Full-colour
photography never ships (screenshots excepted).

**v3-contract semantic markers, applied at fill:** a `**token**` inside an
approved action title → `<span class="hl">token</span>` (strip the asterisks;
one per title max, §4.4). A `Direction?` annotation in a ```` ```data ````
block → `.stat--pos` on `good` (Orange 700; at most ONE per slide; weight
≥300 below 90px) and `.stat--neg` on `bad`; unannotated numbers stay default
ink — never guess direction from the sign (§10.1).

**Layout laws (§15) bind the fill step — the verifier measures them and FAILs
the build.** The ones hand-filling most often breaks:
- Text glyphs stay inside x 80–1840 and above the y 985 footer band; only
  furniture lives in the footer band (§15.1).
- Text never overlaps text; decoration never covers >30% of a text block
  (deliberate exceptions carry `data-text-safe="true"` and get eyeballed);
  rules/stems/vrules keep ≥24px from glyphs — 40px for display numerals
  (§15.2). Ghost numerals sit clear of statement text, never same-tone on top.
- Siblings align: one top edge per row (6px), even gaps (8px), two lanes max
  on timelines, CTAs pinned not flowed, orbit nodes centre-anchored,
  one takeaway geometry (x 160 / y ≈ 877) per deck (§15.3).
- Display numerals must FIT their container (656px inner on a w768 panel ≈
  4 thin glyphs at 240px); cards hug content; no undeclared full-width dead
  band >280px inside y 240–880 (§15.4/15.6).
- Body copy never sits on halftone/texture art; furniture contrast is pixel-
  sampled — keep decorative fills out of the furniture corners (§15.5/15.1).

Icons come from `assets/icons/`, one Markdown file per weight family —
`line.md` (9) · `solid.md` (16) · `bold.md` (5) · `accents.md` (2) — each
icon under its own `##` heading (§8.1 — ONE weight family per
icon row/slide; deck default is the solid family) pasted **inline** in an
`.icon` host — verbs/capabilities get icons, parallel nouns keep dot headers;
`spark`/`spark-bold` are air accents, max 2 per deck. Mark parallel blocks
with `data-build` to reveal them one per keypress while presenting (§14) —
use on one or two slides, not everywhere. Speaker notes go in
`<aside class="notes" hidden>` (the `N` key reveals them). User-supplied images: downscale to ≤1920px, re-encode, base64-inline, give
each a short descriptive `alt`, sit them on Cream with the `.screenshot`
keyline — never full-bleed — then re-run the verifier. Numbers become a chart archetype — never prose bullets,
never a raw unstyled table.

### 4b. Capacity pre-flight (seconds, no browser)

```bash
python3 scripts/check_capacity.py deck.html --skill .
```

Catches text overflow from the HTML alone, before you spend a single
screenshot on it. It reads `capacity.json` and flags any slot over its limit
(`.body 371/194 chars (+91%)`) plus slides over their total.

Read the summary line, not just the absence of errors: **`checked N · over
limit N · locked/exempt N · UNCHECKED N`**. Slides with no `data-archetype`
cannot be checked, and the tool says so rather than passing them — a run over
an unfilled shell reports `NOTHING WAS CHECKED`. Fix overflow by picking a
lower-density variant, never by shrinking type (§4.5).

This is text volume ONLY. It is a cheap gate before step 5, not a substitute
for it.

### 5. The art-direction pass — LOOK at every slide (mandatory, unskippable)

You are an agent with eyes: nothing ships that you have not literally seen.

```bash
python scripts/verify_deck.py deck.html --screenshots shots/ --contact-sheet
```

1. The verifier checks self-containment, banned strings, structure, sizes,
   brand discipline, and captures **every** slide headlessly (its composition
   heuristic flags dead lower halves — that is a tripwire, not the review).
   With `--screenshots` it also runs the **§15 geometry pass** (glyph-accurate
   overlap / margin / footer-band / grid-drift checks straight from the
   rendered DOM) and **furniture contrast sampling**. Geometry FAILs block
   delivery — fix the layout, re-run, and only then judge aesthetics.
2. **Read the direction's exemplar first** (`assets/exemplars/<direction>.png`)
   — that image is the bar every slide gets compared against.
3. **Read `shots/contact-sheet.png` — one image, every slide.** Judge the
   whole-deck criteria there: C6 deck rhythm (does one archetype repeat? do
   two adjacent slides share archetype + treatment?), C7 colour quota, C2 dead
   lower halves, C1 focal element. Repetition is far easier to catch on the
   sheet than across a dozen separate images, and it costs a fraction of the
   context.
   **The sheet cannot judge type legibility, glyph collisions or contrast at
   480×270 — do not try.** The verifier measures those from the DOM, and every
   slide it FAILed or WARNed is outlined in orange on the sheet.
4. **Read at full resolution only: the cover, and every outlined slide.**
   Then critique what you actually see against the checklist (§12.15a):
   C1 focal element · C2 no dead lower half · C3 edge anchor · C4 type
   discipline · C5 collisions · C6 deck rhythm · C7 colour quota. Keep a
   slide × criterion table.
5. Patch fails by **upgrading to a stronger recipe** (strip → the snippet's
   variant 1, add a field/panel/takeaway) — never by nudging paddings. The
   pass cuts as well as adds: quotas are ceilings, not targets — if a
   passing slide reads crowded, remove one element before shipping.
6. Re-shoot only the patched slides (`--slides 4,7`) and **look again**.
   Max 2 iterations per slide; a persistent fail forces the archetype swap
   to the nearest §12.15 recipe (note it in the delivery). A slide failing
   C1 + C2 never ships.

Print-to-PDF works (print CSS ships) — that answers PDF requests for free.

### 6. Deliver (G2 format above, plus the seen-report)

The G2 message includes **one line per content slide**: *seen → issue →
fix* (or "passed first look"). This makes skipping the look visible — if you
cannot write the line, you did not look.

## Input mode: deck-content-builder Markdown

When the input is a content file from the `deck-content-builder` skill,
read **`references/HANDOFF-CONTRACT.md`** — it holds the contract, the
element-to-render mapping, and the `spec` fields it fills. Skip it entirely
for raw input.

## House copy rules

<!-- HOUSE-COPY-RULES v2 — keep byte-identical with the block in deck-content-builder/SKILL.md -->
- **No em-dashes or en-dashes in slide copy.** Use commas or short sentences. (The ` — ` separators in the contract's headings are format syntax, stripped at render — they never reach a slide.)
- **Copy freeze:** never alter the wording, punctuation, or spelling of copy carried from an approved content file. Changes are proposed at the plan gate, never made silently.
- **British spelling for English-language decks** (personalisation, organisation, behaviour). Other languages use their own standard spelling. The brand line "WPP Enterprise Solutions | MAP" stays verbatim in every language.
- **No buzzwords:** leverage, harness, transformative, synergy, paradigm.
- **Concrete and specific, never vague; every claim traces to the provided context.**
<!-- /HOUSE-COPY-RULES -->

(v1 of this skill endorsed em-dashes; v2 flips to the content skill's rule so
approved copy survives rendering untouched.)

## Revising a delivered deck

Editing an already-delivered deck: read **`references/REVISING.md`**.
The one rule that belongs here: if the request adds a chapter, replaces the
narrative spine, changes design direction, or touches more than about a
third of the slides, that is a NEW deck — present a fresh G1 and wait. The
revision path never launders a rebuild past the gate.

## Fences & broader cases

PDF, motion, pptx, aspect ratio, 30+ slide decks, micro-decks, presenters,
non-English decks: **`references/EDGE-CASES.md`**. Open only when one applies.

## Bundled resources

- **`canon/`** — 25 templates traced from the real slide bank:
  `templates/<id>.html` (paste this — in Claude Design, rewrite it inline),
  `PREVIEWS.png` (all 25 on one labelled sheet), and `CATALOG.md` +
  `catalog.json`, generated from sources kept outside the skill.
  **`canon/CATALOG.md` is the entry point for step 4.**
- **`references/CLAUDE-DESIGN.md`** — the whole deck in Claude Design: the
  Slides artifact, the design-system install, and the brand as inline styles.

Each other file is named where it is used. Three rules that live nowhere else:

- **Never read `references/capacity.json`, `assets/exemplars/` or
  `assets/photos/` into context.** They are script and human inputs;
  `capacity.json` alone is ~11,700 tokens. `check_capacity.py` reads it for you.
- **Never open `assets/snippets/*.html` at fill time.** Those 13 files are the
  authoring source, up to 6,300 tokens each; the deck reads `variants/` only.
- **`references/sections/` is the only place to edit the guideline.** `CORE.md`
  and `build/WPP-ES-DESIGN-GUIDELINE.md` are generated by `scripts/build_docs.py`,
  and `verify_deck.py` fails the deck if either has drifted.

After editing a canonical snippet, regenerate the kit:

```bash
python3 scripts/derive_capacity.py --skill . --demo <a-deck>.html --write --index --split
```
