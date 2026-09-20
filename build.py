#!/usr/bin/env python3
"""Builds the static pages for All Wrapped Up (allwrappeduptn.com).
Run:  python3 build.py   — writes *.html + sitemap.xml next to this file.
All page copy lives in this file so nav/footer/SEO tags stay consistent."""
import datetime, html, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://allwrappeduptn.com"
BIZ = "All Wrapped Up"
TAG = "Ribbons & Bows"
OWNER = "Amiebeth Thearp"
PHONE = "540-340-4905"
PHONE_TEL = "+15403404905"
EMAIL = "abthearp@gmail.com"
CITY = "Sweetwater"
REGION = "TN"
ZIP = "37874"
AREA = ["Sweetwater", "Madisonville", "Athens", "Loudon", "Lenoir City", "Maryville", "Farragut", "Knoxville", "Cleveland", "Ooltewah", "Chattanooga"]
TODAY = datetime.date.today().isoformat()
# Where quote requests are delivered. Kept separate from the public EMAIL so the site
# can be tested without contacting Amiebeth. Change to EMAIL when she is ready, rebuild,
# push, and submit one test form: FormSubmit then sends a one-time activation link there.
FORM_EMAIL = "felicia.nevin@gmail.com"
FORM_ACTION = f"https://formsubmit.co/{FORM_EMAIL}"

NAV = [
    ("index.html", "Home"),
    ("corporate-gift-wrapping.html", "Corporate"),
    ("services.html", "Occasions"),
    ("pricing.html", "Pricing"),
    ("holiday-gift-wrapping.html", "Holiday"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
]

# ---------- SVG helpers ----------
def bow_logo():
    return '''<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 34h48v20a4 4 0 0 1-4 4H12a4 4 0 0 1-4-4z" fill="#f4a6bf"/><rect x="6" y="26" width="52" height="10" rx="2" fill="#e5648f"/><rect x="27" y="26" width="10" height="32" fill="#fde4ee"/><path d="M32 26c-6-2-14-10-10-14s10 6 10 14zm0 0c6-2 14-10 10-14s-10 6-10 14z" fill="#b23a5e"/><circle cx="32" cy="25" r="4" fill="#8e2c4a"/></svg>'''

def gift_svg(paper="#fde4ee", ribbon="#e5648f", dots="#fff", bow="#b23a5e", accent="#fff6f9"):
    return f'''<svg viewBox="0 0 200 200" aria-hidden="true">
<defs><pattern id="d{abs(hash(paper+ribbon))%99999}" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.8" fill="{dots}"/></pattern></defs>
<rect x="30" y="86" width="140" height="94" rx="8" fill="{paper}"/>
<rect x="22" y="70" width="156" height="30" rx="5" fill="{accent}" stroke="{paper}" stroke-width="2"/>
<rect x="86" y="70" width="28" height="110" fill="{ribbon}"/><rect x="86" y="70" width="28" height="110" fill="url(#d{abs(hash(paper+ribbon))%99999})"/>
<rect x="22" y="78" width="156" height="14" fill="{ribbon}"/><rect x="22" y="78" width="156" height="14" fill="url(#d{abs(hash(paper+ribbon))%99999})"/>
<path d="M100 74c-14-4-40-26-30-38s26 18 30 38zm0 0c14-4 40-26 30-38s-26 18-30 38z" fill="{bow}"/>
<path d="M100 74c-6 6-18 18-26 12s10-16 26-12zm0 0c6 6 18 18 26 12s-10-16-26-12z" fill="{ribbon}"/>
<circle cx="100" cy="72" r="8" fill="{bow}"/><circle cx="97" cy="69" r="2.5" fill="#fff" opacity=".7"/>
</svg>'''

HERO_SVG = '''<svg viewBox="0 0 480 440" aria-hidden="true">
<defs>
 <pattern id="pd" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="2.2" fill="#fff"/></pattern>
 <linearGradient id="pg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fde4ee"/></linearGradient>
 <linearGradient id="rg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f4a6bf"/><stop offset="1" stop-color="#e5648f"/></linearGradient>
 <linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="#e5648f"/><stop offset="1" stop-color="#b23a5e"/></linearGradient>
</defs>
<ellipse cx="240" cy="420" rx="170" ry="14" fill="#f4a6bf" opacity=".35"/>
<!-- small back box -->
<g transform="translate(300 250)">
 <rect x="0" y="30" width="130" height="120" rx="8" fill="#2b2224"/>
 <rect x="-6" y="14" width="142" height="30" rx="5" fill="#3d3033"/>
 <rect x="54" y="14" width="22" height="136" fill="#c9a227"/><rect x="-6" y="24" width="142" height="12" fill="#c9a227"/>
 <path d="M65 18c-10-2-30-20-22-28s20 14 22 28zm0 0c10-2 30-20 22-28s-20 14-22 28z" fill="#e8c65a"/><circle cx="65" cy="16" r="6" fill="#c9a227"/>
</g>
<!-- main box -->
<g transform="translate(40 120)">
 <rect x="20" y="70" width="300" height="230" rx="14" fill="url(#pg)" stroke="#f9c7d8" stroke-width="3"/>
 <rect x="4" y="34" width="332" height="56" rx="10" fill="#fff" stroke="#f9c7d8" stroke-width="3"/>
 <rect x="140" y="34" width="60" height="266" fill="url(#rg)"/><rect x="140" y="34" width="60" height="266" fill="url(#pd)"/>
 <rect x="4" y="48" width="332" height="28" fill="url(#rg)"/><rect x="4" y="48" width="332" height="28" fill="url(#pd)"/>
 <!-- bow -->
 <path d="M170 44c-28-6-86-52-66-78s60 40 66 78z" fill="url(#bg)"/><path d="M170 44c-28-6-86-52-66-78s60 40 66 78z" fill="url(#pd)" opacity=".8"/>
 <path d="M170 44c28-6 86-52 66-78s-60 40-66 78z" fill="url(#bg)"/><path d="M170 44c28-6 86-52 66-78s-60 40-66 78z" fill="url(#pd)" opacity=".8"/>
 <path d="M170 44c-12 14-36 40-54 26s22-34 54-26z" fill="#e5648f"/><path d="M170 44c12 14 36 40 54 26s-22-34-54-26z" fill="#e5648f"/>
 <path d="M170 44c-12 14-36 40-54 26s22-34 54-26z" fill="url(#pd)" opacity=".7"/><path d="M170 44c12 14 36 40 54 26s-22-34-54-26z" fill="url(#pd)" opacity=".7"/>
 <circle cx="170" cy="42" r="16" fill="#b23a5e"/><circle cx="164" cy="36" r="5" fill="#fff" opacity=".6"/>
 <!-- gift tag -->
 <g transform="rotate(-12 250 120)"><rect x="220" y="100" width="82" height="46" rx="8" fill="#fff" stroke="#c9a227" stroke-width="2"/><circle cx="232" cy="123" r="4" fill="#c9a227"/><text x="266" y="129" text-anchor="middle" font-family="Cormorant Garamond, serif" font-style="italic" font-size="19" fill="#b23a5e">for you</text></g>
</g>
<!-- sparkles -->
<g fill="#c9a227"><path d="M60 60l4 10 10 4-10 4-4 10-4-10-10-4 10-4z"/><path d="M420 90l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/><path d="M400 200l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/></g>
</svg>'''

ICONS = {
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L19 7"/></svg>',
 "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
 "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4"/><path d="M5 12v8h14v-8M12 8v12M12 8c-2-4-6-4-6-1s4 1 6 1zm0 0c2-4 6-4 6-1s-4 1-6 1z"/></svg>',
 "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16M16 9h2a2 2 0 0 1 2 2v10M8 7h4M8 11h4M8 15h4M3 21h18"/></svg>',
 "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.6-9.3-8.6C.9 9.2 2.6 5 6.5 5c2.2 0 3.6 1.3 5.5 3.3C13.9 6.3 15.3 5 17.5 5c3.9 0 5.6 4.2 3.8 7.4C19 16.4 12 21 12 21z"/></svg>',
 "sparkle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/></svg>',
 "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12V4h8l9 9-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6-5.7-6-11a6 6 0 0 1 12 0c0 5.3-6 11-6 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="3"/></svg>',
}

def esc(s): return html.escape(s, quote=True)

# ---------- layout ----------
def layout(page):
    slug = page["slug"]
    url = SITE + "/" + ("" if slug == "index.html" else slug)
    title = page["title"]; desc = page["desc"]
    CUR = ' aria-current="page"'
    nav_links = "".join(f'<a href="{h}"{CUR if h == slug else ""}>{t}</a>' for h, t in NAV)
    crumbs_ld = ""
    if slug != "index.html":
        crumbs_ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"{esc(page['crumb'])}","item":"{url}"}}]}}</script>'''
    extra_ld = page.get("ld", "")
    noindex = '<meta name="robots" content="noindex">' if page.get("noindex") else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{noindex}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#b23a5e">
<meta name="geo.region" content="US-TN"><meta name="geo.placename" content="{CITY}, Tennessee">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ} — {TAG}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(page.get('og_title', title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BIZ} gift wrapping services in {CITY}, Tennessee">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get('og_title', title))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
<link rel="preload" href="assets/fonts/cormorant-garamond.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/style.css">
{LOCAL_BUSINESS_LD}
{crumbs_ld}
{extra_ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="{BIZ} home">{bow_logo()}<span><span class="brand-name">{BIZ}</span><span class="brand-sub">{TAG}</span></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav class="nav-links" id="nav-links" aria-label="Main">{nav_links}<a class="nav-cta" href="contact.html">{ICONS['gift']}Get a Quote</a></nav>
  </div>
</header>
<main id="main">
{page["body"]}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html">{bow_logo()}<span><span class="brand-name">{BIZ}</span><span class="brand-sub">{TAG}</span></span></a>
        <p>Professional gift wrapping services in {CITY}, Tennessee, with pickup and delivery from Knoxville to Chattanooga. Corporate holiday gifts, weddings, showers, birthdays and every occasion in between.</p>
      </div>
      <div><h4>Services</h4><ul>
        <li><a href="corporate-gift-wrapping.html">Corporate gift wrapping</a></li>
        <li><a href="holiday-gift-wrapping.html">Holiday gift wrapping</a></li>
        <li><a href="services.html">Weddings &amp; showers</a></li>
        <li><a href="services.html#birthdays">Birthdays &amp; anniversaries</a></li>
        <li><a href="pricing.html">Pricing &amp; packages</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="about.html">About {OWNER.split()[0]}</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html">Request a quote</a></li>
        <li><a href="about.html#service-area">Service area</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{CITY}, {REGION} {ZIP}</li>
        <li>Knoxville · Chattanooga</li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {BIZ} — {TAG}. {OWNER}, {CITY}, Tennessee.</span>
      <span>Home-based in Sweetwater · By appointment · Pickup &amp; delivery available</span>
    </div>
  </div>
</footer>
<div class="mobile-bar"><a class="btn btn-secondary" href="tel:{PHONE_TEL}">{ICONS['phone']}Call</a><a class="btn btn-primary" href="contact.html">{ICONS['gift']}Get a Quote</a></div>
<script src="assets/main.js" defer></script>
</body>
</html>
'''

