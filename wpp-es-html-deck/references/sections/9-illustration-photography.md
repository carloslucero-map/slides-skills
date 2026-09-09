## 9. Illustration & photography

### 9.1 Dot-halftone illustration (signature style)
- Images are converted to **single-colour halftone dot illustrations** (dot size modulating with tone) — the mountains, balancing rocks, ribbon, coral etc. of the brand playbook, and the "pixelated" image language of the WPP ES website.
- **The canonical generator settings (playbook p.33, verbatim):** Min Dot Size **2.0 px** · Max Dot Size **8.0 px** · Grid Type **Square** · Grid Spacing **10.0 px** · Contrast **1.00** · Jitter **0.00** · Size Variation **0.00**. Tone is expressed purely by dot size on the fixed square grid; highlights and background get sparse or no dots. (The legacy WPP Open motifs shipped in `assets/illustrations/` use a hexagonal pattern — both are sanctioned; new conversions use the canonical square grid.)
- **The pipeline (playbook p.32):** source image → dot generator → **subject-only dots, background cleaned** → recolour to a brand colourway. In this package that generator ships as `scripts/halftone.py` (§9.1c).
- Colours: **Navy on Cream/White** (default) or **Orange on Cream/White** — one colour per illustration; the background stays flat. The shipped `_Orange` files are the sanctioned orange colourways; never recolour a navy PNG.
- Composition: illustrations are anchored to an edge/corner and cropped (e.g. mountain range rising from bottom-right of covers), leaving generous clear space for type.
- New motifs still enter the package only through the registration workflow (§12.1a).

### 9.1a Illustration inventory (as shipped — `assets/illustrations/`)

Exactly **thirteen** files ship (eleven WPP Open motifs + two v4 square-grid conversions). All have transparent grounds so the Cream field shows through.

