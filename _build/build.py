"""Assembles the static pages for rosaschimneyservices.com.
Run from this folder: python3 build.py  (writes the .html files one level up).
The finished site needs no build step; this only keeps header/footer in sync."""
import json, os
import re
from icons import I
from areas import COUNTIES, TOWNS
CBY = {c["slug"]: c for c in COUNTIES}

SITE = "https://rosaschimneyservices.com"
NAME = "Rosas Chimney Services"
PHONE_DISPLAY = "(540) 431-9629"
PHONE = "+15404319629"
EMAIL = "rosaschimneyservices@gmail.com"
FB = "https://www.facebook.com/RosasChimneyServicesLLC/"
IG = "https://www.instagram.com/rosaschimneyservices/"
BOOK = "https://calendar.app.google/X7SwnxsRZ6jpEQaa7"
YELP = "https://www.yelp.com/biz/rosas-chimney-services-front-royal"
CSIA = "11978"
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"),
       ("service-areas/index.html", "Service Areas"), ("contact.html", "Contact")]

BRAND = ('<a class="brand" href="index.html" aria-label="%s home">'
         '<img class="mark" src="assets/img/mark.svg" alt="" width="46" height="46">'
         '<span class="name"><b>Rosas</b><small>Chimney Services</small></span></a>') % NAME

def head(title, desc, path, extra=""):
    clean = path[:-len("index.html")] if path.endswith("index.html") else path
    canon = SITE + "/" + clean
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1c1613">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(path):
    cur = ' aria-current="page"'
    def is_cur(h):
        return h == path or (h.startswith("service-areas/") and path.startswith("service-areas/"))
    links = "".join(f'<a href="{h}"{cur if is_cur(h) else ""}>{t}</a>' for h, t in NAV)
    return f"""<div class="utility"><div class="wrap">
  <div class="u-left"><span>{I['clock']}<span data-open-status>Mon to Sat, 7 AM to 7 PM</span></span><span>{I['award']}CSIA Certified Sweep #{CSIA}</span></div>
  <div class="u-right"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div></div>
<header class="site-header"><div class="wrap">
  {BRAND}
  <nav class="nav" aria-label="Primary">{links}</nav>
  <div class="header-cta">
    <a class="btn btn-ghost-light mobile-only" href="sms:{PHONE}">{I['sms']}Text</a>
    <a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}{PHONE_DISPLAY}</a>
    <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span class="i-open">{I['menu']}</span><span class="i-close" style="display:none">{I['close']}</span></button>
  </div>
</div>
<nav id="mobile-nav" class="mobile-nav" aria-label="Primary (mobile)">
  {links}
  <div class="m-cta"><a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}Call</a><a class="btn btn-ghost mobile-only" href="sms:{PHONE}">{I['sms']}Text</a></div>
</nav>
</header>
<main id="main">
"""

def cta_band(title="Ready for a cleaner, safer chimney?", sub="Call or text for an estimate. We answer Monday through Saturday, 7 AM to 7 PM."):
    return f"""<section class="cta-band"><div class="wrap">
  <div><h2>{title}</h2><p>{sub}</p></div>
  <div class="actions"><a class="btn btn-light" href="tel:{PHONE}">{I['phone']}Call {PHONE_DISPLAY}</a><a class="btn btn-ghost-light" href="contact.html">Request an Estimate</a></div>
</div></section>
"""

