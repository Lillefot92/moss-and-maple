import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from pages import sunflower

GIRLS = []


def gpage(pid, title, season):
    def deco(fn):
        GIRLS.append((pid, title, season, fn))
        return fn
    return deco


def mirror(right):
    """right: points from top centre clockwise down the right side to bottom centre."""
    left = [(-x, y) for x, y in reversed(right[1:-1])]
    return right + left


def U(pts, cx, cy, s):
    return [(cx + x * s, cy + y * s) for x, y in pts]


# ------------------------------------------------------------- the girl
def back_hair(pg, cx, cy, s, style):
    if style == "long":
        r = [(0, -1.24), (0.62, -1.14), (1.12, -0.74), (1.34, -0.05), (1.4, 0.7), (1.5, 1.4), (1.66, 2.05),
             (1.38, 2.0), (1.22, 2.26), (0.98, 2.05), (0.76, 2.22), (0.58, 1.7), (0, 1.3)]
    elif style == "bob":
        r = [(0, -1.24), (0.62, -1.14), (1.12, -0.74), (1.32, -0.05), (1.34, 0.55), (1.22, 0.95), (1.0, 0.85), (0.86, 1.02), (0.6, 0.75), (0, 0.7)]
    else:  # bun: short at the back
        r = [(0, -1.22), (0.62, -1.12), (1.1, -0.74), (1.24, -0.05), (1.18, 0.5), (0.9, 0.7), (0, 0.6)]
    pts = U(mirror(r), cx, cy, s)
    pg.shape(pts, smooth=True)
    if style == "long":
        for sd in (1, -1):
            pg.line(U([(sd * 1.05, -0.4), (sd * 1.22, 0.5), (sd * 1.36, 1.3), (sd * 1.42, 1.95)], cx, cy, s), smooth=True)
    return pts


def face(pg, cx, cy, s, eyes="closed", glasses=False):
    pts = []
    for i in range(60):
        th = 2 * math.pi * i / 60
        sn = math.sin(th)
        x = 0.98 * math.cos(th) * (1 + 0.04 * sn)
        y = sn * (0.86 if sn < 0 else 0.93)
        pts.append((x, y))
    # ears
    pg.shape(U(pts, cx, cy, s), smooth=True)
    # eyes
    for sd in (1, -1):
        ex = sd * 0.36
        if eyes == "closed":
            pg.line(U([(ex - 0.15, 0.1), (ex, 0.19), (ex + 0.15, 0.1)], cx, cy, s), lw=LW, smooth=True)
            pg.line(U([(ex + sd * 0.15, 0.1), (ex + sd * 0.22, 0.04)], cx, cy, s), lw=TH)
            pg.line(U([(ex + sd * 0.1, 0.15), (ex + sd * 0.17, 0.12)], cx, cy, s), lw=TH)
        else:  # open, looking down a little
            pg.ellipse(cx + ex * s, cy + 0.14 * s, 0.085 * s, 0.11 * s, fill=INK, lw=0.5)
            pg.circle(cx + (ex + 0.03) * s, cy + 0.1 * s, 0.03 * s, lw=0.1)
            pg.line(U([(ex - 0.13, 0.0), (ex, -0.05), (ex + 0.13, 0.0)], cx, cy, s), lw=TH, smooth=True)
        # brows
        pg.line(U([(ex - 0.1, -0.12), (ex + 0.1, -0.15)] if sd > 0 else [(ex - 0.1, -0.15), (ex + 0.1, -0.12)], cx, cy, s), lw=TH)
        # blush
        pg.ellipse(cx + sd * 0.56 * s, cy + 0.38 * s, 0.15 * s, 0.085 * s, lw=TH)
    pg.line(U([(-0.03, 0.31), (0.02, 0.33)], cx, cy, s), lw=TH)
    pg.line(U([(-0.11, 0.5), (0, 0.57), (0.11, 0.5)], cx, cy, s), lw=LW, smooth=True)
    if glasses:
        for sd in (1, -1):
            pg.circle(cx + sd * 0.36 * s, cy + 0.12 * s, 0.24 * s, fill="none", lw=LW)
        pg.line(U([(-0.12, 0.08), (0, 0.04), (0.12, 0.08)], cx, cy, s), lw=LW, smooth=True)
    return pts


