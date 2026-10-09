#!/usr/bin/env python3
"""
animate_slides.py — the animated HTML version of a Claude Slides deck, in any
design system.

It takes the deck's own files (project/deck.json and project/slides/<id>.html,
as written for the Claude Slides deck) and writes ONE self-contained HTML file
that a presenter opens in a browser: the same slides, pixel for pixel, with the
deck's transitions and builds played by a small runtime, plus the extra motion
Claude Slides cannot do. Every picture and font is embedded, so the file works
offline (a face linked from Google Fonts stays a link).

  python3 scripts/animate_slides.py --deck <root> --files <dir> [<dir> ...] \\
      --out deck-animated.html [--extras stagger,count,draw,words,drift]

  --deck    the folder holding project/deck.json and project/slides/
  --files   folders holding the deck's pictures and fonts as an Artifact read
            saved them: an asset as <asset id>.<ext> anywhere under the folder,
            an installed file at its deck path (project/ds/<folder>/...)
  --extras  the extra motion to add, comma-separated (default: all of them):
              stagger  units that share a build step arrive one after another
              count    large figures count up from zero as they appear
              draw     thin rules and bars that build draw themselves on
              words    titles that rise in, rise word by word
              drift    full-bleed pictures and decorative art move slowly
            A design system whose motion rules allow only rise and fade gets
            stagger and count only (references/SLIDES.md, *The animated file*).
  --title   the file's title (default: the deck's title)

The runtime keys: → / Space / click to advance (a click reveal waits for it),
← to go back, F full screen, N speaker notes, 1–9 the chapters, Home / End.
Reduced motion, print and ?motion=off show every slide finished.

Exit 0 when written; 1 when the deck cannot be read or a picture or font it
names is not in --files (each missing one is listed, nothing is written).
"""
import argparse, base64, html, json, os, re, sys

EXTRAS = ("stagger", "count", "draw", "words", "drift")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".avif": "image/avif", ".svg": "image/svg+xml",
        ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf",
        ".mp4": "video/mp4", ".webm": "video/webm"}
REF = re.compile(r"""(/?_blob/[0-9A-Za-z]{8,64}|project/ds/[A-Za-z0-9._/-]+)""")


def fail(msg):
    sys.exit(f"FAIL — {msg}")


class Files:
    """Finds a deck's pictures and fonts in the folders an Artifact read saved them to."""

    def __init__(self, dirs, root):
        self.dirs = [root] + list(dirs)
        self.blobs = {}
        for d in self.dirs:
            for base, _, names in os.walk(d):
                for n in names:
                    stem = n.split(".")[0]
                    if re.fullmatch(r"[0-9A-Za-z]{8,64}", stem):
                        self.blobs.setdefault(stem, os.path.join(base, n))
        self.missing = []
        self.cache = {}

    def path(self, ref):
        if "_blob/" in ref:
            return self.blobs.get(ref.rsplit("/", 1)[1])
        for d in self.dirs:
            p = os.path.join(d, ref)
            if os.path.isfile(p):
                return p
        return None

    def uri(self, ref):
        if ref in self.cache:
            return self.cache[ref]
        p = self.path(ref)
        if not p:
            self.missing.append(ref)
            self.cache[ref] = ref
            return ref
        ext = os.path.splitext(p)[1].lower()
        mime = MIME.get(ext)
        if not mime:
            with open(p, "rb") as f:
                head = f.read(16)
            mime = ("image/png" if head.startswith(b"\x89PNG") else "image/jpeg" if head[:3] == b"\xff\xd8\xff"
                    else "font/woff2" if head[:4] == b"wOF2" else "image/svg+xml" if b"<svg" in head or b"<?xml" in head
                    else "application/octet-stream")
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        self.cache[ref] = f"data:{mime};base64,{data}"
        return self.cache[ref]


def embed_refs(markup, files):
    """Every src="…" and url(…) that names a deck asset or an installed file becomes a data: URI."""
    def attr(m):
        return m.group(1) + REF.sub(lambda r: files.uri(r.group(1)), m.group(2)) + m.group(3)
    markup = re.sub(r'''(\bsrc=")([^"]*)(")''', attr, markup)
    markup = re.sub(r'''(url\(\s*['"]?)([^'")]*)(['"]?\s*\))''', attr, markup)
    return markup