def footer():
    svc = "".join(f'<li><a href="services.html#{a}">{t}</a></li>' for a, t in [
        ("sweeps", "Chimney Sweeps"), ("inspections", "Inspections"), ("repairs", "Repairs"),
        ("liners", "Liner Replacement"), ("caps", "Caps &amp; Weatherproofing"), ("installs", "Stoves &amp; Installations")])
    return f"""</main>
<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div>{BRAND}
      <p class="about-blurb">Family-owned chimney care for Warren County, the northern Shenandoah Valley, Loudoun and Fauquier. CSIA Certified and fully insured.</p>
      <div class="social"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{I['facebook']}</a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I['instagram']}</a><a href="{YELP}" target="_blank" rel="noopener" aria-label="Yelp reviews">{I['review']}</a></div>
    </div>
    <div><h4>Services</h4><ul>{svc}</ul></div>
    <div><h4>Service Areas</h4><ul>{"".join(f'<li><a href="service-areas/{c["slug"]}/index.html">{c["name"]}</a></li>' for c in COUNTIES)}</ul></div>
    <div><h4>Company</h4><ul><li><a href="about.html">About Us</a></li><li><a href="service-areas/index.html">All Service Areas</a></li><li><a href="services.html#faq">FAQ</a></li><li><a href="contact.html">Request an Estimate</a></li></ul></div>
    <div><h4>Contact</h4><ul class="foot-contact">
      <li>{I['phone']}<a href="tel:{PHONE}">{PHONE_DISPLAY}</a> (call or text)</li>
      <li>{I['mail']}<a href="mailto:{EMAIL}">{EMAIL.replace("@", "@<wbr>")}</a></li>
      <li>{I['clock']}<span>Mon to Sat, 7 AM to 7 PM<br>Closed Sunday</span></li>
      <li>{I['pin']}<span>Based in Front Royal, serving the Shenandoah Valley, Loudoun &amp; Fauquier</span></li>
    </ul></div>
  </div>
  <div class="foot-bottom"><span>&copy; <span id="year">2026</span> Rosas Chimney Services LLC. All rights reserved.</span><span>Designed and created by <a class="credit" href="https://finnoybu.com" target="_blank" rel="noopener">Ken Tannenbaum</a></span></div>
</div></footer>
<div class="call-bar"><a href="tel:{PHONE}">{I['phone']}Call</a><a href="sms:{PHONE}">{I['sms']}Text Us</a></div>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

def page_hero(crumb, eyebrow, h1, p):
    return f"""<section class="page-hero"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div>
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p>{p}</p>
</div></section>
"""

SCHEMA = {
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "name": "Rosas Chimney Services LLC",
  "url": SITE + "/",
  "logo": SITE + "/assets/img/apple-touch-icon.png",
  "image": SITE + "/assets/img/og-image.png",
  "telephone": PHONE,
  "email": EMAIL,
  "address": {"@type": "PostalAddress", "addressLocality": "Front Royal", "addressRegion": "VA", "addressCountry": "US"},
  "@id": SITE + "/#business",
  "areaServed": [{"@type": "AdministrativeArea", "name": c["name"] + ", VA"} for c in COUNTIES],
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "07:00", "closes": "19:00"}],
  "sameAs": [FB, IG, YELP],
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Chimney services", "itemListElement": [
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
    ["Chimney cleaning and sweeping", "Chimney and fireplace inspection", "Chimney repair", "Chimney liner replacement", "Chimney cap installation and weatherproofing", "Class A chimney, wood stove and pellet stove installation"]]}
}

SERVICES = [
 ("sweeps", "sweep", "Chimney Cleaning &amp; Sweeps", "Creosote and soot removed from the flue, smoke chamber and firebox, with your home protected by drop cloths and a HEPA vacuum the whole time."),
 ("inspections", "inspect", "Chimney &amp; Fireplace Inspections", "A certified, top-to-bottom look at your chimney, flue and fireplace so you know exactly what condition it is in before you light a fire."),
 ("repairs", "repair", "Chimney Repairs", "Crown, mortar, flashing and damper repairs that stop small problems from turning into water damage or an unsafe flue."),
 ("liners", "liner", "Chimney Liner Replacement", "Cracked or missing flue tiles replaced with a properly sized stainless steel liner for safer venting of wood, pellet, gas or oil."),
 ("caps", "cap", "Caps &amp; Weatherproofing", "Chimney caps, chase covers and masonry waterproofing that keep out rain, animals, debris and the freeze-thaw damage that follows."),
 ("installs", "stove", "Stoves &amp; Full Installations", "Complete installs of Class A metal chimneys and wood or pellet stoves, sized, vented and finished to code."),
]

WORK = [
 ("class-a-chimney-shingle-roof", "Class A chimney", "Stainless Class A chimney on a shingle roof"),
 ("wood-stove-installation", "Wood stove", "Wood stove and stovepipe on a protective hearth pad"),
 ("class-a-chimney-braced", "Class A chimney with braces", "Class A chimney with roof braces on a shingle roof"),
 ("flue-before-sweep", "Before the sweep", "Flue coated with creosote and debris before sweeping"),
 ("class-a-chimney-metal-roof", "Braced Class A chimney", "Class A chimney with support braces on a metal roof"),
 ("flue-after-sweep", "After the sweep", "The same flue after sweeping, cleared of creosote"),
]

def work_fig(slug, cap, alt, cls="work"):
    return (f'<figure class="{cls}"><img src="assets/img/work/{slug}.jpg" alt="{alt}" width="900" height="1125" loading="lazy">'
            f'<figcaption>{cap}</figcaption></figure>')

def index():
    cards = ""
    for i, (a, ic, t, d) in enumerate(SERVICES):
        feat = " feature" if i == 0 else ""
        cards += f'<article class="svc{feat} reveal"><div class="ico">{I[ic]}</div><h3>{t}</h3><p>{d}</p><a class="more" href="services.html#{a}">Learn more {I["arrow"]}</a></article>\n'
    stars = I['star'] * 5
    body = f"""<section class="hero">
  <img class="hero-art" src="assets/img/hero.svg" alt="" width="1600" height="900">
  <div class="wrap">
    <span class="eyebrow">Front Royal &middot; Luray &middot; Warren County</span>
    <h1>A safe, clean chimney <em>before the first fire.</em></h1>
    <p>Family-owned chimney sweeping, inspections, repairs and installations from a CSIA Certified sweep who treats your home like our own.</p>
    <div class="hero-actions">
      <a class="btn btn-ember" href="tel:{PHONE}">{I['phone']}Call {PHONE_DISPLAY}</a>
      <a class="btn btn-ghost-light" href="contact.html">Request an Estimate</a>
    </div>
    <p class="hero-note">Prefer texting? Send us a text at the same number for estimates and pricing.</p>
  </div>
</section>

<section class="trust"><div class="wrap"><div class="trust-inner">
  <div class="trust-item">{I['award']}<div><b>CSIA Certified</b><span>Chimney Sweep #{CSIA}</span></div></div>
  <div class="trust-item">{I['shield']}<div><b>Fully Insured</b><span>For your peace of mind</span></div></div>
  <div class="trust-item">{I['heart']}<div><b>Family-Owned</b><span>Local, small business</span></div></div>
  <div class="trust-item">{I['calendar']}<div><b>Six Days a Week</b><span>Mon to Sat, 7 AM to 7 PM</span></div></div>
</div></div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal">
    <span class="eyebrow">What We Do</span>
    <h2>Complete chimney care, from sweep to install</h2>
    <p class="lead">Whether it is a yearly cleaning or a brand new stove, you get the same careful, certified work and a clean living room when we leave.</p>
  </div>
  <div class="services-grid">
{cards}  </div>
</div></section>

