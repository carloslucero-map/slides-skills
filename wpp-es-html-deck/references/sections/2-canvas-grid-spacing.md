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

- Left/right content edge: **80 px**.
- Headline block: y = **28 px**, max-width 1760 px, one or two lines max.
- Optional eyebrow subtitle: y = **132 px** (see §7.1).
- Content band: y = **260 px** to **960 px** (`.content-band`: top 260, bottom inset 120).
- Source/citation line: bottom-left, left 80 / bottom 60 px.
- Footer furniture: brand line right 80 / bottom 34; page number right 80 / bottom 14 (see §7.3).
- Column widths on the 1760 px content band (shipped grid gaps 80/80/56):
  - 1 column: 1760 px · 2 columns: **840 px** each (gap 80) · 3 columns: **≈533 px** each (gap 80) · 4 columns: **398 px** each (gap 56).

**Whitespace rule:** whitespace must be **shaped** and deliberate — asymmetric, counterweighted by the composition, never leftover. Never fill the canvas with text; fill it with composition (§12.15). Leftover whitespace below y = 700 is the #1 rejected-deck signature (§12.15a C2; v4 tightened the tripwire — WARN ≥ 0.83, FAIL ≥ 0.92 background fraction in the content band). Big Statement and divider slides intentionally leave 40–60 % of the canvas empty (or covered only by background dots) — that air is registered and deliberate.

**Margin-consistency law (v4, enforced §15.9):** the content edge is one line, deck-wide. On every non-bleed content slide the leftmost text block starts at **x = 80** (±6 px measured) and the headline sits exactly at x = 80. The only sanctioned departures are **declared edge-bleed media** (§12.9 v4 — media anchored to canvas edges/corners, marked by the `.media--bleed-*`/`.media--corner` utilities or a panel/canvas composition that owns the full height) and the locked slides. A slide whose text edge wanders (x = 96 here, x = 120 there) reads as a different deck — the verifier WARNs on it.

---

