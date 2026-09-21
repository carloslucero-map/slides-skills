#!/usr/bin/env python3
"""
derive_canon_capacity.py — capacity limits for the canon templates.

Without this, every canon slide comes back UNCHECKED from check_capacity.py.
That was the state after wiring the catalogue: ten templates the skill would
happily choose, and no way to tell whether the copy being poured into them
actually fits. They worked with the placeholder copy their author wrote, which
is not the same as working.

The kit gets its limits from derive_capacity.py, which measures each snippet's
own placeholder text and its container width off the shell CSS. This does the
same for canon/<id>/template.html and merges the result into the same
references/capacity.json the checker already reads, so nothing downstream has to
learn a second format.

  python3 authoring/canon-tools/derive_canon_capacity.py --demo <a-deck>.html --write
  python3 authoring/canon-tools/derive_canon_capacity.py --demo <a-deck>.html --check

TWO HONEST LIMITS, stated because a number that looks measured and is not is
worse than no number:

  The measured figure is the placeholder's length, and the placeholder is what
  the template's author happened to write. It is evidence of what fits, not of
  what the slot can hold.

  Canon templates carry their own scoped CSS, so a slot's real width often comes
  from a grid this script cannot resolve. Where the template's own <style> gives
  an explicit font-size the geometry uses it; otherwise it falls back to the
  shell's class metrics, and slots resolved that way are marked basis
  "placeholder" rather than "geometry".
"""
import argparse, json, os, re, sys

# These tools moved out of the skill (wpp-es-html-deck/canon/_tools/) when the
# skill folder had to fit claude.ai's 200-entry cap. The SOURCES they read moved
# with them; the ARTIFACTS they generate still land inside the skill.
#   authoring/canon-src/<id>/{meta,spec,measure}.json, ref.png, preview.png
#   wpp-es-html-deck/canon/{CATALOG.md, catalog.json, PREVIEWS.png, templates/}
HERE = os.path.dirname(os.path.abspath(__file__))
AUTHORING = os.path.dirname(HERE)
REPO = os.path.dirname(AUTHORING)
SKILL = os.path.join(REPO, "wpp-es-html-deck")
SRC = os.path.join(AUTHORING, "canon-src")
CANON = os.path.join(SKILL, "canon")
TEMPLATES = os.path.join(CANON, "templates")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

import derive_capacity as DC   # noqa: E402  — reuse the kit's CSS reader and maths
import check_capacity as CC   # noqa: E402  — and its slot parser, so both see the same slots

CAPACITY = os.path.join(SKILL, "references", "capacity.json")

# The skip list must be check_capacity's, not a second opinion. Diverging by one
# class (sub-item) left 45 second-level items out of the derived total while the
# checker counted them, so seq-steps-panels came back 27% over a ceiling derived
# from its own placeholder copy. Whatever the checker counts, this counts.
SKIP = set(CC.SKIP)


def _skip(cls):
    return cls in SKIP


def template_css_sizes(html):
    """{class: font_px} from the template's OWN <style> block."""
    css = "\n".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    out = {}
    for block in re.finditer(r"\.([a-z][a-z0-9-]*)\s*\{([^}]*)\}", css):
        m = re.search(r"font-size:\s*(\d+(?:\.\d+)?)px", block.group(2))
        if m:
            out.setdefault(block.group(1), float(m.group(1)))
    return out


def slots_of(html):
    """{class: {items, lens}} for every text-bearing class in the section.

    Uses check_capacity's own parser rather than a regex. The regex version
    measured one template out of ten: `<(\\w+)[^>]*class=...>(.*?)</\\1>` stops at
    the first closing tag, which for nested divs is a child's, so every template
    whose slots are not leaf elements silently produced nothing. Same parser as
    the checker means the same slots the checker will look for.
    """
    section = html[html.find("<section"):]
    section = re.sub(r"<style>.*?</style>", "", section, flags=re.S)

    # check_capacity's parser emits one entry per CLASS, so `class="body
    # qsg-note"` yields the same text twice. That is right for per-slot limits
    # and wrong for a slide total — counting both doubled every total and made
    # three templates read as over their own limit. This subclass records the
    # element as well, so slots and totals can each count what they should.
    class PerElement(CC.Slots):
        def __init__(self):
            super().__init__()
            self.elements = []

        def handle_endtag(self, tag):
            while self.stack and self.stack[-1]["depth"] >= self.depth:
                e = self.stack.pop()
                t = re.sub(r"\s+", " ", "".join(e["text"])).strip()
                if t:
                    self.elements.append((tuple(e["cls"]), t))
                    for c in e["cls"]:
                        self.slots.append((c, t))
            self.depth -= 1

    p = PerElement()
    p.feed(section)
    p.close()

    slots = {}
    for cls, text in p.slots:
        if _skip(cls):
            continue
        e = slots.setdefault(cls, {"items": 0, "lens": []})
        e["items"] += 1
        e["lens"].append(len(text))
    # Counted PER CLASS, including the double count for a multi-class element,
    # because that is exactly how check_capacity.py totals a slide (it groups by
    # class and sums every text in every group). Deduplicating here produced a
    # smaller limit than the checker's own arithmetic and put five templates
    # over a ceiling derived from themselves. The limit has to be measured the
    # way it will be enforced, quirk included.
    total = sum(len(t) for cls, t in p.slots if not _skip(cls))
    return slots, total


