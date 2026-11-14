import math, random, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

PAGES = []


def page(pid, title, season):
    def deco(fn):
        PAGES.append((pid, title, season, fn))
        return fn
    return deco


def sunburst(pg, cx, cy, n=24, a0=0, R=900):
    for i in range(n):
        a = math.radians(a0 + i * 360 / n)
        pg.line([(cx, cy), (cx + R * math.cos(a), cy + R * math.sin(a))], lw=TH)


def scatter_swirls(pg, rng, n, box=(30, 30, 570, 770), size=(8, 14)):
    for _ in range(n):
        x = rng.uniform(box[0], box[2]); y = rng.uniform(box[1], box[3])
        spiral(pg, x, y, rng.uniform(*size), turns=1.6, a0=rng.uniform(0, 6.28), direction=rng.choice((1, -1)))


# =============================================================== SPRING ====
@page("spring-blossom", "Cherry Blossom Branch", "spring")
def p1(pg):
    rng = random.Random(11)
    # background: big soft sun with rings + wind curls
    for r in (230, 190, 150):
        pg.circle(395, 270, r, lw=TH if r != 230 else LW)
    for (x, y, L, a, fl) in [(40, 120, 110, -6, 1), (60, 470, 90, 4, -1), (330, 610, 120, -4, 1), (420, 700, 90, 2, -1), (60, 300, 80, 0, 1)]:
        curl(pg, x, y, L, a, size=14, flip=fl)
    for _ in range(16):
        x, y = rng.uniform(30, 570), rng.uniform(40, 760)
        draw_leaf(pg, x, y, rng.uniform(0, 360), 20, 14, "round", veins=-1, notch=True, lw=TH)
    # branches
    main = [(-20, 690), (110, 620), (230, 545), (350, 455), (450, 360), (530, 280), (620, 220)]
    pg.tapered(main, 40, 12)
    b1 = [(235, 545), (225, 450), (255, 360), (300, 300)]
    pg.tapered(b1, 20, 7)
    b2 = [(450, 362), (470, 300), (455, 230)]
    pg.tapered(b2, 11, 4)
    b3 = [(350, 455), (420, 470), (485, 520)]
    pg.tapered(b3, 12, 4)
    b4 = [(110, 622), (95, 560), (120, 505)]
    pg.tapered(b4, 10, 4)
    # bark lines
    for t, (x, y) in enumerate([(40, 660), (160, 590), (300, 494), (400, 410)]):
        pg.line([(x - 10, y + 2), (x + 6, y - 8)], lw=TH)
    # leaves
    for (x, y, a) in [(300, 300, 40), (455, 230, -20), (485, 520, 120), (120, 505, -30), (530, 280, 60), (225, 450, -60)]:
        draw_leaf(pg, x, y, a, 48, 17, "ovate", veins=3, stem=6)
    # bird on branch
    bird(pg, 185, 520, 56)
    # blossoms
    for (x, y, R, a) in [(300, 300, 58, 10), (258, 405, 46, 40), (445, 365, 52, 5), (455, 225, 44, 22),
                         (345, 462, 40, 60), (490, 525, 50, 30), (560, 255, 52, 15), (60, 660, 42, 50),
                         (95, 505, 42, 20), (545, 410, 36, 70)]:
        flower(pg, x, y, R, n=5, wr=0.5, kind="round", center=0.2, a0=a, notch=True, stamens=8, inner=False)
    # buds
    for (x, y, a) in [(335, 285, 30), (240, 445, -40), (500, 300, 20), (520, 560, 130)]:
        draw_leaf(pg, x, y, a, 18, 9, "round", veins=-1, stem=8)
        draw_leaf(pg, x, y, a, 7, 6, "lance", veins=-1)


