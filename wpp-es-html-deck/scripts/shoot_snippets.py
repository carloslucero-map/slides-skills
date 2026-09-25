#!/usr/bin/env python3
"""
shoot_snippets.py — render every snippet variant on the real shell and look at it.

The kit has never been rendered. verify_deck.py checks built decks; nothing has
ever checked the templates those decks are assembled from, and there is not one
PNG per variant on disk. That is how `stats` came to hold seven unrelated
compositions under a single archetype without anyone noticing.

This script closes that hole the cheap way: build the shell once with
build_shell.py, splice ONE variant into it, screenshot it at 1920x1080, and tile
the results into a labelled contact sheet per archetype.

The gate is mechanical and deliberately narrow — horizontal overflow, blank
renders, and elements escaping the slide box. It is NOT the review. Most of what
is wrong with a template is visible in a PNG in seconds and invisible to every
assertion in this file, so open the sheets.

Usage
-----
  python3 scripts/shoot_snippets.py                       # all 51, sheets per archetype
  python3 scripts/shoot_snippets.py --only stats          # one archetype family
  python3 scripts/shoot_snippets.py --only stats-v6       # one variant
  python3 scripts/shoot_snippets.py --out /tmp/shots      # somewhere else
  python3 scripts/shoot_snippets.py --strict              # overflow FAILs instead of WARNs

Exit codes: 0 clean (warnings allowed), 1 a shot was missing/blank, or --strict
and something overflowed.

Landing this as WARN is on purpose. Several templates will violate §15 the first
time they are measured; if that blocks the run on day one the gate gets switched
off and the whole exercise is lost. Promote to --strict in CI once the kit is
clean, and never let that promotion happen silently.
"""
import argparse, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from verify_deck import _find_chrome, CHROME_HELP  # noqa: E402  (shared resolver)

CHROME = _find_chrome()
CANVAS_W, CANVAS_H = 1920, 1080
BLANK_PNG_BYTES = 20 * 1024        # a blank 1920x1080 render compresses tiny

FRAME_OPEN = '<div id="stage"><div id="frame">'
FRAME_CLOSE = "</div></div>"

# The shell paints a navigation HUD and a progress bar for a human driving a
# deck. In a template shot they are the harness photographing itself — they sit
# over the composition and would end up on every contact sheet tile.
SHOT_CHROME_KILL = """<style id="shot-kill">
#hud,#prog,.noscript-banner{display:none!important}
*{animation:none!important;transition:none!important;caret-color:transparent!important}
</style>"""

_status = {"fail": 0, "warn": 0, "pass": 0}


def report(status, name, detail):
    _status[status.lower()] = _status.get(status.lower(), 0) + 1
    print(f"{status:4} {name} — {detail}")


# --------------------------------------------------------------------------
# the shell

def build_base_shell():
    """Build the demo shell once; we only ever keep its <head> and chrome."""
    tmp = tempfile.mkdtemp(prefix="snipshoot-")
    out = os.path.join(tmp, "base.html")
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "build_shell.py"), "--out", out],
        capture_output=True, text=True, timeout=180)
    if not os.path.isfile(out):
        sys.exit(f"build_shell.py produced nothing:\n{proc.stdout}\n{proc.stderr}")
    return out


def splice(base_html, section_markup):
    """Replace every slide in the shell with this one section.

    Keeps the head, the inlined fonts and CSS, the runtime and the furniture —
    so what is measured is the template on the real shell, not in a sandbox that
    resembles it.
    """
    i = base_html.find(FRAME_OPEN)
    if i < 0:
        sys.exit("shell has no #frame — build_shell.py output changed shape")
    start = i + len(FRAME_OPEN)
    end = base_html.find(FRAME_CLOSE, start)
    if end < 0:
        sys.exit("shell #frame never closes — build_shell.py output changed shape")
    assets, named = media_assets(section_markup)
    section_markup = fill_media_hosts(section_markup)
    # The asset templates must be parsed BEFORE the shell's inline script, which
    # clones them into [data-motif] hosts on load. Appending them at </body> put
    # them after that script, so querySelector found nothing and every motif
    # rendered empty — which is what made these templates look broken.
    spliced = (base_html[:start] + "\n" + section_markup + "\n"
               + assets + base_html[end:])
    return (spliced.replace("</body>", SHOT_CHROME_KILL + "\n</body>", 1)
            if "</body>" in spliced else spliced + SHOT_CHROME_KILL)


