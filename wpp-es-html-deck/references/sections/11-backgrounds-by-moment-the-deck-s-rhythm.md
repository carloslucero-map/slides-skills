## 11. Backgrounds by moment (the deck's rhythm)

| Moment | Background recipe |
|---|---|
| **Default content** | Flat **WPP Cream** (the one consistent background for all content — never swap to pure White; see §3.3a). No dots behind content-dense slides. |
| **Content, gentle lift** | Cream with a tone-on-tone corner cluster — the shell's `data-dots` lift presets (`lift-corner`, `lift-orange-soft`, `lift-navy-corner`). |
| **Content, composed** | Tone-on-tone dot fields (the `field-*` `data-dots` presets), colour panels, and motif art per the design direction's row in SKILL.md (§12.15–§12.16); Cream stays the base. |
| **Cover / title** | The locked cover frame with registered art (§12.1a) — `mountain` full-bleed by default; alternates via the `cover` spec key. |
| **Divider** | The locked v4 playbook composition (§12.3 — one-hue macro scatter + bottom-pinned Thin caps title; `dividerStyle:"classic"` keeps the v3 geometry) in **one of six sanctioned colourways, chosen ONCE per deck** via the `dividerColourway` spec key: **`orange` (default — the house look) · `orange-600` · `orange-500` · `white` (tone-on-tone) · `navy-dots` (Navy macro dots + Orange 700 accent on Cream) · `navy-full` (full Navy slide, Cream/White dots)**. Every divider in a deck is identical — the colourway never rotates between sections. Footer contrast is automatic: each colourway carries `foot`/`edge` roles so the brand line, page number and confidential line flip Navy/White depending on what they sit over. If no colourway is named, the design direction picks it (`statement-led` → `navy-dots`; otherwise `orange`). |
| **Statement / quote** | Flat Cream, type only; optionally a faint lift cluster on one side. |
| **Outro** | **Light (default):** Cream + the Orange dot composition. **Dark, via `outro:"dark"`:** Navy with cream/white macro dots + Orange 700 accent — the sanctioned close for statement-led decks. Footer contrast handled by the same `foot`/`edge` mechanism. |
| **Dark moments** | Flat Navy `#000050`, White text, White/Cream or Orange 700 dots. Use for at most ~1 in 6 slides. |

---