LOCAL_BUSINESS_LD = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "{SITE}/#business",
  "name": "{BIZ} — {TAG}",
  "alternateName": "All Wrapped Up Gift Wrapping",
  "description": "Professional gift wrapping service based in {CITY}, Tennessee. Corporate holiday gift wrapping, family holiday wrapping, weddings, anniversaries, birthdays, bridal and baby showers. Pickup and delivery from Knoxville to Chattanooga.",
  "url": "{SITE}/",
  "logo": "{SITE}/assets/apple-touch-icon.png",
  "image": "{SITE}/assets/og-image.jpg",
  "telephone": "{PHONE_TEL}",
  "email": "{EMAIL}",
  "founder": {{"@type": "Person", "name": "{OWNER}"}},
  "priceRange": "$$",
  "address": {{"@type": "PostalAddress", "addressLocality": "{CITY}", "addressRegion": "{REGION}", "postalCode": "{ZIP}", "addressCountry": "US"}},
  "geo": {{"@type": "GeoCoordinates", "latitude": 35.6017, "longitude": -84.4613}},
  "areaServed": [{",".join(f'{{"@type":"City","name":"{c}"}}' for c in AREA)}],
  "knowsAbout": ["gift wrapping", "corporate gifts", "holiday gift wrapping", "wedding gift wrapping", "baby shower gifts", "bridal shower gifts"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog", "name": "Gift wrapping services",
    "itemListElement": [
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Corporate gift wrapping", "url": "{SITE}/corporate-gift-wrapping.html"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Holiday gift wrapping for families", "url": "{SITE}/holiday-gift-wrapping.html"}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Wedding, shower and event gift wrapping", "url": "{SITE}/services.html"}}}}
    ]
  }},
  "sameAs": []
}}
</script>'''

def cta_band(h, p, primary=("Request a free quote", "contact.html"), secondary=("See pricing", "pricing.html")):
    return f'''<section class="cta-band"><div class="wrap reveal">
  <span class="kicker">Get started</span>
  <h2>{h}</h2><p>{p}</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary btn-lg" href="{primary[1]}">{primary[0]}</a><a class="btn btn-secondary btn-lg" href="{secondary[1]}">{secondary[0]}</a></div>
  <p class="contact-line">Call or text <a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>'''

def page_head(crumb, h1, lede, kicker=None):
    k = f'<span class="kicker">{kicker}</span>' if kicker else ""
    return f'''<div class="page-head"><div class="wrap">
  <ol class="crumbs"><li><a href="index.html">Home</a></li><li>{crumb}</li></ol>
  {k}<h1>{h1}</h1><p class="lede">{lede}</p>
</div></div>'''

def estimator(compact=False):
    return f'''<form class="estimator reveal" data-estimator onsubmit="return false">
  <div>
    <span class="kicker">Instant estimate</span>
    <h3>Estimate your order</h3>
    <p class="note">Classic wrapping is priced by the group, with all materials included. Signature custom wraps are quoted by the gift.</p>
    <div class="field"><label for="e-gifts">Number of gifts — <span data-count="gifts">0</span></label><input type="range" id="e-gifts" name="gifts" min="0" max="120" value="{'18' if compact else '0'}"></div>
    <div class="field"><label for="e-over">Oversized or odd shapes among them (baskets, bikes, bulky items) — <span data-count="oversized">0</span></label><input type="range" id="e-over" name="oversized" min="0" max="20" value="0"></div>
    <div class="field"><span class="hint" style="font-weight:800;color:var(--ink-soft)">Add-ons</span>
      <div class="chips">
        <label class="chip"><input type="checkbox" name="addon_notes"><span>Handwritten note cards</span></label>
        <label class="chip"><input type="checkbox" name="addon_luxe"><span>Premium ribbon &amp; embellishments</span></label>
        <label class="chip"><input type="checkbox" name="delivery"><span>Pickup &amp; delivery</span></label>
        <label class="chip"><input type="checkbox" name="rush"><span>Rush (under 72 hrs)</span></label>
      </div></div>
    <div class="field"><span class="hint" style="font-weight:800;color:var(--ink-soft)">Discounts</span>
      <div class="chips">
        <label class="chip"><input type="checkbox" name="disc_nobows"><span>Just wrapping, no bows</span></label>
        <label class="chip"><input type="checkbox" name="disc_boxed"><span>Everything boxed &amp; ready</span></label>
        <label class="chip"><input type="checkbox" name="disc_reuse"><span>Reusing last year's boxes</span></label>
      </div></div>
  </div>
  <div class="estimate-out">
    <span class="label">Estimated range</span>
    <div class="amount" data-amount aria-live="polite">$0</div>
    <span class="save" data-save hidden></span>
    <p class="breakdown" data-breakdown>Add a few gifts to see an estimate.</p>
    <a class="btn btn-primary" data-quote-link href="contact.html">Request a written quote</a>
    <p class="fineprint" style="margin-top:12px">Drop-off in Sweetwater is free. Pickup &amp; delivery is from $50 round trip and quoted by distance for Knoxville and Chattanooga.</p>
  </div>
