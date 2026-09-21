#!/usr/bin/env python3
"""
check_capacity.py — WPP ES | MAP HTML Deck Builder

Pre-flight text-overflow check. Reads a FILLED deck and compares each slide's
copy against references/capacity.json, the per-slot limits derived from the
shell's real type metrics.

Why this exists: capacity.json and the inline <!-- capacity --> blocks are
advisory — nothing enforced them. The §15 geometry pass in verify_deck.py does
catch overflow, but it needs headless Chrome and a screenshot per slide. This
runs on the HTML alone, in under a second, so a slide that is obviously 40%
over its limit gets caught before anything is rendered.

It does NOT replace verify_deck.py. It catches ONE failure mode (too much
text) and is blind to everything else: collisions, contrast, composition,
media anchoring. Passing here means "worth rendering", not "ships".

Matching rule: a slide is checked against the MOST PERMISSIVE template sharing
its data-archetype. Several templates can share an archetype (7 are "stats"),
and picking the loosest means a warning is always real overflow rather than an
artefact of guessing the wrong variant. It under-reports by design.

Usage:
  python3 check_capacity.py deck.html [--skill .] [--strict]

Exit codes: 0 clean (or over-limit with warnings), 1 with --strict and any
slide over its limit.
"""

import argparse, json, os, re, sys
from html.parser import HTMLParser

SKIP = {
    "slide", "pageno", "footer-brand", "lift", "motif", "notes", "content-band",
    "cols", "dot", "col-dot", "arrow", "stem", "vrule", "orbit", "confidential",
    "ph", "ph-init", "source",
}


