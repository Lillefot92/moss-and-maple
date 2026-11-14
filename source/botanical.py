"""Realistic, detailed botanical line art for Moss & Maple."""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

BOT = []
FINE = 1.1   # very fine detail lines


def bpage(pid, title, season):
    def deco(fn):
        BOT.append((pid, title, season, fn))
        return fn
    return deco


def frac(v):
    return v - math.floor(v)


# --------------------------------------------------------------- leaves
def real_leaf(pg, x, y, ang, L, W, bend=0.12, profile="ovate", teeth=0, tooth_amp=0.08, lobes=0,
              veins=6, vein_reach=0.9, stem=0, tert=False, rng=None, lw=LW, asym=0.94, N=90):
    """A leaf along a gently curved midrib, with serrated or lobed margins and real venation."""
    def mid(t):
        return (bend * L * t * t, -L * t)

    def nrm(t):
        dx, dy = 2 * bend * L * t, -L
        n = math.hypot(dx, dy)
        return (-dy / n, dx / n)

    def width(t):
        s = math.sin(math.pi * t)
        if profile == "ovate":
            w = max(s, 0) ** 0.72 * (1.02 - 0.32 * t)
        elif profile == "elliptic":
            w = max(s, 0) ** 0.78
        elif profile == "lance":
            w = max(s, 0) ** 0.95 * (1 - 0.2 * t)
        elif profile == "obovate":
            w = max(s, 0) ** 0.75 * (0.7 + 0.45 * t)
        else:
            w = max(s, 0) ** 0.8
        if lobes:
            u = t * lobes + 0.25
            w *= 0.5 + 0.5 * abs(math.sin(math.pi * u)) ** 0.55
        if teeth:
            w *= 1 + tooth_amp * (frac(t * teeth) ** 1.6 - 0.35) * min(1, s * 3)
        return W * w

    ts = [i / N for i in range(N + 1)]
    right, left = [], []
    for t in ts:
        m, n, w = mid(t), nrm(t), width(t)
        right.append((m[0] + n[0] * w, m[1] + n[1] * w))
        left.append((m[0] - n[0] * w * asym, m[1] - n[1] * w * asym))
    outline = right + list(reversed(left))[1:]
    T = lambda pts: tf(pts, x, y, ang)
    if stem:
        pg.union_strokes([(T([(0, 0), (-bend * L * 0.05, stem * 0.5), (-bend * L * 0.12, stem)]), max(2.4, W * 0.06))])
    pg.shape(T(outline), lw=lw)
    pg.line(T([mid(t) for t in [i / 30 * 0.97 for i in range(31)]]), lw=TH)
    # secondary veins
    sides = (1, -1)
    if lobes:
        targets = [(k + 0.25) / lobes for k in range(lobes)]
        for k, tt in enumerate(targets):
            if tt > 0.95 or tt < 0.05:
                continue
            t0 = max(0.04, tt - 0.12)
            for sd in sides:
                m0, m1, n1, w1 = mid(t0), mid(tt), nrm(tt), width(tt)
                end = (m1[0] + sd * n1[0] * w1 * 0.88, m1[1] + sd * n1[1] * w1 * 0.88)
                c = ((m0[0] + end[0]) / 2, (m0[1] + end[1]) / 2 + L * 0.02)
                pg.line(T([m0, c, end]), lw=TH, smooth=True)
    else:
        for i in range(1, veins + 1):
            for sd in sides:
                t0 = 0.06 + 0.82 * (i - 0.5 * (sd < 0) * 0.5) / (veins + 1)
                t1 = min(t0 + 0.16 * (1 - 0.4 * t0), 0.97)
                m0, m1, n1, w1 = mid(t0), mid(t1), nrm(t1), width(t1) * (1 if sd > 0 else asym)
                end = (m1[0] + sd * n1[0] * w1 * vein_reach, m1[1] + sd * n1[1] * w1 * vein_reach)
                mm = mid((t0 + t1) / 2)
                nn = nrm((t0 + t1) / 2)
                c = (mm[0] + sd * nn[0] * w1 * 0.45, mm[1] + sd * nn[1] * w1 * 0.45 + L * 0.015)
                pg.line(T([m0, c, end]), lw=TH, smooth=True)
                if tert and rng:
                    # a couple of fine cross veins
                    for _ in range(2):
                        u = rng.uniform(0.3, 0.7)
                        p = (m0[0] + (end[0] - m0[0]) * u, m0[1] + (end[1] - m0[1]) * u)
                        q = (p[0] + rng.uniform(-1, 1) * W * 0.12, p[1] - rng.uniform(0.04, 0.09) * L)
                        pg.line(T([p, q]), lw=FINE)
    return T(outline)