def bangs(pg, cx, cy, s, part=0.0, locks=5, sides=True):
    # soft, rounded locks of hair across the forehead
    xs = [-1.04] + [-1.04 + 2.08 * (i / locks) + part * (1 - abs(2 * i / locks - 1)) for i in range(1, locks)] + [1.04]
    ys = [0.02] + [-0.5 - 0.06 * math.sin(math.pi * i / locks) for i in range(1, locks)] + [0.02]
    bottom = []
    for i in range(locks):
        xa, xb, ya, yb = xs[i], xs[i + 1], ys[i], ys[i + 1]
        for k in range(10):
            t = k / 10
            depth = 0.3 if 0 < i < locks - 1 else 0.22
            bottom.append((xa + (xb - xa) * t, ya + (yb - ya) * t + depth * math.sin(math.pi * t) ** 0.8))
    bottom.append((xs[-1], ys[-1]))
    top = [(1.0, -0.55), (0.72, -1.02), (0.0, -1.24), (-0.72, -1.02), (-1.0, -0.55)]
    pg.shape(U(bottom + top, cx, cy, s), smooth=True)
    for i in range(1, locks):
        pg.line(U([(part * 0.4, -1.1), (xs[i] * 0.55 + part * 0.2, -0.85), (xs[i], ys[i] - 0.02)], cx, cy, s), smooth=True)
    for sd in ((1, -1) if sides else ()):
        lock = [(sd * 0.84, -0.05), (sd * 1.06, 0.02), (sd * 1.1, 0.5), (sd * 0.99, 0.88), (sd * 0.88, 0.56), (sd * 0.83, 0.18)]
        pg.shape(U(lock, cx, cy, s), smooth=True)


def neck_body(pg, cx, cy, s, sweater=True):
    pg.shape(U([(-0.22, 0.6), (-0.22, 1.3), (0.22, 1.3), (0.22, 0.6)], cx, cy, s))
    r = [(0, 1.02), (0.3, 1.05), (0.95, 1.22), (1.55, 1.58), (1.86, 2.3), (2.0, 3.6), (2.05, 6.0), (0, 6.0)]
    body = U(mirror(r), cx, cy, s)
    pg.shape(body, smooth=True)
    # collar
    pg.line(U([(-0.36, 1.08), (0, 1.32), (0.36, 1.08)], cx, cy, s), smooth=True)
    return body


def mitten(pg, x, y, s, a=0, flip=1):
    palm = [(-0.28, 0.32), (-0.32, -0.05), (-0.22, -0.32), (0, -0.4), (0.22, -0.32), (0.3, -0.05), (0.26, 0.32)]
    thumb = [(0.18, 0.0), (0.42, -0.12), (0.5, 0.04), (0.36, 0.2), (0.2, 0.22)]
    pg.union_shapes([tf([(px * flip, py) for px, py in thumb], x, y, a, s), tf([(px * flip, py) for px, py in palm], x, y, a, s)])
    for k in (-0.1, 0.06):
        pg.line(tf([(k * flip, -0.36), (k * flip, -0.24)], x, y, a, s), lw=TH)


def mug(pg, x, y, w, h, heart=True, steam=True):
    # handle
    pg.union_strokes([(sample_smooth([(x + w * 0.42, y - h * 0.3), (x + w * 0.78, y - h * 0.28), (x + w * 0.8, y + h * 0.15), (x + w * 0.42, y + h * 0.2)], 6), h * 0.14)])
    body = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2 * 0.94, y + h * 0.36), (x + w * 0.3, y + h / 2), (x - w * 0.3, y + h / 2), (x - w / 2 * 0.94, y + h * 0.36)]
    pg.shape(body, smooth=False)
    pg.ellipse(x, y - h / 2, w / 2, h * 0.12)
    pg.ellipse(x, y - h / 2 + h * 0.02, w * 0.42, h * 0.08, lw=TH)
    if heart:
        hx, hy, r = x, y + h * 0.05, w * 0.12
        pts = []
        for i in range(40):
            t = 2 * math.pi * i / 40
            pts.append((hx + r * 16 * math.sin(t) ** 3 / 16, hy - r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16))
        pg.shape(pts, lw=TH)
    if steam:
        for k, dx in enumerate((-w * 0.2, w * 0.08, w * 0.32)):
            yy = y - h / 2 - 12
            pg.line([(x + dx, yy), (x + dx - 8, yy - 18), (x + dx + 6, yy - 34), (x + dx - 4, yy - 52 - k * 6)], lw=LW, smooth=True)


def heart(pg, hx, hy, r, lw=TH):
    pts = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        pts.append((hx + r * math.sin(t) ** 3, hy - r * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16))
    pg.shape(pts, lw=lw)


