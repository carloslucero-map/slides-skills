# Data visualisation

**Charts and diagrams are circles first**, with flat fills from the primary and secondary palettes; bars only
when circles genuinely cannot carry the comparison (ChartsV2, the Gantt of ProcessTimelineV3). No gradients, no
3-D, no outlines.

## The house patterns

**Bubble and stat compositions** — overlapping flat circles at different sizes and colours, each carrying
either a big stat (Thin or Light numeral with a small ALL-CAPS label) or a stage label. The colour sequence
mixes Navy and the orange ramp; text inside follows the contrast matrix.

**Concentric and orbit diagrams** — dotted 1px navy hairline circles as guides, flat circles sized by value
stepping up along a diagonal, thin navy leader lines from each circle's edge to its callout outside on the
cream. Each node is placed by its
centre, at exact clock positions.

**The warm intensity ramp** — a sequence encoding increasing magnitude steps through `orange-500` → `600` →
`700` → `800`/`900` alongside the size step. Colour encodes intensity or sequence, **never good or bad**.

**KPI dashboards** — a row of big stats above short descriptions. Donut percentages are drawn as filled
circles, not ring gauges.

Legends and axes stay minimal: small caps labels, thin navy lines only where a timeline or axis needs one.

## Size by area, not diameter

A circle for twice the value is √2 wider, not twice as wide. Sizing by diameter quadruples apparent magnitude.
This is the data-honesty rule the guideline names explicitly.

## Stat anatomy

Numeral in Thin or Light at 90–150px Navy. The `+` or `−` sign at full numeral size. The `%` set small and
superscripted top-right at roughly 25–30% of the numeral height. Label in Medium ALL CAPS 18px below,
left-aligned to the numeral.

## Direction semantics

The playbook has **no green and no red**. In brand data-viz colour encodes intensity or sequence, and
direction is carried by the sign. One sanctioned semantic layer sits on top, inside the closed palette:

| Token | Colour | Meaning |
|---|---|---|
| `data-pos` → `.stat--pos` | `orange-700` | Direction is meaningful **and favourable** — the win glows |
| `data-neg` → `.stat--neg` | `wpp-navy` | Direction is meaningful and unfavourable — stays quiet, the weight of ink |

- Apply **only when direction is meaningful.** A market size or a headcount is neutral and keeps the
  composition's default colour. Direction is annotated at the content stage, never guessed.
- **Favourable is not the same as a positive sign.** "−41% cycle time" is a win and glows. "+8% churn" is bad
  and does not.
- Never green or red, never another hue, never colour-coded body copy. This is a numeral treatment only.
- **At most one glowing stat per slide.** If everything glows, nothing does.
- Contrast: Orange 700 thin numerals on Cream measure about 2.5:1, so `.stat--pos` ships at weight 300 minimum
  below 90px, or sits on White. At 90px and up, Thin is fine.
- `.stat--neg` is not re-declared for the navy ground, so on a dark slide it resolves Navy on Navy. Set those
  stats in `text-inv` by hand.

Extra categorical colours, if truly needed, come from the tertiary palette with its accessibility
restrictions — large text only for the light set, White type on the dark set.
