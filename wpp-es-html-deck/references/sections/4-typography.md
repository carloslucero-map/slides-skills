## 4. Typography

### 4.1 Typeface

**WPP Sans**, in exactly the **five shipped weights**, in the playbook v0.2 roles: **Thin 100** (large-format display ONLY), **Light 300** (titles and headlines), **Regular 400** (sub-headlines, body copy, footers, cover meta), **Medium 500** (eyebrows, labels, pills), and **Bold 700** — a real bold file, used for the footer brand line (no faux-bold). No Black and no italics ship in this package; design within the five weights and never synthesize the missing ones. Geometric sans with a tall x-height; **turn on stylistic alternates for the single-storey "a"** (`font-feature-settings: "salt" 1`).

**The v4 hierarchy contract: headlines are Light, running text is Regular.** Before v4 both were Light and the only contrast was size — the single most-reported hierarchy failure. Now every text tier differs from its neighbour by **weight or case, not just size**: Thin display → Light headline → Regular-caps sub-headline → Regular body → Medium-caps label.

The generator embeds all five weights as base64 data URIs — one `@font-face` per weight, mapped to the standard weight numbers:

```css
/* Emitted by scripts/build_shell.py — never external font paths (§2a) */
@font-face { font-family:'WPP'; src:url('data:font/woff2;base64,…') format('woff2'); font-weight:100; font-display:swap; }
/* …and likewise for 300, 400, 500, 700 */

body { font-family:'WPP','Poppins','Century Gothic',system-ui,sans-serif;
       font-feature-settings:"salt" 1; }
```

Fallback stack: a geometric sans (Poppins/Century Gothic) is the closest visual substitute if the embedded fonts somehow fail.

### 4.2 Weight usage rules (playbook v0.2, verbatim roles)

- **Thin** — "used for large format display copy only" (Big Statements, section/divider titles, giant numerals). Never at small sizes, never for running text.
- **Light** — "used for titles in all caps and in sentence case for headlines": slide headlines (sentence case, default) and the ALL-CAPS title variant for strong emphasis (`.headline--caps`).
- **Regular** — "used for all other copy": **sub-headlines (set in CAPS — 'use this to support the headline, or lead the body copy')**, **body copy**, and **footers**. Also cover meta lines.
- **Medium** — eyebrows/labels (ALL CAPS), pill text, and the single-token title highlight (§4.4).

### 4.3 Type scale

Values as shipped in the generator's CSS (1920 × 1080 canvas; legacy PowerPoint pt = px ÷ 1.5).