def build(demo):
    css = DC.read_css_metrics(demo)
    DC.CONTENT_X0, DC.CONTENT_X1, DC.CONTENT_W = DC.read_frame(demo)
    out = []
    for f in sorted(os.listdir(TEMPLATES)):
        if not f.endswith(".html"):
            continue
        d = f[:-len(".html")]
        p = os.path.join(TEMPLATES, f)
        html = open(p, encoding="utf-8").read()
        tcss = template_css_sizes(html)
        arch = re.search(r'data-archetype="([^"]+)"', html)
        arch = arch.group(1) if arch else d
        found, total = slots_of(html)
        slots = {}
        for cls, e in found.items():
            measured = max(e["lens"])
            fpx = tcss.get(cls) or (css.get(cls) or {}).get("font_px")
            # Shell geometry only applies when the TEMPLATE has not overridden
            # the class. Canon templates pair the shell's .body with a scoped
            # class that resets size and width, so the shell's .body geometry
            # (max-width 1200px at 26px) describes a box this slot is not in —
            # applying it flagged correct copy as over limit.
            overridden = cls in tcss or any(
                other in tcss for other in found if other != cls)
            geo = (DC.geometric_max(cls, e["items"], css)
                   if (css.get(cls) or {}).get("font_px") and not overridden else None)
            # Tightest wins, exactly as the kit does — never let geometry
            # authorise more copy than the recipe demonstrates.
            hard = min(geo, round(measured * 1.8)) if geo else round(measured * 1.8)
            slots[cls] = {
                "items": e["items"],
                "min_chars": min(e["lens"]),
                "ideal_chars": measured,
                "max_chars": int(hard),
                "font_px": fpx,
                "basis": "geometry" if geo and geo < measured * 1.8 else "placeholder",
            }
        out.append({
            "file": f"canon/{d}/template.html",
            "archetype": arch,
            "label": f"CANON · {d}",
            "slots": slots,
            "slide_ideal_chars": total,
            "slide_max_chars": int(total * 1.35),
            "_source": "canon",
        })
    return out


def merge(existing, canon):
    kept = [t for t in existing if t.get("_source") != "canon"]
    return kept + canon


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", required=True, help="a built deck, for the shell's CSS metrics")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.error("pass --write or --check")
    if not os.path.isfile(CAPACITY):
        sys.exit(f"no capacity.json at {CAPACITY} — run derive_capacity.py first")

    cat = json.load(open(CAPACITY, encoding="utf-8"))
    canon = build(args.demo)
    merged = merge(cat["templates"], canon)

    if args.check:
        have = [t for t in cat["templates"] if t.get("_source") == "canon"]
        if len(have) != len(canon):
            print(f"CANON CAPACITY STALE — {len(canon)} templates on disk, "
                  f"{len(have)} in capacity.json.\nRun: python3 "
                  f"authoring/canon-tools/derive_canon_capacity.py --demo <deck>.html --write",
                  file=sys.stderr)
            sys.exit(1)
        print(f"CANON CAPACITY OK — {len(have)} templates measured")
        return

    cat["templates"] = merged
    open(CAPACITY, "w", encoding="utf-8").write(json.dumps(cat, indent=1) + "\n")
    ph = sum(1 for t in canon for s in t["slots"].values() if s["basis"] == "placeholder")
    geo = sum(1 for t in canon for s in t["slots"].values() if s["basis"] == "geometry")
    print(f"merged {len(canon)} canon templates into references/capacity.json")
    print(f"{geo} slots bounded by geometry, {ph} by the placeholder's own length")
    print("A 'placeholder' basis is evidence of what fits, not proof of what the "
          "slot holds. Treat those maxima as provisional until a real deck "
          "stresses them.")


if __name__ == "__main__":
    main()