@page("spring-tulips", "Tulip Garden", "spring")
def p2(pg):
    rng = random.Random(22)
    # sky
    for i in range(16):
        a = math.radians(i * 22.5)
        pg.line([(480 + 70 * math.cos(a), 130 + 70 * math.sin(a)), (480 + 640 * math.cos(a), 130 + 640 * math.sin(a))], lw=TH)
    pg.circle(480, 130, 70)
    pg.circle(480, 130, 52, lw=TH)
    cloud(pg, 150, 140, 170, rng)
    cloud(pg, 300, 240, 120, rng)
    # hills
    top = hill(pg, 410, 18, 0.4, 0.8)
    offset_line(pg, top, 22); offset_line(pg, top, 44)
    top = hill(pg, 470, 22, 2.0, 0.7)
    offset_line(pg, top, 25)
    for i in range(12):
        x = 25 + i * 50
        pg.circle(x, 520 + 8 * math.sin(i), 4, lw=TH)
    hill(pg, 560, 14, 1.0, 0.9)
    # tulips
    tulips = [(75, 470, 54, -6), (175, 400, 62, 4), (275, 480, 52, -3), (365, 380, 66, 5), (460, 455, 56, -5), (540, 400, 58, 6)]
    for x, hy, s, lean in tulips:
        stem = [(x + lean * 2, 800), (x + lean, 600), (x, hy)]
        pg.tapered(stem, 9, 7)
        # leaves at base
        draw_leaf(pg, x + lean * 2 - 4, 770, -26 - lean, 120 + s, 18, "lance", veins=-1, s=1)
        draw_leaf(pg, x + lean * 2 + 4, 775, 24 - lean, 100 + s, 16, "lance", veins=-1, s=1)
    for x, hy, s, lean in tulips:
        w, h = s, s * 1.5
        L = [(0, 0), (-0.55 * w, -0.25 * h), (-0.62 * w, -0.75 * h), (-0.4 * w, -1.08 * h), (-0.12 * w, -0.7 * h), (0, -0.2 * h)]
        R = [(px * -1, py) for px, py in L]
        pg.shape(tf(L, x, hy), smooth=True)
        pg.shape(tf(R, x, hy), smooth=True)
        C = [(0, 0.04 * h), (-0.42 * w, -0.3 * h), (-0.34 * w, -0.85 * h), (0, -1.12 * h), (0.34 * w, -0.85 * h), (0.42 * w, -0.3 * h)]
        pg.shape(tf(C, x, hy), smooth=True)
        pg.line(tf([(0, -0.1 * h), (0, -0.9 * h)], x, hy), smooth=False)
        pg.line(tf([(-0.2 * w, -0.25 * h), (-0.22 * w, -0.7 * h)], x, hy))
        pg.line(tf([(0.2 * w, -0.25 * h), (0.22 * w, -0.7 * h)], x, hy))
    # front border of little daisies and grass
    for i in range(9):
        x = 30 + i * 68 + rng.uniform(-8, 8)
        y = 745 + rng.uniform(-12, 12)
        grass_tuft(pg, x + 30, 790, 34, rng)
        flower(pg, x, y, 18, n=8, wr=0.35, kind="round", center=0.3, a0=rng.uniform(0, 40))


@page("spring-mandala", "Spring Mandala", "spring")
def p3(pg):
    cx, cy = 300, 400
    sunburst(pg, cx, cy, 32)
    pg.circle(cx, cy, 262, lw=TH)
    # corner flowers
    for (x, y) in [(14, 14), (586, 14), (14, 786), (586, 786)]:
        flower(pg, x, y, 95, n=10, wr=0.33, kind="ovate", center=0.3, inner=True)
    # outer leaves
    for i in range(16):
        a = i * 22.5
        p = tf([(0, -150)], cx, cy, a)[0]
        draw_leaf(pg, p[0], p[1], a, 92, 24, "ovate", veins=3)
    for i in range(16):
        a = i * 22.5 + 11.25
        p = tf([(0, -150)], cx, cy, a)[0]
        out = leaf_geom(70, 26, "round")
        pg.shape(tf(out, p[0], p[1], a))
        pg.circle(*tf([(0, -190)], cx, cy, a)[0], 7, lw=TH)
    # scalloped disc
    sc = []
    for i in range(240):
        t = i / 240 * 2 * math.pi
        r = 152 + 7 * abs(math.sin(t * 12))
        sc.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    pg.shape(sc)
    pg.circle(cx, cy, 140, lw=TH)
    for i in range(36):
        q = tf([(0, -131)], cx, cy, i * 10)[0]
        pg.circle(q[0], q[1], 4, lw=TH)
    pg.circle(cx, cy, 122)
    # petals
    for i in range(12):
        a = i * 30 + 15
        out = leaf_geom(112, 30, "ovate")
        pg.shape(tf(out, cx, cy, a))
        pg.shape(tf([(px * 0.55, py * 0.6 - 30) for px, py in out], cx, cy, a), lw=TH)
    for i in range(12):
        a = i * 30
        out = leaf_geom(92, 28, "round")
        pg.shape(tf(out, cx, cy, a))
        pg.line(tf([(0, -30), (0, -75)], cx, cy, a))
    pg.circle(cx, cy, 52)
    for i in range(16):
        q = tf([(0, -44)], cx, cy, i * 22.5)[0]
        pg.circle(q[0], q[1], 5, lw=TH)
    flower(pg, cx, cy, 36, n=8, wr=0.45, kind="round", center=0.3, layers=1)


