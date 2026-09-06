#!/usr/bin/env python3
"""ADVERSE_SITE generator. Source of truth = data/site.json + this file. Run: python3 gen.py  -> writes the .html pages."""
import json, html, os, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, "data/site.json"), encoding="utf-8"))
B = D["brand"]; STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M"); SITE_URL = "https://raouf-hamouda.github.io/adverse-production/"
E = html.escape
PROJ = {p["id"]: p for p in D["projects"]}

def head(title, desc):
    return f'''<!doctype html>
<html lang="en" class="no-js" data-accent="acid">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:site_name" content="Adverse Production">
<meta property="og:image" content="{SITE_URL}media/logo/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Adverse Production">
<meta property="og:image" content="{SITE_URL}media/logo/og-square.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE_URL}media/logo/og.png">
<link rel="icon" href="media/logo/favicon.svg?v={STAMP}" type="image/svg+xml">
<link rel="icon" href="media/logo/favicon-32.png?v={STAMP}" sizes="32x32" type="image/png">
<link rel="icon" href="media/logo/favicon-192.png?v={STAMP}" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="media/logo/apple-touch-icon.png">
<meta name="theme-color" content="#050505">
<link rel="stylesheet" href="css/fonts.css?v={STAMP}">
<link rel="stylesheet" href="css/tokens.css?v={STAMP}">
<link rel="stylesheet" href="css/base.css?v={STAMP}">
<link rel="stylesheet" href="css/site.css?v={STAMP}">
</head>
<body data-theme="dark">
<div class="grid-lines" aria-hidden="true"></div>'''

def loader():
    L = json.load(open(os.path.join(ROOT, "media/logo/logo.json")))
    P = json.load(open(os.path.join(ROOT, "media/logo/mark_paths.json")))
    paths = "".join(f'<path class="p p-{k}" d="{P[k]}"/>' for k in ("tr", "tl", "bl", "br"))   # DOM order = stacking: TR under TL under BL under BR
    CH = 110.0   # the clip box is the word box plus 10% below the baseline, so the letters rise from under a line, never cut on the glyph
    letters = "".join(f'<span class="l" style="left:{l["left"]:.3f}%;top:{l["top"]/CH*100:.3f}%;width:{l["width"]:.3f}%;height:{l["height"]/CH*100:.3f}%;--i:{l["n"]}"><img src="media/logo/letter_{l["n"]}.png" alt=""></span>' for l in L["letters"])
    return f'''<div class="loader" aria-hidden="true">
<div class="logo-stack"><div class="logo-anim"><svg class="mark" viewBox="0 0 470 470" aria-hidden="true">{paths}</svg><div class="word"><div class="clip">{letters}</div></div></div><p class="loader-sub">{E(B["sub"])}</p></div>
<div class="meta"><span>{E(B["sub"])} · Paris</span><span><span data-pct>000</span> / 100</span></div><div class="bar"><i></i></div></div>'''

def nav(current=""):
    items = "".join(f'<a class="link" href="{h}"{" aria-current=page" if h == current else ""}><span class="n">{n}</span>{E(t)}</a>' for n, t, h in D["nav"])
    menu = "".join(f'<a class="item" href="{h}"{" aria-current=page" if h == current else ""}><span class="n">{n}</span>{E(t)}</a>' for n, t, h in D["nav"])
    return f'''<nav class="nav" data-nav aria-label="Main">
  <a class="brand" href="index.html" aria-label="{E(B["name"])} {E(B["sub"])}"><img class="logo" src="media/logo/logo_white.png" alt=""><small>{E(B["sub"])}</small></a>
  <div class="nav-items">{items}</div>
  <button class="burger" aria-expanded="false" aria-controls="menu">Menu</button>
</nav>
<div class="menu" id="menu">{menu}<div class="foot"><a class="btn btn-accent" href="contact.html">Get in touch <span class="arrow">→</span></a><a href="mailto:{B["email"]}">{B["email"]}</a><div class="meta"><a href="{B["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><span>Paris · France</span></div></div></div>'''

