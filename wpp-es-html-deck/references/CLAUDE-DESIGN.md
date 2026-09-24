# Claude Design — the deck lives in the Slides artifact

**In Claude Design, or any session whose Artifact tool offers a Slides type,
the deck is an Artifact made from that type — never a separate `.html`
file.** This page is how the WPP Enterprise Solutions | MAP language is
written in that format.

The Slides type's own instructions, which you read when you open or create
the deck, govern the mechanics: `project/deck.json`, one
`project/slides/<id>.html` per slide, the calls. Where the two meet, the type
decides *how* a slide is written and this page decides *what it looks like*.

## What carries over, what does not

**Unchanged:** a gate before anything is built (here it is the question
card, below), the four design directions, archetype choice, canon-first
selection, the anti-sameness review, the house copy rules, and
non-negotiables 2–8.

**Does not exist here. Never run or write them:** `build_shell.py`,
`check_capacity.py`, `verify_deck.py`, screenshots, the contact sheet; a
standalone `.html` file (the artifact exports HTML, PDF and PPTX itself); CSS
classes, `<style>`, `var()`, base64 or `data:` images, the JS motion layer.

**G2 changes.** The type does not render-check slides and asks you not to,
so there is no seen-report. Deliver the link, name the two slides to look at
first, and offer to revise any slide by number or add an alternative beside
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
   pass. That pass is step 5 and comes **after** the answers, never instead
   of them.
2. **The deck.** One is open: work on that one. None: create it from the
   Slides type, titled with the plan's cover title.
