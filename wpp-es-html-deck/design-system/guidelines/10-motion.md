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

## In Claude Design Slides

The runtime layer above does not exist in Slides, and neither do its hooks. A deck there moves with the Slides
type's own transitions and build-ins:

- every slide takes `data-transition="fade"`, and `push` is fine between chapters;
- a build-in (`data-build-in`) works only on a slide's pinned children, the ones set `position:absolute`;
- with motion off, no build-ins.