def footer():
    cols = "".join(f'<a class="link" href="{h}">{E(t)}</a>' for n, t, h in D["nav"])
    return f'''<footer class="section footer" data-theme="dark">
  <div class="container">
    <div class="cols">
      <div class="col wide"><p class="title">Mission</p><p class="body-l measure-l">We capture missions and frame reality. Production house and agency for the people building real technology.</p></div>
      <div class="col"><p class="title">Site</p>{cols}<a class="link" href="legal.html">Legal</a></div>
      <div class="col"><p class="title">Contact</p><a class="link" href="mailto:{B["email"]}">{B["email"]}</a><a class="link" href="{B["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><p class="body-s muted" style="margin-top:var(--s-3)">{E(B["address"])}</p></div>
    </div>
    <div class="big" aria-hidden="true">{E(B["name"])}</div>
    <div class="legal caption"><span>© {datetime.date.today().year} {E(B["name"])} {E(B["sub"]).upper()}</span><span>Production house · Agency · Paris</span><a class="link" href="#top">Back to top</a></div>
  </div>
</footer>'''

def scripts():
    return f'''<script src="js/lib/lenis.min.js"></script>
<script src="js/lib/gsap.min.js"></script>
<script src="js/lib/ScrollTrigger.min.js"></script>
<script src="js/app.js?v={STAMP}"></script>
<script src="js/site.js?v={STAMP}"></script>
</body></html>'''

def contact_block(theme="light", idx="05"):
    c = D["contact"]
    return f'''<section class="section" data-theme="{theme}" id="contact">
  <div class="container">
    <div class="sec-head"><span class="num">{idx} · Contact</span><h2 class="ttl h1">{E(c["title"])}</h2><p class="aside">{E(c["sub"])}</p></div>
    <div class="contact-block">
      <div class="lead stack">
        <p class="eyebrow">Get in touch</p>
        <p class="body-l measure-l">Tell us what you are building, who needs to understand it, and when. We answer with a first angle, not a brochure.</p>
        <p><a class="link" href="mailto:{B["email"]}">{B["email"]}</a></p>
        <p class="body-s muted">{E(B["address"])}</p>
      </div>
      <div class="form-wrap">
        <form class="form" data-mailto="{B["email"]}" novalidate>
          <div class="field"><label for="f-name">Name*</label><input id="f-name" name="name" type="text" required autocomplete="name"></div>
          <div class="field"><label for="f-email">Email*</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
          <div class="field full"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
          <div class="field full"><label for="f-msg">What are you building?</label><textarea id="f-msg" name="message"></textarea></div>
          <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="full row between"><span class="note">No backend yet · opens your email app</span><button class="btn btn-accent" type="submit">Send <span class="arrow">→</span></button></div>
        </form>
      </div>
    </div>
  </div>
</section>'''

def project_card(p, wide=False):
    media = (f'<video class="media" data-hover muted playsinline loop preload="none" poster="{p["poster"]}" src="{p["video"]}"></video>' if p.get("video")
             else f'<img class="media" src="{p["img"]}" alt="{E(p["name"])}" loading="lazy">')
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in p["tags"])
    href = p["link"] or "portfolio.html"; ext = ' target="_blank" rel="noopener"' if p["link"] else ""
    return f'''<a class="project{" wide" if wide else ""}" href="{href}"{ext} data-reveal>{media}
      <div class="meta"><div><p class="sector">{E(p["sector"])}</p><p class="name">{E(p["name"])}</p></div><div class="tags">{tags}</div></div></a>'''