| Style | Font & weight | Size (px) | Line height | Letter spacing | Case |
|---|---|---|---|---|---|
| **Big Statement / display** | WPP Thin (100) | **150 default** (81–180 range) | × 0.82 | −0.02 em | ALL CAPS or sentence |
| **Divider number & title** | WPP Thin (100) | **104** | × 0.86 (title) | −0.02 em | ALL CAPS |
| **Big Quote** | WPP Thin (100) | 120 | × 1.04 | −0.01 em | Sentence, "curly quotes" |
| **Cover title** | WPP Light (300) | 81 | × 0.9 | 0 | ALL CAPS |
| **Cover subheader** | WPP Light (300) | 31 | × 1.16 | 0 | Sentence |
| **Outro "Thank you"** | WPP Light (300) | 99 | × 0.9 | 0 | Sentence |
| **Slide headline** | WPP Light (300) | **54** | × 0.9 | −0.005 em | Sentence case, **max two lines** — may carry ONE `.hl` Medium token (§4.4) |
| **Slide headline, caps variant** (`.headline--caps`) | WPP Light (300) | **48** | × 0.94 | +0.01 em | ALL CAPS — "strong emphasis" titles (playbook); use on ≤ 1 in 4 content slides |
| **Sub-headline / lead-in** (`.subhead`) | WPP Regular (400) | **24** | × 1.15 | +0.08 em | ALL CAPS, Navy — "supports the headline, or leads the body copy" (playbook); sits at the top of the content band |
| **Eyebrow subtitle** (under headline) | WPP Medium (500) | **24** | × 1 | +0.12 em | ALL CAPS, **Orange 800** |
| **Agenda numeral** | WPP Thin (100) | **88** (72 in 6-chapter dense mode) | × 1 | −0.02 em | `1.` style, Orange 700 |
| **Agenda chapter title** | WPP Light (300) | 50 (42 dense) | × 1 | 0 | Sentence |
| **Big subheader** | WPP Medium (500) | 24 | × 1 | +0.12 em | ALL CAPS |
| **Small subheader / label** | WPP Medium (500) | 15–20 | × 1 | +0.08–0.1 em | ALL CAPS |
| **Large body copy** | **WPP Regular (400)** | 26 (band) · 24 (columns) · 22 (4-col/boxes) | × 1.3 | normal | Sentence — Regular since v4 (playbook: "Regular is used for body copy"); the weight step below the Light headline is what creates the hierarchy |
| **Pill label** | WPP Medium (500) | 15 | 1 | +0.08 em | ALL CAPS |
| **Cover meta** (month/presenter) | WPP Regular (400) | 24 | × 1.3 | −0.01 em (month) | Month ALL CAPS Orange 700 |
| **Source / citation** | WPP Regular (400) | 12 | × 1.1 | normal | Sentence, bottom-left (Regular since v4 — playbook: "Regular is used for footers") |
| **Footer brand line** | **WPP Bold (700)** | 16 | 1 | +0.01 em | `WPP Enterprise Solutions | MAP` |
| **Footer "PRIVATE & CONFIDENTIAL" + page no.** | WPP Regular (400) | **11** | 1 | +0.08 em | ALL CAPS (Regular since v4 — legibility at furniture size) |

Typesetting rules:

- Headlines are **sentence case**; titles that need strong emphasis go **ALL CAPS in Light** (`.headline--caps`) or Thin at display scale.
- Display type is tightly leaded (0.82–0.9) — big type never floats with loose line height.
- No bold within body copy for emphasis; create hierarchy with the Regular-caps `.subhead` or the Medium ALL-CAPS label instead. (The shipped Bold 700 exists for the footer brand line, not for body emphasis.)
- No italics (none ship). No underlines.

### 4.4 Title highlight (v4 — `.hl`)

Inside a **headline, statement or divider title**, the single most important token — the number, the verdict word — may be emphasised by weight: `<span class="hl">…</span>` sets it **Medium 500 at the same size** (e.g. *"Cut onboarding time by <span class="hl">−41%</span> in two quarters"*). Rules:

- **One `.hl` per title, maximum.** Two highlights cancel each other.
- Weight only — same size, same colour (Navy, or White on dark). Never orange, never underline, never a size bump.
- **Titles only** (headline / big-statement / big-quote / divider title). Never inside body copy — body emphasis stays banned.
- The content layer marks the token in the handoff file (`**token**`, HANDOFF-CONTRACT v3); the fill step maps it to `.hl`. Don't invent highlights the content owner didn't mark.

### 4.5 Minimum font sizes (v4 — measured law, §15.10)

| Text class | Floor |
|---|---|
| Body copy (paragraphs, bullets, column text) | **20 px** |
| Any other informational text (labels, captions, chips, chart labels, table cells) | **16 px** |
| Footer furniture ONLY (`.pageno`, `.confidential`, `.source`, `.footer-brand`) | **11 px** (frozen — never add new text at this size) |

No new text below 16 px, ever — if it doesn't fit at 16 px, the slide has too much content (split it or cut copy). The verifier measures computed sizes in the rendered DOM and FAILs sub-floor text (§15.10).

This row read **15 px** until 2026-09-11, one pixel under the floor §15.10 actually enforces, while `.pill`, `.ruler-label`, `.flag`, `.proc .step-l` and `.milestone .ml` all shipped at 15 px in the generated shell. Any deck using a pill, a gantt ruler or a milestone flag therefore failed the verifier on CSS the package itself supplied. Found by building a real deck, not by reading the rule. The table defers to §15.10, so the table and the shell moved to 16 px rather than the law moving down.

---

