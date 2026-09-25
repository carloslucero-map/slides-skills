# Illustration and photography

## Dot-halftone illustration — the signature style

Images are converted to **single-colour halftone dot illustrations**, dot size modulating with tone. This is
the "pixelated" image language of the ES website.

The canonical generator settings, verbatim: min dot 2.0px · max dot 8.0px · square grid · spacing 10.0px ·
contrast 1.00 · jitter 0.00 · size variation 0.00. Tone is expressed purely by dot size on a fixed square
grid; highlights and background get sparse or no dots.

The pipeline: source image → dot generator → **subject-only dots, background cleaned** → recolour to a brand
colourway. Colours are **Navy on Cream or White** (default) or **Orange on Cream or White** — one colour per
illustration, flat background. Never recolour a navy PNG by hand; the shipped `_Orange` files are the
sanctioned orange colourways.

Composition: illustrations anchor to an edge or corner and are cropped, leaving generous clear space for type.
They may sit behind display type, never behind body copy: body copy never sits on a halftone or a texture, and a
statement sits only over a sparse texture. A right-anchored motif keeps text left of x 1200; a motif along the
bottom keeps text above y 560.

**One motif family per deck**, repeated, never rotated slide to slide; brief images converted to halftone take
one colourway per deck. A full-bleed motif is for poster slides and a backdrop motif for stat compositions; a
high-impact deck may bleed its motif on any slide.

## Thirteen motifs ship

See the **Illustrations** asset group. Nine are 1920px-class with fully transparent grounds and may run
full-bleed or right-anchored. `WPPOpen_Mountain-01.png` is the only locked cover default.

**Rocks and Ribbon, both colourways, are different.** They are EMF-sourced at 964 × 540 and carry a **baked
opaque cream field** around the ink, so they are cream-ground-only: on Navy, on a tinted panel or over a photo
they print their own background as pale wedges. Use them as accents **no taller than 640px** — never
full-bleed, never covers. The verifier warns when a 964px asset lands in a host of 1100px or more.

Navy motifs sit over Cream or White only; on Navy they disappear. When no shipped motif fits, use a simple dot
pattern in Navy or Orange 700, or dot clusters instead.

## Two textures

Two full-bleed 1920 × 1080 dot-field textures, quantized to the brand ramp, in the **Textures** group. They are
**backdrops, not ink**: place under a whole slide, **one texture moment per deck at most**, never behind dense
body copy.

## Photography

Three categories, all pillar-agnostic: **abstract** (textures, repetition, movement), **landscapes**
(awe-inspiring nature representing transformation and journeys), **subject focus** (one clear point of
interest, always a living thing). Full-bleed or half-slide crops. Never clip-art, never busy stock-business
imagery.

**Two sanctioned renderings, and only two: dot-halftone conversion or navy duotone.** The halftone route is the
hero treatment; the duotone is the photographic one. Pick one per moment, never both on one image.
**Full-colour photography never ships** — product-UI screenshots are the one exception and stay full-colour on
their own keyline treatment.

For the duotone, wrap the image in `.duo`: the kit renders it as navy shadows and white highlights at runtime
(grayscale plus screen blend against the navy host — isolated, print-safe, no preprocessing). In Claude Design Slides the Photo card sets the same duotone in inline styles. Text never sits
on the duotone; it owns the other half. Keep each image under 300 KB and always give it a short descriptive
`alt`.

**Never generate photography, and never ship a grey box.** A 13-photo pre-duotoned library ships in the
**Photography** group so no photo slot has to render empty; a brief-supplied photo still wins when there is
one. If nothing fits, swap to the motif or panel sibling variant of the template.
