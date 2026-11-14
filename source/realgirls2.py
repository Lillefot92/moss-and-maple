"""Realistic cozy moments, round two: new poses and activities, seen from behind."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import real_leaf, oak_leaf, spruce_twig, FINE
from realgirls import (long_hair_back, bun_back, braid_back, strands, cable_knit, chunky_knit, wicker, spruce_tree,
                       poppy, cornflower, chamomile, grass_head, cumulus, birch, mushroom_real, A)

RG2 = []


def rpage(pid, title, season):
    def deco(fn):
        RG2.append((pid, title, season, fn))
        return fn
    return deco


def limb(pg, pts, w, lw=LW):
    pg.union_strokes([(sample_smooth(pts, 8), w)], lw=lw)


def pom_hat(pg, cx, ty, u, rng):
    hat = [(-0.56, 0.42), (-0.55, 0.05), (-0.38, -0.28), (0, -0.4), (0.38, -0.28), (0.55, 0.05), (0.56, 0.42), (0, 0.48)]
    P = A(hat, cx, ty, u)
    pg.shape(P, smooth=True)
    pg.clip_begin(d_smooth(P))
    for k in range(-6, 7):
        pg.line(A([(k * 0.09, 0.3), (k * 0.07, -0.42)], cx, ty, u), lw=FINE)
    pg.clip_end()
    pg.shape(P, smooth=True, fill="none")
    cuff = [(-0.6, 0.5), (-0.59, 0.22), (0, 0.18), (0.59, 0.22), (0.6, 0.5), (0, 0.56)]
    pg.shape(A(cuff, cx, ty, u), smooth=True)
    for k in range(-10, 11):
        pg.line(A([(k * 0.055, 0.24), (k * 0.055, 0.5)], cx, ty, u), lw=0.8)
    circs = [(cx + dx * u, ty + dy * u, r * u) for dx, dy, r in [(0, -0.55, 0.2), (-0.13, -0.5, 0.13), (0.13, -0.5, 0.13), (-0.06, -0.68, 0.12), (0.08, -0.67, 0.12)]]
    pg.union_circles(circs, lw=TH)
    for _ in range(12):
        a = rng.uniform(0, 6.28)
        r = rng.uniform(0.05, 0.2) * u
        x, y = cx + r * math.cos(a), ty - 0.57 * u + r * math.sin(a) * 0.8
        pg.line([(x, y), (x + 3 * math.cos(a), y + 3 * math.sin(a))], lw=0.7)


def skate(pg, x, y, ang, s):
    boot = [(-0.25, -1.0), (0.2, -1.0), (0.22, -0.4), (0.7, -0.2), (0.75, 0.0), (-0.28, 0.0)]
    pg.shape(tf(boot, x, y, ang, s), smooth=False)
    for k in range(4):
        pg.line(tf([(-0.15, -0.85 + k * 0.15), (0.15, -0.8 + k * 0.15)], x, y, ang, s), lw=0.8)
    pg.line(tf([(-0.3, 0.0), (-0.25, 0.15), (0.6, 0.15), (0.75, 0.1)], x, y, ang, s), lw=TH)
    pg.line(tf([(-0.4, 0.25), (0.8, 0.25), (0.92, 0.12), (0.88, 0.04)], x, y, ang, s), lw=LW, smooth=True)
    pg.line(tf([(-0.2, 0.15), (-0.2, 0.25)], x, y, ang, s), lw=TH)
    pg.line(tf([(0.5, 0.15), (0.5, 0.25)], x, y, ang, s), lw=TH)


def apple(pg, x, y, r, rng, leaf=True):
    pts = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        rr = r * (1 + 0.06 * math.cos(2 * t) - 0.08 * max(0, -math.sin(t)) ** 6)
        pts.append((x + rr * math.cos(t), y + rr * math.sin(t) * 0.95))
    pg.shape(pts, smooth=True)
    pg.line([(x - r * 0.15, y - r * 0.85), (x, y - r * 0.75), (x + r * 0.15, y - r * 0.85)], lw=0.9, smooth=True)
    pg.line([(x, y - r * 0.78), (x + 2, y - r * 1.25)], lw=TH)
    pg.line([(x - r * 0.45, y - r * 0.3), (x - r * 0.55, y + r * 0.2)], lw=0.8, smooth=True)
    if leaf:
        real_leaf(pg, x + 3, y - r * 1.15, rng.uniform(30, 70), r * 1.1, r * 0.4, profile="ovate", teeth=10, tooth_amp=0.12, veins=3, lw=TH)


def watering_can(pg, x, y, s):
    body = [(-0.5, 0), (-0.45, -0.75), (0.45, -0.75), (0.5, 0)]
    pg.union_strokes([(sample_smooth(A([(-0.3, -0.75), (-0.2, -1.15), (0.25, -1.15), (0.35, -0.75)], x, y, s), 8), 0.07 * s)], lw=TH)
    pg.shape(A([(0.4, -0.25), (1.05, -0.95), (1.12, -0.9), (0.48, -0.12)], x, y, s), smooth=False)
    pg.shape(A([(1.0, -1.0), (1.22, -1.08), (1.2, -0.84), (1.08, -0.86)], x, y, s), smooth=False)
    pg.shape(A(body, x, y, s))
    pg.ellipse(x, y - 0.75 * s, 0.45 * s, 0.08 * s, lw=TH)
    for k in (-0.25, 0.25):
        pg.line(A([(-0.48, -0.4 + k * 0.3), (0.48, -0.4 + k * 0.3)], x, y, s), lw=0.8)


def pot(pg, x, y, w, h, rng, plant="seedling"):
    if plant == "seedling":
        for k in range(3):
            sx = x + (k - 1) * w * 0.22
            pg.line([(sx, y - h), (sx + rng.uniform(-3, 3), y - h - 26)], lw=TH)
            for sd in (-1, 1):
                real_leaf(pg, sx, y - h - 22, sd * 55, 18, 8, profile="ovate", veins=1, lw=TH)
    elif plant == "pansy":
        for k in range(3):
            fx, fy = x + (k - 1) * w * 0.28, y - h - 14 - (k % 2) * 10
            for a, r in [(-35, 11), (35, 11), (-120, 10), (120, 10), (180, 12)]:
                px, py = fx + r * 0.7 * math.sin(math.radians(a)), fy - r * 0.7 * math.cos(math.radians(a))
                pg.circle(px, py, r * 0.75, lw=TH)
            pg.circle(fx, fy, 3.5, lw=TH)
            for a in (-25, 0, 25):
                pg.line([(fx, fy), (fx + 9 * math.sin(math.radians(a + 180)), fy - 9 * math.cos(math.radians(a + 180)))], lw=0.7)
    pg.shape([(x - w / 2, y - h), (x + w / 2, y - h), (x + w * 0.4, y), (x - w * 0.4, y)])
    pg.shape([(x - w * 0.55, y - h - 10), (x + w * 0.55, y - h - 10), (x + w * 0.55, y - h + 2), (x - w * 0.55, y - h + 2)])


# ================================================================= pages
@rpage("rg2-spring-planting", "Planting the Spring Garden", "spring")
def r2_spring(pg):
    rng = random.Random(1001)
    # picket fence with climbing roses, a birdhouse
    for k in range(13):
        x = k * 48 + 4
        pg.shape([(x, 330), (x + 12, 312), (x + 24, 330), (x + 24, 470), (x, 470)], lw=TH)
    pg.shape([(0, 360), (600, 360), (600, 372), (0, 372)], lw=TH)
    pg.shape([(0, 430), (600, 430), (600, 442), (0, 442)], lw=TH)
    pg.shape([(500, 140), (520, 140), (520, 470), (500, 470)])
    pg.shape([(470, 205), (510, 165), (550, 205), (545, 270), (475, 270)])
    pg.shape([(462, 210), (510, 158), (558, 210), (552, 214), (510, 170), (468, 214)])
    pg.circle(510, 222, 11)
    pg.line([(500, 248), (520, 248)], lw=LW)
    vine = sample_smooth([(40, 470), (60, 380), (130, 330), (220, 320), (300, 300), (380, 320), (440, 300)], 10)
    pg.line(vine, lw=TH, smooth=True)
    for i in range(3, len(vine), 5):
        x, y = vine[i]
        real_leaf(pg, x, y, rng.uniform(-120, 120), 26, 11, profile="ovate", teeth=12, tooth_amp=0.12, veins=3)
    for i in range(6, len(vine), 9):
        x, y = vine[i]
        flower(pg, x + rng.uniform(-6, 6), y - 6, rng.uniform(16, 22), n=5, wr=0.6, kind="round", center=0.2, a0=rng.uniform(0, 72), notch=True, stamens=6)
    # tulips and daffodils along the fence
    for k in range(10):
        x = 20 + k * 60 + rng.uniform(-8, 8)
        pg.line([(x, 520), (x + rng.uniform(-4, 4), 440)], lw=TH)
        real_leaf(pg, x - 4, 522, -16, 70, 9, profile="lance", veins=-1, bend=-0.1)
        if k % 2:
            w, h = 22, 30
            Lp = [(0, 0), (-0.55 * w, -0.25 * h), (-0.6 * w, -0.75 * h), (-0.4 * w, -1.05 * h), (-0.12 * w, -0.7 * h), (0, -0.2 * h)]
            pg.shape(tf(Lp, x, 446), smooth=True)
            pg.shape(tf([(-px, py) for px, py in Lp], x, 446), smooth=True)
            pg.shape(tf([(0, 0.04 * h), (-0.42 * w, -0.3 * h), (-0.32 * w, -0.85 * h), (0, -1.1 * h), (0.32 * w, -0.85 * h), (0.42 * w, -0.3 * h)], x, 446), smooth=True)
        else:
            flower(pg, x, 438, 20, n=6, wr=0.45, kind="ovate", center=0.0001, a0=0)
            pg.circle(x, 438, 8)
            pg.circle(x, 438, 4.5, lw=TH)
    # garden bed with rows of seedlings
    pg.shape([(-10, 500), (610, 500), (610, 640), (-10, 640)], lw=TH)
    for r, y in enumerate((530, 570, 610)):
        pg.line([(-10, y + 8), (610, y + 8)], lw=0.8)
        for k in range(14):
            x = 20 + k * 44 + (22 if r % 2 else 0)
            pg.line([(x, y + 6), (x, y - 6)], lw=TH)
            for sd in (-1, 1):
                real_leaf(pg, x, y - 4, sd * 60, 12, 6, profile="ovate", veins=-1, lw=FINE)
    for _ in range(50):
        pg.circle(rng.uniform(0, 600), rng.uniform(505, 640), rng.uniform(1, 2.2), lw=0.6)
    # her, kneeling, seen from behind
    cx = 300
    # boot soles towards us
    for sd in (-1, 1):
        sole = [(cx + sd * 30 - 20, 760), (cx + sd * 30 - 22, 700), (cx + sd * 30 - 10, 682), (cx + sd * 30 + 10, 682), (cx + sd * 30 + 22, 700), (cx + sd * 30 + 20, 760), (cx + sd * 30, 766)]
        pg.shape(sole, smooth=True)
        for k in range(6):
            yy = 696 + k * 10
            pg.line([(cx + sd * 30 - 14, yy), (cx + sd * 30 + 14, yy - 3)], lw=0.8)
        pg.shape([(cx + sd * 30 - 16, 744), (cx + sd * 30 + 16, 744), (cx + sd * 30 + 15, 762), (cx + sd * 30 - 15, 762)], lw=TH)
    # kneeling cushion
    cush = [(cx - 120, 770), (cx - 128, 716), (cx + 128, 716), (cx + 120, 770)]
    pg.shape(cush, smooth=False)
    pg.line([(cx - 110, 744), (cx + 110, 744)], lw=0.8)
    # legs folded (trousers) and hips
    hips = [(cx - 80, 560), (cx - 100, 610), (cx - 104, 664), (cx - 80, 704), (cx - 36, 714), (cx, 702), (cx + 36, 714), (cx + 80, 704), (cx + 104, 664), (cx + 100, 610), (cx + 80, 560)]
    pg.shape(hips, smooth=True)
    pg.line([(cx, 600), (cx, 700)], lw=TH)
    for sd in (-1, 1):
        pg.shape([(cx + sd * 30 - 22, 690), (cx + sd * 30 + 22, 690), (cx + sd * 30 + 26, 712), (cx + sd * 30 - 26, 712)], lw=TH)
        pg.line([(cx + sd * 60, 640), (cx + sd * 92, 660), (cx + sd * 98, 690)], lw=0.8, smooth=True)
        # back pockets
        pg.shape([(cx + sd * 30 - 24, 610), (cx + sd * 30 + 24, 610), (cx + sd * 30 + 22, 650), (cx + sd * 30, 658), (cx + sd * 30 - 22, 650)], lw=TH)
    # shirt / cardigan, leaning slightly forward, with sleeves rolled up
    torso = [(cx - 28, 430), (cx - 70, 442), (cx - 86, 480), (cx - 80, 540), (cx - 84, 584), (cx, 594), (cx + 84, 584), (cx + 80, 540), (cx + 86, 480), (cx + 70, 442), (cx + 28, 430)]
    pg.shape(torso, smooth=True)
    pg.clip_begin(d_smooth(torso))
    for k in range(-5, 6):
        pg.line([(cx + k * 18, 420), (cx + k * 17, 600)], lw=0.8)
        pg.line([(cx + k * 18 + 5, 420), (cx + k * 17 + 5, 600)], lw=0.6)
    for k in range(5):
        pg.line([(cx - 110, 455 + k * 30), (cx + 110, 455 + k * 30)], lw=0.8)
        pg.line([(cx - 110, 460 + k * 30), (cx + 110, 460 + k * 30)], lw=0.6)
    pg.line([(cx, 440), (cx, 590)], lw=0.8)
    pg.clip_end()
    pg.shape(torso, smooth=True, fill="none")
    for sd in (-1, 1):
        limb(pg, [(cx + sd * 74, 452), (cx + sd * 96, 500), (cx + sd * 104, 548)], 26)
        pg.shape([(cx + sd * 103 - 15, 530), (cx + sd * 103 + 15, 532), (cx + sd * 104 + 15, 546), (cx + sd * 104 - 15, 544)], lw=TH)
    # trowel in her right hand
    pg.ellipse(cx + 106, 560, 10, 12)
    pg.shape([(cx + 110, 566), (cx + 136, 588), (cx + 148, 626), (cx + 126, 606), (cx + 106, 574)], lw=TH, smooth=True)
    # ponytail and headscarf
    pg.shape([(cx - 24, 432), (cx - 18, 408), (cx + 18, 408), (cx + 24, 432)])
    braid = [(cx, 360), (cx - 18, 380), (cx - 22, 430), (cx - 12, 480), (cx, 500), (cx + 12, 480), (cx + 20, 430), (cx + 16, 380)]
    head = [(0.5 * math.cos(t), 0.58 * math.sin(t) + 0.58) for t in [i * 2 * math.pi / 48 for i in range(48)]]
    hP = A(head, cx, 300, 80)
    pg.shape(hP, smooth=True)
    st, en = [], []
    for k in range(22):
        f = k / 21
        a = math.pi * (0.1 + 0.8 * f)
        st.append((cx - 40 * math.cos(a), 300 + 46 - 46 * math.sin(a) * 0.4))
        en.append((cx + (f - 0.5) * 16, 386))
    strands(pg, hP, st, en, rng, waves=0.02, u=80)
    pg.shape(hP, smooth=True, fill="none")
    pg.shape(braid, smooth=True)
    for k in range(9):
        y = 386 + k * 12
        pg.line([(cx - 14, y), (cx, y + 8), (cx + 14, y)], lw=0.8, smooth=True)
    pg.ellipse(cx, 380, 12, 6, lw=TH)
    scarf = [(cx - 40, 340), (cx - 36, 304), (cx - 10, 290), (cx + 20, 292), (cx + 40, 312), (cx + 41, 342), (cx, 334)]
    pg.shape(scarf, smooth=True)
    pg.clip_begin(d_smooth(scarf))
    for i in range(6):
        for j in range(5):
            pg.circle(cx - 36 + i * 15 + (7 if j % 2 else 0), 296 + j * 10, 2.4, lw=0.7)
    pg.clip_end()
    pg.shape([(cx + 30, 330), (cx + 52, 360), (cx + 44, 366), (cx + 26, 340)], lw=TH)
    pg.shape([(cx + 34, 332), (cx + 60, 352), (cx + 56, 360), (cx + 30, 342)], lw=TH)
    # pots, watering can, seed packets
    pot(pg, 70, 760, 70, 60, rng, "pansy")
    pot(pg, 150, 790, 56, 48, rng, "seedling")
    pot(pg, 520, 770, 64, 56, rng, "seedling")
    watering_can(pg, 470, 800, 80)
    for (x, y, a) in [(560, 660, 12), (40, 665, -10)]:
        pk = tf([(-22, -30), (22, -30), (22, 30), (-22, 30)], x, y, a)
        pg.shape(pk, lw=TH)
        flower(pg, *tf([(0, -6)], x, y, a)[0], 12, n=5, wr=0.5, kind="round", center=0.25)
        pg.line(tf([(-16, 18), (16, 18)], x, y, a), lw=0.8)


@rpage("rg2-summer-hammock", "A Book in the Hammock", "summer")
def r2_summer(pg):
    rng = random.Random(1002)
    # lake and far shore between the trees
    pg.line([(0, 470), (600, 470)], lw=TH)
    hill(pg, 452, 8, 0.6, 1.4, lw=TH, bottom=470)
    for k in range(7):
        x0 = rng.uniform(80, 420)
        pg.line([(x0, 486 + k * 8), (x0 + rng.uniform(40, 120), 486 + k * 8)], lw=0.8)
    sx, sy = 400, 455
    pg.shape([(sx - 18, sy + 20), (sx + 22, sy + 20), (sx + 16, sy + 28), (sx - 12, sy + 28)], lw=TH)
    pg.shape([(sx, sy + 18), (sx, sy - 22), (sx + 18, sy + 16)], lw=TH)
    pg.shape([(sx - 2, sy + 16), (sx - 2, sy - 12), (sx - 16, sy + 16)], lw=TH)
    cumulus(pg, 300, 120, 170, rng)
    # two trees with leafy canopies
    for (x, w) in [(70, 60), (530, 64)]:
        pg.shape([(x - w / 2, 800), (x - w / 2 + 6, 300), (x - w / 4, 120), (x + w / 4, 120), (x + w / 2 - 6, 300), (x + w / 2, 800)], smooth=False)
        for k in range(14):
            y = 160 + k * 46 + rng.uniform(-8, 8)
            pg.line([(x - w / 2 + 8, y), (x - w / 2 + 16, y + 18), (x - w / 2 + 10, y + 34)], lw=0.8, smooth=True)
            pg.line([(x + w / 2 - 10, y + 12), (x + w / 2 - 18, y + 26)], lw=0.8)
    for (x0, y0, x1, y1) in [(70, 200, 260, 120), (70, 160, 0, 60), (530, 200, 340, 110), (530, 150, 600, 50), (70, 260, 200, 230), (530, 260, 410, 230)]:
        sp = pg.tapered([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 20), (x1, y1)], 14, 4, lw=TH)
        for i in range(2, len(sp), 2):
            x, y = sp[i]
            for _ in range(2):
                real_leaf(pg, x, y, rng.uniform(0, 360), rng.uniform(30, 40), 13, profile="elliptic", teeth=12, tooth_amp=0.08, veins=4)
    # ropes and hammock
    pg.line([(98, 330), (150, 382)], lw=LW)
    pg.line([(98, 330), (160, 396)], lw=LW)
    pg.line([(502, 330), (450, 382)], lw=LW)
    pg.line([(502, 330), (440, 396)], lw=LW)
    for (x, y) in [(98, 330), (502, 330)]:
        pg.shape([(x - 34, y - 8), (x + 34, y - 8), (x + 34, y + 8), (x - 34, y + 8)], lw=TH)
    # her: head on the left end, book, crossed ankles on the right
    top_edge = [(150, 382), (220, 420), (300, 438), (380, 424), (450, 382)]
    # hair spilling over the edge
    pg.shape([(150, 372), (176, 340), (220, 346), (232, 384), (200, 404), (160, 398)], smooth=True)
    pg.line([(170, 370), (214, 372)], lw=0.8, smooth=True)
    pg.circle(210, 352, 30)
    hc = [(210 + 30 * math.cos(t), 352 + 30 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    pg.clip_begin(d_smooth(hc))
    for k in range(16):
        a = k * 2 * math.pi / 16
        pg.line([(214, 344), (214 + 18 * math.cos(a + 0.4), 344 + 18 * math.sin(a + 0.4)), (210 + 32 * math.cos(a), 352 + 32 * math.sin(a))], lw=0.8, smooth=True)
    pg.clip_end()
    pg.circle(210, 352, 30, fill="none")
    spill = [(186, 372), (200, 380), (204, 420), (196, 460), (186, 484), (178, 450), (180, 400)]
    pg.shape(spill, smooth=True)
    for k in range(3):
        pg.line([(188 + k * 5, 380), (190 + k * 4, 430), (184 + k * 3, 476)], lw=0.8, smooth=True)
    # knees under a summer skirt
    pg.shape([(300, 430), (340, 372), (372, 366), (396, 400), (404, 426)], smooth=True)
    pg.line([(330, 400), (352, 380), (368, 390)], lw=0.8, smooth=True)
    # crossed ankles and bare feet
    limb(pg, [(400, 410), (440, 392), (470, 380)], 18)
    limb(pg, [(398, 420), (445, 404), (474, 398)], 18)
    for (x, y, a) in [(476, 372, -20), (482, 392, -5)]:
        pg.shape(tf([(-6, -12), (10, -14), (22, -8), (24, 2), (12, 10), (-6, 10)], x, y, a), smooth=True)
        for k in range(4):
            pg.circle(*tf([(22 - k * 3.5, -10 + k * 4.5)], x, y, a)[0], 2.2, lw=0.7)
    # the book held up in front of her
    book = [(240, 330), (290, 300), (300, 318), (310, 300), (360, 330), (352, 380), (305, 360), (298, 368), (290, 360), (246, 382)]
    pg.shape(book, smooth=False)
    for k in range(5):
        pg.line([(254, 340 + k * 8), (288, 324 + k * 8)], lw=0.7)
        pg.line([(312, 324 + k * 8), (346, 340 + k * 8)], lw=0.7)
    pg.line([(299, 318), (298, 366)], lw=TH)
    for (x, y) in [(244, 360), (356, 358)]:
        pg.ellipse(x, y, 10, 14)
    # hammock fabric in front of her body
    sling = [(150, 382), (210, 428), (300, 446), (390, 430), (450, 382), (430, 470), (360, 530), (300, 544), (240, 530), (170, 470)]
    pg.shape(sling, smooth=True)
    pg.clip_begin(d_smooth(sling))
    for k in range(-14, 15):
        pg.line([(300 + k * 16, 380), (300 + k * 16 + 50, 560)], lw=0.8)
        pg.line([(300 + k * 16, 380), (300 + k * 16 - 50, 560)], lw=0.8)
    for y in (450, 470, 490):
        pg.line([(140, y + 20), (300, y + 50), (460, y + 20)], lw=TH, smooth=True)
    pg.clip_end()
    pg.shape(sling, smooth=True, fill="none")
    bottom = sample_smooth([(170, 470), (240, 530), (300, 544), (360, 530), (430, 470)], 6)
    for (x, y) in bottom[1:-1:2]:
        pg.line([(x, y), (x - 2, y + 22)], lw=TH)
        pg.line([(x - 3, y + 4), (x - 6, y + 20)], lw=0.7)
        pg.line([(x + 3, y + 4), (x + 3, y + 20)], lw=0.7)
    # grass, flowers, and her sun hat and lemonade on the grass
    for _ in range(18):
        grass_head(pg, rng.uniform(-10, 610), 820, rng.uniform(120, 220), rng.uniform(-30, 30), rng)
    for (x, y) in [(130, 700), (480, 690), (560, 760), (40, 760)]:
        pg.line([(x, 820), (x, y)], lw=TH)
        poppy(pg, x, y, 26, rng, ang=rng.uniform(0, 90))
    for (x, y) in [(200, 760), (420, 770), (330, 790)]:
        pg.line([(x, 820), (x + 3, y)], lw=TH)
        chamomile(pg, x + 3, y, 16, rng)
    hx, hy = 270, 680
    pg.ellipse(hx, hy, 80, 20)
    pg.clip_begin(f"M{hx - 80} {hy} a80 20 0 1 0 160 0 a80 20 0 1 0 -160 0 Z")
    for r in range(1, 7):
        pg.ellipse(hx, hy, 80 - r * 7, 20 - r * 1.6, lw=0.7)
    pg.clip_end()
    pg.shape([(hx - 36, hy - 2), (hx - 36, hy - 34), (hx, hy - 42), (hx + 36, hy - 34), (hx + 36, hy - 2), (hx, hy + 4)], smooth=True)
    pg.shape([(hx - 36, hy - 6), (hx - 36, hy - 16), (hx, hy - 12), (hx + 36, hy - 16), (hx + 36, hy - 6), (hx, hy)], lw=TH, smooth=True)
    gx, gy = 380, 700
    pg.shape([(gx - 18, gy - 50), (gx + 18, gy - 50), (gx + 15, gy + 30), (gx - 15, gy + 30)])
    pg.line([(gx - 17, gy - 30), (gx + 17, gy - 30)], lw=0.8)
    pg.line([(gx + 4, gy - 72), (gx - 2, gy + 10)], lw=LW)
    pg.circle(gx + 15, gy - 50, 12)
    for k in range(6):
        pg.line([(gx + 15, gy - 50), (gx + 15 + 10 * math.cos(k * math.pi / 3), gy - 50 + 10 * math.sin(k * math.pi / 3))], lw=0.7)


@rpage("rg2-autumn-apples", "The Apple Harvest", "autumn")
def r2_autumn(pg):
    rng = random.Random(1003)
    # the apple tree
    pg.shape([(470, 800), (480, 560), (470, 420), (440, 300), (500, 300), (520, 430), (530, 560), (550, 800)], smooth=True)
    for k in range(12):
        y = 330 + k * 40
        pg.line([(486, y), (494, y + 16), (488, y + 30)], lw=0.8, smooth=True)
        pg.line([(522, y + 10), (530, y + 30)], lw=0.8)
    branches = [[(460, 310), (380, 230), (260, 170), (120, 150)], [(480, 300), (500, 180), (470, 60)], [(490, 310), (580, 220), (620, 200)],
                [(380, 232), (330, 120), (300, 40)], [(260, 172), (180, 230), (90, 260)], [(500, 190), (590, 120)]]
    leaf_spots, apple_spots = [], []
    for b in branches:
        sp = pg.tapered(b, 22 if b[0][0] > 450 else 10, 4, lw=LW)
        for i in range(2, len(sp), 2):
            leaf_spots.append(sp[i])
        for i in range(4, len(sp), 7):
            apple_spots.append(sp[i])
    for (x, y) in leaf_spots:
        for _ in range(2):
            real_leaf(pg, x, y, rng.uniform(0, 360), rng.uniform(34, 46), 15, profile="elliptic", teeth=14, tooth_amp=0.1, veins=4)
    for (x, y) in apple_spots:
        apple(pg, x + rng.uniform(-6, 6), y + 26, rng.uniform(17, 22), rng)
    # ladder leaning on the tree
    r1 = [(215, 800), (330, 250)]
    r2 = [(300, 800), (410, 262)]
    for rr in (r1, r2):
        limb(pg, rr, 12)
    for k in range(9):
        t = 0.06 + k * 0.11
        a = (r1[0][0] + (r1[1][0] - r1[0][0]) * t, r1[0][1] + (r1[1][1] - r1[0][1]) * t)
        b = (r2[0][0] + (r2[1][0] - r2[0][0]) * t, r2[0][1] + (r2[1][1] - r2[0][1]) * t)
        pg.shape([(a[0] + 4, a[1] - 5), (b[0] - 4, b[1] - 5), (b[0] - 4, b[1] + 5), (a[0] + 4, a[1] + 5)], lw=TH)
    # her, on the ladder, reaching up
    cx = 300
    # boots on a rung
    for (x, y) in [(cx - 26, 612), (cx + 10, 606)]:
        pg.shape([(x - 12, y - 46), (x + 12, y - 46), (x + 14, y - 6), (x + 16, y + 6), (x - 16, y + 6), (x - 14, y - 6)], smooth=False)
        pg.line([(x - 15, y), (x + 15, y)], lw=TH)
    # long skirt
    skirt = [(cx - 54, 470), (cx + 50, 466), (cx + 68, 520), (cx + 80, 572), (cx + 30, 580), (cx - 10, 572), (cx - 50, 580), (cx - 84, 572), (cx - 70, 520)]
    pg.shape(skirt, smooth=True)
    for k in range(-3, 4):
        pg.line([(cx + k * 14, 476), (cx + k * 20, 572)], lw=0.8)
    # left arm holding the ladder rail
    limb(pg, [(cx - 52, 396), (cx - 72, 440), (cx - 60, 478)], 26)
    pg.ellipse(cx - 58, 482, 11, 13)
    # right arm reaching up to an apple
    limb(pg, [(cx + 46, 392), (cx + 70, 330), (cx + 96, 280)], 26)
    pg.shape([(cx + 84, 300), (cx + 108, 296), (cx + 104, 284), (cx + 82, 288)], lw=TH)
    pg.ellipse(cx + 102, 268, 12, 14, a=20)
    apple(pg, cx + 110, 250, 20, rng, leaf=False)
    # cardigan
    torso = [(cx - 28, 368), (cx - 60, 382), (cx - 62, 430), (cx - 58, 478), (cx + 54, 474), (cx + 58, 420), (cx + 56, 380), (cx + 28, 366)]
    pg.shape(torso, smooth=True)
    cable_knit(pg, torso, cx - 70, cx + 70, 360, 480, col=34, row=18)
    pg.shape(torso, smooth=True, fill="none")
    pg.line([(cx - 60, 470), (cx + 56, 466)], lw=TH)
    # hair in a low ponytail with a ribbon
    head = [(0.5 * math.cos(t), 0.6 * math.sin(t) + 0.6) for t in [i * 2 * math.pi / 48 for i in range(48)]]
    hP = A(head, cx, 268, 72)
    pg.shape(hP, smooth=True)
    st = [(cx - 36 * math.cos(math.pi * (0.1 + 0.8 * k / 19)), 268 + 43 - 43 * math.sin(math.pi * (0.1 + 0.8 * k / 19)) * 0.5) for k in range(20)]
    strands(pg, hP, st, [(cx + (k / 19 - 0.5) * 12, 352) for k in range(20)], rng, waves=0.02, u=72)
    pg.shape(hP, smooth=True, fill="none")
    tail = [(cx - 10, 350), (cx - 22, 380), (cx - 26, 430), (cx - 14, 462), (cx - 2, 470), (cx + 10, 440), (cx + 14, 390), (cx + 10, 352)]
    pg.shape(tail, smooth=True)
    for k in range(5):
        pg.line([(cx - 8 + k * 4, 356), (cx - 18 + k * 6, 420), (cx - 10 + k * 5, 464)], lw=0.8, smooth=True)
    for sd in (-1, 1):
        pg.shape([(cx, 350), (cx + sd * 26, 338), (cx + sd * 24, 362)], lw=TH, smooth=True)
        pg.shape([(cx, 352), (cx + sd * 12, 390), (cx + sd * 20, 386)], lw=TH)
    pg.circle(cx, 351, 5)
    # basket hanging on the ladder, apples in the grass, a crate
    bx, by = 252, 560
    pg.line([(bx - 30, by - 10), (bx - 10, by - 60), (262, 506)], lw=LW, smooth=True)
    for (ax, ay, r) in [(bx - 22, by - 14, 15), (bx + 6, by - 18, 16), (bx + 28, by - 12, 14)]:
        apple(pg, ax, ay, r, rng, leaf=False)
    basket = [(bx - 44, by - 8), (bx + 44, by - 8), (bx + 34, by + 40), (bx - 34, by + 40)]
    pg.shape(basket)
    wicker(pg, basket, bx - 46, bx + 46, by - 8, by + 40, rows=4)
    pg.shape(basket, fill="none")
    for _ in range(26):
        x = rng.uniform(-10, 610)
        y = rng.uniform(690, 800)
        pg.line([(x, y), (x + rng.uniform(-4, 4), y - rng.uniform(12, 24))], lw=0.8)
    for (x, y, r) in [(140, 760, 18), (176, 776, 16), (380, 770, 17), (580, 740, 16)]:
        apple(pg, x, y, r, rng, leaf=False)
    cr = [(20, 800), (20, 700), (140, 700), (140, 800)]
    for (ax, ay, r) in [(46, 690, 18), (80, 686, 19), (114, 692, 18), (62, 676, 16), (98, 674, 16)]:
        apple(pg, ax, ay, r, rng, leaf=False)
    pg.shape(cr)
    for y in (720, 748, 776):
        pg.shape([(20, y - 10), (140, y - 10), (140, y + 6), (20, y + 6)], lw=TH)


@rpage("rg2-winter-skating", "Skating at Dusk", "winter")
def r2_winter(pg):
    rng = random.Random(1004)
    # dusk sky
    pg.circle(460, 110, 34, lw=TH)
    for _ in range(26):
        x, y = rng.uniform(20, 580), rng.uniform(20, 300)
        for a in (0, 60, 120):
            pg.line(tf([(0, -3), (0, 3)], x, y, a), lw=0.7)
    # forest on the far shore
    for i in range(14):
        x = -20 + i * 46 + rng.uniform(-8, 8)
        spruce_tree(pg, x, 440, rng.uniform(150, 240), rng.uniform(60, 90), rng, tiers=6)
    hill(pg, 436, 6, 0.3, 1.0, lw=TH)
    # frozen pond
    pond = [(-20, 470), (200, 455), (420, 458), (620, 475), (620, 820), (-20, 820)]
    pg.shape(pond, smooth=True)
    pg.clip_begin(d_smooth(pond))
    for _ in range(14):
        x, y = rng.uniform(0, 600), rng.uniform(480, 800)
        L = rng.uniform(60, 180)
        pg.line([(x, y), (x + L * 0.5, y - 8), (x + L, y + 3)], lw=0.8, smooth=True)
    # skate tracks behind her
    for k in range(3):
        pg.line([(120 + k * 20, 800), (200 + k * 10, 720), (260, 690), (300, 700)], lw=0.8, smooth=True)
    pg.clip_end()
    # snow bank and reeds at the edge, a lantern on a post
    hill(pg, 760, 12, 1.2, 0.8, lw=TH)
    for x in (30, 50, 64, 560, 576, 590):
        h = rng.uniform(90, 140)
        pg.line([(x, 790), (x + rng.uniform(-10, 10), 790 - h)], lw=TH)
        if rng.random() < 0.6:
            tx = x + rng.uniform(-8, 8)
            pg.shape([(tx - 5, 790 - h + 10), (tx + 5, 790 - h + 10), (tx + 5, 790 - h + 50), (tx - 5, 790 - h + 50)], lw=TH, smooth=True)
    lx = 100
    pg.shape([(lx - 5, 790), (lx - 5, 560), (lx + 5, 560), (lx + 5, 790)])
    pg.shape([(lx - 30, 540), (lx + 30, 540), (lx + 30, 552), (lx - 30, 552)])
    lan = [(lx - 22, 540), (lx - 20, 476), (lx + 20, 476), (lx + 22, 540)]
    pg.shape(lan)
    pg.shape([(lx - 26, 476), (lx, 452), (lx + 26, 476)])
    pg.line([(lx, 452), (lx, 440)], lw=TH)
    pg.circle(lx, 436, 5, lw=TH)
    pg.shape([(lx - 7, 538), (lx - 7, 512), (lx + 7, 512), (lx + 7, 538)], lw=TH)
    pg.shape([(lx, 488), (lx + 6, 500), (lx, 510), (lx - 6, 500)], lw=TH, smooth=True)
    for k in (-1, 1):
        pg.line([(lx + k * 10, 478), (lx + k * 10, 540)], lw=0.8)
    # her, skating away, arms out for balance
    cx = 320
    # supporting leg and skate
    limb(pg, [(cx - 18, 560), (cx - 22, 630), (cx - 24, 690)], 26)
    skate(pg, cx - 26, 720, 0, 36)
    # free leg lifted behind
    limb(pg, [(cx + 16, 560), (cx + 50, 616), (cx + 96, 640)], 24)
    skate(pg, cx + 110, 650, -100, 32)
    # skirt
    skirt = [(cx - 52, 520), (cx + 52, 520), (cx + 78, 578), (cx + 40, 586), (cx, 580), (cx - 40, 586), (cx - 78, 578)]
    pg.shape(skirt, smooth=True)
    for k in range(-3, 4):
        pg.line([(cx + k * 12, 524), (cx + k * 18, 582)], lw=0.8)
    # arms out
    limb(pg, [(cx - 50, 420), (cx - 110, 446), (cx - 165, 440)], 26)
    limb(pg, [(cx + 50, 420), (cx + 112, 420), (cx + 170, 404)], 26)
    for (x, y) in [(cx - 180, 438), (cx + 186, 400)]:
        pg.shape([(x - 16, y - 12), (x + 4, y - 18), (x + 18, y - 6), (x + 14, y + 10), (x - 10, y + 12)], smooth=True)
        pg.shape([(x - 4, y - 16), (x + 6, y - 28), (x + 14, y - 20)], lw=TH, smooth=True) if x > cx else pg.shape([(x - 6, y + 10), (x - 18, y + 20), (x - 22, y + 10)], lw=TH, smooth=True)
    for (x, y) in [(cx - 150, 441), (cx + 158, 407)]:
        pg.shape([(x - 8, y - 15), (x + 8, y - 15), (x + 8, y + 15), (x - 8, y + 15)], lw=TH)
    # chunky sweater
    torso = [(cx - 30, 404), (cx - 62, 414), (cx - 62, 470), (cx - 56, 528), (cx + 56, 528), (cx + 62, 470), (cx + 62, 414), (cx + 30, 404)]
    pg.shape(torso, smooth=True)
    chunky_knit(pg, torso, cx - 70, cx + 70, 400, 530, w=16, h=13)
    pg.shape(torso, smooth=True, fill="none")
    pg.shape([(cx - 58, 516), (cx + 58, 516), (cx + 58, 532), (cx - 58, 532)], lw=TH)
    # hair, scarf flying, pom-pom hat
    long_hair_back(pg, cx, 330, 58, 2.6, rng, locks=6, width=0.74)
    scarf = [(cx - 40, 404), (cx, 394), (cx + 40, 404), (cx + 42, 422), (cx, 414), (cx - 42, 422)]
    pg.shape(scarf, smooth=True)
    tail = sample_smooth([(cx - 36, 410), (cx - 80, 400), (cx - 120, 410), (cx - 160, 392)], 8)
    pg.union_strokes([(tail, 20)], lw=LW)
    for k in range(4):
        x, y = tail[-1]
        pg.line([(x - 2, y - 8 + k * 5), (x - 16, y - 12 + k * 6)], lw=TH)
    for i in range(2, len(tail) - 2, 3):
        x, y = tail[i]
        pg.line([(x, y - 9), (x - 2, y + 9)], lw=0.8)
    pom_hat(pg, cx, 318, 62, rng)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in RG2:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("rg2"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