# =============================================================== SUMMER ====
def sunflower(pg, cx, cy, R, rng, a0=0):
    disk = R * 0.48
    for ring, (L, off) in enumerate(((R, 0), (R * 0.86, 360 / 42))):
        for i in range(21):
            a = a0 + off + i * 360 / 21
            out = leaf_geom(L - disk * 0.7, (L - disk) * 0.2, "ovate")
            pts = [(px, py - disk * 0.75) for px, py in out]
            pg.shape(tf(pts, cx, cy, a))
            pg.line(tf([(0, -disk * 0.95), (0, -disk * 0.75 - (L - disk * 0.7) * 0.75)], cx, cy, a))
    pg.circle(cx, cy, disk)
    n = int((disk / 7.5) ** 2 * 1.0)
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(1, n):
        r = disk * 0.9 * math.sqrt(i / n)
        th = i * golden + a0
        sr = max(1.8, disk * 0.075 * (0.55 + 0.45 * math.sqrt(i / n)))
        if r < disk * 0.2:
            continue
        pg.circle(cx + r * math.cos(th), cy + r * math.sin(th), sr, lw=1.2)
    pg.circle(cx, cy, disk * 0.18, lw=TH)


@page("summer-sunflowers", "Sunflower Field", "summer")
def p4(pg):
    rng = random.Random(44)
    # sky bands
    for k, y in enumerate((150, 250, 350)):
        pts = [(x, y + 18 * math.sin(x / 70 + k)) for x in range(-10, 620, 40)]
        pg.line(pts, lw=TH, smooth=True)
    cloud(pg, 110, 90, 150, rng)
    # field rows
    top = hill(pg, 600, 10, 0.5, 0.8)
    for k in range(1, 6):
        offset_line(pg, top, k * 30)
    # stems & leaves
    pg.tapered([(330, 820), (335, 650), (320, 470), (330, 300)], 24, 18)
    pg.tapered([(120, 820), (125, 690), (115, 530)], 16, 12)
    pg.tapered([(500, 820), (505, 720), (490, 610)], 14, 11)
    for (x, y, a, L) in [(328, 560, -55, 120), (322, 640, 60, 130), (122, 650, -60, 80), (500, 720, 55, 70)]:
        draw_leaf(pg, x, y, a, L, L * 0.38, "heart", veins=4, stem=8)
    sunflower(pg, 330, 300, 170, rng)
    sunflower(pg, 115, 520, 85, rng, a0=7)
    sunflower(pg, 490, 600, 70, rng, a0=3)
    # bee
    bx, by = 500, 160
    pg.line([(380, 210), (420, 180), (450, 200), (470, 170)], lw=TH, smooth=True)
    pg.ellipse(bx - 6, by - 22, 16, 24, -30)
    pg.ellipse(bx + 14, by - 22, 16, 24, 30)
    pg.ellipse(bx, by, 32, 22)
    pg.clip_begin(f"M{bx - 32} {by} a32 22 0 1 0 64 0 a32 22 0 1 0 -64 0 Z")
    for k in (-14, 0, 14):
        pg.line([(bx + k - 6, by - 24), (bx + k + 6, by + 24)], lw=LW)
    pg.clip_end()
    pg.circle(bx + 38, by - 4, 13)
    pg.line([(bx + 42, by - 16), (bx + 48, by - 32), (bx + 56, by - 36)], smooth=True)
    pg.line([(bx + 46, by - 15), (bx + 58, by - 28), (bx + 66, by - 28)], smooth=True)
    pg.circle(bx + 42, by - 6, 2.5, fill=INK, lw=0.1)