</form>'''

# ---------- pages ----------
pages = []

# HOME
home_body = f'''
<section class="hero">
  <div class="wrap">
    <div class="reveal in">
      <span class="eyebrow">Sweetwater, Tennessee · Knoxville to Chattanooga</span>
      <h1>Professional gift wrapping for <em>businesses and busy families</em></h1>
      <p class="lede">Themed, custom and classic gift wrapping, from a shirt-and-tie for Dad to a whole Christmas in one family's colors. Corporate orders, client gifts and family celebrations, collected and delivered across East Tennessee.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="contact.html">Request a free quote</a>
        <a class="btn btn-secondary btn-lg" href="pricing.html">See packages &amp; pricing</a>
      </div>
      <ul class="hero-proof">
        <li>{ICONS['check']} Pickup &amp; delivery available</li>
        <li>{ICONS['check']} Bulk corporate orders welcome</li>
        <li>{ICONS['check']} Themed &amp; custom wraps are the specialty</li>
      </ul>
    </div>
    <div class="hero-art">
      <div class="hero-photo"><img src="assets/photos/hero-navy-chiffon.webp" alt="Gift wrapped in navy paper with a navy satin and pale blue chiffon bow by All Wrapped Up" width="1200" height="1500"></div>
      <div class="hero-badge"><strong>Now booking</strong>Holiday 2026 orders</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="audience corp reveal">
        <span class="tag">For businesses</span>
        <h3>Corporate gift wrapping</h3>
        <p>Client gifts, employee appreciation and holiday party favors. Consistent, on-brand wrapping for 25 to 2,500 gifts, delivered ready to present.</p>
        <ul><li>Brand-color ribbon &amp; logo gift tags</li><li>Volume pricing and a single invoice</li><li>Pickup from your office, delivery on your date</li></ul>
        <a class="btn" href="corporate-gift-wrapping.html">Corporate packages →</a>
      </div>
      <div class="audience fam reveal">
        <span class="tag">For families</span>
        <h3>Holiday &amp; everyday wrapping</h3>
        <p>Drop off the shopping bags and collect a beautifully finished stack. Christmas, birthdays, showers, weddings and anniversaries, wrapped to a standard you would be proud to give.</p>
        <ul><li>Coordinated palettes so every gift under the tree belongs together</li><li>Santa gifts wrapped separately and returned sorted by recipient</li><li>Pickup and delivery scheduled around your week</li></ul>
        <a class="btn" href="holiday-gift-wrapping.html">Family packages →</a>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Why hire a professional</span><h2>Presentation is part of the gift</h2><p>The average household spends six or more hours wrapping each December. For a business, the job is measured in days and usually lands on the person who can least spare them.</p></div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="icon">{ICONS['clock']}</div><h3>Reclaim your time</h3><p>Hand over the entire order and spend the season with the people the gifts are for.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['sparkle']}</div><h3>Made to be remembered</h3><p>Themed builds and out-of-the-box ideas people photograph before they open, or a clean classic wrap. Every gift tagged and ready to present.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['building']}</div><h3>On brand, every time</h3><p>Consistent wrapping across every gift in the order, in your colors, with your logo on the tag.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['truck']}</div><h3>Pickup and delivery</h3><p>Collection and delivery along the I-75 corridor from Knoxville to Chattanooga, or drop off in Sweetwater by appointment.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">How it works</span><h2>A simple, four-step process</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Request a quote</h3><p>Send a gift count, approximate sizes and your date through the quote form, or call or text. Quotes are returned within one business day.</p></div>
      <div class="step reveal"><h3>Choose a style</h3><p>Select a curated palette or send brand colors. Paper, ribbon, tags and embellishments are coordinated for you.</p></div>
      <div class="step reveal"><h3>Drop off or schedule pickup</h3><p>Drop off in Sweetwater by appointment, or arrange collection from your home or office.</p></div>
      <div class="step reveal"><h3>Delivered on your date</h3><p>Every gift wrapped, tagged and returned when promised. Corporate orders can be delivered directly to the venue.</p></div>
    </div>
  </div>
</section>

<section class="pinkbg">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Transparent pricing</span><h2>Group pricing, materials included</h2><p>Classic wrapping is priced by the number of gifts, with paper, ribbon, bows and tags included. Signature custom wraps are quoted by the gift. Slide to see an estimate.</p></div>
    {estimator(compact=True)}
    <p style="text-align:center;margin-top:22px"><a class="btn btn-secondary" href="pricing.html">Full price list &amp; packages</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Recent work</span><h2>Styles for every occasion</h2><p>Signature custom builds and classic wraps, all from real orders.</p></div>
    <div class="gallery">
      <figure class="gift-tile reveal"><img src="assets/photos/sq-dad-shirt.webp" alt="Gift wrapped to look like a striped collared shirt with wooden buttons and a bow tie" width="1200" height="1200" loading="lazy"><figcaption>Shirt-and-tie build for Dad</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-bee-bow.webp" alt="Yellow bumblebee paper with a huge honeycomb, buffalo check and black tulle bow" width="1200" height="1200" loading="lazy"><figcaption>Bee-themed statement bow</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-rainbow-box.webp" alt="Large box in watercolor-dot paper with aqua and confetti ribbon" width="1200" height="1200" loading="lazy"><figcaption>Watercolor dots, layered ribbon</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-hannah-check.webp" alt="Buffalo check gift with black yarn, burlap ribbon and Scrabble-tile name tag" width="1200" height="1200" loading="lazy"><figcaption>Scrabble-tile name tag</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-flamingo.webp" alt="Flamingo box with pink and orange tulle bow" width="1200" height="1200" loading="lazy"><figcaption>Flamingos, tulle and satin</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-christmas-gold.webp" alt="Christmas tree paper with gold mesh and red glitter bow" width="1200" height="1200" loading="lazy"><figcaption>Gold mesh and glitter bow</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-western-rose.webp" alt="Coral western paper with brown stitched ribbon and a pink fabric rose" width="1200" height="1200" loading="lazy"><figcaption>Western paper, fabric rose</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-baby-shower.webp" alt="Three baby shower gifts in jungle-animal paper with raffia, gold and purple bows and teething toys tucked in" width="1200" height="1200" loading="lazy"><figcaption>Themed baby shower set</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-snowflake-bow.webp" alt="Purple snowflake paper with a silver-edged organza bow" width="1200" height="1200" loading="lazy"><figcaption>Wired organza bow</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-llama-red-bow.webp" alt="White llama-print paper with a black llama silhouette and a big red bow" width="1200" height="1200" loading="lazy"><figcaption>Llama box, classic red bow</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-pompom-stack.webp" alt="Two stacked boxes in red Happy Holidays paper with a pom-pom garland" width="1200" height="1200" loading="lazy"><figcaption>Pom-pom garland stack</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-paisley.webp" alt="Teal paisley paper with pink and blue curling ribbon and a script Happy Birthday topper" width="1200" height="1200" loading="lazy"><figcaption>Script birthday topper</figcaption></figure>
    </div>
    <p class="fineprint" style="text-align:center">Every photograph is a real order, wrapped by Amiebeth.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Ideas</span><h2>Ways people use us</h2><p>Some of the most fun orders started with "can you do this?"</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{ICONS['gift']}</div><h3>The office white elephant</h3><p>Send every gift and it all comes back wrapped, so the exchange is a true surprise for everyone, including the organizer.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['tag']}</div><h3>Gift cards, but better</h3><p>A gift card in an envelope gets lost on the table. In a small box with ribbon and a tag, or built into a themed wrap, it feels like a real gift.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['star']}</div><h3>Themed to the party</h3><p>Jungle animals for the baby shower, flamingos for the pool party, camo for the hunter. Match the invitation, the nursery or the person.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['heart']}</div><h3>Out-of-the-box builds</h3><p>A shirt and tie for Father's Day, a stack that looks like a cake, a box wrapped to look like the thing inside.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['truck']}</div><h3>Ship your online orders to us</h3><p>Have Amazon and retailer orders sent straight to Amiebeth. Nothing lands on your porch for little eyes to find, you skip the pickup charge, and it all comes back wrapped, tagged and sorted. A small receiving fee covers the tracking and check-in.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['calendar']}</div><h3>Teacher, coach and neighbor gifts</h3><p>The dozen small gifts every December that never get wrapped nicely. Add them to the same order.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Our standard</span><h2>What every order includes</h2></div>
    <div class="promise reveal">
      <div><div class="num">01</div><h3>Logged intake</h3><p>Every gift is recorded at drop-off or pickup and returned against a checklist, so nothing is misplaced.</p></div>
      <div><div class="num">02</div><h3>Photo approval</h3><p>Corporate orders receive a photographed sample in your colors before the batch is wrapped.</p></div>
      <div><div class="num">03</div><h3>On-time delivery</h3><p>Your date is confirmed in writing when the deposit is placed, and it is held.</p></div>
    </div>
  </div>
</section>

