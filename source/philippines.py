"""Philippine pages: the carabao, rice terraces, coconut palms, a bahay kubo, a salakot."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import real_leaf, FINE
from realgirls import strands, cumulus, A, long_hair_back
from realgirls2 import limb

PH = []


def ppage(pid, title, season):
    def deco(fn):
        PH.append((pid, title, season, fn))
        return fn
    return deco


# ------------------------------------------------------------- carabao
BODY = [(0.0, -1.02), (0.4, -0.95), (0.9, -0.93), (1.3, -0.96), (1.6, -0.92), (1.82, -0.84), (1.95, -0.7),
        (2.02, -0.45), (2.0, -0.15), (1.92, 0.1), (1.9, 0.35), (1.94, 0.6), (1.89, 0.85), (1.88, 1.0), (1.91, 1.1),
        (1.64, 1.1), (1.66, 0.98), (1.65, 0.72), (1.6, 0.5), (1.5, 0.38), (1.25, 0.42), (0.9, 0.47), (0.56, 0.43),
        (0.43, 0.46), (0.41, 0.76), (0.42, 1.0), (0.45, 1.1), (0.12, 1.1), (0.15, 1.0), (0.13, 0.72), (0.09, 0.46),
        (-0.03, 0.34), (-0.2, 0.18), (-0.4, 0.05), (-0.6, -0.02), (-0.84, 0.06), (-1.02, 0.14), (-1.16, 0.1),
        (-1.23, -0.02), (-1.21, -0.18), (-1.12, -0.38), (-0.98, -0.56), (-0.82, -0.7), (-0.66, -0.8), (-0.45, -0.9), (-0.22, -0.99)]
HORN_OUT = [(-0.8, -0.78), (-0.76, -1.0), (-0.57, -1.22), (-0.27, -1.37), (0.04, -1.39), (0.22, -1.31), (0.3, -1.18)]
HORN_IN = [(-0.56, -0.76), (-0.58, -0.88), (-0.48, -1.03), (-0.3, -1.17), (-0.07, -1.25), (0.13, -1.23), (0.3, -1.18)]


def carabao(pg, x, y, s, rng, flip=1, egret=False, head_down=0.0):
    """A water buffalo in side view, facing left (flip=-1 faces right). x, y = point under the shoulder at the ground."""
    T = lambda pts: [(x + px * s * flip, y + (py - 1.1) * s) for px, py in pts]
    # far legs, slightly offset and shaded with a line
    far_front = [(0.26, 0.4), (0.52, 0.42), (0.54, 0.74), (0.55, 1.0), (0.58, 1.08), (0.3, 1.08), (0.31, 0.98), (0.28, 0.7)]
    far_hind = [(1.42, 0.3), (1.7, 0.32), (1.8, 0.58), (1.76, 0.9), (1.79, 1.06), (1.54, 1.06), (1.55, 0.92), (1.54, 0.64), (1.46, 0.46)]
    pg.shape(T(far_front), smooth=True, lw=TH)
    pg.shape(T(far_hind), smooth=True, lw=TH)
    # tail
    tail = sample_smooth([(1.92, -0.68), (2.0, -0.4), (2.02, 0.0), (2.0, 0.32)], 8)
    pg.union_strokes([(T(tail), 0.045 * s)], lw=TH)
    tuft = [(1.96, 0.28), (2.06, 0.3), (2.07, 0.48), (2.0, 0.56), (1.95, 0.46)]
    pg.shape(T(tuft), smooth=True, lw=TH)
    for k in range(3):
        pg.line(T([(1.99 + k * 0.02, 0.34), (1.98 + k * 0.025, 0.52)]), lw=0.7)
    # far horn (a little behind)
    far_horn = [(-0.5, -0.8), (-0.42, -1.0), (-0.2, -1.16), (0.08, -1.2), (0.28, -1.12), (0.34, -1.02), (0.16, -1.06), (-0.08, -1.06), (-0.28, -0.96), (-0.4, -0.82)]
    pg.shape(T(far_horn), smooth=True, lw=TH)
    # body
    body = T(BODY)
    pg.shape(body, smooth=True)
    # hide texture: sparse short hairs, skin folds and muscle lines
    pg.clip_begin(d_smooth(body))
    for _ in range(int(140)):
        px, py = rng.uniform(-0.9, 1.9), rng.uniform(-0.9, 0.36)
        if px < -0.5 and py > -0.2:
            continue
        pg.line(T([(px, py), (px + 0.025, py + 0.04)]), lw=0.6)
    pg.clip_end()
    for k, xx in enumerate((-0.42, -0.3, -0.18)):
        pg.line(T([(xx, -0.78 + k * 0.03), (xx - 0.04, -0.45), (xx + 0.02, -0.1)]), lw=0.9, smooth=True)
    pg.line(T([(-0.3, -0.05), (-0.1, 0.05), (0.05, 0.15)]), lw=0.9, smooth=True)          # dewlap fold
    pg.line(T([(0.12, -0.75), (0.2, -0.4), (0.18, 0.2)]), lw=0.9, smooth=True)            # shoulder
    pg.line(T([(0.45, -0.3), (0.7, -0.25), (1.0, -0.28)]), lw=0.8, smooth=True)           # ribs
    pg.line(T([(0.5, -0.12), (0.8, -0.08), (1.1, -0.12)]), lw=0.8, smooth=True)
    pg.line(T([(0.55, 0.12), (0.9, 0.18), (1.2, 0.12)]), lw=0.8, smooth=True)
    pg.line(T([(0.6, 0.3), (0.9, 0.36), (1.2, 0.3)]), lw=0.8, smooth=True)
    pg.line(T([(1.45, -0.75), (1.55, -0.4), (1.5, 0.15)]), lw=0.9, smooth=True)           # thigh
    pg.line(T([(1.75, -0.6), (1.8, -0.2)]), lw=0.8, smooth=True)
    for (lx, ly) in [(0.27, 0.66), (1.8, 0.62)]:                                          # knee / hock creases
        pg.line(T([(lx - 0.06, ly), (lx + 0.06, ly + 0.02)]), lw=0.8)
    for hx in (0.28, 1.77):                                                                 # cloven hooves
        pg.line(T([(hx, 1.0), (hx - 0.01, 1.1)]), lw=0.9)
        pg.line(T([(hx - 0.1, 1.0), (hx + 0.1, 1.0)]), lw=0.8)
    # head details
    pg.ellipse(*T([(-0.88, -0.52)])[0], 0.05 * s, 0.034 * s, -20 * flip)
    pg.circle(*T([(-0.89, -0.525)])[0], 0.018 * s, lw=0.1, fill=INK)
    pg.line(T([(-0.97, -0.56), (-0.88, -0.59), (-0.79, -0.56)]), lw=0.8, smooth=True)
    pg.ellipse(*T([(-1.17, -0.1)])[0], 0.04 * s, 0.026 * s, 30 * flip, lw=TH)
    pg.line(T([(-1.2, 0.04), (-1.08, 0.08), (-0.96, 0.05)]), lw=0.9, smooth=True)    # mouth
    pg.line(T([(-1.1, -0.3), (-1.14, -0.18)]), lw=0.8)
    pg.line(T([(-1.02, -0.4), (-0.96, -0.2), (-0.9, 0.0)]), lw=0.8, smooth=True)      # cheek
    pg.line(T([(-1.2, -0.02), (-1.12, 0.0)]), lw=0.8)
    # ear, sticking out sideways under the horn
    ear = [(-0.66, -0.66), (-0.5, -0.72), (-0.32, -0.68), (-0.24, -0.6), (-0.38, -0.57), (-0.56, -0.58)]
    pg.shape(T(ear), smooth=True)
    pg.line(T([(-0.6, -0.64), (-0.34, -0.63)]), lw=0.8, smooth=True)
    # near horn: big crescent sweeping back, with growth ridges
    hP = T(HORN_OUT + list(reversed(HORN_IN))[1:])
    pg.shape(hP, smooth=True)
    o = sample_smooth(HORN_OUT, 4)
    i_ = sample_smooth(HORN_IN, 4)
    for k in range(1, len(o) - 2):
        a, b = o[k], i_[k]
        m = ((a[0] + b[0]) / 2 + 0.015, (a[1] + b[1]) / 2 + 0.01)
        pg.line(T([a, m, b]), lw=0.7, smooth=True)
    # forehead tuft
    for k in range(5):
        pg.line(T([(-0.66 + k * 0.03, -0.72), (-0.7 + k * 0.03, -0.62)]), lw=0.7)
    if egret:
        bx, by = T([(0.95, -0.94)])[0]
        e = s / 100
        pg.shape([(bx - 18 * e, by - 4 * e), (bx - 6 * e, by - 22 * e), (bx + 18 * e, by - 24 * e), (bx + 30 * e, by - 14 * e), (bx + 20 * e, by - 2 * e)], smooth=True)
        neck = [(bx - 10 * e, by - 14 * e), (bx - 20 * e, by - 22 * e), (bx - 18 * e, by - 32 * e), (bx - 12 * e, by - 38 * e)]
        pg.union_strokes([(sample_smooth(neck, 8), 9 * e)], lw=TH)
        pg.ellipse(bx - 13 * e, by - 42 * e, 7 * e, 5.5 * e)
        pg.shape([(bx - 18 * e, by - 44 * e), (bx - 38 * e, by - 41 * e), (bx - 18 * e, by - 39 * e)], lw=TH)
        pg.circle(bx - 14 * e, by - 43 * e, 1.3 * e, lw=0.1, fill=INK)
        for k in range(4):
            pg.line([(bx - 6 * e - k * 3 * e, by - 46 * e), (bx + 2 * e - k * 2 * e, by - 52 * e)], lw=0.6)
        for k in range(3):
            pg.line([(bx + k * 6 * e, by - 18 * e), (bx + 10 * e + k * 6 * e, by - 10 * e)], lw=0.7)
        pg.line([(bx + 2 * e, by - 2 * e), (bx + 3 * e, by + 8 * e)], lw=TH)
        pg.line([(bx + 8 * e, by - 2 * e), (bx + 9 * e, by + 8 * e)], lw=TH)
    return body


# ---------------------------------------------------------- vegetation
def coconut_palm(pg, x, y, h, lean, rng, fronds=9):
    pts = [(x, y), (x + lean * 0.2, y - h * 0.35), (x + lean * 0.6, y - h * 0.7), (x + lean, y - h)]
    sp = pg.tapered(pts, 22, 14, lw=LW)
    for i in range(2, len(sp) - 1, 2):
        (x0, y0), (x1, y1) = sp[i - 1], sp[i + 1]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        w = 10 - 3 * i / len(sp)
        cx_, cy_ = sp[i]
        pg.line([(cx_ - nx * w, cy_ - ny * w), (cx_ + dx / n * 3, cy_ + dy / n * 3), (cx_ + nx * w, cy_ + ny * w)], lw=0.8, smooth=True)
    tx, ty = x + lean, y - h
    # coconuts
    for (dx, dy) in [(-10, 10), (8, 12), (0, 22), (-16, 22)]:
        pg.circle(tx + dx, ty + dy, 10)
    # fronds: arching rachis with drooping leaflets
    for k in range(fronds):
        a = math.radians(-170 + k * (160 / (fronds - 1)) + rng.uniform(-8, 8))
        L = h * rng.uniform(0.42, 0.55)
        droop = 0.55 + 0.4 * abs(math.cos(a))
        p1 = (tx + L * 0.5 * math.cos(a), ty + L * 0.5 * math.sin(a) - L * 0.12)
        p2 = (tx + L * math.cos(a), ty + L * math.sin(a) + L * droop * 0.5)
        rach = sample_smooth([(tx, ty), p1, p2], 14)
        for i in range(2, len(rach) - 1):
            (x0, y0), (x1, y1) = rach[i - 1], rach[i + 1]
            dx, dy = x1 - x0, y1 - y0
            n = math.hypot(dx, dy) or 1
            ux, uy = dx / n, dy / n
            ll = 34 * math.sin(math.pi * i / len(rach)) ** 0.6 + 6
            for sd in (-1, 1):
                nx, ny = -uy * sd, ux * sd
                bx, by = rach[i]
                ex, ey = bx + (nx * 0.55 + ux * 0.4) * ll, by + (ny * 0.55 + uy * 0.4) * ll + ll * 0.45
                mx, my = (bx + ex) / 2 + nx * 3, (by + ey) / 2 - 2
                pg.shape([(bx, by), (mx + ux * 2.5, my + uy * 2.5), (ex, ey), (mx - ux * 2.5, my - uy * 2.5)], lw=0.8, smooth=True)
        pg.line(rach, lw=TH, smooth=True)


def rice_tuft(pg, x, y, h, rng, lw=0.8):
    for k in range(6):
        a = -50 + 100 * k / 5 + rng.uniform(-8, 8)
        tip = (x + h * math.sin(math.radians(a)) * 0.7, y - h * math.cos(math.radians(a * 0.6)))
        mid = (x + (tip[0] - x) * 0.35, y - h * 0.55)
        pg.line([(x, y), mid, tip], lw=lw, smooth=True)


def terraces(pg, y0, y1, rng, steps=7):
    """Stepped rice terraces climbing a hillside: each step is a curved wall with a band of rice."""
    for i in range(steps):
        t = i / steps
        yb = y0 + (y1 - y0) * t
        amp = 18 + 10 * t
        ph = rng.uniform(0, 3)
        top = [(x, yb + amp * math.sin(x / 120 + ph) + 6 * math.sin(x / 37 + i)) for x in range(-20, 640, 30)]
        P = sample_smooth(top, 6)
        pg.shape(P + [(640, 830), (-40, 830)], lw=TH)
        wall = [(px, py + 8 + 4 * t) for px, py in P]
        pg.line(wall, lw=0.8, smooth=True)
        step_h = (y1 - y0) / steps
        for j in range(0, len(P), 3):
            px, py = P[j]
            if rng.random() < 0.85:
                rice_tuft(pg, px + rng.uniform(-8, 8), py + 8 + step_h * 0.75, 6 + 6 * t, rng, lw=0.6)


def mountains(pg, y, rng):
    pts = [(-20, y + 40)]
    x = -20
    while x < 640:
        x += rng.uniform(60, 120)
        pts.append((x, y - rng.uniform(40, 120)))
        x += rng.uniform(40, 90)
        pts.append((x, y + rng.uniform(-10, 20)))
    pts.append((640, y + 40))
    P = sample_smooth(pts, 6)
    pg.shape(P + [(640, 600), (-20, 600)], lw=TH)
    for i in range(1, len(pts) - 1, 2):
        px, py = pts[i]
        pg.line([(px, py + 6), (px - 20, py + 40), (px - 30, py + 70)], lw=0.8, smooth=True)
        pg.line([(px + 6, py + 10), (px + 18, py + 46)], lw=0.8, smooth=True)


def bahay_kubo(pg, x, y, s, rng):
    """A nipa hut on stilts: bamboo walls, thatched roof, a ladder and a window."""
    T = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    for xx in (-0.85, -0.3, 0.3, 0.85):
        pg.shape(T([(xx - 0.05, 0), (xx - 0.05, -0.55), (xx + 0.05, -0.55), (xx + 0.05, 0)]), lw=TH)
    pg.shape(T([(-1.0, -0.55), (1.0, -0.55), (1.0, -0.62), (-1.0, -0.62)]), lw=TH)
    wall = T([(-0.9, -0.62), (0.9, -0.62), (0.9, -1.35), (-0.9, -1.35)])
    pg.shape(wall)
    pg.clip_begin(d_poly(wall))
    for k in range(40):
        xx = -0.9 + k * 0.045
        pg.line(T([(xx, -0.62), (xx, -1.35)]), lw=0.6)
    pg.clip_end()
    win = T([(0.15, -0.85), (0.6, -0.85), (0.6, -1.18), (0.15, -1.18)])
    pg.shape(win)
    pg.line(T([(0.375, -0.85), (0.375, -1.18)]), lw=TH)
    pg.shape(T([(0.1, -1.18), (0.65, -1.18), (0.72, -1.3), (0.03, -1.3)]), lw=TH)
    door = T([(-0.65, -0.62), (-0.25, -0.62), (-0.25, -1.15), (-0.65, -1.15)])
    pg.shape(door)
    pg.line(T([(-0.45, -0.62), (-0.45, -1.15)]), lw=0.8)
    roof = T([(-1.35, -1.25), (0, -2.2), (1.35, -1.25), (1.2, -1.2), (0, -2.0), (-1.2, -1.2)])
    roofF = T([(-1.38, -1.22), (-0.05, -2.25), (1.38, -1.22), (1.3, -1.12), (-1.3, -1.12)])
    pg.shape(roofF, smooth=False)
    pg.clip_begin(d_poly(roofF))
    for k in range(70):
        xx = -1.4 + k * 0.04
        pg.line(T([(xx, -1.12), (xx * 0.1, -2.2)]), lw=0.5)
    for r in range(4):
        yy = -1.3 - r * 0.22
        pg.line(T([(-1.4, yy), (1.4, yy)]), lw=0.8)
    pg.clip_end()
    pg.shape(roofF, smooth=False, fill="none")
    for k in range(18):
        xx = -1.3 + k * 0.152
        pg.line(T([(xx, -1.12), (xx + 0.02, -1.04)]), lw=0.7)
    # bamboo ladder
    pg.line(T([(-0.62, 0.0), (-0.52, -0.62)]), lw=TH)
    pg.line(T([(-0.3, 0.0), (-0.24, -0.62)]), lw=TH)
    for k in range(4):
        t = 0.15 + k * 0.22
        pg.line(T([(-0.62 + 0.1 * t, -0.62 * t), (-0.3 + 0.06 * t, -0.62 * t)]), lw=TH)


def sampaguita(pg, x, y, r, rng):
    """Sampaguita (Arabian jasmine): a small many-petalled white star flower."""
    for layer, (n, rr, off) in enumerate([(8, 1.0, 0), (6, 0.62, 30)]):
        for i in range(n):
            a = off + i * 360 / n + rng.uniform(-5, 5)
            out = leaf_geom(r * rr, r * rr * 0.32, "ovate", n=10)
            pg.shape(tf(out, x, y, a), lw=0.8)
    pg.circle(x, y, r * 0.15, lw=0.8)


# ================================================================ pages
@ppage("ph-carabao-terraces", "Carabao in the Rice Terraces", "summer")
def p_carabao(pg):
    rng = random.Random(1101)
    cumulus(pg, 130, 90, 170, rng)
    cumulus(pg, 470, 70, 140, rng)
    mountains(pg, 250, rng)
    terraces(pg, 250, 470, rng, steps=7)
    bahay_kubo(pg, 470, 330, 34, rng)
    coconut_palm(pg, 70, 560, 360, 40, rng)
    coconut_palm(pg, 560, 600, 400, -50, rng)
    coconut_palm(pg, 600, 520, 300, -20, random.Random(3))
    # flooded paddy in front with rows of young rice
    pg.shape([(-20, 500), (640, 500), (640, 830), (-20, 830)], lw=TH)
    for r in range(6):
        y = 530 + r * 46
        for k in range(16):
            x = 10 + k * 40 + (20 if r % 2 else 0)
            if 140 < x < 470 and 560 < y < 740:
                continue
            rice_tuft(pg, x, y, 14 + r * 3, rng)
            pg.line([(x - 10, y + 3), (x + 10, y + 3)], lw=0.6)
    # the carabao, with an egret on its back
    carabao(pg, 230, 720, 118, rng, flip=1, egret=True)
    # water ripples around its legs
    for (lx, ly) in [(230 + 0.28 * 118, 720), (230 + 1.77 * 118, 720)]:
        for k in range(2):
            w = 18 + k * 12
            pg.line([(lx - w, ly + 3 + k * 6), (lx - w * 0.3, ly + 6 + k * 7)], lw=0.8, smooth=False)
            pg.line([(lx + w * 0.3, ly + 6 + k * 7), (lx + w, ly + 3 + k * 6)], lw=0.8, smooth=False)
    for k in range(6):
        y = 740 + k * 10
        pg.line([(200 + rng.uniform(-20, 20), y), (260 + k * 30, y)], lw=0.7)


@ppage("ph-salakot-sunset", "Going Home with the Carabao", "summer")
def p_salakot(pg):
    rng = random.Random(1102)
    # big setting sun with rays, palm silhouettes, mountains
    sx, sy = 300, 300
    for i in range(26):
        a = math.radians(180 + i * 180 / 25)
        pg.line([(sx + 90 * math.cos(a), sy + 90 * math.sin(a)), (sx + 700 * math.cos(a), sy + 700 * math.sin(a))], lw=0.8)
    pg.circle(sx, sy, 80)
    for k in range(4):
        pg.line([(sx - 76 + k * 6, sy + 30 + k * 12), (sx + 76 - k * 6, sy + 30 + k * 12)], lw=0.8)
    cumulus(pg, 110, 140, 150, rng)
    cumulus(pg, 500, 170, 120, rng)
    mountains(pg, 330, rng)
    bahay_kubo(pg, 470, 400, 26, rng)
    coconut_palm(pg, 520, 420, 220, 20, rng, fronds=8)
    coconut_palm(pg, 90, 420, 250, -20, rng, fronds=8)
    # paddies with dikes leading into the distance
    pg.shape([(-20, 400), (640, 400), (640, 830), (-20, 830)], lw=TH)
    for y in (430, 470, 530, 610):
        pg.line([(-20, y), (640, y + 6)], lw=0.9)
    dike = [(330, 830), (318, 600), (300, 470), (290, 400)]
    pg.shape([(250, 830), (296, 400), (302, 400), (420, 830)], lw=TH)
    for k in range(14):
        y = 410 + k * 30
        t = (y - 400) / 430
        pg.line([(296 - 46 * t, y), (302 + 118 * t, y + 2)], lw=0.6)
    for r in range(5):
        y = 450 + r * 70
        for k in range(14):
            x = 10 + k * 46 + (23 if r % 2 else 0)
            t = (y - 400) / 430
            if 250 - 10 < x < 420 + 10 and y > 420:
                if (296 - 46 * t) - 10 < x < (302 + 118 * t) + 10:
                    continue
            rice_tuft(pg, x, y, 10 + r * 5, rng)
    # the carabao walking in the paddy beside the dike, facing away to the right side
    carabao(pg, 488, 650, 76, rng, flip=-1)
    # her, seen from behind, in a salakot, holding the rope
    cx = 300
    # long skirt (patadyong pattern)
    skirt = [(cx - 44, 610), (cx + 44, 610), (cx + 58, 700), (cx + 64, 780), (cx - 64, 780), (cx - 58, 700)]
    pg.shape(skirt, smooth=True)
    pg.clip_begin(d_smooth(skirt))
    for k in range(-6, 7):
        pg.line([(cx + k * 14, 600), (cx + k * 18, 790)], lw=0.8)
    for y in range(620, 790, 22):
        pg.line([(cx - 80, y), (cx + 80, y)], lw=0.8)
        pg.line([(cx - 80, y + 4), (cx + 80, y + 4)], lw=0.6)
    pg.clip_end()
    pg.shape(skirt, smooth=True, fill="none")
    for sd in (-1, 1):
        pg.shape([(cx + sd * 24 - 12, 780), (cx + sd * 24 + 12, 780), (cx + sd * 24 + 14, 796), (cx + sd * 24 - 14, 796)], lw=TH)
    # arms: left relaxed, right holding the rope
    limb(pg, [(cx - 44, 520), (cx - 56, 580), (cx - 56, 626)], 22)
    pg.ellipse(cx - 56, 636, 9, 12)
    limb(pg, [(cx + 44, 520), (cx + 70, 572), (cx + 96, 600)], 22)
    pg.ellipse(cx + 104, 604, 10, 11)
    rope = sample_smooth([(cx + 104, 604), (cx + 140, 640), (cx + 180, 620), (430 - 1.08 * 100 * -1 - 210, 640)], 10)
    mx, my = 488 + 1.2 * 76, 650 + (-0.05 - 1.1) * 76
    pg.line([(cx + 104, 604), (cx + 150, 640), (cx + 240, 620), (mx, my)], lw=TH, smooth=True)
    # blouse (baro) with loose sleeves
    blouse = [(cx - 24, 500), (cx - 50, 508), (cx - 56, 560), (cx - 48, 616), (cx + 48, 616), (cx + 56, 560), (cx + 50, 508), (cx + 24, 500)]
    pg.shape(blouse, smooth=True)
    for k in range(-2, 3):
        pg.line([(cx + k * 16, 520), (cx + k * 20, 612)], lw=0.8, smooth=True)
    for sd in (-1, 1):
        pg.shape([(cx + sd * 42, 506), (cx + sd * 60, 512), (cx + sd * 66, 544), (cx + sd * 48, 548)], smooth=True)
        pg.line([(cx + sd * 50, 512), (cx + sd * 56, 544)], lw=0.7)
    # long hair under the hat
    long_hair_back(pg, cx, 440, 50, 3.0, rng, locks=6, width=0.7)
    # salakot: a wide conical woven hat
    hy = 450
    rim = 96
    cone = [(cx - rim, hy), (cx, hy - 62), (cx + rim, hy), (cx + rim * 0.6, hy + 14), (cx, hy + 18), (cx - rim * 0.6, hy + 14)]
    pg.shape(cone, smooth=False)
    pg.clip_begin(d_poly(cone))
    for k in range(-14, 15):
        pg.line([(cx, hy - 62), (cx + k * 8, hy + 20)], lw=0.6)
    for r in range(1, 8):
        t = r / 8
        pg.line([(cx - rim * t, hy - 62 + 62 * t), (cx, hy - 62 + 80 * t), (cx + rim * t, hy - 62 + 62 * t)], lw=0.7, smooth=True)
    pg.clip_end()
    pg.shape(cone, smooth=False, fill="none")
    pg.circle(cx, hy - 62, 5)
    # sampaguita garland around her wrist and a few blooms in the foreground grass
    for k in range(5):
        a = k * 2 * math.pi / 5
        sampaguita(pg, cx - 56 + 11 * math.cos(a), 626 + 6 * math.sin(a), 5, rng)
    for (x, y) in [(60, 760), (90, 790), (40, 800), (560, 770), (590, 800), (530, 800)]:
        real_leaf(pg, x - 8, y + 10, -40, 26, 10, profile="ovate", veins=2)
        sampaguita(pg, x, y, 13, rng)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in PH:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("ph"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