<section class="section bg-cream"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Why Rosas</span>
    <h2>Certified know-how with a small-business handshake</h2>
    <p>When you call Rosas Chimney Services, you talk to the people who do the work. We explain what we find in plain language, show you photos of anything that needs attention, and never push repairs you do not need.</p>
    <ul class="check-list">
      <li>{I['check']}<span><b>CSIA Certified.</b> Trained to current Chimney Safety Institute of America standards.</span></li>
      <li>{I['check']}<span><b>Clean, careful work.</b> Drop cloths, HEPA vacuums and a tidy hearth every time.</span></li>
      <li>{I['check']}<span><b>Honest recommendations.</b> Clear findings and straightforward estimates, by call or text.</span></li>
      <li>{I['check']}<span><b>Fully insured.</b> Protection for your home and our crew on every job.</span></li>
    </ul>
    <div class="hero-actions"><a class="btn btn-primary" href="about.html">Meet the Family {I['arrow']}</a></div>
  </div>
  <div class="art-card reveal">
    <img src="assets/img/handshake.jpg" alt="Close-up of a friendly handshake" width="1000" height="800" loading="lazy">
    <div class="badge-float"><b>Sweep #{CSIA}</b><span>CSIA Certified &amp; insured</span></div>
  </div>
</div></section>

<section class="section bg-soot"><div class="wrap">
  <div class="section-head reveal">
    <span class="eyebrow">How It Works</span>
    <h2>Simple from first text to final sweep</h2>
  </div>
  <div class="steps">
    <div class="step reveal"><h3>Call or text</h3><p>Reach us at {PHONE_DISPLAY}. Tell us about your fireplace, stove or chimney and what you have noticed.</p></div>
    <div class="step reveal"><h3>Get a clear estimate</h3><p>We give you straightforward pricing and schedule a visit that works for you, six days a week.</p></div>
    <div class="step reveal"><h3>Certified service</h3><p>We protect your home, do the work right and walk you through what we found, with photos.</p></div>
    <div class="step reveal"><h3>Enjoy your fire</h3><p>Burn with confidence knowing your system is clean, inspected and ready for the season.</p></div>
  </div>
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="season reveal">
    {I['leaf']}
    <div><h3>Book before the cold snap</h3><p>Fall is our busiest season. The Chimney Safety Institute of America recommends an inspection every year, so schedule early to get the date you want. You can now book your visit online.</p></div>
    <a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">{I['calendar']}Schedule Online</a>
  </div>
</div></section>

