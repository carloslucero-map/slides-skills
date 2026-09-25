# The dot system

*"The dot is the most important device in our storytelling. We scale them from micro to macro for a wide range
of expression."* The default dot colour is `accent`.

## Three registers

**Micro** — a dense organic scatter of tiny dots, roughly 1–1.5% of canvas width (20–30px), irregular non-grid
spacing, densest at the cluster's heart and dissolving outward, a few pairs touching or fusing. Reads as
stipple texture and energy. Also the halftone illustrations and the dotted "WPP" logo letters.

**Mid** — roughly a dozen circles at 15–25% of canvas width (290–480px) drifting across a zone, several
overlapping or fused into peanut shapes, several cropped by the edges.

**Macro** — three or four enormous circles at 60–110% of canvas width, **always heavily cropped** by the canvas
edges so they read as crops, never as balls.

They ship as `data-dots` presets: `field-micro`, `field-mid`, `field-macro`, plus the locked agenda, divider,
cover and outro compositions.

## Fused metaballs

Two same-colour circles overlapping merge into one flat peanut silhouette — free in flat CSS, no filters, no
tricks. The playbook uses them in every register. One or two fused pairs per composition is the house accent;
ten is noise.

## Hard rules

- **Never a single circular shape carrying more visual weight than the canvas.** Dots appear as a composition
  of several circles at varied sizes, or bleed off the edge as a crop. Never one dominating centred ball, and
  macro circles must bleed.
- **One hue per register field.** A micro, mid or macro field takes one hue from the sanctioned pairings. The
  corner and edge accent presets the layouts use (`field-right`, `field-bottom`, `field-tl`, `field-accent`)
  mix up to three sanctioned colours, and the agenda and the classic divider carry multi-colour scatters; the
  default divider is one hue.
- Same-colour circles may overlap and merge. Flat fill, no transparency, no strokes.
- Only the sanctioned background and dot pairings in the Colour guideline.
- **Navy dots never sit behind text** — one exception, the divider title knocked out of a large navy dot.
- Dots are decoration anchored to edges and corners. The content zone stays clear.
- **Slides dense with content take no dots behind the content.** A content slide may take a gentle lift instead:
  a small dot cluster in one corner (the `lift-*` presets).
- **Two slides in a row never carry the same heavy dot treatment.**
- Tone-on-tone dots — white on cream, cream on white — are the subtlest treatment and always safe.

## The rest of the shape vocabulary

| Shape | Spec | Use |
|---|---|---|
| Pill | `radius-pill`, padding 10 × 26px, flat Navy fill, White Medium caps label | Column headers, tags, chips |
| Dot bullet | Solid circle Ø 16px, Navy or Orange 700 | Bullet marker, step separator |
| Arrow | Solid Navy triangle about 22 × 30px (`.sep-arrow`) | Flow direction between process boxes |
| Thin rule | 1px Navy line | Table row separators, timeline axes **only** |
| Left bracket | Thin Navy `[` | Grouping rows in tables and timelines |
| Cards and boxes | Square corners, flat fill in White / Cream / Orange 500 / Navy — no border, no shadow, no rounding | Content grouping |
| Stat circle | Flat-fill circle, centred number and label | Data visualisation |

Rounding is reserved for pills. Everything else that is not a circle is square.
