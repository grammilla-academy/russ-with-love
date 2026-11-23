"""Build dependency-free HTML. Run: python build.py. Never includes originals/ or qa/."""
from pathlib import Path
import html
import json
import hashlib
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
BASE = 'https://grammilla-academy.github.io/russ-with-love/'
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
ROUTES = {'en': '', 'it': 'it/', 'ru': 'ru/'}
GOOGLE_SITE_VERIFICATION = 'zuluS6yuf3MvCARNWKIKWjeLZQMuFsAksyqGJu3H5Sc'
SOCIAL = [
    ('YouTube', 'https://www.youtube.com/@russwithlove', '<rect x="2" y="5" width="20" height="14" rx="4"/><path d="m10 8 6 4-6 4Z" fill="var(--paper)"/>'),
    ('Instagram', 'https://www.instagram.com/russ.with.love/', '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2"/>'),
    ('Facebook', 'https://www.facebook.com/profile.php?id=61594652851311&sk=reels_tab', '<path d="M14 22v-9h3l.5-4H14V7c0-1 .4-2 2-2h2V1h-3c-4 0-6 2-6 6v2H6v4h3v9Z"/>'),
    ('TikTok', 'https://www.tiktok.com/@russ.with.love', '<path d="M14 2h4c0 3 2 5 5 5v4c-2 0-4-1-5-2v8a7 7 0 1 1-7-7v4a3 3 0 1 0 3 3Z"/>'),
    ('Telegram', 'https://t.me/russ_with_love', '<path d="M22 3 18 21l-6-5-3 3v-6l10-7-12 5-5-2Z"/>')
]

def e(s):
    return html.escape(str(s), quote=True)

def paragraphs(items):
    return ''.join(f'<p>{e(x)}</p>' for x in items)

