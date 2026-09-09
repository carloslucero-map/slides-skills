## 3. Colour

### 3.1 Primary palette

| Name | HEX | RGB | Pantone | CMYK | Role |
|---|---|---|---|---|---|
| **WPP Navy** | `#000050` | 0, 0, 80 | 2758 C | 100/90/0/25 | The brand colour. Text, logo, dots, dark backgrounds |
| **WPP Cream** | `#FAFAF0` | 250, 250, 240 | 9064 C | 0/0/17/0 | Default slide background |
| **WPP White** | `#FFFFFF` | 255, 255, 255 | Substrate | — | Text on dark backgrounds; **rare** alternate background only (see §3.3a) |

Proportion: **Cream + White always in excess of Navy.** Navy dominates only on deliberate moments (dividers, outros, statement slides) — never the whole deck.

### 3.2 Secondary palette (the Orange ramp)

Used "for distinction and variation as needed" — accents, dots, data viz. Never the base of an entire deck.

| Name | HEX | RGB | Pantone | CMYK |
|---|---|---|---|---|
| **Orange 900** | `#6A290A` | 106, 41, 10 | 175 C | 13/78/77/59 |
| **Orange 800** | `#D94E0E` | 217, 78, 14 | 7598 C | 0/70/100/17 |
| **Orange 700** | `#FF7800` | 255, 120, 0 | 158 C | 0/62/97/0 |
| **Orange 600** | `#F9BD5D` | 249, 189, 93 | 135 C | 0/28/87/0 |
| **Orange 500** | `#FFF5CD` | 255, 245, 205 | 9140 | 0/4/27/0 |

### 3.3 Colour roles (from the playbook "Colour Combinations" page — the master role mapping)

The playbook's roles, verbatim: **Backgrounds = White, Cream, Orange 500 only. Text = Navy, White only. Accents = Navy + the full orange ramp.** Two consequences the playbook states outright: **Orange 600 never carries text** (never use it as a text-bearing background), and only Navy/White ever set type. MAP decks add Navy as a *punctuation* background (dark moments, dividers, outros — established in the ES PowerPoint template); that is the one sanctioned extension.

