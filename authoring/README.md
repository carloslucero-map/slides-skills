# authoring/

Everything the `wpp-es-html-deck` skill was **made from**, kept outside the skill
folder so it cannot count against claude.ai's upload caps.

claude.ai takes a skill at **200 entries — files AND directories — and 30 MB**.
The skill folder is the thing you upload, so it holds only what a deck build
reads. Nothing here is read while a deck is being built.

| | |
|---|---|
| `canon-src/<id>/` | Per template: `meta.json` (what the catalogue is generated from), `spec.json` (what must not change), `measure.json` (geometry off the source slide), `ref.png` (the source slide itself), `preview.png` (what the template renders). 125 files in 25 directories — 150 entries, which is why they are not in the skill. |
| `canon-tools/` | `build_catalog.py` generates the skill's `canon/CATALOG.md` and `catalog.json` from every `canon-src/<id>/meta.json`. `derive_canon_capacity.py` merges canon limits into `references/capacity.json`. `measure.py` writes a `measure.json`. `build_ref_manifest.py` joins the curated selection to bank page order. |
| `refresh_design_system.py` | Writes the skill's copy of the design system, `wpp-es-html-deck/design-system/`, and each layout's `<section>`, from files an agent read with the Artifact tool. One way only: design system to repo. `--check` fails when the copy has drifted. |
| `icons-src/` | The 32 icon SVGs as they were before the design system took them over. Provenance only: the skill's `design-system/icons/<family>.md` are generated from the design system's Icons group. |
| `canon-shots/` | Contact sheets from `wpp-es-html-deck/scripts/shoot_snippets.py`. The review surface: most of what is wrong with a template is visible in a PNG in seconds and invisible to every assertion in the verifier. |
| `canon-ref/` | The source deck the canon was traced from — `renders/` at full resolution, `measure/`, and `manifest.json`. |

## The artifacts these generate, which DO ship

| in the skill | generated from | by |
|---|---|---|
| `canon/CATALOG.md`, `canon/catalog.json` | `canon-src/<id>/meta.json` + `spec.json` | `canon-tools/build_catalog.py --write` |
| `canon/PREVIEWS.png` | `canon-src/<id>/preview.png` | `wpp-es-html-deck/scripts/package_skill.py` built it; rebuild with the snippet in that script |
| `design-system/` (tokens, stylesheet, fonts, icons, the other asset groups, fixed-slide data, `SOURCE.json`) and every layout `<section>` in `canon/templates/` and `assets/snippets/` | the design system in Claude Design | `refresh_design_system.py --write` |
| `references/capacity.json` (canon rows) | `canon/templates/<id>.html` + `canon-src/<id>/measure.json` | `canon-tools/derive_canon_capacity.py --write` |

`verify_deck.py` looks for `canon-tools/` and skips its canon checks when it is
absent — an installed skill has no `authoring/` beside it, and that is not an
error.

## Why things are where they are

`package_skill.py` reports the skill folder's entry count on every run and fails
above the cap. When it fails, the fix is almost never deletion: look for a
directory holding one or two files, since a directory costs exactly as much as a
file, and move authoring-only material here.