@page("summer-butterfly", "Butterfly Meadow", "summer")
def p5(pg):
    rng = random.Random(55)
    scatter_swirls(pg, rng, 14, box=(30, 30, 570, 520))
    for _ in range(40):
        pg.circle(rng.uniform(25, 575), rng.uniform(25, 540), rng.uniform(2, 4), lw=TH)
    # meadow
    top = hill(pg, 580, 16, 0.2, 0.9)
    offset_line(pg, top, 40)
    heads = []
    for i in range(14):
        x = 20 + i * 44 + rng.uniform(-10, 10)
        h = rng.uniform(80, 170)
        stem = [(x, 800), (x + rng.uniform(-10, 10), 800 - h * 0.5), (x + rng.uniform(-14, 14), 800 - h)]
        pg.line(stem, lw=LW, smooth=True)
        heads.append(stem[2])
        if i % 3 == 0:
            draw_leaf(pg, stem[1][0], stem[1][1] + 20, rng.choice((-50, 50)), 40, 13, "lance", veins=-1)
    order = sorted(range(14), key=lambda i: heads[i][1])
    for i in order:
        x, y = heads[i]
        k = i % 3
        if k == 0:
            flower(pg, x, y, 26, n=12, wr=0.28, kind="round", center=0.3, a0=rng.uniform(0, 30))
        elif k == 1:
            flower(pg, x, y, 22, n=5, wr=0.55, kind="round", center=0.25, a0=rng.uniform(0, 70), center_style="dots")
        else:
            flower(pg, x, y, 20, n=6, wr=0.4, kind="ovate", center=0.22, layers=2, a0=rng.uniform(0, 60))
    for i in range(10):
        blade(pg, 30 + i * 62, 800, rng.uniform(50, 90), rng.uniform(-20, 20), 6)
    # butterfly
    cx, cy = 300, 300
    up = [(6, -6), (40, -90), (110, -175), (205, -190), (250, -150), (238, -80), (190, -30), (100, 0), (20, 4)]
    lo = [(8, 8), (90, 14), (165, 55), (190, 130), (150, 200), (85, 205), (35, 150), (10, 60)]
    for sd in (1, -1):
        for wing, nv in ((lo, 5), (up, 6)):
            pts = [(cx + sd * px, cy + py) for px, py in sample_smooth(wing + [wing[0]], 8)]
            pg.shape(pts)
            # inner contour
            inner = [(cx + sd * px * 0.62, cy + py * 0.62) for px, py in sample_smooth(wing + [wing[0]], 8)]
            pg.shape(inner, lw=TH)
            pg.clip_begin(d_poly(pts))
            n = len(pts)
            for v in range(nv):
                q = pts[int((v + 0.7) * n / (nv + 0.6)) % n]
                pg.line([(cx, cy), ((cx + q[0]) / 2 + 3, (cy + q[1]) / 2 - 3), q], lw=TH, smooth=True)
            # spots near edge
            for v in range(nv * 2):
                p = pts[int((v + 0.5) * n / (nv * 2)) % n]
                qx, qy = cx + (p[0] - cx) * 0.86, cy + (p[1] - cy) * 0.86
                pg.circle(qx, qy, 7 if wing is up else 6, lw=TH)
            pg.clip_end()
            pg.shape(pts, fill="none")
    # body
    pg.line([(cx - 4, cy - 70), (cx - 30, cy - 130), (cx - 55, cy - 150)], lw=LW, smooth=True)
    pg.line([(cx + 4, cy - 70), (cx + 30, cy - 130), (cx + 55, cy - 150)], lw=LW, smooth=True)
    pg.circle(cx - 55, cy - 150, 6)
    pg.circle(cx + 55, cy - 150, 6)
    pg.ellipse(cx, cy + 60, 12, 80)
    for k in range(5):
        pg.line([(cx - 11, cy + 20 + k * 20), (cx + 11, cy + 20 + k * 20)], lw=TH)
    pg.ellipse(cx, cy - 18, 15, 30)
    pg.circle(cx, cy - 60, 15)
    # tiny butterflies
    for (x, y, s) in [(90, 110, 0.25), (510, 470, 0.22)]:
        for sd in (1, -1):
            pg.shape([(x + sd * px * s, y + py * s) for px, py in sample_smooth(lo + [lo[0]], 6)])
            pg.shape([(x + sd * px * s, y + py * s) for px, py in sample_smooth(up + [up[0]], 6)])
        pg.ellipse(x, y + 8, 4, 22 * s * 3)


