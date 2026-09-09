## 5. The Dot system (shapes & backgrounds)

The playbook: *"The dot is the most important device in our storytelling"* — default colour **Orange 700**. *"We scale them from micro to macro for a wide range of expression."* The three registers (playbook p.29, now shipped as `data-dots` presets — `field-micro` / `field-mid` / `field-macro`):

1. **MICRO** — a dense **organic scatter** of tiny dots (Ø ≈ 1–1.5 % of canvas width ≈ 20–30 px), irregular non-grid spacing, densest at the cluster's heart and dissolving outward, a few pairs touching/fusing. Reads as stipple texture / energy. (Also the halftone illustrations of §9 and the dotted "WPP" logo letters.)
2. **MID** — roughly a dozen circles (Ø ≈ 15–25 % of canvas width ≈ 290–480 px) drifting across a zone, several overlapping or **fused into peanut shapes**, several cropped by the edges.
3. **MACRO** — 3–4 enormous circles (Ø ≈ 60–110 % of canvas width), **always heavily cropped by the canvas edges** — they read as crops, never as balls.

**Fused metaballs are sanctioned:** two same-colour circles overlapping merge into one flat "peanut" silhouette (free in flat CSS — no filters, no tricks). The playbook uses them in every register; one or two fused pairs per composition is the house accent, ten is noise.

Hard rules:

- **Never use a single circular shape that takes up more visual weight than the canvas** (playbook, verbatim) — dots always appear as a composition (several circles, varied sizes), or bleed off the edge so they read as a crop, never one dominating centred ball. Macro circles must bleed.
- **One colour per dot field.** A register preset is one hue from the sanctioned combos (§3.4) — multi-colour scatters are the agenda/divider locked compositions' privilege, not a content-slide treatment.
- Dots of the same colour may overlap and merge (flat fill, no transparency, no strokes).
- Only the sanctioned background/dot colour combinations of §3.4.
- **Navy dots never sit behind text** (exception: divider title knockout, §12.5).
- Dots are decoration anchored to edges/corners; the content zone stays clear.
- Tone-on-tone dots (white-on-cream / cream-on-white) are the subtlest background treatment and are always safe.

Other shape vocabulary (everything else in the template):

| Shape | Spec | Use |
|---|---|---|
| **Pill** | Fully-rounded rectangle (`border-radius: 999px`), padding 10 × 26 px, flat Navy fill with White 15 px Medium ALL-CAPS label (Cream fill / Navy text on dark slides) | Column headers, tags, category chips |
| **Dot bullet** | Small solid circle Ø **16 px**, Navy or Orange 700 | Bullet marker, step separator between text boxes |
| **Arrow / chevron** | Small solid Navy triangle ≈ 22 × 30 px (`.sep-arrow`) | Between process text boxes (flow direction) |
| **Thin rule** | 1 px Navy line | Table row separators, timeline axes only — never decorative underlines |
| **Left bracket** | Thin Navy `[` | Grouping rows in tables/timelines |
| **Cards/boxes** | Rectangles, square corners, flat fill in White / Cream / Orange 500 / Navy — **no border, no shadow, no rounded corners** (rounding is reserved for pills) | Content grouping |
| **Stat circle** | Flat-fill circle with centred number + label (see §10, §12.12) | Data visualisation |

---

