#!/usr/bin/env python3
"""
refresh_design_system.py — copy the design system into the skill, one way.

The WPP Enterprise Solutions | MAP design system lives in Claude Design and owns
what a deck looks like. The skill's scripts (build_shell, verify_deck,
check_capacity, halftone) cannot reach Claude Design, so the HTML path runs on a
generated copy of it: wpp-es-html-deck/design-system/. This script is the only
thing that writes that copy. It reads the design system and writes the repo;
nothing here writes to the design system, and nothing ever runs the other way.

A refresh, run by an agent that can read the design system (Claude Code or
claude.ai):

  1. Read the design system with the Artifact tool into one folder: every path in
     MANIFEST below (one `paths` call; the layout cards are found from the file
     listing), and every asset in design-system.json's asset groups except Logos
     (one `path` call per blob id; the tool saves each as <blob><ext> beside
     project/).
  2. python3 authoring/refresh_design_system.py --from <that folder> \\
         --artifact <design system url> --version <version id> --write
  3. Prove nothing moved that should not have: build_docs.py --check,
     check_capacity.py, and a demo build and verify.
  4. Commit.

--check builds everything --write would write and compares it with the skill.
It exits 1 on any difference: the design system has changed since the last
refresh, or a generated file was edited by hand.

What it writes, under wpp-es-html-deck/:

  design-system/tokens.json, bundle.css, fonts/   verbatim
  design-system/illustrations/, photos/, textures/, exemplars/
                                                  verbatim, one folder per asset group
  design-system/icons/<family>.md                 the Icons group, grouped by the
                                                  weight families in guideline 07
  design-system/fixed-slides.json                 divider colourways, the light outro,
                                                  cover art and dot presets, read from
                                                  the Fixed slides cards and previews
  design-system/SOURCE.json                       address, version, sha256 per file
  canon/templates/<id>.html                       the layout's <section>, from its
  assets/snippets/variants/<id>.html              preview; the header above it is the
                                                  skill's own and is kept
  assets/snippets/<file>.html                     the same <section> in the kit's
                                                  authoring source, so
                                                  derive_capacity.py --split still
                                                  reproduces the variant

Exceptions, kept from the repo and listed in SOURCE.json with the reason:

  design-system/logos/  the design system's two logo uploads render black (their
                        fill lived in a <style> block, which uploads strip), so the
                        repo's attribute-coloured lockups stay until they are
                        re-uploaded.
"""
import argparse, glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SKILL = os.path.join(REPO, "wpp-es-html-deck")
CACHE = "design-system"                      # relative to SKILL

TITLE = "WPP Enterprise Solutions | MAP"
NAMESPACE = "WppEsMap"

# Everything read by path. Layout cards are added from the folder itself: any
# project/components/<Name>/ holding both README.md and preview.html whose README
# has an Origin line naming a skill file.
MANIFEST = [
    "project/design-system.json",
    "project/tokens.json",
    "project/components/bundle.css",
    "project/guidelines/07-iconography.md",
] + [f"project/components/{c}/{f}" for c in
     ("CoverSlide", "AgendaSlide", "DividerSlide", "ThankYouSlide")
     for f in ("README.md", "preview.html")]

# Asset group -> cache folder. Logos are the exception, see the docstring.
ASSET_DIRS = {"Illustrations": "illustrations", "Photography": "photos",
              "Textures": "textures", "Exemplars": "exemplars"}
LOGOS = "logos"
LOGO_REASON = ("The design system's logo uploads render black: their fill lived in "
               "a <style> block, which uploads strip. These are the repo's lockups, "
               "coloured by attribute; replace them with the design system's once it "
               "is re-uploaded that way.")

ICON_HEADER = ("# Icon suite — {fam} family ({n})\n\n"
               "ONE weight family per icon row / per slide (guideline 07). Paste the\n"
               "`<svg>` inline into `<div class=\"icon\">…</div>` — do not link to it.\n")


