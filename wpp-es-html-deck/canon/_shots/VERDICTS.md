# Kit triage — all 51 variants

A first pass over the 13 contact sheets. **Proposed, not decided** — Carlos
overrides anything here; the point is to argue with a list rather than start
from a blank one.

One criterion did most of the work: **does the composition use the canvas, or
does it put its content in the top third and leave the rest cream?** CORE's own
C2 guardrail forbids the dead lower half, and the mechanical gate passes every
one of these. A takeaway line at the bottom counts as anchoring; nothing at the
bottom does not.

**16 keep · 17 fix · 10 kill · 8 unjudgeable**

---

## Keep (16) — good as they stand

| id | why |
|---|---|
| `charts-v1` | Stat mosaic bento. Navy hero panel, three supporting quads. Best in its family and one of the best in the kit. |
| `cards-v4` | 3×2 tile grid mixing copy tiles with stat tiles. Fills, and the rhythm of plain/navy/tint tiles carries it. |
| `logo-wall-v2` | Hero count plus a 4×4 grid. The number earns the left half; the grid earns the right. |
| `orbit-v1` | Hub, rings, four nodes, takeaway. Balanced. |
| `orbit-v2` | Radial spokes with a context column. Strongest of the three. |
| `orbit-v3` | Overlapping labelled circles. Circles clip very slightly at the right edge — cosmetic. |
| `process-timeline-v3` | Gantt swimlanes with gate markers. Clean and genuinely legible. |
| `process-timeline-v5` | Ecosystem map, four quadrants around a hub. Well balanced. |
| `process-timeline-v6` | Phase board — tint panel, step headers, KPI band at the foot. Best in the family. |
| `splits-v2` | Colour-block split, navy panel carrying a display numeral. Strong and unambiguous. |
| `stats-v5` | Scorecard bento, six KPIs grouped. Uses the whole canvas. |
| `stats-v6` | Cluster diagram plus index row. Dense, and the density is doing work. |
| `statement-quote-v1` | Statement with dot art on the right. |
| `statement-quote-v2` | Big quote with attribution. |
| `statement-quote-v3` | Navy poster with a giant ordinal. The best display slide in the kit. |
| `team-v1` | Three portraits with real bios. Reasonable balance. |

---

## Fix (17) — the composition is sound, the canvas is not

Mostly one defect: content in the top third, then nothing. Either the content
tier grows, or something anchors the foot, or the arity drops.

| id | what is wrong |
|---|---|
| `boxes-v1` | Cards are empty below their first third. |
| `boxes-v2` | Large void between the band and the takeaway. |
| `cards-v1` | 2×2 bento sits high; lower 40% unused. |
| `charts-v2` | Bars occupy the top third only. |
| `columns-v1` | Columns top, takeaway bottom, a lot of nothing between. |
| `columns-v4` | Same shape as v1, same gap. |
| `comparison-v2` | **Collision** — the takeaway line runs into the Venn circles. |
| `logo-wall-v1` | Tiles use the left half only; the right half is empty. |
| `process-timeline-v1` | Five cards, each dead below its first third. |
| `process-timeline-v2` | Milestone ruler, sparse — and a milestone escapes the box by 10px. |
| `splits-v1` | Void between the lead paragraph and the KPI row. |
| `splits-v3` | The navy half renders empty; needs its motif. |
| `stats-v1` | Numerals top, ruler bottom, half the canvas between them. |
| `stats-v2` | Hub is centred but the lower third is unused. |
| `stats-v3` | Bubbles sized honestly — the good part — but the lower half is dead. |
| `stats-v7` | Diagonal ramp leaves the entire right half empty. |
| `team-v2` | Four across, tiny, everything in the top third. |

---

## Kill (10)

| id | why |
|---|---|
| `boxes-v3` | One thin row of arrow-joined boxes, ~80% empty, nothing anchoring the foot. |
| `cards-v2` | Three small cards adrift; ~75% dead canvas. |
| `charts-v3` | A small table in the top-left corner of an otherwise blank slide. |
| `columns-v2` | Four one-line columns, ~85% empty. |
| `columns-v3` | Two columns plus a floating pill row. Enormous void. |
| `columns-v5` | Superseded by `canon/enum-numbered-4`, which does the same job from a measured original. **Retire only after the canon template has been through a real deck.** |
| `comparison-v1` | Two pill-and-text blocks in a sea of cream. Worst in the kit. |
| `process-timeline-v4` | Renders with its headline clipped by the top of the frame, over a mostly empty canvas. |
| `splits-v4` | **Broken** — the headline overlaps itself, and the image half renders blank. |
| `stats-v4` | Headline, one line of framing, a void, then numerals at the foot. |

---

## Cannot judge from these shots (8)

Every one of these is media-led, and the harness splices templates with no
image, so what the sheet shows is the placeholder, not the template. Condemning
them on this evidence would be wrong.

`image-content-v0` · `image-content-v1` · `image-content-v2` ·
`image-content-v3` · `image-content-v4` · `image-content-v5` ·
`statement-quote-v2b` · `cards-v3`

**Fix the harness first.** `shoot_snippets.py` should inject a sample photo and
motif from `assets/` when a template declares one, then re-shoot these eight.
That is a change to the tool, not to the templates, and it is a prerequisite for
judging a sixth of the kit.

---

## What this implies

- **`stats` must be split whatever else happens.** Seven unrelated compositions
  under one `data-archetype` — a quartet with a ruler, a hub, a bubble row, a
  bare numeral row, a scorecard, a cluster diagram, an intensity ramp. A model
  choosing "stats" is drawing a lottery ticket. Same for `image-content`, which
  spans a poster, a screenshot treatment and a duotone hero.
- **`comparison` and `columns` are the weakest families**, and `comparison` is
  also one of the two the curated selection has no green slide for. Both are
  rebuild work, not repair.
- **The dead lower half is systemic**, not a few bad templates. It is the single
  biggest fidelity gap against the bank, where slides run content to y≈960.
- **A fixed template is cheaper than a new one.** Of the 17 fixes, most are one
  decision — grow the content tier, add an anchor, or drop the arity by one.
