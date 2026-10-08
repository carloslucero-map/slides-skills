# The Claude Slides path — the deck is built in Claude Slides

**Wherever Claude can make a Claude Slides deck, the deck is an Artifact made
from the Slides type — never a separate `.html` file.** That is any session
whose Artifact tool offers a Slides type: a chat in claude.ai or the desktop
app with Claude Slides on, Claude Design, Claude Code. A deck is open, or
`quickstart` with intent `slides` returns the type. This is the default; the
standalone HTML file is only for where Claude Slides is not available, and for
the animated HTML deck when it is asked for or picked (`SKILL.md`, *Where the
deck goes*).

Three sources, three jobs:

- **The design system in use** decides what the deck looks like: every
  colour, face, size and position, every element, fixed slide and layout. It
  is "WPP Enterprise Solutions | MAP" unless step 3 picks another, such as a
  client's (`references/DESIGN-SYSTEMS.md`).
- **The Slides type's own instructions**, which you read when you open or
  create the deck, decide how a slide is written: `project/deck.json`, one
  `project/slides/<id>.html` per slide, the calls.
- **This page** decides how the deck gets made here: the gate, the reading
  order and the install.

This page holds no brand values. When you need a hex, a size or a position,
it is in the design system.

## What carries over, what does not

**Unchanged:** a gate before anything is built (here it is the question
card, below), the design directions, archetype choice, traced-first
layout selection, the anti-sameness review, the house copy rules, and
non-negotiables 2–8. In a deck in another design system, that system's own
rules, directions and layouts take the place of WPP's
(`references/DESIGN-SYSTEMS.md`).

**Does not exist here. Never run or write them:** `build_shell.py`,
`check_capacity.py`, `verify_deck.py`, screenshots, the contact sheet; a
standalone `.html` file (the artifact exports HTML, PDF and PPTX itself); CSS
classes, `<style>`, `var()`, base64 or `data:` images, the JS motion layer.
A deck here moves with Slides' own transitions and builds, as the design
system sets them, and `references/MOTION.md` where it sets none (step 6).

**G2 changes.** The type does not render-check slides and asks you not to,
so there is no seen-report. Deliver the link, name the two slides to look at
first, say which headline highlights were dropped (the Headline card says
when), and offer to revise any slide by number or add an alternative beside
it. A deck in another design system also names the system it used and, one
line each, any part that system lacked and how it was filled
(`references/DESIGN-SYSTEMS.md`).

## Asking: the question card, never a slide table

Where the session has the **`AskUserQuestion` tool** (Claude Design and Claude
Code do), questions show as a card in the chat box. A question typed as prose
there — a slide table ending in "reply 1/2/3/4" — arrives as an ordinary
message nobody can click. So G0 and G1 are **one `AskUserQuestion` call**,
before anything is written:

- **At most four questions**, the call tagged
  `"metadata": {"source": "artifact-questions"}`.
- **The brand, only when step 3 cannot tell** (two systems fit the name the
  user gave, or the brand they named has no system): one option per system,
  plus WPP Enterprise Solutions | MAP, `multiSelect: false`.
- **The design direction, always** (unless the user already named one), with
  `multiSelect: false` and your content-signal pick first, marked
  "(Recommended)". These are WPP ES | MAP's; another design system's own
  directions, if it has any, in its own words, and no direction question if
  it has none:

  | label | description |
  |---|---|
  | Editorial quiet | Spacious, cream, no dark slides |
  | Statement-led | A big statement opens each chapter |
  | Data-forward | Numbers lead: stat circles, charts |
  | High-impact | Poster scale, up to 1 in 3 dark |

- **The format, for a special deck in WPP Enterprise Solutions | MAP only**
  (the one design system with an animated HTML deck): a pitch, a keynote, a
  launch, an event or award moment, a talk on a stage, or a user who asks for
  animation. `multiSelect: false`, with the Claude Slides deck first and
  marked "(Recommended)" unless the user asked for animation or the deck is
  presented on a stage, when the animated deck goes first instead:

  | label | description |
  |---|---|
  | Claude Slides deck | Editable here, exports to PowerPoint |
  | Animated HTML deck | Counting numbers, living dots; one browser file |

  Any other deck gets no format question, and a user who names the animated
  version gets it without one. A deck in any other design system has no
  animated HTML version: say so in one line if one is asked for, and build the
  Claude Slides deck at full motion.
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

**No `AskUserQuestion` tool in this session?** Ask the same questions in one
short message instead: the two lines of prose, then each question numbered
with its options lettered and your recommended option first, and end the
turn. Still no slide table: the deck is the plan.

**The waivers still hold.** An explicit "just build it", or nobody there to
answer: no card, the recommended direction, assumptions in one line. An
approved `deck-builder` file: the card holds only the direction, and the
format for a special deck.

## No slide images in the chat

**The draft is the deck in the editor.** Never post a slide, an exemplar, a
preview, a screenshot, a contact sheet or an A/B sheet as an image in the
chat: not to choose a direction, not to show progress, not to offer an
alternative. The four exemplar PNGs stay unopened on the Claude Slides path; each
direction's description in the card carries the difference instead. An
alternative for a slide is a second slide right after it, id `<id>-alt`,
which the user keeps or deletes in the editor.

## Steps

1. **Ask with the card** (above), then wait for the answers. The Slides
   type's own instructions say to decide once and write every slide in one
   pass. That pass is step 6 and comes **after** the answers, never instead
   of them. If the answer is the animated HTML deck, this page ends here:
   build it by `SKILL.md` steps 3–6, the card's answers standing as the
   approved plan.
