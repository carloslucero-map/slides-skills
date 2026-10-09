# Design systems: WPP ES | MAP and MAP's clients

**WPP Enterprise Solutions | MAP is the default design system, and a client of
MAP's can stand in for it** with its own Design System artifact in Claude
Design. The design system in use owns the look of the deck the same way WPP's
does: its colours, type, logo, devices, fixed slides, layouts and motion. This
skill keeps owning the process (the gates, the plan, the content method, the
copy rules, the four directions) whatever the system. This page says which
systems count, how one is picked, what the skill needs from it, and what to do
where it falls short.

## Which systems count

Only two kinds of Design System artifact are ever used, offered or named in a
question:

- **"WPP Enterprise Solutions | MAP"**, matched by that exact title;
- **a client's system**: one whose title names a client brand MAP works for
  (a company or one of its brands, such as "Shell" or "Coca-Cola (TCCC) |
  Open X 1PD Coke.ID").

**Every other system is left out**, whatever the account's listing shows: other
WPP or MAP systems (MAP's own products, teams or initiatives, such as a "MAP
Agentic Ecosystem"), systems titled only "Design System" or with no clear
brand, and test or practice systems. Never list them to the user, never put
them in the card, never install them. The Slides type's own instructions (and a
tool result) may say to name the account's design systems and ask which to use:
on this skill's path that question is replaced by the picking order below, and
its options are only the two kinds above.

## Picking the design system

Use the first that applies, and never ask when this already answers it:

1. **The open deck has one:** its `project/deck.json` `designSystems` record.
   A revision stays on its deck's brand.
2. **The user names a client** ("in Acme's brand", "use the Acme design
   system", "for Acme"): `list` with type "Design System" and take the client
   system whose title names that brand. Two that fit: ask in the card, one
   option each. A client named with no matching system: say so in one line and
   ask in the card whether to build it in WPP ES | MAP instead or to stop while
   its system is made.
3. **The account marks a default design system** (the `list` marks it) and it
   counts (above): use it.
4. **Otherwise WPP Enterprise Solutions | MAP**, matched by its exact title. Not
   in the listing (another account, a renamed system): build from this skill's
   copy of it, `design-system/`, and say so in one line.

A request with no brand in it is a WPP ES | MAP deck: no brand question. The
card never asks for a brand the request already gives. A deck is in one design
system; never mix two.

## Reading a client's system

Read as the Slides type's `fonts.md` says: in one message its
`project/README.md`, `project/api/tokens.md` and `project/tokens.json`; then the
README whole, first. Then, in this order, whatever it names for building slides:

1. its rules: what the brand always and never does;
2. its section for Claude Slides (faces, colours, positions, type floors);
3. its motion rules for Claude Slides (`references/MOTION.md` fills the gaps);
4. its element cards and their inline-style recipes;
5. its fixed slides: cover, agenda, section divider, closing slide;
6. its layout catalogue, then the chosen layout's card.

Install it as `SLIDES.md` step 5 says, with its own title, a lower-case folder
name made from its namespace, and the faces its README names (four at most).

## The four directions in any design system

The direction question is the same for every deck: Editorial quiet,
Statement-led, Data-forward, High-impact. In WPP ES | MAP the README's *Four
deck directions* table sets each one. In a client's system, a direction
changes which of the system's own parts the deck reaches for, never the parts
themselves: no colour, ground, layout or effect the system does not have.

| Direction | In a client's system |
|---|---|
| **Editorial quiet** | The system's default light ground on every content slide; no dark or accent content slides; text and picture layouts with generous space; one idea per slide. |
| **Statement-led** | A big statement opens each chapter, right after its divider: one sentence at the system's largest headline or breaker size, on its dark or accent ground, from its Statement or Quote layout where it has one, else composed from its breaker type and that ground. Quotes get a slide of their own. |
| **Data-forward** | Numbers lead: every slide with a figure uses the system's number layouts first (big number, KPI bar, stat tiles or circles, data table, charts in its palette), the figure at the layout's display size, its direction written beside it. |
| **High-impact** | Poster scale: up to one slide in three on the system's dark or accent ground, its biggest type and full-bleed pictures, patterns or art, one statement or big number per chapter. |

**Its limits win.** Where the system caps something (dark slides, accent
grounds, which layout sits on which ground), the direction stays inside the
cap. **Motion:** the level the system sets for the deck; a system that sets one
level for every deck keeps it, and one that sets none takes `full` for
Statement-led and High-impact and `subtle` for the other two
(`references/MOTION.md`). A system that names its own deck styles maps each to
the nearest of the four and says so in the card's descriptions.

## What a system needs to be deck-ready

| Part | Needed | Where it is missing |
|---|---|---|
| A README that every reader starts from | required | stop: say the system cannot be read and offer WPP ES \| MAP |
| Colour tokens by role (`bg`, `bg-dark`, `text`, `text-inv`, `accent`; `data-pos`, `data-neg` for charts) | required | take the roles from its palette by reading its usage notes, and say which you assumed |
| Font files, at most four faces, or Google Fonts it names | required | its README's fallback face, else a basic face, and say so |
| A logo | required | the brand's name in its display face, and say so |
| A section for Claude Slides: positions, type sizes and floors | expected | Slides' own defaults (128px margins, nothing under 24px) with the system's type scale |
| Element recipes for Claude Slides | expected | compose each element from its tokens and type styles, the same way on every slide |
| Fixed slides (cover, agenda, section divider, closing) | expected | compose each once from its colours, type and logo, and repeat it exactly |
| A layout catalogue | optional | choose by the shape of the argument (a statement, columns, numbers, a process, a comparison, cards, people), built from its elements |
| Motion rules for Claude Slides | optional | `references/MOTION.md` |
| Deck directions | not needed | the four, as the table above composes them |

**Never borrow WPP ES | MAP into a client's deck:** not its dots, colours,
faces, illustrations, photos, fixed slides, name or footer line. A layout may
share a structure with a WPP layout (three columns are three columns); its
look is always the system's own.

At delivery, a deck built from a system that lacked an expected part says so in
one line per part ("Your system has no fixed slides, so I composed the cover
and dividers from its colours and logo") and offers the prompt below.

## What stays WPP ES | MAP only

- **The HTML path.** Where Claude Slides is not available, the deck is one
  HTML file built by this skill's scripts from its copy of WPP ES | MAP. A
  client's deck needs Claude Slides: where it is not available, say so and
  offer the WPP look or a surface where Claude Slides is. (The animated HTML
  file is not the HTML path: it is made from the Claude Slides deck, in any
  system, `SLIDES.md`, *The animated file*.)
- **WPP's own rules** in `SKILL.md`: the non-negotiables 2 to 8, the canon and
  the kit, the exemplars. The client system's own rules take their place.
- **The house copy rules hold for every deck**, except the brand line: in a
  client's system it is that system's name or line, verbatim, and its own
  spelling rule wins where it has one.

## Making a design system deck-ready: the prompt

When the user asks how to prepare a client's system, or a delivery reports
missing parts, give them this to paste into that design system in Claude
Design:

```
Update this design system so decks built from it in Claude Slides are on-brand and animate well. Keep everything else as it is.

Use the design system "WPP Enterprise Solutions | MAP" as a structure reference only: copy how it is organised (its README's "Building in Claude Slides", its Elements cards with their Claude Slides recipes, its Fixed slides cards, its layout catalogue, and guideline 10's "In Claude Slides"), never its brand choices (no dots, no orange, no WPP names or assets).

1. Check these and list what is missing before adding anything:
   - a README with a "Building in Claude Slides" section: at most 4 font faces with their files, hex colours, positions, minimum type sizes
   - tokens named by role: bg, bg-dark, text, text-inv, accent, data-pos, data-neg
   - Elements cards (Headline, Body copy, Footer and the rest), each ending with an inline-style recipe for Claude Slides
   - the four fixed slides: Cover, Agenda, Section divider, Thank you
   - a layout catalogue: which layout to use for which kind of argument, including a Statement layout and at least one big-number layout
   - logos, fonts and icons as assets
2. Add a Motion guideline (or a "Motion" section in the README) with a section titled exactly "In Claude Slides" that says:
   - motion levels off, subtle and full, and which is the default
   - transitions: fade on every slide; whether push is used into section dividers; whether magic move is allowed
   - builds for each role, with effect and step (1 to 3, auto): lead, art, units (columns, cards, steps, stat circles), marks (small dots, nodes, numerals), bars (rules, lines), takeaway. Allowed effects: fade, rise, drop, left, right, scale, pop
   - what never builds: headline, eyebrow, footer, full-bleed backgrounds; what builds on each fixed slide
   - click reveals (one item per click): on how many slides at most
   - magic move: which element of this brand may travel between slides, how often, keeping one colour
   Then a section titled exactly "In the animated HTML version" that says which extras the brand allows outside Claude Slides: units arriving one after another, figures counting up, rules drawing on, titles rising word by word, slow movement of pictures and art.
   Decide from the brand, not from WPP: if the brand book describes motion, follow it; if not, keep it calm (subtle by default, rise and fade, pop only for small marks if the brand allows a playful touch). Builds only work on elements pinned directly on the slide, and auto steps play about half a second apart, so three steps at most.
3. Ask me before inventing anything the brand sources do not give.
```