# ---------------------------------------------------------------- HOME
def home():
    h = D["hero"]; o = D["offer"]; a = D["area"]
    marquee = "".join(f"<span>{E(n)}</span>" for n in D["partners"])
    faces = "".join(f'''<a class="feature" href="{f["href"]}" data-reveal><span class="k">{f["k"]}</span><span class="t">{E(f["t"])}</span><span class="d">{E(f["d"])}</span><span class="go">→</span></a>''' for f in D["faces"])
    offers = "".join(f'''<a class="offer" href="{i["href"]}" data-reveal="{n*0.05:.2f}"><img src="{i["img"]}" alt="" loading="lazy"><span class="letter"><span>—— {i["letter"]}</span><span>{E(i["face"])}</span></span><span class="t">{E(i["t"])}</span><span class="d">{E(i["d"])}</span><ul>{"".join(f"<li>{E(x)}</li>" for x in i["list"])}</ul><span class="go">Learn more →</span></a>''' for n, i in enumerate(o["items"]))
    work = [p for p in D["projects"] if p.get("home")]
    cards = "".join(row(i, p) for i, p in enumerate(work))
    photos = "".join(f'<figure><img src="{src}" alt="" loading="lazy"><figcaption>Adverse area · {i+1:02d}</figcaption></figure>' for i, src in enumerate(a["photos"]))
    subnav = "".join(f'<a href="#{i}"><span class="n">{n}</span>{t}</a>' for n, t, i in [("01","Two faces","faces"),("02","Offer","offer"),("03","Work","work"),("04","Area","area"),("05","Contact","contact")])
    return f'''{head("Adverse Production · Production house and agency for real technology", "At Adverse Production, we showcase the most outstanding tech projects through high-end video productions and the agency work around them: strategy, identity, spaces.")}
{loader()}
{nav("index.html")}
<main id="top">
<section class="hero" data-theme="dark" id="home">
  <div class="bg"><video autoplay muted loop playsinline poster="{h["poster"]}" src="{h["video"]}"></video></div>
  <span class="corner tl">Paris · France</span><span class="corner tr">Production<br>+ Agency</span>
  <div class="container">
    <p class="eyebrow" data-reveal>{E(h["eyebrow"])}</p>
    <h1 class="display-1 measure" style="margin-top:var(--s-5)" data-reveal="0.1">{E(h["title"])}</h1>
    <div class="grid" style="margin-top:var(--s-7)">
      <p class="body-l span-5 muted" data-reveal="0.2">{E(h["sub"])}</p>
      <div class="span-7 cta" style="justify-content:flex-end;align-self:end" data-reveal="0.3"><a class="btn btn-accent" href="portfolio.html">See the work <span class="arrow">→</span></a><a class="btn" href="#contact">Get in touch</a></div>
    </div>
  </div>
</section>
<section class="section-s" data-theme="dark" id="partners" style="background:var(--bg);color:var(--fg)">
  <div class="container partners-head"><p class="eyebrow">They trusted us</p><p class="caption">Selected clients and partners</p></div>
  <div class="marquee" style="margin-top:var(--s-5)"><div class="track">{marquee}</div></div>
</section>
<nav class="subnav" aria-label="Sections">{subnav}</nav>
<section class="section" data-theme="light" id="faces">
  <div class="container">
    <div class="sec-head"><span class="num">01 · Two faces</span><h2 class="ttl h1">One crew. Two faces.</h2><p class="aside">The production house makes the film. The agency makes it land. Same people, same obsession.</p></div>
    <div class="features">{faces}</div>
  </div>
</section>
<section class="section" data-theme="dark" id="offer">
  <div class="container">
    <div class="sec-head"><span class="num">02 · What we offer</span><h2 class="ttl h1">{E(o["title"])}</h2><p class="aside">{E(o["sub"])}</p></div>
    <div class="hgrid">{offers}</div>
  </div>
</section>
<section class="section" data-theme="dark" id="work" style="padding-top:0">
  <div class="container">
    <div class="sec-head"><span class="num">03 · Selected work</span><h2 class="ttl h1">Stories of innovation, captured in motion.</h2><a class="aside link" href="portfolio.html">All projects →</a></div>
    <div class="rows">{cards}</div>
    <div class="row" style="justify-content:flex-end;margin-top:var(--s-6)"><a class="btn" href="portfolio.html">All {len(D["projects"]):02d} projects <span class="arrow">→</span></a></div>
  </div>
</section>
<section class="section" data-theme="gray" id="area">
  <div class="container">
    <p class="eyebrow" data-reveal>{E(a["eyebrow"])}</p>
    <div class="grid" style="margin-top:var(--s-5);margin-bottom:var(--s-8)">
      <h2 class="h1 span-8" data-reveal="0.1">{E(a["title"])}</h2>
      <p class="body-l span-4 muted" style="align-self:end" data-reveal="0.2">{E(a["sub"])}</p>
    </div>
    <div class="strip">{photos}</div>
    <div class="stats" style="margin-top:var(--s-9)">
      <div><div class="stat"><span data-roll="{len(D["projects"])}" data-pad="2">00</span></div><p class="caption" style="margin-top:var(--s-3)">Projects online</p></div>
      <div><div class="stat"><span data-roll="{len(o["items"])}" data-pad="2">00</span></div><p class="caption" style="margin-top:var(--s-3)">Offer pillars</p></div>
      <div><div class="stat"><span data-roll="2" data-pad="2">00</span></div><p class="caption" style="margin-top:var(--s-3)">Faces · production + agency</p></div>
      <div><div class="stat"><span data-roll="1" data-pad="2">00</span></div><p class="caption" style="margin-top:var(--s-3)">Crew · film makers, ad creators, VCs, sales, lobbyists</p></div>
    </div>
  </div>
</section>
{contact_block("light", "05")}
</main>
{footer()}
{scripts()}'''

