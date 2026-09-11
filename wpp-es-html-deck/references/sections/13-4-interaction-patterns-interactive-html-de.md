## 13.4 Interaction patterns (interactive HTML decks)

Slides that are read on screen (not printed) can carry lightweight interaction. **Any element that expands, opens a detail view, or is otherwise clickable uses the one house pattern below** — do not invent a different hover/affordance treatment per deck. It keeps interactive decks feeling like one system and, crucially, makes it obvious to a viewer that something *can* be opened.

**The deck runtime already wires the behaviour:** a single click (or Enter/Space when focused) toggles a card's detail view, and the click-to-advance handler explicitly ignores cards and other interactive elements — **a click on a card never advances the slide**. The shell bakes a minimal `.card` style (hover outline + text CTA with the arrow nudge); the full pill-CTA treatment below is the snippet standard.

**Individual expansion (v4 law):** every expandable element opens and closes **on its own** — opening one card never opens, moves, or resizes anything else on the slide. The opened card's detail drops OVER the content below as a flat white panel (an overlay, not a reflow); closed siblings keep their exact position and height. Mechanically: card grids use `.canvas-grid--cards` (§12.14), and the toggle syncs `aria-expanded` per card. Never build an "accordion" where opening one item closes another — each is independent.

### The expandable-card pattern (house default)

Use it for any card, tile or panel that reveals more on interaction (e.g. a use-case card that opens a full-story modal). Three moving parts:

1. **Card at rest** — flat, borderless, square-cornered, no shadow (per §5). It gives no permanent border; the affordance lives in the hover state and the CTA button, so the resting slide stays quiet and on-brand.
2. **Hover on the card** — a **2 px Orange 600 (`#F9BD5D`) outline** fades in around the card (use `outline`, not `border`, so nothing reflows), and the card's CTA flips from Navy to Orange 700. This is the "this whole thing is live" signal.
3. **The CTA pill** — a fully-rounded pill button (§5 pill shape) sitting at the bottom of the card, carrying a **verb-led call to action + a right arrow** ("Expand the case →"). Navy fill / White Medium ALL-CAPS label at rest; on hover (of the button itself, or of the card) it flips to **Orange 700 fill / Navy label**, and the **arrow nudges ~4 px to the right**. The arrow motion is the small delight that reads as "go".

**Behaviour & accessibility.** The CTA opens the detail view on a **single click**. The whole card also opens on **Enter/Space** when focused, and carries `role="button"` + an `aria-label` — so mouse, trackpad and keyboard users all have a way in. Give the button a visible `:focus-visible` outline (2 px Navy). Respect `prefers-reduced-motion` by dropping the arrow/transition animations (the shell's print/reduced-motion rules already cover this).

**Copy.** CTA is a short **verb + noun**, Title-then-uppercased ("Expand the case", "See the workflow", "Open the story"), always followed by the → arrow. Keep it to 2–3 words.

Reference tokens (matches the pilot use-case cards):

```css
/* Card — flat at rest, orange outline on hover */
.card {
  background: var(--wpp-white);            /* or Cream */
  padding: 36px 34px;
  display: flex; flex-direction: column;
  cursor: pointer;
  outline: 2px solid transparent; outline-offset: -2px;
  transition: outline-color .14s ease;
}
.card:hover        { outline-color: var(--orange-600); }
.card:focus-visible{ outline-color: var(--wpp-navy); }

/* CTA — navy pill that flips to Orange 700 on hover; arrow nudges right */
.card-cta {
  display: inline-flex; align-items: center; gap: 12px; margin-top: 20px;
  padding: 14px 26px; border: none; border-radius: 999px; cursor: pointer;
  background: var(--wpp-navy); color: var(--wpp-white);
  font-family: inherit; font-size: 16px; font-weight: 500; /* 16px = the §4.5 floor */
  letter-spacing: .12em; text-transform: uppercase; line-height: 1; white-space: nowrap;
  transition: background .16s ease, color .16s ease;
}
.card-cta .cta-arrow { font-size: 16px; line-height: 1; transition: transform .16s ease; }
.card:hover .card-cta,
.card-cta:hover        { background: var(--orange-700); color: var(--wpp-navy); }
.card-cta:hover .cta-arrow { transform: translateX(4px); }
.card-cta:focus-visible    { outline: 2px solid var(--wpp-navy); outline-offset: 3px; }
```

```html
<div class="card" data-uc="uc1" tabindex="0" role="button" aria-label="Open full story: …">
  …card content…
  <button class="card-cta" type="button">Expand the case
    <span class="cta-arrow" aria-hidden="true">&rarr;</span>
  </button>
</div>
```

This pattern stays within the brand rules: pills (never rounded cards), flat colour, no shadows or gradients, orange as an interaction accent only, and all text Navy or White. It applies to interactive HTML decks; static/print decks show no hover affordance.

Assemble from `assets/snippets/cards.html` — don't re-derive.

---

