The visual language of the WPP Enterprise Solutions | MAP presentation system: Navy, Cream and an orange ramp; WPP Sans in five weights; and the dot, the device everything else in the system is built from. Treat the system as internal: the fonts, logos and illustrations are proprietary to WPP, and the photographs have no verified licence.

## The eight things that matter

1. **The dot is the most important device in the storytelling.** Backgrounds, illustrations, icons, charts and bullets are all built from circles. When in doubt, express it with a dot.
2. **Navy is the main colour. Avoid making things too orange.** `accent` brings depth; `wpp-navy` carries the brand. Cream and White are always used *in excess of* Navy across a deck.
3. **Quiet, editorial, lots of air.** Thin and Light type, generous whitespace, flat colour. No gradients, no drop shadows, no decorative rules, no accent bars (the HTML deck's progress line is the one exception; see *Motion*). The drama comes from scale contrast (huge thin type against macro dots), never from ornament.
4. **Text is Navy or White.** The sanctioned orange text moments are listed below and nowhere else. Never orange body copy, headlines or bullets. Title emphasis is weight, never colour.
5. **Charts are circles.** Flat fills from the primary and secondary palettes, sized by area.
6. **One warm background, used consistently.** `wpp-cream` on every content slide. Mixing Cream and pure White across a deck is the single most common consistency error in this system.
7. **The name is "WPP Enterprise Solutions | MAP".** Never "VML MAP", never "VMLMAP".
8. **A deck lives where it is presented.** In Claude Design, build a deck inside the Slides artifact with this system installed, never as a separate HTML file, following *Building in Claude Design Slides* below. Elsewhere, the `wpp-es-html-deck` skill writes one self-contained HTML file with fonts, logos, icons and imagery embedded.

## The canvas

16:9 at **1920 × 1080**. The PowerPoint equivalent is 960 × 540 pt, so **pt × 2 = px**.

Everything snaps to the **40px module** (`grid`). The content edge is `m-edge`, 40px; running copy may take the deeper `m-text`. The headline sits at `headline-y`, the eyebrow at `eyebrow-y`, and the content band runs from `band-top` to `band-bottom`. On the 1800px column grid, columns measure 860px at 2-up and about 547px at 3-up with a `gutter`, 408px at 4-up with `gutter-tight`.

Whitespace must be *shaped*: asymmetric, counterweighted by the composition, never leftover. Leftover whitespace below y = 700 is the most common rejected-deck signature. Big Statement and divider slides leave 40–60% of the canvas empty on purpose; that air is registered.

## Colour, in one page

| Role | Token | Rule |
|---|---|---|
| Default ground | `bg` → `wpp-cream` | Every content slide. No exceptions worth making. |
| Dark moment | `bg-dark` → `wpp-navy` | Dividers, outros, statement slides. Punctuation, never the base, and only as often as the deck's direction allows (*Colour*). |
| Accent ground | `bg-tint` → `orange-500` | Occasional accent moment only. |
| Rare ground | `bg-alt` → `wpp-white` | A full-bleed halftone field or a single gallery moment. Not a casual alternate to Cream. |
| Type | `text` / `text-inv` | Navy and White set all type. |
| Accents | `accent` and the orange ramp | Dots, shapes, chart fills. |

**Orange 600 never carries text.** Body copy only ever sits on White, Cream or Orange 500. Orange 900 and Navy always take White type.

The sanctioned orange text moments, in full: the cover month line (`orange-700`), agenda numerals (`orange-700`), the divider sub-label (`orange-800`, or `orange-600` on the navy-full colourway), the content eyebrow (`orange-800`), data-viz accents such as process step numerals (`orange-800`), the favourable stat `data-pos`, a ghost numeral (`orange-500` on Cream), and, in the traced layouts only, the eyebrows, labels and numerals they were measured with (`orange-700`). That is the whole list.

## Type, in one page

**WPP Sans** in exactly five shipped weights: Thin 100, Light 300, Regular 400, Medium 500, Bold 700. No Black, no italics; never synthesise a missing weight. Where the medium allows it, turn on stylistic alternates for the single-storey "a" (`font-feature-settings: "salt" 1`).

The hierarchy contract: **headlines are Light, running text is Regular.** Every tier differs from its neighbour by **weight or case, not just size**: Thin display → Light headline → Regular-caps subhead → Regular body → Medium-caps label.

Bold exists for the footer brand line only. It is not a body-emphasis weight, and there is no bold run inside body copy anywhere in this system.

Each text style names its face rather than a weight: `thin` (WPP Thin), `light` (WPP Light), `sans` (WPP, Regular) and `medium` (WPP Medium), all at weight 400, so the Text style menus in Slides and Design pick the right file. The footer brand line alone stays on `sans` at 700.

Floors: **20px** for body copy and any other running text, **16px** for the fine-print roles the BodyCopy card lists, **11px** for footer furniture only (frozen). If it does not fit at its floor, the slide has too much content.

## Components: elements, fixed slides and layouts

The components come in three kinds, and they do different jobs.

**Elements** (the *Elements* group) are the true components: `Headline`, `Subhead`, `BodyCopy`, `ColumnLabel`, `Pill`, `DotBullet`, `Takeaway`, `CardBox`, `CardLink`, `StatCircle`, `KpiRow`, `DataTable`, `LogoRow`, `ScreenshotFrame`, `Photo`, `Icon`, `DotField` and `FooterFurniture`. They hold the rules that must be identical on every slide, and each card ends with an exact inline-style recipe for Claude Design Slides. Build every slide from them.

**Fixed slides** (the *Fixed slides* group) are the four slides that look the same in every deck: `CoverSlide`, `AgendaSlide`, `DividerSlide` and `ThankYouSlide`. Every deck opens on the cover and closes on the thank-you slide; the agenda follows the cover when the deck has chapters, and a divider opens each chapter. A deck with a single chapter has no agenda and no dividers. Build them exactly from their cards, never from a layout.

**Layouts** (the *Layouts · …* groups) are 76 whole-slide compositions, marked as showcase pages: 25 traced from real bank slides with measured geometry, and 51 from the deck kit. They are patterns to rebuild, not markup to paste. Pick one by the shape of the argument, not its look, from the catalogue below: layouts of the same archetype differ by density, not decoration. Its *When to use it* is quoted from its card. Read the card for composition and capacity, then rebuild the layout from the elements. Over a layout's maximum, pick a lower-density layout or split the slide; never shrink the type. Where a traced and a kit layout cover similar ground both stay, and each card's *Related* section says which to pick.

## Building in Claude Design Slides

A slide in Slides takes inline styles only (no classes, no stylesheet, no scripts, no `var()`), so `components/bundle.css` does not apply there. Where this system and Slides' own defaults differ, this system wins.

- **Faces.** Install `WPP-Regular`, `WPP-Thin`, `WPP-Light` and `WPP-Medium` as the faces `WPP`, `WPP Thin`, `WPP Light` and `WPP Medium`, the four a deck can load. Choose the weight by face and set `font-weight:400` on every text element, headings included, since they default to 600. The footer brand line is set in `WPP Medium`, because Bold would be a fifth face.
- **Positions.** Place by this system's tokens, not Slides' 128px margins or its 24px footer row: the headline at `m-edge` × `headline-y`, the content band pinned as a `div` from `band-top` to `band-bottom` (305px is deeper than a slide's padding allows), and the furniture where the FooterFurniture card puts it. A layout's measured positions win over these defaults.
- **Floors.** This system's floors hold: 20px body, 16px for the BodyCopy card's fine print, 11px furniture only. Slides' 24px suggestion does not apply.
- **Colour.** Write the hex values from the tokens: `#000050` Navy, `#FAFAF0` Cream, `#FF7800` Orange 700, and so on.
- **Dots.** Draw a dot field as one full-bleed `<svg>` listed first on the slide, so cropped circles clip at the canvas edge (Slides clamps negative offsets). Single dots and stat circles are `div`s with `border-radius:50%`.
- **Icons.** Paste the brand icon's SVG inline and replace `currentColor` with the hex ink; as an `<img>` it renders black. Never use Slides' own `x-icon` set.
- **Photos.** Set every photo from the Photo card, which says which photos take the navy duotone and how.
- **Motion.** Slides' own transitions and build-ins only, as the Motion guideline sets them for Slides; the HTML deck's choreography does not exist here.
- **What Slides cannot do.** Stylistic alternates, so the single-storey "a" is lost; a change of typeface inside a line, so the headline highlight needs its own text block or is dropped, never faked with `<b>`; and more than one typeface per table.

## Layout catalogue

Every deck: `CoverSlide` first, `AgendaSlide` when there are chapters, a `DividerSlide` before each chapter, `ThankYouSlide` last. Between them, pick each content slide from these families.

**Narrative.** A statement, a quote, or an argument carried by prose.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `NarrativeStatementField` (traced) | One sentence marking the turn between two arguments. A breath, not a point. | about 60 |
| `NarrativePanelModel` (traced) | A position needing three or four hundred words, with the model it rests on visible alongside. | about 1180 |
| `NarrativeTensionSpectrum` (traced) | Tensions rather than choices — and the evidence to say WHERE something sits between two poles. | about 1180 |
| `StatementQuoteV1` | One short statement beside a motif. | 32 ideal, 43 max |
| `StatementQuoteV2` | A client or leader quote. | 80 ideal, 108 max |
| `StatementQuoteV2b` | One short statement beside a halftone image. | 37 ideal, 49 max |
| `StatementQuoteV3` | A high-impact poster line, used rarely. | 56 ideal, 75 max |
| `SplitsV2` | A headline argument beside a colour block. | 295 ideal, 398 max |
| `SplitsV3` | A short message beside a motif. | 153 ideal, 206 max |

**Enumeration.** Parallel items shown as a set.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `EnumIndex2col` (traced) | Ten to sixteen offerings have to be seen as a whole, where the breadth is the point rather than any one item. | about 620 |
| `EnumIntroGrid5` (traced) | One principle, then four to six named instances of it — and the principle needs more room than any instance. | about 1080 |
| `EnumNumbered4` (traced) | Three or four named stages, each needing a sentence of substance rather than a label. | about 505 |
| `EnumStageBento4` (traced) | Four stages of a transformation, each with a screenshot of what was built and what changed. | about 620 |
| `EnumTierColumns3` (traced) | The same problem appears at three levels of maturity, and each level has a client quote that proves it. | about 840 |
| `ColumnsV1` | Three principles with room to explain each. | 633 ideal, 854 max |
| `ColumnsV2` | Four short parallel points. | 188 ideal, 253 max |
| `ColumnsV3` | Two ideas plus a row of tags. | 208 ideal, 280 max |
| `ColumnsV4` | Three capabilities or verbs, each with an icon. | 254 ideal, 342 max |
| `ColumnsV5` | Three or four numbered points, a line each. | 381 ideal, 514 max |
| `CardsV1` | Four parallel topics with detail held back. | 645 ideal, 870 max |
| `CardsV2` | Three offers or options, each with a next step. | 497 ideal, 670 max |
| `CardsV3` | Three examples that each need an image. | 379 ideal, 511 max |
| `CardsV4` | Six items as a grid of tiles. | 429 ideal, 579 max |
| `BoxesV1` | Three or four parallel points that land on one takeaway. | 329 ideal, 444 max |
| `BoxesV2` | A few related items that belong together. | 214 ideal, 288 max |

**Sequence.** Steps, phases and time.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `SeqPhaseColumns4` (traced) | Three or four phases with long activity lists, and it matters which phase the client is in now. | about 1420 |
| `SeqPhasePanels3` (traced) | Work runs in three named phases with different characters, and each deserves the weight of a full-height panel. | about 1280 |
| `SeqStepsPanels5` (traced) | A method of four or five stages where each stage has real activities and deliverables to name. | about 1450 |
| `BoxesV3` | A short sequence of three or four phrases. | 162 ideal, 218 max |
| `ProcessTimelineV1` | A process of short steps that lands on a takeaway. | 432 ideal, 583 max |
| `ProcessTimelineV2` | Dated milestones along a line. | 226 ideal, 305 max |
| `ProcessTimelineV3` | Parallel workstreams over time. | 125 ideal, 168 max |
| `ProcessTimelineV4` | A simple timeline of a few points. | 126 ideal, 170 max |
| `ProcessTimelineV6` | Phases with detailed steps on one board. | 670 ideal, 904 max |

**Quantitative.** Numbers that make the point.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `QuantScoreCircles` (traced) | Three or four scores on a common scale, shown as derived from named inputs rather than asserted. | about 760 |
| `QuantStatGrid5` (traced) | A claim needing five pieces of quantitative proof, where the claim is what the room should leave with. | about 720 |
| `StatsV1` | Four headline numbers in a row. | 300 ideal, 405 max |
| `StatsV2` | One central number with proof around it. | 311 ideal, 419 max |
| `StatsV3` | A few values compared by circle area. | 99 ideal, 133 max |
| `StatsV4` | A compact row of KPIs. | 95 ideal, 128 max |
| `StatsV5` | KPIs grouped by category. | 203 ideal, 274 max |
| `StatsV6` | Two programmes and what they share. | 515 ideal, 695 max |
| `StatsV7` | Four values stepping up in intensity. | 161 ideal, 217 max |
| `ChartsV1` | One hero measure with supporting figures. | 184 ideal, 248 max |
| `ChartsV2` | A few values compared as bars. | 58 ideal, 78 max |
| `ChartsV3` | Small tabular data, a few rows. | 120 ideal, 162 max |
| `SplitsV1` | One lead message plus its KPIs. | 309 ideal, 417 max |

**Comparison.** Options set against each other.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `CompPriorityGrid` (traced) | Fifteen to twenty-five candidates where the scoring is a judgement and the bands are what gets argued about. | about 560 |
| `CompPriorityScatter` (traced) | Ten to thirty-five candidates to prioritise, where relative position matters more than which box they fall in. | about 620 |
| `ComparisonV1` | Before and after, or two approaches. | 287 ideal, 387 max |
| `ComparisonV2` | Where two or three sets overlap. | 223 ideal, 301 max |

**Relational.** Parts inside a system, and how they connect.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `RelHubRings4` (traced) | Four capabilities that live INSIDE one system rather than beside each other, with prose to land the claim. | about 560 |
| `RelLayeredStack` (traced) | An offer with stacked layers, where one layer is plainly where all the substance lives. | about 1320 |
| `RelStageSplit` (traced) | What the client sees and what runs underneath, shown as one system rather than two. | about 720 |
| `RelTaxonomyBands` (traced) | Three to five named classes that between them exhaust a space. | about 560 |
| `OrbitV1` | A hub and four parts, lightly. | 130 ideal, 175 max |
| `OrbitV2` | A hub with its parts, plus context. | 310 ideal, 418 max |
| `OrbitV3` | Three or four overlapping ideas. | 358 ideal, 483 max |
| `ProcessTimelineV5` | An ecosystem of players across zones. | 458 ideal, 618 max |

**Media.** A photo, screenshot or visual leads.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `MediaAnnotatedCallouts4` (traced) | A screenshot, diagram or dashboard has to be EXPLAINED — the audience needs telling what to look at and in what order. | about 460 |
| `MediaBleedSteps4` (traced) | Three to five named moves in order, where the subject deserves a full-height image. | about 330 |
| `MediaRailCases3` (traced) | A repeatable process produced three concrete examples with a measurable outcome, and the point is that the cases came from the process. | about 960 |
| `ImageContentV0` | A poster moment of a few words. | 17 ideal, 22 max |
| `ImageContentV1` | A short argument beside an image. | 119 ideal, 160 max |
| `ImageContentV2` | One paragraph beside a half-bleed image. | 112 ideal, 151 max |
| `ImageContentV3` | Showing a screenshot of the work. | 100 ideal, 135 max |
| `ImageContentV4` | A photo-led statement of a few words. | 26 ideal, 35 max |
| `ImageContentV5` | A dot-built hero beside a short intro. | 143 ideal, 193 max |
| `SplitsV4` | Structured text beside a full-bleed photo. | 301 ideal, 406 max |

**Entities.** People, partners and logos.

| Layout | When to use it | Copy (characters) |
|---|---|---|
| `EntLogoRows6` (traced) | A partner roster where which category a logo sits in matters as much as its being there. | about 420 |
| `EntPartnerCredentials3` (traced) | Two or three partnerships, each with its own proof and client roster, all of them strong. | about 880 |
| `EntTeamRow6` (traced) | Four to six people placed by role and location at the top of a meeting. Not biographies. | about 540 |
| `LogoWallV1` | Partner or client logos grouped by category. | 242 ideal, 326 max |
| `LogoWallV2` | A headline count backed by a logo wall. | 136 ideal, 183 max |
| `TeamV1` | Three people with full bios. | 397 ideal, 535 max |
| `TeamV2` | Four people with short bios. | 286 ideal, 386 max |

## What is not in this system

The deck generator's tooling (the content-writing skill, the capacity model, the halftone converter, the deck verifier and the handoff contract between the skills) stays in the repository. Where a card mentions the verifier, apply the rule it checks by eye. The system itself is edited here, in Claude Design: the repository copies it one way into the skill and never writes back, so never re-sync it from the repository. Where this system comes from, and its known gaps: *Source and open questions*.