class Slots(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.slots, self.depth = [], [], 0
        self.in_style = False

    # Void elements never produce an end tag, so incrementing depth for them
    # left the stack permanently deeper than the document. Elements then failed
    # to pop and swallowed every following sibling's text: a .venn-label
    # measured 105 chars because it had absorbed the footer brand and the
    # comment after it. Any slide containing <br> or <img> — most of the kit —
    # has been mis-measured this whole time.
    VOID = {"br", "img", "hr", "input", "meta", "link", "source", "col", "area",
            "base", "embed", "param", "track", "wbr"}

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.in_style = True
        if tag in self.VOID:
            return
        self.depth += 1
        classes = (dict(attrs).get("class") or "").split()
        keep = [c for c in classes if c not in SKIP]
        if keep:
            self.stack.append({"cls": keep, "depth": self.depth, "text": []})

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.in_style = False
        while self.stack and self.stack[-1]["depth"] >= self.depth:
            e = self.stack.pop()
            t = re.sub(r"\s+", " ", "".join(e["text"])).strip()
            if t:
                for c in e["cls"]:
                    self.slots.append((c, t))
        self.depth -= 1

    def handle_data(self, data):
        # Canon templates carry their scoped CSS inside the <section> so that
        # pasting the section carries its styling. That means the parser now
        # meets <style> bodies, and counting CSS as slide copy would put every
        # canon slide hundreds of characters over its limit.
        if self.stack and not self.in_style:
            self.stack[-1]["text"].append(data)


def load_limits(skill):
    path = os.path.join(skill, "references", "capacity.json")
    if not os.path.exists(path):
        sys.exit(f"capacity.json not found at {path} — run derive_capacity.py first")
    cat = json.load(open(path, encoding="utf-8"))["templates"]
    # most permissive template per archetype
    limits, slide_max = {}, {}
    for e in cat:
        a = e["archetype"]
        slide_max[a] = max(slide_max.get(a, 0), e["slide_max_chars"])
        for cls, s in e["slots"].items():
            cur = limits.setdefault(a, {}).setdefault(cls, {"max": 0, "ideal": 0})
            cur["max"] = max(cur["max"], s["max_chars"])
            cur["ideal"] = max(cur["ideal"], s["ideal_chars"])
    return limits, slide_max


def slides_of(html):
    """`class` may sit anywhere in the <section> tag.

    This used to require it FIRST, so a slide written
    <section data-x="…" class="slide"> was silently not a slide and its text was
    never measured — a false all-clear, which is the one thing this tool must
    never produce. Found 2026-09-11 by a real deck whose fallback slides carried
    an attribute ahead of the class."""
    out = []
    for m in re.finditer(r'<section\b[^>]*>', html):
        tag = m.group(0)
        if not re.search(r'\bclass="slide[^"]*"', tag):
            continue
        arch = re.search(r'data-archetype="([^"]+)"', tag)
        sid = re.search(r'data-slide-id="([^"]+)"', tag)
        end = html.find("</section>", m.start())
        end = end + 10 if end != -1 else len(html)
        out.append((sid.group(1) if sid else "?",
                    arch.group(1) if arch else None,
                    html[m.start():end]))
    return out


def check_canon_integrity(skill):
    """Every CATALOG row resolves to a template, and every template is listed.

    A catalogue row pointing at nothing sends the model to a file that is not
    there; a template absent from the catalogue is invisible, which is the state
    the whole canon was in until it was wired up. Both are silent failures.
    """
    cat = os.path.join(skill, "canon", "catalog.json")
    cdir = os.path.join(skill, "canon")
    if not os.path.isfile(cat):
        print("CANON SKIP — no canon/catalog.json (run authoring/canon-tools/build_catalog.py)")
        return True
    try:
        listed = {t["id"] for t in json.load(open(cat, encoding="utf-8"))["templates"]}
    except (ValueError, KeyError) as e:
        print(f"CANON FAIL — catalog.json unreadable ({e})")
        return False
    on_disk = {d for d in os.listdir(cdir)
               if not d.startswith("_")
               and os.path.isfile(os.path.join(cdir, d, "template.html"))}
    # The upload bundle flattens canon/<id>/template.html to
    # canon/templates/<id>.html: claude.ai counts DIRECTORIES toward its 200
    # entry cap, and 25 directories holding one file each cost 50 of them.
    # Both layouts are valid; the checker accepts either.
    tdir = os.path.join(cdir, "templates")
    if os.path.isdir(tdir):
        on_disk |= {f[:-len(".html")] for f in os.listdir(tdir)
                    if f.endswith(".html")}
    ok = True
    for missing in sorted(listed - on_disk):
        print(f"CANON FAIL — catalogue lists {missing!r}, which has no template.html")
        ok = False
    for unlisted in sorted(on_disk - listed):
        print(f"CANON FAIL — canon/{unlisted}/ exists but no catalogue row reaches it")
        ok = False
    if ok:
        print(f"CANON OK — {len(listed)} templates, catalogue and disk agree")
    return ok


def check_kit_integrity(skill):
    """Every row of SNIPPET-INDEX.md must resolve to a real file in variants/.

    SKILL.md now forbids opening assets/snippets/*.html at fill time, so a row
    pointing at a variant that --split never wrote is unrecoverable: the model
    is told to open a file that does not exist and forbidden from the canonical
    one it was generated from. Silent before this check; a hard failure now.
    """
    idx = os.path.join(skill, "references", "SNIPPET-INDEX.md")
    vdir = os.path.join(skill, "assets", "snippets", "variants")
    if not os.path.isfile(idx):
        print(f"KIT FAIL — no SNIPPET-INDEX.md at {idx}")
        return False
    rows = re.findall(r'`(variants/[A-Za-z0-9._-]+\.html)`', open(idx, encoding="utf-8").read())
    if not rows:
        print("KIT FAIL — SNIPPET-INDEX.md lists no variants; did --index run?")
        return False
    missing = [r for r in rows if not os.path.isfile(os.path.join(skill, "assets", "snippets", r))]
    orphans = sorted(set(os.listdir(vdir)) - {os.path.basename(r) for r in rows}) \
        if os.path.isdir(vdir) else []
    for r in missing:
        print(f"KIT FAIL — SNIPPET-INDEX.md points at {r}, which does not exist")
    for o in orphans:
        print(f"KIT WARN — variants/{o} exists but no index row reaches it")
    if not missing:
        print(f"KIT OK — {len(rows)} index rows all resolve"
              + (f" ({len(orphans)} unreachable)" if orphans else ""))
    return not missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck", nargs="?",
                    help="built deck to check; omit to run the kit check only")
    ap.add_argument("--skill", default=".")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any slide is over its limit")
    args = ap.parse_args()

    kit_ok = check_kit_integrity(args.skill)
    kit_ok = check_canon_integrity(args.skill) and kit_ok
    if args.deck is None:
        sys.exit(0 if kit_ok else 1)
    print()

    limits, slide_max = load_limits(args.skill)
    html = open(args.deck, encoding="utf-8", errors="replace").read()
    slides = slides_of(html)
    if not slides:
        sys.exit("no <section class=\"slide\"> found — is this a built deck?")

    over = unknown = untagged = locked = checked = 0
    # locked slides carry their own classes and no archetype — legitimately exempt
    LOCKED = ("cover", "agenda", "divider", "thank-you", "thankyou", "outro")
    print(f"{len(slides)} slides · limits from {len(limits)} archetypes\n")

    for i, (sid, arch, body) in enumerate(slides, 1):
        secls = re.search(r'<section\b[^>]*?\bclass="([^"]*)"', body)
        secls = secls.group(1) if secls else ""
        if not arch:
            if any(k in secls or k in sid for k in LOCKED):
                locked += 1
            else:
                # A filled content slide with no data-archetype cannot be checked.
                # Never let that pass silently — a false all-clear is worse than
                # no tool at all.
                untagged += 1
                print(f"  UNCHECKED slide {i:>2} [{sid}] no data-archetype "
                      f"— capacity NOT verified")
            continue
        if arch not in limits:
            print(f"  UNCHECKED slide {i:>2} [{sid}] archetype {arch!r} not in capacity.json")
            unknown += 1
            continue
        checked += 1
        p = Slots()
        p.feed(body)
        try:
            p.close()
        except Exception:
            pass

        grouped = {}
        for cls, t in p.slots:
            grouped.setdefault(cls, []).append(t)

        issues, total = [], 0
        for cls, texts in grouped.items():
            lim = limits[arch].get(cls)
            for t in texts:
                total += len(t)
                if lim and len(t) > lim["max"]:
                    pct = (len(t) / lim["max"] - 1) * 100
                    issues.append(f".{cls} {len(t)}/{lim['max']} chars (+{pct:.0f}%)")

        smax = slide_max.get(arch, 0)
        if smax and total > smax:
            issues.append(f"SLIDE TOTAL {total}/{smax} chars")

        if issues:
            over += 1
            print(f"  OVER slide {i:>2} [{sid}] {arch}")
            for s in issues[:6]:
                print(f"         {s}")

    print()
    print(f"checked {checked} · over limit {over} · locked/exempt {locked} · "
          f"UNCHECKED {untagged + unknown}")
    if over:
        print(f"\n{over} slide(s) over limit. Fix by picking a lower-density "
              f"variant from references/SNIPPET-INDEX.md or cutting copy — "
              f"never by shrinking type (§4.5).")
    elif checked:
        print("\nNo checked slide is over its limit.")
    if untagged + unknown:
        print(f"\n{untagged + unknown} slide(s) could NOT be checked — they carry "
              f"no capacity data. That is not a pass. A shell straight out of "
              f"build_shell.py is unchecked by design: run this AFTER filling.")
    if not checked:
        print("\nNOTHING WAS CHECKED — do not read this as a clean result.")
    print("\nThis checks TEXT VOLUME ONLY. Collisions, contrast, composition and "
          "media anchoring are still verify_deck.py's job.")

    sys.exit(1 if (not kit_ok or (args.strict and (over or untagged))) else 0)


if __name__ == "__main__":
    main()