3. **Design system: "WPP Enterprise Solutions | MAP".** Do not ask which
   one. This skill *is* that system. Find it with `list` (type "Design
   System") by that exact title, then read its `project/README.md` and
   `project/tokens.json`. Install it in the same call that sends the slides:
   `files` entries copy it server-side, `project/ds/wpp-es-map/tokens.json`
   from its `project/tokens.json`, and one `project/ds/wpp-es-map/fonts/<File>`
   from its `project/fonts/<File>` for each of the four faces under Type;
   `project/deck.json` `designSystems` gains `{"title": "WPP Enterprise
   Solutions | MAP", "namespace": "wpp-es-map", "artifact": "<its address
   from list>", "version": "<its version id>", "copiedAt": "<now>"}`.
   Its README describes the HTML pipeline too: where it says every deck is
   one self-contained HTML file, or to load `components/bundle.css`, that is
   the other surface. Ignore both here. Not found: say so and use the values
   on this page.
4. **Upload every asset you place**, logo, photo, illustration, motif,
   texture, from `assets/`. Use the returned `url` verbatim. Never a `data:`
   URI.
5. **Write every slide in one pass** from the recipes below, then one
   publish, then the link.

## Choosing a layout

Choose exactly as SKILL.md step 4 says: `canon/CATALOG.md` first, then
`references/SNIPPET-INDEX.md`. See each composition on `canon/PREVIEWS.png` (read it yourself, never post it),
then read the chosen `canon/templates/<id>.html` for its hierarchy, reading
order and geometry. **Rewrite it in inline styles. Never paste it.** Its
`<style>` block and classes are dropped here, and a pasted template renders
unstyled.

## Colour

| | hex | role |
|---|---|---|
| Navy | `#000050` | all type; dark grounds |
| Cream | `#FAFAF0` | every content slide's `background` |
| White | `#FFFFFF` | type on Navy and Orange 900; a rare ground |
| Orange 900 | `#6A290A` | fills; always takes White type |
| Orange 800 | `#D94E0E` | the eyebrow, the divider sub-label |
| Orange 700 | `#FF7800` | default dot colour, agenda numerals, a favourable stat |
| Orange 600 | `#F9BD5D` | dots and fills; never carries text |
| Orange 500 | `#FFF5CD` | the one tint ground |

Text is Navy or White, except the sanctioned orange moments in CORE §1.4.

## Type

**Four faces, one per weight.** The Slides format loads one font file per
face, at most four per deck, and its own rule is that a static font file with
one weight renders every weight at that weight. WPP ships as five static
files, so a single `WPP` face would set Thin display, Light headlines and
Medium labels all alike, and the hierarchy is gone. Register each weight as
its own face in `project/deck.json` `faces`, each `src` the font installed
with the design system (`project/ds/wpp-es-map/fonts/<File>`):

| `family` | key | file | carries |
|---|---|---|---|
| `WPP` | `wpp` | `WPP-Regular.woff2` | body, subhead, source, page number; the design system's own family name, so its Text styles still find a WPP face |
| `WPP Thin` | `wpp-thin` | `WPP-Thin.woff2` | statements, stat numerals, divider titles |
| `WPP Light` | `wpp-light` | `WPP-Light.woff2` | headlines, cover title, cover subheader |
| `WPP Medium` | `wpp-medium` | `WPP-Medium.woff2` | eyebrow, labels, pills, footer brand line |

**The face carries the weight, never `font-weight`.** Set `font-weight:400`
on every text element. `<h1>`–`<h3>` default to 600 here, and 600 on a
one-weight face is a synthesized fake bold.

**Bold 700 does not load.** It would be a fifth face. The footer brand line,
the only place the brand uses Bold, is set in `WPP Medium`. Never fake Bold
with `-webkit-text-stroke`.

| role | face | size · line-height · tracking |
|---|---|---|
| headline | `WPP Light` | 54px · 0.9 · −0.005em, sentence case, ≤2 lines |
| eyebrow | `WPP Medium` | 24px · 1 · 0.12em, caps, Orange 800 |
| subhead | `WPP` | 24px · 1.15 · 0.08em, caps |
| body | `WPP` | 26px · 1.32 (24px in columns, 22px in 4-up and boxes) |
| label | `WPP Medium` | 18px · 1 · 0.1em, caps |
| pill | `WPP Medium` | 16px · 1 · 0.08em, caps |
| statement, stat numerals | `WPP Thin` | 90px and up; `tokens.json` has the scale |
| footer brand | `WPP Medium` | 16px · 1 · 0.01em |

**The floors are the brand's, not the type's:** body 20px, other
informational text 16px, footer furniture 11px. The type recommends 24px
everywhere; footer furniture is frozen brand furniture and stays as
specified.

**No one-word title highlight here.** The brand's `.hl` is Medium on one
token. A `<span>` in this format takes only a colour, not a face, and `<b>`
is a fake bold on these faces. Leave the highlight out.

## The frame, on every content slide

The `<section>`: `background:#FAFAF0; color:#000050; font-family:'WPP',
sans-serif`. Pin the furniture and flow the content band.

| element | position |
|---|---|
| headline | `position:absolute; left:40px; top:73px`, with a `width` |
| eyebrow | `position:absolute; left:40px; top:177px` |
| content band | a pinned `<div>` at `left:40px; top:305px; width:1840px`: a flex column spaced by its `gap` |
| footer brand | `position:absolute; right:40px; bottom:34px` |
| page number | `position:absolute; right:40px; bottom:14px`, 11px, `opacity:0.7` |
| confidential | `position:absolute; left:40px; bottom:14px`, 11px, `opacity:0.7` |
| source | `position:absolute; left:40px; bottom:60px`, 12px, `opacity:0.75` |

The type's 128px margins are its default. The brand's 40px edge governs.

**Drop the eyebrow when the headline runs to two lines** (§7). At 64px, the
canon's measured bank size, a two-line headline reaches y 188 and would run
straight through the eyebrow at 177.

`margin` is a no-op in this format: space with the parent's `gap`.
`max-width` works on a `<div>` only, so give a `<p>` a `width`.

## Recipes

**Dots, dot fields and bleeds: one full-canvas `<svg>`, the section's first
child.** The type clamps a negative offset to 0, so a pinned circle cannot
bleed off the canvas. An svg the size of the slide crops its circles at its
own edge, and that crop is the bleed. Macro circles (Ø 60–110% of the canvas
width) always bleed. Flat fills only, Navy dots never behind text, each svg
52 KB or less.

```html
<svg aria-label="dot composition" width="1920" height="1080" viewBox="0 0 1920 1080"
     style="position:absolute; left:0; top:0; width:1920px; height:1080px">
  <circle cx="1880" cy="-60" r="520" fill="#FF7800"/>
  <circle cx="1500" cy="1180" r="300" fill="#F9BD5D"/>
</svg>
```

**Stat circle.** A sized `<div style="width:220px; height:220px;
border-radius:50%; background:#FF7800; display:flex; align-items:center;
justify-content:center">` holding a `<p>` in `WPP Thin`. Area is proportional to
value, so diameter goes with √value. Below 90px, an orange stat steps up to
`WPP Light`: Thin orange on Cream measures about 2.5:1.

**Pill.** `<p style="background:#000050; color:#FFFFFF; border-radius:999px;
padding:10px 26px">` in `WPP Medium` 16px caps. It is the only rounded element: no
rounded cards, no shadows, no gradients. The subset allows all three and the
brand forbids them.

**Duotone photo.** The brand's `.duo`, property for property:

```html
<div style="position:absolute; left:1260px; top:420px; width:560px; height:420px;
            overflow:hidden; background:#000050">
  <img src="/_blob/<id>" alt="…" style="width:560px; height:420px; object-fit:cover;
       filter:grayscale(1) contrast(1.08) brightness(1.04); mix-blend-mode:screen">
</div>
```

Media 200×200 or larger anchors to a canvas edge or a corner
(non-negotiable 8).

**Icons.** Never `<x-icon>`: its set is not the WPP suite. Paste the icon's
`<svg>` from `assets/icons/<family>.md`, one weight family per slide (§8.1),
and **replace `fill="currentColor"` with a hex**. An svg renders as an image
here and does not inherit the slide's colour.

**Charts.** `<svg>`, circle-first, flat fills. Labels are `<p>` pinned over
the svg, because fonts never load inside one.

**Halftone and motif art.** Upload the PNG (`assets/illustrations/`, or
`scripts/halftone.py` output) and place it as an `<img>`.

## Motion

`data-transition="fade"` on every section; `push` between chapters is fine.
The kit's choreography does not exist here, and `data-build-in` works on
pinned children only. With motion off, no build-ins.

## What breaks if you are not careful

- **A pasted canon or kit template.** Its `<style>` is dropped. Rewrite it.
- **An over-full box.** The page shrinks its text, which can take it under
  the brand's floors. Split the slide instead.
- **A pinned backdrop after the first flow child** hides the flow text. The
  dot svg goes first.
- **A negative offset** is clamped to 0. Bleeds belong in the svg.
- **Stylistic alternates** (the single-storey "a") are not in the subset.
  Accept the default glyphs.