| File | Pixels | Colourway | Display rules |
|---|---|---|---|
| `WPPOpen_Mountain-01.png` | 1920×1072 | Navy | Full-bleed or right-anchored. **The only locked COVER default (§12.1a).** |
| `MAP_Mountain-01_Orange.png` | 1920×1401 | Orange | Full-bleed or right-anchored accent moment (v3.5, carved from the MAP deck's own vector art). |
| `MAP_Peaks-01_Orange.png` | 1920×1082 | Orange | Full-bleed flanking composition — two peaks framing a valley of air (v3.5). |
| `WPPOpen_Crystal-01.png` | 1920×1072 | Navy | Full-bleed or right-anchored; registered cover alternate. |
| `WPPOpen_Crystal-01_Orange.png` | 1920×1072 | Orange | Full-bleed or right-anchored accent moment. |
| `WPPOpen_Coral-01.png` | 1920×1072 | Navy | Full-bleed or right-anchored; registered cover alternate. |
| `WPPOpen_Coral-01_Orange.png` | 1920×1072 | Orange | Full-bleed or right-anchored accent moment. |
| `WPPOpen_Rocks-01.png` | 964×540 | Navy + cream | **Accent only, ≤ 640 px tall** — pairs with the Comparative archetype (§12.8). |
| `WPPOpen_Rocks-01_Orange.png` | 964×540 | Orange + cream | **Accent only, ≤ 640 px tall** — §12.8 in orange-family decks (v3.5 recolour). |
| `WPPOpen_Ribbon-01_Orange.png` | 964×540 | Orange + cream | **Accent only, ≤ 640 px tall** — pairs with §12.8. |
| `WPPOpen_Ribbon-01_Navy.png` | 964×540 | Navy + cream | **Accent only, ≤ 640 px tall** — §12.8 in navy-family decks; low-contrast ON navy backgrounds, keep it on Cream (v3.5 recolour). |
| `HT_Lighthouse-01.png` (v4) | 1400×808 | Navy | Canonical square-grid dot conversion (§9.1c) — guidance/direction metaphor; right-anchored or split-half hero. 15 KB. |
| `HT_Dancers-01_Orange.png` (v4) | 1400×933 | Orange | Canonical square-grid dot conversion — momentum/craft metaphor; accent moments. 17 KB. |

Rules for use:
- **The 1920px-class motifs** may run **full-bleed** (`object-fit:cover` — their empty
  area is positioned for type) or **right-anchored** (the cover-registry treatment, §12.1a).
- **Rocks / Ribbon** (both colourways) are EMF-sourced at capped resolution: use them as
  **accents no taller than 640 px on the canvas — never full-bleed, never covers**. The
  verifier's motif-routing check WARNs when a 964px asset lands in a ≥1100px host.
- Navy motifs sit over **Cream** (default) or White only — never over Navy (they would
  disappear). For an orange moment use the shipped `_Orange` files.
- Place **behind** text (`z-index` below content) and never let body copy sit over the dense part of the halftone.
- In a generated shell, request motifs via the `illustrations` spec key (keys: `mountain`,
  `mountain-orange`, `peaks-orange`, `crystal`, `crystal-orange`, `coral`, `coral-orange`,
  `rocks`, `rocks-orange`, `ribbon-orange`, `ribbon-navy`, `dot-lighthouse`,
  `dot-dancers-orange`, plus §9.1b textures and §9.2a photos) — the generator pre-inlines
  each as a `<template data-asset="…">` ready for the fill step. (`bee` was retired in
  v3.5: 560px orphan, below the quality bar.)

### 9.1b Background textures (as shipped — `assets/textures/`, v3.5)

Two full-bleed 1920×1080 dot-field textures, quantized to the brand ramp. They are
**backdrops, not ink**: place at `z-index` 0 under a whole slide (via `data-motif` +
`.motif--bleed`), max ONE texture moment per deck, never behind dense body copy.

| Key | File | Feel |
|---|---|---|
| `contours` | `contours-cream.png` | Cream topographic contour lines (slate-navy dots) — tactile paper layer for editorial-quiet; rhymes with the "map" theme. |
| `orbs` | `orbs-cream.png` | Soft navy halftone orbs on cream — quiet depth behind statement moments. |

### 9.1c The halftone converter — `scripts/halftone.py` (v4, authoring-time tool)

Converts any raster image into a brand dot illustration at the canonical settings above. It is a **build-time tool** — its outputs are optimized PNGs/SVGs that get base64-inlined like any motif; the script itself never ships inside a deck.

```
python3 scripts/halftone.py photo.jpg --fg navy --bg none --width 1600   # subject-only dot art
python3 scripts/halftone.py photo.jpg --fg orange --invert               # flip tone mapping when the subject is light
python3 scripts/halftone.py --overlay 1920 1080 --fg orange-800 --seed 7 # website-style halftone-circle cluster overlay
```

- Colourways: `navy` (default) · `orange` (700) · `orange-800` · `white` · `cream` — flat single-colour dots, transparent ground by default.
- **When a brief supplies a photo and the slide wants the "pixelated" hero look, this is the sanctioned route:** convert to dot art (subject-only), inline the result. The alternative photo rendering is the navy duotone (§9.2). **Those two are the only photo treatments — full-colour photography never ships** (screenshots excepted, §12.9).
- `--overlay` produces the website's halftone-circle cluster (2–4 flat macro circles bleeding off the canvas, one colourway) as a transparent PNG for compositing over duotone photos at authoring time — the raster route exists because CSS gradients/filters are banned (§12.16 stays law).
- Outputs obey the §2a payload budget (≤ 300 KB before base64; the script enforces it).

### 9.2 Photography (when photos are used instead of halftone)
Three categories, all pillar-agnostic:
- **Abstract** — textures, repetition, visual movement.
- **Landscapes** — awe-inspiring natural landscapes representing transformation and journeys.
- **Subject focus** — one clear point of interest, always a living thing (person, animal, plant).
Full-bleed or half-slide crops; never clip-art, never busy stock-business imagery. Since v3.5 a **13-photo navy-duotone library ships** (§9.2a) so no photo slot ever renders as a grey box; brief-supplied photos still win when they exist, and everything counts against the §2a payload budget.

**Two sanctioned renderings (v4): dot-halftone conversion (§9.1c) or navy duotone via `.duo`.** The halftone route is the hero treatment — the website's "pixelated" language; the duotone is the photographic treatment. Pick one per moment, never both on one image. For the duotone: any photo the
brief supplies — colour or not — is wrapped in
`<div class="duo" style="…geometry…"><img src="data:…" alt="…"></div>`:
the kit renders it as navy shadows / white highlights at runtime (grayscale +
screen blend against the navy host; isolated, print-safe, works on any image
with zero preprocessing). Rules:

- Compositions: half-slide hero split (photo left or right, statement or
  content on the other half), a split panel fill, or an R11 full-bleed poster
  (high-impact only). Quota: counts as a dark moment for the direction.
- Text never sits ON the duotone; it owns the other half. Keep ≤300 KB per
  image (§2a), always a short descriptive `alt`.
- Product-UI screenshots are NOT photos — they stay full-colour on the
  `.screenshot` keyline (§12.9). Full-colour photography anywhere else is
  off-brand, and the verifier flags raw `<img>` outside `.duo`/`.screenshot`.

**Decision path when a slide wants a photo:** brief supplies one → hero moment?
convert with `halftone.py` (§9.1c); photographic moment? `.duo` +
base64 `<img>`. Brief supplies none → pick from the §9.2a pack by metaphor
(via `data-motif`; pack photos are pre-duotoned, NEVER wrap them in `.duo`).
Nothing fits → swap to the motif/panel sibling variant (splits V3,
image-content V0). **Never generate photography, never ship a grey box.**

### 9.2a Navy-duotone photo library (as shipped — `assets/photos/`, v3.5)

Thirteen photographs mined from the MAP brand deck itself — already navy-duotone,
ten of them cut-outs with transparent grounds. **Internal-WPP-use-only** (stock
imagery licensed to WPP; do not reuse outside WPP deliverables). Request via
`spec.illustrations` and place with `data-motif` like any motif. Pick by metaphor:

| Key | Subject | Metaphor | Form |
|---|---|---|---|
| `photo-lighthouse` | Lighthouse on rocky islet | guidance, direction | cut-out 1150px |
| `photo-handoff` | Hands passing a relay baton | handoff, partnership | cut-out 1200px |
| `photo-confetti` | Falling confetti | celebration, launch | cut-out 1100px |
| `photo-chess` | Row of chess pieces | strategy, precision | cut-out 1200px |
| `photo-globe` | Stippled engraving globe | global, markets | cut-out 820px |
| `photo-pencils` | Hand fanning pencils | creativity, options | cut-out 1050px |
| `photo-dancers` | Dancers' feet mid-step | momentum, craft | cut-out 1050px |
| `photo-gears` | Interlocking halftone gears | integration, systems | cut-out 900px |
| `photo-fibers` | Fiber-optic wisps + nodes | connectivity, data flow | cut-out 1150px |
| `photo-team` | Six people arm-in-arm (from behind) | teamwork, alignment | cut-out 1000px |
| `photo-diver` | Diver under sunlit surface | exploration, depth | full-bleed 1600px |
| `photo-fjord` | Misty fjord, mirror water | clarity, journey | full-bleed 1600px |
| `photo-ridge` | Layered mountain ridge | ascent, long view | full-bleed 1600px |

Rules: cut-outs sit on Cream/White like halftone motifs (they carry their own
transparency); full-bleeds fill `.motif--panel`/`.motif--bleed` hosts. Respect the
native widths (the verifier's motif-routing check WARNs on upscales). Max ONE
photo moment per spread of 6 slides unless the direction is high-impact.

---

