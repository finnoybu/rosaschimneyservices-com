"""Builds the Rosas logo set from the primary shield logo (brand/rosas-logo-primary.svg).

Every other logo reuses the primary's own artwork (chimney, roses, rule, ROSAS and
CHIMNEY SERVICES lettering), so the whole set always matches it. Run from _build/:
    python3 brand_set.py
Writes to brand/ and refreshes the site's header logo, footer shield and favicon SVGs in assets/img/.
"""
import os, re, copy
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, "..", "brand")
SITE_IMG = os.path.join(HERE, "..", "assets", "img")
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

NAVY, RED, GOLD = "#2b3d4f", "#a63c24", "#d79136"
CREAM, EMBER = "#F6EBDD", "#E07A2E"          # lettering, outline and rule on dark backgrounds

# Bounding boxes of the primary's parts, in its drawing units (measured in a browser).
EMBLEM = (-777.89, 64.27, 405.90, 250.48)   # chimney + both roses
ROSAS = (-803.83, 356.03, 457.79, 84.15)
SUB = (-803.83, 460.18, 457.79, 28.96)      # CHIMNEY SERVICES
RULE = (-803.83, 333.38, 457.79, 4.14)
SHIELD = (-858.76, -90.46, 567.65, 760.75)  # border as drawn (it carries translate(0,-15))

def load(path):
    tree = ET.parse(path); root = tree.getroot()
    ids = {e.get("id"): e for e in root.iter() if e.get("id")}
    return root, ids

def clean(el):
    """Copy an element, dropping editor-only attributes."""
    el = copy.deepcopy(el)
    for e in el.iter():
        for k in list(e.attrib):
            if k.startswith("{http://www.inkscape.org") or k.startswith("{http://sodipodi"):
                del e.attrib[k]
    return el

def recolor(el, old, new):
    for e in el.iter():
        for k in ("fill", "stroke", "style"):
            v = e.get(k)
            if v: e.set(k, re.sub(re.escape(old), new, v, flags=re.I))
    return el

def xml(el):
    return ET.tostring(el, encoding="unicode").replace("ns0:", "").replace(":ns0", "")

def place(el, box, X, Y, s=1.0):
    """Wrap a part so its box lands at (X, Y) scaled by s."""
    x0, y0 = box[0], box[1]
    return f'<g transform="translate({X - s * x0:.3f},{Y - s * y0:.3f}) scale({s:.5f})">{xml(el)}</g>'

def doc(w, h, body, title, pad=0):
    return (f'<svg xmlns="{SVG}" viewBox="{-pad:.2f} {-pad:.2f} {w + 2 * pad:.2f} {h + 2 * pad:.2f}" '
            f'width="{w + 2 * pad:.0f}" height="{h + 2 * pad:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def parts(ids):
    p = {k: clean(ids[v]) for k, v in dict(border="path1", rule="rect60", chimney="g113", rosas="path60-1",
                                            sub="chimney-services", rose_l="path6", rose_r="path113").items()}
    emblem = ET.Element(f"{{{SVG}}}g"); emblem.extend([p["chimney"], p["rose_l"], p["rose_r"]])
    p["emblem"] = emblem
    return p

def reversed_text(p):
    q = {k: copy.deepcopy(v) for k, v in p.items()}
    recolor(q["rosas"], NAVY, CREAM); recolor(q["border"], NAVY, CREAM)
    recolor(q["rule"], RED, EMBER); recolor(q["rule"], "#b5452c", EMBER)
    return q

def horizontal(p, title):
    s = EMBLEM[3] / (ROSAS[3] + 13 + RULE[3] + 13 + SUB[3])   # text block as tall as the emblem
    tx = EMBLEM[2] + 70
    y_rule = s * (ROSAS[3] + 13); y_sub = s * (ROSAS[3] + 13 + RULE[3] + 13)
    body = (place(p["emblem"], EMBLEM, 0, 0) + place(p["rosas"], ROSAS, tx, 0, s)
            + place(p["rule"], RULE, tx, y_rule, s) + place(p["sub"], SUB, tx, y_sub, s))
    return doc(tx + ROSAS[2] * s, EMBLEM[3], body, title, pad=14)

def icon(p, title):
    border = copy.deepcopy(p["border"])
    border.set("style", re.sub(r"stroke-width:[\d.]+", "stroke-width:8", border.get("style", "")))
    e = 1.22; cx = SHIELD[0] + SHIELD[2] / 2; cy = 282
    ex, ey = cx - EMBLEM[2] * e / 2, cy - EMBLEM[3] * e / 2
    body = (f'<g transform="translate({-SHIELD[0]:.3f},{-SHIELD[1]:.3f})">{xml(border)}'
            + place(p["emblem"], EMBLEM, ex, ey, e) + "</g>")
    return doc(SHIELD[2], SHIELD[3], body, title, pad=6)

def favicon(p, title):
    side = EMBLEM[2]; dy = (side - EMBLEM[3]) / 2
    return doc(side, side, place(p["emblem"], EMBLEM, 0, dy), title, pad=8)

def primary_reversed(path):
    """The primary with cream outline and lettering and an ember rule, for dark backgrounds."""
    s = open(path, encoding="utf-8").read()
    s = s.replace(f'fill="{NAVY}"', f'fill="{CREAM}"').replace(f'stroke="{NAVY}"', f'stroke="{CREAM}"')
    return re.sub(r'(id="rect60"\s+style=")fill:#a63c24', r"\g<1>fill:" + EMBER, s)

def primary_cream(path):
    """The primary with the shield filled cream, so it reads on dark backgrounds (site footer)."""
    s = open(path, encoding="utf-8").read()
    return s.replace("stroke-dasharray:none;fill:none", "stroke-dasharray:none;fill:" + CREAM, 1)

if __name__ == "__main__":
    src = os.path.join(BRAND, "rosas-logo-primary.svg")
    root, ids = load(src)
    p = parts(ids); r = reversed_text(p)
    out = {
        "rosas-logo-horizontal.svg": horizontal(p, "Rosas Chimney Services"),
        "rosas-logo-horizontal-reversed.svg": horizontal(r, "Rosas Chimney Services"),
        "rosas-logo-icon.svg": icon(p, "Rosas Chimney Services"),
        "rosas-logo-icon-reversed.svg": icon(r, "Rosas Chimney Services"),
        "rosas-favicon.svg": favicon(p, "Rosas Chimney Services"),
        "rosas-logo-primary-reversed.svg": primary_reversed(src),
        "rosas-logo-primary-cream.svg": primary_cream(src),
    }
    for name, text in out.items():
        open(os.path.join(BRAND, name), "w", encoding="utf-8").write(text)
    open(os.path.join(SITE_IMG, "logo-horizontal-light.svg"), "w", encoding="utf-8").write(out["rosas-logo-horizontal-reversed.svg"])
    open(os.path.join(SITE_IMG, "favicon.svg"), "w", encoding="utf-8").write(out["rosas-favicon.svg"])
    open(os.path.join(SITE_IMG, "logo-shield.svg"), "w", encoding="utf-8").write(out["rosas-logo-primary-cream.svg"])
    print("wrote", ", ".join(out))