# ---------------------------------------------------------------- MISSION PAGES (Anduril /space)
def mission(key, current, subtitle):
    m = D[key]; ch = m["chapters"]; n = len(ch)
    caps = "".join(f'<li><a href="#{c["id"]}"><span><span class="i">{i+1:02d}</span>{E(c["t"])}</span></a></li>' for i, c in enumerate(ch))
    def media(c):
        return (f'<video data-hover autoplay muted loop playsinline preload="metadata" poster="{c["poster"]}" src="{c["media"]}"></video>' if c.get("media") else f'<img src="{c["img"]}" alt="" loading="lazy">')
    chapters = "".join(f'''<article class="chapter" id="{c["id"]}" data-title="{E(c["t"])}">
      <div class="txt"><p class="idx"><b>{i+1:02d}</b> / {n:02d}</p><h3 class="ttl">{E(c["t"])}</h3><p class="words">{E(c["w"])}</p></div>
      <div class="media">{media(c)}</div>
    </article>''' for i, c in enumerate(ch))
    lines = "".join(f'<span class="sp" data-reveal="{i*0.08:.2f}">{E(l)}</span>' for i, l in enumerate(m["statement_lines"]))
    specs = "".join(f'''<div class="spec-card" data-reveal="{i*0.06:.2f}"><span class="k">Spec · {i+1:02d}</span><p class="card-title">{E(s["t"])}</p><dl>{"".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in s["rows"])}</dl></div>''' for i, s in enumerate(m["specs"]))
    partners = "".join(f'''<details class="acc"{" open" if i == 0 else ""}><summary><span class="k">{i+1:02d}</span><span class="t">{E(PROJ[pid]["name"])}</span><span class="s">{E(PROJ[pid]["sector"])}</span><span class="plus">+</span></summary>
      <div class="body"><p>{E(PROJ[pid]["d"])}</p><div class="tags">{"".join(f'<span class="tag">{E(t)}</span>' for t in PROJ[pid]["tags"])}</div></div></details>''' for i, pid in enumerate(m["partners"]))
    other = "agency.html" if key == "production" else "production.html"; other_t = "Agency" if key == "production" else "Production"
    return f'''{head(f"{m['title']} · Adverse Production", m["statement"])}
{loader()}
{nav(current)}
<main id="top">
<section class="mission-hero" data-theme="dark">
  <div class="bg"><video autoplay muted loop playsinline poster="{m["poster"]}" src="{m["video"]}"></video></div>
  <div class="container stack-l">
    <p class="short" data-reveal>{E(m["tag"])}</p>
    <h1 class="display-1" data-reveal="0.1">{E(m["title"])}</h1>
    <p class="statement" data-reveal="0.2">{E(m["statement"])}</p>
    <p class="caption" data-reveal="0.3">{E(subtitle)}</p>
  </div>
</section>
<section class="section" data-theme="dark">
  <div class="container caps"><h4>Capabilities</h4><ul>{caps}</ul></div>
</section>
<div class="chap-counter" data-theme="dark"><span><b data-cur>01</b> / {n:02d}</span><span class="bar"><i></i></span><span data-name></span></div>
<section class="section" data-theme="dark" style="padding-top:0">
  <div class="container">{chapters}</div>
</section>
<section class="statement" data-theme="light" style="background:var(--bg);color:var(--fg)">
  <div class="container">{lines}</div>
</section>
<section class="section" data-theme="light" style="padding-top:0">
  <div class="container">
    <div class="sec-head"><span class="num">Specs</span><h2 class="ttl h2">What a mission looks like on paper.</h2><p class="aside">Formats, deliveries and the crew on it. The brief decides the rest.</p></div>
    <div class="specs">{specs}</div>
  </div>
</section>
<section class="section" data-theme="dark">
  <div class="container">
    <div class="sec-head"><span class="num">Partners</span><h2 class="ttl h2">{E(m["partners_title"])}</h2><a class="aside link" href="portfolio.html">All projects →</a></div>
    <div class="accordion">{partners}</div>
  </div>
</section>
<section class="section section-s" data-theme="accent">
  <div class="container row between"><span class="h3">The other face: {other_t}.</span><a class="btn" href="{other}">See {other_t} <span class="arrow">→</span></a></div>
</section>
{contact_block("light", "Contact")}
</main>
{footer()}
{scripts()}'''