{cta_band("Ready to hand off the wrapping?", "Share your gift count and date. Quotes are complimentary and returned within one business day.")}
'''
pages.append(dict(slug="index.html", crumb="Home",
  title=f"Gift Wrapping Service in Sweetwater, TN | {BIZ}",
  og_title=f"{BIZ} — Professional Gift Wrapping Services, Sweetwater TN",
  desc="Professional gift wrapping in Sweetwater, TN for corporate holiday parties, families, weddings and showers. Pickup and delivery Knoxville to Chattanooga. Free quotes.",
  body=home_body))

# CORPORATE
corp_ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service","serviceType":"Corporate gift wrapping","name":"Corporate Gift Wrapping Service","provider":{{"@id":"{SITE}/#business"}},"areaServed":[{",".join(f'{{"@type":"City","name":"{c}"}}' for c in AREA)}],"description":"Bulk gift wrapping for corporate holiday parties, client gifts and employee appreciation with brand-color ribbon, logo gift tags, pickup and delivery across East Tennessee.","offers":{{"@type":"Offer","priceCurrency":"USD","price":"8.00","priceSpecification":{{"@type":"UnitPriceSpecification","price":"8.00","priceCurrency":"USD","unitText":"per gift, starting at"}}}}}}</script>'''
corp_body = page_head("Corporate gift wrapping", "Corporate gift wrapping for holiday parties, client gifts &amp; employee appreciation",
  "Hundreds of gifts, one consistent presentation, delivered on your date. Serving offices, medical practices, dealerships, law firms, churches and schools from Knoxville to Chattanooga.", "For businesses") + f'''
<section>
  <div class="wrap two-col">
    <div class="reveal">
      <span class="kicker">The problem we solve</span>
      <h2>Your team has better uses for the week of the event</h2>
      <p class="lede" style="font-size:18px">Corporate gifting too often ends with a conference room, mismatched paper and a late night for whoever drew the short straw. We take the entire job off your plate so the gifts look intentional and your staff stay on their own work.</p>
      <ul class="checklist">
        <li>Holiday party gifts, door prizes and white elephant exchanges</li>
        <li>Client and referral-partner appreciation gifts</li>
        <li>Employee recognition, welcome kits and milestone gifts</li>
        <li>Conference swag, real-estate closing gifts, teacher appreciation</li>
        <li>Multi-location deliveries and venue drop-off</li>
      </ul>
    </div>
    <div class="reveal">
      <div class="stats">
        <div class="stat"><b>25+</b><span>gifts for volume pricing</span></div>
        <div class="stat"><b>1</b><span>itemized invoice</span></div>
        <div class="stat"><b>5</b><span>business-day standard turnaround</span></div>
      </div>
      <figure class="photo-card reveal"><img src="assets/photos/land-candy-cane-display.webp" alt="A holiday order in candy-stripe and chalkboard papers with tulle-wrapped towers, each gift tagged by recipient" width="1400" height="933" loading="lazy"><figcaption>One order, one look: candy-stripe and chalkboard papers, every gift tagged by recipient.</figcaption></figure>
      <div class="callout"><span class="h">Branded presentation</span><p>Send your logo and brand colors. We source ribbon to match and print custom gift tags so every gift reads as yours.</p></div>
    </div>
  </div>
</section>

<section class="banner">
  <img src="assets/photos/wide-holiday-display.webp" alt="A table full of coordinated holiday gifts in candy-stripe and chalkboard papers with tulle-wrapped towers" width="1400" height="933" loading="lazy">
  <div class="wrap banner-text reveal"><span class="kicker">Volume orders</span><h2>Dozens of gifts, one cohesive look</h2><p>Coordinated papers, ribbons and tags across an entire order, delivered sorted and ready to hand out.</p></div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Corporate packages</span><h2>Volume pricing that gets better as the order grows</h2><p>Corporate rates are for Classic wraps in your colors. Themed or custom builds are quoted separately. Final per-gift price depends on sizes and finishes.</p></div>
    <div class="pricing">
      <div class="plan reveal"><span class="name">Starter</span><h3>Team gifts</h3><p class="who">25 – 99 gifts · small offices, departments, client lists</p><div class="price">from $9<small>/gift</small></div><p class="per">10% off à la carte pricing</p>
        <ul><li>One signature wrap style in your colors</li><li>Printed gift tags, names added from your list</li><li>Pickup &amp; delivery from $50 round trip</li><li>5-business-day turnaround</li></ul><a class="btn btn-secondary" href="contact.html?type=corporate">Quote the Starter package</a></div>
      <div class="plan featured reveal"><span class="flag">Most popular</span><span class="name">Team</span><h3>Holiday party</h3><p class="who">100 – 249 gifts · company parties, client appreciation events</p><div class="price">from $8<small>/gift</small></div><p class="per">20% off à la carte pricing</p>
        <ul><li>Up to two wrap styles (for example, staff and VIP)</li><li>Custom logo gift tags included</li><li>Brand-color ribbon sourced to match</li><li>Pickup &amp; delivery to Knoxville or Chattanooga, quoted by trip</li><li>Delivery straight to the venue on party day</li></ul><a class="btn btn-primary" href="contact.html?type=corporate">Quote the Team package</a></div>
      <div class="plan reveal"><span class="name">Enterprise</span><h3>Large &amp; multi-site</h3><p class="who">250+ gifts · multiple offices, franchise groups, hospital systems</p><div class="price">Custom<small> quote</small></div><p class="per">25%+ volume savings</p>
        <ul><li>Dedicated production timeline &amp; check-ins</li><li>Multi-location delivery scheduling</li><li>Mixed sizes and odd shapes handled in the same order</li><li>Invoicing for business accounts</li></ul><a class="btn btn-gold" href="contact.html?type=corporate">Talk to us about Enterprise</a></div>
    </div>
    <p class="fineprint">Prices are starting points for small and medium gifts. Large and oversized items are quoted individually. Rush orders under 72 hours add 25%. Tennessee sales tax applies where required.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Enhancements</span><h2>Finishing touches for corporate orders</h2></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{ICONS['tag']}</div><h3>Logo gift tags</h3><p>Your logo and a message on a heavy card-stock tag, tied on with ribbon. From $1.50 per gift.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['heart']}</div><h3>Handwritten notes</h3><p>Personal notes handwritten from your message list, so each recipient gets something that feels one-to-one. $2 per gift.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['gift']}</div><h3>White elephant &amp; party gifts</h3><p>Send everything for the office party or white elephant exchange and it all comes back wrapped, so the surprise is real for everyone, including the person who organized it.</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Process</span><h2>From quote to delivery in five steps</h2></div>
    <div class="steps" style="grid-template-columns:repeat(5,1fr)">
      <div class="step reveal"><h3>Quote</h3><p>Send gift count, sizes and your event date. You'll get a written quote within one business day.</p></div>
      <div class="step reveal"><h3>Style approval</h3><p>We send a photographed sample in your colors for approval or revision.</p></div>
      <div class="step reveal"><h3>Pickup</h3><p>We collect gifts from your office, or receive shipments from your vendors directly.</p></div>
      <div class="step reveal"><h3>Wrapping</h3><p>Wrapped by hand in Sweetwater, boxed and labeled by recipient or department.</p></div>
      <div class="step reveal"><h3>Delivery</h3><p>Delivered to your office or venue on the date you choose, with one itemized invoice.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Holiday scheduling</span><h2>December capacity is limited</h2><p>Corporate holiday slots are reserved in order of deposit. Booking by early November guarantees delivery before your event date.</p></div>
    <div class="countdown" data-countdown></div>
    <p style="text-align:center;color:var(--ink-soft)">To guarantee delivery before Christmas, book by <strong data-book-by>early December</strong>.</p>
  </div>
</section>

{cta_band("Receive a corporate quote within one business day", "Share the gift count, approximate sizes and your event date. We will return pricing, a timeline and a photographed sample in your brand colors.", ("Request a corporate quote", "contact.html?type=corporate"), ("Call " + PHONE, "tel:" + PHONE_TEL))}
'''
pages.append(dict(slug="corporate-gift-wrapping.html", crumb="Corporate gift wrapping",
  title="Corporate Gift Wrapping | Knoxville & Chattanooga TN",
  og_title="Corporate Gift Wrapping — Bulk Holiday & Client Gifts, East Tennessee",
  desc="Bulk gift wrapping for holiday parties, client gifts and employee appreciation. Brand-color ribbon, logo tags, volume pricing from $8 per gift, pickup and delivery in East TN.",
  ld=corp_ld, body=corp_body))

