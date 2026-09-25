# Colour

Three primaries and a five-step orange ramp. That is the whole palette; the tertiary set exists for
information graphics only.

## Primary

| Token | Hex | Pantone | CMYK | Role |
|---|---|---|---|---|
| `wpp-navy` | `#000050` | 2758 C | 100/90/0/25 | The brand colour: text, logo, dots, dark grounds |
| `wpp-cream` | `#FAFAF0` | 9064 C | 0/0/17/0 | The default slide background |
| `wpp-white` | `#FFFFFF` | — | — | Text on dark grounds; a rare alternate background |

White has no ink: in print it is the paper.

Proportion: **Cream and White always in excess of Navy.** Navy dominates only on deliberate moments —
dividers, outros, statement slides — never the whole deck. How often a deck goes dark follows its direction: no
Navy content moments in editorial-quiet (tint panels are fine), at most one in six in statement-led, none or one
in data-forward (on the hero number), and up to one in three in high-impact, evenly spread, where a colour-block
split counts as half.

## Secondary — the orange ramp

`orange-900` `#6A290A` (175 C) · `orange-800` `#D94E0E` (7598 C) · `orange-700` `#FF7800` (158 C) ·
`orange-600` `#F9BD5D` (135 C) · `orange-500` `#FFF5CD` (9140).

In print (CMYK): `orange-900` 13/78/77/59 · `orange-800` 0/70/100/17 · `orange-700` 0/62/97/0 · `orange-600`
0/28/87/0 · `orange-500` 0/4/27/0.

Used "for distinction and variation as needed" — accents, dots, data viz. Never the base of a deck.

## The role mapping

The playbook's roles, verbatim: **Backgrounds = White, Cream, Orange 500 only. Text = Navy, White only.
Accents = Navy plus the full orange ramp.** Two consequences it states outright: **Orange 600 never carries
text**, and only Navy and White ever set type. MAP decks add Navy as a *punctuation* background — dark
moments, dividers, outros — and that is the one sanctioned extension.

## Do not mix warm and cold whites

`wpp-cream` is the single default background for the whole deck. Switching some content slides to pure White
and leaving others on Cream is the most common error in this system: side by side, Cream reads warm and White
reads cold, and the deck looks inconsistent.

Pure White is a deliberate, rare device — a full-bleed halftone slide that needs a clean field, a single
gallery moment. The deck's rhythm comes from **Cream (dominant) → Navy (dark punctuation) → Orange 500
(occasional accent)**, not from alternating Cream and White.

In code: `.slide` defaults to Cream, `.slide--navy` for dark moments, `.slide--tint` sparingly, and
`.slide--white` only for the rare case above. `.slide--ground` makes a partial-height ground change at
`ground-y` — measured off a real slide where a numeral row crosses the boundary, which is what makes the
composition read as one object rather than two stacked rows. It is not a licence to invent grounds.

## Sanctioned background × dot pairings

| Background | Tone-on-tone | Orange 700 | Orange 600 | Orange 500 | Navy |
|---|---|---|---|---|---|
| White | ✓ cream dots | ✓ | ✓ | ✓ | ✓ |
| Cream | ✓ white dots | ✓ | ✓ | ✓ | ✓ |
| Orange 500 | ✓ white/cream dots | ✓ | ✓ | — | ✓ |

Text on all of these stays Navy. **When dots are Navy, text must never overlap them** — the one exception is a
divider title in White knocked out of a large navy dot.

On a Navy dark slide, type is White and dots are White, Cream or Orange 700.

## Contrast

| Background | Text | Small | Large |
|---|---|---|---|
| White | Navy | AAA | AAA |
| Cream | Navy | AAA | AAA |
| Orange 500 | Navy | AAA | AAA |
| Orange 700 | Navy | AA | AAA |
| Orange 800 | Navy | AA | AAA |
| Orange 900 | **White** | AAA | AAA |
| Navy | **White** | AAA | AAA |

Contrast is measured against what is actually behind the text, art included: body copy at least 4.5:1,
display type at least 3:1.

Body copy only ever sits on White, Cream or Orange 500. Orange 700 and 800 may carry short, large Navy text
such as labels inside chart circles. Orange 900 and Navy always take White.

**The one failing pair kept from the source:** Orange 700 thin numerals on Cream measure about 2.5:1. It stays
because it is the sanctioned favourable-stat highlight, and the rule that makes it safe is a weight floor —
`data-pos` ships at weight 300 minimum below 90px, or sits on White. At 90px and up, Thin is fine as
wayfinding-scale type. The `KpiRow` component's README carries this in full.

A Thin numeral below 90px that takes orange on a content slide, such as a process step number, takes Orange 800,
which holds 3:1 on Cream; Orange 700 there is the favourable stat's, under its weight rule. A ghost numeral takes
one flat tone, Orange 500 on Cream or White or Cream on Navy, and never transparency.

## Tertiary — information graphics only

Never backgrounds, body text or decoration. Light set, large text only: `tert-pink` `tert-red` `tert-purple`
`tert-blue` `tert-turquoise` `tert-green` `tert-yellow`. Dark set, accessible for body text with White type:
`tert-magenta` `tert-maroon` `tert-plum` `tert-navy` `tert-teal-deep` `tert-green-deep` `tert-olive`
`tert-indigo`.

Green and red carry no good/bad meaning here. The palette has no semantic pair: direction is the `+`/`−` sign
and, where it genuinely matters, the single `data-pos` highlight.

## Per-deck colourways (not tokens)

The divider and outro resolve role variables per deck from the spec. Six divider colourways ship —
`orange`, `orange-600`, `orange-500`, `white`, `navy-dots`, `navy-full` — and two outros, light and dark. Each sets its own
`--dv-bg`, `--dv-text`, `--dv-sub`, `--dv-foot`, `--dv-edge` (and `--ty-*` for the outro), including the
contrast flips: on `navy-dots` the bottom-right locked dot is Navy, so the footer sitting on it turns White.
These are build outputs of `build_shell.py`, not stable tokens, which is why they are documented here instead.
