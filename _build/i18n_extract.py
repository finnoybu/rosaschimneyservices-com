"""Collect every translatable string from the built English pages."""
import os, glob, json, re
from html.parser import HTMLParser
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ATTRS = {"alt", "aria-label", "placeholder", "title", "content"}
META_NAMES = {"description", "og:title", "og:description"}
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.out = []; s.skip = 0; s.ld = False; s.buf = ""
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("style",) or (t == "script" and a.get("type") != "application/ld+json"): s.skip += 1
        if t == "script" and a.get("type") == "application/ld+json": s.ld = True; s.buf = ""
        for k, v in a.items():
            if not v or k not in ATTRS: continue
            if k == "content" and not (a.get("name") in META_NAMES or a.get("property") in META_NAMES): continue
            s.out.append(v.strip())
    def handle_endtag(s, t):
        if t == "style" or (t == "script" and not s.ld): s.skip = max(0, s.skip - 1)
        if t == "script" and s.ld:
            s.ld = False
            def walk(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in ("name", "text", "description", "serviceType") and isinstance(v, str): s.out.append(v.strip())
                        else: walk(v)
                elif isinstance(o, list):
                    for v in o: walk(v)
            walk(json.loads(s.buf))
    def handle_data(s, d):
        if s.ld: s.buf += d; return
        if s.skip: return
        if d.strip(): s.out.append(re.sub(r"\s+", " ", d.strip()))
seen = {}
pages = [f for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
         if not any(x in f for x in ("/_build/", "/brand/", "/dist/", "/es/"))]
for f in pages:
    p = P(); p.feed(open(f, encoding="utf-8").read())
    for t in p.out: seen[t] = seen.get(t, 0) + 1
keep = lambda t: re.search(r"[A-Za-z]{2}", t) and not re.fullmatch(r"[\w.+-]+@[\w.-]+|https?://\S+|\(?\d[\d) .-]+", t)
strings = sorted((t for t in seen if keep(t)), key=lambda t: (-seen[t], t))
json.dump(strings, open(os.path.join(os.path.dirname(__file__), "i18n_strings.json"), "w"), ensure_ascii=False, indent=0)
print(len(pages), "pages,", len(strings), "unique strings,", sum(len(t.split()) for t in strings), "words")