<section class="section bg-cream"><div class="wrap area-wrap">
  <div class="reveal">
    <span class="eyebrow">Service Area</span>
    <h2 style="font-size:clamp(30px,4vw,42px);margin-bottom:16px">Nine counties, one local family</h2>
    <p class="lead">Based in Front Royal and serving the northern Shenandoah Valley, Rappahannock and Culpeper, and east of the Blue Ridge into Fauquier and western Loudoun.</p>
    <ul class="towns">{"".join(f'<li class="{"hub" if c["tier"] == "home" else ""}"><a href="service-areas/{c["slug"]}/index.html">{I["pin"]}{c["name"]}</a></li>' for c in COUNTIES)}</ul>
    <div class="hero-actions"><a class="btn btn-ghost" href="service-areas/index.html">See All Service Areas {I['arrow']}</a></div>
  </div>
  <div class="map-card reveal">{county_map(None)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal">
    <span class="eyebrow">Recent Work</span>
    <h2>From our jobs around the valley</h2>
    <p class="lead">A few recent jobs, and what a neglected flue looks like before we sweep it.</p>
  </div>
  <div class="work-grid">{"".join(work_fig(*w) for w in WORK)}</div>
</div></section>

<section class="section bg-cream"><div class="wrap">
  <div class="section-head center reveal">
    <div class="stars">{stars}</div>
    <span class="eyebrow">Reviews</span>
    <h2>See what your neighbors are saying</h2>
    <p class="lead">Read reviews from local homeowners, or leave one of your own after your service.</p>
  </div>
  <div class="reviews">
    <a class="review-link reveal" href="{FB}" target="_blank" rel="noopener"><span class="r-ico">{I['facebook']}</span><span><b>Facebook</b><span>Rosas Chimney Services LLC</span></span></a>
    <a class="review-link reveal" href="{YELP}" target="_blank" rel="noopener"><span class="r-ico">{I['review']}</span><span><b>Yelp</b><span>Reviews from Front Royal customers</span></span></a>
  </div>
</div></section>
""" + cta_band()
    extra = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>\n'
    return head("Rosas Chimney Services | Chimney Sweep in Front Royal &amp; Luray, VA",
                "Family-owned, CSIA Certified chimney sweep serving Warren County, Front Royal and Luray, VA. Chimney cleaning, inspections, repairs, liners, caps and stove installs. Call or text (540) 431-9629.",
                "index.html", extra) + header("index.html") + body + footer()

def services():
    jump = "".join(f'<a href="#{a}">{t}</a>' for a, _, t, _ in SERVICES) + '<a href="#faq">FAQ</a>'
    det = {
     "sweeps": f"""<p>Every fire leaves behind creosote, a sticky, flammable residue that builds up inside the flue. Regular sweeping is the single best way to prevent chimney fires and keep smoke going up and out instead of into your living room.</p>
<h3>What a sweep includes</h3><ul class="check-list">
<li>{I['check']}<span>Drop cloths and a HEPA vacuum to keep soot out of your home</span></li>
<li>{I['check']}<span>Brushing of the flue, smoke chamber, smoke shelf and firebox</span></li>
<li>{I['check']}<span>Check of the damper, cap and visible components while we are there</span></li>
<li>{I['check']}<span>A plain-language summary of anything that needs attention</span></li></ul>
<div class="svc-photos">{work_fig(*WORK[3])}{work_fig(*WORK[5])}</div>""",
     "inspections": f"""<p>We inspect to the levels defined in NFPA 211, the national standard for chimneys, fireplaces and vents. Most homes need a yearly Level 1, and certain situations call for a deeper look.</p>
<div class="levels">
<div class="level"><b>Level 1</b><p>An annual check of the readily accessible parts of the chimney, flue and appliance for a system that has not changed.</p></div>
<div class="level"><b>Level 2</b><p>Recommended when buying or selling a home, after a chimney fire or storm, or when changing your fuel or appliance. Includes a camera scan of the flue.</p></div>
<div class="level"><b>Level 3</b><p>Used only when a serious hidden problem is suspected and access requires removing parts of the structure.</p></div>
</div>""",
     "repairs": f"""<p>Weather is hard on masonry. Water gets into cracks, freezes and pushes them wider every winter. Catching damage early keeps repairs small and keeps water out of your attic and walls.</p>
<h3>Common repairs</h3><ul class="check-list">
<li>{I['check']}<span>Crown repair and rebuilding</span></li>
<li>{I['check']}<span>Tuckpointing and mortar joint repair</span></li>
<li>{I['check']}<span>Flashing repair to stop roof leaks around the chimney</span></li>
<li>{I['check']}<span>Damper repair and replacement</span></li></ul>""",
     "liners": f"""<p>Your flue liner protects the house from heat and keeps dangerous gases moving out. Cracked clay tiles, a missing liner, or a new stove or insert are all reasons to reline.</p>
<ul class="check-list">
<li>{I['check']}<span>Stainless steel liners sized to your appliance for proper draft</span></li>
<li>{I['check']}<span>Relining for wood, pellet, gas and oil appliances</span></li>
<li>{I['check']}<span>Insulated options where needed for clearance and performance</span></li></ul>""",
     "caps": f"""<p>A good chimney cap is inexpensive protection against rain, birds, squirrels, leaves and wind-driven downdrafts. Pair it with waterproofing and your masonry lasts years longer.</p>
<ul class="check-list">
<li>{I['check']}<span>Chimney cap installation and replacement</span></li>
<li>{I['check']}<span>Chase covers for framed or prefabricated chimneys</span></li>
<li>{I['check']}<span>Breathable masonry water repellent</span></li></ul>""",
     "installs": f"""<p>Adding heat or replacing an old system? We handle the full job, from venting to the finished hearth, so your new appliance is safe and drafts the way it should.</p>
<ul class="check-list">
<li>{I['check']}<span>Class A insulated metal chimney systems</span></li>
<li>{I['check']}<span>Wood stove installation</span></li>
<li>{I['check']}<span>Pellet stove installation and venting</span></li>
<li>{I['check']}<span>Full chimney installations for new or remodeled spaces</span></li></ul>
<div class="svc-photos">{work_fig(*WORK[1])}{work_fig(*WORK[0])}</div>""",
    }
    rows = ""
    for a, ic, t, d in SERVICES:
        q = t.replace("&amp;", "and")
        rows += f"""<article class="svc-detail" id="{a}">
  <div class="label"><div class="ico">{I[ic]}</div><div><h2>{t}</h2><p style="margin-top:10px;color:var(--stone);font-size:15px">{d}</p></div></div>
  <div class="body">{det[a]}<div class="hero-actions" style="margin-top:24px"><a class="btn btn-primary" href="contact.html?service={q.replace(' ', '%20')}">Request {q} {I['arrow']}</a></div></div>
</article>
"""
    faqs = [
     ("How often should my chimney be cleaned?", "The Chimney Safety Institute of America and NFPA 211 recommend an inspection every year, with cleaning whenever it is needed. Homes that burn wood often, or burn unseasoned wood, usually need a sweep at least once a year."),
     ("Is a sweep messy?", "It should not be. We use drop cloths and a HEPA vacuum and protect the area around your fireplace or stove, then leave the hearth clean when we are done."),
     ("What does CSIA Certified mean?", "It means our sweep has passed the Chimney Safety Institute of America certification exams on chimney and venting safety and keeps that certification current with ongoing education. Our certification number is %s." % CSIA),
     ("How do I get pricing?", "Call or text (540) 431-9629 with a short description of your chimney or appliance, or use our estimate form. We will give you straightforward pricing before any work begins."),
     ("Do you work on pellet and wood stoves?", "Yes. We clean, inspect and install wood and pellet stoves, including the venting and Class A chimney they connect to."),
     ("What areas do you serve?", "We serve Warren County, including Front Royal, south to Luray and the surrounding communities. If you are nearby and not sure, just ask."),
    ]
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    body = page_hero("Services", "Our Services", "Chimney services done right, and done clean",
                     "Sweeps, inspections, repairs, liners, caps and complete installations from a CSIA Certified, fully insured local team.")
    body += f"""<section class="section-sm bg-cream"><div class="wrap"><nav class="jump" aria-label="Jump to a service">{jump}</nav></div></section>
<section><div class="wrap">
{rows}</div></section>
<section class="section bg-cream" id="faq"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
  <div class="faq">{faq}</div>
</div></section>
""" + cta_band()
    extra = '<script type="application/ld+json">' + json.dumps(faq_schema) + '</script>\n'
    return head("Chimney Services | Sweeps, Inspections, Liners &amp; Repair | Rosas Chimney Services",
                "Chimney cleaning, NFPA 211 inspections, repairs, stainless liner replacement, chimney caps, waterproofing and Class A, wood and pellet stove installs in Warren County, VA.",
                "services.html", extra) + header("services.html") + body + footer()

def about():
    body = page_hero("About", "About Us", "A family business built on honest, careful work",
                     "Rosas Chimney Services is a small, family-owned company serving homeowners across Warren County and the Shenandoah Valley.")
    body += f"""<section class="section"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Our Story</span>
    <h2>We’re Mark and Peyton</h2>
    <p>Rosas Chimney Services was started with a simple idea: homeowners deserve a chimney company that shows up when it says it will, explains things clearly and leaves the house cleaner than it found it.</p>
    <p>As a small, local business, every job carries our name. That is why we take the time to do it right, from a routine sweep to a full stove and chimney installation.</p>
    <div class="tags"><span>Family-owned</span><span>Latino-owned</span><span>Women-owned</span><span>Small business</span></div>
    <div class="cred">{I['award']}<div><b>CSIA Certified Chimney Sweep #{CSIA}</b><span>Certified by the Chimney Safety Institute of America and fully insured.</span></div></div>
  </div>
  <div class="art-card photo reveal"><img src="assets/img/mark-and-peyton.jpg" alt="Mark and Peyton of Rosas Chimney Services, smiling outdoors in the Shenandoah Valley" width="1080" height="1350" loading="lazy"></div>
</div></section>

<section class="section bg-cream"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">What You Can Count On</span><h2>How we work</h2></div>
  <div class="values">
    <div class="value reveal">{I['shield']}<h3>Safety first</h3><p>Every visit is about one thing: a chimney and venting system that is safe to use.</p></div>
    <div class="value reveal">{I['home']}<h3>Respect for your home</h3><p>Drop cloths, HEPA vacuums and a clean hearth. We treat your house like our own.</p></div>
    <div class="value reveal">{I['users']}<h3>Straight answers</h3><p>Clear findings, photos when helpful and honest pricing. No pressure, no surprises.</p></div>
  </div>
</div></section>
""" + cta_band("Let us take care of your chimney", "Call or text the family at (540) 431-9629.")
    return head("About Us | Family-Owned Chimney Sweep | Rosas Chimney Services",
                "Meet Rosas Chimney Services, a family-owned, CSIA Certified and fully insured chimney company serving Warren County, Front Royal and Luray, VA.",
                "about.html") + header("about.html") + body + footer()

def area():
    body = page_hero("Service Area", "Where We Work", "Serving Warren County and the surrounding valley",
                     "From Front Royal to Luray, we bring certified chimney care to homes across the northern Shenandoah Valley.")
    body += f"""<section class="section"><div class="wrap area-wrap">
  <div class="reveal">
    <span class="eyebrow">Communities</span>
    <h2 style="font-size:clamp(30px,4vw,42px);margin-bottom:16px">Local to you</h2>
    <p class="lead">We are based in the Front Royal area and regularly serve Warren County, Luray and Page County, and nearby communities in between.</p>
    <ul class="towns"><li class="hub">{I['pin']}Front Royal</li><li class="hub">{I['pin']}Luray</li><li>{I['pin']}Warren County</li><li>{I['pin']}Page County</li><li>{I['pin']}Surrounding communities</li></ul>
    <p style="margin-top:26px;color:var(--stone)">Not sure if you are in our area? Send a text with your town and we will let you know right away.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}Call {PHONE_DISPLAY}</a><a class="btn btn-ghost" href="contact.html">Request an Estimate</a></div>
  </div>
  <div class="map-card reveal"><img src="assets/img/area-map.svg" alt="Stylized map showing the service area around Front Royal and Luray, Virginia" width="560" height="520" loading="lazy"></div>