# SERVICES / OCCASIONS
services_body = page_head("Occasions", "Gift wrapping for weddings, showers, birthdays, anniversaries &amp; holidays",
  "One gift or one hundred, themed to the party or the person. Classic wraps and signature custom builds, wrapped by hand in Sweetwater, Tennessee.", "Occasions") + f'''
<section>
  <div class="wrap">
    <div class="occasions">
      <div class="occasion reveal" id="weddings"><img src="assets/photos/sq-wedding-navy.webp" alt="Navy gift with navy satin and pale blue chiffon bow" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['heart']}</div><h3>Weddings</h3><p>Bridesmaid and groomsmen gifts, parent gifts, welcome bags for out-of-town guests and the gift you're bringing to someone else's big day.</p><ul><li>Ribbon matched to your wedding palette</li><li>Welcome-bag assembly and tagging</li><li>Delivery to the venue or hotel block</li></ul></div>
      <div class="occasion reveal" id="bridal-showers"><img src="assets/photos/sq-rainbow-dots.webp" alt="Watercolor-dot paper with aqua and confetti ribbon bow" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['sparkle']}</div><h3>Bridal showers</h3><p>Host gifts, favors and shower gifts wrapped to match the theme, so the gift table looks styled and photographs beautifully.</p><ul><li>Favor wrapping in bulk</li><li>Coordinated gift-table display</li><li>Registry gifts received and wrapped for you</li></ul></div>
      <div class="occasion reveal" id="baby-showers"><img src="assets/photos/sq-baby-shower.webp" alt="Three baby shower gifts in jungle-animal paper with raffia, gold and purple bows" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['gift']}</div><h3>Baby showers</h3><p>Large boxes, unusual shapes and the smallest keepsakes, wrapped to the shower theme or the nursery colors the parents have chosen.</p><ul><li>Oversized item specialists</li><li>Gender-reveal wrapping handled discreetly</li><li>Diaper cakes and gift baskets finished</li></ul></div>
      <div class="occasion reveal" id="birthdays"><img src="assets/photos/sq-paisley.webp" alt="Teal paisley birthday gift with curling ribbon and script topper" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['star']}</div><h3>Birthdays</h3><p>Milestone birthdays, children's parties and surprise gifts. Themed to the party or the person, from a llama box with a big red bow to a shirt and tie for Dad.</p><ul><li>Durable wrapping that travels well</li><li>Themed paper and ribbon</li><li>Same-week turnaround when available</li></ul></div>
      <div class="occasion reveal" id="anniversaries"><img src="assets/photos/sq-western-rose.webp" alt="Coral paper with stitched brown ribbon and a fabric rose" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['heart']}</div><h3>Anniversaries</h3><p>Elegant paper, satin ribbon and a handwritten card, finished well ahead of the date.</p><ul><li>Premium finishes and embellishments</li><li>Handwritten note cards</li><li>Discreet pickup and delivery</li></ul></div>
      <div class="occasion reveal" id="holidays"><img src="assets/photos/sq-christmas-gold.webp" alt="Christmas tree paper with gold mesh and red glitter bow" width="1200" height="1200" loading="lazy"><div class="icon">{ICONS['calendar']}</div><h3>Holidays</h3><p>Christmas, Hanukkah, Valentine's Day, Mother's and Father's Day, Easter and graduation. Seasonal palettes or your own family tradition.</p><ul><li>Whole-family Christmas packages</li><li>Santa paper kept separate</li><li><a href="holiday-gift-wrapping.html">See holiday packages →</a></li></ul></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap two-col">
    <div class="reveal">
      <span class="kicker">What's included</span>
      <h2>Every gift, every time</h2>
      <ul class="checklist">
        <li><strong>Coordinated paper</strong> — matched to the occasion, the theme or your colors</li>
        <li><strong>Ribbon that suits the gift</strong> — grosgrain, satin, velvet, tulle, mesh or classic curling ribbon, chosen to match the look</li>
        <li><strong>Hand-tied bow</strong> — full, even and secured so it survives the trip</li>
        <li><strong>Gift tag</strong> — printed or handwritten with the recipient's name</li>
        <li><strong>Crisp corners &amp; a full bow</strong> — the details people notice</li>
      </ul>
    </div>
    <div class="reveal">
      <div class="callout"><span class="h">Unusual shapes welcome</span><p>Baskets, bicycles, instruments, plush toys and bottles are all wrapped regularly. Send a photograph for an exact quote.</p></div>
      <div class="callout"><span class="h">Your own materials</span><p>Supply your own paper and ribbon and we will wrap with it at a reduced rate. Mention it when you book.</p></div>
    </div>
  </div>
</section>

{cta_band("Tell us about the occasion", "Send the date, the gift count and any colors you have in mind. We will take it from there.")}
'''
pages.append(dict(slug="services.html", crumb="Occasions",
  title="Wedding, Shower & Birthday Gift Wrapping | All Wrapped Up TN",
  og_title="Gift Wrapping for Weddings, Showers, Birthdays & Anniversaries — East Tennessee",
  desc="Gift wrapping for weddings, bridal and baby showers, birthdays, anniversaries and holidays in Sweetwater, Knoxville and Chattanooga, TN. Real ribbon, hand-tied bows.",
  body=services_body))

# PRICING
pricing_body = page_head("Pricing", "Gift wrapping prices &amp; packages",
  "Two levels of wrapping, priced clearly. Classic wrapping is priced by the group with all materials included. Signature custom wraps are quoted by the gift, because the materials and the time are more.", "Pricing") + f'''
<section>
  <div class="wrap">
    <div class="section-head left reveal"><span class="kicker">Classic wrap</span><h2>Priced by the group, all materials included</h2><p>Paper, coordinating ribbon, a bow and a gift tag on every gift, in any color scheme or theme you like. Standard-size gifts; oversized items are quoted.</p></div>
    <table class="sizes reveal">
      <thead><tr><th>Group</th><th>Good for</th><th>Price</th></tr></thead>
      <tbody>
        <tr><td><strong>Small group</strong><small>1 – 10 gifts</small></td><td>One person's list, a shower gift or two, the special few</td><td>$60</td></tr>
        <tr><td><strong>Medium group</strong><small>11 – 25 gifts</small></td><td>The whole family, grandparents and teachers included</td><td>$80</td></tr>
        <tr><td><strong>Large group</strong><small>26 – 50 gifts</small></td><td>Large households and the home everyone gathers in</td><td>$100</td></tr>
        <tr><td><strong>Extra large group</strong><small>51+ gifts</small></td><td>Big families, class parties, office exchanges</td><td>from $120</td></tr>
      </tbody>
    </table>
    <p class="fineprint">Prices include all wrapping materials. Oversized and odd-shaped items add from $15 each. Gift cards can be dressed up in a small box with ribbon and a tag for $5 each.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head left reveal"><span class="kicker">Signature custom wrap</span><h2>Themed and custom builds, quoted by the gift</h2><p>The shirt-and-tie for Dad, the tulle-topped baby shower set, the box that matches the party invitation. Custom wraps use specialty ribbon, tulle, mesh, toppers and hand-built details, and take real time, so they cost more than a Classic wrap.</p></div>
    <table class="sizes reveal">
      <thead><tr><th>Size</th><th>What you get</th><th>Starting at</th></tr></thead>
      <tbody>
        <tr><td><strong>Small</strong></td><td>Themed paper and ribbon, a statement bow or topper, tag</td><td>from $15</td></tr>
        <tr><td><strong>Medium</strong></td><td>Themed build with layered ribbon, tulle or mesh, embellishments</td><td>from $22</td></tr>
        <tr><td><strong>Large</strong></td><td>Full custom build, stacked or shaped, hand-made details</td><td>from $32</td></tr>
        <tr><td><strong>Oversized / one-of-a-kind</strong></td><td>Shirt-and-tie wraps, character builds, anything you can dream up</td><td>quoted</td></tr>
      </tbody>
    </table>
    <p class="fineprint">Send a photo of the gift and tell us the theme. Custom quotes are returned within one business day.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Discounts</span><h2>Three easy ways to save</h2><p>Taken off the group price on any Classic order.</p></div>
    <table class="sizes reveal">
      <tbody>
        <tr><td><strong>Just wrapping, no bows</strong></td><td>Paper and a tag only, no ribbon or bow</td><td>$15 off</td></tr>
        <tr><td><strong>Everything boxed and ready to wrap</strong></td><td>Gifts arrive already in boxes, so wrapping starts right away</td><td>$10 off</td></tr>
        <tr><td><strong>Recycled box discount</strong></td><td>Save and reuse gift boxes from last year</td><td>$10 off</td></tr>
      </tbody>
    </table>
    <p class="fineprint">Bringing your own paper and ribbon? Mention it when you book and we will price it in.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Corporate volume rates</span><h2>Business pricing</h2></div>
    <table class="sizes reveal">
      <thead><tr><th>Order size</th><th>Included</th><th>Starting rate</th></tr></thead>
      <tbody>
        <tr><td><strong>25 – 99 gifts</strong><small>Starter</small></td><td>One wrap style, printed tags, pickup &amp; delivery from $50</td><td>$9 / gift</td></tr>
        <tr><td><strong>100 – 249 gifts</strong><small>Team</small></td><td>Two wrap styles, custom logo tags, brand-color ribbon, venue delivery</td><td>$8 / gift</td></tr>
        <tr><td><strong>250+ gifts</strong><small>Enterprise</small></td><td>Dedicated timeline, multi-site delivery, invoicing for business accounts</td><td>Custom</td></tr>
      </tbody>
    </table>
    <p style="margin-top:16px"><a class="btn btn-secondary" href="corporate-gift-wrapping.html">Corporate package details →</a></p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Add-ons &amp; extras</span><h2>Finishing touches</h2></div>
    <table class="sizes reveal">
      <tbody>
        <tr><td><strong>Handwritten note card</strong></td><td>Your message, our handwriting, tucked under the ribbon</td><td>$2 / gift</td></tr>
        <tr><td><strong>Custom logo gift tags</strong></td><td>Heavy card stock printed with your logo and message</td><td>$1.50 / gift</td></tr>
        <tr><td><strong>Premium ribbon &amp; embellishments</strong></td><td>Satin or velvet ribbon, tulle, a topper or ornament added to a Classic wrap</td><td>+$4 / gift</td></tr>
        <tr><td><strong>Rush (under 72 hours)</strong></td><td>Subject to availability, especially in December</td><td>+25%</td></tr>
        <tr><td><strong>Gift card wrap</strong></td><td>A gift card dressed up in a small box with ribbon and a tag</td><td>$5 each</td></tr>
        <tr><td><strong>Oversized / odd shape</strong></td><td>Baskets, bikes, guitars, plush animals, anything without flat sides</td><td>from $15 each</td></tr>
        <tr><td><strong>Ship-to-us receiving</strong></td><td>Online orders sent straight to Amiebeth, logged on arrival and checked against your list. Saves the pickup trip.</td><td>$15 / order</td></tr>
        <tr><td><strong>Pickup &amp; delivery</strong></td><td>Round trip beyond 5 miles of Sweetwater. Knoxville, Maryville, Cleveland and Chattanooga quoted by distance.</td><td>from $50</td></tr>
      </tbody>
    </table>
    <p class="fineprint">A 50% deposit reserves your date; the balance is due at delivery. Cash, Venmo or personal check. Business accounts may be invoiced. Prices effective for the 2026 season and subject to change.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Booking &amp; deposit</span><h2>Space is limited, first come first served</h2><p>Amiebeth wraps every gift herself, so there are only so many slots in a season and December fills first.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{ICONS['calendar']}</div><h3>Dates are held in booking order</h3><p>Your date is confirmed when the deposit is in. Once a week is full, it is full.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['shield']}</div><h3>50% deposit reserves your spot</h3><p>The balance is due at delivery or pickup. Cash, Venmo or personal check.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['tag']}</div><h3>Non-refundable once materials are bought</h3><p>Paper, ribbon and embellishments are purchased for your order right after booking. Need to move your date? One reschedule is free when space allows.</p></div>
    </div>
  </div>
</section>

<section class="pinkbg">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Estimate</span><h2>Build an estimate for your order</h2></div>
    {estimator()}
  </div>
</section>

{cta_band("Need an exact figure?", "Send a count and a few photographs and we will price the order precisely, within one business day.")}
'''
pricing_ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ItemList","name":"Gift wrapping packages","itemListElement":[
{{"@type":"Offer","position":1,"name":"Small group — 1 to 10 gifts","price":"60","priceCurrency":"USD","url":"{SITE}/pricing.html"}},
{{"@type":"Offer","position":2,"name":"Medium group — 11 to 25 gifts","price":"80","priceCurrency":"USD","url":"{SITE}/pricing.html"}},
{{"@type":"Offer","position":3,"name":"Large group — 26 to 50 gifts","price":"100","priceCurrency":"USD","url":"{SITE}/pricing.html"}},
{{"@type":"Offer","position":4,"name":"Corporate Starter — 25 to 99 gifts","price":"9","priceCurrency":"USD","url":"{SITE}/corporate-gift-wrapping.html"}},
{{"@type":"Offer","position":5,"name":"Corporate Team — 100 to 249 gifts","price":"8","priceCurrency":"USD","url":"{SITE}/corporate-gift-wrapping.html"}}]}}</script>'''
pages.append(dict(slug="pricing.html", crumb="Pricing",
  title="Gift Wrapping Prices & Packages | Groups from $60 | TN",
  og_title="Gift Wrapping Prices & Packages — All Wrapped Up",
  desc="East Tennessee gift wrapping prices: Classic wrapping from $60 for up to 10 gifts with all materials included, custom themed wraps from $15 per gift, corporate rates from $8 per gift.",
  ld=pricing_ld, body=pricing_body))

# HOLIDAY
holiday_body = page_head("Holiday gift wrapping", "Christmas &amp; holiday gift wrapping for busy families",
  "Drop off the shopping bags and collect a tree's worth of beautifully wrapped, tagged and sorted gifts. Serving Sweetwater, Knoxville, Chattanooga and the communities along I-75.", "Holiday 2026") + f'''
