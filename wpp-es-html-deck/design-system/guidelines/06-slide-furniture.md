# Slide furniture

Every standard content slide carries the same four pieces, in the same places.

## Headline zone, top-left

The headline in Light 300, Navy, sentence case, two lines at most, max-width 1840px (the canvas less both edges). Optionally an **eyebrow
subtitle** in Medium 500 ALL CAPS `orange-800` beneath it — one of the sanctioned orange moments.

**Drop the eyebrow when the headline runs to two lines.**

## Source line, bottom-left

"Source: …" at 12px, 75% opacity, only when citing a claim.

## Footer strip

| Position | Element | Set |
|---|---|---|
| Bottom-left | `PRIVATE & CONFIDENTIAL` | 11px ALL CAPS, 70% opacity |
| Bottom-right | `WPP Enterprise Solutions \| MAP` | **Bold 700** 16px Navy, White on dark |
| Far bottom-right | Page number | 11px, 70% opacity |

The confidential line is wired to a spec key and added to every non-cover slide; a Spanish rendering
(`PRIVADO Y CONFIDENCIAL`) comes automatically with `lang:"es"`, other languages via a `strings` key.

**The page-number element ships empty.** Page numbers are computed at runtime from the live slide count.
Never hand-number a slide.

Covers have no footer strip — the logo badge takes its place. Dividers and outros keep the brand line and page
number, with contrast handled by the colourway's own foot and edge roles.