2. **The deck.** One is open: work on that one. None: create it from the
   Slides type, titled with the plan's cover title.
3. **Pick the design system** as `references/DESIGN-SYSTEMS.md` says: the
   open deck's own, else the one the user names, else the account's marked
   default, else "WPP Enterprise Solutions | MAP" (`list` with type "Design
   System", exact title; not found: say so in one line and build from this
   skill's copy of it, `design-system/`, its README, guidelines and cards with
   the same Slides recipes, written as inline styles). Do not ask which one
   when the request already says.
4. **Read it before writing a slide.** Another design system: in the order
   `references/DESIGN-SYSTEMS.md` gives, and where it lacks a part, that
   page's table says what to do. WPP ES | MAP, in this order:
   1. **`project/README.md`**: the eight rules, the canvas, colour and type
      on one page each, and *Building in Claude Slides* (faces,
      positions, floors, colour, dots, icons, photos, motion, what Slides
      cannot do). Where
      it describes the HTML pipeline (one self-contained file,
      `components/bundle.css`), that is the HTML path: ignore it here.
   2. **The guidelines** (`project/guidelines/`): 01 to 04 and 06 before any
      slide (colour, typography, grid and composition, the dot system, slide
      furniture), then 07 to 09 when the deck has icons, imagery or charts,
      and the *In Claude Slides* section of 10, its motion, unless motion is
      off. The
      layout laws in 03 hold here too: check them by eye. Where a guideline
      names the HTML deck's classes or its verifier, that is the HTML path.
   3. **The Elements cards** (Headline, Subhead, BodyCopy, Pill, StatCircle,
      FooterFurniture and the rest). Each ends with its inline-style recipe
      for Slides. Build every piece of text and every shape from them.
   4. **The four Fixed slides cards.** The cover, agenda, dividers and
      thank-you are built from their recipes, exactly.
   5. **The Layout catalogue** in the README, then the chosen layout's card
      and preview (below).

   `project/tokens.json` holds every value by name, for when a card names a
   token.
5. **Install it in the same call that sends the slides.** `files` entries
   copy it server-side: `project/ds/<folder>/tokens.json` from its
   `project/tokens.json`, and one `project/ds/<folder>/fonts/<File>` from its
   `project/fonts/<File>` for each face its README names (four at most; WPP
   ES | MAP's are the four on its *Faces* line). `<folder>` is a lower-case
   name made from the system's namespace by the Slides type's rule
   (`deck-files.md`); WPP ES | MAP's is `wpp-es-map`, and a deck that already
   records a system keeps that record's folder. Register each face
   as its own entry in `project/deck.json` `faces`, with the README's family
   names, `src` the installed file. `project/deck.json` `designSystems` gains
   `{"title": "<its title>", "namespace": "<folder>", "artifact": "<its
   address from list>", "version": "<its version id>", "copiedAt": "<now>"}`.
6. **Write every slide in one pass**, then one publish, then the link.
   - **Assets.** Copy each image you place from the design system's asset
     groups into the deck (`from_url` the design system, `asset_ids` from
     its `assets` listing) and use the returned `url` verbatim. Never a
     `data:` URI. Icons are pasted inline, as the system's Icon card says.
   - **Page numbers are typed**, as `NN / total` (the FooterFurniture card).
     After adding, removing or moving a slide, retype every one.
   - **Motion.** Every slide takes its transition and builds from the
     design system's motion rules for Claude Slides (in WPP ES | MAP,
     guideline 10, *In Claude Slides*), at the motion level the system sets
     for the deck's direction, unless the user chose another. Whatever the
     system leaves unsaid, and all of it for a system that sets no motion,
     comes from **`references/MOTION.md`**: what Slides can do, the roles and
     the quiet default. Decide it per slide as you write it: what builds is
     pinned directly on the slide, the headline and the furniture never
     build, and at full motion name the one or two magic-move pairs before
     writing the slides that hold them.

## Choosing a layout

Pick from the design system's Layout catalogue by the shape of the argument
(a system with none: `references/DESIGN-SYSTEMS.md`). In WPP ES | MAP,
traced layouts, measured off real MAP slides, come before kit layouts, and where
a card's *Related* section names a pair, it says which to pick. Read the
card for when to use it, its capacity and what the consumer supplies; take
its positions and sizes from its preview. **Rebuild it in inline styles from
the Elements recipes. Never paste the preview's markup**: its classes and
`<style>` are dropped here, and pasted markup renders unstyled.

Over a layout's capacity, pick a lower-density layout or split the slide.
Never set the type smaller.

`canon/` and `references/SNIPPET-INDEX.md` are the HTML path's copies of the
same layouts; you do not need them here.

## What breaks if you are not careful

- **Pasted markup** from a preview or a template. Its `<style>` is dropped.
  Rebuild it.
- **An over-full box.** The page shrinks its text, which can take it under
  the brand's floors. Split the slide instead.
- **A pinned backdrop after the first flow child** hides the flow text. The
  background art (in WPP ES | MAP, the dot svg) goes first.
- **A negative offset** is clamped to 0. Bleeds belong in the svg.
- **A build on a flow child** (or anything inside a `div`) is dropped, and so
  is a magic-move `id`. Pin what moves directly on the slide.
- **`margin`** is a no-op: space with the parent's `gap`. `max-width` works
  on an element inside a `<div>` (the cards set it on a `<p>`); give a pinned
  element a `width`.
- **An SVG coloured by a `<style>` block** renders black once uploaded.
  Colour it by attribute.
- **Stylistic alternates** (the single-storey "a") are not in the subset.
  Accept the default glyphs.
