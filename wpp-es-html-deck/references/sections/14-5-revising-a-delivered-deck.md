## 14.5 Revising a delivered deck

- **Never rerun `build_shell.py` on a delivered deck** — it regenerates the shell and wipes the filled content. Edit the delivered HTML in place, addressing slides by their `data-slide-id`.
- Page numbers are runtime-computed — add or remove slides freely; never hand-renumber.
- Re-run `scripts/verify_deck.py` after every edit. The full revision protocol lives in SKILL.md.

---