def variant_markup(path):
    """The <section> only — the capacity comment is metadata, not markup."""
    src = open(path, encoding="utf-8").read()
    i = src.find("<section")
    if i < 0:
        return None
    return src[i:]


# --------------------------------------------------------------------------
# media

# A template that declares media renders empty in a bare shell: data-motif hosts
# are filled at runtime by cloning an inlined <template data-asset>, and the
# .img-*-media boxes ship a navy stand-in with a "replace me" comment. Shooting
# without either means photographing the placeholder and calling it the
# template — which left a sixth of the kit unreviewable on the first pass.
SAMPLE_PHOTO = "photo-ridge"          # a real brand photo, for stand-in media boxes
MEDIA_HOSTS = ("img-right-media", "img-half-media", "screenshot")


def media_assets(markup):
    """<template data-asset> blocks for every motif this template names."""
    import build_shell as BS
    names = sorted(set(re.findall(r'data-motif="([^"]+)"', markup)))
    needed = [n for n in names if n in BS.MOTIF_FILES]
    for n in names:
        if n not in BS.MOTIF_FILES:
            report("WARN", "media", f"template names motif {n!r}, which the shell has no file for")
    if any(h in markup for h in MEDIA_HOSTS) and SAMPLE_PHOTO not in needed:
        needed.append(SAMPLE_PHOTO)
    return "".join(f'<template data-asset="{n}"><img src="{BS.motif_uri(n)}" alt=""></template>'
                   for n in needed), needed


def fill_media_hosts(markup):
    """Swap the shipped navy stand-in for a real photo so the shot shows a
    filled slide. Cosmetic to the harness, decisive to the review."""
    if not any(h in markup for h in MEDIA_HOSTS):
        return markup
    return re.sub(
        r'<div style="width:100%;height:100%;background:var\(--wpp-navy\);"></div>',
        f'<div data-motif="{SAMPLE_PHOTO}" style="width:100%;height:100%;"></div>',
        markup)


# --------------------------------------------------------------------------
# the probe

OVERFLOW_PROBE = r"""
<style id="probe-kill">*{animation:none!important;transition:none!important}
#hud,#prog,.noscript-banner{display:none!important}</style>
<script id="probe">
(function(){
  function run(){
    try{
      document.body.setAttribute('data-motion','off');
      var frame=document.getElementById('frame');
      if(frame) frame.style.transform='none';
      var slide=document.querySelector('.slide');
      var out={docW:document.documentElement.scrollWidth, esc:[], empty:true};
      if(slide){
        var sb=slide.getBoundingClientRect();
        out.empty = slide.textContent.trim().length===0 &&
                    slide.querySelectorAll('img,svg').length===0;
        // Anything whose painted box leaves the slide by more than a rounding
        // error. Decoration that bleeds on purpose is tagged and exempt.
        var EXEMPT='.lift,.dot,.motif,.cover-art,.dv-dots,.ty-dots,.spark,.vrule';
        [].forEach.call(slide.querySelectorAll('*'), function(el){
          if(el.closest(EXEMPT)) return;
          var r=el.getBoundingClientRect();
          if(r.width===0&&r.height===0) return;
          var dx=Math.max(sb.left-r.left, r.right-sb.right);
          var dy=Math.max(sb.top-r.top, r.bottom-sb.bottom);
          if(dx>1.5||dy>1.5){
            out.esc.push({sel:(el.tagName.toLowerCase()+'.'+
              (el.className&&el.className.baseVal!==undefined?el.className.baseVal:
               (typeof el.className==='string'?el.className:'')).trim()
               .split(/\s+/).slice(0,3).join('.')).replace(/\.$/,''),
              dx:Math.round(dx), dy:Math.round(dy)});
          }
        });
      }
      // Only the worst few — a broken template reports hundreds of children.
      out.esc.sort(function(a,b){return (b.dx+b.dy)-(a.dx+a.dy);});
      out.esc=out.esc.slice(0,6);
      var p=document.createElement('pre'); p.id='ov';
      p.textContent=JSON.stringify(out); document.body.appendChild(p);
    }catch(e){
      var q=document.createElement('pre'); q.id='ov-err';
      q.textContent=String(e&&e.message||e); document.body.appendChild(q);
    }
  }
  if(document.readyState==='complete') setTimeout(run,60);
  else window.addEventListener('load', function(){setTimeout(run,60);});
})();
</script>
"""


