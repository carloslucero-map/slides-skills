## 15. Layout & UX laws (v3.6) — enforced geometry

Everything above says what the brand looks like; this section says what a slide
is **mechanically allowed to do**. These are laws, not taste: `verify_deck.py
--screenshots` measures every one of them from the rendered DOM (glyph-accurate
rects, headless Chrome) and **FAILs the build** on violations. A slide that
looks right but breaks a law is broken — fix the geometry, don't argue with
the ruler.

### 15.1 Safe areas & reserved bands

| Zone | Reserved for | Law |
|---|---|---|
| x < 80 · x > 1840 | margins | No text glyph starts left of x 80 or ends past x 1840. Decorative art bleeds freely; text never does. |
| y 28–132 | headline block | Only `.headline` (+ `.subtitle` at 132). Content never rises above y 240 except panel/canvas compositions that own the full height. |
| y 985–1080 | footer furniture | Only `.footer-brand`, `.pageno`, `.confidential`, `.source`. No other TEXT enters this band, ever. |
| Furniture anchor corners — bottom-left (0–420, 1000–1080) and bottom-right (1500–1920, 1000–1080) | furniture legibility | Decorative fills entering these corners must leave the furniture readable: the verifier samples the pixels under each furniture line and fails contrast < 2:1 (warns < 3:1). White/Cream shapes under Navy text pass; same-tone shapes under same-tone text are the classic failure (a cream dot under the cream `PRIVATE & CONFIDENTIAL` line on a navy slide). |

### 15.2 Overlap laws (the collision register)

1. **Text never intersects text.** Two text-bearing elements from different
   components may not overlap by more than 4px in both axes. This includes
   display numerals vs their own captions (a 280px `.hero-num--l` line box
   WILL collide with a `.col-sub` below it inside a 768px panel — size down).
2. **Decoration never covers more than 30% of a text block.** Dots, motifs,
   ghost numerals, rules and panels either stay clear of text boxes or the
   text moves. The sanctioned escape hatch for a deliberate composition is
   `data-text-safe="true"` on the decor element — the verifier downgrades to
   a printed WARN and the art pass must confirm legibility by eye.
3. **Body copy never sits on halftone/texture art.** Statements and headlines
   may cross *sparse* texture only when the art-direction pass confirms
   contrast by eye; paragraphs (< 28px) never do. The §12.8 `.compare-art`
   centrepiece is sized by CSS (`width:100%` on its img — never remove it);
   its text zones at x 80–500 / 1420–1840 exist because the art stays inside
   x 478–1442.
4. **Ghost numerals (`.num-ghost`) live in text-free zones.** Same-colour
   ghost + statement = both illegible. Differentiate by POSITION (right/below
   the text box), never by opacity (opacity tricks are off-brand, §12.14).
5. **Diagram hairlines keep 24px clearance from glyphs.** A vrule crossing a
   `−` sign turns "−50%" into "+50%" — rules, stems and ticks sit ≥ 24px from
   any glyph edge (40px for display-size numerals), and identical siblings use
   identical clearance.
6. **One art layer per canvas zone.** A dot field and a motif/texture never
   occupy the same region of a slide — the later one paints over the circles
   and reads as a rendering error, not a composition. Statement recipes take
   the accent field (V1) **or** the motif (V1b), never both; when two art
   devices genuinely coexist on one slide they live in separate zones
   (e.g. `field-tl` + `motif--bottom`).

### 15.3 Alignment laws (the grid is not a suggestion)

- **Siblings share edges.** Same-component siblings (columns, cards, KPIs,
  milestones, links inside cards) align their tops within 6px and their gaps
  within 8px. Auto-sized (`max-content`) grid tracks drift when content
  lengths differ — the kit's `.hero-row`/`.kpi-row` are `grid-auto-columns:1fr`
  for exactly this reason; don't override to auto.
- **Timelines run on two lanes.** Above-axis milestones share ONE top edge,
  below-axis milestones share ONE top edge; stem length absorbs copy-length
  differences. One milestone width per slide.
- **Pinned, not flowed.** Anything that must share a baseline across sibling
  containers (card CTAs, panel captions) is pinned (`margin-top:auto` /
  absolute), never flowed after variable-length copy.
- **Centre-anchored nodes.** Radial/orbit nodes anchor by their centre
  (`translate(-50%,-50%)`) at exact clock positions — top-left anchoring skews
  every label by half its own width.
- **Diagrams centre on the slide midline (x 960)** unless a content column
  justifies the offset; an unexplained 100px skew reads as an accident.
- **One geometry per furniture element per deck.** The `.takeaway` bracket
  band lives at x 160 / y ≈ 877 everywhere; in split layouts adjust `right`,
  never `left`. Source lines, subtitles and takeaways sit at the same y on
  every slide that carries them.

### 15.4 Spacing & fit laws

- **Containers fit their content and content fits its container.** Display
  numerals must fit their panel's inner width (768px navy panel − 2×56 padding
  = 656px: ≈ 4 thin glyphs at 240px — measure, then size). Text inside
  circles stays within 70% of the diameter. Cards hug content height
  (`.proc--cards` is 260→700 + takeaway) — a card whose bottom half is empty
  white is a composition failure, not whitespace.
