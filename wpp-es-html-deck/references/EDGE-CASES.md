<!-- Split out of SKILL.md to keep the always-loaded file small.
     Loaded on demand; see the stub in SKILL.md for the trigger. -->

## Fences & broader cases

- **PDF:** print CSS ships — Ctrl+P → save as PDF, one page per slide. On
  the Claude Slides path the Claude Slides deck exports PDF itself.
- **Motion:** on the Claude Slides path, Slides' own transitions and builds
  as the design system sets them, and `references/MOTION.md` where it sets
  none, for any design system (`references/SLIDES.md`, step 6). Counting
  numbers, word-by-word titles and living dots belong to the animated HTML
  deck, built only when it is asked for or picked, and only in WPP ES | MAP,
  the one system the skill carries a copy of. On the HTML path, a
  runtime layer only (`HTML-BUILD.md` §14) — never bespoke keyframes,
  never a JS/React library; auto-static under reduced-motion, print and
  headless capture, so PDFs and the verifier are unaffected.
- **pptx:** on the Claude Slides path the Claude Slides deck exports PPTX itself, so
  that is the answer there. On the HTML path it is out of scope: hand the
  *Markdown content* to a pptx skill; never screenshot-paste slides.
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

