"""Builds the Spanish (/es/) mirror from the English page HTML."""
import re, json, html as H
from es_strings_1 import ES1
from es_strings_2 import ES2, KEEP, CALL
from areas import COUNTIES, TOWNS

DICT = {**ES1, **ES2}
TOWN_NAMES = {t["name"] for t in TOWNS}
X = r"([A-Z][A-Za-z]+)"          # county stem, e.g. Warren
P = r"([A-Z][A-Za-z .]+?)"       # a town or "X County"

def cty(x): return f"Condado de {x}"
def loc(p): return "el " + cty(p[:-7]) if p.endswith(" County") else p
def y_list(s):
    parts = [a.strip() for a in s.split(",")]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " y " + parts[-1]

RULES = [
 (rf"A local chimney company for {P} homeowners", lambda m: f"Una empresa de chimeneas local para los propietarios de {m[1]}"),
 (rf"All of {X} County", lambda m: f"Todo el {cty(m[1])}"),
 (rf"CSIA Certified, family-owned chimney care for {P} and the rest of {X} County\.", lambda m: f"Cuidado de chimeneas de una empresa familiar certificada por la CSIA para {m[1]} y el resto del {cty(m[2])}."),
 (rf"Chimney Services in {X} County, VA", lambda m: f"Servicios de chimenea en el {cty(m[1])}, VA"),
 (rf"Chimney Sweep & Chimney Services in {P}, VA", lambda m: f"Deshollinador y servicios de chimenea en {m[1]}, VA"),
 (rf"Chimney Sweep in {P}, VA \| Rosas Chimney Services", lambda m: f"Deshollinador en {loc(m[1])}, VA | Rosas Chimney Services"),
 (rf"Chimney care across {X} County", lambda m: f"Cuidado de chimeneas en todo el {cty(m[1])}"),
 (rf"Chimney services in {P}, VA", lambda m: f"Servicios de chimenea en {loc(m[1])}, VA"),
 (rf"Chimney services we provide in {P}", lambda m: f"Servicios de chimenea que ofrecemos en {m[1]}"),
 (rf"Chimney sweep and chimney services in {X} County, VA, including (.+)\. CSIA Certified, family-owned and insured\. Call or text \(540\) 431-9629\.",
  lambda m: f"Deshollinador y servicios de chimenea en el {cty(m[1])}, VA, incluidos {y_list(m[2])}. Certificados por la CSIA, empresa familiar y asegurada. {CALL}"),
 (rf"Chimney sweep in {P}, VA\. Family-owned, CSIA Certified and insured chimney cleaning, inspections, repairs, liners, caps and stove installs in {X} County\. Call or text \(540\) 431-9629\.",
  lambda m: f"Deshollinador en {m[1]}, VA. Limpieza, inspecciones, reparaciones, revestimientos, sombreretes e instalación de estufas en el {cty(m[2])}, con una empresa familiar, certificada por la CSIA y asegurada. {CALL}"),
 (rf"Communities in {X} County", lambda m: f"Comunidades del {cty(m[1])}"),
 (rf"Ready for a safer chimney in {P}\?", lambda m: f"¿Listo para una chimenea más segura en {m[1]}?"),
 (rf"Serving homeowners across {X} County", lambda m: f"Al servicio de los propietarios de todo el {cty(m[1])}"),
 (rf"Southern {X} County", lambda m: f"Sur del {cty(m[1])}"),
 (rf"View {X} County", lambda m: f"Ver el {cty(m[1])}"),
 (rf"Why {P} homeowners choose Rosas", lambda m: f"Por qué los propietarios de {m[1]} eligen a Rosas"),
 (rf"{X} County, VA", lambda m: f"{cty(m[1])}, VA"),
 (rf"{X} County", lambda m: cty(m[1])),
]
RULES = [(re.compile(r + r"\Z"), f) for r, f in RULES]
MISSES = set()

def translate(s):
    if s in DICT: return DICT[s]
    if s in KEEP or s in TOWN_NAMES: return s
    if re.fullmatch(r"[A-Z][A-Za-z .]+, VA", s) and s[:-4] in TOWN_NAMES: return s
    for rx, f in RULES:
        m = rx.match(s)
        if m: return f(m)
    MISSES.add(s); return s

def esc_text(s): return H.escape(s, quote=False).replace("\xa0", "&nbsp;")

def tx_text(seg):
    raw = H.unescape(seg)
    if not re.search(r"[A-Za-z]{2}", raw): return seg
    lead = re.match(r"[\s\xa0/]*", raw).group()
    trail = re.search(r"[\s\xa0]*\Z", raw).group()
    core = raw[len(lead):len(raw) - len(trail)]
    norm = re.sub(r"\s+", " ", core)
    if not re.search(r"[A-Za-z]{2}", norm) or re.fullmatch(r"[\w.+-]+@[\w.-]+|https?://\S+", norm): return seg
    return esc_text(lead) + esc_text(translate(norm)) + esc_text(trail)

META = {"description", "og:title", "og:description", "og:image:alt"}
def tx_tag(tag):
    def attr(m):
        v = H.unescape(m[2]).strip()
        if not re.search(r"[A-Za-z]{2}", v): return m[0]
        t = H.escape(translate(re.sub(r"\s+", " ", v)))
        return m[1] + '="' + t + '"'
    tag = re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"', attr, tag)
    if tag.startswith("<meta") and (re.search(r'(name|property)="([^"]+)"', tag) or [0, 0, ""])[2] in META:
        tag = re.sub(r'\b(content)="([^"]*)"', attr, tag)
    return tag

def tx_ld(block, site):
    m = re.match(r"(<script[^>]*>)(.*)(</script>)\Z", block, re.S)
    data = json.loads(m[2])
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and k in ("name", "text", "description", "serviceType"): o[k] = translate(v.strip())
                elif isinstance(v, str) and k in ("item", "url") and v.startswith(site + "/") and "/assets/" not in v:
                    o[k] = site + "/es/" + v[len(site) + 1:]
                else: walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    return m[1] + json.dumps(data, ensure_ascii=False) + m[3]

TOKEN = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)", re.S)
def to_spanish(page_html, site):
    out = []
    for i, part in enumerate(TOKEN.split(page_html)):
        if i % 2 == 0: out.append(tx_text(part) if part else part)
        elif part.startswith("<script") and "ld+json" in part[:60]: out.append(tx_ld(part, site))
        elif part.startswith(("<script", "<style", "<!--")): out.append(part)
        else: out.append(tx_tag(part))
    h = "".join(out)
    h = h.replace('<html lang="en">', '<html lang="es">', 1)
    # internal page links point at the Spanish pages; assets stay shared
    def link(m):
        url = m[2]; path = re.split(r"[?#]", url)[0]
        return f'{m[1]}="es/{url}"' if path.endswith(".html") else m[0]
    h = re.sub(r'(href)="(?!https?:|tel:|sms:|mailto:|#|data:|/)([^"]*)"', link, h)
    return h
