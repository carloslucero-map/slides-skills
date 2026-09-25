# Typography

**WPP Sans** in exactly five shipped weights. A geometric sans with a tall x-height; turn on stylistic
alternates for the single-storey "a" with `font-feature-settings: "salt" 1`.

| Weight | Role, verbatim from the playbook |
|---|---|
| **Thin 100** | "used for large format display copy only" — Big Statements, divider titles, giant numerals. Never small, never running text. |
| **Light 300** | "used for titles in all caps and in sentence case for headlines" |
| **Regular 400** | "used for all other copy" — sub-headlines, body copy, footers, cover meta |
| **Medium 500** | Eyebrows, labels, pill text, and the one title highlight |
| **Bold 700** | A real bold file, for the footer brand line. Never faux-bold, never body emphasis. |

No Black, no italics ship. Design within the five and never synthesize the missing ones. The fallback stack is
`'WPP', 'Poppins', 'Century Gothic', system-ui, sans-serif` — a geometric sans is the closest substitute if the
embedded faces fail.

## The hierarchy contract

**Headlines are Light, running text is Regular.** Every tier differs from its neighbour by **weight or case,
not just size**: Thin display → Light headline → Regular-caps sub-headline → Regular body → Medium-caps label.

This is a correction, not a preference. Both headline and body used to be Light, with size the only contrast,
and it was the single most-reported hierarchy failure in the system.

## The scale

Every value below is as shipped in the generated stylesheet at 1920 × 1080.

| Style | Weight | Size | Line height | Tracking | Case |
|---|---|---|---|---|---|
| Big Statement | Thin 100 | 150px (81–220 range; 220 on the poster) | 0.82 | −0.02em | Caps or sentence |
| Big Quote | Thin 100 | 120px | 1.04 | −0.01em | Sentence, curly quotes |
| Divider number | Thin 100 | 104px | 1 | −0.02em | Written "01." |
| Divider title | Thin 100 | 136px (104 classic) | 0.88 (0.86 classic) | −0.02em | ALL CAPS |
| Hero numeral | Thin 100 | 240px (144 / 280 variants) | 0.8 | −0.02em | — |
| KPI numeral | Thin 100 | 110px | 1 | — | — |
| Agenda numeral | Thin 100 | 88px (72 dense) | 1 | −0.02em | "1." |
| Stat-circle numeral | Thin 100 | 90px | 1 | — | — |
| Outro title | Light 300 | 99px | 0.9 | — | Sentence |
| Cover title | Light 300 | 81px | 0.9 | 0 | ALL CAPS |
| Headline, measured | Light 300 | 64px | 0.9 | −0.005em | Sentence |
| Headline, default | Light 300 | 54px | 0.9 | −0.005em | Sentence, max two lines |
| Agenda chapter | Light 300 | 50px (42 dense) | 1 | — | Sentence |
| Headline, caps variant | Light 300 | 48px | 0.94 | +0.01em | ALL CAPS |
| Cover subheader | Light 300 | 31px | 1.16 | — | Sentence |
| Body, band | Regular 400 | 26px | 1.32 | — | Sentence |
| Body, columns | Regular 400 | 24px | 1.3 | — | Sentence |
| Body, 4-col and boxes | Regular 400 | 22px | 1.3 | — | Sentence |
| Sub-headline | Regular 400 | 24px | 1.15 | +0.08em | ALL CAPS |
| Cover meta | Regular 400 | 24px | 1.3 | −0.01em month | Month caps, Orange 700 |
| Eyebrow subtitle | Medium 500 | 24px | 1 | +0.12em | ALL CAPS, Orange 800 |
| Label | Medium 500 | 18px | 1 | +0.1em | ALL CAPS |
| Pill | Medium 500 | 16px | 1 | +0.08em | ALL CAPS |
| Footer brand | **Bold 700** | 16px | 1 | +0.01em | `WPP Enterprise Solutions \| MAP` |
| Source | Regular 400 | 12px | 1.1 | — | Sentence |
| Page number, confidential | Regular 400 | 11px | 1 | +0.08em | ALL CAPS |

Two sizes are worth knowing the history of. **54 vs 64px:** the bank sets slide headlines at 32pt, which is
64px at pt × 2; the 54px default descends from the retired ×1.5 conversion. Canon templates use 64; the
default stays 54 until the whole scale is re-decided. **15 vs 16px:** the label row read 15px until
2026-09-11, one pixel under the floor the verifier actually enforces, while pills, gantt rulers and milestone
flags all shipped at 15px — so any deck using them failed the verifier on CSS the package itself supplied.
The table moved up to the law rather than the law moving down.

## Setting rules

- Headlines are sentence case. Titles needing strong emphasis go ALL CAPS in Light, or Thin at display scale.
- Display type is tightly leaded, 0.82–0.9. Big type never floats with loose line height.
- No bold inside body copy. Create hierarchy with the Regular-caps sub-headline or a Medium ALL-CAPS label.
- No italics. No underlines.
- Body text is left-aligned.
- A display numeral fits the inner width of its box: measure it, then size it.

## The one title highlight

Inside a headline, statement, Big Quote or divider title, the single most important token — the number, the verdict word
— may be emphasised by weight: `<span class="hl">` sets it Medium 500 at the same size and colour.

One per title, maximum; two cancel each other out. Weight only: never orange, never underline, never a size
bump. Titles only — body emphasis stays banned. The content layer marks the token in the handoff file; do not
invent highlights the content owner did not mark.

## Floors

| Class | Floor |
|---|---|
| Body copy, and any text not in a fine-print role — paragraphs, bullets, column text | **20px** |
| Fine print — labels, chips, chart and table labels, each in one of the roles the BodyCopy card lists | **16px** |
| Footer furniture only | **11px**, frozen |

Between 16 and 20px sits only the BodyCopy card's closed list of fine-print roles. No new text below 16px, ever.
If it does not fit at its floor the slide has too much content: split it or cut copy.
The verifier measures computed sizes in the rendered DOM and fails anything under its floor.
