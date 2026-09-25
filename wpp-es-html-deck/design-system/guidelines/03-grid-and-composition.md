# Grid and composition

| Property | Value |
|---|---|
| Aspect | 16:9 |
| Canvas | 1920 × 1080 px |
| PowerPoint | 960 × 540 pt, so **pt × 2 = px** |
| Base grid | 40px square module (`grid`) |
| Margins | `m-edge` for structure; `m-text` for a column of running copy |
| Gutter | `gutter` at 2- and 3-up, `gutter-tight` at 4-up |

Columns on the 1800px column grid (x = 40 to 1840; the grid keeps an 80px right inset): one at 1800, two at 860,
three at about 547, four at 408.

The headline block sits at y = `headline-y` with the optional eyebrow at `eyebrow-y`; the content band runs
`band-top` to `band-bottom`; the source line sits bottom-left and the footer furniture bottom-right.

## The content edge

The content edge is `m-edge`, 40px, the playbook's own margin: the headline sits at (40, `headline-y`) and every
structural block starts at x = 40. A column of running copy may take the deeper `m-text`, 56px. The verifier
reads both from the deck: a text glyph outside x = 32 to 1888 fails, and a headline that starts at neither edge
warns.

## The margin-consistency law

The content edge is one line, deck-wide: on every non-bleed content slide the leftmost text block and the
headline start at the same x. A slide whose text edge wanders — 96 here, 120 there — reads as a different
deck, and the verifier warns on it.

The only sanctioned departures are declared edge-bleed media (anchored to canvas edges or corners, marked by
the `.media--bleed-*` and `.media--corner` utilities, or a panel composition owning the full height) and the
locked slides.

## Whitespace is shaped

Whitespace must be deliberate — asymmetric, counterweighted by the composition, never leftover. Never fill the
canvas with text; fill it with composition.

Leftover whitespace below y = 700 is the most common rejected-deck signature. The verifier warns at a
background fraction of 0.83 in the content band and fails at 0.92.

Big Statement and divider slides intentionally leave 40–60% of the canvas empty, or covered only by background
dots. That air is registered and deliberate — it is not the same thing as a slide that ran out of content.

## Layout laws

These hold on every content slide, whatever builds it. The HTML deck's verifier measures most of them; in
Claude Design Slides, check them by eye.

- **Text stays inside the content edge**, left and right. Art may bleed off the canvas; text never does.
- **The headline band is the headline's.** From y 73 to 201 sit only the headline and its eyebrow. Content
  starts no higher than y 240, unless a full-height panel owns the slide.
- **The footer band is the furniture's.** Below y 985 only the footer furniture carries text.
- **Text never overlaps text**, a numeral and its own caption included.
- **Decoration covers at most 30% of a block of text**; past that, the text moves.
- **Ghost numerals sit where there is no text**, set apart by position.
- **Lines, stems and ticks keep 24px from any text**, 40px from display numerals.
- **One art layer per area of the slide:** a dot field and a motif or texture never share a region.
- **Repeated items line up.** Columns, cards, KPIs and milestones share their top edge within 6px and keep
  their gaps even within 8px. Anything that must line up across siblings, such as card links, is pinned to
  the bottom rather than placed after text of varying length.
- **Diagrams centre on the midline**, x 960, unless a text column justifies the offset.
- **Text keeps 40px from the edge of unrelated art.**
- **The content band is balanced:** it sits centred between the bottom of the headline block (about y 201
  with an eyebrow, 122 without) and its anchor, the takeaway near y 877 or the footer.

## Archetypes

Pick a template by the **shape of the argument**, not by appearance. The snippet library is organised by
archetype — statement, quote, stats, columns, cards, boxes, process, timeline, orbit, splits, comparison,
media, entities — and variants within an archetype differ by density, not decoration.

No two adjacent content slides share a layout and treatment, and a deck of eight or more content slides uses at
least two densities and three layouts. A composed content slide may add dot fields, colour panels and motif
art as far as the deck's direction allows; Cream stays the base.

The canon set adds a second axis: eight families — narrative, enumeration, sequence, quantitative, comparison,
relational, media, entities — each template traced off a real bank slide with its measured geometry recorded
in its README, including where it deliberately deviates from the source and why.