def pumpkin(pg, x, y, w, h):
    for k, off in enumerate((-0.32, 0.32, -0.16, 0.16, 0.0)):
        ww = w * (0.42 if k < 2 else 0.4)
        pg.ellipse(x + off * w, y, ww, h / 2)
    pg.shape([(x - 6, y - h / 2 + 4), (x - 4, y - h / 2 - 18), (x + 8, y - h / 2 - 22), (x + 6, y - h / 2 + 4)], smooth=True)
    pg.line([(x + 4, y - h / 2 - 14), (x + 22, y - h / 2 - 30), (x + 34, y - h / 2 - 18)], smooth=True)


def cat_curled(pg, x, y, s):
    body = [(math.cos(t) * 1.25, math.sin(t) * 0.62) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    tail = sample_smooth([(1.05, 0.3), (0.6, 0.62), (-0.3, 0.7), (-0.9, 0.5)], 8)
    pg.shape(U(body, x, y, s), smooth=True)
    pg.union_strokes([(U(tail, x, y, s), 0.24 * s)])
    head = [(-0.75 + 0.48 * math.cos(t), -0.18 + 0.4 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    for ex in (-1.08, -0.5):
        pg.shape(U([(ex - 0.16, -0.38), (ex, -0.75), (ex + 0.16, -0.4)], x, y, s))
        pg.shape(U([(ex - 0.08, -0.42), (ex, -0.62), (ex + 0.08, -0.43)], x, y, s), lw=TH)
    pg.shape(U(head, x, y, s), smooth=True)
    for ex in (-0.95, -0.58):
        pg.line(U([(ex - 0.09, -0.15), (ex, -0.1), (ex + 0.09, -0.15)], x, y, s), lw=TH, smooth=True)
    pg.line(U([(-0.8, -0.02), (-0.77, 0.01), (-0.74, -0.02)], x, y, s), lw=TH)
    for sd in (-1, 1):
        pg.line(U([(-0.76 + sd * 0.12, 0.0), (-0.76 + sd * 0.42, -0.04)], x, y, s), lw=TH)
    for k in range(3):
        pg.line(U([(0.1 + k * 0.3, -0.58), (0.0 + k * 0.3, -0.3)], x, y, s), lw=TH, smooth=False)


def book(pg, x, y, w, h, tilt=0):
    # open book seen from the front
    L = [(-w / 2, -h / 2 + 10), (-w * 0.25, -h / 2 - 8), (0, -h / 2 + 6), (0, h / 2), (-w * 0.25, h / 2 - 12), (-w / 2, h / 2)]
    R = [(px * -1, py) for px, py in L]
    cover = [(-w / 2 - 12, -h / 2 + 18), (0, -h / 2 + 18), (w / 2 + 12, -h / 2 + 18), (w / 2 + 12, h / 2 + 12), (0, h / 2 + 12), (-w / 2 - 12, h / 2 + 12)]
    pg.shape(tf(cover, x, y, tilt))
    for side in (L, R):
        pg.shape(tf(side, x, y, tilt), smooth=True)
        sd = 1 if side is R else -1
        for k in range(6):
            yy = -h / 2 + 34 + k * (h - 70) / 6
            pg.line(tf([(sd * 20, yy + 2), (sd * w * 0.25, yy - 6), (sd * (w / 2 - 22), yy + 2)], x, y, tilt), lw=TH, smooth=True)
    pg.line(tf([(0, -h / 2 + 6), (0, h / 2)], x, y, tilt), lw=LW)


# ================================================================= pages
@gpage("winter-cocoa", "Cocoa by the Window", "winter")
def g_winter(pg):
    rng = random.Random(501)
    # wallpaper
    for i in range(-2, 16):
        x = i * 44
        pg.line([(x, 0), (x, 800)], lw=TH)
        for j in range(0, 20):
            y = j * 48 + (24 if i % 2 else 0)
            pg.circle(x + 22, y, 4, lw=TH)
    # window with arched top
    wx0, wx1, wy0, wy1 = 110, 490, 70, 520
    arch = [(wx0, wy1), (wx0, wy0 + 190)] + [(300 + 190 * math.cos(math.pi + math.pi * i / 30), wy0 + 190 + 190 * math.sin(math.pi + math.pi * i / 30)) for i in range(31)] + [(wx1, wy1)]
    pg.shape([(x + (8 if x > 300 else -8 if x < 300 else 0), y - (8 if y < wy1 else -8)) for x, y in arch])
    pg.shape(arch)
    pg.clip_begin(d_poly(arch))
    pg.circle(395, 175, 34)
    for _ in range(30):
        pg.circle(rng.uniform(120, 480), rng.uniform(80, 420), rng.uniform(2, 4.5), lw=TH)
    for (x, h, w) in [(150, 150, 70), (215, 190, 80), (395, 175, 75), (455, 140, 66)]:
        pine(pg, x, 470, h, w, tiers=4, snow=True)
    hill(pg, 455, 12, 0.5, 0.9)
    pg.clip_end()
    pg.line([(300, wy0), (300, wy1)], lw=LW * 2.2)
    pg.line([(wx0, 300), (wx1, 300)], lw=LW * 2.2)
    pg.line([(300, wy0 + 2), (300, wy1)], lw=LW * 0.1)
    # fairy lights along the arch
    lights = [(300 + 212 * math.cos(math.pi + math.pi * i / 14), wy0 + 196 + 212 * math.sin(math.pi + math.pi * i / 14) + 10 * (i % 2)) for i in range(15)]
    pg.line(lights, lw=TH, smooth=True)
    for (x, y) in lights[1:-1]:
        pg.ellipse(x, y + 9, 5.5, 8)
    # curtains
    for sd in (-1, 1):
        cx0 = 300 + sd * 245
        cur = [(cx0 - sd * 60, 40), (cx0 + sd * 70, 40), (cx0 + sd * 70, 560), (cx0 - sd * 10, 560), (cx0 - sd * 22, 380), (cx0 - sd * 70, 120)]
        pg.shape(cur, smooth=False)
        for k in range(3):
            pg.line([(cx0 - sd * (40 - k * 30), 50), (cx0 - sd * (8 - k * 22), 330), (cx0 + sd * (10 + k * 18), 550)], smooth=True)
        pg.shape([(cx0 - sd * 26, 360), (cx0 + sd * 72, 350), (cx0 + sd * 72, 378), (cx0 - sd * 22, 388)], smooth=False)
    pg.shape([(0, 28), (600, 28), (600, 46), (0, 46)])
    # window seat
    pg.shape([(40, 510), (560, 510), (575, 545), (25, 545)])
    pg.shape([(25, 545), (575, 545), (575, 800), (25, 800)])
    for x in (150, 300, 450):
        pg.line([(x, 560), (x, 800)], lw=TH)
    # plump pillows
    for (x, a) in [(92, -10), (508, 10)]:
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            r = 1 + 0.08 * math.cos(4 * t)
            pts.append((58 * r * math.cos(t), 40 * r * math.sin(t)))
        pg.shape(tf(pts, x, 488, a), smooth=True)
        pg.line(tf([(-50, -6), (-20, 4), (20, 4), (50, -6)], x, 488, a), lw=TH, smooth=True)
        pg.circle(*tf([(0, 4)], x, 488, a)[0], 6)
    # the girl, wrapped in a blanket
    cx, cy, s = 300, 360, 74
    back_hair(pg, cx, cy, s, "bob")
    blanket = [(300, 395), (360, 420), (430, 480), (470, 560), (492, 660), (480, 735), (300, 750), (120, 735), (108, 660), (130, 560), (170, 480), (240, 420)]
    pg.shape(blanket, smooth=True)
    pg.clip_begin(d_smooth(blanket))
    for k in range(-8, 9):
        pg.line([(300 + k * 34, 380), (300 + k * 34 + 40, 760)], lw=TH)
    for y in range(470, 760, 46):
        pg.line([(90, y), (510, y + 6)], lw=TH)
    pg.clip_end()
    pg.shape(blanket, smooth=True, fill="none")
    # opening in the blanket with a knit sweater
    opening = [(300, 445), (352, 470), (372, 560), (348, 660), (300, 690), (252, 660), (228, 560), (248, 470)]
    pg.shape(opening, smooth=True)
    for k in range(-2, 3):
        x = 300 + k * 26
        for y in range(470, 680, 20):
            pg.line([(x - 8, y), (x, y + 10), (x + 8, y)], lw=TH)
    pg.shape(opening, smooth=True, fill="none")
    face(pg, cx, cy, s, "closed")
    bangs(pg, cx, cy, s, part=0.05)
    # beanie
    beanie = [(-1.06, -0.32), (-0.98, -0.85), (-0.55, -1.32), (0, -1.45), (0.55, -1.32), (0.98, -0.85), (1.06, -0.32)]
    pg.shape(U(beanie, cx, cy, s), smooth=True)
    for k in range(-3, 4):
        pg.line(U([(k * 0.22, -0.55), (k * 0.17, -1.2)], cx, cy, s), lw=TH, smooth=True)
    cuff = [(-1.12, -0.18), (-1.1, -0.58), (0, -0.66), (1.1, -0.58), (1.12, -0.18), (0, -0.26)]
    pg.shape(U(cuff, cx, cy, s), smooth=True)
    for k in range(-9, 10):
        pg.line(U([(k * 0.11, -0.56 + abs(k) * 0.004), (k * 0.11, -0.24 + abs(k) * 0.004)], cx, cy, s), lw=TH)
    pg.union_circles([(cx + dx * s, cy + dy * s, r * s) for dx, dy, r in [(0, -1.55, 0.26), (-0.2, -1.5, 0.18), (0.2, -1.5, 0.18), (-0.1, -1.72, 0.16), (0.12, -1.72, 0.16)]])
    # mug with mittens
    mug(pg, 300, 548, 78, 82)
    for c in [(285, 528, 6), (300, 522, 6), (314, 530, 6)]:
        pg.union_circles([c])
    mitten(pg, 256, 560, 52, a=20, flip=-1)
    mitten(pg, 344, 560, 52, a=-20, flip=1)
    # cat on the cushion
    cat_curled(pg, 490, 630, 62)
    # books and candle
    for k, (w, h) in enumerate([(130, 26), (116, 22), (124, 24)]):
        y = 770 - k * 24
        pg.shape([(70 - w / 2 + k * 6, y), (70 + w / 2 + k * 6, y), (70 + w / 2 + k * 6, y - h), (70 - w / 2 + k * 6, y - h)])
        pg.line([(70 + w / 2 + k * 6 - 14, y - 3), (70 + w / 2 + k * 6 - 14, y - h + 3)], lw=TH)
    pg.shape([(64, 698), (64, 640), (96, 640), (96, 698)])
    pg.line([(80, 640), (80, 628)], lw=TH)
    pg.shape([(80, 590), (90, 612), (80, 630), (70, 612)], smooth=True)
    pg.shape([(80, 604), (84, 614), (80, 624), (76, 614)], lw=TH, smooth=True)


@gpage("autumn-scarf", "Warm Cup, Cool Breeze", "autumn")
def g_autumn(pg):
    rng = random.Random(502)
    cx, cy, s = 300, 330, 82
    # background circle with leaves
    for r in (262, 232):
        pg.circle(300, 390, r, lw=LW if r == 262 else TH)
    for (x, y, L, a, fl) in [(30, 80, 110, -6, 1), (440, 60, 110, 4, -1), (20, 700, 120, -4, 1), (460, 720, 100, 4, -1)]:
        curl(pg, x, y, L, a, size=14, flip=fl)
    for i in range(14):
        a = -80 + i * 360 / 14
        p = (300 + 262 * math.cos(math.radians(a)), 390 + 262 * math.sin(math.radians(a)))
        if i % 2 == 0:
            maple(pg, p[0], p[1], a + 90, 46)
        else:
            draw_leaf(pg, p[0], p[1], a + 90 + rng.uniform(-30, 30), 70, 22, "oak", veins=3)
    back_hair(pg, cx, cy, s, "long")
    body = neck_body(pg, cx, cy, s)
    # a fair-isle band across the sweater
    pg.clip_begin(d_smooth(body))
    for y0 in (cy + 1.95 * s, cy + 3.3 * s):
        pg.line([(0, y0), (600, y0)], lw=TH)
        pg.line([(0, y0 + 30), (600, y0 + 30)], lw=TH)
        for k in range(30):
            x = k * 22
            pg.shape([(x, y0 + 26), (x + 11, y0 + 5), (x + 22, y0 + 26)], lw=TH)
    pg.clip_end()
    # long hair in front of the shoulders
    for sd in (1, -1):
        lock = [(sd * 0.84, -0.1), (sd * 1.12, 0.3), (sd * 1.3, 0.9), (sd * 1.28, 1.4), (sd * 1.46, 1.9), (sd * 1.5, 2.35),
                (sd * 1.32, 2.22), (sd * 1.16, 2.44), (sd * 1.06, 2.0), (sd * 0.98, 1.5), (sd * 1.02, 1.0), (sd * 0.9, 0.5)]
        pg.shape(U(lock, cx, cy, s), smooth=True)
        pg.line(U([(sd * 1.0, 0.2), (sd * 1.16, 0.9), (sd * 1.14, 1.5), (sd * 1.3, 2.15)], cx, cy, s), smooth=True)
    # chunky scarf
    scarf = [(-1.05, 1.0), (-0.6, 0.82), (0, 0.9), (0.6, 0.82), (1.05, 1.0), (1.0, 1.42), (0.5, 1.6), (0, 1.62), (-0.5, 1.6), (-1.0, 1.42)]
    tail = [(0.25, 1.4), (0.75, 1.45), (0.82, 2.3), (0.3, 2.35)]
    pg.shape(U(tail, cx, cy, s), smooth=True)
    for k in range(5):
        x = 0.35 + k * 0.11
        pg.line(U([(x, 2.33), (x - 0.02, 2.55)], cx, cy, s), lw=LW)
    for y in (1.7, 1.95, 2.15):
        pg.line(U([(0.3, y), (0.8, y + 0.02)], cx, cy, s), lw=TH)
    pg.shape(U(scarf, cx, cy, s), smooth=True)
    for k in range(-8, 9):
        x = k * 0.12
        pg.line(U([(x - 0.05, 0.98), (x, 1.12), (x + 0.05, 0.98)], cx, cy, s), lw=TH)
        pg.line(U([(x - 0.05, 1.24), (x, 1.38), (x + 0.05, 1.24)], cx, cy, s), lw=TH)
    face(pg, cx, cy, s, "closed")
    bangs(pg, cx, cy, s, part=-0.08, sides=False)
    # beret
    beret = [(-1.2, -0.62), (-1.0, -1.05), (-0.3, -1.38), (0.45, -1.36), (1.05, -1.0), (1.2, -0.6), (0.6, -0.72), (-0.4, -0.74)]
    pg.shape(U([(x, y + 0.05) for x, y in beret], cx, cy, s), smooth=True)
    pg.line(U([(-0.95, -0.68), (0, -0.78), (0.95, -0.66)], cx, cy, s), lw=TH, smooth=True)
    pg.shape(U([(0.1, -1.3), (0.12, -1.48), (0.22, -1.5), (0.22, -1.32)], cx, cy, s))
    # mug with both hands
    mug(pg, cx, cy + 2.55 * s, 96, 104)
    mitten(pg, cx - 62, cy + 2.62 * s, 62, a=16, flip=-1)
    mitten(pg, cx + 62, cy + 2.62 * s, 62, a=-16, flip=1)
    # sleeves cuffs
    # pumpkins at the bottom corners
    pumpkin(pg, 85, 735, 120, 86)
    pumpkin(pg, 155, 760, 80, 56)
    pumpkin(pg, 515, 740, 120, 84)
    for (x, y, a) in [(60, 300, -30), (540, 280, 30), (560, 560, -20), (40, 540, 15)]:
        acorn(pg, x, y, a, 36)


@gpage("spring-bouquet", "A Bouquet for Spring", "spring")
def g_spring(pg):
    rng = random.Random(503)
    cx, cy, s = 300, 360, 80
    # blossom branches from the corners
    pg.tapered([(-20, 140), (80, 150), (170, 110), (240, 50)], 18, 6)
    pg.tapered([(620, 220), (520, 200), (440, 150), (390, 70)], 18, 6)
    pg.tapered([(240, 52), (300, 30), (360, 40)], 8, 4)
    for (x, y, R, a) in [(80, 150, 34, 10), (170, 112, 30, 40), (238, 52, 26, 5), (520, 200, 34, 30), (440, 150, 30, 0), (392, 70, 26, 20), (30, 140, 26, 50), (575, 212, 28, 60), (300, 32, 22, 15), (356, 42, 20, 40)]:
        flower(pg, x, y, R, n=5, wr=0.5, kind="round", center=0.2, a0=a, notch=True, stamens=6)
    for _ in range(14):
        draw_leaf(pg, rng.uniform(30, 570), rng.uniform(240, 560), rng.uniform(0, 360), 18, 13, "round", veins=-1, notch=True, lw=TH)
    # butterflies
    for (x, y, sz, a) in [(80, 330, 34, -15), (520, 380, 30, 15)]:
        for sd in (1, -1):
            pg.shape(tf([(sd * px * sz / 30, py * sz / 30) for px, py in sample_smooth([(0, 0), (16, -26), (34, -24), (34, -4), (18, 6), (0, 0)], 4)], x, y, a), smooth=True)
            pg.shape(tf([(sd * px * sz / 30, py * sz / 30) for px, py in sample_smooth([(0, 2), (22, 8), (24, 26), (8, 26), (0, 2)], 4)], x, y, a), smooth=True)
        pg.ellipse(x, y + 4, 3.5, 16, a)
    back_hair(pg, cx, cy, s, "long")
    body = neck_body(pg, cx, cy, s)
    # dress collar & buttons
    pg.shape(U([(-0.45, 1.06), (0, 1.36), (-0.1, 1.55), (-0.62, 1.32)], cx, cy, s), smooth=True)
    pg.shape(U([(0.45, 1.06), (0, 1.36), (0.1, 1.55), (0.62, 1.32)], cx, cy, s), smooth=True)
    pg.clip_begin(d_smooth(body))
    for _ in range(26):
        x, y = rng.uniform(cx - 2 * s, cx + 2 * s), rng.uniform(cy + 1.5 * s, 800)
        flower(pg, x, y, 9, n=5, wr=0.55, kind="round", center=0.3)
    pg.clip_end()
    for sd in (1, -1):
        lock = [(sd * 0.84, -0.1), (sd * 1.12, 0.3), (sd * 1.3, 0.9), (sd * 1.28, 1.4), (sd * 1.46, 1.9), (sd * 1.5, 2.35),
                (sd * 1.32, 2.22), (sd * 1.16, 2.44), (sd * 1.06, 2.0), (sd * 0.98, 1.5), (sd * 1.02, 1.0), (sd * 0.9, 0.5)]
        pg.shape(U(lock, cx, cy, s), smooth=True)
        pg.line(U([(sd * 1.0, 0.2), (sd * 1.16, 0.9), (sd * 1.14, 1.5), (sd * 1.3, 2.15)], cx, cy, s), smooth=True)
    face(pg, cx, cy, s, "closed")
    bangs(pg, cx, cy, s, part=0.1, sides=False)
    # sun hat: brim, crown, ribbon, flowers
    pg.ellipse(cx, cy - 0.78 * s, 1.95 * s, 0.42 * s)
    pg.ellipse(cx, cy - 0.78 * s, 1.6 * s, 0.3 * s, lw=TH)
    crown = [(-0.88, -0.86), (-0.85, -1.3), (-0.5, -1.62), (0, -1.68), (0.5, -1.62), (0.85, -1.3), (0.88, -0.86), (0, -0.78)]
    pg.shape(U(crown, cx, cy, s), smooth=True)
    band = [(-0.88, -0.86), (-0.87, -1.08), (0, -1.0), (0.87, -1.08), (0.88, -0.86), (0, -0.78)]
    pg.shape(U(band, cx, cy, s), smooth=True)
    for (dx, dy, R, a) in [(-0.62, -1.02, 0.2, 10), (-0.3, -1.12, 0.17, 30), (-0.85, -1.15, 0.15, 0)]:
        flower(pg, cx + dx * s, cy + dy * s, R * s, n=5, wr=0.55, kind="round", center=0.28, a0=a)
    draw_leaf(pg, cx - 0.08 * s, cy - 1.0 * s, 70, 0.32 * s, 0.11 * s, "ovate", veins=-1)
    # bouquet held in front
    bx, by = cx, cy + 2.55 * s
    stems = []
    for k in range(-3, 4):
        stems.append((sample_smooth([(bx + k * 4, by + 150), (bx + k * 10, by + 40), (bx + k * 26, by - 50)], 6), 6))
    pg.union_strokes(stems)
    for (dx, dy, a, L) in [(-70, -40, -60, 60), (70, -40, 60, 60), (-55, 10, -100, 50), (55, 10, 100, 50)]:
        draw_leaf(pg, bx + dx * 0.3, by + dy + 30, a, L, 16, "lance", veins=-1)
    blooms = [(-62, -78, "tulip"), (0, -110, "tulip"), (62, -78, "tulip"), (-30, -40, "daisy"), (32, -42, "daisy"), (-82, -20, "daisy"), (84, -22, "daisy")]
    for dx, dy, kind in blooms:
        x, y = bx + dx, by + dy
        if kind == "daisy":
            flower(pg, x, y, 26, n=12, wr=0.3, kind="round", center=0.3)
        else:
            w, h = 40, 56
            Lp = [(0, 0), (-0.55 * w, -0.25 * h), (-0.6 * w, -0.75 * h), (-0.4 * w, -1.05 * h), (-0.12 * w, -0.7 * h), (0, -0.2 * h)]
            pg.shape(tf(Lp, x, y + h * 0.5), smooth=True)
            pg.shape(tf([(-px, py) for px, py in Lp], x, y + h * 0.5), smooth=True)
            pg.shape(tf([(0, 0.04 * h), (-0.42 * w, -0.3 * h), (-0.32 * w, -0.85 * h), (0, -1.1 * h), (0.32 * w, -0.85 * h), (0.42 * w, -0.3 * h)], x, y + h * 0.5), smooth=True)
    # wrapping paper & ribbon
    wrap = [(bx - 70, by + 20), (bx + 70, by + 20), (bx + 30, by + 170), (bx - 30, by + 170)]
    pg.shape(wrap)
    pg.line([(bx - 40, by + 22), (bx - 14, by + 168)], lw=TH)
    pg.line([(bx + 40, by + 22), (bx + 14, by + 168)], lw=TH)
    pg.shape([(bx - 22, by + 80), (bx - 60, by + 62), (bx - 58, by + 100)], smooth=True)
    pg.shape([(bx + 22, by + 80), (bx + 60, by + 62), (bx + 58, by + 100)], smooth=True)
    pg.circle(bx, by + 80, 12)
    mitten(pg, bx - 40, by + 110, 54, a=10, flip=-1)
    mitten(pg, bx + 40, by + 110, 54, a=-10, flip=1)


@gpage("summer-reading", "Lost in a Summer Book", "summer")
def g_summer(pg):
    rng = random.Random(504)
    cx, cy, s = 300, 360, 82
    # sky: sun with soft rays and clouds
    for i in range(18):
        a = math.radians(i * 20)
        pg.line([(300 + 130 * math.cos(a), 300 + 130 * math.sin(a)), (300 + 700 * math.cos(a), 300 + 700 * math.sin(a))], lw=TH)
    pg.circle(300, 300, 250, lw=TH)
    cloud(pg, 100, 110, 150, rng)
    cloud(pg, 510, 150, 130, rng)
    # sunflowers on both sides
    for (x, y, R, st) in [(80, 420, 70, 800), (525, 450, 64, 800), (40, 590, 50, 800), (565, 610, 46, 800)]:
        pg.tapered([(x, st), (x + 4, (y + st) / 2), (x, y)], 14, 10)
    for (x, y, a) in [(80, 560, -55), (525, 600, 55)]:
        draw_leaf(pg, x, y, a, 70, 26, "heart", veins=3, stem=6)
    sunflower(pg, 80, 420, 70, rng)
    sunflower(pg, 525, 450, 64, rng, a0=5)
    sunflower(pg, 40, 590, 50, rng, a0=2)
    sunflower(pg, 565, 610, 46, rng, a0=4)
    # the girl, hair up in a bun with a bow
    pg.circle(cx, cy - 1.32 * s, 0.42 * s)
    spiral(pg, cx, cy - 1.32 * s, 0.32 * s, turns=1.5, lw=TH)
    back_hair(pg, cx, cy, s, "bun")
    neck_body(pg, cx, cy, s)
    face(pg, cx, cy, s, "closed", glasses=True)
    bangs(pg, cx, cy, s, part=0.0)
    # bow
    for sd in (-1, 1):
        pg.shape(U([(0.55, -1.0), (0.55 + sd * 0.38, -1.22), (0.55 + sd * 0.4, -0.85)], cx, cy, s), smooth=True)
        pg.line(U([(0.55, -1.0), (0.55 + sd * 0.25, -1.06)], cx, cy, s), lw=TH)
    pg.circle(cx + 0.55 * s, cy - 1.02 * s, 0.09 * s)
    # the big open book in front
    book(pg, cx, 640, 420, 230)
    mitten(pg, cx - 175, 548, 56, a=-8, flip=-1)
    mitten(pg, cx + 175, 548, 56, a=8, flip=1)
    # bee & butterflies
    bx, by = 470, 270
    pg.line([(400, 320), (430, 300), (450, 316), (460, 290)], lw=TH, smooth=True)
    pg.ellipse(bx - 4, by - 18, 12, 18, -30)
    pg.ellipse(bx + 12, by - 18, 12, 18, 30)
    pg.ellipse(bx, by, 24, 16)
    pg.clip_begin(f"M{bx - 24} {by} a24 16 0 1 0 48 0 a24 16 0 1 0 -48 0 Z")
    for k in (-10, 0, 10):
        pg.line([(bx + k - 5, by - 18), (bx + k + 5, by + 18)], lw=LW)
    pg.clip_end()
    pg.circle(bx + 28, by - 3, 10)
    # daisies along the bottom
    for i in range(7):
        x = 250 + i * 60 + rng.uniform(-8, 8)
        flower(pg, x, 785 + rng.uniform(-6, 6), 18, n=10, wr=0.32, kind="round", center=0.3)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in GIRLS:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("girls"):
        print(m["id"], len(m["svg"]))
