import math, random

W, H = 600, 800
LW = 2.2      # main line width
TH = 1.4      # thin detail line width
INK = "#3a312a"
FX0, FY0, FX1, FY1 = 14, 14, 586, 786  # frame interior


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v) < 1e6 else str(v)


def rot(p, a):
    r = math.radians(a)
    c, s = math.cos(r), math.sin(r)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def tf(pts, x=0, y=0, a=0, s=1.0, sx=None):
    sx = s if sx is None else sx
    out = []
    for px, py in pts:
        q = rot((px * sx, py * s), a)
        out.append((q[0] + x, q[1] + y))
    return out


def d_poly(pts, close=True):
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    return d + (" Z" if close else "")


def d_smooth(pts, close=True, k=6.0):
    n = len(pts)
    if n < 3:
        return d_poly(pts, close)
    P = pts
    d = f"M{f(P[0][0])} {f(P[0][1])}"
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if close else P[max(i - 1, 0)]
        p1 = P[i % n]
        p2 = P[(i + 1) % n] if close else P[min(i + 1, n - 1)]
        p3 = P[(i + 2) % n] if close else P[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / k, p1[1] + (p2[1] - p0[1]) / k)
        c2 = (p2[0] - (p3[0] - p1[0]) / k, p2[1] - (p3[1] - p1[1]) / k)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + (" Z" if close else "")


def lerp(a, b, t):
    return a + (b - a) * t