@page("summer-sun", "Sleepy Summer Sun", "summer")
def p6(pg):
    rng = random.Random(66)
    cx, cy = 300, 370
    # sea: overlapping wave scales
    pg.clip_begin("M0 650 H600 V800 H0 Z")
    for row in range(8):
        y = 640 + row * 22
        for i in range(-1, 12):
            x = i * 56 + (28 if row % 2 else 0)
            pg.circle(x, y, 34)
            pg.circle(x, y, 24, lw=TH)
            pg.circle(x, y, 13, lw=TH)
    pg.clip_end()
    pg.line([(0, 650), (600, 650)], lw=LW)
    # clouds
    cloud(pg, 90, 80, 120, rng)
    cloud(pg, 505, 85, 120, rng)
    # long rays
    for i in range(16):
        a = i * 22.5
        pts = [(-26, -160), (0, -275), (26, -160)]
        pg.shape(tf(pts, cx, cy, a))
        pg.line(tf([(0, -175), (0, -245)], cx, cy, a))
    # wavy rays
    for i in range(16):
        a = i * 22.5 + 11.25
        pts = []
        for j in range(13):
            t = j / 12
            pts.append((12 * (1 - t) * math.sin(t * 9) + 14 * (1 - t), -160 - 70 * t))
        pts = pts + [(-px + 2 * 0, py) for px, py in reversed(pts)]
        pts = [(px - 7 * (1 - abs(py + 195) / 35) * 0, py) for px, py in pts]
        flame = [(-16, -150), (-20, -185), (-6, -205), (-10, -225), (0, -240), (10, -225), (6, -205), (20, -185), (16, -150)]
        pg.shape(tf(flame, cx, cy, a), smooth=True)
    pg.circle(cx, cy, 168)
    for i in range(48):
        a = i * 7.5
        pg.shape(tf([(-6, -150), (0, -166), (6, -150)], cx, cy, a), lw=TH)
    pg.circle(cx, cy, 150)
    for i in range(12):
        a = i * 30 + 15
        out = leaf_geom(70, 20, "ovate")
        pg.shape(tf([(px, py - 80) for px, py in out], cx, cy, a))
        pg.circle(*tf([(0, -132)], cx, cy, a)[0], 5, lw=TH)
    pg.circle(cx, cy, 98)
    pg.circle(cx, cy, 88, lw=TH)
    # sleepy face
    for sd in (-1, 1):
        ex = cx + sd * 32
        pg.line([(ex - 14, cy - 8), (ex, cy + 2), (ex + 14, cy - 8)], lw=LW, smooth=True)
        for k in (-8, 0, 8):
            pg.line([(ex + k, cy + 1 - abs(k) * 0.4), (ex + k * 1.4, cy + 9)], lw=TH)
        pg.circle(cx + sd * 50, cy + 22, 11, lw=TH)
    pg.line([(cx - 16, cy + 34), (cx, cy + 44), (cx + 16, cy + 34)], lw=LW, smooth=True)
    # shells in sand corners
    for (x, y, a) in [(70, 600, -20), (530, 610, 20)]:
        pts = []
        for i in range(9):
            ang = math.radians(-160 + i * 140 / 8)
            pts.append((36 * math.cos(ang), 36 * math.sin(ang)))
        shell = [(0, 18)] + pts
        pg.shape(tf(shell, x, y, a))
        for p in pts[1:-1]:
            pg.line(tf([(0, 16), (p[0] * 0.95, p[1] * 0.95)], x, y, a), lw=TH)
        pg.shape(tf([(-12, 12), (12, 12), (8, 24), (-8, 24)], x, y, a))


# =============================================================== AUTUMN ====
@page("autumn-leaves", "Falling Leaves", "autumn")
def p7(pg):
    rng = random.Random(77)
    for (x, y, L, a, fl) in [(30, 90, 140, -8, 1), (300, 60, 120, 6, -1), (40, 420, 120, -4, -1), (330, 520, 140, 4, 1), (60, 720, 130, -6, 1), (380, 750, 110, 3, -1)]:
        curl(pg, x, y, L, a, size=16, flip=fl)
    for _ in range(26):
        pg.circle(rng.uniform(25, 575), rng.uniform(25, 775), rng.uniform(2.5, 5), lw=TH)
    items = [
        ("oak", 470, 110, 35, 170), ("maple", 150, 160, -15, 130), ("ovate", 530, 330, -40, 150),
        ("ovate", 60, 330, 120, 120), ("oak", 300, 330, 160, 150), ("maple", 420, 450, 20, 120),
        ("oak", 130, 500, -50, 160), ("ovate", 480, 640, 60, 140), ("maple", 250, 640, 10, 130),
        ("maple", 530, 760, -25, 90), ("ovate", 80, 760, 100, 100), ("maple", 330, 110, 30, 70),
        ("maple", 190, 360, 35, 105), ("ovate", 330, 250, -70, 120),
    ]
    for kind, x, y, a, s in items:
        if kind == "maple":
            maple(pg, x, y, a, s)
        elif kind == "oak":
            draw_leaf(pg, x + s * 0.4 * math.sin(math.radians(a)), y + s * 0.4 * math.cos(math.radians(a)), a, s, s * 0.32, "oak", veins=5, stem=14)
        else:
            draw_leaf(pg, x + s * 0.4 * math.sin(math.radians(a)), y + s * 0.4 * math.cos(math.radians(a)), a, s, s * 0.36, "ovate", veins=5, stem=14)
    for (x, y, a, s) in [(285, 480, -20, 62), (345, 505, 25, 56), (110, 650, 10, 60), (565, 530, -30, 50), (240, 50, 15, 44), (370, 720, -10, 52)]:
        acorn(pg, x, y, a, s)
    # berries sprig
    pg.line([(30, 600), (60, 600), (90, 585)], lw=LW, smooth=True)
    for (x, y) in [(30, 590), (44, 608), (90, 576), (100, 592), (82, 594)]:
        pg.circle(x, y, 9)


