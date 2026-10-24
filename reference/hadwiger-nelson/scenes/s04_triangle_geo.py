"""Scene-local geometry for S04_Triangle (pure numpy, manim coordinates).

- a checkerboard of unit squares and a smooth, fold-free warp of it (the "cleverer" pattern),
- a two-colour Voronoi mosaic (the plane painted with only two colours),
- searches that pick stick / triangle placements whose dots sit clearly inside one colour.
"""
import numpy as np
from scipy.spatial import cKDTree

SQ3 = np.sqrt(3.0)
U = 2.0                        # manim units per problem unit
FLOOR_Y = -2.5                 # patterns stay above this line (the scoreboard lives below)
REGION = (-7.4, 7.4, FLOOR_Y, 4.2)


# ---------------------------------------------------------------- polygons
def clip_halfplane(poly, n, c):
    """Keep the part of polygon `poly` (list of 2D points) with n·x <= c (Sutherland-Hodgman)."""
    out = []
    L = len(poly)
    for k in range(L):
        A, B = poly[k], poly[(k + 1) % L]
        ina, inb = n @ A <= c, n @ B <= c
        if ina:
            out.append(A)
        if ina != inb:
            t = (c - n @ A) / (n @ (B - A))
            out.append(A + t * (B - A))
    return out


def rect_poly(x0, x1, y0, y1):
    return [np.array(p, float) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]


def rounded_rect_poly(cx, cy, w, h, r, k=7):
    pts = []
    for (sx, sy, a0) in ((1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)):
        ccx, ccy = cx + sx * (w / 2 - r), cy + sy * (h / 2 - r)
        for i in range(k + 1):
            a = np.radians(a0 + 90 * i / k)
            pts.append(np.array([ccx + r * np.cos(a), ccy + r * np.sin(a)]))
    return pts


def inside(poly, p):
    """Point-in-polygon (ray casting). poly: (N,2) array."""
    x, y = p
    xs, ys = poly[:, 0], poly[:, 1]
    xs2, ys2 = np.roll(xs, -1), np.roll(ys, -1)
    cond = (ys > y) != (ys2 > y)
    with np.errstate(divide="ignore", invalid="ignore"):
        xint = xs + (y - ys) * (xs2 - xs) / (ys2 - ys)
    return bool(np.sum(cond & (x < xint)) % 2)


def edge_dist(poly, p):
    """Distance from p to the boundary of a densely sampled polygon."""
    return float(np.min(np.linalg.norm(poly - np.asarray(p)[:2], axis=1)))


# ---------------------------------------------------------------- checkerboard + warp
CHECK_COLS = range(-4, 5)      # column i covers x in [2i-1, 2i+1]
CHECK_ROWS = range(0, 4)       # row j covers y in [FLOOR_Y + 2j, FLOOR_Y + 2j + 2]


def check_color(i, j):
    """0 = blue, 1 = yellow. The square [-1,1] x [-0.5,1.5] (i=0, j=1) is blue."""
    return (i + j + 1) % 2


def square_outline(i, j, n=28):
    x0, y0 = 2 * i - 1, FLOOR_Y + 2 * j
    c = [(x0, y0), (x0 + 2, y0), (x0 + 2, y0 + 2), (x0, y0 + 2)]
    pts = []
    for k in range(4):
        a, b = np.array(c[k], float), np.array(c[(k + 1) % 4], float)
        for t in np.linspace(0, 1, n, endpoint=False):
            pts.append(a + t * (b - a))
    return np.array(pts)


WARP_A = 0.46


def _ramp(y):
    t = np.clip((y - FLOOR_Y) / 1.3, 0, 1)
    return t * t * (3 - 2 * t)


def warp(p):
    """Smooth fold-free warp (|d dx/dy| * |d dy/dx| < 1). Keeps the floor line y = FLOOR_Y fixed."""
    x, y = p[0], p[1]
    s = _ramp(y)
    dx = WARP_A * s * (np.sin(1.25 * y + 0.9) + 0.3 * np.sin(2.3 * y - 1.1))
    dy = WARP_A * s * (np.sin(1.1 * x + 2.0) + 0.3 * np.sin(2.1 * x + 0.4))
    return np.array([x + dx, y + dy] + ([p[2]] if len(p) > 2 else []))