def head(lang, privacy=False):
    d = DATA[lang]
    prefix = '../' if lang != 'en' else './'
    route = ROUTES[lang]
    url = BASE + route + ('privacy.html' if privacy else '')
    title = d['privacyTitle'] + ' | Russ with Love' if privacy else d['title']
    description = d['privacyIntro'] if privacy else d['description']
    style_version = hashlib.sha256((ROOT/'site.css').read_bytes()).hexdigest()[:10]
    alternates = ''.join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}{"privacy.html" if privacy else ""}">' for k, v in ROUTES.items())
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#fbf8f3"><meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">
<link rel="canonical" href="{url}">{alternates}<link rel="alternate" hreflang="x-default" href="{BASE}{'privacy.html' if privacy else ''}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Russ with Love"><meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:locale" content="{dict(en='en_GB',it='it_IT',ru='ru_RU')[lang]}"><meta property="og:image" content="{BASE}assets/social.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(d['portraitAlt'])}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{BASE}assets/social.jpg"><meta name="twitter:image:alt" content="{e(d['portraitAlt'])}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="icon" sizes="32x32" href="{prefix}assets/favicon.png"><link rel="stylesheet" href="{prefix}site.css?v={style_version}"></head><body>
<a class="skip" href="#main">{e(d['skip'])}</a><header><div class="wrap topbar"><a class="brand" href="./" lang="en">Russ <em>with Love</em><span class="heart" aria-hidden="true">♡</span></a>
<nav aria-label="{e(d['nav'][0] + ' / ' + d['nav'][3])}">{''.join(f'<a href="./#{anchor}">{e(label)}</a>' for anchor,label in zip(['about','approach','lessons','contact'],d['nav']))}</nav>
<div class="languages" role="navigation" aria-label="{e(d['languageLabel'])}">{''.join(f'<a lang="{k}" hreflang="{k}" href="{prefix}{v}{"privacy.html" if privacy else ""}"'+(' aria-current="page"' if k==lang else '')+f'>{k.upper()}</a>' for k,v in ROUTES.items())}</div></div></header>'''

def footer(lang):
    d = DATA[lang]
    return f'''<footer><div class="wrap footer-row"><span>© 2026 Russ with Love · Liuba</span><span>P.IVA 04015341201</span><a href="./privacy.html">{e(d['privacyLabel'])}</a></div></footer></body></html>'''

def prices(d, pair=False):
    rows = d['pairPackages'] if pair else d['individualPackages']
    values = [(160,176),(370,400)] if pair else [(30,33),(140,155),(270,298)]
    return f'''<div class="pricing"><h3>{e(d['pairPricingTitle'] if pair else d['pricingTitle'])}</h3><p class="time">{e(d['pairTimes'] if pair else d['individualTimes'])}</p><div class="table-scroll"><table><caption class="sr-only">{e(d['pairPricingTitle'] if pair else d['pricingTitle'])}</caption><thead><tr><th scope="col">{e(d['package'])}</th><th scope="col">{e(d['day'])}</th><th scope="col">{e(d['evening'])}</th></tr></thead><tbody>{''.join(f'<tr><th scope="row">{e(label)}</th><td>€{day}</td><td>€{evening}</td></tr>' for label,(day,evening) in zip(rows,values))}</tbody></table></div></div>'''

def build(lang):
    d = DATA[lang]
    prefix = '../' if lang != 'en' else './'
    mail = 'mailto:grammilla.academy@gmail.com?subject=' + quote(d['emailSubject'])
    cta = lambda label: f'<a class="button" href="{mail}">{e(label)}</a>'
    graph = {'@context':'https://schema.org','@graph':[
        {'@type':'Person','@id':BASE+'#liuba','name':'Liuba','alternateName':'Люба','jobTitle':{'en':'Russian language teacher','it':'Insegnante di russo','ru':'Преподаватель русского языка'}[lang], 'description':d['about'][0], 'knowsLanguage':['Russian','English','Italian'], 'url':BASE,'image':BASE+'assets/liuba-1080.webp','sameAs':[s[1] for s in SOCIAL]},
        {'@type':'WebSite','@id':BASE+'#website','name':'Russ with Love','url':BASE,'inLanguage':['en','it','ru']},
        {'@type':'WebPage','@id':BASE+ROUTES[lang]+'#page','url':BASE+ROUTES[lang], 'name':d['title'],'description':d['description'],'inLanguage':lang,'isPartOf':{'@id':BASE+'#website'},'about':{'@id':BASE+'#liuba'},'primaryImageOfPage':{'@type':'ImageObject','contentUrl':BASE+'assets/liuba-1080.webp','width':1080,'height':1080,'caption':d['portraitAlt']}}]}
    page = head(lang)+f'''<main id="main"><div class="wrap"><section class="hero" aria-labelledby="hero-title"><div><p class="eyebrow">{e(d['eyebrow'])}</p><h1 id="hero-title">{d['h1']}</h1>{paragraphs(d['hero'])}<p class="experience">{e(d['experience'])}</p>{cta(d['cta'])}<p class="note">{e(d['emailNote'])}</p></div><figure class="portrait"><img src="{prefix}assets/liuba-1080.webp" srcset="{prefix}assets/liuba-540.webp 540w, {prefix}assets/liuba-1080.webp 1080w" sizes="(max-width:740px) calc(100vw - 36px), (max-width:1250px) 45vw, 520px" width="1254" height="1254" alt="{e(d['portraitAlt'])}" fetchpriority="high"><figcaption>{e(d['caption'])}</figcaption></figure></section><div class="intro-line">{''.join(f'<span>{e(x)}</span>' for x in d['strip'])}</div>