def probe(html_path):
    """-> (record, None) or (None, why)."""
    src = open(html_path, encoding="utf-8").read()
    instr = (src.replace("</body>", OVERFLOW_PROBE + "\n</body>", 1)
             if "</body>" in src else src + OVERFLOW_PROBE)
    d = tempfile.mkdtemp(prefix="snipprobe-")
    p = os.path.join(d, "probe.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(instr)
    try:
        proc = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             f"--window-size={CANVAS_W},{CANVAS_H}",
             "--virtual-time-budget=12000", "--dump-dom",
             "file://" + p + "?motion=off"],
            capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, OSError) as e:
        return None, f"Chrome probe failed ({e})"
    m = re.search(r'<pre id="ov">(.*?)</pre>', proc.stdout, re.S)
    if not m:
        err = re.search(r'<pre id="ov-err">(.*?)</pre>', proc.stdout, re.S)
        return None, ("probe JS error: " + err.group(1)[:200]) if err else "probe produced nothing"
    try:
        return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")), None
    except ValueError as e:
        return None, f"probe returned unparseable JSON ({e})"


def shoot(html_path, png_path):
    cmd = [CHROME, "--headless=new", "--disable-gpu",
           f"--window-size={CANVAS_W},{CANVAS_H}", "--hide-scrollbars",
           f"--screenshot={png_path}", "file://" + html_path + "?motion=off"]
    try:
        subprocess.run(cmd, capture_output=True, timeout=90)
    except subprocess.TimeoutExpired:
        return "Chrome timed out"
    if not os.path.isfile(png_path) or os.path.getsize(png_path) == 0:
        return "no PNG written"
    if os.path.getsize(png_path) <= BLANK_PNG_BYTES:
        return f"{os.path.getsize(png_path)//1024} KB — looks blank"
    return None


# --------------------------------------------------------------------------
# the review surface

def contact_sheet(entries, outpath, cols=3, tw=560, th=315):
    """Tile shots labelled BY VARIANT ID.

    verify_deck's sheet labels tiles "slide 7", which is right for a deck and
    useless here — reviewing a kit, the name is the whole point.
    """
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        report("WARN", "contact sheet", "Pillow not installed — skipped")
        return None
    if not entries:
        return None
    pad, band = 10, 22
    rows = (len(entries) + cols - 1) // cols
    W, H = cols * tw + (cols + 1) * pad, rows * (th + band) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (232, 232, 232))
    d = ImageDraw.Draw(sheet)
    for i, (vid, png, flag) in enumerate(entries):
        try:
            im = Image.open(png).convert("RGB").resize((tw, th))
        except Exception as e:
            report("WARN", f"contact sheet {vid}", str(e))
            continue
        r, c = divmod(i, cols)
        x, y = pad + c * (tw + pad), pad + r * (th + band + pad)
        sheet.paste(im, (x, y))
        d.text((x + 2, y + th + 5), f"{vid}{'   << ' + flag if flag else ''}",
               fill=(180, 60, 0) if flag else (20, 20, 20))
        if flag:
            d.rectangle([x - 2, y - 2, x + tw + 1, y + th + 1],
                        outline=(255, 120, 0), width=3)
    os.makedirs(os.path.dirname(os.path.abspath(outpath)) or ".", exist_ok=True)
    sheet.save(outpath)
    return outpath