<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Holiday timeline</span><h2>Christmas is closer than it looks</h2></div>
    <div class="countdown" data-countdown></div>
    <p style="text-align:center;color:var(--ink-soft)">Book by <strong data-book-by>mid-December</strong> to guarantee your gifts are back under the tree in time.</p>
  </div>
</section>

<section class="banner">
  <img src="assets/photos/wide-holiday-display.webp" alt="A table full of coordinated holiday gifts in candy-stripe and chalkboard papers with tulle-wrapped towers" width="1400" height="933" loading="lazy">
  <div class="wrap banner-text reveal"><span class="kicker">Recent holiday work</span><h2>A whole family's Christmas, wrapped and sorted</h2></div>
</section>

<section class="alt">
  <div class="wrap two-col">
    <div class="reveal">
      <span class="kicker">For families</span>
      <h2>Reclaim the best part of December</h2>
      <p class="lede" style="font-size:18px">The shopping is the hard part, and it is done. Wrapping is what consumes the last two weekends of the year. Hand it over and spend them on the season instead.</p>
      <ul class="checklist">
        <li>Santa gifts wrapped in separate paper and kept apart from family gifts</li>
        <li>Gifts returned sorted by recipient, so stockings and tree are a five-minute job</li>
        <li>Pickup and delivery scheduled around your week, evenings and weekends included</li>
        <li>Teacher, coach and neighbor gifts included in the same order</li>
        <li>Coordinated palette so the tree looks styled, not random</li>
      </ul>
    </div>
    <div class="reveal">
      <div class="stats">
        <div class="stat"><b>6+</b><span>hours the average family spends wrapping</span></div>
        <div class="stat"><b>$80</b><span>for 11 to 25 gifts, materials included</span></div>
        <div class="stat"><b>$0</b><span>to drop off in Sweetwater</span></div>
      </div>
      <div class="callout"><span class="h">Ship your online orders to us</span><p>Have Amazon and retailer orders delivered straight to Amiebeth in Sweetwater. Each package is logged when it arrives, checked against your list, wrapped and delivered finished. No boxes on the porch for curious kids, and no pickup charge. Receiving is $15 per order.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Holiday pricing</span><h2>Pick your group size and consider it done</h2><p>Classic wrapping with paper, ribbon, bows and tags included. Themed and custom builds are quoted by the gift.</p></div>
    <div class="pricing">
      <div class="plan reveal"><span class="name">Small group</span><h3>1 – 10 gifts</h3><p class="who">One person's list or the special few</p><div class="price">$60</div><p class="per">all materials included</p><ul><li>One coordinated palette</li><li>Tags with names</li><li>Drop-off in Sweetwater</li></ul><a class="btn btn-secondary" href="contact.html?type=family">Book now</a></div>
      <div class="plan featured reveal"><span class="flag">Most popular</span><span class="name">Medium group</span><h3>11 – 25 gifts</h3><p class="who">The whole family plus teachers and grandparents</p><div class="price">$80</div><p class="per">all materials included</p><ul><li>Santa paper + family paper</li><li>Handwritten tags</li><li>Sorted by recipient</li><li>Priority December dates</li></ul><a class="btn btn-primary" href="contact.html?type=family">Book now</a></div>
      <div class="plan reveal"><span class="name">Large group</span><h3>26 – 50 gifts</h3><p class="who">Large households and the home everyone gathers in</p><div class="price">$100</div><p class="per">51+ gifts from $120</p><ul><li>Up to three palettes</li><li>Tags and note cards</li><li>Two pickups if you shop in rounds</li><li>First pick of dates</li></ul><a class="btn btn-gold" href="contact.html?type=family">Book now</a></div>
    </div>
    <p class="fineprint">Standard-size gifts. Oversized items add from $15 each. No bows, pre-boxed and recycled-box discounts apply. <a href="pricing.html">Full price list →</a></p>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Holiday portfolio</span><h2>Real orders, December after December</h2></div>
    <div class="gallery">
      <figure class="gift-tile reveal"><img src="assets/photos/sq-christmas-gold.webp" alt="Christmas tree paper with gold mesh and red glitter bow" width="1200" height="1200" loading="lazy"><figcaption>Gold mesh, red glitter</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-christmas-gold-white.webp" alt="Christmas tree paper with gold mesh and white glitter poinsettias" width="1200" height="1200" loading="lazy"><figcaption>Gold mesh, white poinsettias</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-special-delivery.webp" alt="North Pole special delivery box with emerald satin bow" width="1200" height="1200" loading="lazy"><figcaption>North Pole special delivery</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-pompom-stack.webp" alt="Two stacked boxes in red Happy Holidays paper with a pom-pom garland" width="1200" height="1200" loading="lazy"><figcaption>Pom-pom garland stack</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-snowflake-cube.webp" alt="Oversized cube gift in purple snowflake paper with silver organza bow and snowflake" width="1200" height="1200" loading="lazy"><figcaption>Oversized, finished in silver</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-snowflake-just-for-you.webp" alt="Purple snowflake gift with a silver organza bow and Just For You tag" width="1200" height="1200" loading="lazy"><figcaption>Organza bow and tag</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-nutcracker.webp" alt="Nutcracker print paper with sage green glitter ribbon" width="1200" height="1200" loading="lazy"><figcaption>Nutcracker print</figcaption></figure>
      <figure class="gift-tile reveal"><img src="assets/photos/sq-plaid-green-bow.webp" alt="Green and navy plaid paper with emerald ribbon and a curling-ribbon burst" width="1200" height="1200" loading="lazy"><figcaption>Plaid, emerald ribbon</figcaption></figure>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Booking &amp; deposit</span><h2>Space is limited, first come first served</h2><p>Amiebeth wraps every gift herself, so there are only so many slots in a season and December fills first.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{ICONS['calendar']}</div><h3>Dates are held in booking order</h3><p>Your date is confirmed when the deposit is in. Once a week is full, it is full.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['shield']}</div><h3>50% deposit reserves your spot</h3><p>The balance is due at delivery or pickup. Cash, Venmo or personal check.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['tag']}</div><h3>Non-refundable once materials are bought</h3><p>Paper, ribbon and embellishments are purchased for your order right after booking. Need to move your date? One reschedule is free when space allows.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Year round</span><h2>Every holiday on the calendar</h2></div>
    <div class="grid grid-4">
      <div class="card reveal"><h3>Hanukkah</h3><p>Eight nights, eight gifts per person, blue-and-silver or your family's palette.</p></div>
      <div class="card reveal"><h3>Valentine's Day</h3><p>One perfect gift, luxe ribbon, handwritten card, ready before the 14th.</p></div>
      <div class="card reveal"><h3>Mother's &amp; Father's Day</h3><p>Coordinated gifts from every child, each one finished to the same standard.</p></div>
      <div class="card reveal"><h3>Easter &amp; graduation</h3><p>Baskets finished with cello and bows, graduation gifts wrapped in school colors.</p></div>
    </div>
  </div>
