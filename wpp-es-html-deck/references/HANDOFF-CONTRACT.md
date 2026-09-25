<!-- Split out of SKILL.md to keep the always-loaded file small.
     Loaded on demand; see the stub in SKILL.md for the trigger. -->

## Input mode: deck-content-builder Markdown

When the input is a content file produced by the `deck-content-builder` skill
(the handoff contract below):

| Contract element | Renders as |
|---|---|
| `**Cover:**` line | spec title / subtitle / month / presenter |
| `_Deck type / Audience / Language / Confidential_` | spec `lang`, `confidential`, G0 answers |
| `## Section N — <title>` | chapter (agenda row + divider) |
| `### Slide N — <action title>` | slide headline — **verbatim, always**; any change must be surfaced at G1, never silent |
| `**token**` inside an action title (≤1 per title) | `<span class="hl">token</span>` — the Headline card's one highlight, Medium weight (strip the asterisks; NEVER render literal `**`) |
| `**Visual:**` hint | archetype via the SKILL.md quick-map; the last four name a layout family: `relational` (a hub, rings, a stack or a taxonomy: the rel-* canon, `orbit-*`, `process-timeline-v5`), `logos` (`ent-logo-rows-6`, `ent-partner-credentials-3`, `logo-wall-*`), `chart` (`charts-v1`, `-v2`), `split` (`splits-v1` to `-v3`). In Claude Design, the design system's catalogue family of the same shape |
| Bullets | the archetype's content (columns, boxes…) |
| `**Callout:**` | the slide's focal element (stat circle, pill, statement line) |
| `**Speaker notes:**` | `<aside class="notes">` |
| `_Source:_` | the `.source` bottom-left line |
| ```` ```data ```` block | a chart archetype (`stats-v*` / `charts-v*`) — numbers survive intact |
| `Direction?` column in a ```` ```data ```` block | `good` → `.stat--pos` (Orange 700) · `bad` → `.stat--neg` (Navy) · blank/`neutral` → default ink (guideline 09; max ONE `.stat--pos` per slide) |

<!-- HANDOFF-CONTRACT v3 — keep byte-identical with the block in deck-content-builder/SKILL.md -->
````markdown
# <Deck title (a full sentence; unconstrained)>
**Cover:** <2–4 word ALL-CAPS short title> · <one-sentence subheader> · <Month Year> · <Presenter or blank>
_Deck type: <MT | sales | discovery | other> · Audience: <who + the decision they need> · Language: <en | es | …> · Confidential: <yes | no>_

## Section 1 — <Chapter title, ≤4 words>

### Slide 1 — <Action title (the renderer keeps this verbatim; **bold** on AT MOST ONE key token marks it as the title highlight)>
**Visual:** columns | statement | quote | comparison | process | timeline | stats | boxes | table | team | image | cards | dot-hero | relational | logos | chart | split
- Bullet that proves the title
- Bullet that proves the title
**Callout:** <the single most important insight>
**Speaker notes:** <2–3 sentences for the presenter>
_Source: <source tag for any data claim>_

```data
Label | Value | Direction?
Search | 42 |
Cycle time | -41% | good
Churn | +8% | bad
```
````
<!-- /HANDOFF-CONTRACT -->

