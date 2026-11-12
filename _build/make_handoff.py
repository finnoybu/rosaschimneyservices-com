"""SITE DESIGNER ONLY. Builds dist/Rosas-Website-Handoff.zip for Rosas Chimney Services:
the live-ready website, the logo set and the owners' guides. Nothing from the github.io
demo (publish script, .nojekyll, README.md, build tools) goes in it.
Run from _build/:  python3 make_handoff.py   (run build.py first)"""
import os, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "dist", "Rosas-Website-Handoff.zip")
PREFIX = "Rosas-Website-Handoff/"
SITE_DIRS = ["assets", "es", "service-areas"]
SITE_FILES = ["favicon.ico", "robots.txt", "sitemap.xml"]
SKIP = {"assets/img/chimney-detail.svg"}            # no longer used by any page
LOGO_SKIP = {"original-logo.png"}                    # the owners already have their original artwork

def site_files():
    for f in sorted(os.listdir(ROOT)):
        if f.endswith(".html") or f in SITE_FILES:
            yield f
    for d in SITE_DIRS:
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(base, f), ROOT).replace(os.sep, "/")
                if rel not in SKIP:
                    yield rel

os.makedirs(os.path.dirname(OUT), exist_ok=True)
n = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in site_files():
        z.write(os.path.join(ROOT, rel), PREFIX + "website/" + rel); n += 1
    for f in sorted(os.listdir(os.path.join(ROOT, "brand"))):
        if f not in LOGO_SKIP:
            z.write(os.path.join(ROOT, "brand", f), PREFIX + "logos/" + f); n += 1
    hand = os.path.join(HERE, "handoff")
    for base, _, files in os.walk(hand):
        for f in files:
            full = os.path.join(base, f)
            z.write(full, PREFIX + os.path.relpath(full, hand).replace(os.sep, "/")); n += 1
print("wrote", OUT, "with", n, "files")
