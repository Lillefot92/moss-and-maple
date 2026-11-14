"""Cozy moments with a woman seen from behind, drawn realistically, in detailed nature scenes."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import (real_leaf, garden_rose, wild_rose, compound_leaf, spruce_twig, pine_cone, oak_leaf,
                       acorn_real, FINE, frac)

RG = []


def rpage(pid, title, season):
    def deco(fn):
        RG.append((pid, title, season, fn))
        return fn
    return deco


def A(pts, cx, cy, u):
    return [(cx + x * u, cy + y * u) for x, y in pts]


def mirror_pts(right):
    return right + [(-x, y) for x, y in reversed(right[1:-1])]


# ------------------------------------------------------------------ hair
def strands(pg, outline_abs, starts, ends, rng, waves=0.06, u=1.0, n_pts=24, lw=FINE):
    pg.clip_begin(d_smooth(outline_abs))
    for (x0, y0), (x1, y1) in zip(starts, ends):
        ph = rng.uniform(0, 6.28)
        fq = rng.uniform(2.2, 3.4)
        pts = []
        for i in range(n_pts + 1):
            t = i / n_pts
            e = t * t * (3 - 2 * t)
            x = x0 + (x1 - x0) * e + waves * u * math.sin(ph + t * math.pi * fq) * t
            y = y0 + (y1 - y0) * t
            pts.append((x, y))
        pg.line(pts, lw=lw, smooth=True)
    pg.clip_end()


def long_hair_back(pg, cx, ty, u, L, rng, locks=7, width=0.82):
    """Long wavy hair from behind. u = head width unit; L = length in units."""
    right = [(0, 0), (0.3, 0.03), (0.5, 0.18), (0.57, 0.45), (0.58, 0.8), (0.64, 1.15), (0.74, 1.55), (width, 2.0)]
    y_shoulder = 2.0
    for k in range(1, 5):
        t = k / 4
        right.append((width + 0.06 * math.sin(t * 5), y_shoulder + (L - 0.3 - y_shoulder) * t))
    bottom = []
    for i in range(locks):
        xa = width - 2 * width * i / locks
        xb = width - 2 * width * (i + 1) / locks
        tipx = (xa + xb) / 2 + rng.uniform(-0.04, 0.04)
        bottom += [(xa, L - 0.28 + rng.uniform(-0.05, 0.05)), (tipx + 0.03, L - 0.05), (tipx, L + rng.uniform(-0.02, 0.1))]
    left = [(-width - 0.06 * math.sin(t * 5), y_shoulder + (L - 0.3 - y_shoulder) * t) for t in [k / 4 for k in range(4, 0, -1)]]
    left += [(-width, 2.0), (-0.73, 1.55), (-0.63, 1.15), (-0.58, 0.8), (-0.57, 0.45), (-0.5, 0.18), (-0.3, 0.03)]
    out = A(right + bottom + left, cx, ty, u)
    pg.shape(out, smooth=True)
    tips = [p for i, p in enumerate(bottom) if i % 3 == 2]
    starts, ends = [], []
    n = 30
    for k in range(n):
        f = k / (n - 1)
        a = math.pi * (0.08 + 0.84 * f)
        # start on the crown arc, so the hair falls around the head
        sx, sy = 0.5 * math.cos(math.pi - a), 0.04 + 0.5 * math.sin(a) * 0.45
        tip = tips[len(tips) - 1 - min(int(f * len(tips)), len(tips) - 1)]
        starts.append((cx + sx * u * 0.9, ty + sy * u))
        ends.append((cx + (tip[0] + rng.uniform(-0.06, 0.06)) * u, ty + (tip[1] - rng.uniform(0.0, 0.25)) * u))
    strands(pg, out, starts, ends, rng, waves=0.09, u=u, lw=0.9)
    # clump separations: a few stronger flowing lines
    for k in range(locks - 1):
        f = (k + 1) / locks
        a = math.pi * (0.1 + 0.8 * f)
        sx = 0.5 * math.cos(math.pi - a)
        bx = -width + 2 * width * (k + 1) / locks
        pts = []
        for i in range(21):
            t = i / 20
            x = sx * 0.9 + (bx - sx * 0.9) * (t * t * (3 - 2 * t)) + 0.08 * math.sin(t * 7 + k) * t
            pts.append((cx + x * u, ty + (0.3 + (L - 0.4) * t) * u))
        pg.clip_begin(d_smooth(out))
        pg.line(pts, lw=TH, smooth=True)
        pg.clip_end()
    pg.shape(out, smooth=True, fill="none")
    return out


def bun_back(pg, cx, ty, u, rng):
    """Hair swept up into a loose bun, nape and a few tendrils showing."""
    head = [(0.5 * math.cos(t), 0.62 * math.sin(t) + 0.62) for t in [i * 2 * math.pi / 48 for i in range(48)]]
    nape = A([(-0.16, 1.0), (-0.17, 1.45), (0.17, 1.45), (0.16, 1.0)], cx, ty, u)
    pg.shape(nape)
    out = A(head, cx, ty, u)
    pg.shape(out, smooth=True)
    bc = (cx + 0.02 * u, ty + 0.12 * u)
    starts, ends = [], []
    for k in range(26):
        a = math.pi * (0.1 + 0.8 * k / 25)
        starts.append((cx - 0.5 * u * math.cos(a), ty + 0.62 * u + 0.62 * u * math.sin(a)))
        ends.append((bc[0] + rng.uniform(-0.06, 0.06) * u, bc[1] + 0.05 * u))
    strands(pg, out, starts, ends, rng, waves=0.025, u=u)
    pg.shape(out, smooth=True, fill="none")
    # the bun itself: a coil of hair
    pg.circle(bc[0], bc[1] - 0.05 * u, 0.3 * u)
    for k in range(5):
        ph = k * 1.25
        pts = []
        for i in range(30):
            t = i / 29
            r = 0.28 * u * (1 - 0.65 * t)
            a = ph + t * 3.6
            pts.append((bc[0] + r * math.cos(a), bc[1] - 0.05 * u + r * 0.85 * math.sin(a)))
        pg.line(pts, lw=FINE, smooth=True)
    # hair tie
    pg.ellipse(bc[0], bc[1] + 0.2 * u, 0.13 * u, 0.05 * u, lw=TH)
    # loose tendrils
    for sd in (-1, 1):
        x0 = cx + sd * 0.36 * u
        pg.line([(x0, ty + 1.02 * u), (x0 + sd * 0.04 * u, ty + 1.2 * u), (x0 - sd * 0.02 * u, ty + 1.36 * u), (x0 + sd * 0.03 * u, ty + 1.5 * u)], lw=FINE, smooth=True)
    return out


def braid_back(pg, cx, ty, u, L, rng):
    head = [(0.5 * math.cos(t), 0.6 * math.sin(t) + 0.6) for t in [i * 2 * math.pi / 48 for i in range(48)]]
    out = A(head, cx, ty, u)
    pg.shape(out, smooth=True)
    nape = (cx, ty + 1.12 * u)
    starts, ends = [], []
    for k in range(26):
        f = k / 25
        a = math.pi * (0.06 + 0.88 * f)
        starts.append((cx - 0.5 * u * math.cos(a), ty + 0.6 * u - 0.6 * u * math.sin(a)))
        ends.append((nape[0] + (f - 0.5) * 0.18 * u, nape[1]))
    strands(pg, out, starts, ends, rng, waves=0.03, u=u)
    pg.shape(out, smooth=True, fill="none")
    # braid: alternating plaits that taper down the back
    y = ty + 1.05 * u
    seg = 0.3 * u
    k = 0
    while y < ty + L * u:
        t = (y - ty - 1.05 * u) / ((L - 1.05) * u)
        w = (0.22 - 0.1 * t) * u
        sd = 1 if k % 2 == 0 else -1
        lobe = [(0, 0), (sd * w * 0.9, seg * 0.25), (sd * w * 0.7, seg * 0.85), (-sd * w * 0.25, seg * 1.15), (-sd * w * 0.3, seg * 0.6)]
        P = [(cx + x + 0.04 * u * math.sin(t * 3), y + yy) for x, yy in lobe]
        pg.shape(P, smooth=True)
        pg.line([(P[0][0] + sd * w * 0.15, y + seg * 0.2), (P[0][0] + sd * w * 0.45, y + seg * 0.7)], lw=FINE, smooth=False)
        y += seg * 0.72
        seg *= 0.985
        k += 1
    # tie and tuft
    by = y + 0.1 * u
    pg.ellipse(cx + 0.04 * u * math.sin(3), by, 0.09 * u, 0.04 * u, lw=TH)
    tuft = [(-0.08, 0), (-0.14, 0.2), (-0.06, 0.38), (0, 0.3), (0.06, 0.4), (0.13, 0.2), (0.08, 0)]
    T = A(tuft, cx + 0.04 * u * math.sin(3), by + 0.03 * u, u)
    pg.shape(T, smooth=True)
    for xx in (-0.05, 0.0, 0.05):
        pg.line(A([(xx, 0.03), (xx * 1.4, 0.3)], cx + 0.04 * u * math.sin(3), by + 0.03 * u, u), lw=FINE)


# -------------------------------------------------------------- textiles
def cable_knit(pg, clip_abs, x0, x1, y0, y1, col=46, row=26):
    pg.clip_begin(d_smooth(clip_abs))
    x = x0
    k = 0
    while x < x1:
        if k % 2 == 0:  # a twisted cable
            y = y0
            while y < y1:
                pg.line([(x - 9, y), (x + 9, y + row * 0.5), (x - 9, y + row)], lw=FINE, smooth=True)
                pg.line([(x + 9, y + 3), (x + 2, y + row * 0.35)], lw=FINE)
                pg.line([(x - 2, y + row * 0.65), (x - 9, y + row - 3)], lw=FINE)
                y += row
            pg.line([(x - 15, y0), (x - 15, y1)], lw=FINE)
            pg.line([(x + 15, y0), (x + 15, y1)], lw=FINE)
        else:  # seed stitch between cables
            y = y0
            while y < y1:
                for dx in (-8, 0, 8):
                    pg.line([(x + dx - 2, y), (x + dx, y + 3), (x + dx + 2, y)], lw=0.8)
                y += 9
        x += col / 2 + 7
        k += 1
    pg.clip_end()


def chunky_knit(pg, clip_abs, x0, x1, y0, y1, w=18, h=14, wave=0.0):
    pg.clip_begin(d_smooth(clip_abs))
    r = 0
    y = y0
    while y < y1:
        x = x0 + (w / 2 if r % 2 else 0)
        while x < x1:
            dy = wave * math.sin(x / 60)
            pg.shape([(x - w / 2, y + dy), (x - w * 0.1, y + h * 0.15 + dy), (x, y + h + dy), (x - w * 0.18, y + h * 0.95 + dy)], lw=FINE, smooth=True)
            pg.shape([(x + w / 2, y + dy), (x + w * 0.1, y + h * 0.15 + dy), (x, y + h + dy), (x + w * 0.18, y + h * 0.95 + dy)], lw=FINE, smooth=True)
            x += w
        y += h * 0.8
        r += 1
    pg.clip_end()


def wicker(pg, clip_abs, x0, x1, y0, y1, rows=10):
    pg.clip_begin(d_smooth(clip_abs))
    h = (y1 - y0) / rows
    for r in range(rows):
        y = y0 + r * h
        pg.line([(x0, y), (x1, y)], lw=FINE)
        x = x0 + (r % 2) * 9
        while x < x1:
            pg.line([(x, y + 2), (x + 9, y + h / 2), (x, y + h - 2)], lw=FINE, smooth=True)
            x += 18
    pg.clip_end()


# --------------------------------------------------------------- nature
def spruce_tree(pg, x, base, h, w, rng, snow=True, tiers=7):
    pg.shape([(x - w * 0.04, base), (x - w * 0.04, base - h * 0.1), (x + w * 0.04, base - h * 0.1), (x + w * 0.04, base)])
    for i in range(tiers):
        t = i / tiers
        top = base - h * (0.1 + 0.9 * (i + 1) / tiers) - h * 0.05
        bot = base - h * (0.08 + 0.9 * i / tiers)
        ww = w / 2 * (1 - t * 0.85)
        pts = [(x, top)]
        n = 9
        for k in range(n + 1):
            u = k / n
            px = x + ww * (1 - 2 * u)
            py = bot + (5 if k % 2 else -2) * (1 - t) + rng.uniform(-2, 2)
            if k == 0:
                pts.append((x + ww * 0.6, (top + bot) / 2 + 4))
            pts.append((px, py))
            if k == n:
                pts.append((x - ww * 0.6, (top + bot) / 2 + 4))
        pg.shape(pts, lw=TH)
        if snow:
            sw = ww * 0.75
            sy = bot - (bot - top) * 0.35
            pg.shape([(x - sw, sy + 3), (x - sw * 0.5, sy - 4), (x, sy - 2), (x + sw * 0.5, sy - 5), (x + sw, sy + 3), (x, sy + 6)], lw=FINE, smooth=True)


def frost(pg, x, y, ang, L, rng, depth=3):
    if depth == 0 or L < 4:
        return
    ex, ey = x + L * math.cos(math.radians(ang)), y + L * math.sin(math.radians(ang))
    pg.line([(x, y), (ex, ey)], lw=0.9)
    for k in range(1, 4):
        t = k / 4
        px, py = x + (ex - x) * t, y + (ey - y) * t
        for sd in (-1, 1):
            a2 = ang + sd * 55
            l2 = L * 0.35 * (1 - t * 0.5)
            pg.line([(px, py), (px + l2 * math.cos(math.radians(a2)), py + l2 * math.sin(math.radians(a2)))], lw=0.8)
    frost(pg, ex, ey, ang + rng.uniform(-25, 25), L * 0.6, rng, depth - 1)


def poppy(pg, x, y, R, rng, ang=0):
    for i in range(4):
        a = ang + i * 90 + 45 + rng.uniform(-8, 8)
        pts = []
        for k in range(30):
            v = -1 + 2 * k / 29
            aa = math.radians(a + v * 58)
            r = R * (0.95 - 0.12 * v * v + 0.07 * math.sin(v * 11 + i * 2))
            pts.append((x + r * math.cos(aa), y + r * math.sin(aa) * 0.8))
        pg.shape([(x, y)] + pts, smooth=True)
        for v in (-0.4, 0, 0.4):
            aa = math.radians(a + v * 40)
            pg.line([(x + R * 0.3 * math.cos(aa), y + R * 0.3 * math.sin(aa) * 0.8), (x + R * 0.75 * math.cos(aa + 0.05), y + R * 0.75 * math.sin(aa + 0.05) * 0.8)], lw=FINE, smooth=False)
    pg.circle(x, y, R * 0.28)
    pg.ellipse(x, y - R * 0.05, R * 0.17, R * 0.12, lw=TH)
    for k in range(8):
        a = k * math.pi / 4
        pg.line([(x, y - R * 0.05), (x + R * 0.15 * math.cos(a), y - R * 0.05 + R * 0.1 * math.sin(a))], lw=FINE)
    for k in range(18):
        a = k * 2 * math.pi / 18
        pg.circle(x + R * 0.33 * math.cos(a), y + R * 0.3 * math.sin(a), R * 0.025, lw=0.8)


def cornflower(pg, x, y, R, rng):
    for i in range(9):
        a = math.radians(i * 40 + rng.uniform(-6, 6))
        L = R * rng.uniform(0.8, 1.0)
        ca, sa = math.cos(a), math.sin(a)
        base = (x + R * 0.18 * ca, y + R * 0.18 * sa)
        tip = (x + L * ca, y + L * sa)
        nx, ny = -sa, ca
        w = R * 0.22
        teeth = [(tip[0] + nx * w + ca * 2, tip[1] + ny * w + sa * 2), (tip[0] + nx * w * 0.4 + ca * 6, tip[1] + ny * w * 0.4 + sa * 6), (tip[0] + ca * 2, tip[1] + sa * 2),
                 (tip[0] - nx * w * 0.4 + ca * 6, tip[1] - ny * w * 0.4 + sa * 6), (tip[0] - nx * w + ca * 2, tip[1] - ny * w + sa * 2)]
        pg.shape([base] + teeth, lw=FINE)
    pg.circle(x, y, R * 0.22)
    for k in range(6):
        a = k * math.pi / 3
        pg.line([(x, y), (x + R * 0.18 * math.cos(a), y + R * 0.18 * math.sin(a))], lw=0.8)


def chamomile(pg, x, y, R, rng, tilt=0.8):
    n = 16
    for i in range(n):
        a = math.radians(i * 360 / n + rng.uniform(-5, 5))
        ln = R * rng.uniform(0.85, 1.0)
        out = leaf_geom(ln * 0.75, R * 0.14, "round", n=10)
        P = [(x + px, y + py * tilt) for px, py in tf(out, 0, 0, math.degrees(a) + 90, 1)]
        P = [(px + (R * 0.28) * math.cos(a), py + (R * 0.28) * math.sin(a) * tilt) for px, py in P]
        pg.shape(P, lw=FINE)
    pg.ellipse(x, y - R * 0.05, R * 0.3, R * 0.26)
    for k in range(10):
        a = k * 2 * math.pi / 10
        pg.circle(x + R * 0.15 * math.cos(a), y - R * 0.05 + R * 0.12 * math.sin(a), R * 0.03, lw=0.8)


def grass_head(pg, x, y, h, lean, rng):
    stem = [(x, y), (x + lean * 0.3, y - h * 0.5), (x + lean, y - h)]
    pg.line(stem, lw=TH, smooth=True)
    tx, ty = x + lean, y - h
    for k in range(7):
        t = k / 7
        px, py = tx - lean * 0.05 * t, ty + h * 0.25 * t
        for sd in (-1, 1):
            g = leaf_geom(10 - 4 * t, 2.6, "lance", n=8)
            pg.shape(tf(g, px, py, sd * 30 + lean * 0.1), lw=0.8)


def wheat(pg, x, y, h, lean):
    pg.line([(x, y), (x + lean * 0.3, y - h * 0.5), (x + lean, y - h)], lw=TH, smooth=True)
    tx, ty = x + lean, y - h
    for k in range(9):
        t = k / 9
        px, py = tx - lean * 0.08 * t, ty + 55 * t
        for sd in (-1, 1):
            g = leaf_geom(11, 4, "round", n=8)
            pg.shape(tf(g, px + sd * 2, py, sd * 22 + lean * 0.15), lw=0.9)
            pg.line(tf([(0, -11), (0, -24)], px + sd * 2, py, sd * 22 + lean * 0.15), lw=0.7)


def cumulus(pg, x, y, w, rng):
    circs = []
    for i in range(7):
        t = i / 6
        cx = x + (t - 0.5) * w * 0.85
        b = math.sin(t * math.pi)
        circs.append((cx, y - b * w * 0.16 + rng.uniform(-3, 3), w * (0.1 + 0.12 * b)))
    circs += [(x - w * 0.2, y + w * 0.04, w * 0.14), (x + w * 0.18, y + w * 0.05, w * 0.13)]
    pg.union_circles(circs, lw=TH)
    for cx, cy, r in circs[2:5]:
        pg.line([(cx - r * 0.6, cy + r * 0.3), (cx, cy + r * 0.45), (cx + r * 0.6, cy + r * 0.3)], lw=0.8, smooth=True)


def birch(pg, x, top, bot, w, rng):
    pts = [(x - w / 2, bot), (x - w / 2 + 3, (top + bot) / 2), (x - w / 2 + 6, top), (x + w / 2 - 6, top), (x + w / 2 - 3, (top + bot) / 2), (x + w / 2, bot)]
    pg.shape(pts)
    y = top + 10
    while y < bot - 10:
        side = rng.choice((-1, 1))
        ln = rng.uniform(w * 0.25, w * 0.6)
        x0 = x + side * (w / 2 - 2)
        pg.shape([(x0, y), (x0 - side * ln, y + 2), (x0 - side * ln * 0.8, y + 6), (x0, y + 5)], lw=FINE)
        y += rng.uniform(16, 34)


def mushroom_real(pg, x, y, w, h, rng):
    stem = [(x - w * 0.12, y), (x - w * 0.1, y - h * 0.6), (x - w * 0.08, y - h * 0.85), (x + w * 0.08, y - h * 0.85), (x + w * 0.1, y - h * 0.6), (x + w * 0.13, y)]
    pg.shape(stem, smooth=True)
    for k in range(3):
        pg.line([(x - w * 0.06 + k * w * 0.05, y - h * 0.1), (x - w * 0.05 + k * w * 0.05, y - h * 0.75)], lw=0.8)
    cap = []
    for i in range(25):
        t = math.pi * i / 24
        cap.append((x - math.cos(t) * w / 2, y - h * 0.82 - math.sin(t) ** 0.9 * h * 0.45))
    cap += [(x + w * 0.45, y - h * 0.8), (x, y - h * 0.76), (x - w * 0.45, y - h * 0.8)]
    pg.shape(cap, smooth=True)
    for k in range(-4, 5):
        pg.line([(x + k * w * 0.1, y - h * 0.8), (x + k * w * 0.07, y - h * 0.86 - h * 0.25 * (1 - abs(k) / 5))], lw=0.8, smooth=False)


def cat_back(pg, x, y, s, rng):
    """A cat sitting, seen from behind, looking out."""
    T = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    tail = sample_smooth([(0.3, 0.0), (0.75, -0.05), (0.85, -0.25), (0.7, -0.38)], 8)
    pg.union_strokes([(T(tail), 0.16 * s)], lw=TH)
    body = [(0, -1.25), (0.3, -1.1), (0.45, -0.7), (0.52, -0.25), (0.45, 0.0), (0, 0.04), (-0.45, 0.0), (-0.52, -0.25), (-0.45, -0.7), (-0.3, -1.1)]
    pg.shape(T(body), smooth=True)
    head = [(0.32 * math.cos(t), -1.38 + 0.27 * math.sin(t)) for t in [i * 2 * math.pi / 30 for i in range(30)]]
    for sd in (-1, 1):
        pg.shape(T([(sd * 0.12, -1.58), (sd * 0.27, -1.78), (sd * 0.3, -1.45)]), lw=TH)
    pg.shape(T(head), smooth=True)
    for k in range(10):
        a = rng.uniform(-1, 1)
        px, py = a * 0.35, rng.uniform(-1.05, -0.15)
        pg.line(T([(px, py), (px + 0.02, py + 0.08)]), lw=0.8)
    pg.line(T([(0, -1.12), (0, -0.4)]), lw=0.8)


# ================================================================= pages
@rpage("rg-winter-window", "Frost on the Window", "winter")
def r_winter(pg):
    rng = random.Random(901)
    # wall with wainscot
    pg.shape([(0, 600), (600, 600), (600, 800), (0, 800)])
    for x in range(20, 600, 70):
        pg.shape([(x + 8, 630), (x + 62, 630), (x + 62, 780), (x + 8, 780)], lw=TH)
    # window
    X0, X1, Y0, Y1 = 70, 530, 40, 540
    pg.shape([(X0 - 18, Y0 - 18), (X1 + 18, Y0 - 18), (X1 + 18, Y1 + 10), (X0 - 18, Y1 + 10)])
    pg.shape([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
    pg.clip_begin(d_poly([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]))
    pg.circle(420, 120, 30, lw=TH)
    for _ in range(45):
        pg.circle(rng.uniform(X0, X1), rng.uniform(Y0, 380), rng.uniform(1.5, 3.5), lw=0.8)
    top = hill(pg, 400, 14, 0.4, 0.8, lw=TH)
    for (x, h, w) in [(90, 200, 90), (150, 260, 110), (230, 180, 80), (360, 230, 100), (440, 280, 120), (515, 210, 90)]:
        spruce_tree(pg, x, 470, h, w, rng)
    hill(pg, 465, 8, 1.4, 0.9, lw=TH)
    for (x, y, a) in [(X0, Y0, 45), (X1, Y0, 135), (X0, Y0 + 260, -30), (X1, Y0 + 260, 210)]:
        for k in range(4):
            frost(pg, x, y, a + k * 14 - 21, 48 + rng.uniform(-8, 12), rng, depth=3)
    pg.clip_end()
    for x in (X0 + (X1 - X0) / 3, X0 + 2 * (X1 - X0) / 3):
        pg.shape([(x - 5, Y0), (x + 5, Y0), (x + 5, Y1), (x - 5, Y1)])
    pg.shape([(X0, 290 - 5), (X1, 290 - 5), (X1, 290 + 5), (X0, 290 + 5)])
    # sill
    pg.shape([(30, 540), (570, 540), (585, 566), (15, 566)])
    pg.shape([(15, 566), (585, 566), (585, 600), (15, 600)])
    # eucalyptus sprigs in a stoneware jug on the left
    jx, jy = 120, 540
    for (ang, L) in [(-30, 150), (-8, 180), (14, 160), (34, 130)]:
        stem = [(jx, jy - 60), tf([(0, -L * 0.5)], jx, jy - 60, ang)[0], tf([(0, -L)], jx, jy - 60, ang + ang * 0.2)[0]]
        sp = sample_smooth(stem, 10)
        pg.line(sp, lw=TH, smooth=True)
        for i in range(5, len(sp), 6):
            x, y = sp[i]
            r = 11 - 5 * i / len(sp)
            for sd in (-1, 1):
                ox, oy = x + sd * r * 0.9, y
                pg.ellipse(ox, oy, r, r * 0.85, lw=TH)
                pg.line([(x, y), (ox + sd * r * 0.4, oy - r * 0.1)], lw=0.8)
    jug = [(jx - 26, jy), (jx - 34, jy - 30), (jx - 22, jy - 58), (jx - 16, jy - 72), (jx + 16, jy - 72), (jx + 22, jy - 58), (jx + 34, jy - 30), (jx + 26, jy)]
    pg.shape(jug, smooth=True)
    pg.line([(jx - 30, jy - 36), (jx + 30, jy - 36)], lw=0.8)
    pg.line([(jx - 31, jy - 30), (jx + 31, jy - 30)], lw=0.8)
    # cocoa mug on the sill
    mx, my = 470, 515
    pg.union_strokes([(sample_smooth([(mx + 22, my - 18), (mx + 40, my - 14), (mx + 40, my + 8), (mx + 22, my + 12)], 6), 7)], lw=TH)
    pg.shape([(mx - 26, my - 30), (mx + 26, my - 30), (mx + 24, my + 24), (mx - 24, my + 24)])
    pg.ellipse(mx, my - 30, 26, 7)
    for dx in (-10, 4, 16):
        pg.line([(mx + dx, my - 40), (mx + dx - 6, my - 56), (mx + dx + 4, my - 70), (mx + dx - 3, my - 86)], lw=TH, smooth=True)
    # the cat, looking out
    cat_back(pg, 530, 540, 62, rng)
    # her: bun hair, shoulders wrapped in a cable-knit blanket
    cx = 290
    bun_back(pg, cx, 300, 92, rng)
    blanket = [(cx, 420), (cx + 70, 425), (cx + 130, 450), (cx + 165, 500), (cx + 185, 580), (cx + 200, 700), (cx + 170, 740),
               (cx, 735), (cx - 170, 740), (cx - 200, 700), (cx - 185, 580), (cx - 165, 500), (cx - 130, 450), (cx - 70, 425)]
    pg.shape(blanket, smooth=True)
    cable_knit(pg, blanket, cx - 220, cx + 220, 420, 760)
    pg.shape(blanket, smooth=True, fill="none")
    # rolled edge of the blanket around her neck
    collar = [(cx - 110, 440), (cx - 60, 418), (cx, 412), (cx + 60, 418), (cx + 110, 440), (cx + 100, 460), (cx, 446), (cx - 100, 460)]
    pg.shape(collar, smooth=True)
    for k in range(-5, 6):
        pg.line([(cx + k * 18, 418 + abs(k) * 2.4), (cx + k * 19, 452 - abs(k) * 0.5)], lw=0.8)
    # tassels hanging over the seat
    for k in range(-8, 9):
        tx = cx + k * 21
        ty = 738 - abs(k) * 0.8
        pg.line([(tx, ty), (tx + 1, ty + 26)], lw=TH)
        pg.line([(tx - 3, ty + 4), (tx - 5, ty + 24)], lw=0.8)
        pg.line([(tx + 3, ty + 4), (tx + 5, ty + 24)], lw=0.8)
    # yarn basket on the floor
    bx, by = 520, 760
    basket = [(bx - 55, by - 40), (bx + 55, by - 40), (bx + 45, by + 30), (bx - 45, by + 30)]
    for (yx, yy, r) in [(bx - 22, by - 52, 22), (bx + 18, by - 50, 20)]:
        pg.circle(yx, yy, r)
        for k in range(4):
            a = k * 0.8
            pg.line([(yx + r * math.cos(a + 2.4), yy + r * math.sin(a + 2.4)), (yx + r * 0.3 * math.cos(a), yy + r * 0.2), (yx + r * math.cos(a - 0.8), yy + r * math.sin(a - 0.8))], lw=0.8, smooth=True)
    pg.line([(bx - 10, by - 90), (bx + 40, by - 40)], lw=LW)
    pg.line([(bx + 10, by - 92), (bx - 30, by - 40)], lw=LW)
    pg.shape(basket)
    wicker(pg, basket, bx - 60, bx + 60, by - 40, by + 30, rows=6)
    pg.shape(basket, fill="none")


@rpage("rg-summer-meadow", "Golden Hour Meadow", "summer")
def r_summer(pg):
    rng = random.Random(902)
    # sky and low sun
    sx, sy = 430, 330
    for i in range(22):
        a = math.radians(180 + i * 180 / 21)
        pg.line([(sx + 70 * math.cos(a), sy + 70 * math.sin(a)), (sx + 700 * math.cos(a), sy + 700 * math.sin(a))], lw=0.9)
    pg.circle(sx, sy, 56)
    cumulus(pg, 140, 130, 200, rng)
    cumulus(pg, 480, 90, 150, rng)
    for (bx, by, s) in [(260, 170, 9), (285, 185, 7), (300, 160, 8)]:
        pg.line([(bx - s, by - s * 0.3), (bx - s * 0.4, by - s * 0.5), (bx, by), (bx + s * 0.4, by - s * 0.5), (bx + s, by - s * 0.3)], lw=TH, smooth=True)
    # distant hills, tree line and lake
    top = hill(pg, 330, 18, 0.3, 0.8, lw=TH)
    for x in range(-10, 620, 14):
        y = 330 + 18 * math.sin(0.3 + (x + 40) / 680 * 8 * 0.8) - 4
        pg.circle(x, y + 6, 9 + rng.uniform(-2, 3), lw=0.9)
    pg.shape([(-10, 350), (610, 350), (610, 410), (-10, 410)], lw=TH)
    for k in range(9):
        y = 358 + k * 6
        x0 = rng.uniform(0, 400)
        pg.line([(x0, y), (x0 + rng.uniform(40, 180), y)], lw=0.8)
    for k in range(5):
        pg.line([(sx - 40 + k * 8, 360 + k * 9), (sx + 40 - k * 8, 360 + k * 9)], lw=0.9)
    # meadow behind her
    hill(pg, 420, 8, 1.0, 0.9, lw=TH)
    for _ in range(60):
        x = rng.uniform(0, 600)
        y = rng.uniform(430, 520)
        pg.line([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(8, 16))], lw=0.8)
    # her, seated, with a straw hat
    cx = 250
    # shoulders and arms (sundress straps)
    torso = [(cx - 40, 545), (cx - 95, 560), (cx - 120, 600), (cx - 128, 700), (cx - 100, 820), (cx + 100, 820), (cx + 128, 700), (cx + 120, 600), (cx + 95, 560), (cx + 40, 545)]
    pg.shape(torso, smooth=True)
    pg.line([(cx - 92, 600), (cx - 98, 700), (cx - 92, 820)], lw=TH, smooth=True)
    pg.line([(cx + 92, 600), (cx + 98, 700), (cx + 92, 820)], lw=TH, smooth=True)
    dress = [(cx - 88, 640), (cx - 30, 652), (cx + 30, 652), (cx + 88, 640), (cx + 92, 820), (cx - 92, 820)]
    pg.shape(dress, smooth=True)
    pg.clip_begin(d_smooth(dress))
    for _ in range(40):
        fx, fy = rng.uniform(cx - 100, cx + 100), rng.uniform(650, 820)
        for k in range(5):
            a = k * 2 * math.pi / 5
            pg.circle(fx + 3.4 * math.cos(a), fy + 3.4 * math.sin(a), 2.2, lw=0.7)
    pg.clip_end()
    for sd in (-1, 1):
        pg.line([(cx + sd * 72, 652), (cx + sd * 66, 600), (cx + sd * 60, 560)], lw=TH, smooth=True)
    long_hair_back(pg, cx, 400, 82, 3.0, rng, locks=7, width=0.72)
    # straw hat
    hy = 410
    pg.ellipse(cx, hy, 150, 34)
    pg.clip_begin(f"M{cx - 150} {hy} a150 34 0 1 0 300 0 a150 34 0 1 0 -300 0 Z")
    for r in range(1, 9):
        pg.ellipse(cx, hy, 150 - r * 9, 34 - r * 2, lw=0.8)
    for k in range(36):
        a = k * 2 * math.pi / 36
        pg.line([(cx + 60 * math.cos(a), hy + 14 * math.sin(a)), (cx + 150 * math.cos(a), hy + 34 * math.sin(a))], lw=0.6)
    pg.clip_end()
    crown = [(cx - 62, hy - 4), (cx - 64, hy - 50), (cx - 40, hy - 74), (cx, hy - 80), (cx + 40, hy - 74), (cx + 64, hy - 50), (cx + 62, hy - 4), (cx, hy + 6)]
    pg.shape(crown, smooth=True)
    pg.clip_begin(d_smooth(crown))
    for k in range(-6, 7):
        pg.line([(cx + k * 10, hy - 80), (cx + k * 11, hy + 6)], lw=0.6)
    for r in range(8):
        pg.line([(cx - 70, hy - 70 + r * 9), (cx, hy - 74 + r * 9), (cx + 70, hy - 70 + r * 9)], lw=0.6, smooth=True)
    pg.clip_end()
    band = [(cx - 62, hy - 8), (cx - 63, hy - 26), (cx, hy - 18), (cx + 63, hy - 26), (cx + 62, hy - 8), (cx, hy + 2)]
    pg.shape(band, smooth=True)
    for sd in (-1, 1):
        pg.shape([(cx + 50, hy - 14), (cx + 50 + sd * 6, hy + 40 + sd * 6), (cx + 64 + sd * 6, hy + 60), (cx + 62, hy - 10)], lw=TH, smooth=True)
    flower(pg, cx + 50, hy - 18, 13, n=5, wr=0.5, kind="round", center=0.3)
    # foreground flowers and grasses
    for _ in range(14):
        x = rng.uniform(-10, 610)
        grass_head(pg, x, 830, rng.uniform(180, 300), rng.uniform(-40, 40), rng)
    for x in (30, 90, 520, 570):
        wheat(pg, x, 830, rng.uniform(260, 320), rng.uniform(-30, 30))
    for (x, y, R) in [(60, 600, 34), (150, 690, 30), (400, 610, 36), (470, 700, 32), (540, 560, 28), (350, 740, 30)]:
        pg.line([(x, 830), (x + rng.uniform(-15, 15), (830 + y) / 2), (x, y)], lw=TH, smooth=True)
        poppy(pg, x, y, R, rng, ang=rng.uniform(0, 90))
    for (x, y) in [(110, 560), (440, 520), (585, 650), (20, 700), (500, 760), (200, 780)]:
        pg.line([(x, 830), (x, y)], lw=TH)
        cornflower(pg, x, y, 18, rng)
    for (x, y) in [(90, 760), (420, 780), (560, 730), (330, 690), (25, 620)]:
        pg.line([(x, 830), (x + 4, y)], lw=TH)
        chamomile(pg, x + 4, y, 18, rng)


@rpage("rg-autumn-walk", "A Walk in the Autumn Woods", "autumn")
def r_autumn(pg):
    rng = random.Random(904)
    pg.shape([(150, 800), (282, 440), (322, 440), (530, 800)], lw=TH)
    for _ in range(46):
        y = rng.uniform(445, 800)
        t = (y - 440) / 360
        x = rng.uniform(282 - 130 * t, 322 + 205 * t)
        pg.ellipse(x, y, 2 + 6 * t, 1 + 2.5 * t, lw=0.8)
    trunks = [(255, 12, 300), (350, 14, 290), (215, 20, 230), (390, 22, 220), (140, 30, 120), (460, 34, 100), (60, 46, -10), (560, 50, -10)]
    for (x, w, top) in trunks:
        birch(pg, x, top, 440 + (w * 4 if w > 25 else w * 2), w, rng)
    # canopy of autumn leaves along branches
    for (x0, y0, x1, y1) in [(60, 150, 200, 90), (560, 140, 420, 80), (140, 240, 240, 200), (460, 230, 360, 190), (30, 60, 150, 20), (580, 50, 470, 20)]:
        pg.tapered([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 10), (x1, y1)], 7, 3, lw=TH)
        for k in range(9):
            t = k / 8
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t - 10 * math.sin(math.pi * t)
            real_leaf(pg, x, y, rng.uniform(100, 260), rng.uniform(26, 36), 11, profile="ovate", teeth=10, tooth_amp=0.15, veins=3)
    for _ in range(12):
        x, y = rng.uniform(30, 570), rng.uniform(260, 560)
        if abs(x - 300) < 90 and y > 330:
            continue
        if rng.random() < 0.5:
            oak_leaf(pg, x, y, rng.uniform(0, 360), rng.uniform(36, 50), rng)
        else:
            real_leaf(pg, x, y, rng.uniform(0, 360), rng.uniform(32, 44), 14, profile="ovate", teeth=10, tooth_amp=0.15, veins=4)
    for (x, y) in [(70, 720), (110, 760), (40, 790), (560, 720), (520, 770), (590, 800), (150, 690), (480, 800)]:
        oak_leaf(pg, x, y, rng.uniform(0, 360), rng.uniform(60, 80), rng)
    for (x, y, w, h) in [(120, 660, 60, 70), (160, 670, 40, 48), (470, 640, 52, 60)]:
        mushroom_real(pg, x, y, w, h, rng)
    # her, walking away
    cx = 318
    # legs: left foot planted, right heel lifting
    pg.shape([(cx - 30, 652), (cx - 33, 700), (cx - 34, 738), (cx - 14, 738), (cx - 12, 700), (cx - 8, 652)], smooth=True)
    pg.shape([(cx + 8, 652), (cx + 14, 690), (cx + 20, 722), (cx + 38, 718), (cx + 32, 686), (cx + 28, 652)], smooth=True)
    # boots
    pg.shape([(cx - 36, 700), (cx - 12, 700), (cx - 11, 752), (cx - 9, 760), (cx - 40, 760), (cx - 38, 740)], smooth=False)
    pg.line([(cx - 39, 752), (cx - 10, 752)], lw=TH)
    pg.shape([(cx + 16, 694), (cx + 36, 690), (cx + 42, 728), (cx + 44, 736), (cx + 20, 742), (cx + 18, 728)], smooth=False)
    pg.line([(cx + 19, 732), (cx + 43, 728)], lw=TH)
    # sleeves
    pg.union_strokes([(sample_smooth([(cx - 50, 476), (cx - 60, 540), (cx - 62, 598)], 6), 26)], lw=LW)
    pg.union_strokes([(sample_smooth([(cx + 50, 476), (cx + 64, 530), (cx + 76, 578)], 6), 26)], lw=LW)
    for (x, y) in [(cx - 62, 596), (cx + 76, 576)]:
        pg.shape([(x - 14, y - 6), (x + 14, y - 6), (x + 14, y + 4), (x - 14, y + 4)], lw=TH)
    pg.ellipse(cx - 62, 612, 9, 12)
    # coat with a belt and soft folds
    coat = [(cx - 26, 462), (cx - 54, 470), (cx - 62, 520), (cx - 64, 570), (cx - 80, 660), (cx - 40, 668), (cx, 664), (cx + 40, 668), (cx + 80, 660), (cx + 64, 570), (cx + 62, 520), (cx + 54, 470), (cx + 26, 462)]
    pg.shape(coat, smooth=True)
    pg.shape([(cx - 63, 556), (cx + 63, 556), (cx + 64, 572), (cx - 64, 572)], lw=TH)
    pg.line([(cx, 600), (cx, 664)], lw=TH)
    for sd in (-1, 1):
        pg.line([(cx + sd * 30, 480), (cx + sd * 34, 550)], lw=0.8)
        pg.line([(cx + sd * 26, 585), (cx + sd * 46, 660)], lw=0.8)
        pg.line([(cx + sd * 52, 585), (cx + sd * 70, 655)], lw=0.8)
    # hair, scarf and beret
    long_hair_back(pg, cx, 384, 56, 3.0, rng, locks=6, width=0.74)
    scarf = [(cx - 40, 458), (cx, 448), (cx + 40, 458), (cx + 42, 478), (cx, 470), (cx - 42, 478)]
    pg.shape(scarf, smooth=True)
    for k in range(-3, 4):
        pg.line([(cx + k * 11, 452 + abs(k)), (cx + k * 11, 474 - abs(k))], lw=0.8)
    beret = [(cx - 36, 396), (cx - 32, 374), (cx - 6, 362), (cx + 24, 364), (cx + 40, 380), (cx + 36, 398), (cx, 402)]
    pg.shape(beret, smooth=True)
    pg.shape([(cx + 2, 362), (cx + 4, 354), (cx + 9, 354), (cx + 9, 362)], lw=TH)
    # basket in her right hand
    bx, by = cx + 96, 612
    pg.line([(cx + 78, 588), (bx - 30, by - 32), (bx, by - 52), (bx + 30, by - 32)], lw=LW, smooth=True)
    for (ax, ay, r) in [(bx - 18, by - 18, 15), (bx + 10, by - 20, 14)]:
        pg.circle(ax, ay, r)
        pg.line([(ax, ay - r), (ax + 2, ay - r - 7)], lw=TH)
    mushroom_real(pg, bx + 26, by - 8, 26, 30, rng)
    pg.ellipse(cx + 78, 592, 9, 12)
    basket = [(bx - 36, by - 12), (bx + 38, by - 12), (bx + 30, by + 30), (bx - 28, by + 30)]
    pg.shape(basket)
    wicker(pg, basket, bx - 40, bx + 40, by - 12, by + 30, rows=4)
    pg.shape(basket, fill="none")


@rpage("rg-spring-bench", "Under the Apple Blossoms", "spring")
def r_spring(pg):
    rng = random.Random(905)
    # blossoming apple branches arching over
    br = [[(-20, 150), (100, 110), (220, 70), (330, 40)], [(620, 190), (500, 140), (420, 80), (360, 30)],
          [(100, 112), (140, 190), (150, 270)], [(500, 142), (470, 220), (490, 300)], [(220, 72), (250, 140), (230, 200)]]
    for b in br:
        pg.tapered(b, 20 if b[0][0] in (-20, 620) else 9, 4, lw=LW)
    for b in br:
        sp = sample_smooth(b, 6)
        for i in range(2, len(sp), 4):
            x, y = sp[i]
            for _ in range(2):
                real_leaf(pg, x, y, rng.uniform(-70, 70) + 180 * (rng.random() < 0.5), 40, 16, profile="ovate", teeth=14, tooth_amp=0.1, veins=4)
        for i in range(3, len(sp), 4):
            x, y = sp[i]
            flower(pg, x + rng.uniform(-10, 10), y + rng.uniform(-6, 14), rng.uniform(22, 30), n=5, wr=0.62, kind='round', center=0.16, a0=rng.uniform(0, 72), stamens=9, inner=False)
    for _ in range(18):
        draw_leaf(pg, rng.uniform(20, 580), rng.uniform(220, 470), rng.uniform(0, 360), 13, 11, "round", veins=-1, notch=True, lw=FINE)
    # hedge in the back
    hill(pg, 410, 10, 0.2, 1.2, lw=TH)
    for _ in range(110):
        x, y = rng.uniform(0, 600), rng.uniform(420, 540)
        real_leaf(pg, x, y, rng.uniform(0, 360), 14, 6.5, profile="ovate", veins=-1, lw=0.8)
    # her: cardigan, sleeves, long braid
    cx = 230
    torso = [(cx - 30, 452), (cx - 70, 462), (cx - 104, 490), (cx - 118, 560), (cx - 122, 700), (cx + 122, 700), (cx + 118, 560), (cx + 104, 490), (cx + 70, 462), (cx + 30, 452)]
    pg.shape(torso, smooth=True)
    cable_knit(pg, torso, cx - 130, cx + 130, 450, 710, col=40, row=22)
    pg.shape(torso, smooth=True, fill="none")
    for sd in (-1, 1):
        pg.line([(cx + sd * 82, 480), (cx + sd * 90, 560), (cx + sd * 92, 700)], lw=TH, smooth=True)
        pg.line([(cx + sd * 100, 500), (cx + sd * 84, 486)], lw=0.8)
    pg.shape([(cx - 30, 452), (cx - 22, 432), (cx + 22, 432), (cx + 30, 452)])
    braid_back(pg, cx, 330, 84, 3.7, rng)
    # basket of tulips on the seat (behind the bench back)
    bx, by = 440, 600
    for k in range(7):
        x = bx - 40 + k * 13
        h = rng.uniform(80, 115)
        pg.line([(x, by), (x + rng.uniform(-10, 10), by - h * 0.6), (x + rng.uniform(-14, 14), by - h)], lw=TH, smooth=True)
    for (a, L) in [(-30, 90), (25, 80), (-8, 70)]:
        real_leaf(pg, bx + a, by, a, L, 11, profile="lance", veins=-1, bend=0.1)
    for k in range(7):
        x = bx - 40 + k * 13 + rng.uniform(-6, 6)
        y = by - rng.uniform(90, 120)
        w, h = 22, 30
        Lp = [(0, 0), (-0.55 * w, -0.25 * h), (-0.6 * w, -0.75 * h), (-0.4 * w, -1.05 * h), (-0.12 * w, -0.7 * h), (0, -0.2 * h)]
        a = rng.uniform(-15, 15)
        pg.shape(tf(Lp, x, y + h * 0.5, a), smooth=True)
        pg.shape(tf([(-px, py) for px, py in Lp], x, y + h * 0.5, a), smooth=True)
        pg.shape(tf([(0, 0.04 * h), (-0.42 * w, -0.3 * h), (-0.32 * w, -0.85 * h), (0, -1.1 * h), (0.32 * w, -0.85 * h), (0.42 * w, -0.3 * h)], x, y + h * 0.5, a), smooth=True)
    pg.line([(bx - 56, by - 6), (bx - 40, by - 70), (bx, by - 88), (bx + 40, by - 70), (bx + 56, by - 6)], lw=LW, smooth=True)
    basket = [(bx - 62, by - 6), (bx + 62, by - 6), (bx + 56, by + 40), (bx - 56, by + 40)]
    pg.shape(basket)
    wicker(pg, basket, bx - 66, bx + 66, by - 6, by + 40, rows=4)
    pg.shape(basket, fill="none")
    # bench back, in front of her (we see her from behind)
    for x in (52, 548):
        pg.shape([(x - 12, 600), (x + 12, 600), (x + 12, 800), (x - 12, 800)])
        pg.shape([(x - 16, 592), (x + 16, 592), (x + 16, 604), (x - 16, 604)], lw=TH)
    for k in range(4):
        y = 630 + k * 34
        pg.shape([(30, y), (570, y), (570, y + 24), (30, y + 24)], lw=TH)
        for j in range(5):
            x = 60 + j * 110 + rng.uniform(-10, 10)
            pg.line([(x, y + 7), (x + 30, y + 9), (x + 55, y + 6)], lw=0.7, smooth=True)
            pg.circle(x - 8, y + 12, 1.6, lw=0.7)
    # tulip bed in front
    for k in range(9):
        x = 20 + k * 70 + rng.uniform(-10, 10)
        real_leaf(pg, x - 6, 815, -18, 90, 13, profile="lance", veins=-1, bend=-0.1)
        real_leaf(pg, x + 6, 815, 20, 80, 12, profile="lance", veins=-1, bend=0.1)
        pg.line([(x, 815), (x + 2, 755)], lw=TH)
        w, h = 24, 32
        y = 760
        Lp = [(0, 0), (-0.55 * w, -0.25 * h), (-0.6 * w, -0.75 * h), (-0.4 * w, -1.05 * h), (-0.12 * w, -0.7 * h), (0, -0.2 * h)]
        pg.shape(tf(Lp, x + 2, y), smooth=True)
        pg.shape(tf([(-px, py) for px, py in Lp], x + 2, y), smooth=True)
        pg.shape(tf([(0, 0.04 * h), (-0.42 * w, -0.3 * h), (-0.32 * w, -0.85 * h), (0, -1.1 * h), (0.32 * w, -0.85 * h), (0.42 * w, -0.3 * h)], x + 2, y), smooth=True)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in RG:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("rg"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
