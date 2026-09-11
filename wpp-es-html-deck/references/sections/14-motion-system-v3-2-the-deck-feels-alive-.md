## 14. Motion system (v3.2) — the deck feels alive, the brand stays flat

Motion is a **runtime layer the shell applies automatically** — recipes need no
markup changes. It is a registered choice: `"motion": "full" | "subtle" | "off"`
(default per direction: high-impact and statement-led → `full`; editorial-quiet
and data-forward → `subtle`).

**Doctrine — elements move, colours never do.** Only the movement channels
animate — the individual `translate` / `scale` properties plus `opacity`;
keyframes NEVER touch the `transform` shorthand (kit elements are positioned
with base transforms and would "teleport"; `transform` belongs exclusively to
the pointer-parallax). Fills stay flat, no colour/hue animation, no blur, no
shadows in motion. Restraint carries the brand; choreography carries the energy.

- **Entrance choreography** (both levels): on each slide activation the shell
  staggers the kit in reading order — panels wipe in from their edge, headlines
  and blocks rise 34px, decorative dots pop with a spring overshoot
  (`cubic-bezier(.34,1.56,.4,1)` — the ONE sanctioned overshoot), rulers and
  bars draw themselves (`scaleX`), stems grow, motifs float in, ghost numerals
  drift in from the right. Stagger 75ms, cap ~1s; durations .5–.95s.
- **A canon template must DECLARE its motion roles, or it will not move.** The
  choreography is driven by `M_ROLES`, a closed list of selectors in
  `build_shell.py`, and every entry in it is a KIT class. The 25 canon templates
  invent 432 class names of their own; when they shipped, none were in that list,
  so twelve of them animated nothing at all but the slide fade while kit slides
  moved — decks built mostly from the canon looked dead by comparison, with no
  error anywhere. Found 2026-09-11 by opening a real deck and noticing.

  The fix is not 432 more entries. Five generic hooks sit at the top of `M_ROLES`
  and a template opts in by declaring one alongside its own class, exactly as it
  declares `fine-label` for the type tier:

  | hook | motion | what it goes on |
  |---|---|---|
  | `m-lead` | rise | the statement, lede or panel the slide opens with |
  | `m-art` | float-in | a motif or media host |
  | `m-unit` | rise, staggered | THE repeated block — column, band, card, step, person |
  | `m-mark` | pop | plotted dots, ring nodes, numerals, rail chips |
  | `m-bar` | draw | rules, bands and bars that read as drawn lines |

  Put the hook on the OUTERMOST repeated element, never on its children: the
  stagger index counts matched elements, so hooking the leaves gives forty beats
  where the design wants five. Order in `M_ROLES` sets the reading order, which
  is why the hooks lead the list.
- **Data counts up** (both levels): `.hero-num`, `.hero-row .n`, `.kpi .v`,
  `.stat-circle .v`, `.proc .n` animate 0 → value (~950ms) on first reveal,
  preserving comma decimals, dot thousands, prefixes/suffixes and zero-padding.
  Any other numeral opts in with a bare `data-count` attribute. This is the
  motion signature: **los datos cuentan**.
- **Ambient life** (`full` only): dots breathe (scale ≤1.055, 7.5s alternate,
  desynced), motif art floats ±14px (9s). Never on text.
- **Pointer parallax** (`full` only): art layers only — dot fields ≤14px,
  motifs ≤24px, ghost numerals ≤34px — text never moves.
- **Hover states** (hover-capable screens, any level except `off`): cards and
  process steps lift 8px, columns / KPIs / milestones lift 6px, stat circles
  and hero numerals swell ~5% on the sanctioned spring, takeaway bracket arms
  stretch, agenda rows nudge right. Movement only — hover never changes a
  colour outside the §13.4 clickable-card pattern.
- **Deck progress hairline** (any level except `off`): a fixed 3px orange-700
  line along the bottom edge grows with deck position — the web-page tell.
  Hidden in print and when motion is off.
- **Kinetic type** (both levels): Big Statements, Big Quotes, divider titles
  and the cover title split into word spans at runtime and rise word by word.
  Plain-text elements only; the shell handles it — never hand-split.
- **Fragments** (`data-build`, opt-in per element): blocks marked `data-build`
  hide on slide entry and reveal one per forward step (→ / Space / click)
  before the deck advances — progressive disclosure for presenting. Use on
  parallel blocks (cards, steps, columns), 3–5 per slide max; print and
  motion-off show everything.
- **Duotone life** (`full` only): `.duo` photos get a slow Ken Burns
  (scale ≤1.07 over 16s, alternating); sparks twinkle (rotate ±10°). Both
  respect every kill switch above.
- **Deterministic capture:** the verifier and any headless/PDF path pin
  `?motion=off` in the URL — screenshots and prints always see the finished
  layout, never a mid-entrance frame.
- **Always static:** `prefers-reduced-motion`, print/PDF, and headless capture
  (`navigator.webdriver`) force `off` — the verifier and PDFs see the finished
  layout. URL override for testing: `?motion=off|subtle|full` (`?motion=force`
  keeps full even headless, for motion smoke-tests).

Never add per-deck bespoke keyframes, easing, or a motion library (no React,
no GSAP — the deck stays ONE dependency-free file). New motion behaviours are
kit upgrades in `build_shell.py`, registered here — same governance as §12.1a.

---