# ---------------------------------------------------------------- PORTFOLIO
def row(i, p):
    """One project row: media left, sector + name + text middle, tags + link right. Used on the portfolio page and on the home."""
    media = (f'<video data-hover muted playsinline loop preload="none" poster="{p["poster"]}" src="{p["video"]}"></video>' if p.get("video") else f'<img src="{p["img"]}" alt="{E(p["name"])}" loading="lazy">')
    tags = "".join(f'<span class="tag">{E(t)}</span>' for t in p["tags"])
    link = f'<a class="btn" href="{p["link"]}" target="_blank" rel="noopener">Visit <span class="arrow">→</span></a>' if p["link"] else '<span class="caption">Unreleased</span>'
    return f'''<article class="prow" data-tags="{E("|".join(p["tags"]))}" data-reveal><div class="m">{media}</div>
        <div class="i"><p class="meta">{i+1:02d} · {E(p["sector"])}</p><h3 class="name">{E(p["name"])}</h3><p class="d">{E(p["d"])}</p></div>
        <div class="r"><div class="tags">{tags}</div>{link}</div></article>'''

def portfolio():
    pf = D["portfolio"]
    tabs = "".join(f'<button class="tab" role="tab" data-filter="{"all" if f == "All" else E(f)}" aria-selected="{"true" if f == "All" else "false"}">{E(f)}</button>' for f in pf["filters"])
    rows = "".join(row(i, p) for i, p in enumerate(D["projects"]))
    return f'''{head("Portfolio · Adverse Production", "Stories of innovation, captured in motion. Selected work for Ion-X, Ægir, Alta Ares, Electronic Bird Control, Oscar Mike, Safran and Naval Group.")}
{loader()}
{nav("portfolio.html")}
<main id="top">
<section class="section page-hero" data-theme="dark">
  <div class="container">
    <p class="eyebrow" data-reveal>Portfolio · {len(D["projects"]):02d} projects</p>
    <h1 class="display-1" style="margin-top:var(--s-5)" data-reveal="0.1">{E(pf["title_lines"][0])}<br>{E(pf["title_lines"][1])}</h1>
    <div class="tabs" role="tablist" style="margin-top:var(--s-8)" data-reveal="0.2">{tabs}</div>
  </div>
</section>
<section class="section" data-theme="dark" style="padding-top:0">
  <div class="container rows">{rows}</div>
</section>
{contact_block("light", "Contact")}
</main>
{footer()}
{scripts()}'''