@page("autumn-mushrooms", "Mushroom Forest", "autumn")
def p8(pg):
    rng = random.Random(88)
    # moon + stars
    pg.circle(450, 130, 72)
    for (x, y, r) in [(425, 110, 14), (470, 150, 10), (480, 100, 7), (440, 165, 6)]:
        pg.circle(x, y, r, lw=TH)
    for _ in range(14):
        star(pg, rng.uniform(30, 570), rng.uniform(30, 300), rng.uniform(6, 11))
    # background trees
    for (x, h, w) in [(40, 330, 120), (150, 380, 130), (270, 300, 110), (560, 360, 120), (370, 340, 120), (470, 300, 110)]:
        pine(pg, x, 470, h, w, tiers=5)
    top = hill(pg, 470, 14, 0.3, 0.8)
    offset_line(pg, top, 30)
    top = hill(pg, 560, 18, 1.4, 0.7)
    # ferns
    fern(pg, 60, 700, 190, -15, side=1)
    fern(pg, 540, 690, 170, 18, side=-1)
    fern(pg, 360, 600, 120, 10, side=-1)
    # mushrooms
    mushroom(pg, 220, 680, 250, 300, rng, spots=7, tilt=-4)
    mushroom(pg, 410, 690, 150, 170, rng, spots=5, tilt=8)
    mushroom(pg, 520, 760, 90, 100, rng, spots=4, tilt=-6)
    mushroom(pg, 80, 770, 80, 90, rng, spots=3, tilt=5)
    # snail
    sx, sy = 330, 765
    body = [(-60, 18), (-50, 4), (20, 0), (40, -18), (52, -24), (60, -14), (52, 2), (40, 18)]
    pg.shape(tf(body, sx, sy), smooth=True)
    pg.line([(sx + 48, sy - 20), (sx + 56, sy - 44)], lw=LW)
    pg.line([(sx + 54, sy - 18), (sx + 70, sy - 38)], lw=LW)
    pg.circle(sx + 56, sy - 46, 3.5)
    pg.circle(sx + 71, sy - 40, 3.5)
    pg.circle(sx - 10, sy - 18, 30)
    spiral(pg, sx - 10, sy - 18, 26, turns=2.2, a0=0, direction=1, lw=LW)
    for i in range(12):
        grass_tuft(pg, 20 + i * 52, 792, 30, rng)


@page("autumn-mandala", "Harvest Mandala", "autumn")
def p9(pg):
    cx, cy = 300, 400
    # woven background
    for k in range(-20, 21):
        pg.line([(k * 40, 0), (k * 40 + 800, 800)], lw=TH)
        pg.line([(k * 40, 800), (k * 40 + 800, 0)], lw=TH)
    pg.circle(cx, cy, 275)
    pg.circle(cx, cy, 262, lw=TH)
    for i in range(8):
        a = i * 45
        p = tf([(0, -120)], cx, cy, a)[0]
        maple(pg, *tf([(0, -190)], cx, cy, a)[0], a, 80)
    for i in range(8):
        a = i * 45 + 22.5
        p = tf([(0, -120)], cx, cy, a)[0]
        draw_leaf(pg, p[0], p[1], a, 140, 36, "oak", veins=5)
    pg.circle(cx, cy, 128)
    for i in range(8):
        a = i * 45
        p = tf([(0, -96)], cx, cy, a)[0]
        acorn(pg, p[0], p[1], a + 180, 40)
    for i in range(8):
        a = i * 45 + 22.5
        p = tf([(0, -100)], cx, cy, a)[0]
        pg.circle(p[0], p[1], 9)
    pg.circle(cx, cy, 64)
    flower(pg, cx, cy, 58, n=10, wr=0.35, kind="ovate", center=0.32, inner=True, center_style="dots")
    # corner acorns and leaves
    for (x, y, a) in [(50, 60, 140), (550, 60, -140), (50, 740, 40), (550, 740, -40)]:
        draw_leaf(pg, x, y, a, 70, 24, "ovate", veins=3)
        acorn(pg, x + (20 if x < 300 else -20), y + (20 if y < 400 else -20), a / 4, 34)


