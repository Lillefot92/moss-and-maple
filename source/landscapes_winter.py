"""Winter versions of the landscapes: a snowy alpine valley and a frozen lake."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from botanical import real_leaf, FINE
from realgirls import spruce_tree, birch, cumulus
from landscapes import tree_line, reflection, rowboat, cattail

LW_ = []


def wpage(pid, title, season):
    def deco(fn):
        LW_.append((pid, title, season, fn))
        return fn
    return deco


def snowfall(pg, rng, n=60, y0=20, y1=780):
    for _ in range(n):
        x, y = rng.uniform(20, 580), rng.uniform(y0, y1)
        r = rng.uniform(1.6, 3.6)
        if rng.random() < 0.25:
            for a in (0, 60, 120):
                pg.line(tf([(0, -r * 1.8), (0, r * 1.8)], x, y, a), lw=0.6)
        else:
            pg.circle(x, y, r, lw=0.7)


def snow_cap(pg, x0, x1, y, depth, rng, drips=True, lw=TH):
    """A soft cap of snow sitting on top of an edge from x0 to x1 at height y."""
    top = [(x0 - 4, y + 2)]
    n = max(3, int((x1 - x0) / 18))
    for k in range(n + 1):
        t = k / n
        top.append((x0 + (x1 - x0) * t, y - depth * (0.6 + 0.4 * math.sin(math.pi * t)) + rng.uniform(-2, 2)))
    top.append((x1 + 4, y + 2))
    bottom = []
    for k in range(n, -1, -1):
        t = k / n
        dy = 3 + (rng.uniform(2, 7) if drips and k % 2 else 0)
        bottom.append((x0 + (x1 - x0) * t, y + dy))
    pg.shape(top + bottom, lw=lw, smooth=True)


def icicles(pg, x0, x1, y, rng, n=None):
    n = n or int((x1 - x0) / 10)
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n + rng.uniform(-2, 2)
        L = rng.uniform(6, 20)
        pg.shape([(x - 2.5, y), (x + 2.5, y), (x, y + L)], lw=0.7)


def bare_larch(pg, x, base, h, w, rng):
    pg.shape([(x - 4, base), (x - 2, base - h), (x + 2, base - h), (x + 4, base)], lw=TH)
    for k in range(11):
        t = k / 11
        y = base - h * (0.15 + 0.82 * t)
        bw = w / 2 * (1 - t) ** 0.85
        for sd in (-1, 1):
            pts = [(x, y), (x + sd * bw * 0.5, y + 2), (x + sd * bw, y + 8)]
            pg.line(pts, lw=0.8, smooth=True)
            for j in range(1, 4):
                px = x + sd * bw * j / 4
                py = y + 2 + 6 * (j / 4) ** 2
                pg.line([(px, py), (px + sd * 4, py + 7)], lw=0.5)
            if rng.random() < 0.5:
                pg.ellipse(x + sd * bw * 0.45, y - 1, bw * 0.3, 2.2, lw=0.6)


def dry_stalk(pg, x, y, h, lean, rng):
    pg.line([(x, y), (x + lean * 0.4, y - h * 0.5), (x + lean, y - h)], lw=0.8, smooth=True)
    tx, ty = x + lean, y - h
    kind = rng.random()
    if kind < 0.4:  # seed head
        for k in range(5):
            pg.line([(tx, ty), (tx + 5 * math.cos(k * 1.25 - 1.6), ty + 5 * math.sin(k * 1.25 - 1.6))], lw=0.6)
            pg.circle(tx + 5 * math.cos(k * 1.25 - 1.6), ty + 5 * math.sin(k * 1.25 - 1.6), 1.4, lw=0.5)
    elif kind < 0.7:  # grass plume with a little snow
        for k in range(5):
            pg.line([(tx, ty + k * 4), (tx + 5, ty + k * 4 - 4)], lw=0.5)
            pg.line([(tx, ty + k * 4), (tx - 5, ty + k * 4 - 4)], lw=0.5)
        pg.ellipse(tx, ty - 3, 4, 2.5, lw=0.6)


def fox_tracks(pg, pts):
    for i, (x, y) in enumerate(pts):
        s = 0.6 + 0.4 * (y / 800)
        off = 5 if i % 2 else -5
        cx = x + off * s
        pg.ellipse(cx, y, 3.2 * s, 4 * s, lw=0.7)
        for k in (-1, 0, 1):
            pg.circle(cx + k * 2.6 * s, y - 5 * s, 1.3 * s, lw=0.5)


def chalet(pg, x, y, s, rng):
    T = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    wall = T([(-1.0, 0), (-1.0, -0.9), (1.0, -0.9), (1.0, 0)])
    pg.shape(wall)
    pg.clip_begin(d_poly(wall))
    for k in range(10):
        pg.line(T([(-1.0, -0.86 + k * 0.09), (1.0, -0.86 + k * 0.09)]), lw=0.6)
    pg.clip_end()
    for sd in (-1, 1):
        w = T([(sd * 0.55 - 0.18, -0.62), (sd * 0.55 + 0.18, -0.62), (sd * 0.55 + 0.18, -0.28), (sd * 0.55 - 0.18, -0.28)])
        pg.shape(w)
        pg.line(T([(sd * 0.55, -0.62), (sd * 0.55, -0.28)]), lw=0.7)
        pg.line(T([(sd * 0.55 - 0.18, -0.45), (sd * 0.55 + 0.18, -0.45)]), lw=0.7)
        pg.shape(T([(sd * 0.55 - 0.22, -0.28), (sd * 0.55 + 0.22, -0.28), (sd * 0.55 + 0.22, -0.23), (sd * 0.55 - 0.22, -0.23)]), lw=0.8)
        snow_cap(pg, *[v for v in T([(sd * 0.55 - 0.22, -0.23)])[0][:1]], T([(sd * 0.55 + 0.22, -0.23)])[0][0], T([(0, -0.29)])[0][1], 4, rng, drips=False, lw=0.8)
    pg.shape(T([(-0.16, 0), (-0.16, -0.5), (0.16, -0.5), (0.16, 0)]))
    pg.circle(*T([(0.1, -0.24)])[0], 1.6, lw=0.6)
    roof = T([(-1.3, -0.82), (0, -1.6), (1.3, -0.82), (1.22, -0.76), (0, -1.48), (-1.22, -0.76)])
    pg.shape(roof)
    # heavy snow on the roof with icicles under the eaves
    sn = T([(-1.36, -0.84), (-0.7, -1.3), (0, -1.74), (0.7, -1.3), (1.36, -0.84), (1.2, -0.8), (0.7, -1.18), (0, -1.6), (-0.7, -1.18), (-1.2, -0.8)])
    pg.shape(sn, smooth=True)
    for sd in (-1, 1):
        a, b = T([(sd * 1.22, -0.76)])[0], T([(sd * 0.3, -1.3)])[0]
        for k in range(8):
            t = (k + 0.5) / 8
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + 4
            pg.shape([(px - 2, py), (px + 2, py), (px, py + rng.uniform(6, 14))], lw=0.6)
    # chimney with smoke
    pg.shape(T([(0.5, -1.25), (0.5, -1.62), (0.72, -1.62), (0.72, -1.05)]))
    snow_cap(pg, T([(0.48, 0)])[0][0], T([(0.74, 0)])[0][0], T([(0, -1.62)])[0][1], 5, rng, drips=False, lw=0.8)
    circs = []
    for i in range(6):
        t = i / 5
        cx, cy = T([(0.61 + 0.35 * t + 0.06 * math.sin(i * 1.3), -1.8 - 0.26 * i)])[0]
        circs.append((cx, cy, s * (0.12 + 0.12 * t)))
    pg.union_circles(circs, lw=TH)


# ================================================================= pages
@wpage("ls-snowy-alpine", "Snowy Alpine Valley", "winter")
def w_alpine(pg):
    rng = random.Random(1401)
    # far range and main peaks, deep in snow
    far = [(-20, 250), (90, 150), (160, 190), (300, 130), (360, 170), (600, 110), (640, 150), (640, 380), (-20, 380)]
    pg.shape(far, lw=TH)
    peaks = [(-20, 330), (60, 200), (130, 250), (230, 90), (330, 230), (400, 170), (480, 120), (560, 210), (640, 260), (640, 380), (-20, 380)]
    pg.shape(peaks, lw=LW)
    # dark rock outcrops showing through the snow below the ridges
    for (x, y, sz) in [(236, 150, 16), (220, 200, 12), (250, 230, 10), (484, 170, 14), (506, 215, 11), (470, 240, 9), (396, 220, 12), (66, 240, 10), (150, 280, 8), (330, 270, 9), (560, 260, 10)]:
        pts = [(x - sz, y + sz * 0.4), (x - sz * 0.3, y - sz * 0.6), (x + sz * 0.5, y - sz * 0.3), (x + sz, y + sz * 0.5), (x, y + sz * 0.7)]
        pg.shape(pts, lw=0.8)
        pg.line([(x - sz * 0.3, y - sz * 0.6), (x, y + sz * 0.7)], lw=0.5)
    for (a, b) in [((230, 90), (250, 260)), ((230, 90), (190, 230)), ((480, 120), (470, 270)), ((480, 120), (520, 260)), ((400, 170), (380, 280))]:
        pg.line([a, ((a[0] + b[0]) / 2 + rng.uniform(-8, 8), (a[1] + b[1]) / 2), b], lw=0.7, smooth=True)
    for _ in range(30):
        x, y = rng.uniform(0, 600), rng.uniform(170, 340)
        pg.line([(x, y), (x + rng.uniform(10, 26), y + rng.uniform(-2, 3))], lw=0.5)
    # snowy spruces and bare larches on the lower slopes
    for k in range(11):
        x = 15 + k * 56 + rng.uniform(-10, 10)
        if k % 3 == 1:
            bare_larch(pg, x, 420, rng.uniform(110, 140), 54, rng)
        else:
            spruce_tree(pg, x, 420, rng.uniform(110, 160), rng.uniform(50, 64), rng, snow=True, tiers=6)
    hill(pg, 420, 10, 0.4, 0.9, lw=TH)
    # chalet with a warm window, smoke, heavy snow on the roof
    chalet(pg, 440, 520, 62, rng)
    # half-frozen stream with snowy banks and capped stones
    s1 = sample_smooth([(250, 430), (220, 500), (300, 580), (200, 680), (260, 830)], 10)
    s2 = sample_smooth([(272, 430), (258, 500), (346, 580), (280, 680), (380, 830)], 10)
    pg.shape(s1 + list(reversed(s2)), lw=TH)
    for i in range(3, len(s1) - 2, 4):
        (a1, b1), (a2, b2) = s1[i], s2[i]
        pg.line([(a1 + (a2 - a1) * 0.2, b1 + 2), (a1 + (a2 - a1) * 0.5, b1 - 3), (a1 + (a2 - a1) * 0.8, b1 + 1)], lw=0.6, smooth=True)
    for (x, y, w) in [(205, 690, 30), (360, 800, 40), (300, 585, 24), (240, 520, 20)]:
        pg.ellipse(x, y + 4, w * 0.8, w * 0.45, lw=TH)
        cap = [(x - w * 0.72, y + 2), (x - w * 0.5, y - w * 0.3), (x, y - w * 0.42), (x + w * 0.5, y - w * 0.3), (x + w * 0.72, y + 2), (x + w * 0.3, y + 6), (x - w * 0.3, y + 6)]
        pg.shape(cap, lw=0.8, smooth=True)
    # a fence half buried in snow
    for k in range(7):
        x = 30 + k * 30
        top = 592 - (k % 2) * 6
        pg.shape([(x, 640), (x, top), (x + 8, top - 4), (x + 8, 640)], lw=TH)
        pg.shape([(x - 1, top + 1), (x + 4, top - 7), (x + 9, top - 3), (x + 9, top + 1)], lw=0.7, smooth=True)
    pg.shape([(26, 604), (230, 600), (230, 608), (26, 612)], lw=0.8)
    pg.line(sample_smooth([(10, 642), (80, 632), (160, 640), (238, 634)], 6), lw=TH, smooth=True)
    # foreground: snowdrifts, dry stalks poking through, young snowy spruces, fox tracks
    pg.line(sample_smooth([(380, 720), (470, 700), (560, 712), (640, 700)], 8), lw=TH, smooth=True)
    pg.line(sample_smooth([(-20, 760), (80, 745), (190, 762)], 8), lw=TH, smooth=True)
    for _ in range(26):
        x = rng.choice([rng.uniform(-10, 190), rng.uniform(400, 610)])
        dry_stalk(pg, x, 830, rng.uniform(70, 150), rng.uniform(-20, 20), rng)
    for (x, h) in [(80, 120), (140, 90), (520, 130), (580, 100), (470, 80)]:
        spruce_tree(pg, x, 810, h, h * 0.5, rng, snow=True, tiers=5)
    fox_tracks(pg, [(330 + 30 * math.sin(i * 0.5) + i * 4, 470 + i * 26) for i in range(14)])
    snowfall(pg, rng, n=70, y0=20, y1=440)


@wpage("ls-frozen-lake", "Frozen Lake at Dawn", "winter")
def w_lake(pg):
    rng = random.Random(1402)
    sx, sy = 380, 250
    for i in range(18):
        a = math.radians(180 + i * 180 / 17)
        pg.line([(sx + 60 * math.cos(a), sy + 60 * math.sin(a)), (sx + 420 * math.cos(a), sy + 420 * math.sin(a))], lw=0.6)
    pg.circle(sx, sy, 46, lw=TH)
    tree_line(pg, 300, 130, 56, rng, step=24, snow=True, tiers=6)
    tree_line(pg, 345, 170, 72, rng, step=34, snow=True, tiers=7)
    snow_bank = sample_smooth([(-20, 352), (150, 344), (330, 354), (480, 346), (640, 352)], 8)
    pg.shape(snow_bank + [(640, 368), (-20, 368)], lw=TH, smooth=True)
    # the ice: cracks, trapped bubbles, drifts of snow and skate marks
    pg.shape([(-20, 368), (640, 368), (640, 830), (-20, 830)], lw=TH)
    for _ in range(9):
        x, y = rng.uniform(0, 600), rng.uniform(390, 800)
        def crack(x, y, a, L, d):
            if d == 0 or L < 8:
                return
            ex, ey = x + L * math.cos(a), y + L * math.sin(a) * 0.35
            pg.line([(x, y), ((x + ex) / 2 + rng.uniform(-4, 4), (y + ey) / 2 + rng.uniform(-2, 2)), (ex, ey)], lw=0.7)
            crack(ex, ey, a + rng.uniform(-0.6, 0.6), L * 0.7, d - 1)
            if rng.random() < 0.6:
                crack(ex, ey, a + rng.uniform(0.8, 1.6) * rng.choice((-1, 1)), L * 0.5, d - 1)
        crack(x, y, rng.uniform(0, 6.28), rng.uniform(30, 60), 3)
    for _ in range(26):
        x, y = rng.uniform(300, 600), rng.uniform(600, 800)
        pg.ellipse(x, y, rng.uniform(2, 6), rng.uniform(1.5, 3.5), lw=0.6)
    for (x, y, w) in [(470, 420, 120), (150, 470, 90), (540, 560, 70)]:
        pts = [(x - w, y), (x - w * 0.4, y - 7), (x + w * 0.2, y - 5), (x + w, y)]
        pg.shape(sample_smooth(pts, 6) + [(x + w * 0.5, y + 4), (x - w * 0.5, y + 4)], lw=0.8, smooth=True)
    for k in range(3):
        pg.line(sample_smooth([(330 + k * 14, 800), (380 + k * 10, 650), (470, 560), (560, 540), (600, 570)], 8), lw=0.6, smooth=True)
    for k in range(4):
        pg.line([(sx - 40 + k * 10, 378 + k * 12), (sx + 40 - k * 10, 378 + k * 12)], lw=0.7)
    # the jetty under snow, with a lantern
    J = [(-20, 830), (90, 530), (170, 530), (300, 830)]
    pg.shape(J, lw=LW)
    for k in range(16):
        t = (k + 1) / 17
        y = 530 + 300 * t ** 1.4
        xl = 90 - 110 * (y - 530) / 300
        xr = 170 + 130 * (y - 530) / 300
        pg.line([(xl, y), (xr, y)], lw=0.8)
    for _ in range(9):
        y = rng.uniform(545, 800)
        xl = 90 - 110 * (y - 530) / 300
        xr = 170 + 130 * (y - 530) / 300
        cx_ = xl + (xr - xl) * rng.uniform(0.2, 0.8)
        w = (xr - xl) * rng.uniform(0.12, 0.25)
        pg.shape([(cx_ - w, y + 3), (cx_ - w * 0.4, y - w * 0.18), (cx_ + w * 0.5, y - w * 0.2), (cx_ + w, y + 3)], lw=0.7, smooth=True)
    for (px, py, w) in [(92, 530, 8), (168, 530, 8), (40, 660, 12), (230, 660, 12)]:
        pg.shape([(px - w / 2, py - 20), (px + w / 2, py - 20), (px + w / 2, py + 46), (px - w / 2, py + 46)], lw=TH)
        snow_cap(pg, px - w / 2 - 2, px + w / 2 + 2, py - 20, w * 0.7, rng, drips=False, lw=0.8)
    lx, ly = 228, 640
    pg.shape([(lx - 13, ly), (lx - 11, ly - 34), (lx + 11, ly - 34), (lx + 13, ly)], lw=TH)
    pg.shape([(lx - 16, ly - 34), (lx, ly - 48), (lx + 16, ly - 34)], lw=TH)
    pg.circle(lx, ly - 52, 3.5, lw=0.8)
    pg.shape([(lx, ly - 26), (lx + 4, ly - 18), (lx, ly - 9), (lx - 4, ly - 18)], lw=0.8, smooth=True)
    snow_cap(pg, lx - 16, lx + 16, ly - 36, 5, rng, drips=False, lw=0.7)
    # frosted reeds and cattails behind a snowy shore
    for k in range(9):
        x = 450 + k * 20 + rng.uniform(-6, 6)
        y = 700 + rng.uniform(-10, 10)
        h = rng.uniform(160, 240)
        lean = rng.uniform(-30, 20)
        cattail(pg, x, y, h, lean, rng)
        tx, ty = x + lean * 0.88, y - h * 0.88
        pg.ellipse(tx, ty - 28, 6, 4, lw=0.7)
    shore = sample_smooth([(360, 830), (390, 740), (470, 700), (560, 690), (640, 680)], 8)
    pg.shape(shore + [(640, 830)], lw=TH, smooth=True)
    for _ in range(18):
        x = rng.uniform(420, 600)
        pg.line([(x, 830), (x + rng.uniform(-4, 4), 830 - rng.uniform(40, 90))], lw=0.6)
    # the rowboat turned over on the shore, under a blanket of snow
    bx, by = 500, 740
    hull = [(-110, 0), (-90, -26), (0, -36), (100, -26), (122, 0), (100, 6), (0, 10), (-90, 6)]
    pg.shape([(bx + px, by + py) for px, py in hull], smooth=True)
    for k in (-14, -6):
        pg.line([(bx - 96, by + k + 2), (bx, by + k - 4), (bx + 104, by + k + 2)], lw=0.7, smooth=True)
    snow_cap(pg, bx - 108, bx + 118, by - 30, 16, rng, drips=True, lw=TH)
    icicles(pg, bx - 90, bx + 100, by + 8, rng, n=12)
    snowfall(pg, rng, n=55, y0=20, y1=520)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in LW_:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("lsw"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