def main():
    ap = argparse.ArgumentParser()
    # Outside the skill on purpose: contact sheets are authoring output and the
    # skill directory has a 30 MB upload cap. See authoring/README.md.
    ap.add_argument("--out", default=os.path.normpath(
        os.path.join(SKILL, os.pardir, "authoring", "canon-shots")))
    ap.add_argument("--only", help="archetype family (stats) or one variant (stats-v6)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on overflow too, not just on missing/blank shots")
    ap.add_argument("--no-sheets", action="store_true")
    ap.add_argument("--canon", action="store_true",
                    help="shoot canon/<id>/template.html instead of the snippet kit; "
                         "each preview.png lands beside its ref.png in "
                         "authoring/canon-src/<id>/")
    args = ap.parse_args()

    if not CHROME:
        sys.exit(CHROME_HELP)

    if args.canon:
        cdir = os.path.join(SKILL, "canon", "templates")
        names = sorted(f[:-len(".html")] for f in os.listdir(cdir)
                       if f.endswith(".html"))
        vdir = None
    else:
        vdir = os.path.join(SKILL, "assets", "snippets", "variants")
        names = sorted(f[:-5] for f in os.listdir(vdir) if f.endswith(".html"))
    if args.only:
        names = [n for n in names if n == args.only or n.rsplit("-v", 1)[0] == args.only]
        if not names:
            sys.exit(f"--only {args.only!r} matched nothing in {vdir}")

    os.makedirs(args.out, exist_ok=True)
    base = open(build_base_shell(), encoding="utf-8").read()
    work = tempfile.mkdtemp(prefix="snipdeck-")
    print(f"{len(names)} variants · {CANVAS_W}x{CANVAS_H} · shots -> {args.out}\n")

    results, overflowed = [], []
    for vid in names:
        src = (os.path.join(SKILL, "canon", "templates", vid + ".html") if args.canon
               else os.path.join(vdir, vid + ".html"))
        markup = variant_markup(src)
        if markup is None:
            report("FAIL", vid, "no <section> in the variant file")
            continue
        page = os.path.join(work, vid + ".html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(splice(base, markup))

        # Canon previews are authoring output: they live beside the ref.png they
        # are judged against, outside the skill. The skill ships no sheet of
        # them; each layout's card in the design system renders it.
        png = (os.path.join(SKILL, os.pardir, "authoring", "canon-src", vid,
                            "preview.png") if args.canon
               else os.path.join(args.out, vid + ".png"))
        os.makedirs(os.path.dirname(png), exist_ok=True)
        err = shoot(page, png)
        if err:
            report("FAIL", vid, err)
            continue

        rec, why = probe(page)
        flag = ""
        if why:
            report("WARN", vid, why)
        else:
            if rec.get("empty"):
                report("FAIL", vid, "renders empty — no text, no media")
                continue
            if rec.get("docW", 0) > CANVAS_W:
                flag = f"page scrolls to {rec['docW']}px"
            elif rec.get("esc"):
                w = rec["esc"][0]
                flag = f"{w['sel']} escapes by {max(w['dx'], w['dy'])}px"
            if flag:
                overflowed.append(vid)
                report("WARN", vid, flag)
            else:
                report("PASS", vid, f"{os.path.getsize(png)//1024} KB, in the box")
        results.append((vid, png, flag))

    if not args.no_sheets and results:
        print()
        fams = {}
        for vid, png, flag in results:
            fam = "canon" if args.canon else vid.rsplit("-v", 1)[0]
            fams.setdefault(fam, []).append((vid, png, flag))
        for fam, entries in sorted(fams.items()):
            p = contact_sheet(entries, os.path.join(args.out, f"_sheet-{fam}.png"))
            if p:
                report("PASS", f"sheet {fam}",
                       f"{len(entries)} tiled -> {os.path.relpath(p, SKILL)}")

    print(f"\n{_status['pass']} pass · {_status['warn']} warn · {_status['fail']} fail")
    if overflowed:
        print(f"\n{len(overflowed)} template(s) do not fit the canvas: "
              f"{', '.join(overflowed)}")
        print("These are WARN by design — promote with --strict once the kit is clean.")
    print("\nThe gate is mechanical and narrow. It cannot see a dead lower half, "
          "a broken hierarchy or a composition that is simply ugly.\nRead the sheets.")
    sys.exit(1 if (_status["fail"] or (args.strict and overflowed)) else 0)


if __name__ == "__main__":
    main()
