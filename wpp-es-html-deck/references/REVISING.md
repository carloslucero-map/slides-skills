<!-- Split out of SKILL.md to keep the always-loaded file small.
     Loaded on demand; see the stub in SKILL.md for the trigger. -->

## Revising a delivered deck (the most common real job)

**Revision means edits to an already-delivered deck, addressed by slide
number / `data-slide-id`.** If the request adds a chapter, replaces the
narrative spine, changes the design direction, or touches more than about a
third of the slides, that is a NEW deck: present a fresh G1 (marking which
slides survive) and wait — the revision path never launders a rebuild past
the gate.

- **Never rerun `build_shell.py` on an existing deck** — it would discard
  filled slides. Edit in place, addressing slides by `data-slide-id`.
- Page numbers are runtime-computed: add, remove, reorder freely.
- After any edit, re-run `verify_deck.py`; deliver with a one-line diff
  summary ("slide 5 is now a comparison; nothing else touched").
- One slide, alternative treatment: build it in place, screenshot both, let
  the user pick.
- **A/B compare sheet** (12+ slide decks, or on request): for the 2–3
  highest-stakes slides, render A/B alternates differing on a *free axis
  only* into a separate throwaway `deck-variants.html` — a plain scrolling
  page of scaled thumbnails (wrap each slide in a fixed 768×432 crop box,
  `transform:scale(0.4)`), pairs labelled "Slide 7 — A: 3-column / B:
  stat-circle comp". Never put duplicates inside the real deck. Splice the
  winners, delete the sheet, re-verify.

### In Claude Design

The deck is the Slides artifact, so the revision happens there, and the same
new-deck rule applies.

- **Edit the slide files in place** (`project/slides/<id>.html`) and publish
  them to the same artifact. Never rebuild the deck, and never produce an
  `.html` copy beside it.
- **Page numbers are typed, not computed.** After adding, removing or moving
  a slide, rewrite every slide's page number as `NN / total` (the design
  system's FooterFurniture card).
- **No verifier, no screenshots.** The Slides type asks not to render-check
  slides unless the user asks. Deliver the link with the one-line diff
  summary.
- **An alternative treatment is a second slide** right after the original,
  id `<id>-alt`, which the user keeps or deletes in the editor. There is no
  A/B sheet and no `deck-variants.html`, and never an image in the chat.

