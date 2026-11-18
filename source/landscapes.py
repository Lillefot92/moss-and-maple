"""Realistic landscape pages for Moss & Maple."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import real_leaf, fern_frond, moss, FINE
from realgirls import spruce_tree, birch, cumulus, chamomile, cornflower, grass_head, poppy

LS = []


def lpage(pid, title, season):
    def deco(fn):
        LS.append((pid, title, season, fn))
        return fn
    return deco


# ------------------------------------------------------------------ helpers
def tree_line(pg, y, h, w, rng, step=None, snow=False, tiers=6, x0=-30, x1=640):
    step = step or w * 0.55
    x = x0
    while x < x1:
        spruce_tree(pg, x + rng.uniform(-step * 0.2, step * 0.2), y, h * rng.uniform(0.75, 1.15), w * rng.uniform(0.85, 1.1), rng, snow=snow, tiers=tiers)
        x += step


def mist_band(pg, y, rng, amp=6):
    pts = [(x, y + amp * math.sin(x / 70 + rng.uniform(0, 0.3))) for x in range(-20, 640, 30)]
    P = sample_smooth(pts, 6)
    pg.shape(P + [(640, y + 60), (-20, y + 60)], lw=TH)
    for k in range(3):
        x0 = rng.uniform(0, 450)
        pg.line([(x0, y + 14 + k * 12), (x0 + 60, y + 10 + k * 12), (x0 + 140, y + 15 + k * 12)], lw=0.7, smooth=True)


def reflection(pg, x, y, h, w, rng):
    """Broken horizontal strokes that echo a tree in still water."""
    for k in range(int(h / 7)):
        t = k * 7 / h
        ww = w * 0.5 * (1 - t) * rng.uniform(0.5, 1.0)
        yy = y + 4 + k * 7
        if ww > 2:
            pg.line([(x - ww, yy), (x + ww, yy)], lw=0.7)


def lily_pad(pg, x, y, r, ang, rng):
    pts = []
    for i in range(41):
        a = math.radians(ang + 14 + i * (332 / 40))
        pts.append((x + r * math.cos(a), y + r * 0.42 * math.sin(a)))
    pg.shape([(x, y)] + pts, lw=TH, smooth=False)
    for k in range(6):
        a = math.radians(ang + 40 + k * 55)
        pg.line([(x, y), (x + r * 0.85 * math.cos(a), y + r * 0.36 * math.sin(a))], lw=0.6)


def water_lily(pg, x, y, r, rng):
    for layer, (n, rr, lift) in enumerate([(8, 1.0, 0.25), (6, 0.75, 0.55), (5, 0.5, 0.8)]):
        for i in range(n):
            a = math.radians(i * 360 / n + layer * 20 + rng.uniform(-6, 6))
            tip = (x + r * rr * math.cos(a), y + r * rr * 0.4 * math.sin(a) - r * lift * 0.6)
            w = r * 0.18 * rr
            base = (x, y)
            nx, ny = -math.sin(a), math.cos(a) * 0.4
            pg.shape([(base[0] + nx * w * 0.4, base[1] + ny * w * 0.4), ((base[0] + tip[0]) / 2 + nx * w, (base[1] + tip[1]) / 2 + ny * w - 2),
                      tip, ((base[0] + tip[0]) / 2 - nx * w, (base[1] + tip[1]) / 2 - ny * w - 2), (base[0] - nx * w * 0.4, base[1] - ny * w * 0.4)], lw=TH, smooth=True)
    pg.ellipse(x, y - r * 0.5, r * 0.16, r * 0.1, lw=TH)
    for k in range(8):
        a = k * math.pi / 4
        pg.line([(x, y - r * 0.5), (x + r * 0.2 * math.cos(a), y - r * 0.55 + r * 0.08 * math.sin(a))], lw=0.6)


def cattail(pg, x, y, h, lean, rng):
    pg.line([(x, y), (x + lean * 0.4, y - h * 0.5), (x + lean, y - h)], lw=TH, smooth=True)
    tx, ty = x + lean * 0.88, y - h * 0.88
    pg.shape([(tx - 7, ty + 30), (tx - 8, ty), (tx - 4, ty - 26), (tx + 4, ty - 26), (tx + 8, ty), (tx + 7, ty + 30), (tx, ty + 34)], lw=TH, smooth=True)
    for k in range(6):
        pg.line([(tx - 6, ty - 20 + k * 9), (tx + 6, ty - 18 + k * 9)], lw=0.5)
    for sd in (-1, 1):
        L = h * rng.uniform(0.6, 0.9)
        pts = [(x + sd * 2, y), (x + sd * L * 0.12, y - L * 0.5), (x + sd * L * 0.3, y - L)]
        real_leaf(pg, x + sd * 3, y, sd * rng.uniform(4, 14), L, 5.5, profile="lance", veins=-1, bend=0.15 * sd, lw=TH)


def rowboat(pg, x, y, s, rng):
    T = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    hull = [(-1.0, -0.12), (-0.7, 0.0), (0, 0.06), (0.75, 0.0), (1.05, -0.2), (0.95, 0.06), (0.6, 0.28), (0, 0.33), (-0.6, 0.28), (-0.95, 0.1)]
    pg.shape(T(hull), smooth=True)
    inner = [(-0.9, -0.08), (-0.6, 0.02), (0, 0.07), (0.7, 0.02), (0.96, -0.15), (0.6, -0.08), (0, -0.07), (-0.6, -0.08)]
    pg.shape(T(inner), smooth=True, lw=TH)
    for k in (0.12, 0.2):
        pg.line(T([(-0.92, -0.02 + k), (-0.5, 0.06 + k), (0.2, 0.08 + k), (0.85, -0.02 + k)]), lw=0.8, smooth=True)
    for bx in (-0.35, 0.3):
        pg.shape(T([(bx - 0.07, 0.07), (bx + 0.07, 0.07), (bx + 0.07, -0.06), (bx - 0.07, -0.06)]), lw=TH)
    # oars resting across
    for (a, b) in [((-0.6, -0.25), (0.4, 0.15)), ((-0.4, 0.16), (0.65, -0.2))]:
        pg.union_strokes([(T([a, b]), 0.025 * s)], lw=TH)
        bx2, by2 = T([b])[0]
        pg.ellipse(bx2, by2, 0.12 * s, 0.035 * s, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), lw=TH)
    pg.line(T([(-0.98, -0.1), (-1.3, -0.3)]), lw=TH, smooth=False)


def rock(pg, pts, rng, cracks=3, moss_top=False, lw=LW):
    pg.shape(pts, smooth=True, lw=lw)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    pg.clip_begin(d_smooth(pts))
    for _ in range(cracks):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        L = (x1 - x0) * rng.uniform(0.2, 0.45)
        a = rng.uniform(-0.6, 0.6) + (math.pi / 2 if rng.random() < 0.4 else 0)
        pg.line([(cx, cy), (cx + L * 0.5 * math.cos(a) + rng.uniform(-4, 4), cy + L * 0.5 * math.sin(a)), (cx + L * math.cos(a), cy + L * math.sin(a))], lw=0.8)
    if moss_top:
        for _ in range(int((x1 - x0) / 5)):
            mx = rng.uniform(x0, x1)
            my = y0 + rng.uniform(2, (y1 - y0) * 0.3)
            pg.line([(mx, my), (mx + 2, my - 3)], lw=0.6)
            pg.line([(mx, my), (mx - 2, my - 3)], lw=0.6)
    pg.clip_end()
    pg.shape(pts, smooth=True, fill="none", lw=lw)


def lupine(pg, x, y, h, rng):
    pg.line([(x, y), (x + rng.uniform(-4, 4), y - h)], lw=TH)
    tx, ty = x, y - h
    n = 14
    for k in range(n):
        t = k / n
        py = ty + h * 0.45 * t
        w = 4 + 10 * t
        for sd in (-1, 1):
            if (k + (sd > 0)) % 2:
                continue
            pg.shape([(tx + sd * 1, py), (tx + sd * w, py - 4), (tx + sd * (w + 3), py + 2), (tx + sd * w * 0.6, py + 5)], lw=0.8, smooth=True)
    pg.ellipse(tx, ty - 4, 2.5, 6, lw=0.8)
    # palmate leaf near the base
    lx, ly = x, y - h * 0.18
    for k in range(7):
        a = -150 + k * 20
        real_leaf(pg, lx, ly, a + 90, 30, 4.5, profile="lance", veins=-1, lw=0.8)


def edelweiss(pg, x, y, r, rng):
    pg.line([(x, y + r * 3), (x, y)], lw=TH)
    for i in range(9):
        a = i * 40 + rng.uniform(-6, 6)
        out = leaf_geom(r, r * 0.28, "lance", n=12)
        pg.shape(tf(out, x, y, a), lw=0.8)
        for k in range(3):
            p = tf([(rng.uniform(-r * 0.08, r * 0.08), -r * (0.3 + k * 0.2))], x, y, a)[0]
            pg.line([p, (p[0] + 1.5, p[1] - 1.5)], lw=0.5)
    for (dx, dy) in [(0, 0), (-r * 0.22, -r * 0.1), (r * 0.22, -r * 0.1), (-r * 0.12, r * 0.18), (r * 0.12, r * 0.18)]:
        pg.circle(x + dx, y + dy, r * 0.13, lw=0.8)


def gentian(pg, x, y, s, ang=0):
    pg.line(tf([(0, s * 1.6), (0, 0.2 * s)], x, y, ang), lw=TH)
    for sd in (-1, 1):
        real_leaf(pg, *tf([(0, s * 1.3)], x, y, ang)[0], ang + sd * 50, s * 0.8, s * 0.22, profile="elliptic", veins=-1, lw=0.8)
    trumpet = [(-0.22, 0.2), (-0.3, -0.5), (-0.5, -0.95), (-0.25, -0.88), (0, -1.0), (0.25, -0.88), (0.5, -0.95), (0.3, -0.5), (0.22, 0.2)]
    pg.shape(tf([(px * s, py * s) for px, py in trumpet], x, y, ang), lw=TH, smooth=True)
    for xx in (-0.1, 0.1):
        pg.line(tf([(xx * s, 0.1 * s), (xx * 1.6 * s, -0.8 * s)], x, y, ang), lw=0.6)


def larch(pg, x, base, h, w, rng):
    pg.shape([(x - 4, base), (x - 2, base - h), (x + 2, base - h), (x + 4, base)], lw=TH)
    for k in range(9):
        t = k / 9
        y = base - h * (0.15 + 0.82 * t)
        bw = w / 2 * (1 - t) ** 0.85
        for sd in (-1, 1):
            # a soft tuft of needles: a scalloped clump shape
            pts = [(x, y - 4)]
            for j in range(6):
                u = j / 5
                pts.append((x + sd * bw * u, y - 6 + 4 * u * u - (3 if j % 2 else 0)))
            for j in range(6):
                u = 1 - j / 5
                pts.append((x + sd * bw * u, y + 6 + 5 * u * u + (3 if j % 2 else 0)))
            pg.shape(pts, lw=0.8, smooth=True)
            for j in range(1, 4):
                px = x + sd * bw * j / 4
                pg.line([(px, y - 2), (px + sd * 3, y + 5)], lw=0.5)


# ================================================================= pages
@lpage("ls-misty-lake", "Misty Lake at Dawn", "summer")
def l_lake(pg):
    rng = random.Random(1301)
    sx, sy = 380, 250
    for i in range(18):
        a = math.radians(180 + i * 180 / 17)
        pg.line([(sx + 60 * math.cos(a), sy + 60 * math.sin(a)), (sx + 420 * math.cos(a), sy + 420 * math.sin(a))], lw=0.6)
    pg.circle(sx, sy, 46, lw=TH)
    for (bx, by, s) in [(150, 130, 10), (176, 146, 8), (196, 120, 9)]:
        pg.line([(bx - s, by - s * 0.3), (bx - s * 0.4, by - s * 0.5), (bx, by), (bx + s * 0.4, by - s * 0.5), (bx + s, by - s * 0.3)], lw=TH, smooth=True)
    tree_line(pg, 300, 130, 56, rng, step=24, snow=False, tiers=6)
    mist_band(pg, 280, rng, amp=5)
    tree_line(pg, 340, 170, 72, rng, step=34, snow=False, tiers=7)
    # soft wisps of morning mist
    for (y, x0, x1) in [(318, -20, 220), (326, 260, 520), (334, 120, 640), (346, -20, 300)]:
        pts = sample_smooth([(x0, y + 4), ((x0 + x1) / 2 - 50, y - 5), ((x0 + x1) / 2 + 50, y + 2), (x1, y - 3)], 8)
        pg.line(pts, lw=0.8, smooth=True)
    # still water with tree reflections
    pg.shape([(-20, 360), (640, 360), (640, 830), (-20, 830)], lw=TH)
    for k in range(18):
        x = rng.uniform(-10, 610)
        reflection(pg, x, 360, rng.uniform(60, 110), rng.uniform(40, 70), rng)
    for k in range(4):
        pg.line([(sx - 40 + k * 10, 372 + k * 12), (sx + 40 - k * 10, 372 + k * 12)], lw=0.8)
    # jetty from the bottom left, in perspective
    J = [(-20, 830), (90, 530), (170, 530), (300, 830)]
    pg.shape(J, lw=LW)
    for k in range(16):
        t = (k + 1) / 17
        y = 530 + 300 * t ** 1.4
        xl = 90 - 110 * (y - 530) / 300
        xr = 170 + 130 * (y - 530) / 300
        pg.line([(xl, y), (xr, y)], lw=TH if k % 4 == 0 else 0.8)
        if k % 3 == 0:
            for u in (0.3, 0.7):
                pg.circle(xl + (xr - xl) * u, y - 3, 1.2, lw=0.5)
    for (px, py, w) in [(92, 530, 8), (168, 530, 8), (40, 660, 12), (230, 660, 12)]:
        pg.shape([(px - w / 2, py), (px + w / 2, py), (px + w / 2, py + 46), (px - w / 2, py + 46)], lw=TH)
        pg.line([(px - w, py + 46), (px + w, py + 46)], lw=0.7)
    # the rowboat tied to the jetty
    rowboat(pg, 330, 560, 110, rng)
    pg.line([(205, 560), (240, 570), (220, 550)], lw=0.9, smooth=True)
    # reeds and cattails on the right, lily pads in front
    for k in range(9):
        cattail(pg, 470 + k * 18 + rng.uniform(-6, 6), 700 + rng.uniform(-10, 10), rng.uniform(160, 260), rng.uniform(-30, 20), rng)
    for k in range(3):
        pg.ellipse(330, 594, 130 + k * 26, 14 + k * 5, lw=0.7, fill="none")
    for (x, y, r, a) in [(380, 720, 40, 20), (330, 780, 34, 200), (470, 770, 42, 90), (560, 790, 30, 300), (260, 720, 26, 120),
                         (440, 660, 30, 60), (520, 680, 26, 250), (360, 650, 22, 150), (590, 640, 24, 30), (250, 790, 30, 330)]:
        lily_pad(pg, x, y, r, a, rng)
    for (x, y, r) in [(390, 712, 28), (480, 760, 30), (262, 714, 20), (442, 654, 22), (590, 634, 18)]:
        water_lily(pg, x, y, r, rng)


@lpage("ls-waterfall", "Waterfall in the Mossy Gorge", "spring")
def l_waterfall(pg):
    rng = random.Random(1302)
    # trees on the top edge
    tree_line(pg, 150, 120, 60, rng, step=40, snow=False, tiers=6)
    # rock walls left and right, layered
    left = [[(-20, 140), (140, 150), (190, 260), (170, 330), (-20, 340)], [(-20, 330), (160, 320), (210, 430), (180, 520), (-20, 530)],
            [(-20, 510), (200, 500), (240, 600), (210, 650), (-20, 660)]]
    right = [[(640, 140), (440, 150), (390, 270), (420, 340), (640, 340)], [(640, 330), (420, 320), (370, 440), (400, 520), (640, 530)],
             [(640, 510), (380, 500), (350, 600), (390, 650), (640, 660)]]
    # the falls behind the rocks
    fall = [(240, 150), (360, 150), (390, 620), (210, 620)]
    pg.shape(fall, lw=TH)
    pg.clip_begin(d_poly(fall))
    for k in range(28):
        x = 230 + k * 6 + rng.uniform(-2, 2)
        pg.line([(x, 150), (x + rng.uniform(-6, 6), 380), (x + rng.uniform(-14, 14) + (x - 300) * 0.1, 620)], lw=0.7, smooth=True)
    pg.clip_end()
    for blk in left + right:
        pts = []
        for i in range(len(blk)):
            a, b = blk[i], blk[(i + 1) % len(blk)]
            for k in range(4):
                t = k / 4
                pts.append((a[0] + (b[0] - a[0]) * t + rng.uniform(-7, 7), a[1] + (b[1] - a[1]) * t + rng.uniform(-6, 6)))
        pg.shape(pts, lw=LW)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pg.clip_begin(d_poly(pts))
        for k in range(int((max(ys) - min(ys)) / 16)):
            y = min(ys) + 10 + k * 16
            seg = []
            x = min(xs)
            while x < max(xs):
                seg.append((x, y + rng.uniform(-3, 3)))
                x += rng.uniform(12, 24)
            pg.line(seg, lw=0.7)
        for _ in range(6):
            x, y = rng.uniform(min(xs), max(xs)), rng.uniform(min(ys), max(ys))
            pg.line([(x, y), (x + rng.uniform(-6, 6), y + rng.uniform(10, 22)), (x + rng.uniform(-10, 10), y + rng.uniform(24, 40))], lw=0.8)
        for _ in range(int((max(xs) - min(xs)) / 6)):
            mx = rng.uniform(min(xs), max(xs))
            my = min(ys) + rng.uniform(4, 22)
            pg.line([(mx, my), (mx + 2, my - 4)], lw=0.6)
            pg.line([(mx, my), (mx - 2, my - 4)], lw=0.6)
        pg.clip_end()
        pg.shape(pts, lw=LW, fill="none")
    # ferns growing from the rock ledges
    fern_frond(pg, (160, 330), [(130, 270), (80, 230), (20, 230)], rng, pinnae=14, pmax=46)
    fern_frond(pg, (440, 330), [(480, 280), (540, 250), (600, 260)], rng, pinnae=14, pmax=46)
    fern_frond(pg, (190, 510), [(150, 470), (90, 450), (40, 460)], rng, pinnae=12, pmax=40)
    # foam and pool
    pool = [(-20, 640), (640, 640), (640, 830), (-20, 830)]
    pg.shape(pool, lw=TH)
    for _ in range(60):
        x = rng.gauss(300, 70)
        y = rng.uniform(625, 690)
        pg.circle(x, y, rng.uniform(3, 9), lw=0.8)
    for k in range(8):
        y = 700 + k * 14
        x0 = rng.uniform(40, 380)
        pg.line([(x0, y), (x0 + 50, y - 3), (x0 + 110, y)], lw=0.7, smooth=True)
    # mossy boulders in the pool
    for (x, y, w, h) in [(90, 760, 150, 70), (470, 750, 170, 80), (300, 790, 110, 50), (590, 800, 90, 50)]:
        pts = [(x - w / 2, y + h / 2), (x - w * 0.47, y + h * 0.1), (x - w * 0.36, y - h * 0.3), (x - w * 0.12, y - h * 0.5), (x + w * 0.15, y - h * 0.46),
               (x + w * 0.38, y - h * 0.25), (x + w * 0.48, y + h * 0.05), (x + w / 2, y + h / 2)]
        pg.shape(pts, lw=LW)
        pg.line([(x - w * 0.12, y - h * 0.5), (x - w * 0.02, y - h * 0.1), (x + w * 0.1, y + h * 0.4)], lw=0.8)
        pg.line([(x + w * 0.15, y - h * 0.46), (x + w * 0.2, y - h * 0.1)], lw=0.8)
        for k in range(int(w / 14)):
            mx = x - w * 0.4 + k * 14
            pg.line([(mx, y - h * 0.3), (mx + 3, y - h * 0.42), (mx + 6, y - h * 0.3)], lw=0.7, smooth=True)
    # an overhanging branch with leaves
    sp = pg.tapered([(640, 40), (540, 70), (460, 90), (400, 120)], 12, 4, lw=LW)
    for i in range(2, len(sp), 2):
        x, y = sp[i]
        for _ in range(2):
            real_leaf(pg, x, y, rng.uniform(120, 240), rng.uniform(34, 44), 15, profile="ovate", teeth=12, tooth_amp=0.1, veins=4)


@lpage("ls-red-cottage", "Red Cottage by the Birches", "summer")
def l_cottage(pg):
    rng = random.Random(1303)
    cumulus(pg, 470, 90, 170, rng)
    cumulus(pg, 140, 70, 120, rng)
    # forest edge behind
    tree_line(pg, 360, 150, 60, rng, step=34, snow=False, tiers=6)
    hill(pg, 350, 8, 0.4, 1.0, lw=TH)
    # the cottage
    X0, X1, Y0, Y1 = 230, 520, 290, 470
    pg.shape([(X0, Y1), (X0, Y0), (X1, Y0), (X1, Y1)])
    pg.clip_begin(d_poly([(X0, Y1), (X0, Y0), (X1, Y0), (X1, Y1)]))
    x = X0
    while x < X1:
        pg.line([(x, Y0), (x, Y1)], lw=0.7)
        pg.line([(x + 9, Y0), (x + 9, Y1)], lw=0.5)
        x += 14
    pg.clip_end()
    for xx in (X0, X1 - 12):
        pg.shape([(xx, Y1), (xx, Y0), (xx + 12, Y0), (xx + 12, Y1)])
    # roof with clay tiles and a chimney
    pg.shape([(470, 230), (470, 180), (496, 180), (496, 230)])
    pg.shape([(466, 180), (500, 180), (500, 172), (466, 172)], lw=TH)
    roof = [(X0 - 26, Y0 + 4), (X0 + 40, 200), (X1 - 40, 200), (X1 + 26, Y0 + 4)]
    pg.shape(roof)
    pg.clip_begin(d_poly(roof))
    for r in range(9):
        y = 204 + r * 10
        for k in range(30):
            x = X0 - 30 + k * 12 + (6 if r % 2 else 0)
            pg.line([(x, y), (x + 6, y + 8), (x + 12, y)], lw=0.6, smooth=True)
    pg.clip_end()
    pg.shape(roof, fill="none")
    pg.shape([(X0 - 30, Y0 + 2), (X1 + 30, Y0 + 2), (X1 + 30, Y0 + 10), (X0 - 30, Y0 + 10)], lw=TH)
    # windows with white frames, door with a little porch
    for wx in (262, 430):
        pg.shape([(wx - 6, 324), (wx + 56, 324), (wx + 56, 404), (wx - 6, 404)])
        pg.shape([(wx, 330), (wx + 50, 330), (wx + 50, 398), (wx, 398)], lw=TH)
        pg.line([(wx + 25, 330), (wx + 25, 398)], lw=TH)
        pg.line([(wx, 364), (wx + 50, 364)], lw=TH)
        pg.shape([(wx - 12, 404), (wx + 62, 404), (wx + 62, 412), (wx - 12, 412)], lw=TH)
        for k in range(3):
            fx = wx + 6 + k * 19
            flower(pg, fx, 398, 7, n=5, wr=0.6, kind="round", center=0.25)
    pg.shape([(340, 470), (340, 340), (402, 340), (402, 470)])
    pg.line([(371, 344), (371, 468)], lw=0.8)
    for k in range(4):
        pg.line([(344, 360 + k * 28), (398, 360 + k * 28)], lw=0.6)
    pg.circle(392, 410, 3)
    pg.shape([(326, 340), (416, 340), (424, 326), (318, 326)], lw=TH)
    pg.shape([(330, 470), (412, 470), (418, 482), (324, 482)], lw=TH)
    # flag pole with a long pennant
    pg.line([(570, 470), (570, 150)], lw=LW)
    pg.circle(570, 146, 4)
    pen = [(572, 160), (600, 170), (640, 186), (600, 176), (572, 174)]
    pg.shape(pen, lw=TH, smooth=True)
    pg.line([(572, 167), (612, 176)], lw=0.7)
    # birches on the left with leafy crowns
    for (x, w, top) in [(60, 30, 90), (130, 22, 150), (180, 16, 200)]:
        birch(pg, x, top, 560, w, rng)
    for (x0, y0, x1, y1) in [(60, 150, -10, 90), (60, 120, 150, 60), (130, 200, 210, 150), (130, 180, 70, 230), (180, 240, 230, 210)]:
        sp = sample_smooth([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 10), (x1, y1)], 6)
        pg.line(sp, lw=TH, smooth=True)
        for i in range(1, len(sp), 1):
            x, y = sp[i]
            for _ in range(2):
                real_leaf(pg, x + rng.uniform(-6, 6), y + rng.uniform(-4, 10), rng.uniform(150, 210), rng.uniform(16, 22), 9, profile="ovate", teeth=10, tooth_amp=0.15, veins=2, lw=TH)
    # picket fence
    for k in range(14):
        x = 20 + k * 42
        if 300 < x < 440:
            continue
        pg.shape([(x, 600), (x, 520), (x + 8, 508), (x + 16, 520), (x + 16, 600)], lw=TH)
    pg.shape([(0, 540), (300, 540), (300, 550), (0, 550)], lw=TH)
    pg.shape([(440, 540), (610, 540), (610, 550), (440, 550)], lw=TH)
    pg.shape([(0, 576), (300, 576), (300, 586), (0, 586)], lw=TH)
    pg.shape([(440, 576), (610, 576), (610, 586), (440, 586)], lw=TH)
    # stepping-stone path to the door
    for k in range(6):
        t = k / 5
        x = 371 + (300 - 371) * t * 0.4
        y = 500 + 280 * t
        pg.ellipse(x, y, 18 + 26 * t, 6 + 9 * t, lw=TH)
    # midsummer meadow: lupines, daisies, cornflowers, grasses
    for _ in range(10):
        grass_head(pg, rng.uniform(-10, 610), 830, rng.uniform(140, 220), rng.uniform(-30, 30), rng)
    for x in (40, 75, 110, 520, 555, 590, 260):
        lupine(pg, x + rng.uniform(-6, 6), 830, rng.uniform(150, 220), rng)
    for (x, y) in [(150, 700), (210, 760), (460, 730), (500, 790), (30, 760), (300, 790)]:
        pg.line([(x, 830), (x + 3, y)], lw=TH)
        chamomile(pg, x + 3, y, 18, rng)
    for (x, y) in [(190, 650), (430, 680), (580, 700), (90, 650)]:
        pg.line([(x, 830), (x, y)], lw=TH)
        cornflower(pg, x, y, 16, rng)


@lpage("ls-alpine-meadow", "Alpine Meadow", "autumn")
def l_alpine(pg):
    rng = random.Random(1304)
    cumulus(pg, 120, 80, 140, rng)
    # snowy peaks with ridges
    far = [(-20, 250), (90, 150), (160, 190), (300, 130), (360, 170), (600, 110), (640, 150), (640, 380), (-20, 380)]
    pg.shape(far, lw=TH)
    peaks = [(-20, 330), (60, 200), (130, 250), (230, 90), (330, 230), (400, 170), (480, 120), (560, 210), (640, 260), (640, 380), (-20, 380)]
    pg.shape(peaks, lw=LW)
    pg.clip_begin(d_poly(peaks))
    for _ in range(70):
        x, y = rng.uniform(0, 600), rng.uniform(150, 330)
        L_ = rng.uniform(10, 26)
        pg.line([(x, y), (x + L_ * 0.4, y + L_ * 0.5), (x + L_ * 0.1, y + L_)], lw=0.6)
    pg.clip_end()
    snow = [[(185, 140), (230, 90), (275, 150), (255, 160), (240, 140), (225, 165), (205, 150)],
            [(440, 160), (480, 120), (520, 165), (500, 172), (485, 155), (468, 180), (455, 165)],
            [(40, 225), (60, 200), (85, 222), (70, 232), (58, 222)]]
    for sp in snow:
        pg.shape(sp, lw=TH)
    for (a, b) in [((230, 90), (250, 260)), ((230, 90), (190, 230)), ((480, 120), (470, 270)), ((480, 120), (520, 260)), ((400, 170), (380, 280))]:
        pts = [a, ((a[0] + b[0]) / 2 + rng.uniform(-8, 8), (a[1] + b[1]) / 2), b]
        pg.line(pts, lw=0.8, smooth=True)
    for _ in range(40):
        x = rng.uniform(0, 600)
        y = rng.uniform(220, 360)
        pg.line([(x, y), (x + rng.uniform(-8, 8), y + rng.uniform(6, 14))], lw=0.5)
    # golden larches and spruces on the slopes
    for k in range(10):
        x = 20 + k * 62 + rng.uniform(-10, 10)
        if k % 3 == 0:
            spruce_tree(pg, x, 420, rng.uniform(110, 150), 52, rng, snow=False, tiers=6)
        else:
            larch(pg, x, 420, rng.uniform(110, 150), 56, rng)
    top = hill(pg, 420, 10, 0.4, 0.9, lw=TH)
    # a hay barn
    bx, by = 430, 500
    pg.shape([(bx - 60, by), (bx - 60, by - 50), (bx + 60, by - 50), (bx + 60, by)])
    pg.clip_begin(d_poly([(bx - 60, by), (bx - 60, by - 50), (bx + 60, by - 50), (bx + 60, by)]))
    for k in range(7):
        pg.line([(bx - 60, by - 44 + k * 8), (bx + 60, by - 44 + k * 8)], lw=0.6)
    pg.clip_end()
    pg.shape([(bx - 74, by - 46), (bx, by - 92), (bx + 74, by - 46)])
    for k in range(6):
        pg.line([(bx - 60 + k * 12, by - 46 - k * 4), (bx + 60 - k * 12, by - 46 - k * 4)], lw=0.5)
    pg.shape([(bx - 16, by), (bx - 16, by - 34), (bx + 16, by - 34), (bx + 16, by)], lw=TH)
    pg.line([(bx - 16, by - 34), (bx + 16, by)], lw=0.7)
    pg.line([(bx + 16, by - 34), (bx - 16, by)], lw=0.7)
    # a winding stream
    s1 = sample_smooth([(250, 430), (220, 500), (300, 580), (200, 680), (260, 830)], 10)
    s2 = sample_smooth([(272, 430), (258, 500), (346, 580), (280, 680), (380, 830)], 10)
    pg.shape(s1 + list(reversed(s2)), lw=TH)
    for k in range(10):
        t = 0.08 + k * 0.09
        i = int(t * (len(s1) - 1))
        (a1, b1), (a2, b2) = s1[i], s2[i]
        pg.line([(a1 + (a2 - a1) * 0.25, b1), (a1 + (a2 - a1) * 0.6, b1 + 3)], lw=0.6)
    for (x, y, w, h) in [(205, 690, 30, 18), (360, 800, 40, 22), (300, 585, 24, 14)]:
        pg.ellipse(x, y, w, h, lw=TH)
        pg.line([(x - w * 0.5, y - h * 0.2), (x + w * 0.3, y - h * 0.4)], lw=0.6)
    # meadow grasses and alpine flowers
    for _ in range(14):
        grass_head(pg, rng.uniform(-10, 610), 830, rng.uniform(120, 210), rng.uniform(-30, 30), rng)
    for (x, y, r) in [(70, 700, 26), (140, 760, 24), (470, 720, 26), (540, 780, 24), (420, 800, 20), (30, 620, 20), (590, 640, 20), (180, 640, 18)]:
        edelweiss(pg, x, y, r, rng)
    for (x, y, a) in [(40, 780, -10), (110, 660, 6), (500, 660, 10), (580, 720, -6), (170, 800, 4), (440, 640, -8), (380, 720, 6), (140, 560, -4), (560, 560, 8)]:
        gentian(pg, x, y, 30, a)
    for (x, y) in [(90, 590), (520, 590), (160, 620), (580, 620)]:
        pg.line([(x, 830), (x + 2, y)], lw=TH)
        chamomile(pg, x + 2, y, 14, rng)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in LS:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("ls"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