def compound_leaf(pg, x, y, ang, L, leaflets=5, size=0.42, rng=None, teeth=16):
    """Rose-like compound leaf: a rachis with paired serrated leaflets and one at the tip."""
    rach = [(0, 0), (L * 0.04, -L * 0.5), (0, -L)]
    pts = tf(sample_smooth(rach, 10), x, y, ang)
    pg.line(pts, lw=LW)
    pairs = (leaflets - 1) // 2
    for k in range(pairs):
        t = 0.3 + 0.55 * k / max(pairs, 1)
        base = tf([(L * 0.04 * math.sin(math.pi * t), -L * t)], x, y, ang)[0]
        for sd in (1, -1):
            real_leaf(pg, base[0], base[1], ang + sd * (62 - k * 8), L * size * (0.85 + 0.1 * k), L * size * 0.27,
                      bend=0.08 * sd, profile="elliptic", teeth=teeth, tooth_amp=0.12, veins=5, rng=rng)
    tip = tf([(0, -L)], x, y, ang)[0]
    real_leaf(pg, tip[0], tip[1], ang + 4, L * size * 1.05, L * size * 0.3, bend=0.05, profile="elliptic",
              teeth=teeth, tooth_amp=0.12, veins=5, rng=rng)


# ------------------------------------------------------------------ rose
def garden_rose(pg, cx, cy, R, rot=0, tilt=0.86, rng=None):
    rng = rng or random.Random(1)
    rings = [(6, 1.0, 0.0), (5, 0.84, 31), (5, 0.68, 67), (4, 0.52, 13), (3, 0.38, 50)]
    for j, (n, rr, off) in enumerate(rings):
        Rj = R * rr
        for i in range(n):
            a = math.radians(rot + off + i * 360 / n + rng.uniform(-8, 8))
            hw = math.radians(360 / n * (0.66 if j < 3 else 0.8))
            pts = []
            # inner base of the petal
            for k in range(6):
                u = -1 + 2 * k / 5
                aa = a + u * hw * 0.55
                pts.append((Rj * 0.18 * math.cos(aa), Rj * 0.18 * math.sin(aa)))
            pts = list(reversed(pts))
            edge = []
            for k in range(25):
                u = -1 + 2 * k / 24
                aa = a + u * hw
                wav = 1 + 0.05 * math.sin(u * math.pi * 2 + i) - 0.06 * u * u
                notch = -0.06 * math.exp(-(u / 0.12) ** 2) if j < 2 else 0
                r = Rj * (wav + notch)
                edge.append((r * math.cos(aa), r * math.sin(aa)))
            shape = pts[:3] + edge + pts[3:]
            P = [(cx + px, cy + py * tilt) for px, py in shape]
            pg.shape(P, smooth=True)
            # curled lip along the middle of the edge
            lip = [(e[0] * 0.9, e[1] * 0.9) for e in edge[5:20]]
            pg.line([(cx + px, cy + py * tilt) for px, py in lip], lw=TH, smooth=True)
            # a few soft veins
            if j < 3:
                for v in (-0.35, 0, 0.35):
                    aa = a + v * hw
                    pg.line([(cx + Rj * 0.3 * math.cos(aa), cy + Rj * 0.3 * math.sin(aa) * tilt),
                             (cx + Rj * 0.62 * math.cos(aa + v * 0.1), cy + Rj * 0.62 * math.sin(aa + v * 0.1) * tilt)], lw=FINE)
    # tight spiral heart
    # the tight heart: small cupped petals wrapped around each other
    for k in range(5):
        r0 = R * (0.26 - 0.045 * k)
        a0 = math.radians(rot + k * 75)
        arc = [(cx + r0 * math.cos(a0 + u), cy + r0 * math.sin(a0 + u) * tilt) for u in [i / 14 * 3.6 for i in range(15)]]
        inner = [(cx + r0 * 0.55 * math.cos(a0 + 3.6 - u), cy + r0 * 0.55 * math.sin(a0 + 3.6 - u) * tilt) for u in [i / 8 * 3.0 for i in range(9)]]
        pg.shape(arc + inner, smooth=True)
    pg.line([(cx - R * 0.03, cy), (cx + R * 0.03, cy - R * 0.02 * tilt)], lw=TH)


