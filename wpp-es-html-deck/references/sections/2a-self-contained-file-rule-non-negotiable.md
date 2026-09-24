## 2a. Self-contained file rule (non-negotiable)

**Scope: the standalone HTML file.** In Claude Design the deck is an Artifact made from the Slides type, and the opposite holds there: images and fonts are *uploaded* and referenced by the URL the upload returns — a `data:` URI is refused — so this section does not apply. `references/CLAUDE-DESIGN.md` governs that surface.

**Every deck ships as a single, standalone `.html` file that opens correctly by double-clicking it in any browser, with no other files present, no folder structure, and no internet connection.** Decks are shared with colleagues who just open them locally, so a deck that relies on an external path is broken on arrival.

Concretely, this means **all** of the following are embedded inline, never linked out to:

- **Fonts** — the five WPP Sans weights embedded as base64 inside `@font-face { src: url("data:font/woff2;base64,…") }`. The generator does this for you.
- **Logos** — the MAP lockup pasted in as an **inline `<svg>…</svg>`** element (preferred) or a base64 data URI, never an `<img src>` file path.
- **Icons** — any dotted icon as inline SVG, never an external reference.
- **Illustrations & halftone artwork** — the mountain/bee/etc. as a base64 `data:image/…` URI, never a file path.
- **PNGs, JPEGs, photos, and any other raster or vector asset** — base64 data URI in the `src` / `background-image`, never a file path.

Rules of thumb:

- **No relative or absolute file paths, and no external URLs**, anywhere in the final HTML — not in `<img src>`, `background-image`, `@font-face src`, `<link>`, `<script src>`, `<use href>`, or CSS `url()`. The only sanctioned "external" thing is an inline SVG referencing its own internal `#id`.
- **No CDN links either** (fonts, CSS resets, JS libraries) — pull the content in and inline it. The file must render fully offline.
- The `assets/` paths quoted throughout this guideline are **build-time sources**: the generator (and you, during the fill step) read the asset from there, then **inline its contents** into the HTML. They are never left as live references in the shipped file.

**Payload budget.** Base64 makes files ~33 % bigger, so keep sources lean: **every raster asset ≤ 300 KB before base64**, and treat **5 MB total deck size as the warn threshold** (`verify_deck.py` checks both). The shipped motifs are pre-optimized for this budget — the mountain is now ~150 KB against the 2.4 MB original — so preferring the shipped assets keeps you inside the budget automatically.

**Verification before sharing:** move the finished `.html` to an empty folder on its own (or disconnect from the network) and open it in a browser. If any font falls back, any logo/icon/illustration/image fails to appear, or anything 404s, the file is not self-contained — fix it before it goes out. Then run `scripts/verify_deck.py`.

---