# =============================================================== WINTER ====
@page("winter-snowflakes", "Snowflakes", "winter")
def p10(pg):
    rng = random.Random(1010)
    for k, y in enumerate((170, 330, 500, 650)):
        pts = [(x, y + 26 * math.sin(x / 90 + k * 1.3)) for x in range(-20, 640, 40)]
        pg.line(pts, lw=TH, smooth=True)
    for _ in range(60):
        pg.circle(rng.uniform(25, 575), rng.uniform(25, 775), rng.uniform(2, 5), lw=TH)
    for _ in range(12):
        x, y, r = rng.uniform(30, 570), rng.uniform(30, 770), rng.uniform(6, 10)
        for a in (0, 60, 120):
            pg.line(tf([(0, -r), (0, r)], x, y, a), lw=TH)
    for (x, y, R, a) in [(100, 110, 70, 10), (490, 120, 60, 0), (110, 660, 62, 20), (500, 680, 78, 5), (60, 390, 40, 0), (545, 400, 44, 15), (300, 720, 38, 0)]:
        pg.circle(x, y, R * 1.12, lw=TH)
        snowflake(pg, x, y, R, a0=a, branches=2)
    pg.circle(300, 390, 225, lw=LW)
    pg.circle(300, 390, 212, lw=TH)
    snowflake(pg, 300, 390, 200, a0=0, branches=3, arm_w=16)
    # inner star
    star(pg, 300, 390, 40, n=6, inner=0.6, lw=TH)


@page("winter-cabin", "Cozy Winter Cabin", "winter")
def p11(pg):
    rng = random.Random(1111)
    # moon & stars
    pg.circle(470, 110, 50)
    pg.circle(470, 110, 38, lw=TH)
    for _ in range(18):
        star(pg, rng.uniform(30, 570), rng.uniform(30, 330), rng.uniform(5, 10))
    # far hills
    top = hill(pg, 360, 30, 0.5, 0.9)
    offset_line(pg, top, 28)
    for (x, h, w) in [(30, 210, 90), (110, 250, 100), (500, 240, 100), (575, 200, 90)]:
        pine(pg, x, 520, h, w, tiers=5, snow=True)
    hill(pg, 520, 12, 2.0, 0.6)
    # smoke
    circs = []
    for i in range(7):
        t = i / 6
        circs.append((380 + 40 * t + 12 * math.sin(i * 1.2), 336 - i * 24, 13 + 12 * t))
    pg.union_circles(circs)
    # chimney
    pg.shape([(362, 470), (362, 360), (398, 360), (398, 470)])
    pg.shape([(356, 360), (356, 346), (404, 346), (404, 360)])
    for y in (380, 400, 420):
        pg.line([(362, y), (398, y)], lw=TH)
    # cabin body
    pg.shape([(170, 640), (170, 470), (430, 470), (430, 640)])
    for y in range(490, 640, 20):
        pg.line([(170, y), (430, y)], lw=TH)
    for y in range(480, 640, 20):
        pg.circle(170, y, 9, lw=TH)
        pg.circle(430, y, 9, lw=TH)
    # roof
    pg.shape([(140, 485), (300, 355), (460, 485), (440, 495), (300, 382), (160, 495)])
    snow = [(146, 480), (300, 352), (454, 480), (446, 490), (432, 484), (420, 496), (405, 480)]
    snow += [(300, 395), (195, 480), (180, 494), (168, 486), (156, 496)]
    pg.shape([(142, 482), (300, 348), (458, 482), (448, 492), (430, 484), (300, 378), (172, 484), (162, 494)], smooth=False)
    # gable window (round)
    pg.circle(300, 430, 22)
    pg.line([(278, 430), (322, 430)], lw=TH)
    pg.line([(300, 408), (300, 452)], lw=TH)
    # window
    pg.shape([(196, 520), (196, 590), (276, 590), (276, 520)])
    pg.shape([(204, 528), (204, 582), (268, 582), (268, 528)], lw=TH)
    pg.line([(236, 528), (236, 582)], lw=LW)
    pg.line([(204, 555), (268, 555)], lw=LW)
    pg.shape([(190, 590), (282, 590), (282, 600), (190, 600)])
    for k in range(5):
        pg.circle(200 + k * 18, 588, 8, lw=TH)
    # door
    door = [(320, 640), (320, 545)]
    for i in range(11):
        a = math.pi + math.pi * i / 10
        door.append((355 + 35 * math.cos(a), 545 + 35 * math.sin(a)))
    door += [(390, 545), (390, 640)]
    pg.shape(door)
    for x in (338, 355, 372):
        pg.line([(x, 640), (x, 515 + abs(x - 355) * 0.6)], lw=TH)
    pg.circle(380, 590, 4)
    pg.circle(355, 545, 14)
    pg.circle(355, 545, 8, lw=TH)
    # snowy ground & path
    top = hill(pg, 650, 8, 0.0, 0.8)
    pg.shape([(330, 642), (380, 642), (440, 800), (260, 800)])
    for y in (680, 720, 760):
        pg.line([(330 - (y - 642) * 0.45 + 6, y), (380 + (y - 642) * 0.38 - 6, y)], lw=TH)
    # snowman
    mx = 505
    pg.circle(mx, 700, 50)
    pg.circle(mx, 625, 36)
    pg.line([(mx - 34, 625), (mx - 70, 600), (mx - 80, 588)], lw=LW)
    pg.line([(mx + 34, 625), (mx + 70, 598), (mx + 82, 600)], lw=LW)
    pg.circle(mx, 570, 26)
    pg.shape([(mx - 22, 556), (mx - 18, 520), (mx + 18, 520), (mx + 22, 556)])
    pg.shape([(mx - 32, 556), (mx + 32, 556), (mx + 32, 564), (mx - 32, 564)])
    pg.shape([(mx - 30, 588), (mx + 30, 588), (mx + 30, 600), (mx - 30, 600)])
    pg.shape([(mx + 8, 598), (mx + 26, 640), (mx + 12, 642), (mx + 2, 600)])
    pg.circle(mx - 9, 566, 3, fill=INK, lw=0.1)
    pg.circle(mx + 9, 566, 3, fill=INK, lw=0.1)
    pg.shape([(mx - 2, 572), (mx + 26, 578), (mx - 2, 580)], lw=TH)
    for y in (620, 640, 690, 715):
        pg.circle(mx, y, 4.5, lw=TH)
    # front snow bank with little pines
    for (x, h, w) in [(70, 160, 80), (140, 110, 60)]:
        pine(pg, x, 760, h, w, tiers=4, snow=True)
    hill(pg, 760, 10, 1.0, 1.1)