SHAPES = {
    "rect": "", "rounded": "border-radius:24px;", "ellipse": "border-radius:50%;",
    "diamond": "clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%);",
    "arrow-right": "clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%);",
    "arrow-left": "clip-path:polygon(100% 30%,40% 30%,40% 0,0 50%,40% 100%,40% 70%,100% 70%);",
    "arrow-up": "clip-path:polygon(30% 100%,30% 40%,0 40%,50% 0,100% 40%,70% 40%,70% 100%);",
    "arrow-down": "clip-path:polygon(30% 0,30% 60%,0 60%,50% 100%,100% 60%,70% 60%,70% 0);",
}


def custom_elements(markup, warnings, sid):
    """Claude Slides' own elements, in plain HTML: shapes, connectors and live embeds."""
    def shape(m):
        attrs, kind = m.group(1), (re.search(r'kind="([a-z-]+)"', m.group(1)) or [None, "rect"])[1]
        style = (re.search(r'style="([^"]*)"', attrs) or [None, ""])[1]
        if kind == "line":
            colour = (re.search(r"background:\s*([^;]+)", style) or [None, "currentColor"])[1]
            extra = f"height:0;border-top:2px solid {colour};background:none;"
        else:
            extra = SHAPES.get(kind, "")
        rest = re.sub(r'\s*(kind|style)="[^"]*"', "", attrs)
        return f'<div{rest} style="{style};{extra}"></div>'
    markup = re.sub(r"<x-shape\b([^>]*)>\s*</x-shape>", shape, markup)
    markup = re.sub(r"<x-shape\b([^>]*)/>", shape, markup)

    def connector(m):
        a = m.group(1)
        num = lambda k: float((re.search(rf'\b{k}="([-0-9.]+)', a) or [None, "nan"])[1])
        x1, y1, x2, y2 = num("x1"), num("y1"), num("x2"), num("y2")
        if any(v != v for v in (x1, y1, x2, y2)):
            warnings.append(f"{sid}: a connector without coordinates was left out")
            return ""
        style = (re.search(r'style="([^"]*)"', a) or [None, ""])[1]
        colour = (re.search(r"(?<![-a-z])color:\s*([^;]+)", style) or [None, "#000"])[1].strip()
        width = (re.search(r"border-width:\s*([0-9.]+)", style) or [None, "2"])[1]
        dash = ' stroke-dasharray="8 6"' if "dashed" in style else ' stroke-dasharray="2 6"' if "dotted" in style else ""
        route = (re.search(r'route="([a-z]+)"', a) or [None, "straight"])[1]
        pts = [(x1, y1), (x2, y2)]
        if route == "hv":
            pts = [(x1, y1), (x2, y1), (x2, y2)]
        elif route == "vh":
            pts = [(x1, y1), (x1, y2), (x2, y2)]
        elif route == "elbow":
            mx = (x1 + x2) / 2
            pts = [(x1, y1), (mx, y1), (mx, y2), (x2, y2)]
        head = (re.search(r'\bhead="([a-z]+)"', a) or [None, "end"])[1]
        mid = f"m{abs(hash(a)) % 10**8}"
        marker = (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
                  f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{colour}"/></marker></defs>')
        ends = (f' marker-end="url(#{mid})"' if head in ("end", "both") else "") + \
               (f' marker-start="url(#{mid})"' if head == "both" else "")
        p = " ".join(f"{x},{y}" for x, y in pts)
        return (f'<svg aria-hidden="true" style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible" '
                f'viewBox="0 0 1920 1080">{marker}<polyline points="{p}" fill="none" stroke="{colour}" '
                f'stroke-width="{width}"{dash}{ends}/></svg>')
    markup = re.sub(r"<x-connector\b([^>]*)>\s*</x-connector>", connector, markup)
    markup = re.sub(r"<x-connector\b([^>]*)/>", connector, markup)

    def embed(m):
        style = (re.search(r'style="([^"]*)"', m.group(1)) or [None, ""])[1]
        return (f'<iframe sandbox="allow-scripts" style="{style};border:0;background:transparent" '
                f'srcdoc="{html.escape(m.group(2), quote=True)}"></iframe>')
    markup = re.sub(r"<x-embed\b([^>]*)>(.*?)</x-embed>", embed, markup, flags=re.S)

    if "<x-icon" in markup:
        warnings.append(f"{sid}: Claude Slides' own icons (x-icon) do not exist outside Claude Slides and were left out")
        markup = re.sub(r"<x-icon\b[^>]*>\s*</x-icon>|<x-icon\b[^>]*/>", "", markup)
    return markup


CSS = r"""
html,body{margin:0;height:100%;background:#111;overflow:hidden}
#stage{position:fixed;inset:0;overflow:hidden}
#frame{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
#frame>section{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;
  visibility:hidden;margin:0}
#frame>section:not([style*="display"]){display:flex;flex-direction:column}
#frame>section.on,#frame>section.out{visibility:visible}
#frame>section.out{z-index:1}#frame>section.on{z-index:2}
#frame section *{box-sizing:border-box}
#frame section h1,#frame section h2,#frame section h3,#frame section p,#frame section ul,#frame section ol,#frame section li{margin:0}
#frame section h1{font-size:96px;font-weight:600;line-height:1.1}
#frame section h2{font-size:64px;font-weight:600;line-height:1.15}
#frame section h3{font-size:44px;font-weight:600;line-height:1.2}
#frame section p{font-size:32px;font-weight:400;line-height:1.4}
#frame section ul,#frame section ol{font-size:32px;line-height:1.4;padding:0 0 0 1.15em}
#frame section div:not([style*="display"]){display:flex;flex-direction:column}
#frame section img{display:block}
#frame section svg{display:block}
#frame section>aside{display:none}
#frame .w{display:inline-block;will-change:transform}
.pre{opacity:0!important}
#notes{position:fixed;left:24px;right:24px;bottom:24px;max-height:40vh;overflow:auto;padding:18px 22px;border-radius:10px;
  background:rgba(20,20,20,.92);color:#f2f2f2;font:16px/1.5 system-ui,-apple-system,Segoe UI,Arial,sans-serif;display:none;z-index:9}
body.notes-on #notes{display:block}
#hint{position:fixed;right:18px;bottom:14px;padding:6px 10px;border-radius:6px;background:rgba(0,0,0,.55);color:#eee;
  font:12px/1.4 system-ui,-apple-system,Segoe UI,Arial,sans-serif;z-index:9;transition:opacity .6s}
@media print{
  @page{size:1920px 1080px;margin:0}
  html,body{height:auto;overflow:visible;background:none}
  #stage{position:static}#frame{position:static;transform:none!important;width:auto;height:auto}
  #frame>section{position:relative;visibility:visible!important;page-break-after:always;break-after:page}
  .pre{opacity:1!important}#notes,#hint{display:none!important}
}
"""

JS = r"""
(function(){
  var CFG=__CFG__;
  var X={};CFG.extras.forEach(function(k){X[k]=1;});
  var frame=document.getElementById('frame'),slides=[].slice.call(frame.children),
      notes=document.getElementById('notes'),hint=document.getElementById('hint');
  var mp=(location.search.match(/[?&]motion=([a-z]+)/)||[])[1];
  var still=mp==='off'||(mp!=='force'&&(navigator.webdriver||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)));
  var EASE='cubic-bezier(.2,.7,.2,1)',i=-1,queue=[],timers=[],running=[];

  function fit(){var s=Math.min(innerWidth/1920,innerHeight/1080);
    frame.style.transform='translate('+((innerWidth-1920*s)/2)+'px,'+((innerHeight-1080*s)/2)+'px) scale('+s+')';}
  function base(e){return e.style.transform&&e.style.transform!=='none'?' '+e.style.transform:'';}
  function anim(e,kf,o){var a=e.animate(kf,o);running.push(a);return a;}
  function clear(){timers.forEach(clearTimeout);timers=[];running.forEach(function(a){try{
    if(a.effect&&a.effect.getTiming().iterations===Infinity)a.cancel();else a.finish();}catch(_){a.cancel();}});running=[];}
  function later(fn,ms){timers.push(setTimeout(fn,ms));}

  // Builds: data-build-in="<effect> [step] [auto]" on a slide's pinned children.
  function builds(s){
    var g={};
    [].slice.call(s.children).forEach(function(e){
      var b=(e.getAttribute('data-build-in')||'').trim().split(/\s+/);if(!b[0])return;
      var n=parseInt(b[1],10);if(isNaN(n))n=1;
      (g[n]=g[n]||{n:n,auto:false,els:[]}).els.push({e:e,fx:b[0]});
      if(b.indexOf('auto')>=0)g[n].auto=true;
    });
    return Object.keys(g).map(Number).sort(function(a,b){return a-b;}).map(function(k){return g[k];});
  }
  function isBar(e){var w=e.offsetWidth,h=e.offsetHeight;return e.tagName==='DIV'&&!e.children.length&&((h<=10&&w>=40)||(w<=10&&h>=40));}
  function title(e){
    if(/^H[12]$/.test(e.tagName))return e;
    var h=e.querySelectorAll('h1,h2');return h.length===1&&e.textContent.trim()===h[0].textContent.trim()?h[0]:null;
  }
  function splitWords(h){
    if(h.getAttribute('data-w'))return [].slice.call(h.querySelectorAll('.w'));
    if([].some.call(h.children,function(c){return c.tagName!=='BR';}))return null;
    var out=[];h.setAttribute('data-w','1');
    [].slice.call(h.childNodes).forEach(function(n){
      if(n.nodeType!==3)return;
      var f=document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(function(t){
        if(!t)return;if(/^\s+$/.test(t)){f.appendChild(document.createTextNode(t));return;}
        var sp=document.createElement('span');sp.className='w';sp.textContent=t;f.appendChild(sp);out.push(sp);
      });
      h.replaceChild(f,n);
    });
    return out.length>1&&out.length<=16?out:null;
  }
  var FX={
    fade:function(){return [{opacity:0},{opacity:1}];},
    rise:function(b){return [{opacity:0,transform:'translateY(48px)'+b},{opacity:1,transform:(b||'none')}];},
    drop:function(b){return [{opacity:0,transform:'translateY(-48px)'+b},{opacity:1,transform:(b||'none')}];},
    left:function(b){return [{opacity:0,transform:'translateX(-72px)'+b},{opacity:1,transform:(b||'none')}];},
    right:function(b){return [{opacity:0,transform:'translateX(72px)'+b},{opacity:1,transform:(b||'none')}];},
    scale:function(b){return [{opacity:0,transform:'scale(.86)'+b},{opacity:1,transform:(b||'none')}];},
    pop:function(b){return [{opacity:0,transform:'scale(.5)'+b},{opacity:1,transform:'scale(1.08)'+b,offset:.7},{opacity:1,transform:(b||'none')}];}
  };
  function play(it,delay){
    var e=it.e,b=base(e),fx=FX[it.fx]?it.fx:'fade';
    e.classList.remove('pre');later(function(){count(e);},delay+150);
    if(X.draw&&isBar(e)&&(fx==='fade'||fx==='left'||fx==='right')){
      var tall=e.offsetHeight>e.offsetWidth,o=e.style.transformOrigin;
      e.style.transformOrigin=tall?'50% 0':(fx==='right'?'100% 50%':'0 50%');
      var a=anim(e,[{transform:(tall?'scaleY(0)':'scaleX(0)')+b},{transform:(b||'none')}],{duration:800,delay:delay,easing:EASE,fill:'backwards'});
      a.onfinish=function(){e.style.transformOrigin=o;};return;
    }
    var h=X.words&&fx==='rise'?title(e):null,w=h?splitWords(h):null;
    if(w){w.forEach(function(s,k){anim(s,[{opacity:0,transform:'translateY(.6em)'},{opacity:1,transform:'none'}],
      {duration:650,delay:delay+k*70,easing:EASE,fill:'backwards'});});return;}
    anim(e,FX[fx](b),{duration:fx==='pop'?560:fx==='fade'?600:700,delay:delay,easing:fx==='pop'?'cubic-bezier(.3,1.4,.5,1)':EASE,fill:'backwards'});
  }
  function playGroup(g,delay){
    g.els.forEach(function(it,k){play(it,delay+(X.stagger?Math.min(k,6)*90:0));});
  }
  // Count-up: a large figure counts from zero as it appears (1.2M, 18%, €4.2M, 1,200, 3,5).
  function count(root){
    if(!X.count||still)return;
    var els=/^(P|H1|H2|H3|LI)$/.test(root.tagName)?[root]:[].slice.call(root.querySelectorAll('p,h1,h2,h3'));
    els.forEach(function(e){
      if(e.getAttribute('data-c')||e.children.length||e.closest('.pre')||e.closest('[data-kept]'))return;
      if(parseFloat(getComputedStyle(e).fontSize)<40)return;
      var t=e.textContent.trim(),m=t.match(/^([^0-9A-Za-z]{0,2})([0-9][0-9.,]*)(\s?(?:%|x|X|M|K|k|bn|m|pts?|M\+|K\+|\+)?)$/);
      if(!m)return;
      var raw=m[2],sep=raw.match(/[.,](\d+)$/),dec=0,dch='.',tch='';
      if(sep&&sep[1].length!==3){dec=sep[1].length;dch=raw.charAt(raw.length-dec-1);}
      var rest=dec?raw.slice(0,-dec-1):raw;
      if(/[.,]/.test(rest)){tch=rest.match(/[.,]/)[0];}
      var v=parseFloat(rest.split(tch||'#').join('')+(dec?'.'+raw.slice(-dec):''));
      if(isNaN(v)||(!dec&&v<10)||/^0\d/.test(raw)||(!dec&&!tch&&v>=1900&&v<=2100&&raw.length===4))return;
      e.setAttribute('data-c',t);e.style.minWidth=e.offsetWidth+'px';
      var t0=performance.now(),D=1100;
      function fmt(x){var s=x.toFixed(dec),p=s.split('.'),n=p[0];
        if(tch)n=n.replace(/\B(?=(\d{3})+(?!\d))/g,tch);return m[1]+n+(dec?dch+p[1]:'')+m[3];}
      (function step(now){var p=Math.min(1,((now||t0)-t0)/D);p=1-Math.pow(1-p,3);
        if(p<1){e.textContent=fmt(v*p);requestAnimationFrame(step);}else{e.textContent=t;e.style.minWidth='';e.removeAttribute('data-c');}})();
    });
  }
  // Drift: full-bleed pictures and decorative art move slowly while the slide shows.
  function drift(s){
    if(!X.drift||still)return;
    [].slice.call(s.children).forEach(function(e,k){
      var full=e.offsetWidth>=1700&&e.offsetHeight>=950,deco=!full&&!e.getAttribute('data-build-in')&&
        (e.tagName==='svg'||e.tagName==='SVG')&&e.getBoundingClientRect().width>=0&&e.offsetWidth*e.offsetHeight>=90000;
      var b=base(e);
      if(full&&e.tagName==='IMG')anim(e,[{transform:'scale(1)'+b},{transform:'scale(1.05)'+b}],{duration:18000,direction:'alternate',iterations:Infinity,easing:'ease-in-out'});
      else if(deco)anim(e,[{transform:'translate(0,0)'+b},{transform:'translate('+(k%2?8:-8)+'px,'+(k%3?-10:10)+'px)'+b}],
        {duration:9000+k*700,direction:'alternate',iterations:Infinity,easing:'ease-in-out'});
    });
  }
  function finishAll(s){builds(s).forEach(function(g){g.els.forEach(function(it){it.e.classList.remove('pre');});});}
  function enter(s){
    queue=builds(s);
    if(still){finishAll(s);queue=[];return;}
    queue.forEach(function(g){g.els.forEach(function(it){it.e.classList.add('pre');});});
    drift(s);
    later(function(){count(s);},350);
    autos(600);
  }
  function autos(delay){
    var d=delay;
    while(queue.length&&queue[0].auto){playGroup(queue.shift(),d);d+=500;}
  }
  function step(){if(!queue.length)return false;playGroup(queue.shift(),0);autos(500);return true;}

  // Transitions: data-transition on the slide that LEAVES (fade, push, magic).
  function show(n,how){
    n=Math.max(0,Math.min(slides.length-1,n));if(n===i)return;
    clear();[].forEach.call(frame.querySelectorAll('[data-kept]'),function(e){e.removeAttribute('data-kept');});
    var prev=slides[i],next=slides[n],tr=prev&&how==='fwd'?(prev.getAttribute('data-transition')||'fade'):'none';
    slides.forEach(function(s){s.classList.remove('on','out');});
    i=n;next.classList.add('on');
    notes.textContent=((next.querySelector(':scope>aside')||{}).textContent||'').trim()||'No notes on this slide.';
    if(history.replaceState)history.replaceState(null,'','#'+(i+1));
    if(how!=='fwd'||still){finishAll(next);queue=[];if(!still)drift(next);return;}
    if(prev&&tr!=='none'){
      prev.classList.add('out');
      if(tr==='push'){
        anim(prev,[{transform:'translateX(0)'},{transform:'translateX(-1920px)'}],{duration:700,easing:EASE}).onfinish=function(){prev.classList.remove('out');};
        anim(next,[{transform:'translateX(1920px)'},{transform:'translateX(0)'}],{duration:700,easing:EASE});
      }else if(tr==='magic'){
        magic(prev,next);
      }else{
        anim(next,[{opacity:0},{opacity:1}],{duration:550,easing:'ease'}).onfinish=function(){prev.classList.remove('out');};
      }
    }
    enter(next);
  }
  // Magic move: an element with the same id on both slides travels from its old place to its new one.
  function magic(a,b){
    var map=[];
    [].slice.call(b.children).forEach(function(e){
      if(!e.id)return;var o=a.querySelector(':scope>#'+CSS.escape(e.id));if(o)map.push([o,e]);
    });
    map.forEach(function(p){
      var o=p[0],e=p[1],r0={x:o.offsetLeft,y:o.offsetTop,w:o.offsetWidth,h:o.offsetHeight},
          r1={x:e.offsetLeft,y:e.offsetTop,w:e.offsetWidth,h:e.offsetHeight},b=base(e),ob=e.style.transformOrigin;
      o.style.visibility='hidden';e.style.transformOrigin='0 0';e.classList.remove('pre');e.setAttribute('data-kept','1');
      var sx=r1.w?r0.w/r1.w:1,sy=r1.h?r0.h/r1.h:1;
      anim(e,[{transform:'translate('+(r0.x-r1.x)+'px,'+(r0.y-r1.y)+'px) scale('+sx+','+sy+')'+b},{transform:(b||'none')}],
        {duration:900,easing:'cubic-bezier(.45,0,.2,1)'}).onfinish=function(){e.style.transformOrigin=ob;o.style.visibility='';};
      e.setAttribute('data-moved','1');
    });
    [].slice.call(b.children).forEach(function(e){
      if(e.getAttribute('data-moved')){e.removeAttribute('data-moved');return;}
      anim(e,[{opacity:0},{opacity:1}],{duration:700,delay:200,easing:'ease',fill:'backwards'});
    });
    anim(a,[{opacity:1},{opacity:0}],{duration:600,easing:'ease'}).onfinish=function(){a.classList.remove('out');
      [].slice.call(a.children).forEach(function(o){o.style.visibility='';});};
    // the travelling elements must not build on arrival: they are already there
    queueSkip=map.map(function(p){return p[1];});
  }
  var queueSkip=[];
  var enter0=enter;enter=function(s){enter0(s);
    if(queueSkip.length){queue.forEach(function(g){g.els=g.els.filter(function(it){
      if(queueSkip.indexOf(it.e)>=0){it.e.classList.remove('pre');return false;}return true;});});
      queue=queue.filter(function(g){return g.els.length;});queueSkip=[];}};

  function fwd(){if(!step())show(i+1,'fwd');}
  function back(){show(i-1,'back');}
  addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'||e.key==='Enter'){fwd();e.preventDefault();}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'||e.key==='Backspace'){back();e.preventDefault();}
    else if(e.key==='Home')show(0,'back');else if(e.key==='End')show(slides.length-1,'back');
    else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
    else if(e.key==='n'||e.key==='N'){document.body.classList.toggle('notes-on');}
    else if(e.key>='1'&&e.key<='9'){var k=CFG.chapters[+e.key-1];if(k!==undefined)show(k,'fwd');}
  });
  document.getElementById('stage').addEventListener('click',function(e){
    if(e.target.closest('a,iframe'))return;if(e.clientX>innerWidth*.35)fwd();else back();});
  addEventListener('resize',fit);fit();
  if(hint)setTimeout(function(){hint.style.opacity=0;},5000);
  var h=parseInt(location.hash.slice(1),10);show(!isNaN(h)?h-1:0,'fwd');
})();
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--deck", required=True)
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--extras", default=",".join(EXTRAS))
    ap.add_argument("--title")
    a = ap.parse_args()

    extras = [x.strip() for x in a.extras.split(",") if x.strip() and x.strip() != "none"]
    bad = [x for x in extras if x not in EXTRAS]
    if bad:
        fail(f"unknown extra {', '.join(bad)}; choose from {', '.join(EXTRAS)}")
    idx_path = os.path.join(a.deck, "project", "deck.json")
    try:
        deck = json.load(open(idx_path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail(f"cannot read {idx_path}: {e}")
    files = Files(a.files, a.deck)
    warnings = []

    order = list(deck.get("order") or [])
    slide_dir = os.path.join(a.deck, "project", "slides")
    if os.path.isdir(slide_dir):
        for n in sorted(os.listdir(slide_dir)):
            sid = n[:-5]
            if n.endswith(".html") and sid not in order:
                order.append(sid)   # a file the index leaves out shows last, as in Claude Slides
    sections, ids = [], []
    for sid in order:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", sid):
            fail(f"slide id {sid!r} is not a slide id")
        p = os.path.join(slide_dir, sid + ".html")
        if not os.path.isfile(p):
            warnings.append(f"{sid}: in the index but has no file; left out")
            continue
        s = open(p, encoding="utf-8").read().strip()
        if not s.startswith("<section"):
            fail(f"{sid}.html does not hold one <section>")
        if re.match(r"<section\b[^>]*\shidden(\s|>|=)", s):
            continue
        s = custom_elements(s, warnings, sid)
        sections.append(embed_refs(s, files))
        ids.append(sid)
    if not sections:
        fail("the deck has no slides")

    faces, links = [], []
    for key, f in (deck.get("faces") or {}).items():
        fam = f.get("family")
        if not fam:
            continue
        if f.get("src"):
            uri = files.uri(f["src"].lstrip("/") if f["src"].startswith("/project/") else f["src"])
            fmt = {"font/woff2": "woff2", "font/woff": "woff", "font/ttf": "truetype", "font/otf": "opentype"}.get(
                uri.split(";")[0][5:], "woff2")
            faces.append(f'@font-face{{font-family:"{fam}";src:url({uri}) format("{fmt}");font-display:block}}')
        elif f.get("href", "").startswith("https://fonts.googleapis.com/css2?"):
            links.append(f'<link rel="stylesheet" href="{html.escape(f["href"])}">')
            warnings.append(f"face {fam}: linked from Google Fonts, so it needs a connection (every other file is embedded)")

    if files.missing:
        print("FAIL — not found in --files (read each from the deck, then run again):", file=sys.stderr)
        for m in sorted(set(files.missing)):
            print(f"  {m}", file=sys.stderr)
        sys.exit(1)

    chapters = []
    for sec in (deck.get("sections") or {}).values():
        st = sec.get("start") if isinstance(sec, dict) else None
        if st in ids:
            chapters.append(ids.index(st))
    chapters = sorted(set(chapters))
    cfg = json.dumps({"extras": extras, "chapters": chapters})
    title = a.title or deck.get("title") or "Deck"
    doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
           f"<title>{html.escape(title)}</title>\n" + "".join(l + "\n" for l in links) +
           "<style>\n" + "\n".join(faces) + CSS + "</style>\n</head>\n<body>\n"
           "<div id=\"stage\"><div id=\"frame\">\n" + "\n".join(sections) + "\n</div></div>\n"
           "<div id=\"notes\"></div>\n<div id=\"hint\">→ next · ← back · F full screen · N notes</div>\n"
           "<script>" + JS.replace("__CFG__", cfg) + "</script>\n</body>\n</html>\n")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(doc)
    for w in warnings:
        print(f"note: {w}")
    print(f"WROTE — {a.out}: {len(sections)} slides, {os.path.getsize(a.out) / 1048576:.2f} MB, "
          f"extras: {', '.join(extras) or 'none'}")


if __name__ == "__main__":
    main()
