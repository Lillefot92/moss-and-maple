"""More Philippine pages: sampaguita & ilang-ilang, bangka beach, Chocolate Hills with a tarsier, a jeepney."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import real_leaf, FINE
from realgirls import cumulus, A
from philippines import coconut_palm, sampaguita, mountains, bahay_kubo

PH2 = []


def ppage(pid, title, season):
    def deco(fn):
        PH2.append((pid, title, season, fn))
        return fn
    return deco


def ribbon(pg, center, w0, w1, lw=TH, twist=True):
    """A narrow, wavy petal along a centre line, tapering from w0 to w1."""
    sp = sample_smooth(center, 8)
    n = len(sp)
    L, R = [], []
    for i in range(n):
        (x0, y0), (x1, y1) = sp[max(i - 1, 0)], sp[min(i + 1, n - 1)]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) * math.sin(math.pi * min(1, 0.15 + t * 0.95)) ** 0.5
        w *= (1 + 0.25 * math.sin(t * 9))
        L.append((sp[i][0] + nx * w, sp[i][1] + ny * w))
        R.append((sp[i][0] - nx * w, sp[i][1] - ny * w))
    pg.shape(L + list(reversed(R)), lw=lw, smooth=True)
    pg.line(sp[1:-2], lw=0.7, smooth=True)


def sampaguita_big(pg, x, y, R, rng, a0=0):
    for layer, (n, rr, wr) in enumerate([(9, 1.0, 0.36), (7, 0.74, 0.38), (5, 0.48, 0.4)]):
        off = a0 + layer * 17
        for i in range(n):
            a = off + i * 360 / n + rng.uniform(-6, 6)
            out = leaf_geom(R * rr, R * rr * wr, "round", n=16)
            out = [(px * (1 + 0.05 * math.sin(py * 0.3)), py) for px, py in out]
            pg.shape(tf(out, x, y, a), lw=TH, smooth=True)
            if layer == 0:
                pg.line(tf([(0, -R * 0.35), (0, -R * 0.8)], x, y, a), lw=0.6)
    pg.circle(x, y, R * 0.1, lw=TH)


def sampaguita_bud(pg, x, y, ang, s):
    bud = [(0, 0), (-0.16, -0.25), (-0.18, -0.6), (-0.08, -0.95), (0, -1.0), (0.09, -0.92), (0.17, -0.6), (0.15, -0.25)]
    pg.shape(tf(bud, x, y, ang, s), smooth=True)
    pg.line(tf([(-0.12, -0.2), (0.05, -0.55), (-0.02, -0.95)], x, y, ang, s), lw=0.7, smooth=True)
    for sd in (-1, 0, 1):
        pg.line(tf([(0, 0.02), (sd * 0.14, 0.1), (sd * 0.26, -0.12)], x, y, ang, s), lw=0.8, smooth=True)
    pg.line(tf([(0, 0.02), (0, 0.25)], x, y, ang, s), lw=TH)


def ilang_flower(pg, x, y, s, rng, ang=0):
    """Ilang-ilang: six long, narrow, twisting petals hanging down from a small calyx."""
    for i in range(6):
        a = ang + (i - 2.5) * 20 + rng.uniform(-6, 6)
        L = s * rng.uniform(0.85, 1.05)
        pts = []
        for k in range(7):
            t = k / 6
            px = math.sin(math.radians(a)) * L * t + s * 0.08 * math.sin(t * 6 + i)
            py = math.cos(math.radians(a)) * L * t * 0.95 + s * 0.1 * t * t
            pts.append((x + px, y + py))
        ribbon(pg, pts, s * 0.07, s * 0.035)
    pg.shape([(x - s * 0.08, y + 2), (x - s * 0.06, y - s * 0.08), (x + s * 0.06, y - s * 0.08), (x + s * 0.08, y + 2), (x, y + s * 0.06)], smooth=True)


def karst_island(pg, x, base, w, h, rng):
    pts = [(x - w / 2, base)]
    n = 7
    for k in range(1, n):
        t = k / n
        bump = math.sin(math.pi * t) ** 0.6
        pts.append((x - w / 2 + w * t + rng.uniform(-6, 6), base - h * bump * (0.85 + 0.25 * rng.random())))
    pts.append((x + w / 2, base))
    top = sample_smooth(pts, 8)
    pg.shape(top, lw=TH)
    for _ in range(int(w / 6)):
        px = rng.uniform(x - w * 0.42, x + w * 0.42)
        t = (px - (x - w / 2)) / w
        py = base - h * math.sin(math.pi * t) ** 0.6 * rng.uniform(0.25, 0.85)
        pg.line([(px, py), (px + rng.uniform(-2, 2), py + rng.uniform(8, 18))], lw=0.6)
    for k in range(4):
        px = x - w * 0.3 + k * w * 0.2
        pg.line([(px, base - h * 0.55), (px + 6, base - h * 0.25), (px + 2, base - 4)], lw=0.7, smooth=True)


def shell(pg, x, y, s, ang):
    pts = []
    for i in range(9):
        a = math.radians(-150 + i * 120 / 8)
        pts.append((s * math.cos(a), s * math.sin(a)))
    pg.shape(tf([(0, s * 0.45)] + pts, x, y, ang), smooth=True)
    for p in pts[1:-1]:
        pg.line(tf([(0, s * 0.42), (p[0] * 0.92, p[1] * 0.92)], x, y, ang), lw=0.7)
    pg.shape(tf([(-s * 0.3, s * 0.3), (s * 0.3, s * 0.3), (s * 0.22, s * 0.6), (-s * 0.22, s * 0.6)], x, y, ang), lw=TH)


def starfish(pg, x, y, r, ang):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = math.radians(ang + i * 36)
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a) * 0.7))
    pg.shape(pts, smooth=True)
    for i in range(5):
        a = math.radians(ang + i * 72)
        for k in range(1, 5):
            t = k / 5
            pg.circle(x + r * 0.8 * t * math.cos(a), y + r * 0.8 * t * math.sin(a) * 0.7, 1.5, lw=0.6)


def tarsier(pg, x, y, s, rng):
    """A Philippine tarsier clinging to a vertical branch (branch centre at x)."""
    T = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    # tail hanging down along the branch
    tail = sample_smooth([(0.25, 0.95), (0.3, 1.5), (0.22, 2.1), (0.28, 2.6)], 8)
    pg.union_strokes([(T(tail), 0.06 * s)], lw=TH)
    tuft = [(0.22, 2.5), (0.36, 2.55), (0.38, 2.85), (0.28, 2.95), (0.2, 2.8)]
    pg.shape(T(tuft), smooth=True, lw=TH)
    # long hind leg folded, foot gripping
    leg = [(0.55, 0.6), (0.85, 0.75), (0.8, 1.05), (0.45, 1.15), (0.25, 1.1), (0.3, 0.9)]
    pg.shape(T(leg), smooth=True)
    for k in range(3):
        pg.shape(T([(0.12, 1.02 + k * 0.08), (-0.18, 0.98 + k * 0.1), (-0.24, 1.02 + k * 0.1), (-0.2, 1.07 + k * 0.1), (0.1, 1.1 + k * 0.08)]), lw=TH, smooth=True)
        pg.circle(*T([(-0.22, 1.03 + k * 0.1)])[0], 0.035 * s, lw=TH)
    # body with soft fur
    body = [(0.05, -0.15), (0.5, -0.1), (0.75, 0.25), (0.78, 0.65), (0.6, 0.95), (0.3, 1.0), (0.1, 0.8), (0.02, 0.4)]
    bP = T(body)
    pg.shape(bP, smooth=True)
    pg.clip_begin(d_smooth(bP))
    for _ in range(50):
        px, py = rng.uniform(0.05, 0.75), rng.uniform(-0.1, 0.95)
        pg.line(T([(px, py), (px + 0.02, py + 0.06)]), lw=0.6)
    pg.clip_end()
    pg.shape(bP, smooth=True, fill="none")
    # arms reaching to the branch with long fingers and round pads
    for (sy_, ln) in [(0.05, 1.0), (0.32, 0.95)]:
        arm = [(0.35, sy_ - 0.02), (0.1, sy_ + 0.02), (-0.05, sy_ + 0.08), (0.1, sy_ + 0.12), (0.38, sy_ + 0.1)]
        pg.shape(T(arm), smooth=True)
        for k in range(4):
            fy = sy_ - 0.02 + k * 0.05
            pg.line(T([(-0.03, fy + 0.05), (-0.2, fy + 0.02)]), lw=TH)
            pg.circle(*T([(-0.22, fy + 0.02)])[0], 0.028 * s, lw=TH)
    # head: huge eyes, big thin ears
    hx, hy = 0.45, -0.55
    for sd in (-1, 1):
        ear = [(hx + sd * 0.28, hy - 0.25), (hx + sd * 0.52, hy - 0.62), (hx + sd * 0.62, hy - 0.42), (hx + sd * 0.5, hy - 0.18)]
        pg.shape(T(ear), smooth=True)
        pg.line(T([(hx + sd * 0.34, hy - 0.26), (hx + sd * 0.5, hy - 0.5), (hx + sd * 0.54, hy - 0.36)]), lw=0.7, smooth=True)
    head = [(hx + 0.52 * math.cos(t), hy + 0.46 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    pg.shape(T(head), smooth=True)
    for sd in (-1, 1):
        ex = hx + sd * 0.24
        pg.circle(*T([(ex, hy)])[0], 0.24 * s)
        pg.circle(*T([(ex, hy)])[0], 0.17 * s, lw=TH)
        pg.circle(*T([(ex, hy)])[0], 0.09 * s, fill=INK, lw=0.1)
        pg.circle(*T([(ex - 0.04, hy - 0.05)])[0], 0.03 * s, lw=0.1)
        for k in range(8):
            a = k * math.pi / 4
            pg.line(T([(ex + 0.1 * math.cos(a), hy + 0.1 * math.sin(a)), (ex + 0.16 * math.cos(a), hy + 0.16 * math.sin(a))]), lw=0.5)
    pg.shape(T([(hx - 0.04, hy + 0.27), (hx + 0.04, hy + 0.27), (hx, hy + 0.31)]), lw=TH)
    pg.line(T([(hx - 0.1, hy + 0.37), (hx, hy + 0.4), (hx + 0.1, hy + 0.37)]), lw=0.8, smooth=True)
    for k in range(10):
        a = math.pi * (1.1 + 0.8 * k / 9)
        px, py = hx + 0.5 * math.cos(a), hy + 0.44 * math.sin(a)
        pg.line(T([(px, py), (px + 0.03 * math.cos(a), py + 0.06 * math.sin(a))]), lw=0.6)


def wheel(pg, x, y, r):
    pg.circle(x, y, r)
    pg.circle(x, y, r * 0.66, lw=TH)
    pg.circle(x, y, r * 0.5)
    for k in range(8):
        a = k * math.pi / 4
        pg.line([(x + r * 0.16 * math.cos(a), y + r * 0.16 * math.sin(a)), (x + r * 0.46 * math.cos(a), y + r * 0.46 * math.sin(a))], lw=0.9)
    pg.circle(x, y, r * 0.16)
    for k in range(18):
        a = k * 2 * math.pi / 18
        pg.line([(x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a)), (x + r * 0.95 * math.cos(a), y + r * 0.95 * math.sin(a))], lw=0.6)


def chrome_horse(pg, x, y, s, flip=1):
    """A stylised chrome horse ornament, rearing, as seen on jeepney hoods."""
    pts = [(0, 0), (0.1, -0.35), (0.05, -0.6), (0.2, -0.8), (0.35, -0.95), (0.5, -0.92), (0.45, -0.8), (0.3, -0.7),
           (0.3, -0.5), (0.5, -0.45), (0.65, -0.55), (0.6, -0.35), (0.4, -0.28), (0.35, -0.05), (0.45, 0.0)]
    P = [(x + px * s * flip, y + py * s) for px, py in pts]
    pg.shape(P, smooth=True, lw=TH)
    pg.line([(x + 0.25 * s * flip, y - 0.75 * s), (x + 0.1 * s * flip, y - 0.5 * s)], lw=0.7)
    pg.shape([(x - 0.08 * s, y), (x + 0.55 * s * flip, y), (x + 0.55 * s * flip, y + 0.08 * s), (x - 0.08 * s, y + 0.08 * s)], lw=TH)


# ================================================================= pages
@ppage("ph-sampaguita", "Sampaguita & Ilang-Ilang", "spring")
def p_flowers(pg):
    rng = random.Random(1201)
    # sampaguita branches with glossy opposite leaves
    branches = ([(-20, 560), (120, 470), (250, 360), (330, 250)], [(620, 330), (520, 360), (420, 430), (350, 500)],
                [(-20, 300), (80, 290), (170, 250), (220, 190)])
    for br in branches:
        sp = pg.tapered(br, 9, 4, lw=LW)
        for i in range(3, len(sp) - 2, 5):
            x, y = sp[i]
            (x0, y0), (x1, y1) = sp[i - 1], sp[i + 1]
            phi = math.degrees(math.atan2(y1 - y0, x1 - x0))
            for sd in (-1, 1):
                real_leaf(pg, x, y, phi + sd * 50 + 90, 72, 30, profile="elliptic", veins=5, bend=0.1 * sd, stem=8)
    for (x, y, R, a) in [(330, 245, 46, 0), (250, 350, 42, 15), (140, 460, 38, 5), (350, 500, 44, 20), (450, 420, 38, 8), (60, 515, 30, 12),
                         (220, 190, 40, 30), (100, 285, 34, 10), (240, 560, 30, 0), (470, 560, 32, 40)]:
        sampaguita_big(pg, x, y, R, rng, a0=a)
    for (x, y, a) in [(300, 215, -20), (282, 330, 30), (175, 435, -40), (390, 485, 40), (480, 390, 10), (100, 490, -15), (190, 170, -30), (150, 265, 20)]:
        sampaguita_bud(pg, x, y, a, 34)
    # ilang-ilang twig hanging from the top right, with long wavy leaves
    tw = pg.tapered([(620, 40), (520, 70), (440, 120), (400, 170)], 8, 3, lw=LW)
    for (x, y, a, L) in [(560, 55, 160, 120), (480, 90, -150, 110), (430, 135, 170, 100), (590, 48, 200, 100)]:
        real_leaf(pg, x, y, a, L, 26, profile="elliptic", veins=6, bend=0.12, teeth=8, tooth_amp=0.08)
    for (x, y, s, a) in [(520, 80, 110, -10), (455, 120, 100, 6), (410, 168, 95, -4)]:
        pg.line([(x, y), (x + 2, y + 14)], lw=TH)
        ilang_flower(pg, x + 2, y + 16, s, rng, ang=a)
    # a sampaguita garland draped across the bottom, with a ribbon tassel
    g = sample_smooth([(-20, 620), (120, 700), (300, 730), (480, 690), (620, 610)], 14)
    pg.line(g, lw=TH, smooth=True)
    for i in range(1, len(g) - 1, 2):
        x, y = g[i]
        if i % 6 == 1:
            sampaguita_big(pg, x, y, 18, rng, a0=rng.uniform(0, 40))
        else:
            sampaguita_bud(pg, x, y + 6, 180 + rng.uniform(-30, 30), 22)
    tx, ty = 300, 730
    pg.shape([(tx - 16, ty + 10), (tx + 16, ty + 10), (tx + 22, ty + 40), (tx - 22, ty + 40)], lw=TH)
    for k in range(7):
        xx = tx - 18 + k * 6
        pg.line([(xx, ty + 40), (xx + (k - 3) * 1.5, ty + 78)], lw=TH)
    for sd in (-1, 1):
        ribbon(pg, [(tx, ty + 12), (tx + sd * 30, ty + 30), (tx + sd * 46, ty + 70), (tx + sd * 40, ty + 100)], 7, 5)


@ppage("ph-bangka-beach", "Bangka on the Beach", "summer")
def p_beach(pg):
    rng = random.Random(1202)
    pg.circle(150, 150, 46, lw=TH)
    cumulus(pg, 430, 110, 180, rng)
    # limestone islands on the horizon
    pg.line([(-10, 340), (610, 340)], lw=TH)
    for (x, w, h) in [(120, 140, 150), (230, 90, 110), (470, 170, 190), (580, 80, 90)]:
        karst_island(pg, x, 340, w, h, rng)
    # sea with gentle wave lines
    for k in range(10):
        y = 350 + k * 14
        for _ in range(4):
            x0 = rng.uniform(-20, 560)
            pg.line([(x0, y), (x0 + 20, y - 3), (x0 + 40, y), (x0 + 60, y - 3)], lw=0.7, smooth=True)
    # the shoreline with foam
    shore = sample_smooth([(-20, 500), (120, 492), (260, 506), (420, 494), (620, 504)], 8)
    pg.shape(shore + [(620, 830), (-20, 830)], lw=TH)
    foam = [(x, y + 8) for x, y in shore]
    pg.line(foam, lw=0.8, smooth=True)
    for i in range(0, len(shore), 2):
        x, y = shore[i]
        pg.circle(x + rng.uniform(-4, 4), y + 4, 2.4, lw=0.6)
    # palm leaning over the sand
    coconut_palm(pg, 540, 640, 460, -150, rng, fronds=10)
    # the bangka: slim hull with upturned ends, bamboo outrigger
    hx, hy = 290, 610
    float_ = sample_smooth([(70, 690), (300, 700), (520, 682)], 8)
    pg.union_strokes([(float_, 12)], lw=LW)
    for k in range(0, len(float_), 3):
        x, y = float_[k]
        pg.line([(x, y - 5), (x, y + 5)], lw=0.7)
    for ax in (180, 400):
        arm = sample_smooth([(ax, 610), (ax - 6, 640), (ax - 14, 688)], 6)
        pg.union_strokes([(arm, 8)], lw=TH)
    hull = [(40, 548), (90, 580), (200, 600), (380, 604), (500, 590), (560, 552), (548, 572), (500, 618), (380, 640), (200, 638), (100, 616), (54, 572)]
    pg.shape(hull, smooth=True)
    pg.line([(70, 572), (200, 614), (380, 618), (530, 576)], lw=TH, smooth=True)
    pg.line([(80, 590), (200, 624), (380, 628), (520, 594)], lw=0.8, smooth=True)
    for k in range(7):
        x = 150 + k * 50
        pg.shape([(x, 604 + abs(k - 3) * 0.6), (x + 14, 600), (x + 28, 604 + abs(k - 3) * 0.6), (x + 14, 610)], lw=0.8)
    for ax in (180, 400):
        pg.union_strokes([([(ax - 60, 602), (ax, 598), (ax + 60, 602)], 8)], lw=TH)
    pg.shape([(36, 546), (44, 528), (52, 552)], lw=TH)
    pg.shape([(552, 550), (566, 530), (568, 556)], lw=TH)
    # shells, a starfish, a little crab and footprints
    for (x, y, s, a) in [(80, 760, 18, 10), (470, 760, 16, -20), (230, 790, 14, 30), (560, 730, 15, 0)]:
        shell(pg, x, y, s, a)
    starfish(pg, 380, 760, 30, 15)
    cx, cy = 150, 720
    pg.ellipse(cx, cy, 20, 13)
    for sd in (-1, 1):
        for k in range(3):
            pg.line([(cx + sd * 16, cy + 2 + k * 4), (cx + sd * 30, cy - 2 + k * 6), (cx + sd * 36, cy + 8 + k * 6)], lw=TH, smooth=True)
        pg.shape([(cx + sd * 14, cy - 8), (cx + sd * 30, cy - 22), (cx + sd * 38, cy - 16), (cx + sd * 26, cy - 10)], lw=TH, smooth=True)
        pg.line([(cx + sd * 5, cy - 12), (cx + sd * 7, cy - 22)], lw=TH)
        pg.circle(cx + sd * 7, cy - 24, 2.5, lw=TH)


@ppage("ph-chocolate-hills", "The Chocolate Hills", "summer")
def p_hills(pg):
    rng = random.Random(1203)
    cumulus(pg, 160, 90, 180, rng)
    cumulus(pg, 470, 120, 140, rng)
    mountains(pg, 270, rng)
    # rows of rounded hills, back to front
    rows = [(300, 40, 70, 13), (360, 56, 92, 10), (440, 76, 120, 7), (540, 100, 150, 5)]
    for (base, h, w, n) in rows:
        for k in range(n + 1):
            x = -40 + k * (680 / n) + rng.uniform(-w * 0.2, w * 0.2)
            hh = h * rng.uniform(0.85, 1.15)
            ww = w * rng.uniform(0.85, 1.1)
            pts = [(x - ww / 2 + ww * (i / 20), base - hh * math.sin(math.pi * i / 20) ** 0.8) for i in range(21)]
            pg.shape(pts + [(x + ww / 2, base + 30), (x - ww / 2, base + 30)], lw=TH, smooth=False)
            for _ in range(int(ww / 7)):
                u = rng.uniform(0.12, 0.88)
                px = x - ww / 2 + ww * u
                top = base - hh * math.sin(math.pi * u) ** 0.8
                py = rng.uniform(top + 6, base)
                pg.line([(px, py), (px + rng.uniform(-1.5, 1.5), py - rng.uniform(4, 8))], lw=0.6)
        # trees between the hills
        for _ in range(n):
            tx, ty = rng.uniform(0, 600), base + rng.uniform(2, 14)
            pg.union_circles([(tx + dx, ty - h * 0.12 + dy, r) for dx, dy, r in [(0, 0, h * 0.08), (-h * 0.07, h * 0.03, h * 0.06), (h * 0.07, h * 0.03, h * 0.06)]], lw=0.9)
    # foreground: the branch, leaves and the tarsier
    pg.shape([(-10, 600), (610, 600), (610, 820), (-10, 820)], lw=TH)
    for _ in range(80):
        x, y = rng.uniform(0, 600), rng.uniform(610, 800)
        pg.line([(x, y), (x + rng.uniform(-3, 3), y - rng.uniform(10, 22))], lw=0.7)
    bx = 150
    branch = [(bx - 18, 820), (bx - 14, 600), (bx - 10, 380), (bx - 6, 120), (bx - 2, -10)]
    pg.shape([(bx - 22, 820), (bx - 14, 380), (bx - 10, -10), (bx + 10, -10), (bx + 14, 380), (bx + 22, 820)], smooth=False)
    for k in range(16):
        y = 20 + k * 50 + rng.uniform(-10, 10)
        pg.line([(bx - 10, y), (bx - 4, y + 12), (bx - 8, y + 26)], lw=0.8, smooth=True)
        pg.line([(bx + 8, y + 18), (bx + 4, y + 34)], lw=0.8)
    side = pg.tapered([(bx + 8, 300), (220, 260), (300, 250), (380, 210)], 10, 3, lw=TH)
    for i in range(3, len(side), 4):
        x, y = side[i]
        real_leaf(pg, x, y, rng.uniform(-60, 60) + 180 * (i % 8 < 4), 60, 22, profile="elliptic", veins=5, bend=0.1, stem=6)
    real_leaf(pg, bx + 6, 160, 50, 80, 28, profile="elliptic", veins=6, stem=10)
    real_leaf(pg, bx - 8, 700, -60, 80, 28, profile="elliptic", veins=6, stem=10)
    tarsier(pg, bx + 16, 470, 110, rng)


@ppage("ph-jeepney", "Jeepney Ride", "summer")
def p_jeepney(pg):
    rng = random.Random(1204)
    # street backdrop: a sari-sari store, a wall of bougainvillea, palms
    coconut_palm(pg, 70, 470, 420, 30, rng, fronds=9)
    coconut_palm(pg, 560, 470, 380, -30, random.Random(5), fronds=9)
    pg.shape([(200, 470), (200, 250), (430, 250), (430, 470)])
    for k in range(10):
        pg.line([(200, 270 + k * 20), (430, 270 + k * 20)], lw=0.6)
    awn = [(186, 250), (444, 250), (452, 290), (178, 290)]
    pg.shape(awn)
    for k in range(9):
        x = 186 + k * 29
        pg.line([(x + 4, 250), (x - 2, 290)], lw=TH)
        pg.line([(x - 2, 290), (x + 12, 300), (x + 27, 290)], lw=TH, smooth=True)
    pg.shape([(230, 310), (400, 310), (400, 400), (230, 400)])
    for r in range(3):
        for k in range(9):
            bx, by = 240 + k * 18, 330 + r * 30
            pg.shape([(bx, by + 22), (bx, by + 6), (bx + 3, by), (bx + 7, by), (bx + 10, by + 6), (bx + 10, by + 22)], lw=0.7)
    pg.line([(230, 400), (400, 400)], lw=TH)
    for x in range(-10, 620, 4):
        pass
    for _ in range(36):
        x = rng.choice([rng.uniform(0, 190), rng.uniform(440, 600)])
        y = rng.uniform(300, 460)
        flower(pg, x, y, rng.uniform(9, 13), n=3, wr=0.9, kind="round", center=0.15, a0=rng.uniform(0, 120))
    for _ in range(26):
        x = rng.choice([rng.uniform(0, 190), rng.uniform(440, 600)])
        y = rng.uniform(300, 460)
        real_leaf(pg, x, y, rng.uniform(0, 360), 18, 8, profile="ovate", veins=-1, lw=0.8)
    pg.line([(-10, 470), (610, 470)], lw=LW)
    # road
    pg.line([(-10, 700), (610, 700)], lw=TH)
    for k in range(6):
        pg.shape([(k * 110 + 10, 750), (k * 110 + 70, 750), (k * 110 + 70, 758), (k * 110 + 10, 758)], lw=TH)
    # the jeepney (side view, facing left)
    Y = 630
    wheel(pg, 135, Y, 42)
    wheel(pg, 470, Y, 42)
    def arch(cx_, r, a0=0, a1=180):
        return [(cx_ + r * math.cos(math.radians(a)), Y + 4 - r * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 10)]
    body = [(40, 612), (40, 560), (60, 520), (175, 510), (195, 440), (230, 420), (560, 420), (566, 612)] + arch(470, 54) + arch(135, 54)
    pg.shape(body, smooth=False)
    # curved fenders over the wheels
    for wx in (135, 470):
        pg.line([(wx + 64 * math.cos(math.radians(a)), Y + 4 - 64 * math.sin(math.radians(a))) for a in range(0, 181, 10)], lw=TH, smooth=True)
    # roof with overhang and rack
    pg.shape([(220, 404), (572, 404), (572, 422), (220, 422)])
    for k in range(9):
        pg.line([(240 + k * 40, 404), (240 + k * 40, 390)], lw=TH)
    pg.line([(230, 390), (565, 390)], lw=TH)
    # windshield and side windows
    pg.shape([(180, 512), (198, 446), (230, 432), (232, 512)])
    for k in range(7):
        x = 250 + k * 44
        pg.shape([(x, 436), (x + 36, 436), (x + 36, 486), (x, 486)])
        pg.line([(x, 452), (x + 36, 452)], lw=0.6)
    # chrome strips, painted panels with swirls and stars
    for y in (494, 502, 578):
        pg.line([(60, y + (12 if y > 560 else 30)), (560, y)], lw=0.9) if False else pg.line([(232 if y < 560 else 44, y), (562, y)], lw=TH)
    panel = [(240, 510), (550, 510), (550, 570), (240, 570)]
    pg.shape(panel, lw=TH)
    pg.clip_begin(d_poly(panel))
    for k in range(6):
        cx = 265 + k * 55
        pg.line([(cx - 20, 540), (cx - 8, 522), (cx + 8, 528), (cx + 6, 544), (cx - 6, 548), (cx - 6, 538), (cx + 2, 536)], lw=0.9, smooth=True)
        star(pg, cx + 22, 556, 7, lw=0.8)
    pg.clip_end()
    pg.shape([(300, 516), (490, 516), (490, 534), (300, 534)], lw=TH)
    pg.raw('<text x="395" y="530" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-style="italic" fill="none" stroke="#3a312a" stroke-width="0.9" letter-spacing="2">Mabuhay</text>')
    # hood with chrome horses, grille, bumper and headlight
    pg.line([(60, 520), (175, 510)], lw=TH)
    for k in range(5):
        pg.line([(70 + k * 18, 528), (70 + k * 18, 556)], lw=0.8)
    chrome_horse(pg, 95, 518, 40, flip=-1)
    chrome_horse(pg, 140, 514, 40, flip=-1)
    pg.shape([(28, 560), (44, 560), (44, 606), (28, 606)], lw=TH)
    pg.circle(48, 548, 12)
    pg.circle(48, 548, 7, lw=TH)
    pg.shape([(22, 606), (80, 606), (80, 618), (22, 618)])
    # side mirror, antenna flags, mud flap, rear step
    pg.line([(196, 470), (172, 462)], lw=TH)
    pg.shape([(160, 452), (174, 452), (174, 472), (160, 472)], lw=TH)
    pg.line([(70, 518), (64, 440)], lw=TH)
    pg.shape([(64, 440), (40, 446), (64, 454)], lw=TH)
    pg.shape([(530, 612), (548, 612), (548, 664), (530, 664)], lw=TH)
    pg.shape([(560, 600), (590, 600), (590, 614), (560, 614)], lw=TH)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in PH2:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("ph2"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
