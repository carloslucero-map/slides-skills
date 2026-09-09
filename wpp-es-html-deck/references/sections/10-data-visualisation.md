## 10. Data visualisation

- **All charts and diagrams are based on circles** with **flat fills** from the primary + secondary palettes. No gradients, no 3-D, no outlines.
- **Bubble/stat compositions** (the house style): overlapping flat circles of different sizes and colours; each circle carries either a **big stat** (WPP Thin/Light numeral + small ALL-CAPS label) or a **stage label**. Circle colour sequence mixes Navy, Orange 900/800/700/600/500; text inside follows §3.5 (Navy on light circles, White on Navy/Orange 900). Sizing is by **area**, not diameter — see the data-honesty rule in §12.12.
- **Concentric/orbit diagrams** (playbook p.46): dotted 1 px navy hairline circles as guides/orbits, flat circles sized by value stepping up along a diagonal, **thin navy leader lines** from each circle's edge to its stat callout outside on the cream.
- **Warm intensity ramp** (playbook p.46): a sequence of circles encoding INCREASING magnitude steps through the ramp light→dark — Orange 500 → 600 → 700 → 800/900 — alongside the size step. Colour encodes intensity or sequence here, **never good/bad** (direction semantics live in §10.1).
- Stat callouts outside circles: numeral in WPP Thin/Light 90–150 px Navy with the `+`/`−` sign at full numeral size and **`%` set small, superscripted top-right (~25–30 % of numeral height)** — the playbook stat anatomy; label in Medium ALL CAPS 18 px below, left-aligned to the numeral.
- KPI dashboard pattern: row of big stats (e.g. `$2M`, `24K`, `8%`) each above a short Light description (Thin 110 px numerals in the shipped `.kpi` block); donut-style percentages are drawn as filled circles, not ring gauges.
- Legends/axes minimal: WPP Light small caps labels; thin navy lines only where needed (timelines, axes).
- Extra categorical colours, if truly needed, come from the tertiary palette (§3.6) with its accessibility restrictions.

### 10.1 Direction semantics (v4 — when a number is good or bad)

When a stat's **direction is meaningful**, give the room the cue (§3.8): the favourable number takes `.stat--pos` (Orange 700); the unfavourable one takes `.stat--neg` (Navy — the explicit "this one is the problem" registration, visually identical to default ink but semantically declared in the markup and the handoff file). Favourable follows **meaning, not sign**: "−41% cycle time" glows, "+8% churn" does not. Neutral figures (sizes, counts, dates) stay in the composition's default colour and carry no class. One glowing number per slide, maximum. The deck-content-builder marks direction in the handoff file (`(dir: good|bad|neutral)`); never guess it from the sign.

---