- **Minimum clearances:** 24px text↔hairline, 40px text↔display-rule, 40px
  text↔unrelated art edge, 36px padding inside white surfaces (`.tbx`,
  `.card`, `.cell`).
- **No accidental dead bands.** A full-width empty strip > 280px inside
  y 240–880 must be either declared (`data-composition="intentional-air"` on
  statement-class slides) or filled by the recipe's anchor (ruler, takeaway,
  field). The stats V1 quartet keeps its bottom ruler for exactly this reason.

### 15.5 Contrast floor (measured, not assumed)

- Body copy ≥ 4.5:1, display type ≥ 3:1 against its EFFECTIVE background —
  the pixels actually behind it, not the slide colour.
- Footer furniture ≥ 3:1 always (verifier samples it; < 2:1 fails the build).
- Thin (weight-100) orange numerals: Orange 700 on cream measures ~2.5:1 —
  sanctioned ONLY as ≥ 64px wayfinding numerals inside locked compositions
  (agenda). Content-slide numerals default to **Orange 800** (`.proc .n`
  ships that way) or Navy.
- The §3.5 matrix governs colour pairs; this law extends it to text-over-art:
  when text must cross art, the art under the glyphs is what counts.

### 15.6 Vertical balance

Content bands centre between the headline bottom (y ≈ 132) and their anchor
(takeaway top y ≈ 877, or the footer band). Top-heavy compositions with all
mass above the fold and 40%+ empty below read as unfinished — anchor the
bottom (takeaway / ruler / KPI band / field) or centre the mass.

### 15.7 Motion UX laws (why the deck never "teleports")

The §14 doctrine says what may move; these laws say what must NEVER happen —
each one is wired into the shell, listed here so nobody undoes it:

1. **Choreography ends exactly at static layout.** Every entrance keyframe's
   end state equals the element's resting geometry; captures with
   `?motion=off` are the reference the animated deck must settle into.
2. **No property is contested.** Entrances own `translate`/`scale`/`opacity`;
   pointer-parallax owns `transform`; hover states own `transform` (buttons)
   or `scale` where no entrance animates it. A hover transition on a property
   an entrance keyframe animates completes invisibly under the animation,
   then SNAPS on release — the #1 teleport cause.
3. **Count-ups never reflow.** Counting numerals pin their final width
   (`min-width` for the duration + `tabular-nums` + `1fr` tracks) so ticking
   digits can't resize columns or re-wrap neighbours. Numerals with word
   suffixes ('1 Sep', '12 weeks') never count.
4. **Kinetic type splits before first paint.** Word-span splitting after
   display re-runs text-wrap balancing and can visibly re-break lines
   (Safari); the shell splits at load.
5. **Re-showing the current slide is a no-op.** Boundary keys / same-hash
   navigation must not replay choreography on a visible slide.
6. **Parallax variables are seeded** (0,0) so the first pointer event eases
   from rest instead of lurching from an unset state.

### 15.9 Placement laws (v4): the content edge and media anchoring

1. **Content-edge conformance.** On every non-bleed content slide the leftmost
   text block starts at x = 80 ± 6 and the `.headline` sits at exactly x = 80.
   Slides whose text edge wanders are WARNed (§2). Panel/canvas compositions
   that own the full height, edge-bled media, and the locked slides are exempt.
2. **Media anchoring.** Any rendered media block ≥ 200 × 200 px (`<img>`, motif
   host, `.duo`, photo panel) must touch at least one canvas edge (bleed), sit
   in a canvas corner, or carry `data-inset-ok` (implied by `.screenshot`;
   granted to mosaic tiles whose gutters are the composition). A rectangle
   floating inside the margins on all four sides is a FAIL — corner it or
   bleed it (§12.9). Decorative dots and icons are not media; they are exempt.

### 15.10 Type-size floor (v4)

Measured on the rendered DOM (§4.5): body-class text < 20 px WARNs; any other
visible text < 15 px FAILs, except the four furniture elements (`.pageno`,
`.confidential`, `.source`, `.footer-brand`), which are frozen at their shipped
sizes (≥ 11 px) and may never be joined by new text at that scale.

### 15.8 Enforcement

`python scripts/verify_deck.py deck.html --screenshots shots/` runs, on top of
the brand checks: glyph-accurate **overlap / margin / footer-band / grid-drift
geometry** (15.1–15.3), **furniture contrast sampling** (15.1/15.5), and the
v4 probes — **type-size floor** (15.10), **content-edge conformance** (15.9.1),
**media anchoring** (15.9.2), and the **card-grid static check** (§12.14).
FAILs block delivery; WARNs (including every `data-text-safe` and
`intentional-air` declaration) are re-checked by eye in the §12.15a art pass.
The art pass judges what the ruler can't (balance, rhythm, legibility over
art); the ruler catches what eyes skim past (a 4px overlap, a 1.04:1 footer).
A deck ships only when both agree.