</div></section>
""" + cta_band()
    return head("Service Area | Chimney Sweep for Front Royal, Luray &amp; Warren County | Rosas Chimney Services",
                "Rosas Chimney Services serves Warren County, Front Royal, Luray, Page County and surrounding Shenandoah Valley communities. Call or text (540) 431-9629.",
                "service-area.html") + header("service-area.html") + body + footer()

def contact():
    opts = ["Chimney cleaning and sweep", "Chimney inspection", "Chimney repair", "Chimney liner replacement", "Chimney cap or weatherproofing", "Wood or pellet stove installation", "Class A chimney installation", "Something else"]
    # values that services.html links pass in via ?service=
    alias = {"Chimney Cleaning and Sweeps": "Chimney cleaning and sweep", "Chimney and Fireplace Inspections": "Chimney inspection",
             "Chimney Repairs": "Chimney repair", "Chimney Liner Replacement": "Chimney liner replacement",
             "Caps and Weatherproofing": "Chimney cap or weatherproofing", "Stoves and Full Installations": "Wood or pellet stove installation"}
    options = '<option value="" disabled selected>Choose a service</option>' + "".join(f'<option value="{o}">{o}</option>' for o in opts)
    body = page_hero("Contact", "Get In Touch", "Request an estimate",
                     "The fastest way to reach us is a call or text. You can also send the form below and we will get back to you.")
    body += f"""<section class="section"><div class="wrap contact-grid">
  <div class="contact-cards">
    <a class="c-card" href="tel:{PHONE}"><span class="ico">{I['phone']}</span><span><small>Call</small><b>{PHONE_DISPLAY}</b></span></a>
    <a class="c-card mobile-only" href="sms:{PHONE}"><span class="ico">{I['sms']}</span><span><small>Text for estimates &amp; pricing</small><b>{PHONE_DISPLAY}</b></span></a>
    <a class="c-card" href="mailto:{EMAIL}"><span class="ico">{I['mail']}</span><span><small>Email</small><b>{EMAIL.replace("@", "@<wbr>")}</b></span></a>
    <div class="c-card" style="align-items:flex-start"><span class="ico">{I['clock']}</span><span style="flex:1"><small>Hours</small>
      <table class="hours"><tbody>
        <tr><td>Mon to Fri</td><td>7 AM to 7 PM</td></tr>
        <tr><td>Saturday</td><td>7 AM to 7 PM</td></tr>
        <tr class="closed"><td>Sunday</td><td>Closed</td></tr>
      </tbody></table></span></div>
    <a class="c-card" href="{FB}" target="_blank" rel="noopener"><span class="ico">{I['facebook']}</span><span><small>Follow us</small><b>Facebook</b></span></a>
    <a class="c-card" href="{IG}" target="_blank" rel="noopener"><span class="ico">{I['instagram']}</span><span><small>See our work</small><b>Instagram</b></span></a>
  </div>
  <div class="form-card">
    <h2>Tell us about your chimney</h2>
    <p>Fields marked <span style="color:var(--brick)">*</span> are required.</p>
    <form id="estimate-form" novalidate>
      <div class="form-row">
        <div class="field"><label for="name">Name <span class="req">*</span></label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
      </div>
      <fieldset class="addr">
        <legend>Service address <span class="req">*</span></legend>
        <div class="field"><label for="address1">Street address <span class="req">*</span></label><input id="address1" name="address1" autocomplete="address-line1" required></div>
        <div class="field"><label for="address2">Apt, suite, unit, etc. <span class="opt">(optional)</span></label><input id="address2" name="address2" autocomplete="address-line2"></div>
        <div class="form-row-3">
          <div class="field"><label for="city">City or town <span class="req">*</span></label><input id="city" name="city" autocomplete="address-level2" required></div>
          <div class="field"><label for="state">State <span class="req">*</span></label><input id="state" name="state" autocomplete="address-level1" value="VA" maxlength="2" pattern="[A-Za-z]{{2}}" title="Two-letter state, e.g. VA" required></div>
          <div class="field"><label for="zip">ZIP code <span class="req">*</span></label><input id="zip" name="zip" autocomplete="postal-code" inputmode="numeric" maxlength="10" pattern="[0-9]{{5}}(-[0-9]{{4}})?" title="5-digit ZIP code, e.g. 22630" required></div>
        </div>
      </fieldset>
      <div class="field"><label for="service">Service needed <span class="req">*</span></label><select id="service" name="service" required>{options}</select></div>
      <div class="field"><label for="message">Details</label><textarea id="message" name="message" placeholder="Fireplace, wood stove or pellet stove? Anything you have noticed, like smoke, odors or leaks?"></textarea></div>
      <div class="field"><span style="font-size:13.5px;font-weight:600;color:var(--smoke)">Best way to reach you</span>
        <div class="radio-row"><label><input type="radio" name="contact" value="Call" checked> Call</label><label><input type="radio" name="contact" value="Text"> Text</label><label><input type="radio" name="contact" value="Email"> Email</label></div></div>
      <div class="form-foot">
        <small>Sending opens your email app with your request filled in.</small>
        <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-ghost mobile-only" type="submit" value="sms">{I['sms']}Send by Text</button><button class="btn btn-primary" type="submit" value="email">{I['mail']}Send by Email</button></div>
      </div>
      <div id="form-msg" class="form-msg" role="status" aria-live="polite"></div>
    </form>
  </div>
