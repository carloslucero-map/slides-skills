# Claude Design — the deck lives in the Slides artifact

**In Claude Design, or any session whose Artifact tool offers a Slides type,
the deck is an Artifact made from that type — never a separate `.html`
file.**

Three sources, three jobs:

- **The design system "WPP Enterprise Solutions | MAP"** decides what the
  deck looks like: every colour, face, size and position, every element,
  fixed slide and layout.
- **The Slides type's own instructions**, which you read when you open or
  create the deck, decide how a slide is written: `project/deck.json`, one
  `project/slides/<id>.html` per slide, the calls.
- **This page** decides how the deck gets made here: the gate, the reading
  order, the install, and the one Slides rule the design system does not
  carry yet.

This page holds no brand values. When you need a hex, a size or a position,
it is in the design system.

## What carries over, what does not

**Unchanged:** a gate before anything is built (here it is the question
card, below), the four design directions, archetype choice, traced-first
layout selection, the anti-sameness review, the house copy rules, and
non-negotiables 2–8.

**Does not exist here. Never run or write them:** `build_shell.py`,
`check_capacity.py`, `verify_deck.py`, screenshots, the contact sheet; a
standalone `.html` file (the artifact exports HTML, PDF and PPTX itself); CSS
classes, `<style>`, `var()`, base64 or `data:` images, the JS motion layer.

**G2 changes.** The type does not render-check slides and asks you not to,
so there is no seen-report. Deliver the link, name the two slides to look at
first, say which headline highlights were dropped (the Headline card says
when), and offer to revise any slide by number or add an alternative beside
it.

## Asking: the question card, never text

Claude Design shows questions as a card in the chat box, and that card is the
**`AskUserQuestion` tool**. A question typed as prose — a slide table ending
in "reply 1/2/3/4" — arrives as an ordinary message nobody can click. So here
G0 and G1 are **one `AskUserQuestion` call**, before anything is written:

- **At most four questions**, the call tagged
  `"metadata": {"source": "artifact-questions"}`.
- **The design direction, always** (unless the user already named one), with
  `multiSelect: false` and your content-signal pick first, marked
  "(Recommended)":

  | label | description |
  |---|---|
  | Editorial quiet | Spacious, cream, no dark slides |
  | Statement-led | A big statement opens each chapter |
  | Data-forward | Numbers lead: stat circles, charts |
  | High-impact | Poster scale, up to 1 in 3 dark |

- **Then what their material leaves open**, most decisive first and in its
  own terms: which thread leads, what the room should do afterwards, whose
  voice the slides carry. Two to four concrete options each, a few words per
  label and description, `multiSelect: true` unless the options exclude each
  other.
- **Never ask** what the brief already answers, a question only free text can
  answer (a presenter's name, a figure: use the default or a placeholder,
  `[Presenter]`, `[€__]`), or with an "Other" or "you choose" option. The card
  adds "Other" itself.

