"""Traces the chimney-and-roses emblem from the original raster logo
(brand/original-logo.png, 6000x6000) into SVG paths. Writes _build/emblem_traced.json."""
import cv2, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
im = cv2.imread(os.path.join(HERE, "..", "brand", "original-logo.png"))
X0, X1, Y0, Y1 = 1400, 4600, 1220, 3160          # emblem region (above the first rule)
roi = im[Y0:Y1, X0:X1].astype(np.int32)
pal = [("white", (255,255,255)), ("brick", (35,60,169)), ("dark", (37,28,66)),
       ("dark", (76,62,46)), ("dark", (0,0,0)), ("gold", (73,149,213))]
P = np.array([c for _, c in pal], np.int32)
lab = np.zeros(roi.shape[:2], np.int32)
best = np.full(roi.shape[:2], 1e18)
for i, (_, c) in enumerate(pal):            # nearest palette colour, row-chunked for memory
    dist = ((roi - np.array(c)) ** 2).sum(-1)
    m = dist < best; best[m] = dist[m]; lab[m] = i
def smooth_path(pts, corner_deg=100):
    """Closed polygon -> cubic Bezier path (Catmull-Rom), keeping sharp corners sharp."""
    n = len(pts)
    P = pts.astype(float)
    def ang(i):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        v1, v2 = a - b, c - b
        cosv = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
        return np.degrees(np.arccos(np.clip(cosv, -1, 1)))
    corner = [ang(i) < corner_deg for i in range(n)]
    out = [f"M{P[0][0]:.0f} {P[0][1]:.0f}"]
    for i in range(n):
        p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % n], P[(i + 2) % n]
        if corner[i]: p0 = p1
        if corner[(i + 1) % n]: p3 = p2
        c1 = p1 + (p2 - p0) / 6.0
        c2 = p2 - (p3 - p1) / 6.0
        out.append(f"C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {p2[0]:.0f} {p2[1]:.0f}")
    return "".join(out) + "Z"

def mask_of(name):
    idx = [i for i, (n, _) in enumerate(pal) if n == name]
    return np.isin(lab, idx).astype(np.uint8) * 255

brickdark = cv2.bitwise_or(mask_of("brick"), mask_of("dark"))
layers = {}
for name in ("gold", "brick", "dark"):
    mask = mask_of(name)
    if name == "gold":
        # keep only pixels that are genuinely gold, so the orange anti-aliasing
        # between brick and white is not mistaken for gold
        gd = ((roi - np.array((73, 149, 213))) ** 2).sum(-1)
        mask = ((gd < 55 ** 2) * 255).astype(np.uint8)
        mask[cv2.dilate(brickdark, np.ones((5, 5), np.uint8)) > 0] = 0
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
        # smooth the slightly jagged source edges before tracing
        mask = cv2.GaussianBlur(mask, (0, 0), 3.5)
        mask = (mask > 127).astype(np.uint8) * 255
    else:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.medianBlur(mask, 5)
    cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d = []
    for c in cs:
        if abs(cv2.contourArea(c)) < 150: continue
        a = cv2.approxPolyDP(c, 1.4 if name == "gold" else 2.0, True).reshape(-1, 2)
        if len(a) < 3: continue
        d.append(smooth_path(a) if name == "gold" else "M" + " ".join(f"{x} {y}" for x, y in a) + "Z")
    layers[name] = " ".join(d)
    print(name, "contours", len(d), "chars", len(layers[name]))
json.dump({"w": X1 - X0, "h": Y1 - Y0, "chimney_cx": 1600, "cap_w": 1440, "layers": layers},
          open(os.path.join(HERE, "emblem_traced.json"), "w"))
