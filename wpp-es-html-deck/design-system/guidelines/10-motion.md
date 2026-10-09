# Motion

Motion is a **runtime layer the shell applies automatically** — templates need no markup changes for the basic
choreography. It is a registered per-deck choice of `full`, `subtle` or `off`, defaulting by direction to full for
high-impact and statement-led decks and subtle for editorial-quiet and data-forward, and it is auto-disabled for
`prefers-reduced-motion`, for print, and for headless capture, so the verifier and exported PDFs always see the
static deck.

Nothing here is tokenized: the design-system token format carries no motion family, so this page is the record.

## Doctrine: elements move, colours never do

Only the movement channels animate — the individual `translate` and `scale` properties plus `opacity`.
Keyframes never touch the `transform` shorthand, because kit elements are positioned with base transforms and
would teleport; `transform` belongs to the pointer parallax and the hover offsets.

Fills stay flat. No colour or hue animation, no blur, no shadows in motion. **Restraint carries the brand;
choreography carries the energy.** No deck invents its own animations or easing: a new motion is a change to the
system, recorded here.

## Entrance choreography

On each slide activation the shell staggers the kit in reading order: panels wipe in from their edge, headlines
and blocks rise 34px, decorative dots pop with a spring overshoot — `cubic-bezier(.34, 1.56, .4, 1)`, the one
sanctioned overshoot in the system — rulers and bars draw themselves, stems grow, motifs float in, ghost
numerals drift in from the right. Stagger 75ms, capped around 1s; durations 0.38–1.05s. Numerals count up. Big Statements, Big Quotes, divider
titles and the cover title rise word by word. Step-by-step reveals go on parallel blocks, three to five per
slide at most; with motion off, or in print, everything shows.

At full motion, dots breathe and motif art floats; ambient motion never touches text. A 3px Orange 700 progress
line along the bottom edge grows as the deck advances: the one exception to "no accent bars", hidden in print
and with motion off.

## A template must declare its motion roles

The choreography is driven by a closed list of selectors, and every entry in it is a kit class. The 25 canon
templates invent 432 class names of their own, so when they shipped, twelve of them animated nothing but the
slide fade while kit slides moved — decks built mostly from canon looked dead, with no error anywhere. It was
found by opening a real deck and noticing.

The fix is five generic hooks a template opts into:

| Hook | Motion | Goes on |
|---|---|---|
| `m-lead` | rise | The statement, lede or panel the slide opens with |
| `m-art` | float-in | A motif or media host |
| `m-unit` | rise, staggered | *The* repeated block — column, band, card, step, person |
| `m-mark` | pop | Plotted dots, ring nodes, numerals, rail chips |
| `m-bar` | draw | Rules, bands and bars that read as drawn lines |

Put the hook on the **outermost repeated element**, never on its children: the stagger index counts matched
elements, so hooking the leaves gives forty beats where the design wants five.

The preview cards in this system render the static state — the motion layer is not loaded here.

## In Claude Slides

The runtime layer above does not exist in Slides, and neither do its hooks. A deck there moves with the Slides
type's own transitions and builds, which play only when the deck is presented; everywhere else every slide shows
finished. The vocabulary below is closed: no other effect, no build-out, and no animation inside an `<x-embed>`
(the brand faces do not load there, and the exports flatten it).

**Transitions** go on the `<section>` and say how that slide leaves it (`data-transition`):

- `fade` on every slide;
- `push` on the last slide of a chapter, so the deck turns the page into the divider (full motion only);
- `magic` on a slide whose dot carries into the next one (*Magic move*, below).

**Builds** (`data-build-in="<effect> <step> auto"`) work only on a slide's pinned children: elements set
`position:absolute` directly in the `<section>`. Inside a `div` a build is dropped, so units that flow inside one
band build together, as the band. Builds that share a step number play together, and `auto` plays a step without
a click. Auto steps chain: the first plays 0.6s after the slide arrives and each next one about 0.5s later, so an
entrance takes three steps at most. The hooks map onto them:

| Hook | In Slides | Step |
|---|---|---|
| `m-lead`, the statement, lede or panel the slide opens with | `rise`; a panel anchored to an edge comes in from it, `left` or `right` | 1 |
| `m-art`, a motif or media host | `fade`; a ghost numeral `right` | 1 |
| `m-unit`, the repeated block: a column, card, step, person or stat circle | `rise`, every unit in the one step | 2 |
| `m-mark`, a small pinned dot, a timeline node or a numeral | `pop`, the one effect with a spring overshoot | 3 |
| `m-bar`, a pinned rule or bar | `left`, so it reads as drawn | 3 |
| The takeaway | `rise`, after everything else | 3 |

Stat circles rise with the units, as they do in the HTML deck; only small marks pop, so the spring stays an
accent. The takeaway rises with the units at subtle motion, which stops at step 2, and on a click-reveal slide it
takes its own click, after the last unit.

The headline and its eyebrow, the footer furniture and a full-bleed dot field take no build: they arrive with
the slide, so a slide never opens empty. On the cover, the dividers and the thank-you slide only the type block
builds, `rise 1 auto`; on the agenda, the block of chapter rows, `rise 1 auto`, under a headline that stays put.
The art, the dots and the logo badge are there from the start.

| Motion | Transitions | Builds | Magic move | Click reveals |
|---|---|---|---|---|
| `off` | `fade` | none | none | none |
| `subtle` | `fade` | steps 1 and 2, `rise` and `fade` only | none | on one or two slides |
| `full` | `fade`, and `push` into each divider | steps 1 to 3, every effect above | at most two per deck | on one or two slides |

**Click reveals** are the HTML deck's fragments. On one or two slides of a deck, three to five parallel units, each
pinned on its own, take a step each without `auto` (`rise 2`, `rise 3`, …) and appear on the presenter's click;
the slide's lead can still rise on its own first (`rise 1 auto`).

**Magic move** is the dot travelling. A circle pinned on one slide (a `div` with `border-radius:50%`, or a stat
circle) carries the same `id` as a circle pinned on the next, and the first slide takes `data-transition="magic"`:
the dot moves and grows from one to the other. Use it where the second slide zooms into the first, such as a stat
circle that becomes the next slide's hero. Both circles keep one colour, because colours never move.

What the HTML deck does and Slides cannot is never imitated in a Slides deck: no counting numerals, no word-by-word
type, no breathing dots or floating art, no progress line, no hover. They belong to the animated HTML version, below.

## In the animated HTML version

When someone asks for it, the `slides-builder` skill makes the animated version beside the Claude Slides deck (README,
rule 8): one self-contained HTML file made from that deck's own slides, presented from a browser. It plays the deck's
transitions and builds as above, magic move as a real morph, and adds what Slides cannot do. This system allows every
extra:

| Extra | What it does | Allowed |
|---|---|---|
| `stagger` | Units that share a build step arrive one after another, about 90ms apart | yes |
| `count` | Display figures count up from zero as they appear | yes |
| `draw` | Rules and bars that build draw themselves on | yes |
| `words` | Titles that rise in rise word by word | yes |
| `drift` | Large dot fields and art move slowly while the slide shows; full-bleed pictures take a slow Ken Burns | yes |

The doctrine still holds: colours never move, and nothing ambient touches text. With reduced motion, in print, or
with `?motion=off`, the file shows every slide finished.
