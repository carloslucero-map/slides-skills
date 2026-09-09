<!-- Split out of SKILL.md to keep the always-loaded file small.
     Loaded on demand; see the stub in SKILL.md for the trigger. -->

## Fences & broader cases

- **PDF:** print CSS ships — Ctrl+P → save as PDF, one page per slide.
- **Motion:** a runtime layer only (guideline §14) — never bespoke keyframes,
  never a JS/React library; auto-static under reduced-motion, print and
  headless capture, so PDFs and the verifier are unaffected.
- **pptx:** out of scope — hand the *Markdown content* to a pptx skill; never
  screenshot-paste slides.
- **16:9 only.** Offer the 16:9 deck; never stretch the locked slides.
- **30+ slides:** keep every raster ≤300KB; more than 6 chapters → split the
  deck into parts (the locked agenda physically holds 6).
- **Micro-decks:** ≤4 content slides or one chapter → cover + content +
  thank-you only (no agenda/dividers). Auto for single-chapter; set
  `"microDeck": true` otherwise.
- **Presenters:** comma-separate up to 2 names, else a team name. `""` means
  no presenter line — never a placeholder.
- **Non-English decks:** `lang` + `strings` keys; British-spelling rule is
  English-only; the brand line never translates.