@page("winter-wreath", "Winter Wreath", "winter")
def p12(pg):
    rng = random.Random(1212)
    cx, cy = 300, 380
    # knit-like argyle background
    for k in range(-20, 21):
        pg.line([(k * 56, 0), (k * 56 + 800, 800)], lw=TH)
        pg.line([(k * 56, 800), (k * 56 + 800, 0)], lw=TH)
    # wreath base ring
    pg.circle(cx, cy, 215)
    # holly leaves around
    for i in range(20):
        a = i * 18
        rr = 182 if i % 2 == 0 else 152
        p = tf([(0, -rr)], cx, cy, a)[0]
        draw_leaf(pg, p[0], p[1], a + (60 if i % 2 else -60), 78, 26, "ovate", veins=-1, spiky=5)
        pg.line(tf([(0, 0), (0, -70)], p[0], p[1], a + (60 if i % 2 else -60)))
    for i in range(14):
        a = i * 360 / 14 + 9
        p = tf([(0, -168)], cx, cy, a)[0]
        draw_leaf(pg, p[0], p[1], a + 180 + (40 if i % 2 else -40), 66, 22, "ovate", veins=-1, spiky=4)
        pg.line(tf([(0, 0), (0, -58)], p[0], p[1], a + 180 + (40 if i % 2 else -40)))
    for i in range(10):
        a = i * 36 + 20
        p = tf([(0, -170)], cx, cy, a)[0]
        for (dx, dy) in [(-9, -4), (8, -6), (0, 9)]:
            pg.circle(p[0] + dx, p[1] + dy, 9)
    pg.circle(cx, cy, 125)
    # bird in centre on a little branch
    pg.tapered([(200, 470), (260, 455), (330, 458), (400, 440)], 10, 5)
    draw_leaf(pg, 380, 445, 60, 40, 13, "ovate", veins=-1, spiky=3)
    draw_leaf(pg, 222, 466, -70, 40, 13, "ovate", veins=-1, spiky=3)
    bird(pg, 300, 395, 52, crest=True)
    # bow
    by = cy + 205
    for sd in (-1, 1):
        loop = [(0, 0), (sd * 30, -30), (sd * 70, -38), (sd * 80, -10), (sd * 66, 18), (sd * 30, 14)]
        pg.shape(tf(loop, cx, by), smooth=True)
        pg.line(tf([(sd * 10, -2), (sd * 55, -20)], cx, by), lw=TH, smooth=False)
        tail = [(sd * 6, 8), (sd * 30, 60), (sd * 48, 110), (sd * 34, 104), (sd * 22, 118), (sd * 14, 66), (0, 14)]
        pg.shape(tf(tail, cx, by), smooth=False)
    pg.shape([(-14, -14), (14, -14), (16, 14), (-16, 14)], smooth=True) if False else pg.ellipse(cx, by, 16, 18)
    # snow dots
    for _ in range(30):
        x, y = rng.uniform(25, 575), rng.uniform(25, 775)
        if (x - cx) ** 2 + (y - cy) ** 2 > 225 ** 2:
            pg.circle(x, y, rng.uniform(4, 7))


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in PAGES:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    json.dump(meta, open(os.path.join(outdir, "pages.json"), "w"))
    return meta


if __name__ == "__main__":
    m = build(sys.argv[1] if len(sys.argv) > 1 else "out")
    for p in m:
        print(p["id"], len(p["svg"]))
