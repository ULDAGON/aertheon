"""S11_Today: five, six or seven. Why it is hard, then back to the line, the floor, the stick and the paints.

Scale: the floor uses U = 2.0 manim per unit (the same as S01/S03), and its hexagons are geom's Isbell
colouring (side HEX_SIDE = 0.45 unit). The stick is exactly one unit on that floor at all times: hovering is
shown by a thicker line, bigger ends and a shadow (S01's convention), never by a longer stick, and during the
final pull-back it scales with the floor. Both landings are checked at import time: two different colours,
each end well inside its hexagon.

The opening's paint mosaic and box of paints are copies of S01's (build_mosaic seed 5, spacing 0.62; tray
corner 0.3, height 0.72, swatch radius 0.21 at UP*3.2), duplicated here because scenes never import each other.

No camera moves (the scoreboard stays on screen); every zoom scales the content about the frame centre.
The pull-back updater sits on the floor itself, so the renderer redraws the floor on every frame.
Overlapping beats inside one play() are staggered with `win()` rate functions, so the clock stays exact.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

from scipy.spatial import Voronoi  # noqa: E402

U = 2.0                 # manim units per problem unit on the floor
FLOOR_OP = 0.6          # paint opacity of the floor while it morphs (matches the opening mosaic)
FLOOR_HEX = 0.82        # ... and once it has settled into hexagons (reads as S07's bright pattern, FILL 0.88)
FLOOR_DIM = 0.2
FIVE = [BLUE_P, YELLOW_P, PINK_P, PURPLE_P, TEAL_P]   # a "5-colour" palette (no green: GOOD owns it)
GREEN_I = PALETTE.index(GREEN_P)

LEFT_C = np.array([-3.7, 0.45, 0.0])    # centre of the left half (the trap)
RIGHT_C = np.array([3.7, 0.45, 0.0])    # centre of the right half (the pattern)
HDR_Y = 2.85
LAB1_Y, LAB2_Y = -1.65, -2.18           # labels under the P2/P3 halves
LAB5_Y = -1.53                          # labels under the P5 lenses
HALF_K = 1.2                            # the P2/P3 halves are drawn 1.2x


def win(total, start, dur, base=smooth):
    """Rate function for an animation inside a play of length `total` that runs from `start` for `dur` s."""
    s = start / total
    e = min(1.0, (start + dur) / total)

    def f(t):
        return base(float(np.clip((t - s) / max(e - s, 1e-6), 0.0, 1.0)))
    return f


# ------------------------------------------------------------------ small drawing helpers
def seg_points(polys):
    """Closed polygons -> one point array of straight cubic segments (for a batched VMobject)."""
    out = []
    for poly in polys:
        poly = [np.array([p[0], p[1], 0.0]) for p in poly]
        for a, b in zip(poly, poly[1:] + poly[:1]):
            out += [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]
    return np.array(out)


def lines_points(pairs):
    out = []
    for a, b in pairs:
        a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
        out += [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]
    return np.array(out)


def labelled(txt, size=28, color=INK):
    t = T(txt, size, color)
    t.set_stroke(BG, width=7, background=True)
    return t


def header(a, b, pointing_right=True):
    """'5 → 6' or '6 ← 7' in number font with a drawn arrow."""
    na, nb = N(a, 52), N(b, 52)
    arr = Arrow(LEFT * 0.42, RIGHT * 0.42, buff=0, color=ACCENT, stroke_width=5,
                max_tip_length_to_length_ratio=0.32, max_stroke_width_to_length_ratio=12)
    if not pointing_right:
        arr.rotate(PI)
    g = VGroup(na, arr, nb).arrange(RIGHT, buff=0.22)
    return g, na, arr, nb


def lens(center, r):
    """A dark round window, so an overlay reads over the painted floor."""
    return Circle(radius=r).set_fill(BG, 0.8).set_stroke(FAINT, 1.5, opacity=0.8).move_to(center)


# ------------------------------------------------------------------ the '?'-shaped trap (a genuine unit-distance web)
def _q_centerline():
    c, R = np.array([0.0, 0.8]), 0.62
    th = np.linspace(np.radians(162), np.radians(-72), 140)
    arc = c + R * np.c_[np.cos(th), np.sin(th)]
    stem_end = np.array([0.03, -0.3])
    stem = arc[-1] + np.linspace(0, 1, 30)[1:, None] * (stem_end - arc[-1])
    return np.vstack([arc, stem])


def q_cloud(a=0.165, half_w=0.2, dot_c=(0.03, -0.93), dot_r=0.26, tilt=0.12):
    """Triangular-lattice points inside a '?' (local coords, about 2.75 tall), joined when exactly `a` apart.
    Returns (points (n,2), edges (m,2), order-parameter per point)."""
    line = _q_centerline()
    s_line = np.linspace(0, 1, len(line))
    pts, par = [], []
    for i in range(-24, 25):
        for j in range(-24, 25):
            p = rot([i * a + j * a / 2, j * a * SQ3 / 2], tilt)
            d = np.linalg.norm(line - p, axis=1)
            k = int(np.argmin(d))
            if d[k] < half_w:
                pts.append(p); par.append(s_line[k])
            elif np.linalg.norm(p - np.array(dot_c)) < dot_r:
                pts.append(p); par.append(1.08)
    P = np.array(pts)
    E = [(i, j) for i in range(len(P)) for j in range(i + 1, len(P)) if abs(dist(P[i], P[j]) - a) < 1e-6]
    return P, np.array(E), np.array(par)


Q_P, Q_E, Q_PAR = q_cloud()
Q_P = Q_P - (Q_P.max(axis=0) + Q_P.min(axis=0)) / 2      # centre the glyph


def make_cloud(center, scale=1.0, dot_r=0.04):
    P = Q_P * scale
    order = np.argsort([max(Q_PAR[i], Q_PAR[j]) for i, j in Q_E], kind="stable")
    E = Q_E[order]
    sticks = VMobject()
    sticks.set_points(lines_points([(P[i], P[j]) for i, j in E]))
    sticks.set_fill(opacity=0).set_stroke(UNIT_COLOR, width=2.4, opacity=0.7)
    dots = VGroup(*[Dot(np.array([p[0], p[1], 0]), radius=dot_r, color=INK)
                    for p in P[np.argsort(Q_PAR, kind="stable")]])
    g = VGroup(sticks, dots).shift(center)
    return g, sticks, dots


def cloud_anims(sticks, dots, total, start, dur):
    return [Create(sticks, rate_func=win(total, start, dur, linear)),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03,
                        rate_func=win(total, start, dur, linear))]


# ------------------------------------------------------------------ hexagon patch -> polygon mosaic -> speckles
PATCH_S = 0.3      # hexagon side in manim units inside the small patch
PATCH_R = 1.75


def patch_cells(seed=4):
    rng = np.random.default_rng(seed)
    cells = []
    R = int(PATCH_R / PATCH_S) + 3
    for q in range(-R, R + 1):
        for r in range(-R, R + 1):
            c = hex_center(q, r, PATCH_S)
            if np.linalg.norm(c) <= PATCH_R - 0.12:
                cells.append((c, hex_color(q, r)))
    jit = {}

    def j(p, amt):
        key = (round(p[0], 4), round(p[1], 4))
        if key not in jit:
            jit[key] = rng.uniform(-1, 1, 2) * amt
        return p + jit[key]

    hexes, irregular, colors = [], [], []
    for c, col in cells:
        v = hex_vertices(c, PATCH_S)
        reg, irr = [], []
        for k in range(6):
            a, b = v[k], v[(k + 1) % 6]
            m = (a + b) / 2
            reg += [a, m]
            irr += [j(a, 0.36 * PATCH_S), j(m, 0.3 * PATCH_S)]
        hexes.append(reg); irregular.append(irr); colors.append(col)
    return hexes, irregular, colors


def poly_mob(pts, color, center, op=0.9):
    p = Polygon(*[np.array([x, y, 0]) + center for x, y in pts])
    return p.set_fill(color, op).set_stroke(BG, width=1.5)


def as_hole(m):
    """An unpainted cell: dark, with a faint outline (the hexagon version of ring())."""
    return m.set_fill(BG, 1).set_stroke(DIM, width=1.5)


def speckle(center, R=PATCH_R, px=0.05, seed=9, buckets=5, op=0.92,
            c=complex(-0.8, 0.156), view=(0.3, 0.1), span=0.35, noise=0.06):
    """A fine, fractal-looking five-colour texture in a disc: Julia-set escape bands plus speckle noise.
    Returns a VGroup of batched VMobjects (colour x random bucket), for a dissolve."""
    rng = np.random.default_rng(seed)
    n = int(R / px)
    xs = np.arange(-n, n + 1) * px
    X, Y = np.meshgrid(xs, xs)
    Z = (view[0] + X / R * span) + 1j * (view[1] + Y / R * span)
    K = np.zeros(Z.shape, int)
    alive = np.ones(Z.shape, bool)
    for k in range(120):
        Z[alive] = Z[alive] ** 2 + c
        esc = alive & (np.abs(Z) > 2)
        K[esc] = k
        alive &= ~esc
    K[alive] = 120
    ci = K % 5
    m = rng.random(K.shape) < noise
    ci[m] = rng.integers(0, 5, int(m.sum()))
    bk = rng.integers(0, buckets, K.shape)
    inside = X ** 2 + Y ** 2 <= (R - px / 2) ** 2
    h = px / 2 * 0.99
    mobs = VGroup()
    for col in range(5):
        for b in range(buckets):
            sel = inside & (ci == col) & (bk == b)
            if not sel.any():
                continue
            sq = [[(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)] for x, y in zip(X[sel], Y[sel])]
            v = VMobject()
            v.set_points(seg_points(sq))
            v.set_fill(FIVE[col], op).set_stroke(width=0)
            mobs.add(v)
    return mobs.shift(center)


# ------------------------------------------------------------------ the opening's paint mosaic (copy of S01's)
S01_HALF = UNIT / 2


def _s01_ends(c, th):
    d = S01_HALF * np.array([np.cos(th), np.sin(th), 0.0])
    return c - d, c + d


_A1, _B1 = _s01_ends(np.array([0.5, -0.55, 0.0]), 60 * DEGREES)
_A2, _B2 = _s01_ends(np.array([-2.5, 0.85, 0.0]), 130 * DEGREES)
S01_SPECIAL = [(_A1, BLUE_P), (_B1, PINK_P), (_A2, PURPLE_P), (_B2, YELLOW_P),
               (np.array([-4.3, 1.45, 0]), ORANGE_P), (np.array([3.7, 1.25, 0]), TEAL_P),
               (np.array([2.5, -1.95, 0]), YELLOW_P), (np.array([-3.1, -1.7, 0]), GREEN_P)]


def build_mosaic(seed=5, spacing=0.62):
    """S01's Voronoi 'paint mosaic' (same seed, same tiles, same colours).
    Returns (polygons: list of (k,2) vertex arrays, seeds (N,2), colour indices)."""
    rng = np.random.default_rng(seed)
    xs = np.arange(-8.2, 8.21, spacing)
    ys = np.arange(-5.0, 5.01, spacing * 0.9)
    pts = []
    for j, y in enumerate(ys):
        for x in xs:
            p = np.array([x + (spacing / 2 if j % 2 else 0), y]) + rng.uniform(-0.2, 0.2, 2)
            pts.append(p)
    pts = np.array(pts)
    sp = np.array([s[0][:2] for s in S01_SPECIAL])
    keep = np.min(np.linalg.norm(pts[:, None, :] - sp[None, :, :], axis=2), axis=1) > 0.45
    pts = np.vstack([sp, pts[keep]])
    n = len(pts)
    far = np.array([[x, y] for x in (-30, 0, 30) for y in (-30, 0, 30) if (x, y) != (0, 0)])
    vor = Voronoi(np.vstack([pts, far]))
    nb = [set() for _ in range(n)]
    for a, b in vor.ridge_points:
        if a < n and b < n:
            nb[a].add(b)
            nb[b].add(a)
    col = [None] * n
    for i, (_, c) in enumerate(S01_SPECIAL):
        col[i] = PALETTE.index(c)
    order = sorted(range(len(S01_SPECIAL), n), key=lambda i: np.linalg.norm(pts[i]))
    for i in order:
        used = {col[k] for k in nb[i] if col[k] is not None}
        free = [c for c in range(7) if c not in used]
        col[i] = int(rng.choice(free)) if free else int(rng.integers(7))
    polys = []
    for i in range(n):
        reg = vor.regions[vor.point_region[i]]
        assert -1 not in reg and reg
        polys.append(vor.vertices[reg])
    return polys, pts, col


# ------------------------------------------------------------------ Isbell's hexagon floor
FLOOR = hex_cells(7.8)                                   # problem units; covers the frame even at zoom 0.55
FC = np.array([c for _q, _r, c, _k in FLOOR])
FCOL = np.array([k for _q, _r, _c, k in FLOOR])
_DD = SQ3 * HEX_SIDE


def floor_look(p):
    """(colour index, distance to the nearest hexagon border) of floor point p (problem units)."""
    d = np.linalg.norm(FC - np.asarray(p)[:2], axis=1)
    o = np.argsort(d)[:2]
    return int(FCOL[o[0]]), (d[o[1]] ** 2 - d[o[0]] ** 2) / (2 * _DD)


def check_landing(c, ang):
    e = 0.5 * np.array([np.cos(ang), np.sin(ang)])
    (ca, ma), (cb, mb) = floor_look(np.asarray(c) - e), floor_look(np.asarray(c) + e)
    assert ca != cb and min(ma, mb) > 0.1, (c, ang, ca, cb, ma, mb)
    return ca, cb


CK_OFF, CK_SIZE, CK_R = 0.64, 0.28, 0.34     # check mark: offset from the stick, size, dark disc behind it


def up_normal(ang):
    u = np.array([np.cos(ang), np.sin(ang)])
    nrm = np.array([-u[1], u[0]])
    return -nrm if nrm[1] < -1e-9 else nrm


def check_side(c, ang, z):
    """+1 / -1: the side of the stick whose floor under the check is not green (GOOD must not sit on green)."""
    nrm = up_normal(ang)
    for s in (1, -1):
        if floor_look(np.asarray(c) + s * nrm * CK_OFF / (U * z))[0] != GREEN_I:
            return s
    return 1


# landings (problem units, radians): verified two different colours, ends > 0.1 unit from any border
LAND4_C, LAND4_A = np.array([0.3, 0.2]), np.radians(39 + 180)     # blue / yellow
LAND6_C, LAND6_A = np.array([0.7, 0.8]), np.radians(90 + 180)     # yellow / purple
Z_END = 0.55                                                      # floor zoom at the end of the pull-back
check_landing(LAND4_C, LAND4_A)
check_landing(LAND6_C, LAND6_A)
SIDE4 = check_side(LAND4_C, LAND4_A, 1.0)
SIDE6 = check_side(LAND6_C, LAND6_A, Z_END)


# ------------------------------------------------------------------ scene
class S11_Today(TimedScene):
    def construct(self):
        # ============================================================ P1: five, six or seven
        bar = BoundsBar(lo=5, hi=7).scale(0.8).to_edge(DOWN, buff=0.3)
        panel = RoundedRectangle(width=bar.width + 0.5, height=bar.height + 0.3, corner_radius=0.22)
        panel.set_fill(BG, 1).set_stroke(width=0).move_to(bar)
        barg = VGroup(panel, bar).set_z_index(10)
        HOME = barg.get_center()
        BIG_K, BIG_C = 1.7, np.array([0.0, 0.25, 0.0])     # S10's "the scoreboard moved" pose
        big = barg.copy().scale(BIG_K).move_to(BIG_C)
        q_big = N("?", 110, ACCENT).next_to(big[1].title, UP, buff=0.35).set_x(big[1].box.get_x())
        q_small = N("?", 110, ACCENT).scale(1 / BIG_K).next_to(bar.title, UP, buff=0.25).set_x(bar.box.get_x())

        self.until("p1", FadeIn(barg))
        self.at("stand", barg.animate.scale(BIG_K).move_to(BIG_C), run_time=1.0)
        self.at("five", Indicate(bar.cells[4], color=ACCENT, scale_factor=1.35), run_time=0.62)
        self.at("six", Indicate(bar.cells[5], color=ACCENT, scale_factor=1.35), run_time=0.42)
        self.at("seven", Indicate(bar.cells[6], color=ACCENT, scale_factor=1.35), run_time=0.6)
        qmark = q_big.copy()
        self.at(3.5, FadeIn(qmark, shift=UP * 0.2), run_time=0.55)

        # ============================================================ P2: do five colours fail somewhere? none known
        self.at("p2", barg.animate.scale(1 / BIG_K).move_to(HOME), Transform(qmark, q_small), run_time=0.9)

        hl, hl5, hl_arr, hl6 = header("5", "6", True)
        hl.move_to([LEFT_C[0], HDR_Y, 0])
        self.at(6.45, FadeIn(hl5, shift=DOWN * 0.15), Indicate(bar.cells[4], color=ACCENT, scale_factor=1.4),
                run_time=0.55)
        self.at(7.0, GrowArrow(hl_arr), FadeIn(hl6, shift=LEFT * 0.15), run_time=0.5)

        # the '?' flies up and becomes a web of sticks shaped like a '?': the trap nobody has found
        cloud, c_sticks, c_dots = make_cloud(LEFT_C, scale=HALF_K, dot_r=0.045)
        q0 = qmark.copy()
        qk = cloud.height / qmark.height

        def fly(m, a):     # a: 0..1 over 1.2 s: arrive by 0.55, fade from 0.45 while the web writes over it
            k = smooth(min(1.0, a / 0.55))
            m.become(q0.copy().scale(1 + (qk - 1) * k).move_to(interpolate(q0.get_center(), LEFT_C, k)))
            m.set_opacity(1 - smooth(float(np.clip((a - 0.45) / 0.55, 0, 1))))

        lab_trap = labelled("5 colors fail?", 28).move_to([LEFT_C[0], LAB1_Y, 0])
        TT = 1.8
        self.at("trap_six",
                UpdateFromAlphaFunc(qmark, fly, rate_func=win(TT, 0, 1.2, linear)),
                *cloud_anims(c_sticks, c_dots, TT, 0.5, 1.05),
                FadeIn(lab_trap, shift=UP * 0.1, rate_func=win(TT, 1.25, 0.55)),
                run_time=TT)
        self.remove(qmark)
        lab_none = labelled("none known", 26, DIM).move_to([LEFT_C[0], LAB2_Y, 0])
        self.at("none", FadeIn(lab_none, shift=UP * 0.1),
                c_dots.animate.set_opacity(0.35), c_sticks.animate.set_stroke(opacity=0.25), run_time=0.8)

        # ============================================================ P3: a better pattern would be strange
        hr, hr6, hr_arr, hr7 = header("6", "7", False)
        hr.move_to([RIGHT_C[0], HDR_Y, 0])
        hexes, irregular, pidx = patch_cells()
        hex_mobs = VGroup(*[poly_mob(h, PALETTE[k], RIGHT_C) for h, k in zip(hexes, pidx)])
        by_r = sorted(range(len(hex_mobs)), key=lambda i: np.linalg.norm(hex_mobs[i].get_center() - RIGHT_C))
        MISSING = PALETTE.index(TEAL_P)          # the colour a "better" pattern would try to do without
        miss = [i for i, k in enumerate(pidx) if k == MISSING]

        # "the seven": the 7-colour hexagon patch grows with the 7 (it is the reason for the seven)
        TH = 1.45
        self.at(13.35, FadeIn(hr7, shift=DOWN * 0.15, rate_func=win(TH, 0, 0.55)),
                Indicate(bar.cells[6], color=ACCENT, scale_factor=1.4, rate_func=win(TH, 0, 0.55, there_and_back)),
                LaggedStart(*[GrowFromCenter(hex_mobs[i]) for i in by_r], lag_ratio=0.025,
                            rate_func=win(TH, 0.05, 1.1, linear)),
                GrowArrow(hr_arr, rate_func=win(TH, 0.55, 0.5)),
                FadeIn(hr6, shift=RIGHT * 0.15, rate_func=win(TH, 0.55, 0.5)),
                run_time=TH)

        # "a better pattern" = fewer colours: one paint goes missing and leaves holes
        lab_fewer = labelled("fewer colors?", 28, DIM).move_to([RIGHT_C[0], LAB1_Y, 0])
        TB = 1.0
        self.at("better", FadeIn(lab_fewer, shift=UP * 0.1, rate_func=win(TB, 0, 0.5)),
                *[as_hole(hex_mobs[i].animate(rate_func=win(TB, 0.3, 0.6))) for i in miss],
                run_time=TB)

        # "ordinary polygon patches": they wobble into irregular polygons ... "need all seven": the holes refill
        irr_mobs = [poly_mob(h, PALETTE[k], RIGHT_C) for h, k in zip(irregular, pidx)]
        for i in miss:
            as_hole(irr_mobs[i])
        lab_poly = labelled("polygon patches", 28).move_to([RIGHT_C[0], LAB1_Y, 0])
        lab_seven = labelled("7 needed", 26, DIM).move_to([RIGHT_C[0], LAB2_Y, 0])
        TP = self.t("p3s2") + 1.94 - self.t("polygons")      # until "need" (18.34)
        self.at("polygons",
                *[Transform(h, g, rate_func=win(TP, 0, 1.3)) for h, g in zip(hex_mobs, irr_mobs)],
                FadeOut(lab_fewer, rate_func=win(TP, 0, 0.35)),
                FadeIn(lab_poly, shift=UP * 0.1, rate_func=win(TP, 0.56, 0.5)),
                run_time=TP)
        self.play(*[hex_mobs[i].animate.set_fill(PALETTE[MISSING], 0.9).set_stroke(BG, 1.5) for i in miss],
                  FadeIn(lab_seven, shift=UP * 0.1), run_time=0.5)

        spk = speckle(RIGHT_C)
        rng = np.random.default_rng(3)
        polys = list(hex_mobs)
        rng.shuffle(polys)
        spk_order = list(spk)
        rng.shuffle(spk_order)
        lab_strange = labelled("strange?", 32, ACCENT).move_to([RIGHT_C[0], (LAB1_Y + LAB2_Y) / 2, 0])
        TS = 1.4
        self.at("strange",
                LaggedStart(*[FadeOut(p, scale=0.6) for p in polys], lag_ratio=0.02, rate_func=win(TS, 0, 1.2, linear)),
                LaggedStart(*[FadeIn(m) for m in spk_order], lag_ratio=0.1, rate_func=win(TS, 0, 1.2, linear)),
                FadeOut(lab_poly, rate_func=win(TS, 0.35, 0.4)), FadeOut(lab_seven, rate_func=win(TS, 0.35, 0.4)),
                FadeIn(lab_strange, scale=0.9, rate_func=win(TS, 0.64, 0.5)),
                run_time=TS)

        # ============================================================ P4: the line needs two; the floor 5, 6 or 7
        LY = 1.2
        stripes = VGroup()
        for k in range(-4, 4):
            x0, x1 = max(-6.6, k * U), min(6.6, (k + 1) * U)
            stripes.add(Rectangle(width=x1 - x0, height=0.14, stroke_width=0)
                        .set_fill(BLUE_P if k % 2 == 0 else YELLOW_P, 1).move_to([(x0 + x1) / 2, LY, 0]))
        ticks = VGroup(*[Line([k * U, LY - 0.17, 0], [k * U, LY + 0.17, 0], color=FAINT, stroke_width=2)
                         for k in range(-3, 4)])
        line_g = VGroup(ticks, stripes)
        lab_line = labelled("line: 2", 36, ACCENT).move_to([0, LY + 1.35, 0])

        lx = ValueTracker(-2.15)      # left end of the line-stick, in units
        lop = ValueTracker(0.0)

        def line_stick():
            x, o = lx.get_value(), lop.get_value()
            a, b = np.array([x * U, LY + 0.42, 0]), np.array([(x + 1) * U, LY + 0.42, 0])
            s = stick(a, b, width=5).set_stroke(opacity=o)
            ea = pt(a, PALETTE[line_color(x)], r=0.1).set_opacity(o)
            eb = pt(b, PALETTE[line_color(x + 1)], r=0.1).set_opacity(o)
            ck = check_mark((a + b) / 2 + UP * 0.34, size=0.16).set_stroke(opacity=o)
            return VGroup(s, ea, eb, ck)

        lstick = always_redraw(line_stick)
        self.add(lstick)
        # the halves clear fast; the line slides in on the word "line", the stick and "line: 2" on "two"
        halves = VGroup(hl, cloud, lab_trap, lab_none, hr, spk, lab_strange)
        TL = self.t("p4s2") - self.t("p4")
        o_line = self.t("line") - 0.46 - self.t("p4")        # ~23.0: "line" is spoken at 22.96
        o_two = self.t("p4s1") + 1.36 - self.t("p4")         # "two" at 24.04
        self.at("p4",
                FadeOut(halves, rate_func=win(TL, 0, 0.4)),
                FadeIn(line_g, shift=RIGHT * 3, rate_func=win(TL, o_line, 0.5)),
                lop.animate(rate_func=win(TL, o_two - 0.34, 0.4)).set_value(1.0),
                FadeIn(lab_line, shift=UP * 0.1, rate_func=win(TL, o_two, 0.45)),
                lx.animate(rate_func=win(TL, o_two - 0.04, TL - o_two + 0.04)).set_value(-0.3),
                run_time=TL)
        self.remove(*polys)

        # the painted floor of the opening blooms back (S01's mosaic, S01's bloom) ...
        m_polys, m_seeds, m_col = build_mosaic()
        mos_mobs = VGroup()
        for poly, sd, k in zip(m_polys, m_seeds, m_col):
            p = Polygon(*[np.array([x, y, 0.0]) for x, y in poly])
            p.set_fill(PALETTE[k], 0).set_stroke(BG, 1.6, 0)
            p.base = p.points.copy()
            p.seed = np.array([sd[0], sd[1], 0.0])
            p.r = float(np.linalg.norm(sd))
            mos_mobs.add(p)
        span = 9.6                                   # past the frame corner (8.2) + the 1.0 bloom edge
        self.add(mos_mobs)

        def bloom(m, a):
            B = a * span
            for c in m:
                p = float(np.clip((B - c.r) / 1.0, 0, 1))
                k = 0.3 + 0.7 * rate_functions.ease_out_cubic(p)
                c.points = c.seed + (c.base - c.seed) * k
                c.set_fill(opacity=FLOOR_OP * p).set_stroke(opacity=p)

        TF = self.t("floor") - self.t("p4s2")
        self.at("p4s2",
                FadeOut(line_g, rate_func=win(TF, 0, 0.4)), FadeOut(lab_line, rate_func=win(TF, 0, 0.4)),
                lop.animate(rate_func=win(TF, 0, 0.4)).set_value(0.0),
                UpdateFromAlphaFunc(mos_mobs, bloom, rate_func=win(TF, 0.1, TF - 0.1, rate_functions.ease_in_out_sine)),
                run_time=TF)
        self.remove(lstick, line_g, lab_line)

        # ... and settles into Isbell's seven-colour hexagons (a genuinely valid colouring)
        floor = VGroup(*[Polygon(*[to_scene(v, U) for v in hex_vertices(c)])
                         .set_fill(PALETTE[k], FLOOR_OP).set_stroke(BG, 1.6) for _q, _r, c, k in FLOOR])
        settle = [mob.animate.set_fill(PALETTE[floor_look(mob.seed[:2] / U)[0]]) for mob in mos_mobs]

        # the stick (always exactly one floor unit; `lift` > 0 = hovering: thicker, bigger hollow ends, shadow)
        zoom = ValueTracker(1.0)
        cx, cy = ValueTracker(LAND4_C[0]), ValueTracker(LAND4_C[1])
        ang = ValueTracker(LAND4_A - np.radians(140))
        lift = ValueTracker(1.0)
        fill = ValueTracker(0.0)
        chk = ValueTracker(0.0)
        sop = ValueTracker(0.0)
        side = {"s": SIDE4}

        def floor_stick():
            z, L, o, f = zoom.get_value(), lift.get_value(), sop.get_value(), fill.get_value()
            c = np.array([cx.get_value(), cy.get_value()])
            a = ang.get_value()
            e = 0.5 * np.array([np.cos(a), np.sin(a)])
            A, B = to_scene(c - e, U * z), to_scene(c + e, U * z)
            mid = (A + B) / 2
            shadow = Line(A, B, stroke_width=9 + 3 * L, color=BG).shift(DR * 0.08 * L)
            shadow.set_stroke(opacity=0.6 * o * L)
            s = Line(A, B, color=UNIT_COLOR, stroke_width=5 + 3 * L).set_stroke(opacity=o)
            s.set_stroke(BG, width=8 + 3 * L, background=True, opacity=0.7 * o)
            ends = VGroup()
            for P_scene, P_floor in ((A, c - e), (B, c + e)):
                col = PALETTE[floor_look(P_floor)[0]]
                d = Circle(radius=0.105 + 0.03 * L).move_to(P_scene)
                d.set_fill(interpolate_color(ManimColor(BG), ManimColor(col), f), o)
                d.set_stroke(UNIT_COLOR if f < 0.5 else BG, width=2.5, opacity=o)
                ends.add(d)
            n2 = up_normal(a) * side["s"]
            pos = mid + np.array([n2[0], n2[1], 0.0]) * CK_OFF
            co = chk.get_value() * o
            disc = Circle(radius=CK_R).move_to(pos + UP * 0.075 * CK_SIZE)
            disc.set_fill(BG, 0.72 * co).set_stroke(width=0)
            ck = check_mark(pos, size=CK_SIZE).set_stroke(opacity=co)
            ck.set_stroke(BG, width=10, background=True, opacity=co)
            return VGroup(shadow, s, ends, disc, ck).set_z_index(5)

        fstick = always_redraw(floor_stick)
        self.add(fstick)
        self.at("floor", *settle, run_time=0.42)
        self.play(FadeIn(floor), FadeOut(mos_mobs), sop.animate.set_value(1.0), run_time=0.45)
        self.remove(mos_mobs)
        # "free to turn": the stick turns while hovering and the settled hexagons brighten to S07's pattern;
        # then the scoreboard steps forward for "five, six, seven"
        TU = 28.5 - self.now
        self.until(28.5, ang.animate(rate_func=win(TU, 0, 1.0)).set_value(LAND4_A),
                   floor.animate(rate_func=win(TU, 0.05, 0.9)).set_fill(opacity=FLOOR_HEX),
                   barg.animate(rate_func=win(TU, TU - 0.42, 0.4)).scale(1.25, about_edge=DOWN))
        self.at(28.57, Indicate(bar.cells[4], color=ACCENT, scale_factor=1.4), run_time=0.5)
        self.at(29.13, Indicate(bar.cells[5], color=ACCENT, scale_factor=1.4), run_time=0.45)
        # "... or seven": and in the pause it lands on two different colours while the scoreboard steps back
        TD = 1.2
        self.at(29.61, Indicate(bar.cells[6], color=ACCENT, scale_factor=1.4, rate_func=win(TD, 0, 0.5, there_and_back)),
                lift.animate(rate_func=win(TD, 0.42, 0.25)).set_value(0.0),
                fill.animate(rate_func=win(TD, 0.55, 0.3)).set_value(1.0),
                chk.animate(rate_func=win(TD, 0.7, 0.35)).set_value(1.0),
                barg.animate(rate_func=win(TD, 0.75, 0.45)).scale(1 / 1.25, about_edge=DOWN),
                run_time=TD)

        # ============================================================ P5: somewhere out there ...
        # the floor dims under "Somewhere"; the landed, checked stick stays until "there"
        T5a = self.t("p5s1") + 0.68 + 0.5 - self.t("p5")
        self.at("p5", floor.animate(rate_func=win(T5a, 0, 0.8)).set_fill(opacity=FLOOR_DIM),
                sop.animate(rate_func=win(T5a, 0.68, 0.5)).set_value(0.0),
                run_time=T5a)
        chk.set_value(0.0); fill.set_value(0.0); lift.set_value(1.0)

        lens_l = lens(LEFT_C + UP * 0.12, 1.62)
        trap2, t2_sticks, t2_dots = make_cloud(LEFT_C + UP * 0.12, scale=0.88)
        lab_trap2 = labelled("5 colors fail?", 28).move_to([LEFT_C[0], LAB5_Y, 0])
        T5 = 1.7
        self.at("trap", FadeIn(lens_l, scale=0.9, rate_func=win(T5, 0, 0.45)),
                *cloud_anims(t2_sticks, t2_dots, T5, 0.15, 1.1),
                FadeIn(lab_trap2, shift=UP * 0.1, rate_func=win(T5, 1.15, 0.5)),
                run_time=T5)
        lab_or = labelled("or", 32, DIM).move_to([0, LEFT_C[1] + 0.12, 0])
        self.at(34.8, FadeIn(lab_or), run_time=0.4)
        lens_r = lens(RIGHT_C + UP * 0.12, 1.62)
        spk2 = speckle(RIGHT_C + UP * 0.12, R=1.32, op=0.55, seed=13)
        spk2_order = list(spk2)
        rng.shuffle(spk2_order)
        q2 = N("?", 84, ACCENT).move_to(RIGHT_C + UP * 0.12)
        q2.set_stroke(BG, width=9, background=True)
        lab_pat = labelled("5 colors work?", 28).move_to([RIGHT_C[0], LAB5_Y, 0])
        T6 = 1.5
        self.at("pattern", FadeIn(lens_r, scale=0.9, rate_func=win(T6, 0, 0.45)),
                LaggedStart(*[FadeIn(m) for m in spk2_order], lag_ratio=0.1, rate_func=win(T6, 0.1, 1.0, linear)),
                FadeIn(q2, scale=0.8, rate_func=win(T6, 0.8, 0.5)),
                FadeIn(lab_pat, shift=UP * 0.1, rate_func=win(T6, 0.95, 0.5)),
                run_time=T6)
        self.at(37.3, Indicate(q2, color=ACCENT, scale_factor=1.2), run_time=0.7)
        # pause: both fade, the floor comes back
        self.at("p5_end", FadeOut(VGroup(lens_l, trap2, lab_trap2, lab_or, lens_r, spk2, q2, lab_pat)),
                floor.animate.set_fill(opacity=FLOOR_HEX), run_time=0.8)

        # ============================================================ P6: anyone with a box of paints
        # "the last big step": the struck 4 flashes and the 5 lights up (the hobbyist's 4 -> 5)
        TG = 1.05
        self.at(self.t("p6s1") + 0.16,
                Indicate(VGroup(bar.cells[3], bar.strikes[3]), color=ACCENT, scale_factor=1.35,
                         rate_func=win(TG, 0, 0.55, there_and_back)),
                Indicate(bar.cells[4], color=ACCENT, scale_factor=1.55, rate_func=win(TG, 0.35, 0.7, there_and_back)),
                run_time=TG)

        # "a hobbyist": the box of paints from the opening slides back in along the top edge
        sw = VGroup(*[Circle(radius=0.21).set_fill(c, 1).set_stroke(BG, 2) for c in PALETTE]).arrange(RIGHT, buff=0.2)
        tray = RoundedRectangle(corner_radius=0.3, width=sw.width + 0.5, height=0.72)
        tray.set_fill(BG, 0.9).set_stroke(DIM, 2)
        VGroup(tray, sw).move_to(UP * 3.2).set_z_index(10)
        T7 = 1.3
        self.at(self.t("p6s1") + 1.44, FadeIn(tray, shift=DOWN * 0.6, rate_func=win(T7, 0, 0.5)),
                LaggedStart(*[FadeIn(s, shift=DOWN * 0.25, scale=0.6) for s in sw], lag_ratio=0.18,
                            rate_func=win(T7, 0.3, 1.0, linear)),
                run_time=T7)

        # "the next one": a stick drops onto the floor, hovering
        c0, a0 = np.array([-0.45, 0.1]), np.radians(150)
        c1, a1 = LAND6_C, LAND6_A
        cx.set_value(c0[0]); cy.set_value(c0[1]); ang.set_value(a0)
        side["s"] = SIDE6
        self.at("p6s2", sop.animate.set_value(1.0), run_time=0.45)

        # "could come from anyone": pull back over the endless floor while the stick drifts, spins and lands.
        # One play drives the floor itself (so it is redrawn on every frame) from scene time, not from dt:
        # no play boundary inside the pull, so there is no stalled frame and the stick stays in register.
        T_PULL, T_MOVE, T_LAND = 2.7, 1.2, 0.25
        t_any = self.t("anyone")
        t_land = t_any + 0.1 + T_MOVE + T_LAND                            # ~43.89, on "with"
        t_box = self.t("p6s2") + 2.28                                      # "box" (44.08)
        t_pull = t_any + T_PULL + 0.05
        TE = t_pull - t_any
        clock = {"z": 1.0}

        def director(m, alpha):
            t = alpha * TE
            z = 1.0 - (1.0 - Z_END) * smooth(min(1.0, t / T_PULL))
            m.scale(z / clock["z"], about_point=ORIGIN)
            clock["z"] = z
            zoom.set_value(z)
            a = smooth(min(1.0, max(0.0, (t - 0.1) / T_MOVE)))
            cx.set_value(c0[0] + (c1[0] - c0[0]) * a)
            cy.set_value(c0[1] + (c1[1] - c0[1]) * a)
            ang.set_value(a0 + (a1 - a0) * a)
            lift.set_value(1.0 - smooth(min(1.0, max(0.0, (t - 0.1 - T_MOVE) / T_LAND))))

        self.at("anyone")
        self.until(t_pull,
                   UpdateFromAlphaFunc(floor, director, rate_func=linear),
                   fill.animate(rate_func=win(TE, t_land - 0.05 - t_any, 0.3)).set_value(1.0),
                   chk.animate(rate_func=win(TE, t_land + 0.1 - t_any, 0.35)).set_value(1.0),
                   LaggedStart(*[s.animate(rate_func=there_and_back).shift(UP * 0.14) for s in sw], lag_ratio=0.12,
                               rate_func=win(TE, t_box - t_any, 0.8, linear)))

        # final hold: the window 5-6-7 glows once, then everything fades to the empty background
        wc = bar.box.get_center()
        self.play(bar.cells[4:7].animate(rate_func=there_and_back).scale(1.2, about_point=wc).set_color(ACCENT),
                  bar.box.animate(rate_func=there_and_back).scale(1.2, about_point=wc).set_stroke(width=7),
                  run_time=0.55)
        self.until(self.t("end") - 0.8)
        fstick.clear_updaters()
        self.until("end", FadeOut(floor, fstick, tray, sw, barg))