def sample_smooth(pts, per=12):
    """Sample a Catmull-Rom curve (open) into many points."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, n - 1)]
        for j in range(per):
            t = j / per
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


class Page:
    def __init__(self, pid, title, season):
        self.pid, self.title, self.season = pid, title, season
        self.el = []
        self.defs = []
        self._clip = 0

    def raw(self, s):
        self.el.append(s)

    def shape(self, pts, lw=LW, smooth=False, fill="#fff"):
        d = d_smooth(pts) if smooth else d_poly(pts)
        self.el.append(f'<path d="{d}" fill="{fill}" stroke-width="{lw}"/>')

    def path(self, d, lw=LW, fill="#fff"):
        self.el.append(f'<path d="{d}" fill="{fill}" stroke-width="{lw}"/>')

    def line(self, pts, lw=TH, smooth=False):
        d = d_smooth(pts, close=False) if smooth else d_poly(pts, close=False)
        self.el.append(f'<path d="{d}" fill="none" stroke-width="{lw}"/>')

    def circle(self, cx, cy, r, lw=LW, fill="#fff"):
        self.el.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke-width="{lw}"/>')

    def ellipse(self, cx, cy, rx, ry, a=0, lw=LW, fill="#fff"):
        self.el.append(f'<ellipse cx="0" cy="0" rx="{f(rx)}" ry="{f(ry)}" transform="translate({f(cx)} {f(cy)}) rotate({f(a)})" fill="{fill}" stroke-width="{lw}"/>')

    def dot(self, cx, cy, r):
        self.el.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{INK}" stroke="none"/>')

    # union outlines -------------------------------------------------------
    def union_strokes(self, segs, lw=LW):
        """segs: list of (pts, width). Outline of the union of thick strokes."""
        dark, white = [], []
        for pts, w in segs:
            d = d_smooth(pts, close=False) if len(pts) > 2 else d_poly(pts, close=False)
            dark.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w + lw)}"/>')
            white.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{f(max(w - lw, 0.1))}"/>')
        self.el.extend(dark + white)

    def tapered(self, pts, w0, w1, lw=LW, per=10):
        sp = sample_smooth(pts, per)
        segs = []
        n = len(sp)
        for i in range(n - 1):
            w = lerp(w0, w1, i / (n - 1))
            segs.append(([sp[i], sp[i + 1]], w))
        dark, white = [], []
        for (a, b), w in segs:
            d = f"M{f(a[0])} {f(a[1])} L{f(b[0])} {f(b[1])}"
            dark.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w + lw)}"/>')
            white.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{f(w - lw)}"/>')
        self.el.extend(dark + white)
        return sp

    def union_circles(self, circs, lw=LW):
        dark = [f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + lw / 2)}" fill="{INK}" stroke="none"/>' for x, y, r in circs]
        white = [f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r - lw / 2)}" fill="#fff" stroke="none"/>' for x, y, r in circs]
        self.el.extend(dark + white)

    def union_shapes(self, shapes, lw=LW, smooth=True):
        ds = [d_smooth(s) if smooth else d_poly(s) for s in shapes]
        dark = [f'<path d="{d}" fill="{INK}" stroke="{INK}" stroke-width="{f(lw * 2)}"/>' for d in ds]
        white = [f'<path d="{d}" fill="#fff" stroke="none"/>' for d in ds]
        self.el.extend(dark + white)

    def clip_begin(self, d):
        self._clip += 1
        cid = f"c{self.pid}{self._clip}"
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        self.el.append(f'<g clip-path="url(#{cid})">')

    def clip_end(self):
        self.el.append("</g>")

    def svg(self):
        frame = f"M{FX0+18} {FY0} H{FX1-18} Q{FX1} {FY0} {FX1} {FY0+18} V{FY1-18} Q{FX1} {FY1} {FX1-18} {FY1} H{FX0+18} Q{FX0} {FY1} {FX0} {FY1-18} V{FY0+18} Q{FX0} {FY0} {FX0+18} {FY0} Z"
        defs = "".join(self.defs)
        body = "".join(self.el)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<defs><clipPath id="fr{self.pid}"><path d="{frame}"/></clipPath>{defs}</defs>'
                f'<rect width="{W}" height="{H}" fill="#fff"/>'
                f'<g stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
                f'<g clip-path="url(#fr{self.pid})">{body}</g>'
                f'<path d="{frame}" fill="none" stroke-width="2.8"/></g></svg>')


# ---------------------------------------------------------------- motifs ---

def prof(kind, t):
    s = math.sin(math.pi * t)
    if kind == "ovate":
        return (max(s, 0) ** 0.75) * (1.0 - 0.3 * t)
    if kind == "lance":
        return max(s, 0) ** 0.9 * (1.0 - 0.15 * t)
    if kind == "round":
        return max(s, 0) ** 0.5
    if kind == "heart":
        return max(s, 0) ** 0.6 * (1.15 - 0.55 * t)
    if kind == "oak":
        return (max(s, 0) ** 0.7) * (0.62 + 0.38 * abs(math.sin(t * math.pi * 4.5)))
    if kind == "petal":
        return max(s, 0) ** 0.6 * (0.8 + 0.3 * t) if t < 0.95 else max(s, 0) ** 0.6
    return s


def leaf_geom(L, Wd, kind="ovate", n=40, notch=False, spiky=0):
    right = []
    for i in range(n + 1):
        t = i / n
        right.append((Wd * prof(kind, t), -L * t))
    if spiky:
        # holly style: alternate points pushed out
        right = []
        m = spiky * 2
        for i in range(m + 1):
            t = i / m
            w = Wd * prof("ovate", t)
            if i % 2 == 1:
                w *= 1.28
                t = t + 0.02
            else:
                w *= 0.82
            right.append((w, -L * t))
    left = [(-x, y) for x, y in reversed(right)]
    outline = right[:-1] + ([(0, -L * 0.86)] if notch else [right[-1]]) + left[1:]
    return outline


def draw_leaf(pg, x, y, a, L, Wd, kind="ovate", veins=4, stem=0, s=1.0, notch=False, spiky=0, smooth=False, lw=LW):
    out = leaf_geom(L, Wd, kind, notch=notch, spiky=spiky)
    if stem:
        pg.line(tf([(0, stem), (0, 0)], x, y, a, s), lw=lw)
    pg.shape(tf(out, x, y, a, s), lw=lw, smooth=smooth)
    if veins >= 0:
        pg.line(tf([(0, 0), (0, -L * 0.92)], x, y, a, s))
    for k in range(1, veins + 1):
        t0 = 0.1 + 0.72 * k / (veins + 1)
        t1 = min(t0 + 0.14, 0.95)
        kk = "ovate" if spiky else kind
        for side in (1, -1):
            ex = side * Wd * prof(kk, t1) * (0.82 if spiky else 1.0)
            mid = (ex * 0.5, -L * (t0 + t1) / 2 + L * 0.015)
            pg.line(tf([(0, -L * t0), mid, (ex, -L * t1)], x, y, a, s), smooth=True)
    return out


def flower(pg, cx, cy, R, n=5, wr=0.45, kind="round", center=0.25, a0=0, notch=False,
           layers=1, inner=False, stamens=0, center_style="rings", veins=-1):
    for layer in range(layers):
        RR = R * (1 - 0.28 * layer)
        off = a0 + (180 / n) * layer
        for i in range(n):
            a = off + i * 360 / n
            L = RR
            Wd = RR * wr
            out = leaf_geom(L, Wd, kind, notch=notch)
            pg.shape(tf(out, cx, cy, a), smooth=False)
            if inner:
                inn = leaf_geom(L * 0.62, Wd * 0.5, kind)
                pg.shape(tf([(px, py - L * 0.22) for px, py in inn], cx, cy, a), lw=TH)
            if veins >= 0:
                pg.line(tf([(0, -R * center), (0, -L * 0.8)], cx, cy, a))
    cr = R * center
    if stamens:
        for i in range(stamens):
            a = a0 + i * 360 / stamens + 18
            p = tf([(0, 0), (0, -cr * 2.0)], cx, cy, a)
            pg.line(p)
            pg.circle(p[1][0], p[1][1], max(cr * 0.22, 2), lw=TH)
    pg.circle(cx, cy, cr)
    if center_style == "rings" and cr > 8:
        pg.circle(cx, cy, cr * 0.55, lw=TH)
    elif center_style == "dots" and cr > 8:
        for i in range(7):
            a = i * 360 / 7
            q = tf([(0, -cr * 0.55)], cx, cy, a)[0]
            pg.circle(q[0], q[1], cr * 0.16, lw=TH)
        pg.circle(cx, cy, cr * 0.2, lw=TH)


def spiral(pg, cx, cy, r, turns=2.2, a0=0, direction=1, lw=TH):
    pts = []
    N = int(40 * turns)
    for i in range(N + 1):
        t = i / N
        ang = a0 + direction * t * turns * 2 * math.pi
        rr = r * (1 - t) ** 1.2 + 1
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    pg.line(pts, lw=lw, smooth=True)


def curl(pg, x, y, length, a=0, size=12, lw=TH, flip=1, turns=1.6):
    """A wind line that ends in a curl."""
    pts = [(0, 0), (length * 0.35, -5 * flip), (length * 0.7, 2 * flip), (length, 0)]
    N = int(45 * turns)
    for i in range(1, N + 1):
        t = i / N
        th = math.pi / 2 - t * turns * 2 * math.pi
        rr = size * (1 - t) ** 1.1 + 0.6
        pts.append((length + rr * math.cos(th), (-size + rr * math.sin(th)) * flip))
    pg.line(tf(pts, x, y, a), lw=lw, smooth=True)


def cloud(pg, x, y, w, rng):
    circs = []
    n = max(4, int(w / 24))
    for i in range(n):
        t = i / (n - 1)
        cx = x + (t - 0.5) * w * 0.82
        bump = math.sin(t * math.pi)
        r = w * 0.11 + bump * w * 0.14 + rng.uniform(-2, 2)
        circs.append((cx, y - bump * w * 0.08, r))
    circs.append((x - w * 0.15, y + w * 0.05, w * 0.15))
    circs.append((x + w * 0.15, y + w * 0.05, w * 0.15))
    pg.union_circles(circs)


def hill(pg, y, amp, phase, freq=1.0, bottom=820, lw=LW, rng=None, n=9):
    pts = []
    for i in range(n):
        x = -40 + i * (680 / (n - 1))
        yy = y + amp * math.sin(phase + i * freq)
        pts.append((x, yy))
    top = sample_smooth(pts, 10)
    shape = top + [(680, bottom), (-80, bottom)]
    pg.shape(shape, lw=lw)
    return top


def offset_line(pg, top, dy, lw=TH):
    pg.line([(x, yv + dy) for x, yv in top], lw=lw)


def star(pg, cx, cy, r, n=5, inner=0.45, a0=-90, lw=TH):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(a0 + i * 180 / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    pg.shape(pts, lw=lw)


def grass_tuft(pg, x, y, h, rng, n=5, lw=TH):
    for i in range(n):
        a = -40 + 80 * i / max(n - 1, 1) + rng.uniform(-6, 6)
        hh = h * rng.uniform(0.6, 1.0)
        tip = tf([(0, -hh)], x, y, a * 0.6)[0]
        mid = tf([(0, -hh * 0.5)], x, y, a * 0.3)[0]
        pg.line([(x, y), mid, tip], lw=lw, smooth=True)


def blade(pg, x, y, h, a, w=7):
    pts = [(-w, 0), (-w * 0.6, -h * 0.5), (0, -h), (w * 0.3, -h * 0.5), (w, 0)]
    pg.shape(tf(pts, x, y, a), smooth=False)


def maple(pg, x, y, a, R, veins=True):
    lobes = [-90, -90 - 52, -90 + 52, -90 - 112, -90 + 112]
    lens = [1.0, 0.92, 0.92, 0.62, 0.62]
    pts = []
    N = 220
    for i in range(N):
        th = -90 + 155 - (310 * i / (N - 1))  # from lower right around to lower left
        best = 0.0
        for la, ln in zip(lobes, lens):
            dd = (th - la)
            best = max(best, ln * math.exp(-(dd / 17.0) ** 2))
        r = R * (0.36 + 0.64 * best)
        # serration
        r += R * 0.045 * (1 if (i // 4) % 2 == 0 else -1) * best
        pts.append((r * math.cos(math.radians(th)), r * math.sin(math.radians(th))))
    pts.append((0, R * 0.12))
    pg.line(tf([(0, R * 0.1), (0, R * 0.55)], x, y, a), lw=LW)
    pg.shape(tf(pts, x, y, a))
    if veins:
        for la, ln in zip(lobes, lens):
            tip = (R * ln * 0.9 * math.cos(math.radians(la)), R * ln * 0.9 * math.sin(math.radians(la)))
            pg.line(tf([(0, R * 0.08), (tip[0] * 0.5, tip[1] * 0.5 + 2), tip], x, y, a), smooth=True)


def acorn(pg, x, y, a, s):
    nut = [(0, 0.95), (-0.45, 0.55), (-0.5, 0.0), (-0.42, -0.15), (0.42, -0.15), (0.5, 0.0), (0.45, 0.55)]
    nut = [(px * s, py * s) for px, py in nut]
    pg.shape(tf(nut, x, y, a), smooth=True)
    pg.line(tf([(0, 0.95 * s), (0, 0.78 * s)], x, y, a))
    cap = [(-0.58, 0.02), (-0.55, -0.25), (-0.3, -0.45), (0, -0.5), (0.3, -0.45), (0.55, -0.25), (0.58, 0.02)]
    cap = [(px * s, py * s) for px, py in cap]
    capP = tf(cap, x, y, a)
    pg.line(tf([(0, -0.45 * s), (0.05 * s, -0.68 * s), (0.18 * s, -0.75 * s)], x, y, a), lw=LW, smooth=True)
    pg.shape(capP, smooth=True)
    pg.clip_begin(d_smooth(capP))
    for k in range(-4, 5):
        pg.line(tf([(k * 0.24 * s - 0.6 * s, 0.1 * s), (k * 0.24 * s + 0.6 * s, -0.6 * s)], x, y, a))
        pg.line(tf([(k * 0.24 * s + 0.6 * s, 0.1 * s), (k * 0.24 * s - 0.6 * s, -0.6 * s)], x, y, a))
    pg.clip_end()
    pg.shape(capP, smooth=True, fill="none")


def bird(pg, x, y, s, flip=1, crest=False):
    def T(pts):
        return [(x + px * s * flip, y + py * s) for px, py in pts]
    # tail
    for ang, ln in ((-112, 1.15), (-100, 1.25), (-88, 1.1)):
        out = leaf_geom(ln, 0.22, "lance")
        pts = tf(out, 0, 0, ang)
        pts = [(px - 0.7, py + 0.1) for px, py in pts]
        pg.shape(T(pts))
    # beak
    pg.shape(T([(1.02, -0.72), (1.42, -0.58), (1.02, -0.45)]))
    # legs
    pg.line(T([(-0.1, 0.7), (-0.15, 1.05)]), lw=LW)
    pg.line(T([(0.25, 0.7), (0.3, 1.05)]), lw=LW)
    # body + head union
    body = [(1.0 * math.cos(t), 0.78 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    head = [(0.62 + 0.5 * math.cos(t), -0.55 + 0.5 * math.sin(t)) for t in [i * 2 * math.pi / 40 for i in range(40)]]
    shapes = [T(body), T(head)]
    if crest:
        shapes.append(T([(0.35, -0.8), (0.3, -1.35), (0.55, -1.0), (0.75, -0.95)]))
    pg.union_shapes(shapes, smooth=False)
    # belly
    pg.line(T([(-0.45, 0.6), (0.2, 0.55), (0.75, 0.15), (1.02, -0.35)]), lw=TH, smooth=True)
    # wing
    out = leaf_geom(1.05, 0.38, "ovate")
    wing = tf(out, -0.05, -0.05, -78 if flip == 1 else -78)
    pg.shape(T(wing))
    for k in range(3):
        t = 0.3 + 0.2 * k
        p1 = tf([(0, -1.05 * t)], -0.05, -0.05, -78)[0]
        p2 = tf([(0.3 * (1 - t), -1.05 * (t + 0.18))], -0.05, -0.05, -78)[0]
        p3 = tf([(-0.3 * (1 - t), -1.05 * (t + 0.18))], -0.05, -0.05, -78)[0]
        pg.line(T([p2, p1, p3]))
    # eye
    pg.circle(*T([(0.8, -0.66)])[0], 0.1 * s, lw=TH, fill=INK)
    pg.circle(*T([(0.83, -0.69)])[0], 0.03 * s, lw=0.1, fill="#fff")
    # cheek
    pg.circle(*T([(0.72, -0.4)])[0], 0.1 * s, lw=TH)


def pine(pg, x, y, h, w, tiers=4, snow=False, rng=None):
    pg.shape([(x - w * 0.08, y), (x - w * 0.08, y - h * 0.2), (x + w * 0.08, y - h * 0.2), (x + w * 0.08, y)])
    th = h * 0.9 / tiers
    for i in range(tiers):
        bot = y - h * 0.14 - i * th * 0.8
        top = bot - th * 1.45
        ww = w * (1 - i / (tiers + 0.8)) / 2
        pts = [(x, top), (x + ww, bot)]
        for k in range(1, 8):
            pts.append((x + ww - 2 * ww * k / 8, bot + (6 if k % 2 else 0)))
        pts.append((x - ww, bot))
        pg.shape(pts)
        if snow:
            sw = ww * 0.5
            sy = top + (bot - top) * 0.5
            sp = [(x, top + 1), (x + sw, sy)]
            for k in range(1, 6):
                sp.append((x + sw - 2 * sw * k / 6, sy + (6 if k % 2 else 0)))
            sp.append((x - sw, sy))
            pg.shape(sp, lw=TH)


def mushroom(pg, x, y, w, h, rng, spots=6, tilt=0):
    # stem
    sw = w * 0.16
    stem = [(-sw, 0), (-sw * 0.85, -h * 0.5), (-sw * 0.7, -h * 0.9), (sw * 0.7, -h * 0.9), (sw * 0.85, -h * 0.5), (sw, 0)]
    pg.shape(tf(stem, x, y, tilt), smooth=False)
    # skirt ring
    ring = [(-sw * 1.05, -h * 0.62), (0, -h * 0.55), (sw * 1.05, -h * 0.62), (sw * 0.9, -h * 0.7), (-sw * 0.9, -h * 0.7)]
    pg.shape(tf(ring, x, y, tilt), lw=TH, smooth=True)
    # gills (underside)
    gy = -h * 0.88
    gill = [(-w * 0.5, gy), (0, gy + h * 0.1), (w * 0.5, gy), (0, gy - h * 0.04)]
    gp = tf(gill, x, y, tilt)
    pg.shape(gp, smooth=True)
    pg.clip_begin(d_smooth(gp))
    for k in range(-9, 10):
        pg.line(tf([(0, gy + h * 0.12), (k * w * 0.06, gy - h * 0.05)], x, y, tilt))
    pg.clip_end()
    pg.shape(gp, smooth=True, fill="none")
    # cap
    cap = []
    N = 30
    for i in range(N + 1):
        t = math.pi * i / N
        cap.append((-math.cos(t) * w * 0.55, gy - math.sin(t) ** 0.8 * h * 0.62))
    capP = tf(cap + [(w * 0.4, gy + 2), (0, gy + 5), (-w * 0.4, gy + 2)], x, y, tilt)
    pg.shape(capP, smooth=True)
    pg.clip_begin(d_smooth(capP))
    for _ in range(spots):
        sx = rng.uniform(-0.42, 0.42) * w
        sy = gy - rng.uniform(0.18, 0.5) * h
        pg.ellipse(*tf([(sx, sy)], x, y, tilt)[0], w * rng.uniform(0.05, 0.09), w * rng.uniform(0.04, 0.07), tilt, lw=TH)
    pg.clip_end()


def fern(pg, x, y, L, a, n=9, s=1.0, side=1):
    spine = [(0, 0), (side * 0.12 * L, -0.4 * L), (side * 0.1 * L, -0.75 * L), (side * -0.05 * L, -L)]
    sp = sample_smooth(spine, 12)
    spT = tf(sp, x, y, a)
    for i in range(1, n + 1):
        t = i / (n + 1)
        idx = int(t * (len(sp) - 1))
        px, py = sp[idx]
        size = L * 0.24 * (1 - t * 0.75)
        for sd in (-1, 1):
            out = leaf_geom(size, size * 0.28, "lance", n=16)
            pts = tf(out, px, py, sd * 62 - 8 * t)
            pg.shape(tf(pts, x, y, a), lw=TH)
    pg.line(spT, lw=LW)


def snowflake(pg, cx, cy, R, a0=0, arm_w=None, branches=2, detail=True):
    arm_w = arm_w or max(R * 0.09, 5)
    segs = []
    for i in range(6):
        a = a0 + i * 60
        segs.append((tf([(0, 0), (0, -R)], cx, cy, a), arm_w))
        for b in range(branches):
            t = 0.4 + 0.25 * b
            bl = R * (0.42 - 0.12 * b)
            for sd in (-1, 1):
                p0 = (0, -R * t)
                p1 = rot((0, -bl), sd * 50)
                p1 = (p1[0], p1[1] - R * t)
                segs.append((tf([p0, p1], cx, cy, a), arm_w * 0.8))
    pg.union_strokes(segs)
    # center hexagon
    hx = [rot((0, -R * 0.24), a0 + i * 60) for i in range(6)]
    pg.shape([(cx + px, cy + py) for px, py in hx])
    if detail:
        hx2 = [rot((0, -R * 0.13), a0 + 30 + i * 60) for i in range(6)]
        pg.shape([(cx + px, cy + py) for px, py in hx2], lw=TH)
        for i in range(6):
            a = a0 + i * 60
            # diamond on arm tip
            d = [(0, -R * 0.82), (arm_w * 1.3, -R * 0.9), (0, -R * 1.02), (-arm_w * 1.3, -R * 0.9)]
            pg.shape(tf(d, cx, cy, a), lw=TH)