</section>

{cta_band("Reserve your holiday date", "Space is limited and December dates go in the order deposits come in. A 50% deposit holds yours. Quotes are complimentary.", ("Book holiday wrapping", "contact.html?type=family"), ("Text " + PHONE, "sms:" + PHONE_TEL))}
'''
pages.append(dict(slug="holiday-gift-wrapping.html", crumb="Holiday gift wrapping",
  title="Christmas Gift Wrapping Service | Sweetwater, Knoxville & Chattanooga",
  og_title="Christmas & Holiday Gift Wrapping Service — East Tennessee",
  desc="Holiday gift wrapping for busy families in Sweetwater, Knoxville and Chattanooga, TN. From $60 for up to 10 gifts, materials included, Santa paper kept separate, pickup and delivery. Book early.",
  body=holiday_body))

# ABOUT
about_body = page_head("About", f"Meet {OWNER.split()[0]}, the hands behind the bows",
  f"{BIZ} is a one-woman gift wrapping service run from {OWNER.split()[0]}'s home in {CITY}, Tennessee, built on a love of themed, memorable gifts and a well-tied bow.", "About Amiebeth") + f'''
<section>
  <div class="wrap two-col">
    <div class="prose reveal">
      <h2 style="margin-top:0">A little about me</h2>
      <p>I'm {OWNER}. {BIZ} began because every December I was the person friends and family handed their gifts to. Somewhere between wrapping for the whole street and the first office that asked me to finish their client gifts, it became a business.</p>
      <p>I work from my home in {CITY}, on I-75 between Knoxville and Chattanooga, which means I can collect from a Knoxville office in the morning and deliver to a Chattanooga venue the same week. Every gift is wrapped by hand, by me. What I love most is a theme: a shirt and tie for Dad, a jungle nursery for a baby shower, a whole Christmas in one family's colors. Classic paper-and-ribbon wraps are always on the menu too.</p>
      <h3>What I care about</h3>
      <ul>
        <li><strong>The details.</strong> A theme that lands, a bow that stays full through the car ride, a tag that makes them smile.</li>
        <li><strong>Your colors, not mine.</strong> Corporate orders match your brand. Family orders match your tree.</li>
        <li><strong>Being easy to work with.</strong> Prompt replies, clear pricing and delivery when promised.</li>
      </ul>
      <div class="callout"><span class="h">Two ways to wrap</span><p><strong>Classic</strong> is paper, ribbon, a bow and a tag, in whatever colors or theme you like. <strong>Signature custom</strong> is the fun stuff: themed builds, specialty ribbon, tulle and mesh, toppers and hand-built details. Custom costs more because the materials and the time are more, and it is quoted gift by gift.</p></div>
    </div>
    <div class="reveal">
      <figure class="photo-card reveal"><img src="assets/photos/about-hannah.webp" alt="Buffalo check gift with black yarn, burlap ribbon and a Scrabble-tile name tag reading Hannah" width="1200" height="1500" loading="lazy"><figcaption>Details like a Scrabble-tile name tag are what people remember.</figcaption></figure>
    </div>
  </div>
</section>

<section class="alt" id="service-area">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Service area</span><h2>Sweetwater home base, Knoxville to Chattanooga by appointment</h2><p>Drop-off in {CITY} is always free. Pickup and delivery is from $50 round trip beyond 5 miles of {CITY}, and quoted by distance for the wider corridor.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{ICONS['pin']}</div><h3>Home base</h3><p>Sweetwater, Madisonville, Athens, Loudon, Niota, Philadelphia, Vonore, Tellico Village and Lenoir City.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['truck']}</div><h3>North to Knoxville</h3><p>Maryville, Alcoa, Farragut, Oak Ridge, West Knoxville and downtown Knoxville. Pickup and delivery quoted by distance, from $50 round trip.</p></div>
      <div class="card reveal"><div class="icon">{ICONS['truck']}</div><h3>South to Chattanooga</h3><p>Cleveland, Ooltewah, Hixson, East Ridge and downtown Chattanooga. Pickup and delivery quoted by distance, from $50 round trip.</p></div>
    </div>
    <p class="fineprint" style="text-align:center">Outside these areas? Please ask. Larger corporate orders often justify the distance.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Good to know</span><h2>How I work</h2></div>
    <div class="benefit-list">
      <div class="benefit reveal"><div class="n">{ICONS['calendar']}</div><div><h3>By appointment</h3><p>Drop-offs and pickups are scheduled so every order receives full attention. Call or text to arrange a time.</p></div></div>
      <div class="benefit reveal"><div class="n">{ICONS['shield']}</div><div><h3>Your gifts are safe</h3><p>Gifts are logged at intake, stored safely and returned against a checklist.</p></div></div>
      <div class="benefit reveal"><div class="n">{ICONS['eye']}</div><div><h3>Photo approvals</h3><p>Corporate orders receive a photographed sample before the batch is wrapped. Families may request one as well.</p></div></div>
      <div class="benefit reveal"><div class="n">{ICONS['heart']}</div><div><h3>Local and personal</h3><p>You work with the owner from the first message to the final delivery.</p></div></div>
    </div>
  </div>
</section>

{cta_band("Let's talk about your gifts", "One anniversary gift or a thousand client boxes, I would be glad to hear about it.")}
'''
about_ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Person","name":"{OWNER}","jobTitle":"Owner & gift wrapper","worksFor":{{"@id":"{SITE}/#business"}},"email":"{EMAIL}","telephone":"{PHONE_TEL}","address":{{"@type":"PostalAddress","addressLocality":"{CITY}","addressRegion":"{REGION}","addressCountry":"US"}}}}</script>'''
pages.append(dict(slug="about.html", crumb="About",
  title=f"About {OWNER} | {BIZ}, Sweetwater TN",
  og_title=f"About {BIZ} — Home-Based Gift Wrapping in Sweetwater, TN",
  desc=f"Meet {OWNER}, owner of {BIZ}, a home-based gift wrapping service in Sweetwater, Tennessee serving Knoxville to Chattanooga with pickup and delivery.",
  ld=about_ld, body=about_body))