| Role | Allowed colours |
|---|---|
| **Backgrounds** | **WPP Cream (default, every content slide)** · Orange 500 (`#FFF5CD`) (occasional accent moment) · WPP White (rare — see §3.3a) · WPP Navy (dark **moments** only, never the deck's base) |
| **Text** | WPP Navy · WPP White — plus **only** the sanctioned Orange moments listed in §1.4 |
| **Accents** (dots, shapes, chart fills) | WPP Navy · Orange 900 · Orange 800 · Orange 700 · Orange 600 · Orange 500 |

### 3.3a Background consistency (do not mix warm and cold whites)

**WPP Cream `#FAFAF0` is the single default background for the whole deck (a locked default — §12.0).** Every content slide uses it. This keeps the deck's "white" one warm, consistent tone from first slide to last.

- **Do not** switch some content slides to pure White `#FFFFFF` and leave others on Cream — side by side, Cream reads warm and White reads cold, and the deck looks inconsistent. This is the most common error to avoid.
- Pure **White** is used only as a deliberate, rare device — e.g. a full-bleed photography/halftone slide that needs a clean white field, or a single gallery moment — never as a casual alternate to Cream for ordinary content.
- The deck's rhythm comes from **Cream (dominant) → Navy (dark punctuation) → Orange 500 (occasional accent moment)**, not from alternating Cream and White.
- In code: default `.slide` background is Cream; use `.slide--navy` for dark moments and `.slide--tint` (Orange 500) sparingly. Avoid `.slide--white` unless the rare case above genuinely applies.

### 3.4 Sanctioned background + dot combinations

When a background carries decorative dots, only these pairings are used (background × dot colour):

| Background ↓ / Dots → | Cream/White (tone-on-tone) | Orange 700 | Orange 600 | Orange 500 | WPP Navy |
|---|---|---|---|---|---|
| **WPP White** | ✓ (cream dots) | ✓ | ✓ | ✓ | ✓ |
| **WPP Cream** | ✓ (white dots) | ✓ | ✓ | ✓ | ✓ |
| **Orange 500** | ✓ (white/cream dots) | ✓ | ✓ | — | ✓ |

Text on all of these remains **WPP Navy**. **When using Navy dots, text must never overlap the dots** — keep type entirely on the light ground (with the one exception of divider titles set in WPP White knocked out of a large navy dot, see §12.5).

### 3.5 Accessibility matrix (text on background)

| Background | Text colour | Small text | Large text |
|---|---|---|---|
| White `#FFFFFF` | Navy | AAA | AAA |
| Cream `#FAFAF0` | Navy | AAA | AAA |
| Orange 500 `#FFF5CD` | Navy | AAA | AAA |
| Orange 700 `#FF7800` | Navy | AA | AAA |
| Orange 800 `#D94E0E` | Navy | AA | AAA |
| Orange 900 `#6A290A` | **White** | AAA | AAA |
| Navy `#000050` | **White** | AAA | AAA |

Practical rules: body copy only ever sits on White, Cream or Orange 500. Orange 700/800 may carry short, large Navy text (labels inside chart circles). Orange 900 and Navy always take White text.

### 3.6 Tertiary palette (information graphics only)

The template's user guide defines a tertiary set strictly for data visualisation when the primary/secondary ramps run out. Never for backgrounds, body text or decoration.

Light set (accessible for infographics; large text only — never body text):
`#FFC8DC` pink · `#FFB4B4` red · `#D2BEFF` purple · `#80C0F5` blue · `#15FFCC` turquoise · `#B4FF64` green · `#FFFF78` yellow

Dark set (accessible for large/body text, white type):
`#8C0050` magenta · `#500000` maroon · `#500050` plum · `#000050` navy · `#00423E` deep teal · `#005000` deep green · `#A0A000` olive · `#0A1E78` indigo

(An indigo-violet ramp `#0A1E78 · #323CAA · #6464D2 · #AA96FF · #D2BEFF` also exists in the wider WPP pillar system and appears in the template's user guide — treat it as reference only; the ES pillar ramp is the Orange one.)

### 3.7 CSS tokens

```css
:root {
  /* Primary */
  --wpp-navy:  #000050;
  --wpp-cream: #FAFAF0;
  --wpp-white: #FFFFFF;
  /* Secondary (orange ramp) */
  --orange-900: #6A290A;
  --orange-800: #D94E0E;
  --orange-700: #FF7800;
  --orange-600: #F9BD5D;
  --orange-500: #FFF5CD;
  /* Roles */
  --bg:        var(--wpp-cream);
  --bg-alt:    var(--wpp-white);
  --bg-tint:   var(--orange-500);
  --bg-dark:   var(--wpp-navy);
  --text:      var(--wpp-navy);
  --text-inv:  var(--wpp-white);
  --accent:    var(--orange-700);
  /* Semantic data colours (§3.8) */
  --data-pos:  var(--orange-700);
  --data-neg:  var(--wpp-navy);
}
```

(The generator also emits per-deck role vars — `--dv-*` for the divider colourway and `--ty-*` for the outro — resolved from the spec keys; see §11.)

### 3.8 Semantic data colours (v4 — the positive/negative cue)

The playbook has **no green/red**: in brand data-viz, colour encodes intensity or sequence, never good/bad, and direction is carried by the `+`/`−` sign. v4 adds one sanctioned semantic layer on top, inside the closed palette:

| Token | Colour | Meaning |
|---|---|---|
| `--data-pos` → `.stat--pos` | **Orange 700** `#FF7800` | A number whose direction is meaningful **and favourable** — the win glows |
| `--data-neg` → `.stat--neg` | **WPP Navy** `#000050` | A number whose direction is meaningful and unfavourable — stays quiet, weight of ink |

Rules:

- Apply **only when direction is meaningful** — a market-size figure or a headcount is neutral and stays in the composition's default colour. Annotate direction at the content stage (HANDOFF-CONTRACT v3 `(dir: good|bad|neutral)`), not by guessing.
- **Favourable ≠ positive sign.** "−41% cycle time" is a win → `.stat--pos`. "+8% churn" is bad → `.stat--neg`. The semantics follow the meaning, never the arithmetic sign.
- Never green/red, never other hues, never colour-coding body copy — this is a numeral/stat treatment only (`.kpi .v`, `.hero-num`, `.hero-row .n`, stat callouts).
- Contrast: Orange 700 thin numerals on Cream measure ~2.5:1 (§15.5) — `.stat--pos` therefore ships at **weight 300 minimum (never Thin 100) below 90 px**, or sits on White; at display sizes (≥ 90 px) Thin is fine as wayfinding-scale type.
- At most **one `.stat--pos` moment per slide** — if everything glows, nothing does.

---

