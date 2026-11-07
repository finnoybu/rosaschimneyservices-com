"""Vector redraw of the Rosas Chimney Services logo.
Writes SVGs (text converted to outlines) to ../brand/. Run: python3 logo.py"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = os.path.join(os.path.dirname(__file__), "..", "brand")
FONT = TTFont("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf")
GS, CMAP, UPM = FONT.getGlyphSet(), FONT.getBestCmap(), FONT["head"].unitsPerEm
KERN = None

NAVY, BRICK, BRICK_DK, MORTAR_SH = "#2B3D4F", "#A63C24", "#4A1F15", "#7A2B18"
GOLD, GOLD_TXT, CREAM, RULE = "#D99A3E", "#A8742A", "#FBE8C6", "#B5452C"

def text_width(txt, size, tracking=0):
    w = sum(GS[CMAP[ord(c)]].width for c in txt) * size / UPM
    return w + tracking * (len(txt) - 1)

def text_path(txt, size, cx, baseline, tracking=0, fill=NAVY, anchor="middle"):
    s = size / UPM
    w = text_width(txt, size, tracking)
    x = cx - w / 2 if anchor == "middle" else cx
    pen = SVGPathPen(GS)
    for c in txt:
        g = CMAP[ord(c)]
        GS[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        x += GS[g].width * s + tracking
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'

def chimney(cx, top, cap_w=156, stack_w=128, rows=6, row_h=32):
    o = []
    cl, sl = cx - cap_w / 2, cx - stack_w / 2
    o.append(f'<rect x="{cl}" y="{top}" width="{cap_w}" height="28" rx="2" fill="{BRICK}"/>')
    o.append(f'<rect x="{cx-(cap_w-16)/2}" y="{top+28}" width="{cap_w-16}" height="10" fill="{BRICK_DK}"/>')
    y0, gap = top + 38, 6
    for i in range(rows):
        y = y0 + i * row_h + gap
        h = row_h - gap
        if i % 2 == 0:
            q = (stack_w - 2 * gap) / 4.4
            segs = [(0, q), (q + gap, stack_w - 2 * q - 2 * gap), (stack_w - q, q)]
        else:
            half = (stack_w - gap) / 2
            segs = [(0, half), (half + gap, half)]
        for sx, sw in segs:
            o.append(f'<rect x="{sl+sx:.1f}" y="{y}" width="{sw:.1f}" height="{h}" rx="1.5" fill="{BRICK}"/>')
            o.append(f'<rect x="{sl+sx:.1f}" y="{y+h-5}" width="{sw:.1f}" height="5" fill="{MORTAR_SH}"/>')
    return "".join(o), y0 + rows * row_h

ROSE = (  # centered on 0,0, ~76 wide
    f'<path fill="{GOLD}" d="M-36 2C-42-22-22-42 0-38C22-42 42-22 36 2C38 24 20 38 0 36C-20 38-38 24-36 2Z"/>'
    f'<g fill="none" stroke="{CREAM}" stroke-width="3" stroke-linecap="round">'
    '<path d="M-3-4C5-10 13-2 6 6C-2 13-15 6-12-6C-9-19 9-23 19-12"/>'
    '<path d="M-30 8C-20 22 20 22 30 8"/>'
    '<path d="M-28-14C-18-28-4-30 4-28"/>'
    '<path d="M24-20C30-12 30-2 26 6"/></g>')
LEAF = (f'<path fill="{GOLD}" d="M0 0C12-12 34-13 50 0C34 13 12 12 0 0Z"/>'
        f'<path d="M4 0H42" stroke="{CREAM}" stroke-width="2.5" stroke-linecap="round"/>')

def rose_side(base_x, base_y, flip=False):
    # stem from chimney base out to the bloom, with three leaves
    g = (f'<path d="M{base_x} {base_y}C-24 {base_y-30} -52 {base_y-70} -60 {base_y-150}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
         f'<g transform="translate(-24 {base_y-28}) rotate(200)">{LEAF}</g>'
         f'<g transform="translate(-44 {base_y-80}) rotate(215)">{LEAF}</g>'
         f'<g transform="translate(-58 {base_y-118}) rotate(160) scale(.8)">{LEAF}</g>'
         f'<g transform="translate(-66 {base_y-170})">{ROSE}</g>')
    return g

def emblem(cx, top):
    """Chimney flanked by roses. Returns svg and bottom y."""
    ch, bottom = chimney(cx, top)
    left = f'<g transform="translate({cx-66} 0)">{rose_side(0, bottom-2)}</g>'
    right = f'<g transform="translate({cx+66} 0) scale(-1 1)">{rose_side(0, bottom-2)}</g>'
    return left + right + ch, bottom

SHIELD = "M40 105C150 100 270 80 300 15C330 80 450 100 560 105L560 470C560 600 420 690 300 750C180 690 40 600 40 470Z"

def shield_x_at(y):
    # right edge of the shield at height y (straight side, then bezier to the tip)
    if y <= 470: return 560
    p0, p1, p2, p3 = (560, 470), (560, 600), (420, 690), (300, 750)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        t = (lo + hi) / 2
        by = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        lo, hi = (t, hi) if by < y else (lo, t)
    t = lo
    return (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{title}</title>{body}</svg>\n')

def primary(llc=True):
    cx = 300
    em, bottom = emblem(cx, 156)
    o = [f'<path d="{SHIELD}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>', em]
    ry = bottom + 18
    o.append(f'<rect x="88" y="{ry}" width="424" height="4" fill="{RULE}"/>')
    b1 = ry + 22 + 80                      # ROSAS, cap height ~80
    o.append(text_path("ROSAS", 121, cx, b1, tracking=4))
    b2 = b1 + 20 + 54                      # CHIMNEY, cap height ~54
    o.append(text_path("CHIMNEY", 82, cx, b2, tracking=2))
    sub = "SERVICES LLC" if llc else "SERVICES"
    b3 = b2 + 18 + 20
    o.append(text_path(sub, 30, cx, b3, tracking=3, fill=GOLD_TXT))
    tw = text_width(sub, 30, 3)
    ly = b3 - 12
    xin = shield_x_at(ly) - 24
    print("  sub rule width:", round(xin - (cx + tw / 2 + 16)), "shield edge at", round(shield_x_at(ly)))
    o.append(f'<rect x="{600-xin:.1f}" y="{ly}" width="{(cx-tw/2-16)-(600-xin):.1f}" height="4" fill="{RULE}"/>')
    o.append(f'<rect x="{cx+tw/2+16:.1f}" y="{ly}" width="{xin-(cx+tw/2+16):.1f}" height="4" fill="{RULE}"/>')
    return svg(600, 770, "".join(o), "Rosas Chimney Services")

def icon():
    em, bottom = emblem(300, 190)
    o = [f'<path d="{SHIELD}" fill="#FFFFFF" stroke="{NAVY}" stroke-width="12" stroke-linejoin="round"/>',
         f'<g transform="translate(300 400) scale(1.45) translate(-300 -297)">{em}</g>']
    return svg(600, 770, "".join(o), "Rosas Chimney Services icon")

def horizontal():
    em, bottom = emblem(185, 40)
    o = [f'<g>{em}</g>']
    x0 = 395
    o.append(text_path("ROSAS", 150, x0, 165, tracking=5, anchor="start"))
    o.append(f'<rect x="{x0+4}" y="190" width="{text_width("ROSAS",150,5)-6:.1f}" height="5" fill="{RULE}"/>')
    o.append(text_path("CHIMNEY SERVICES", 47, x0 + 4, 252, tracking=5.2, fill=GOLD_TXT, anchor="start"))
    w = x0 + max(text_width("ROSAS", 150, 5), text_width("CHIMNEY SERVICES", 47, 5.2)) + 20
    return svg(int(w), 300, "".join(o), "Rosas Chimney Services")

os.makedirs(OUT, exist_ok=True)
files = {"rosas-logo-primary.svg": primary(True), "rosas-logo-primary-no-llc.svg": primary(False),
         "rosas-logo-horizontal.svg": horizontal(), "rosas-logo-icon.svg": icon()}
for n, c in files.items():
    open(os.path.join(OUT, n), "w").write(c)
    print(n, len(c))