</div></section>
<script>window.SERVICE_ALIAS={json.dumps(alias)};</script>
"""
    return head("Contact &amp; Estimates | Rosas Chimney Services | (540) 431-9629",
                "Call or text (540) 431-9629 for chimney service estimates and pricing in Warren County, Front Royal and Luray, VA. Open Monday to Saturday, 7 AM to 7 PM.",
                "contact.html") + header("contact.html") + body + footer()

def notfound():
    body = page_hero("Page not found", "404", "That page went up the flue",
                     "The page you are looking for is not here. Try one of the links below, or give us a call.")
    body += f"""<section class="section"><div class="wrap" style="text-align:center">
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="index.html">Back to Home</a><a class="btn btn-ghost" href="services.html">Our Services</a><a class="btn btn-ghost" href="tel:{PHONE}">{I['phone']}{PHONE_DISPLAY}</a></div>
</div></section>
"""
    return head("Page Not Found | Rosas Chimney Services", "This page could not be found.", "404.html") + header("") + body + footer()

# ---------------- Service-area pages (inserted into build.py) ----------------
POLY = {
 "frederick-county": "286,47 423,104 401,229 366,297 291,314 190,257 225,144",
 "clarke-county": "423,104 511,132 511,246 454,303 366,297 401,229",
 "warren-county": "366,297 454,303 436,399 374,439 304,394 291,314",
 "shenandoah-county": "291,314 190,257 53,445 128,541 163,530 304,394",
 "page-county": "304,394 163,530 207,638 278,598 330,530 374,439",
 "rappahannock-county": "374,439 436,399 467,473 436,541 357,587 278,598 330,530",
 "culpeper-county": "357,587 436,541 546,553 599,598 533,695 436,712 392,666",
 "loudoun-county": "511,132 559,132 674,189 731,280 691,348 643,399 546,359 454,303 511,246",
 "fauquier-county": "454,303 546,359 603,382 612,541 599,598 546,553 436,541 467,473 436,399",
}
LBL = {"frederick-county": (290, 172, 19), "clarke-county": (462, 182, 19), "warren-county": (378, 332, 18),
       "shenandoah-county": (160, 457, 19), "page-county": (245, 582, 19), "rappahannock-county": (394, 527, 14),
       "culpeper-county": (495, 652, 19), "loudoun-county": (600, 277, 19), "fauquier-county": (530, 467, 19)}

def county_map(highlight, link=True):
    """Inline SVG map of the nine counties. highlight=None marks Warren as home base."""
    hi = highlight or "warren-county"
    out = ['<svg class="cmap" viewBox="40 36 704 690" role="img" aria-label="Map of the Rosas Chimney Services area: '
           + ", ".join(c["name"] for c in COUNTIES) + ', Virginia">']
    for c in COUNTIES:
        sl = c["slug"]; on = sl == hi
        poly = (f'<polygon points="{POLY[sl]}" fill="{"#9b3a22" if on else "#f6c99b"}" fill-opacity="{0.9 if on else 0.55}" '
                f'stroke="{"#7a2b17" if on else "#b4512b"}" stroke-width="2" stroke-linejoin="round"/>')
        x, y, fs = LBL[sl]
        txt = (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="{fs}" '
               f'font-weight="600" fill="{"#ffffff" if on else "#2a2320"}">{c["name"].replace(" County", "")}</text>')
        if link:
            out.append(f'<a href="service-areas/{sl}/index.html" aria-label="{c["name"]}">{poly}{txt}</a>')
        else:
            out.append(poly + txt)
    fr_fill = "#ffffff" if hi == "warren-county" else "#2a2320"
    out.append(f'<circle cx="352" cy="359" r="6" fill="#e07a2e" stroke="#fff" stroke-width="2"/>'
               f'<text x="352" y="384" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="13" fill="{fr_fill}">Front Royal</text>')
    out.append('<text x="52" y="716" font-family="Inter,Arial,sans-serif" font-size="13" fill="#9a9089">Approximate county outlines</text></svg>')
    return "".join(out)

def relink(html, depth):
    if depth == 0:
        return html
    pre = "../" * depth
    return re.sub(r'(href|src)="(?!https?:|tel:|sms:|mailto:|#|data:|/)([^"]*)"', lambda m: f'{m.group(1)}="{pre}{m.group(2)}"', html)

def clean_url(path):
    return SITE + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)

def breadcrumb(items):
    """items: [(name, path or None)] -> (html, json-ld)"""
    parts = []
    for name, path in items:
        parts.append(f'<a href="{path}">{name}</a>' if path else f'<span aria-current="page">{name}</span>')
    html = ' &nbsp;/&nbsp; '.join(parts)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n.replace("&amp;", "&"), **({"item": clean_url(p)} if p else {})}
        for i, (n, p) in enumerate(items)]}
    return html, ld

def area_hero(crumb_html, eyebrow, h1, p):
    return f"""<section class="page-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb">{crumb_html}</nav>
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p>{p}</p>
</div></section>
"""

def ld(*objs):
    return "".join('<script type="application/ld+json">' + json.dumps(o) + '</script>\n' for o in objs)

def svc_links():
    return "".join(f'<li><a href="services.html#{a}">{I[ic]}<span>{t}</span></a></li>' for a, ic, t, _ in SERVICES)

def side_card(town_label, county):
    q = town_label.replace(" ", "%20")
    return f"""<aside class="area-side">
  <div class="side-card">
    <b>Get an estimate</b>
    <p>Call or text for pricing. We answer Monday to Saturday, 7 AM to 7 PM.</p>
    <a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}{PHONE_DISPLAY}</a>
    <a class="btn btn-ghost mobile-only" href="sms:{PHONE}">{I['sms']}Text Us</a>
    <a class="btn btn-ghost" href="contact.html?town={q}">Request Online</a>
  </div>
  <div class="side-card map-mini">{county_map(county)}</div>