def wild_rose(pg, cx, cy, R, rot=0, rng=None):
    rng = rng or random.Random(2)
    for i in range(5):
        a = rot + i * 72 + rng.uniform(-5, 5)
        # broad heart-shaped petal with wavy edge
        pts = []
        for k in range(41):
            u = -1 + 2 * k / 40
            ang = math.radians(a + u * 40)
            r = R * (0.96 - 0.1 * u * u + 0.04 * math.sin(u * 9 + i) - 0.12 * math.exp(-(u / 0.13) ** 2))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        base = [(cx + R * 0.12 * math.cos(math.radians(a + 30)), cy + R * 0.12 * math.sin(math.radians(a + 30))),
                (cx + R * 0.12 * math.cos(math.radians(a - 30)), cy + R * 0.12 * math.sin(math.radians(a - 30)))]
        pg.shape([base[1]] + pts + [base[0]], smooth=True)
        for v in (-24, -12, 0, 12, 24):
            ang = math.radians(a + v)
            r1 = R * rng.uniform(0.5, 0.7)
            pg.line([(cx + R * 0.24 * math.cos(ang), cy + R * 0.24 * math.sin(ang)),
                     (cx + r1 * math.cos(ang + 0.03), cy + r1 * math.sin(ang + 0.03))], lw=FINE)
    # stamens
    pg.circle(cx, cy, R * 0.26, lw=TH)
    for k in range(34):
        ang = k * 2 * math.pi / 34 + rng.uniform(-0.05, 0.05)
        r1 = R * rng.uniform(0.3, 0.4)
        e = (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))
        pg.line([(cx + R * 0.14 * math.cos(ang), cy + R * 0.14 * math.sin(ang)), e], lw=FINE)
        pg.ellipse(e[0], e[1], R * 0.035, R * 0.022, math.degrees(ang), lw=FINE)
    pg.circle(cx, cy, R * 0.12)
    for k in range(7):
        ang = k * 2 * math.pi / 7
        pg.circle(cx + R * 0.06 * math.cos(ang), cy + R * 0.06 * math.sin(ang), R * 0.025, lw=FINE)


def rose_bud(pg, x, y, ang, s, rng=None):
    T = lambda pts: tf(pts, x, y, ang, s)
    # hip and sepals
    pg.shape(T([(-0.18, 0.3), (-0.22, 0.12), (0, 0.02), (0.22, 0.12), (0.18, 0.3), (0, 0.38)]), smooth=True)
    bud = [(0, 0.08), (-0.34, -0.12), (-0.32, -0.55), (-0.12, -0.92), (0, -1.0), (0.14, -0.9), (0.32, -0.55), (0.34, -0.12)]
    pg.shape(T(bud), smooth=True)
    pg.line(T([(-0.25, -0.2), (-0.05, -0.55), (0.02, -0.98)]), lw=TH, smooth=True)
    pg.line(T([(0.28, -0.25), (0.1, -0.6)]), lw=TH, smooth=True)
    for sd, a2, ln in ((-1, -35, 0.9), (1, 30, 0.85), (-1, -8, 0.6)):
        sep = leaf_geom(ln, 0.09, "lance", n=18)
        pg.shape(tf(tf(sep, 0, 0.05, a2), x, y, ang, s), lw=TH)
        tipx, tipy = tf([(0, -ln)], 0, 0.05, a2)[0]
        pg.line(tf([(tipx, tipy), (tipx + sd * 0.12, tipy - 0.12)], x, y, ang, s), lw=FINE)