Before the call, at most two lines of prose: what you read and the length
you plan ("Your notes cover four workstreams; I plan 12 slides in three
chapters"). **No slide table here.** The deck in the editor is the plan.
Restate the answers as a one-line assumption, then build. Ask a second round
only if the user asks for more or an answer opens a question you could not
have asked before, and never re-ask.

**The waivers still hold.** An explicit "just build it", or nobody there to
answer: no card, the recommended direction, assumptions in one line. An
approved `deck-content-builder` file: the card holds only the direction.

## No slide images in the chat

**The draft is the deck in the editor.** Never post a slide, an exemplar, a
preview, a screenshot, a contact sheet or an A/B sheet as an image in the
chat: not to choose a direction, not to show progress, not to offer an
alternative. The four exemplar PNGs stay unopened on this surface; each
direction's description in the card carries the difference instead. An
alternative for a slide is a second slide right after it, id `<id>-alt`,
which the user keeps or deletes in the editor.

## Steps

1. **Ask with the card** (above), then wait for the answers. The Slides
   type's own instructions say to decide once and write every slide in one
   pass. That pass is step 6 and comes **after** the answers, never instead
   of them.
2. **The deck.** One is open: work on that one. None: create it from the
   Slides type, titled with the plan's cover title.
3. **Find the design system "WPP Enterprise Solutions | MAP".** Do not ask
   which one. `list` with type "Design System", and match that exact title.
   Not found (another account, or a renamed system): say so in one line and
   build from `references/CORE.md`, this skill's downstream copy of the same
   rules, written as inline styles.
4. **Read it in this order**, before writing a slide:
   1. **`project/README.md`**: the eight rules, the canvas, colour and type
      on one page each, and *Building in Claude Design Slides* (faces,
      positions, floors, colour, dots, icons, photos, motion, what Slides
      cannot do). Where
      it describes the HTML pipeline (one self-contained file,
      `components/bundle.css`), that is the other surface: ignore it here.
   2. **The Elements cards** (Headline, Subhead, BodyCopy, Pill, StatCircle,
      FooterFurniture and the rest). Each ends with its inline-style recipe
      for Slides. Build every piece of text and every shape from them.
   3. **The four Fixed slides cards.** The cover, agenda, dividers and
      thank-you are built from their recipes, exactly.
   4. **The Layout catalogue** in the README, then the chosen layout's card
      and preview (below).

   `project/tokens.json` holds every value by name, for when a card names a
   token.
5. **Install it in the same call that sends the slides.** `files` entries
   copy it server-side: `project/ds/wpp-es-map/tokens.json` from its
   `project/tokens.json`, and one `project/ds/wpp-es-map/fonts/<File>` from
   its `project/fonts/<File>` for each of the four faces the README's
   *Faces* line names. Register each as its own face in `project/deck.json`
   `faces`, with the README's family names, `src` the installed file.
   `project/deck.json` `designSystems` gains `{"title": "WPP Enterprise
   Solutions | MAP", "namespace": "wpp-es-map", "artifact": "<its address
   from list>", "version": "<its version id>", "copiedAt": "<now>"}`.
6. **Write every slide in one pass**, then one publish, then the link.
   - **Assets.** Copy each image you place from the design system's asset
     groups into the deck (`from_url` the design system, `asset_ids` from
     its `assets` listing) and use the returned `url` verbatim. Never a
     `data:` URI. Icons are pasted inline, as the Icon card says.
   - **Page numbers are typed**, as `NN / total` (the FooterFurniture card).
     After adding, removing or moving a slide, retype every one.

## Choosing a layout

Pick from the design system's Layout catalogue by the shape of the argument:
traced layouts, measured off real MAP slides, before kit layouts, and where
a card's *Related* section names a pair, it says which to pick. Read the
card for when to use it, its capacity and what the consumer supplies; take
its positions and sizes from its preview. **Rebuild it in inline styles from
the Elements recipes. Never paste the preview's markup**: its classes and
`<style>` are dropped here, and pasted markup renders unstyled.

Over a layout's capacity, pick a lower-density layout or split the slide.
Never set the type smaller.

`canon/` and `references/SNIPPET-INDEX.md` are the HTML path's copies of the
same layouts; you do not need them here.

## Until the design system carries it

This Slides rule exists only on this page. It leaves once the design system
holds it.

- **Chart labels.** Fonts never load inside an `<svg>`, so a chart's labels
  are `<p>` elements pinned over it.

## What breaks if you are not careful

- **Pasted markup** from a preview or a template. Its `<style>` is dropped.
  Rebuild it.
- **An over-full box.** The page shrinks its text, which can take it under
  the brand's floors. Split the slide instead.
- **A pinned backdrop after the first flow child** hides the flow text. The
  dot svg goes first.
- **A negative offset** is clamped to 0. Bleeds belong in the svg.
- **`margin`** is a no-op: space with the parent's `gap`. `max-width` works
  on an element inside a `<div>` (the cards set it on a `<p>`); give a pinned
  element a `width`.
- **An SVG coloured by a `<style>` block** renders black once uploaded.
  Colour it by attribute.
- **Stylistic alternates** (the single-storey "a") are not in the subset.
  Accept the default glyphs.