# FAQ
faqs = [
 ("How much does professional gift wrapping cost?", "Classic wrapping is priced by the group with all materials included: $60 for 1 to 10 gifts, $80 for 11 to 25, $100 for 26 to 50 and from $120 for 51 or more. Oversized items add from $15 each and gift cards can be boxed and ribboned for $5. Signature custom wraps, the themed and hand-built ones, start around $15 per gift and are quoted individually because the materials and time are more. Corporate volume pricing starts at $8 per gift for 100 or more."),
 ("Do you offer pickup and delivery?", "Yes. Drop-off in Sweetwater is free. Pickup and delivery beyond 5 miles is $50 round trip, and Knoxville, Maryville, Cleveland and Chattanooga are quoted by distance."),
 ("How far in advance should I book holiday wrapping?", "For Christmas, book by early November for corporate orders and by the first week of December for family bundles. Dates are reserved in order of deposit and December fills quickly. Rush orders under 72 hours may be available for a 25% surcharge."),
 ("Can you match my company's brand colors?", "Absolutely. Send your logo and brand colors and we'll source ribbon to match and print custom logo gift tags. Corporate orders receive a photo mock-up for approval before the batch is wrapped."),
 ("Can I ship online orders directly to you?", "Yes. Have Amazon or retailer orders shipped straight to Amiebeth in Sweetwater. Each package is logged when it arrives, checked against your list, wrapped and delivered finished. It keeps surprises off your porch and saves you the pickup charge. Receiving and check-in is $15 per order, since every package is tracked and accounted for. Ask for the shipping address when you book."),
 ("What if my gift is an odd shape?", "Bikes, baskets, guitars, plush animals, bottles and other awkward shapes are welcome. They add from $15 each to the group price. Send a photo for an exact quote."),
 ("Can I supply my own wrapping paper and ribbon?", "Yes. Mention it when you book and we will price it in. There are also three standing discounts: just wrapping with no bows is $15 off, gifts that arrive already boxed are $10 off, and reusing last year's gift boxes is another $10 off."),
 ("How do you keep Santa gifts separate?", "Tell us which gifts are from Santa and we'll wrap them in a distinct paper, tag them separately and return them in their own labeled bag so nothing gets mixed up on Christmas Eve."),
 ("Can you wrap the gifts for an office party or white elephant?", "Yes, and it is one of our favorite jobs. Send every gift, in a bag with a note of who it is from if you like, and it all comes back wrapped so the surprise is real for everyone, including whoever organized it. We can wrap in one coordinated style or make every gift look different."),
 ("Do you wrap gift cards?", "Yes. A gift card in a plain envelope is easy to overlook. We dress it up in a small box with ribbon and a tag for $5, or build it into a themed wrap that hints at where the card is from."),
 ("What payment methods do you accept?", "Cash, Venmo and personal check. A 50% deposit reserves your date and the balance is due at delivery. Business accounts can be invoiced."),
 ("Is the deposit refundable?", "The deposit holds your date and pays for your materials, which are bought right after you book, so it is non-refundable once materials have been purchased. If your plans change, one reschedule is free when space allows. Space is limited and dates are held in the order deposits come in, so booking early matters in November and December."),
 ("Where are you located?", f"{BIZ} is home-based in {CITY}, Tennessee, right off I-75 between Knoxville and Chattanooga. Drop-offs are by appointment. Call or text {PHONE} to schedule."),
 ("Are my gifts safe with you?", "Every gift is logged at intake with a description, stored safely and returned with a checklist. Corporate orders can be labeled by recipient or department for easy distribution."),
]
faq_html = "".join(f'<details class="reveal"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q, a in faqs)
import json as _j
faq_ld = '<script type="application/ld+json">' + _j.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}, ensure_ascii=False) + '</script>'
faq_body = page_head("FAQ", "Frequently asked questions", "Pricing, timing, pickup and delivery, unusual shapes and everything else clients ask before booking.", "FAQ") + f'''
<section><div class="wrap"><div class="faq">{faq_html}</div>
<p style="text-align:center;margin-top:30px;color:var(--ink-soft)">Have another question? <a href="contact.html"><strong>Contact us directly →</strong></a></p></div></section>
{cta_band("Ready when you are", "Complimentary quotes, prompt replies and gifts finished with care.")}
'''
pages.append(dict(slug="faq.html", crumb="FAQ",
  title="Gift Wrapping FAQ | All Wrapped Up, Sweetwater TN",
  og_title="Gift Wrapping FAQ — All Wrapped Up, Sweetwater TN",
  desc="Answers on gift wrapping in East Tennessee: cost, pickup and delivery from Knoxville to Chattanooga, how early to book for Christmas, odd shapes and corporate branding.",
  ld=faq_ld, body=faq_body))

# CONTACT
contact_body = page_head("Contact", "Request a gift wrapping quote", f"Tell us what you are wrapping and when you need it. Quotes are returned within one business day. Prefer to talk? Call or text {PHONE}.", "Get a quote") + f'''
<section>
  <div class="wrap contact-grid">
    <form class="form-card reveal" data-contact data-mailto-to="{FORM_EMAIL}" action="{FORM_ACTION}" method="POST">
      <input type="hidden" name="_subject" value="New gift wrapping quote request">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="{SITE}/thank-you.html">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <div class="form-row">
        <div class="field"><label for="c-name">Your name *</label><input id="c-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="c-company">Company (if corporate)</label><input id="c-company" name="company" autocomplete="organization"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="c-email">Email *</label><input id="c-email" type="email" name="email" required autocomplete="email"></div>
        <div class="field"><label for="c-phone">Phone</label><input id="c-phone" type="tel" name="phone" autocomplete="tel"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="c-type">I'm wrapping for *</label><select id="c-type" name="client_type" required><option value="">Choose one</option><option value="corporate">A business / corporate event</option><option value="family">My family or household</option><option value="wedding">A wedding</option><option value="shower">A bridal or baby shower</option><option value="birthday">A birthday or anniversary</option><option value="other">Something else</option></select></div>
        <div class="field"><label for="c-count">Approximate number of gifts *</label><input id="c-count" type="number" name="gift_count" min="1" required inputmode="numeric"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="c-date">Need them by</label><input id="c-date" type="date" name="needed_by"></div>
        <div class="field"><label for="c-city">Your city</label><input id="c-city" name="city" placeholder="Sweetwater, Knoxville, Chattanooga…" autocomplete="address-level2"></div>
      </div>
      <div class="field"><label for="c-pickup">Pickup &amp; delivery?</label><select id="c-pickup" name="pickup"><option>I'll drop off in Sweetwater</option><option>Please pick up and deliver</option><option>Ship gifts directly to you</option><option>Not sure yet</option></select></div>
      <div class="field"><label for="c-msg">Tell us about the gifts</label><textarea id="c-msg" name="message" rows="5" placeholder="Sizes, colors you love, brand colors, anything oversized, event details…"></textarea></div>
      <button class="btn btn-primary btn-lg btn-block" type="submit">Send my quote request</button>
      <p class="form-note">Or <a href="#" data-mailto>open this request in your email app</a>. Your information is never shared.</p>
    </form>
    <aside class="info-card reveal">
      <h3>Reach {OWNER.split()[0]} directly</h3>
      <ul class="info-list">
        <li>{ICONS['phone']}<span>Call or text<br><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
        <li>{ICONS['mail']}<span>Email<br><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        <li>{ICONS['pin']}<span>Based in<br><strong>{CITY}, Tennessee {ZIP}</strong><br>Home-based. Drop-off by appointment; address shared when you book.</span></li>
        <li>{ICONS['truck']}<span>Pickup &amp; delivery<br>Knoxville · Maryville · Athens · Cleveland · Chattanooga</span></li>
      </ul>
      <div class="hours"><b>Appointments</b>By appointment, evenings and weekends included. Text to find a time.</div>
      <div class="hours"><b>Response time</b>Quotes within one business day. Texts usually faster.</div>
    </aside>
  </div>
</section>
'''
pages.append(dict(slug="contact.html", crumb="Contact",
  title=f"Get a Gift Wrapping Quote | {BIZ} | {PHONE}",
  og_title="Request a Free Gift Wrapping Quote — All Wrapped Up",
  desc=f"Free quote for corporate or family gift wrapping in Sweetwater, Knoxville or Chattanooga, TN. Call or text {PHONE} or email {EMAIL}.",
  body=contact_body))

# THANK YOU
pages.append(dict(slug="thank-you.html", crumb="Thank you", noindex=True,
  title="Thanks! Your quote request is in | All Wrapped Up",
  desc="Your gift wrapping quote request has been received.",
  body=page_head("Thank you", "Your request has been received", f"We will reply within one business day with pricing and next steps. For anything urgent, text {PHONE}.", "Thank you") + f'''
<section><div class="wrap" style="text-align:center"><div class="gift-tile reveal in" style="background:#fde4ee;width:220px;margin:0 auto 24px">{gift_svg("#fff","#e5648f","#fff","#b23a5e","#fde4ee")}</div>
<a class="btn btn-primary" href="index.html">Back to the home page</a></div></section>'''))

# 404
pages.append(dict(slug="404.html", crumb="Not found", noindex=True,
  title="Page not found | All Wrapped Up",
  desc="That page seems to have gone missing under the tree.",
  body=page_head("Not found", "That page could not be found", "The link may be out of date or mistyped. Here is the way back.", "404") + '''
<section><div class="wrap" style="text-align:center"><div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="index.html">Home</a><a class="btn btn-secondary" href="pricing.html">Pricing</a><a class="btn btn-secondary" href="contact.html">Get a quote</a></div></div></section>'''))

# ---------- write ----------
for p in pages:
    (ROOT / p["slug"]).write_text(layout(p), encoding="utf-8")
    print("wrote", p["slug"])

prio = {"index.html": "1.0", "corporate-gift-wrapping.html": "0.9", "holiday-gift-wrapping.html": "0.9", "pricing.html": "0.9", "services.html": "0.8", "contact.html": "0.8", "about.html": "0.6", "faq.html": "0.7"}
urls = "".join(f"  <url><loc>{SITE}/{'' if s=='index.html' else s}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n" for s, pr in prio.items())
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
(ROOT / "CNAME").write_text("allwrappeduptn.com\n", encoding="utf-8")
(ROOT / "site.webmanifest").write_text(_j.dumps({"name": f"{BIZ} — {TAG}", "short_name": BIZ, "start_url": "./index.html", "display": "standalone", "background_color": "#fffdfa", "theme_color": "#b23a5e", "icons": [{"src": "assets/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}, {"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2), encoding="utf-8")
print("wrote sitemap.xml robots.txt CNAME site.webmanifest")
