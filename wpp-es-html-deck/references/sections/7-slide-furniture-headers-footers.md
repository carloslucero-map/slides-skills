## 7. Slide furniture (headers & footers)

Every standard content slide carries:

### 7.1 Headline zone (top-left, full width)
- Headline: WPP Light 54 px, Navy, sentence case, max two lines, at (80, 28) px, max-width 1760 px.
- Optional **eyebrow subtitle**: WPP Medium 24 px ALL CAPS **Orange 800** at y = 132 (`.subtitle` — one of the sanctioned orange moments, §1.4). *Drop it when the headline runs to two lines.*

### 7.2 Source line (bottom-left)
- "Source: …" WPP Light 12 px Navy at left 80 / bottom 60 px. Only when citing.

### 7.3 Footer strip
- Bottom-left: `PRIVATE & CONFIDENTIAL` — 11 px ALL CAPS at left 80 / bottom 14. **Wired to the `confidential: true` spec key** — the generator adds it to every non-cover slide; the Spanish rendering (`PRIVADO Y CONFIDENCIAL`) comes automatically with `lang:"es"`, and any other language via the `strings` spec key.
- Bottom-right: **`WPP Enterprise Solutions | MAP`** — WPP **Bold 700** 16 px Navy (White on dark slides), at right 80 / bottom 34.
- Far bottom-right: page number — 11 px, at right 80 / bottom 14. The `.pageno` element ships **empty**: page numbers are computed at runtime from the live slide count (see §14.5) — never hand-number.
- Covers have no footer strip (the logo badge takes its place). Dividers/outros keep the brand line + page number, with contrast handled automatically by the colourway's `foot`/`edge` roles (§11).

---