def best_segment(poly, length=U, near=None):
    """Find a segment of `length` inside poly with the largest clearance; returns (a, b, clearance)."""
    lo, hi = poly.min(axis=0), poly.max(axis=0)
    best = (None, None, -1)
    for cx in np.linspace(lo[0], hi[0], 17):
        for cy in np.linspace(lo[1], hi[1], 17):
            c = np.array([cx, cy])
            if not inside(poly, c):
                continue
            for ang in np.radians(np.arange(0, 180, 6)):
                d = 0.5 * length * np.array([np.cos(ang), np.sin(ang)])
                samp = [c + t * d for t in np.linspace(-1, 1, 11)]
                if not all(inside(poly, q) for q in samp):
                    continue
                clr = min(edge_dist(poly, q) for q in samp)
                clr = min(clr, edge_dist(poly, c - d) * 1.0, edge_dist(poly, c + d))
                if near is not None:
                    clr -= 0.02 * np.linalg.norm(c - near)
                if clr > best[2]:
                    best = (c - d, c + d, clr)
    return best


# ---------------------------------------------------------------- two-colour mosaic
def _field(p):
    x, y = p[..., 0], p[..., 1]
    return (np.sin(1.05 * x + 0.4) + np.sin(0.83 * y - 0.45 * x + 1.7)
            + 0.8 * np.sin(1.7 * y + 1.25 * x + 0.3))


def mosaic(region, spacing, seed, noise=1.1, field_scale=1.0, field_shift=(0, 0)):
    """Two-colour Voronoi mosaic clipped to `region` (a convex polygon: list of 2D points).
    Returns (seeds (N,2), colours (N,) in {0,1}, cells: list of polygons)."""
    rng = np.random.default_rng(seed)
    poly = np.array(region)
    lo, hi = poly.min(axis=0) - spacing, poly.max(axis=0) + spacing
    xs = np.arange(lo[0], hi[0] + 1e-9, spacing)
    ys = np.arange(lo[1], hi[1] + 1e-9, spacing * SQ3 / 2)
    S = []
    for r, y in enumerate(ys):
        for x in xs:
            S.append([x + (spacing / 2 if r % 2 else 0), y])
    S = np.array(S) + rng.uniform(-0.36, 0.36, (len(S), 2)) * spacing
    f = _field((S + np.array(field_shift)) * field_scale) + noise * rng.normal(size=len(S))
    col = (f > 0).astype(int)
    tree = cKDTree(S)
    cells = []
    for i, s in enumerate(S):
        cp = [np.array(p, float) for p in region]
        for j in tree.query_ball_point(s, 3.2 * spacing):
            if j == i:
                continue
            n = S[j] - s
            cp = clip_halfplane(cp, n, n @ (S[j] + s) / 2)
            if len(cp) < 3:
                break
        cells.append(cp if len(cp) >= 3 else [])
    return S, col, cells


class Painting:
    """Colour lookup on a mosaic: which colour is under a point, and how far a different colour is."""

    def __init__(self, seeds, cols):
        self.S, self.col = seeds, cols
        self.tree = cKDTree(seeds)

    def color_at(self, p):
        return int(self.col[self.tree.query(np.asarray(p)[:2])[1]])

    def margin(self, p):
        """Lower bound on the distance from p to the nearest point of a differently coloured cell."""
        p = np.asarray(p)[:2]
        i = self.tree.query(p)[1]
        si, ci = self.S[i], self.col[i]
        m = np.inf
        for j in self.tree.query_ball_point(p, 3.0):
            if self.col[j] == ci:
                continue
            n = self.S[j] - si
            c = n @ (self.S[j] + si) / 2
            m = min(m, (c - n @ p) / np.linalg.norm(n))
        return m


# ---------------------------------------------------------------- triangle rig
P0 = np.array([-1.0, -0.2])
Q0 = np.array([1.0, -0.2])
R0 = np.array([0.0, -0.2 + SQ3])      # upper crossing of the two rings
R1 = np.array([0.0, -0.2 - SQ3])      # lower crossing
G0 = (P0 + Q0 + R0) / 3
OFFS = [P0 - G0, Q0 - G0, R0 - G0]    # vertex offsets from the centroid at full size


def rot2(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def tri_points(c, th, s):
    return [np.asarray(c)[:2] + s * rot2(o, th) for o in OFFS]


def find_spot(paint, target, s, want_major, radius=1.1, min_margin=0.17, seed=0):
    """A placement (centre, angle) near `target` whose three dots are split 2:1 with the pair in colour
    `want_major`, every dot at least `min_margin` inside its colour. Deterministic."""
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(6000):
        c = np.asarray(target) + rng.uniform(-radius, radius, 2)
        th = rng.uniform(-np.pi / 3, np.pi / 3)
        pts = tri_points(c, th, s)
        cols = [paint.color_at(p) for p in pts]
        if sorted(cols).count(want_major) != 2:
            continue
        m = min(paint.margin(p) for p in pts)
        score = m - 0.04 * np.linalg.norm(c - target)
        if m >= min_margin and (best is None or score > best[0]):
            best = (score, c, th, cols, m)
    return best