def thorns(pg, pts, every=5, size=9, rng=None):
    rng = rng or random.Random(3)
    for i in range(3, len(pts) - 2, every):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        sd = 1 if (i // every) % 2 else -1
        bx, by = pts[i]
        w = size * 0.6
        tip = (bx + sd * nx * size * 1.4 - dx / n * size * 0.9, by + sd * ny * size * 1.4 - dy / n * size * 0.9)
        pg.shape([(bx + dx / n * w, by + dy / n * w), tip, (bx - dx / n * w, by - dy / n * w)], lw=TH)


# ------------------------------------------------------------------- oak
def acorn_real(pg, x, y, ang, s, rng):
    T = lambda pts: tf(pts, x, y, ang, s)
    nut = [(0, 1.05), (-0.12, 0.98), (-0.36, 0.72), (-0.46, 0.3), (-0.44, -0.05), (0.44, -0.05), (0.46, 0.3), (0.36, 0.72), (0.12, 0.98)]
    pg.shape(T(nut), smooth=True)
    pg.shape(T([(0, 1.03), (-0.05, 1.12), (0, 1.16), (0.05, 1.12)]), lw=TH, smooth=True)
    for xx in (-0.22, 0.2):
        pg.line(T([(xx, 0.1), (xx * 1.15, 0.45), (xx * 0.6, 0.85)]), lw=FINE, smooth=True)
    pg.line(T([(-0.3, 0.6), (-0.1, 0.66)]), lw=FINE)
    cup = [(-0.58, 0.08), (-0.6, -0.12), (-0.48, -0.36), (-0.25, -0.5), (0, -0.54), (0.25, -0.5), (0.48, -0.36), (0.6, -0.12), (0.58, 0.08)]
    rim = [(0.58, 0.08), (0.3, 0.14), (0, 0.15), (-0.3, 0.14), (-0.58, 0.08)]
    cupP = T(cup + rim)
    pg.union_strokes([(T([(0.02, -0.5), (0.06, -0.7), (0.0, -0.86)]), 0.09 * s)])
    pg.shape(cupP, smooth=True)
    pg.clip_begin(d_smooth(cupP))
    for row in range(6):
        yy = 0.1 - row * 0.12
        off = 0.06 if row % 2 else 0
        for k in range(-6, 7):
            xx = k * 0.12 + off
            pg.line(T([(xx - 0.065, yy - 0.02), (xx, yy + 0.06), (xx + 0.065, yy - 0.02)]), lw=FINE, smooth=True)
    pg.clip_end()
    pg.shape(cupP, smooth=True, fill="none")


def oak_leaf(pg, x, y, ang, L, rng, bend=0.1):
    return real_leaf(pg, x, y, ang, L, L * 0.34, bend=bend, profile="obovate", lobes=5, stem=L * 0.12, rng=rng)


# ---------------------------------------------------------------- spruce
def pine_cone(pg, x, y, ang, H, W, rng, open_=1.0):
    """A hanging cone: scales in a Fibonacci spiral, drawn top to bottom so lower scales overlap."""
    N = 110
    golden = math.radians(137.508)
    items = []
    for i in range(N):
        z = (i + 0.5) / N
        th = i * golden
        r = W / 2 * (math.sin(math.pi * min(1, z ** 0.75 * 1.02)) ** 0.55) + 2
        c = math.cos(th)
        if c < -0.15:
            continue
        items.append((z, c, math.sin(th), r))
    items.sort(key=lambda it: (it[0], it[1]))
    pg.union_strokes([(tf([(0, -0.02 * H), (0, -0.14 * H), (0.03 * H, -0.2 * H)], x, y, ang), 0.06 * W)])
    for z, c, sn, r in items:
        px, py = r * sn, z * H
        sw = (2 * math.pi * max(r, 6) / 9.5) * (0.4 + 0.6 * max(c, 0)) * open_ + 4
        sh = sw * (0.62 + 0.2 * z)
        shape = [(0, -sh * 0.45), (sw * 0.5, -sh * 0.05), (sw * 0.36, sh * 0.42), (0, sh * 0.62), (-sw * 0.36, sh * 0.42), (-sw * 0.5, -sh * 0.05)]
        lean = -sn * 18
        P = tf(tf(shape, px, py, lean), x, y, ang)
        pg.shape(P, smooth=True)
        if c > 0.2 and sw > 10:
            pg.line(tf(tf([(-sw * 0.28, sh * 0.16), (0, sh * 0.36), (sw * 0.28, sh * 0.16)], px, py, lean), x, y, ang), lw=FINE, smooth=True)
            pg.shape(tf(tf([(0, sh * 0.24), (sw * 0.06, sh * 0.32), (0, sh * 0.4), (-sw * 0.06, sh * 0.32)], px, py, lean), x, y, ang), lw=FINE)


def spruce_twig(pg, pts, needle=20, density=2.4, rng=None, snow=None, w0=7, w1=3):
    rng = rng or random.Random(9)
    sp = sample_smooth(pts, 14)
    # needles behind the twig first
    lines_back, lines_front = [], []
    acc = 0.0
    for i in range(1, len(sp)):
        (x0, y0), (x1, y1) = sp[i - 1], sp[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        dx, dy = (x1 - x0) / (seg or 1), (y1 - y0) / (seg or 1)
        acc += seg
        while acc >= density:
            acc -= density
            t = i / len(sp)
            L = needle * (0.65 + 0.35 * math.sin(math.pi * min(1, t * 1.6))) * rng.uniform(0.85, 1.1)
            for sd in (1, -1):
                a = math.radians(sd * rng.uniform(48, 68))
                ndx = dx * math.cos(a) - dy * math.sin(a)
                ndy = dx * math.sin(a) + dy * math.cos(a)
                bx, by = x1 + rng.uniform(-1, 1), y1 + rng.uniform(-1, 1)
                lines_back.append([(bx, by), (bx + ndx * L * 0.5 + rng.uniform(-1, 1), by + ndy * L * 0.5), (bx + ndx * L, by + ndy * L)])
            if rng.random() < 0.8:
                a = math.radians(rng.uniform(-35, 35))
                ndx = dx * math.cos(a) - dy * math.sin(a)
                ndy = dx * math.sin(a) + dy * math.cos(a)
                L2 = L * 0.55
                lines_front.append([(x1, y1), (x1 + ndx * L2, y1 + ndy * L2)])
    for l in lines_back:
        pg.line(l, lw=1.25)
    pg.tapered(pts, w0, w1, lw=TH)
    for l in lines_front:
        pg.line(l, lw=1.25)
    if snow:
        for (u, sz) in snow:
            idx = int(u * (len(sp) - 1))
            bx, by = sp[idx]
            blob = [(bx + rng.uniform(-sz, sz) * 0.9, by - sz * 0.35 + rng.uniform(-sz * 0.2, sz * 0.1), sz * rng.uniform(0.35, 0.6)) for _ in range(5)]
            pg.union_circles(blob, lw=TH)
    return sp


# ------------------------------------------------------------------ fern
def fern_frond(pg, base, pts, rng, pinnae=26, pmax=70, lean=1):
    sp = sample_smooth([base] + pts, 16)
    n = len(sp)
    shapes = []
    for k in range(pinnae):
        t = 0.08 + 0.9 * k / pinnae
        idx = int(t * (n - 1))
        (x0, y0), (x1, y1) = sp[max(idx - 1, 0)], sp[min(idx + 1, n - 1)]
        dx, dy = x1 - x0, y1 - y0
        ang_r = math.degrees(math.atan2(dy, dx))
        sd = 1 if k % 2 == 0 else -1
        P = pmax * (math.sin(math.pi * min(1, (t - 0.02) * 1.0)) ** 0.7) * (1 - 0.55 * t)
        if P < 6:
            continue
        a_pin = ang_r + sd * 62
        bx, by = sp[idx]
        axis = [(0, 0), (P * 0.5, -sd * P * 0.06), (P, -sd * P * 0.02)]
        axisT = tf(axis, bx, by, a_pin)
        m = max(3, int(P / 9))
        spacing = P / (m + 0.3)
        for j in range(m):
            u = (j + 0.5) / (m + 0.3)
            q = tf([(P * u, -sd * P * 0.06 * math.sin(math.pi * u))], bx, by, a_pin)[0]
            size = (P * 0.24 * (1 - 0.6 * u) + 4)
            wd = min(size * 0.36, spacing * 0.52)
            for side in (1, -1):
                g = leaf_geom(size, wd, "round", n=16)
                lob = []
                for (gx, gy) in g:
                    tt = -gy / size
                    lob.append((gx * (1 + 0.16 * abs(math.sin(tt * math.pi * 3))), gy))
                ang_p = a_pin + 28 if side > 0 else a_pin + 152
                pg.shape(tf(lob, q[0], q[1], ang_p), lw=FINE)
                pg.line(tf([(0, 0), (0, -size * 0.72)], q[0], q[1], ang_p), lw=0.8)
        pg.line(axisT, lw=FINE, smooth=True)
    pg.tapered([base] + pts, 5, 1.8, lw=TH)


def fiddlehead(pg, x, y, s, flip=1):
    stem = [(x, y), (x + 4 * flip, y - s * 0.6), (x + s * 0.12 * flip, y - s * 1.1)]
    pg.tapered(stem, 6, 4, lw=TH)
    cx, cy = x + s * 0.32 * flip, y - s * 1.18
    coil = []
    for k in range(120):
        t = k / 119
        th = math.pi * (1 + flip * 0) + flip * t * 3.4 * math.pi
        r = s * 0.24 * (1 - t) ** 0.9 + 1.5
        coil.append((cx + r * math.cos(th) * flip * -1, cy + r * math.sin(th)))
    pg.union_strokes([(coil, 7)], lw=TH)
    for k in range(0, 110, 7):
        px, py = coil[k]
        pg.line([(px, py - 3), (px + 2, py + 3)], lw=FINE)


def lily_of_valley(pg, x, y, s, flip=1, rng=None):
    rng = rng or random.Random(4)
    for a, L, W, bd in ((-6 * flip, 1.7, 0.3, 0.1 * flip), (16 * flip, 1.45, 0.26, -0.12 * flip)):
        real_leaf(pg, x, y, a, s * L, s * W, bend=bd, profile="elliptic", veins=0)
        for v in (-0.55, -0.25, 0.25, 0.55):
            pts = []
            for i in range(24):
                t = 0.04 + 0.9 * i / 23
                mx, my = bd * s * L * t * t, -s * L * t
                pts.append((mx + s * W * v * math.sin(math.pi * t) ** 0.78, my))
            pg.line(tf(pts, x, y, a), lw=FINE, smooth=True)
    stalk = [(x + 4 * flip, y), (x + 10 * flip, y - s * 0.9), (x + s * 0.4 * flip, y - s * 1.5), (x + s * 0.95 * flip, y - s * 1.45)]
    sp = sample_smooth(stalk, 12)
    pg.line(sp, lw=LW, smooth=True)
    for k in range(7):
        t = 0.4 + 0.58 * k / 7
        bx, by = sp[int(t * (len(sp) - 1))]
        sz = s * (0.2 - 0.08 * t)
        hx, hy = bx + 3 * flip, by + sz * 1.1
        pg.line([(bx, by), (bx + 4 * flip, by + sz * 0.5), (hx, hy - sz * 0.55)], lw=TH, smooth=True)
        bell = [(hx, hy - sz * 0.62), (hx + sz * 0.3, hy - sz * 0.55), (hx + sz * 0.5, hy - sz * 0.2), (hx + sz * 0.52, hy + sz * 0.05)]
        rim = [(hx + sz * 0.66, hy + sz * 0.22), (hx + sz * 0.38, hy + sz * 0.12), (hx + sz * 0.2, hy + sz * 0.28), (hx, hy + sz * 0.14),
               (hx - sz * 0.2, hy + sz * 0.28), (hx - sz * 0.38, hy + sz * 0.12), (hx - sz * 0.66, hy + sz * 0.22)]
        left = [(hx - sz * 0.52, hy + sz * 0.05), (hx - sz * 0.5, hy - sz * 0.2), (hx - sz * 0.3, hy - sz * 0.55)]
        pg.shape(bell + rim + left, smooth=True)
        pg.line([(hx - sz * 0.22, hy - sz * 0.4), (hx - sz * 0.3, hy + sz * 0.05)], lw=FINE, smooth=True)
        pg.line([(hx + sz * 0.1, hy - sz * 0.45), (hx + sz * 0.12, hy + sz * 0.05)], lw=FINE, smooth=True)


def moss(pg, x0, x1, y, rng):
    pts = [(x0, y + 30)]
    for i in range(14):
        xx = x0 + (x1 - x0) * i / 13
        pts.append((xx, y + rng.uniform(-14, 4) - 10 * math.sin(math.pi * i / 13)))
    pts.append((x1, y + 30))
    top = sample_smooth(pts[1:-1], 6)
    pg.shape([(x0, 820)] + top + [(x1, 820)], smooth=False)
    for _ in range(int((x1 - x0) / 5)):
        u = rng.random()
        bx, by = top[int(u * (len(top) - 1))]
        by += rng.uniform(2, 40)
        a = rng.uniform(0, 6.28)
        for k in range(3):
            aa = a + k * 2.1
            pg.line([(bx, by), (bx + 4 * math.cos(aa), by + 4 * math.sin(aa))], lw=FINE)


# ================================================================= pages
@bpage("bot-roses", "Wild & Garden Roses", "summer")
def b_roses(pg):
    rng = random.Random(701)
    # stems
    s1 = pg.tapered([(120, 820), (170, 640), (250, 470), (300, 330)], 11, 7, lw=LW)
    s2 = pg.tapered([(470, 820), (440, 660), (430, 520), (460, 420)], 9, 6, lw=LW)
    s3 = pg.tapered([(250, 470), (200, 360), (150, 250)], 7, 5, lw=LW)
    s4 = pg.tapered([(430, 600), (500, 520), (520, 360)], 7, 5, lw=LW)
    for s_ in (s1, s2, s3, s4):
        thorns(pg, s_, every=7, size=6, rng=rng)
    for (x, y, a, L) in [(175, 620, -70, 170), (210, 540, 60, 150), (130, 720, -40, 140), (440, 690, 55, 160), (455, 560, -60, 150),
                         (500, 520, 50, 120), (200, 360, -60, 120), (520, 420, 40, 110), (90, 470, -20, 110),
                         (150, 790, -65, 150), (460, 790, 60, 150), (300, 800, -10, 140), (160, 680, 50, 120), (450, 760, -50, 120)]:
        compound_leaf(pg, x, y, a, L, leaflets=5, size=0.4, rng=rng)
    garden_rose(pg, 300, 300, 125, rot=12, rng=rng)
    garden_rose(pg, 330, 600, 80, rot=40, tilt=0.8, rng=rng)
    wild_rose(pg, 470, 400, 78, rot=10, rng=rng)
    wild_rose(pg, 150, 240, 66, rot=-20, rng=rng)
    for (x, y, a, s) in [(520, 340, 25, 60), (95, 420, -35, 52), (480, 600, 50, 46)]:
        rose_bud(pg, x, y, a, s, rng)
    # a few fallen petals
    for (x, y, a) in [(300, 740, 20), (360, 770, -40), (240, 780, 70)]:
        pg.shape(tf(leaf_geom(26, 20, "round", notch=True), x, y, a), lw=TH, smooth=True)


@bpage("bot-oak", "Oak Branch & Acorns", "autumn")
def b_oak(pg):
    rng = random.Random(702)
    main = [(-20, 560), (110, 500), (250, 430), (380, 380), (500, 320), (620, 280)]
    sp = pg.tapered(main, 24, 9, lw=LW)
    for i in range(2, len(sp) - 4, 3):
        x, y = sp[i]
        w = 24 - 15 * i / len(sp)
        pg.line([(x - 4, y - w * 0.35), (x + 6, y - w * 0.1), (x + 2, y + w * 0.3)], lw=FINE, smooth=True)
    pg.tapered([(250, 432), (300, 520), (330, 600)], 9, 5, lw=LW)
    pg.tapered([(380, 382), (360, 300), (390, 230)], 8, 4, lw=LW)
    # leaves above the branch, then below
    up = [(40, 520, -30, 180), (150, 480, -12, 200), (260, 425, 15, 190), (390, 232, 5, 180), (470, 335, 35, 190), (560, 300, 60, 170), (330, 380, -40, 160)]
    down = [(90, 510, -150, 180), (200, 460, 170, 190), (330, 600, 160, 170), (440, 360, 150, 190), (560, 300, 130, 160), (300, 520, -130, 150)]
    for (x, y, a, L) in down + up:
        oak_leaf(pg, x, y, a, L, rng, bend=rng.uniform(-0.14, 0.14))
    for (x, y, a, s) in [(250, 470, 8, 54), (290, 488, -18, 50), (380, 420, 12, 50), (410, 430, -14, 46), (120, 530, 6, 50)]:
        acorn_real(pg, x, y + 30, a, s, rng)
    # on the ground
    oak_leaf(pg, 140, 790, -100, 170, rng, bend=0.08)
    oak_leaf(pg, 470, 800, -60, 150, rng, bend=-0.1)
    acorn_real(pg, 300, 740, 70, 54, rng)
    acorn_real(pg, 380, 760, -40, 48, rng)
    cup = [(-0.58, 0.08), (-0.6, -0.12), (-0.48, -0.36), (-0.25, -0.5), (0, -0.54), (0.25, -0.5), (0.48, -0.36), (0.6, -0.12), (0.58, 0.08), (0, 0.2)]
    pg.shape(tf(cup, 230, 760, 160, 46), smooth=True)
    pg.ellipse(*tf([(0, 0.06)], 230, 760, 160, 46)[0], 24, 8, 160, lw=TH)


@bpage("bot-spruce", "Spruce & Pine Cones", "winter")
def b_spruce(pg):
    rng = random.Random(703)
    for _ in range(26):
        pg.circle(rng.uniform(25, 575), rng.uniform(25, 775), rng.uniform(2, 4), lw=FINE)
    spruce_twig(pg, [(-20, 120), (140, 150), (300, 200), (430, 230)], needle=34, rng=rng, snow=[(0.2, 22), (0.5, 26), (0.8, 18)], w0=10, w1=4)
    spruce_twig(pg, [(150, 152), (200, 90), (230, 30)], needle=20, rng=rng, w0=5, w1=2)
    spruce_twig(pg, [(300, 200), (360, 280), (380, 360)], needle=20, rng=rng, w0=5, w1=2)
    spruce_twig(pg, [(620, 330), (500, 360), (380, 450), (300, 470)], needle=34, rng=rng, snow=[(0.25, 24), (0.6, 20)], w0=10, w1=4)
    spruce_twig(pg, [(500, 362), (520, 440), (560, 500)], needle=20, rng=rng, w0=5, w1=2)
    pine_cone(pg, 250, 210, 0, 230, 105, rng)
    pine_cone(pg, 130, 165, 8, 180, 86, rng)
    pine_cone(pg, 440, 455, -6, 170, 86, rng)
    # cones lying in the snow
    pine_cone(pg, 40, 735, -82, 190, 92, rng)
    pine_cone(pg, 590, 745, 84, 170, 84, rng)
    hill(pg, 760, 8, 0.5, 0.9)
    spruce_twig(pg, [(220, 760), (300, 700), (400, 690)], needle=18, rng=rng, w0=5, w1=2)
    for (x, y) in [(330, 600), (360, 620)]:
        pass


@bpage("bot-fern", "Fern Glade", "spring")
def b_fern(pg):
    rng = random.Random(704)
    fern_frond(pg, (300, 790), [(250, 600), (170, 400), (90, 220), (40, 120)], rng, pinnae=24, pmax=125)
    fern_frond(pg, (320, 790), [(380, 610), (470, 430), (550, 300), (600, 250)], rng, pinnae=22, pmax=115)
    fern_frond(pg, (310, 790), [(300, 600), (310, 400), (330, 210), (350, 60)], rng, pinnae=24, pmax=110)
    fiddlehead(pg, 230, 780, 150, flip=-1)
    fiddlehead(pg, 395, 780, 120, flip=1)
    lily_of_valley(pg, 80, 790, 170, flip=1, rng=rng)
    lily_of_valley(pg, 520, 790, 150, flip=-1, rng=rng)
    moss(pg, -10, 610, 740, rng)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for pid, title, season, fn in BOT:
        pg = Page(pid.replace("-", ""), title, season)
        fn(pg)
        svg = pg.svg()
        open(os.path.join(outdir, pid + ".svg"), "w").write(svg)
        meta.append({"id": pid, "title": title, "season": season, "svg": svg})
    return meta


if __name__ == "__main__":
    for m in build("bot"):
        print(m["id"], len(m["svg"]) // 1024, "KB")