</aside>"""

WHY = f"""<ul class="check-list">
  <li>{I['check']}<span><b>CSIA Certified Chimney Sweep #{CSIA}.</b> Trained to current Chimney Safety Institute of America standards.</span></li>
  <li>{I['check']}<span><b>Fully insured.</b> Protection for your home and our crew on every job.</span></li>
  <li>{I['check']}<span><b>Family-owned and local.</b> You talk to the people who do the work, not a call center.</span></li>
  <li>{I['check']}<span><b>Clean, careful work.</b> Drop cloths, HEPA vacuums and photos of anything that needs attention.</span></li>
</ul>"""

TOWN_BY = {t["slug"]: t for t in TOWNS}

def town_page(t):
    c = CBY[t["county"]]
    path = f'service-areas/{c["slug"]}/{t["slug"]}.html'
    crumb_html, crumb_ld = breadcrumb([("Home", "index.html"), ("Service Areas", "service-areas/index.html"),
                                       (c["name"], f'service-areas/{c["slug"]}/index.html'), (t["name"], None)])
    near = "".join(f'<li><a href="service-areas/{TOWN_BY[n]["county"]}/{n}.html">{I["pin"]}{TOWN_BY[n]["name"]}</a></li>' for n in t["near"])
    near += f'<li class="hub"><a href="service-areas/{c["slug"]}/index.html">{I["pin"]}All of {c["name"]}</a></li>'
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "@id": clean_url(path) + "#service",
              "name": f'Chimney services in {t["name"]}, VA', "serviceType": "Chimney sweeping, inspection and repair",
              "url": clean_url(path), "provider": {"@id": SITE + "/#business"},
              "areaServed": {"@type": "City", "name": f'{t["name"]}, VA', "containedInPlace": {"@type": "AdministrativeArea", "name": c["name"] + ", VA"}}}
    body = area_hero(crumb_html, t["note"], f'Chimney Sweep &amp; Chimney Services in {t["name"]}, VA',
                     f'CSIA Certified, family-owned chimney care for {t["name"]} and the rest of {c["name"]}.')
    body += f"""<section class="section"><div class="wrap area-layout">
  <div class="area-main">
    <p class="lead-lg">{t["intro"]}</p>
    <div class="hero-actions"><a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}Call {PHONE_DISPLAY}</a><a class="btn btn-ghost" href="contact.html?town={t["name"].replace(" ", "%20")}">Request an Estimate</a></div>
    <h2>Chimney services we provide in {t["name"]}</h2>
    <ul class="svc-links">{svc_links()}</ul>
    <h2>A local chimney company for {t["name"]} homeowners</h2>
    <p>{t["context"]}</p>
    <h2>Why {t["name"]} homeowners choose Rosas</h2>
    {WHY}
    <h2>Nearby communities we serve</h2>
    <ul class="towns">{near}</ul>
  </div>
  {side_card(t["name"], c["slug"])}
