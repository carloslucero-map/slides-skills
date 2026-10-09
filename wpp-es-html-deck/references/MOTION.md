# Motion in Claude Slides, for any design system

Two sources, two jobs. **The design system in use decides how its decks move:**
its motion rules for Claude Slides (WPP Enterprise Solutions | MAP keeps them in
guideline 10, *In Claude Slides*). **This page holds what is true of Claude
Slides whatever the design system, and a quiet default for whatever a system
leaves unsaid.** Where the system speaks, it wins; this page fills the gaps and
never overrides it. It holds no brand values: no colour, face or shape.

## What Claude Slides can do

- **Transitions** go on the `<section>` and say how that slide leaves:
  `data-transition="fade"`, `"push"` or `"magic"`.
- **Builds** go on an element: `data-build-in="<effect> <step> auto"`. The
  effects are `fade`, `rise`, `drop`, `left`, `right`, `scale` and `pop`
  (`left` comes in from the left, `right` from the right; `pop` is the only one
  with a spring overshoot). Builds that share a step number play together;
  `auto` plays a step without a click; a step without `auto` waits for the
  presenter's click.
- **Only pinned elements move.** A build, or a magic-move `id`, works only on
  an element set `position:absolute` directly in the `<section>`; inside a
  `div` it is dropped. Whatever moves is pinned on the slide, and units that
  flow inside one band build together, as the band.
- **Auto steps chain slowly.** The first plays about 0.6s after the slide
  arrives and each next one about 0.5s later, so an entrance takes three auto
  steps at most.
- **Magic move:** the same `id` on a pinned element of two consecutive slides,
  and `data-transition="magic"` on the first. The element moves and resizes
  between them.
- **It plays only when the deck is presented.** The editor, the thumbnails and
  the PDF show every slide finished.
- **Never:** a build-out, an effect outside the list, or animation inside an
  `<x-embed>` (the deck's faces do not load there, and the exports flatten it).
  Counting numbers, word-by-word type, ambient motion and hover do not exist in
  Claude Slides and are never imitated in a slide. The animated HTML file adds
  them where the design system allows (`references/SLIDES.md`, *The animated
  file*).

## The roles

Every element on a slide plays one role. The roles are brand-neutral; a design
system may rename them (WPP ES | MAP calls them the motion hooks `m-lead`,
`m-art`, `m-unit`, `m-mark`, `m-bar`).

| Role | What it is | Default build | Step |
|---|---|---|---|
| Lead | the statement, lede or panel the slide opens with | `rise`; a panel anchored to an edge comes in from it, `left` or `right` | 1 |
| Art | an illustration, photo, motif or other media | `fade` | 1 |
| Units | the repeated block: columns, cards, steps, people, stat circles | `rise`, all in one step | 2 |
| Marks | small dots, timeline nodes, numerals | `pop` | 3 |
| Bars | rules and bars that read as drawn lines | `left` | 3 |
| Takeaway | the closing line of a slide | `rise`, after everything else | 3 |

**No build:** the headline and its eyebrow, the footer furniture, and any
full-bleed background, dot field or texture. They arrive with the slide, so a
slide never opens empty.

**Fixed slides:** on the cover, the section dividers and the closing slide,
only the type block builds, `rise 1 auto`; on the agenda, the block of chapter
rows, `rise 1 auto`, under a headline that stays put. Art, background shapes
and the logo are there from the start.

## The default, where the design system sets none

**The motion level** is the one the design system sets for the deck (by its
direction or style, where it has them; a system with one level for every deck
keeps it whatever the direction). A system that sets none: `full` for the
Statement-led and High-impact directions, `subtle` for Editorial quiet and
Data-forward. The user's words win: "more animation" means `full`, "no
animation" means `off`.

| Motion | Transitions | Builds | Magic move | Click reveals |
|---|---|---|---|---|
| `off` | `fade` | none | none | none |
| `subtle` | `fade` | steps 1 and 2, `rise` and `fade` only; the takeaway rises with the units | none | on one or two slides |
| `full` | `fade`, and `push` on the last slide of each chapter | steps 1 to 3, the roles above | at most two per deck | on one or two slides |

- **Click reveals:** on one or two slides of a deck, three to five parallel
  units, each pinned on its own, take a step each without `auto` and appear on
  the presenter's click; the lead may rise first (`rise 1 auto`) and the
  takeaway takes the last click.
- **Magic move** is for one element that clearly continues from one slide to
  the next: a stat circle that becomes the next slide's hero, or the system's
  own signature shape. It keeps one colour on both slides: colours never
  animate.
- `drop` and `scale` are never used by default; a design system may name them.

## A design system with its own rules

Read its motion rules for Claude Slides whole, before writing a slide, and use
them. Where they name an effect, a step, a level or a limit, they win. Where
they are silent on a role, use that role's row above. A system that rules
motion out takes `fade` transitions and no builds on every slide, whatever the
level.