<section class="section about" id="about" aria-labelledby="about-title"><div><p class="eyebrow">{e(d['aboutLabel'])}</p><h2 id="about-title">{e(d['aboutTitle'])}</h2><p class="aside">{e(d['aside'])}</p></div><div class="body">{paragraphs(d['about'])}</div></section></div>
<section class="tint section" aria-labelledby="audience-title"><div class="wrap"><div class="section-heading"><p class="eyebrow">{e(d['audienceLabel'])}</p><h2 id="audience-title">{e(d['audienceTitle'])}</h2><p>{e(d['audienceIntro'])}</p></div><div class="audience">{''.join(f'<article><h3>{e(t)}</h3><p>{e(p)}</p></article>' for t,p in d['audience'])}</div></div></section>
<div class="wrap"><section class="section approach" id="approach" aria-labelledby="approach-title"><div><p class="eyebrow">{e(d['approachLabel'])}</p><h2 id="approach-title">{d['approachTitle']}</h2><p class="steps">{e(d['steps'])}</p></div><div class="body">{paragraphs(d['approach'])}</div></section>
<section class="section lessons" id="lessons" aria-labelledby="lessons-title"><div class="section-heading"><p class="eyebrow">{e(d['formatsLabel'])}</p><h2 id="lessons-title">{e(d['formatsTitle'])}</h2></div><div class="formats"><article class="format"><span class="tag">{e(d['individualLabel'])}</span><h3>{d['individualTitle']}</h3>{paragraphs(d['individual'])}<p class="meta">{e(d['individualMeta'])}</p></article><article class="format"><span class="tag">{e(d['groupLabel'])}</span><h3>{d['groupTitle']}</h3>{paragraphs(d['group'])}<p class="meta">{e(d['groupMeta'])}</p><p>{e(d['groupLevel'])}</p><p><strong>{e(d['groupPrice'])}</strong></p></article></div>
{prices(d)}<div class="pair-intro"><h3>{e(d['pairTitle'])}</h3><p>{e(d['pairText'])}</p></div>{prices(d,True)}<p class="time">{e(d['timezone'])}</p><p class="price-note">{e(d['priceNote'])}</p><a class="text-link" href="#start">{e(d['cta'])}</a></section>
<section class="section practical" aria-labelledby="practical-title"><div><p class="eyebrow">{e(d['practicalLabel'])}</p><h2 id="practical-title">{d['practicalTitle']}</h2></div><ul>{''.join(f'<li><strong>{e(t)}</strong>{e(p)}</li>' for t,p in d['practical'])}</ul></section>
<section class="section reviews" aria-labelledby="reviews-title"><div class="section-heading"><p class="eyebrow">Russ with Love</p><h2 id="reviews-title">{e(d['reviewsTitle'])}</h2><p>{e(d['reviewNote'])}</p></div><div class="review-grid">{''.join(f'<figure><blockquote><p>“{e(text)}”</p></blockquote><figcaption>{e(name)}<span>{e(d["originalEnglish"] if name=="Corinne" else d["translated"])}</span></figcaption></figure>' for name,text in d['reviews'])}</div></section></div>
<section class="call section" id="start" aria-labelledby="call-title"><div class="wrap call-grid"><div><p class="eyebrow">{e(d['callLabel'])}</p><h2 id="call-title">{d['callTitle']}</h2></div><div class="body">{paragraphs(d['call'])}{cta(d['cta2'])}<p class="note">{e(d['emailNote'])}</p></div></div></section>
<div class="wrap"><section class="app-block section" aria-labelledby="app-title"><div><p class="eyebrow">{e(d['appLabel'])}</p><h2 id="app-title">{e(d['appTitle'])}</h2><div class="app-name" lang="en">Grammilla</div></div><div class="body">{paragraphs(d['app'])}<a class="text-link" href="https://gramillaapp.github.io/grammilla-support/">{e(d['appCta'])}</a></div></section>
<section class="section faq" aria-labelledby="faq-title"><h2 id="faq-title">{e(d['faqTitle'])}</h2>{''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in d['faq'])}</section>
<section class="contact" id="contact" aria-labelledby="contact-title"><div><h2 id="contact-title">{e(d['contactTitle'])}</h2><p>{e(d['contactText'])}</p><a class="text-link email" href="mailto:grammilla.academy@gmail.com">grammilla.academy@gmail.com</a></div><div><p>{e(d['socialIntro'])}</p><div class="socials">{''.join(f'<a href="{e(url)}"><svg viewBox="0 0 24 24" aria-hidden="true">{svg}</svg>{name}</a>' for name,url,svg in SOCIAL)}</div></div></section></div></main><script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script>'''+footer(lang)
    path = ROOT / ROUTES[lang]
    path.mkdir(parents=True, exist_ok=True)
    (path/'index.html').write_text(page,encoding='utf-8')
    privacy = head(lang,True)+f'<main class="wrap privacy" id="main"><p class="eyebrow">Russ with Love</p><h1>{e(d["privacyTitle"])}</h1><p>{e(d["privacyIntro"])}</p>'+''.join(f'<h2>{e(t)}</h2><p>{e(p)}</p>' for t,p in d['privacySections'])+f'<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy Statement</a></p><a class="text-link" href="./">{e(d["back"])}</a></main>'+footer(lang)
    (path/'privacy.html').write_text(privacy,encoding='utf-8')

if __name__ == '__main__':
    for language in DATA:
        build(language)
    urls = [BASE + r + p for r in ROUTES.values() for p in ['', 'privacy.html']]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /russ-with-love/\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    print('Built EN / IT / RU, three privacy notices, sitemap.xml and robots.txt.')