# ---------------------------------------------------------------- CONTACT / LEGAL / 404
def contact():
    c = D["contact"]
    return f'''{head("Contact · Adverse Production", c["title"])}
{loader()}
{nav("contact.html")}
<main id="top">
<section class="section page-hero" data-theme="dark" style="padding-bottom:0">
  <div class="container"><p class="eyebrow" data-reveal>Contact</p><h1 class="display-2" style="margin-top:var(--s-5)" data-reveal="0.1">{E(c["title"])}</h1></div>
</section>
{contact_block("dark", "Contact")}
</main>
{footer()}
{scripts()}'''

def legal():
    lines = [l for l in open(os.path.join(ROOT, "data/legal.txt"), encoding="utf-8").read().splitlines() if l.strip()]
    heads = {"Contact Information", "Hosting", "Domain Name Provider", "Intellectual Property", "Liability", "External Links", "Privacy"}
    body = ""; i = 0
    while i < len(lines):
        l = lines[i]
        if l in heads: body += f'<h3 class="h3">{E(l)}</h3>'
        elif l.startswith("©"): pass
        elif l == "This website is hosted by": body += f'<p>{E(l)} {E(lines[i+1])} {E(lines[i+2])}</p>'; i += 2
        elif l == "The domain name was purchased through": body += f'<p>{E(l)} {E(lines[i+1])} {E(lines[i+2])}</p>'; i += 2
        elif l == "Framer B.V.": body += f'<p>This website is hosted by a static host chosen by Adverse Production. Previous host: Framer B.V., Singel 542, 1017 AZ Amsterdam, The Netherlands.</p>'
        else: body += f'<p>{E(l)}</p>'
        i += 1
    return f'''{head("Legal · Adverse Production", "Legal notice of adverseprod.com")}
{nav("legal.html")}
<main id="top">
<section class="section page-hero" data-theme="light">
  <div class="container"><p class="eyebrow">Legal</p><h1 class="display-2" style="margin-top:var(--s-5)">Legal notice.</h1></div>
</section>
<section class="section" data-theme="light" style="padding-top:0"><div class="container legal-text stack">{body}</div></section>
</main>
{footer()}
{scripts()}'''

def notfound():
    return f'''{head("404 · Adverse Production", "Page not found")}
{nav()}
<main id="top">
<section class="hero" data-theme="dark">
  <div class="bg"><video autoplay muted loop playsinline poster="media/web/MLWPbW1dUQawJLhhun3dBwpgJak.jpg" src="media/web/MLWPbW1dUQawJLhhun3dBwpgJak.mp4"></video></div>
  <div class="container stack-l"><p class="eyebrow">404</p><h1 class="display-1">Lost in the mission.</h1><p class="body-l muted measure-l">This page does not exist, or not yet. The rest of the site does.</p><div class="row"><a class="btn btn-accent" href="index.html">Home <span class="arrow">→</span></a><a class="btn" href="portfolio.html">Portfolio</a></div></div>
</section>
</main>
{footer()}
{scripts()}'''

PAGES = {"index.html": home(), "production.html": mission("production", "production.html", "The production house. Shot where the technology lives."),
         "agency.html": mission("agency", "agency.html", "The agency. Built around the film so the story holds."),
         "portfolio.html": portfolio(), "contact.html": contact(), "legal.html": legal(), "404.html": notfound()}
for fn, out in PAGES.items():
    open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(out); print(f"{len(out):7d} B  {fn}")
