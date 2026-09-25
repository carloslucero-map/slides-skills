## 2. Canvas, grid & spacing


| Property | Value |
|---|---|
| Aspect ratio | 16:9 |
| Design canvas (HTML) | **1920 × 1080 px** |
| PowerPoint canvas equivalent | 13.33 × 7.5 in (**960 × 540 pt**) — **multiply pt × 2** to get px at 1920. Derivable two ways and not open to argument: 12,192,000 EMU / 1920 px = 6350 EMU/px, and 13.33 in × 72 pt/in = 960 pt, so 1920/960 = 2.0. The old ×1.5 came from treating the canvas as 1280 pt, which is its width in px at 96/in — points are 72/in. Every type and spacing figure derived through it ran 25% short. |
| Base grid | **40 px square grid** (at 1920 × 1080) — the playbook's verbatim spec: "Our most used format uses 40px square grid using 40px margins and 40px column space." The content edge is **one module (40 px)**, as stated. Everything snaps to the 40 px module |
| Page margins | **40 px left/right** (`--m-edge`, one grid unit — the content edge is x = 40, the playbook's own number). For text-dense slides the bank's own practice is a deeper text edge: `--m-text: 56px` (the measured mode of real body copy is x=57). Use `--m-edge` for structure and full-bleed furniture, `--m-text` when a column of running copy needs the extra breathing room. The previous 80 px was not in the playbook — it was two modules chosen locally and called presentation-safe |
| Column gutter | **80 px** (56 px in the 4-column grid) |

Layout maths that the shipped generator actually uses (all values from `scripts/build_shell.py`):

- Left/right content edge: **40 px** (`--m-edge`); **56 px** (`--m-text`) for a column of running copy.
- Headline block: at (40, **73**) px, max-width 1840 px (the canvas less both edges), one or two lines max.
- Optional eyebrow subtitle: y = **177 px** (see §7.1).
- Content band: x 40–1880, y = **305 px** to **1020 px** (`.content-band`: `--band-top` 305, `--band-bottom` inset 60). The column grid (`.cols`) starts higher, at y 260.
- Source/citation line: bottom-left, left 40 / bottom 60 px.
- Footer furniture: brand line right 40 / bottom 34; page number right 40 / bottom 14 (see §7.3).
- Column widths on the 1800 px column grid (`.cols`: x 40 to 1840, right inset 80; shipped gaps 80/80/56):
  - 1 column: 1800 px · 2 columns: **860 px** each (gap 80) · 3 columns: **≈547 px** each (gap 80) · 4 columns: **408 px** each (gap 56).

**Whitespace rule:** whitespace must be **shaped** and deliberate — asymmetric, counterweighted by the composition, never leftover. Never fill the canvas with text; fill it with composition (§12.15). Leftover whitespace below y = 700 is the #1 rejected-deck signature (§12.15a C2; v4 tightened the tripwire — WARN ≥ 0.83, FAIL ≥ 0.92 background fraction in the content band). Big Statement and divider slides intentionally leave 40–60 % of the canvas empty (or covered only by background dots) — that air is registered and deliberate.

**Margin-consistency law (v4, enforced §15.9):** the content edge is one line, deck-wide. On every non-bleed content slide the leftmost text block and the headline start at the content edge, **x = 40** (`--m-edge`), or at the text edge, **x = 56** (`--m-text`), ±6 px measured. The only sanctioned departures are **declared edge-bleed media** (§12.9 v4 — media anchored to canvas edges/corners, marked by the `.media--bleed-*`/`.media--corner` utilities or a panel/canvas composition that owns the full height) and the locked slides. A slide whose text edge wanders (x = 96 here, x = 120 there) reads as a different deck — the verifier WARNs on it.

---

