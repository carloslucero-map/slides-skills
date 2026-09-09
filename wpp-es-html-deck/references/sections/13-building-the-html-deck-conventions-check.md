## 13. Building the HTML deck — conventions & checklist

### 13.1 Skeleton

```css
.slide {
  position: absolute; top: 0; left: 0;
  width: 1920px; height: 1080px; overflow: hidden;
  background: var(--bg);            /* Cream — the one content background */
  color: var(--text);
  font-family: 'WPP', 'Poppins', 'Century Gothic', system-ui, sans-serif;
  font-weight: 300;                 /* Light is the display voice; .body/.tbx set Regular 400 (§4.2) */
  font-feature-settings: "salt" 1;
  display: none;                    /* nav script reveals the active slide */
}
body:not(.js) #frame .slide:first-of-type { display: block; }  /* no-JS fallback */
body.js .slide.is-active            { display: block; }         /* script adds .js */
.slide--navy  { background: var(--bg-dark); color: var(--text-inv); }
.slide--tint  { background: var(--bg-tint); }
/* .slide--white — rare only; see §3.3a. Default (.slide) is Cream. */
.slide--white { background: var(--bg-alt); }
```

- One `<section class="slide" data-slide-id="…">` per slide; keyboard ←/→ navigation; slide counter. The nav script stamps `body.js` on load (a `<noscript>` banner explains the single-slide fallback) and **fills every empty `.pageno` at runtime from the live slide count** — never bake page numbers into the markup.
- **Scaling — avoid the flex-shrink trap.** Do **not** put the fixed 1920 × 1080 `#frame` inside a `display:flex` centring container: a flex child with an explicit width still shrinks (default `flex-shrink:1`), which silently squashes the frame and pushes content off the right edge. Instead scale it absolutely and centre by translate:

```css
#stage { position: fixed; inset: 0; overflow: hidden; background: #0a0a1a; }
#frame { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; transform-origin: top left; }
```
```js
function fit(){
  var vw=innerWidth, vh=innerHeight, s=Math.min(vw/1920, vh/1080);
  frame.style.transform='translate('+(vw-1920*s)/2+'px,'+(vh-1080*s)/2+'px) scale('+s+')';
}
addEventListener('resize', fit); fit();
```
  (If you prefer flex centring, you must add `flex-shrink:0` to `#frame`.) Always verify in the browser that `#frame`'s bounding rect fills the viewport with no side gutter before shipping.
- Decorative dots: absolutely-positioned `div`s with `border-radius: 50%`, flat `background`, no opacity, `z-index` below content, cropped by `overflow: hidden`. The locked compositions are drawn by the shell's `[data-dots]` presets — their geometry is verbatim and their colours resolve through the deck's colourway; never hand-edit them.
- Halftone illustrations: use the eight shipped motifs (§9.1a). Where no shipped motif fits, approximate with an inline-SVG dot pattern in Navy or Orange 700 — or omit and use dot clusters instead. Do not substitute regular photography for the halftone style unless the outline calls for photography, and never promise assets the package does not contain.

### 13.2 Mapping an outline to slides

1. Generate the shell: `python scripts/build_shell.py --spec spec.json --out deck.html`. The spec's five required keys (title, subtitle, month, presenter, chapters) plus the sanctioned choice keys (`direction`, `dividerColourway`, `cover`, `outro`, `confidential`, `lang`, `contact`, `illustrations`) produce the locked cover, agenda, dividers and Thank-you, and one placeholder per planned content slide. (Single-chapter micro-decks omit the agenda and dividers automatically.)
2. **When the input is a deck-content-builder Markdown file, follow the input-mode mapping in SKILL.md — approved titles are carried verbatim.**
3. Fill each placeholder from the archetype snippets: key messages / transitions → **Big Statement**; quotes → **Big Quote** (§12.4–§12.5).
4. Body content: choose column count by the number of parallel points (1–4); sequences get **Arrows**, parallel relations get **Dots**, categories get **Pills** (§12.6–§12.7).
5. Numbers → data-viz archetypes (§12.12) — circles first (area-true, never diameter-scaled), bars only when genuinely needed.
6. Rhythm check: all content slides on the one Cream background (§3.3a), orange as seasoning, navy for punctuation moments (max ~1 in 6); no two adjacent slides carrying the same heavy dot treatment.
7. Verify: self-containment (§2a), payload budget, then `scripts/verify_deck.py`.

### 13.3 Do / Don't

**Do**
- Apply the **five locked defaults** via the generator (§12.0) — cover, agenda, divider, Thank-you, Cream background — changing only spec keys and content placeholders.
- Name the company **"WPP Enterprise Solutions | MAP"** everywhere (§1.7).
- Use huge Thin type and macro dots for drama; keep content slides quiet and airy; orange as seasoning ("avoid making things too orange").
- Keep headlines to two lines max; drop the eyebrow subtitle when the headline wraps.
- Anchor decorative dots to edges/corners, bleeding off-canvas.
- Keep all body text Navy (or White on dark), left-aligned; use the exact hex values; flat fills everywhere.
- Assemble content slides from `assets/snippets/`; for interactive decks, use the house expandable-card pattern for anything clickable (§13.4).

**Don't**
- No gradients, shadows, outlines around cards, rounded-corner cards (pills only), accent bars/underlines.
- No text over Navy dots (except the divider-title knockout).
- No single dominant centred circle heavier than the canvas.
- No orange body copy, headlines or bullets — only the sanctioned moments of §1.4; no colours outside this document; no bold-in-body emphasis.
- No dense multi-colour charts, and no diameter-scaled bubbles (§12.12) — circles, flat colours, generous labels.
- Never recolour or restyle the logo; Navy or White only, safe space respected. Never write "VML MAP" / "VMLMAP" (§1.7).
- Never hand-build, hand-edit or skip any of the four locked slides — the generator emits them; spec keys are the only sanctioned variation (§12.0).
- Never reference or promise assets that are not in the ships-with inventory.

---