</div></section>
""" + cta_band(f'Ready for a safer chimney in {t["name"]}?', "Call or text for an estimate, or send a request online.")
    meta = (f'Chimney sweep in {t["name"]}, VA. Family-owned, CSIA Certified and insured chimney cleaning, inspections, '
            f'repairs, liners, caps and stove installs in {c["name"]}. Call or text (540) 431-9629.')
    return path, head(f'Chimney Sweep in {t["name"]}, VA | Rosas Chimney Services', meta, path, ld(crumb_ld, svc_ld)) + header(path) + body + footer()

def county_page(c):
    path = f'service-areas/{c["slug"]}/index.html'
    towns = [t for t in TOWNS if t["county"] == c["slug"]]
    crumb_html, crumb_ld = breadcrumb([("Home", "index.html"), ("Service Areas", "service-areas/index.html"), (c["name"], None)])
    cards = "".join(f'<a class="town-card" href="service-areas/{c["slug"]}/{t["slug"]}.html"><span class="ico">{I["pin"]}</span><span><b>{t["name"]}</b><small>{t["note"]}</small></span>{I["arrow"]}</a>' for t in towns)
    places = "".join(f'<li>{p}</li>' for p in c["places"])
    others = "".join(f'<li><a href="service-areas/{o["slug"]}/index.html">{I["pin"]}{o["name"]}</a></li>' for o in COUNTIES if o["slug"] != c["slug"])
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "@id": clean_url(path) + "#service",
              "name": f'Chimney services in {c["name"]}, VA', "serviceType": "Chimney sweeping, inspection and repair",
              "url": clean_url(path), "provider": {"@id": SITE + "/#business"},
              "areaServed": {"@type": "AdministrativeArea", "name": c["name"] + ", VA"}}
    body = area_hero(crumb_html, "Service Area", f'Chimney Services in {c["name"]}, VA', c["intro"])
    body += f"""<section class="section"><div class="wrap area-layout">
  <div class="area-main">
    <h2>Chimney care across {c["name"]}</h2>
    <p>{c["overview"]}</p>
    <h2>Communities in {c["name"]}</h2>
    <div class="town-cards">{cards}</div>
    <h3 class="also">Also serving</h3>
    <ul class="places">{places}<li>and the surrounding area</li></ul>
    <h2>What we do</h2>
    <ul class="svc-links">{svc_links()}</ul>
    <h2>Other counties we serve</h2>
    <ul class="towns">{others}</ul>
  </div>
  {side_card(towns[0]["name"] if towns else c["name"], c["slug"])}
</div></section>
""" + cta_band(f'Serving homeowners across {c["name"]}', "Call or text for an estimate. We answer Monday through Saturday, 7 AM to 7 PM.")
    town_names = ", ".join(t["name"] for t in towns)
    meta = (f'Chimney sweep and chimney services in {c["name"]}, VA, including {town_names}. CSIA Certified, family-owned '
            f'and insured. Call or text (540) 431-9629.')
    return path, head(f'Chimney Sweep in {c["name"]}, VA | Rosas Chimney Services', meta, path, ld(crumb_ld, svc_ld)) + header(path) + body + footer()

def hub_page():
    path = "service-areas/index.html"
    crumb_html, crumb_ld = breadcrumb([("Home", "index.html"), ("Service Areas", None)])
    cards = ""
    for c in COUNTIES:
        towns = [t for t in TOWNS if t["county"] == c["slug"]]
        tl = "".join(f'<li><a href="service-areas/{c["slug"]}/{t["slug"]}.html">{t["name"]}</a></li>' for t in towns)
        tag = {"home": "Home base", "core": "", "extended": ""}[c["tier"]]
        cards += f"""<article class="county-card{' home' if c['tier'] == 'home' else ''}">
  <h3><a href="service-areas/{c["slug"]}/index.html">{c["name"]}</a>{f'<span class="tag">{tag}</span>' if tag else ''}</h3>
  <ul>{tl}</ul>
  <a class="more" href="service-areas/{c["slug"]}/index.html">View {c["name"]} {I['arrow']}</a>
</article>"""
    body = area_hero(crumb_html, "Where We Work", "Our Service Areas",
                     "From our home base in Front Royal, Rosas Chimney Services serves nine counties across the northern Shenandoah Valley, the Piedmont and western Loudoun.")
    body += f"""<section class="section"><div class="wrap area-wrap">
  <div>
    <span class="eyebrow">Nine Counties</span>
    <h2 style="font-size:clamp(30px,4vw,42px);margin-bottom:16px">Local chimney care, close to home</h2>
    <p class="lead">Tap a county on the map or choose your community below. Not sure if you are in our area? Give us a call with your town and we will let you know right away.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="tel:{PHONE}">{I['phone']}Call {PHONE_DISPLAY}</a><a class="btn btn-ghost" href="contact.html">Request an Estimate</a></div>
  </div>
  <div class="map-card">{county_map(None)}</div>
</div></section>
<section class="section bg-cream"><div class="wrap"><div class="county-grid">{cards}</div></div></section>
""" + cta_band()
    meta = ("Rosas Chimney Services serves Warren, Frederick, Clarke, Shenandoah, Page, Rappahannock, Culpeper, Fauquier and "
            "Loudoun counties in Virginia. CSIA Certified chimney sweep. Call or text (540) 431-9629.")
    return path, head("Service Areas | Chimney Sweep for the Shenandoah Valley, Loudoun &amp; Fauquier | Rosas Chimney Services",
                      meta, path, ld(crumb_ld)) + header(path) + body + footer()

def area_pages():
    out = dict([hub_page()])
    for c in COUNTIES:
        out.update([county_page(c)])
    for t in TOWNS:
        out.update([town_page(t)])
    return out

def write_sitemap(pages):
    pri = lambda p: "1.0" if p == "index.html" else "0.9" if p in ("services.html", "service-areas/index.html") else "0.8" if p.endswith("/index.html") or p == "contact.html" else "0.7"
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        if p == "404.html":
            continue
        x += f'  <url><loc>{clean_url(p)}</loc><lastmod>2026-11-04</lastmod><priority>{pri(p)}</priority></url>\n'
    open(os.path.join(OUT, "sitemap.xml"), "w").write(x + "</urlset>\n")
    open(os.path.join(OUT, "assets/img/area-map.svg"), "w").write(
        county_map(None, link=False).replace('<svg class="cmap"', '<svg xmlns="http://www.w3.org/2000/svg"'))

pages = {"index.html": index(), "services.html": services(), "about.html": about(),
         "contact.html": contact(), "404.html": notfound()}
pages.update(area_pages())
for name, html in pages.items():
    depth = name.count("/")
    full = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(relink(html, depth))
write_sitemap(pages)
print("built", len(pages), "pages")