class Fail(Exception):
    pass


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def read(src, rel, binary=False):
    p = os.path.join(src, rel)
    if not os.path.isfile(p):
        raise Fail(f"missing from the read: {rel} (read it with the Artifact tool first)")
    with open(p, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8"})) as f:
        return f.read()


def blob_file(src, blob):
    hits = glob.glob(os.path.join(src, blob + ".*")) or glob.glob(os.path.join(src, "assets", blob + ".*"))
    if not hits:
        raise Fail(f"asset {blob} was not downloaded (Artifact read with path={blob})")
    return hits[0]


# ── the layouts: every card that names a skill file as its origin ─────────────

SECTION = re.compile(r'<section\b[^>]*class="slide[^"]*"[^>]*>.*?</section>', re.S)


def one_section(text, where):
    found = SECTION.findall(text)
    if len(found) != 1:
        raise Fail(f"{where}: expected one <section class=\"slide\">, found {len(found)}")
    return found[0]


def layout_cards(src):
    """[(card, skill-relative target, kind)] from each card's Origin line."""
    out = []
    comp = os.path.join(src, "project", "components")
    for card in sorted(os.listdir(comp)):
        readme, preview = (os.path.join(comp, card, f) for f in ("README.md", "preview.html"))
        if not (os.path.isfile(readme) and os.path.isfile(preview)):
            continue
        m = re.search(r"^## Origin\s*\n+(.+)", open(readme, encoding="utf-8").read(), re.M)
        if not m:
            continue
        kit = re.search(r"assets/snippets/variants/([\w-]+)\.html", m.group(1))
        canon = re.search(r"canon template `([\w-]+)`", m.group(1))
        if kit:
            out.append((card, f"assets/snippets/variants/{kit.group(1)}.html", "kit"))
        elif canon:
            out.append((card, f"canon/templates/{canon.group(1)}.html", "canon"))
    return out


def translate_icon_pointers(section, families):
    """The design system's layouts point at its own asset paths
    (`assets/icons/<name>.svg`); the skill ships its icons grouped by weight family."""
    def repl(m):
        name = m.group(1)
        fam = next((f for f, icons in families.items() if name in icons), None)
        if fam is None:
            raise Fail(f"a layout points at icon {name!r}, which no weight family holds")
        return f"{CACHE}/icons/{fam}.md (## {name})"
    return re.sub(r"(?:assets|design-system)/icons/([a-z0-9-]+)\.svg", repl, section)


# ── icons ─────────────────────────────────────────────────────────────────────

def icon_families(guideline, names):
    """{family: [icon, ...]} from guideline 07's "The suite, by weight family".

    Parsed, never hardcoded: shipping an icon under the wrong weight is the
    pairing rule's "most visible amateur tell". Every icon in the group must be
    placed exactly once, or the refresh fails."""
    if "## The suite, by weight family" not in guideline:
        raise Fail("guideline 07 has no 'The suite, by weight family' section")
    body = guideline.split("## The suite, by weight family", 1)[1].split("\n## ", 1)[0]
    fams, claimed = {}, set()
    for m in re.finditer(r"^\*\*([a-z]+)\*\*(.*?)(?=^\*\*[a-z]+\*\*|\Z)", body, re.M | re.S):
        picked = [i for i in dict.fromkeys(re.findall(r"`([a-z0-9-]+)`", m.group(2)))
                  if i in names and i not in claimed]
        if picked:
            fams[m.group(1)] = picked
            claimed |= set(picked)
    if claimed != set(names):
        raise Fail(f"guideline 07 leaves icons without a family: {sorted(set(names) - claimed)}")
    return fams


# ── the fixed slides ──────────────────────────────────────────────────────────

COLOURWAY_COLUMNS = {"Ground": "ground", "Type": "type", "Sub-label": "subLabel",
                     "Dots": "dots", "Brand line and page number": "footer",
                     "Confidential line": "confidential"}
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")


def colourways(readme):
    part = readme.split("## Colourways", 1)
    if len(part) < 2:
        raise Fail("DividerSlide has no Colourways section")
    rows = [r for r in part[1].split("\n## ", 1)[0].splitlines() if r.startswith("|")]
    head = [c.strip() for c in rows[0].strip("|").split("|")]
    keys = [COLOURWAY_COLUMNS.get(h) for h in head[1:]]
    if head[0] != "Colourway" or None in keys:
        raise Fail(f"DividerSlide's colourway table has columns this script does not know: {head}")
    out = {}
    for r in rows[2:]:
        cells = [c.strip().strip("`") for c in r.strip("|").split("|")]
        vals = cells[1:]
        if len(vals) != len(keys) or not all(HEX.fullmatch(v) for v in vals):
            raise Fail(f"DividerSlide colourway row is not a row of hex values: {r}")
        out[cells[0]] = {k: v.upper() for k, v in zip(keys, vals)}
    if not out:
        raise Fail("DividerSlide's colourway table is empty")
    return out


def js_object(script, name):
    """`var NAME={...};` from a preview's script, as data. Handles the two
    spellings the previews use: JSON, and a JS literal with bare or single-quoted
    keys and // comments."""
    m = re.search(r"var " + name + r"\s*=\s*(\{.*?\});", script, re.S)
    if not m:
        return None
    body = re.sub(r"//[^\n]*", "", m.group(1))
    body = re.sub(r"'([^']*)'", r'"\1"', body)
    body = re.sub(r'([{,]\s*)([A-Za-z_][\w-]*)\s*:', r'\1"\2":', body)
    try:
        return json.loads(body)
    except ValueError as e:
        raise Fail(f"could not read {name} in a preview script: {e}")


def fixed_slides(src, previews):
    divider = read(src, "project/components/DividerSlide/README.md")
    thanks = read(src, "project/components/ThankYouSlide/README.md")
    cover = read(src, "project/components/CoverSlide/README.md")

    # The light outro: its ground and type from the card's Slides recipe, its
    # three dot colours from the preview.
    sec = re.search(r'<section id="thank-you" style="([^"]*)"', thanks)
    if not sec:
        raise Fail("ThankYouSlide's Slides recipe has no <section id=\"thank-you\" style=…>")
    style = dict(p.split(":", 1) for p in (s.strip() for s in sec.group(1).split(";")) if ":" in p)
    ty_colours = js_object(read(src, "project/components/ThankYouSlide/preview.html"), "DOTCOLORS")
    outro = {"ground": style["background"].strip().upper(), "type": style["color"].strip().upper(),
             "dots": {k: v.upper() for k, v in ty_colours["thankyou"].items()}}

    art = re.search(r"\| Art \| `([\w-]+\.png)`", cover)
    alts = re.search(r"`([\w-]+\.png)` and `([\w-]+\.png)` are the registered alternates", cover)
    if not (art and alts):
        raise Fail("CoverSlide no longer names its art as this script expects")

    # Dot presets and their fixed colours, from every preview that carries them.
    # A preset is geometry; it must read the same in every preview that has it.
    dots, colours = {}, {}
    per_deck = {"divider", "divider-playbook", "thankyou"}   # coloured by the spec
    for where, text in previews:
        for table, into, skip in (("DOTS", dots, set()), ("DOTCOLORS", colours, per_deck)):
            obj = js_object(text, table) or {}
            for k, v in obj.items():
                if k in skip:
                    continue
                if table == "DOTCOLORS":
                    v = {a: c.upper() for a, c in v.items()}
                if k in into and into[k] != v:
                    raise Fail(f"{table}[{k!r}] differs between previews (seen again in {where})")
                into[k] = v
    return {
        "$comment": "Generated by authoring/refresh_design_system.py from the design "
                    "system's Fixed slides cards and layout previews. Do not edit.",
        "colourways": colourways(divider),
        "outros": {"light": outro},
        "covers": {"default": art.group(1), "alternates": [alts.group(1), alts.group(2)]},
        "dots": dict(sorted(dots.items())),
        "dotColours": dict(sorted(colours.items())),
    }


# ── the plan: every file and section a refresh produces ───────────────────────

def plan(src, artifact, version):
    ds = json.loads(read(src, "project/design-system.json"))
    if ds.get("title") != TITLE or ds.get("namespace") != NAMESPACE:
        raise Fail(f"{src} is not the {TITLE!r} design system ({ds.get('title')!r})")
    tokens = read(src, "project/tokens.json", binary=True)
    files = {}                                   # skill-relative path -> (bytes, from)

    files[f"{CACHE}/tokens.json"] = (tokens, "project/tokens.json")
    files[f"{CACHE}/bundle.css"] = (read(src, "project/components/bundle.css", binary=True),
                                    "project/components/bundle.css")
    for font in dict.fromkeys(f["file"] for f in json.loads(tokens)["type"]["fonts"]):
        files[f"{CACHE}/{font}"] = (read(src, f"project/{font}", binary=True), f"project/{font}")

    groups = ds["assetGroups"]
    for group, folder in ASSET_DIRS.items():
        for name in groups[group]["order"]:
            meta = groups[group]["files"][name]
            data = open(blob_file(src, meta["blob"]), "rb").read()
            if len(data) != meta["size"]:
                raise Fail(f"{group}/{name}: read {len(data)} bytes, the design system says {meta['size']}")
            files[f"{CACHE}/{folder}/{name}"] = (data, f"asset {group}/{name} ({meta['blob']})")

    icons = {}
    for name in groups["Icons"]["order"]:
        meta = groups["Icons"]["files"][name]
        icons[name[:-len(".svg")]] = open(blob_file(src, meta["blob"]), encoding="utf-8").read().strip()
    families = icon_families(read(src, "project/guidelines/07-iconography.md"), icons)
    for fam, members in families.items():
        md = ICON_HEADER.format(fam=fam, n=len(members)) + "".join(
            f"\n## {i}\n\n{icons[i]}\n" for i in members)
        files[f"{CACHE}/icons/{fam}.md"] = (md.encode("utf-8"),
                                            "asset group Icons + guideline 07 families")

    sections, previews = {}, []
    for c in ("DividerSlide", "ThankYouSlide", "AgendaSlide", "CoverSlide"):
        previews.append((c, read(src, f"project/components/{c}/preview.html")))
    for card, target, kind in layout_cards(src):
        preview = read(src, f"project/components/{card}/preview.html")
        previews.append((card, preview))
        sections[target] = (translate_icon_pointers(one_section(preview, card), families),
                            f"project/components/{card}/preview.html", kind)
    if not sections:
        raise Fail("no layout card names a skill file in its Origin line")

    fixed = fixed_slides(src, previews)
    files[f"{CACHE}/fixed-slides.json"] = (
        (json.dumps(fixed, indent=1, ensure_ascii=False) + "\n").encode("utf-8"),
        "Fixed slides cards + layout previews")

    exceptions = {}
    for p in sorted(glob.glob(os.path.join(SKILL, CACHE, LOGOS, "*.svg"))):
        rel = os.path.relpath(p, SKILL)
        exceptions[rel] = {"sha256": sha(open(p, "rb").read()), "why": LOGO_REASON}
    if len(exceptions) != len(groups["Logos"]["order"]):
        raise Fail(f"expected the {len(groups['Logos']['order'])} logos in {CACHE}/{LOGOS}/, "
                   f"found {len(exceptions)}")

    source = {
        "$comment": "Generated by authoring/refresh_design_system.py. Every file below "
                    "is a copy of the design system; verify_deck.py fails the deck when "
                    "one no longer matches its sha256. Edit the design system, then "
                    "refresh; never edit these by hand.",
        "designSystem": {"title": TITLE, "namespace": NAMESPACE, "artifact": artifact,
                         "version": version, "lastChange": ds.get("lastChange")},
        "files": {p: {"sha256": sha(b), "from": f} for p, (b, f) in sorted(files.items())},
        "sections": {p: {"sha256": sha(s), "from": f} for p, (s, f, _) in sorted(sections.items())},
        "exceptions": exceptions,
    }
    files[f"{CACHE}/SOURCE.json"] = (
        (json.dumps(source, indent=1, ensure_ascii=False) + "\n").encode("utf-8"), None)
    return files, sections


# ── apply, or compare ─────────────────────────────────────────────────────────

def kit_source_for(variant_now, target):
    """The authoring source that holds this variant's current <section>, verbatim."""
    hits = [p for p in glob.glob(os.path.join(SKILL, "assets", "snippets", "*.html"))
            if variant_now in open(p, encoding="utf-8").read()]
    if len(hits) != 1:
        raise Fail(f"{target}: its <section> is in {len(hits)} kit sources, expected exactly 1")
    return hits[0]


def run(files, sections, write):
    drift = []
    for rel, (data, _) in files.items():
        p = os.path.join(SKILL, rel)
        now = open(p, "rb").read() if os.path.isfile(p) else None
        if now != data:
            drift.append(("new" if now is None else "changed", rel))
            if write:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "wb").write(data)
    for rel, (section, _, kind) in sections.items():
        p = os.path.join(SKILL, rel)
        if not os.path.isfile(p):
            raise Fail(f"{rel} does not exist: a new layout needs its header written first")
        text = open(p, encoding="utf-8").read()
        now = one_section(text, rel)
        if now == section:
            if kind == "kit":
                # the variant is current; its authoring source must be too, or the
                # next derive_capacity.py --split quietly undoes this refresh
                held = [q for q in glob.glob(os.path.join(SKILL, "assets", "snippets", "*.html"))
                        if section in open(q, encoding="utf-8").read()]
                if len(held) != 1:
                    drift.append(("kit source out of step", rel))
            continue
        drift.append(("section", rel))
        if write:
            if kind == "kit":
                srcp = kit_source_for(now, rel)
                s = open(srcp, encoding="utf-8").read()
                open(srcp, "w", encoding="utf-8").write(s.replace(now, section, 1))
                drift.append(("section", os.path.relpath(srcp, SKILL)))
            open(p, "w", encoding="utf-8").write(text.replace(now, section, 1))
    cached = {os.path.relpath(p, SKILL) for p in glob.glob(os.path.join(SKILL, CACHE, "**", "*"), recursive=True)
              if os.path.isfile(p)}
    stray = sorted(cached - set(files) - {r for r in cached if r.startswith(f"{CACHE}/{LOGOS}/")})
    for rel in stray:
        drift.append(("not in the design system", rel))
        if write:
            os.remove(os.path.join(SKILL, rel))
    return drift


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from", dest="src", required=True,
                    help="the folder the Artifact tool saved the design system into")
    ap.add_argument("--artifact", required=True, help="the design system's claude.ai address")
    ap.add_argument("--version", required=True, help="the version id the read reported")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args()
    try:
        files, sections = plan(os.path.abspath(args.src), args.artifact, args.version)
        drift = run(files, sections, write=args.write)
    except Fail as e:
        sys.exit(f"REFRESH FAILED — {e}")
    n_assets = sum(1 for p in files if p.split("/")[1] in ASSET_DIRS.values())
    summary = (f"{len(files)} files ({n_assets} assets), {len(sections)} layout sections, "
               f"design system {args.version}")
    if args.write:
        print(f"REFRESHED — {summary}")
        for kind, rel in drift:
            print(f"  {kind:>26}  {rel}")
        return
    if drift:
        print(f"CACHE STALE — {len(drift)} difference(s) from {summary}:", file=sys.stderr)
        for kind, rel in drift:
            print(f"  {kind:>26}  {rel}", file=sys.stderr)
        sys.exit(1)
    print(f"CACHE OK — {summary}")


if __name__ == "__main__":
    main()
