"""S08_Stall: sixty-eight years at four to seven.

A timeline (1950 -> 2020) whose ACCENT marker keeps moving for the whole scene while the
scoreboard window stays at 4..7:
  p1  1950: 'at least 4' on "four", the bar's window glows on "the answer sat between", Isbell's flower
      'at most 7' lands on "seven"; the marker sets off.
  p2  the title 'The Hadwiger–Nelson problem'; Hugo Hadwiger under the early 1960s.
  p3  1970, 1990, 2010: the marker lands on each tick as it is said; a ghost of the window pops
      above each; a flat line joins them: still four to seven.
  p4  the timeline parks at the top edge in exactly S09's opening style (y 3.0, x ±5.6, FAINT axis,
      small marker, thin trail), so the cut into S09 does not jump; a magnified copy of the window
      sits at centre: 'trap? · finite' (a Moser-spindle-like icon, marked hypothetical) pushes on the 4,
      'pattern · endless' (hexagon patch) pushes on the 7. Nothing moves.
  p5  an INK flag at 1951; de Bruijn & Erdős; the web of the plane's unit sticks; a search lens glides
      over it, lighting the sticks beneath; on "finite" the lens widens around one cluster whose own
      sticks brighten in place, then the web fades and the cluster lifts out inside the lens: 'trap?'
      (with the usual axioms).
  p6  Erdős: 5?  Candidates (triangle, spindle, Golomb graph, lattice patch) are painted with
      at most four colors, each gets a check. Marker reaches 2017; everything fades.

The marker is driven by a time-based updater that reads the scene's frame-exact clock, so it can
move continuously under every other animation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: F401,F403,E402
from geom import *  # noqa: F401,F403,E402
from scipy.interpolate import PchipInterpolator  # noqa: E402

# The marker's motion depends on the scene clock, which manim's play-hash cannot see.
# Never reuse a cached partial movie for this scene.
config.disable_caching = True

Y_FIRST, Y_LAST = 1950, 2020
TL_BIG_Y, TL_BIG_HALF = 1.2, 5.4        # p1-p3: timeline across the upper middle
TL_TOP_Y, TL_TOP_HALF = 3.0, 5.6        # p4-p6: parked at the top edge, styled exactly like S09's opening timeline
TAG_Y = 2.2                              # centre height of the 1950 tags and the ghost windows
PARK_DUR = 1.0                           # p4: seconds the timeline takes to park (marker/trail restyle with it)
GOLD_SOFT = interpolate_color(ManimColor(INK), ManimColor(ACCENT), 0.6)
PAINT4 = [BLUE_P, YELLOW_P, PINK_P, PURPLE_P]   # no green: GOOD check marks use it


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def glow_of(m, color=ACCENT):
    """Soft halo copies of a stroked shape (fade them in with there_and_back)."""
    return VGroup(*[m.copy().set_fill(opacity=0).set_stroke(color, width=w, opacity=o)
                    for w, o in ((18, 0.08), (11, 0.16), (6, 0.32))])


# ---------------------------------------------------------------- timeline
def axis_body(y, half, parked):
    """VGroup(line, ticks, label 1950, label 2020). The parked style is S09's opening timeline
    (FAINT axis, DIM end ticks, FAINT inner ticks, 24 pt labels), so the cut into S09 does not jump."""
    def x_of(yr):
        return -half + 2 * half * (yr - Y_FIRST) / (Y_LAST - Y_FIRST)

    if parked:
        line = Line([-half, y, 0], [half, y, 0], color=FAINT, stroke_width=3)
        th, tw, size, buff = 0.08, 2, 24, 0.16
        tcol = lambda yr: DIM if yr in (Y_FIRST, Y_LAST) else FAINT   # noqa: E731
    else:
        line = Line([-half, y, 0], [half, y, 0], color=DIM, stroke_width=3, stroke_opacity=0.75)
        th, tw, size, buff = 0.11, 2.5, 28, 0.22
        tcol = lambda yr: DIM   # noqa: E731
    ticks = VGroup(*[Line([x_of(yr), y - th, 0], [x_of(yr), y + th, 0], color=tcol(yr), stroke_width=tw)
                     for yr in range(Y_FIRST, Y_LAST + 1, 10)])
    l0 = N(str(Y_FIRST), size, DIM).next_to([x_of(Y_FIRST), y, 0], DOWN, buff=buff)
    l1 = N(str(Y_LAST), size, DIM).next_to([x_of(Y_LAST), y, 0], DOWN, buff=buff)
    return VGroup(line, ticks, l0, l1)


class Axis:
    """1950..2020 axis. `body` moves as one piece; `at(year)` always follows the live line."""

    def __init__(self):
        self.body = axis_body(TL_BIG_Y, TL_BIG_HALF, parked=False)
        self.line, self.ticks, self.l0, self.l1 = self.body

    def parked(self):
        return axis_body(TL_TOP_Y, TL_TOP_HALF, parked=True)

    def at(self, year):
        s, e = self.line.get_start(), self.line.get_end()
        return s + (year - Y_FIRST) / (Y_LAST - Y_FIRST) * (e - s)

    def tick(self, year):
        return self.ticks[(year - Y_FIRST) // 10]


def mini_window(size=30):
    """A small ghost of the scoreboard window: 4 5 6 7 in an ACCENT box."""
    digs = VGroup(*[N(d, size) for d in "4567"]).arrange(RIGHT, buff=0.17)
    box = RoundedRectangle(corner_radius=0.13, width=digs.width + 0.36, height=digs.height + 0.3,
                           color=ACCENT, stroke_width=2.5).move_to(digs)
    return VGroup(box, digs)


def hex_poly(c, s, color, opacity=1.0, stroke=1.5):
    return Polygon(*[to_scene(v, 1.0) for v in hex_vertices(c, s)], fill_color=color, fill_opacity=opacity,
                   stroke_color=BG, stroke_width=stroke)


def mini_flower(s=0.11):
    """Isbell's seven-color flower as an icon (geom.hex_color)."""
    return VGroup(*[hex_poly(hex_center(q, r, s), s, PALETTE[hex_color(q, r)], 1.0, 1.0)
                    for q, r in [(0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]])


# p4's "endless pattern": the hexagon 7-colouring seen through a fixed soft window at the right edge.
# The tiles pan slowly left under the window (entering from beyond the frame, dissolving at its left
# rim), so the pattern reads as a view onto something that goes on, not as a finite cut-out.
FIELD_S = 0.42                                 # hexagon side (manim units)
FIELD_X0, FIELD_X1 = 3.95, 5.4                 # left rim: invisible at X0, full strength from X1 on
FIELD_Y0, FIELD_Y1, FIELD_FY = -0.8, 2.55, 0.75  # bottom / top rims and their fade width
FIELD_TOP = 0.92                               # fill opacity in the middle of the window
FIELD_V0, FIELD_V, FIELD_TS = 1.5, 0.25, 1.2   # pan speed: from V0 easing to V over TS seconds (units/s)


def field_weight(c):
    return float(smoothstep((c[0] - FIELD_X0) / (FIELD_X1 - FIELD_X0))
                 * smoothstep((c[1] - FIELD_Y0) / FIELD_FY) * smoothstep((FIELD_Y1 - c[1]) / FIELD_FY))


def field_travel(u):
    """Distance the tiles have panned left u seconds after they appear."""
    u = max(u, 0.0)
    a = min(u, FIELD_TS)
    return FIELD_V * u + (FIELD_V0 - FIELD_V) * FIELD_TS / 3 * (1 - (1 - a / FIELD_TS) ** 3)


def hex_field(travel):
    """Tiles covering the window now and everything that will pan into it over `travel` units."""
    s, cells = FIELD_S, []
    R = int(16 / s)
    for q in range(-R, R + 1):
        for r in range(-R, R + 1):
            c = hex_center(q, r, s)
            if FIELD_X0 - s <= c[0] <= 7.11 + s + travel and FIELD_Y0 - s <= c[1] <= FIELD_Y1 + s:
                cells.append(hex_poly(c, s, PALETTE[hex_color(q, r)], 0.0, 2.0))
    return VGroup(*cells)


# ---------------------------------------------------------------- small unit-distance shapes
def golomb():
    """Golomb graph: wheel (centre + 6 rim) + inner unit triangle tied to alternate rim dots. 10 dots, 18 sticks."""
    th = np.arccos(SQ3 / 6)                        # makes |t_i - h_2i| = 1 for a triangle of circumradius 1/sqrt3
    P = {"c": np.zeros(2)}
    for k in range(6):
        P[f"h{k}"] = rot([1.0, 0.0], np.pi / 2 + k * np.pi / 3)
    for i in range(3):
        P[f"t{i}"] = rot([1 / SQ3, 0.0], np.pi / 2 + 2 * i * np.pi / 3 + th)
    E = [("c", f"h{k}") for k in range(6)] + [(f"h{k}", f"h{(k + 1) % 6}") for k in range(6)]
    E += [("t0", "t1"), ("t1", "t2"), ("t0", "t2")] + [(f"t{i}", f"h{2 * i}") for i in range(3)]
    col = {"c": 0, "h0": 1, "h2": 1, "h4": 1, "h1": 2, "h3": 2, "h5": 2, "t0": 0, "t1": 2, "t2": 3}
    return P, E, col


def lattice_patch():
    """Rows 3-4-3 of the triangular lattice (10 dots, 19 sticks), 3-coloured by (a + 2b) mod 3."""
    P, col = {}, {}
    for b, xs in ((-1, (-1, 0, 1)), (0, (-1.5, -0.5, 0.5, 1.5)), (1, (-1, 0, 1))):
        for x in xs:
            a = int(round(x - b / 2 + 0.5))   # row 0 sits at half-integers
            k = f"{a},{b}"
            P[k] = np.array([x, b * SQ3 / 2])
            col[k] = (a + 2 * b) % 3
    names = list(P)
    E = [(p, q) for i, p in enumerate(names) for q in names[i + 1:] if abs(dist(P[p], P[q]) - 1) < 1e-9]
    return P, E, col


def candidate_shapes():
    tri = dict(zip("ABC", triangle()))
    tri_c = {"A": 0, "B": 1, "C": 2}
    sp, sp_e = moser_spindle()
    sp_c = {"A": 0, "B": 1, "C": 2, "D": 0, "B2": 1, "C2": 3, "D2": 2}
    shapes = [(tri, [("A", "B"), ("B", "C"), ("A", "C")], tri_c), (sp, sp_e, sp_c), golomb(), lattice_patch()]
    for P, E, col in shapes:   # faithful: unit sticks, proper colouring, at most four colours
        for a, b in E:
            assert abs(dist(P[a], P[b]) - 1) < 1e-9, (a, b)
            assert col[a] != col[b], (a, b)
        assert len(set(col.values())) <= 4
    return shapes


def build_shape(P, E, col, u, center, dot_r=0.075):
    pts = {k: to_scene(v, u) for k, v in P.items()}
    arr = np.array(list(pts.values()))
    mid = (arr.min(0) + arr.max(0)) / 2
    pts = {k: v - mid + np.asarray(center) for k, v in pts.items()}
    sticks = VGroup(*[stick(pts[a], pts[b], width=3) for a, b in E])
    names = list(pts)
    dots = VGroup(*[ring(pts[k], r=dot_r) for k in names])
    painted = VGroup(*[pt(pts[k], PAINT4[col[k]], r=dot_r + 0.01) for k in names])
    return VGroup(sticks, dots), painted


# ---------------------------------------------------------------- the web (de Bruijn–Erdős)
WEB_S = 1.8                          # manim units per problem unit
WEB_C = np.array([0.0, -0.1, 0.0])
WEB_P, WEB_E = unit_web(n_points=3000, lattice_r=5)
WEB_M = WEB_C + WEB_S * np.c_[WEB_P, np.zeros(len(WEB_P))]
WEB_RX, WEB_RY = 6.8, 2.45           # the cloud: an ellipse from the bar's panel up to just under the caption


def web_weight(p):
    """Opacity weight of the web cloud: an ellipse around the frame centre, soft at every edge."""
    rr = np.sqrt((p[:, 0] / WEB_RX) ** 2 + ((p[:, 1] - WEB_C[1]) / WEB_RY) ** 2)
    return smoothstep((1 - rr) / 0.32)


def pick_cluster(target, rho=1.05, k=20):
    """k web dots around the web dot nearest `target` (problem coords) with many sticks among them:
    take the dots within rho and peel the least-connected ones."""
    adj = [set() for _ in range(len(WEB_P))]
    for a, b in WEB_E:
        adj[a].add(b)
        adj[b].add(a)
    c = WEB_P[int(np.argmin(np.linalg.norm(WEB_P - target, axis=1)))]
    S = set(np.where(np.linalg.norm(WEB_P - c, axis=1) <= rho)[0])
    while len(S) > k:
        v = min(S, key=lambda v: (len(adj[v] & S), -np.linalg.norm(WEB_P[v] - c)))
        S.remove(v)
    idx = sorted(S)
    return idx, [(a, b) for a, b in WEB_E if a in S and b in S]


def enclosing_circle(pts):
    """(centre, radius) of the smallest circle around `pts` (grid search, plenty for 20 dots)."""
    lo, hi = pts.min(0), pts.max(0)
    best = None
    for x in np.linspace(lo[0], hi[0], 61):
        for y in np.linspace(lo[1], hi[1], 61):
            r = np.linalg.norm(pts[:, :2] - [x, y], axis=1).max()
            if best is None or r < best[1]:
                best = (np.array([x, y, 0.0]), r)
    return best


# The trap-to-be: 20 dots, 44 sticks, compact (enclosing radius about 1.53 manim) and wholly in the
# middle of the web (every dot at full web opacity), right of centre around (1.36, -0.06).
CL_IDX, CL_E = pick_cluster(np.array([0.709, 0.025]), rho=0.95)
CL_PTS = WEB_M[CL_IDX]
CL_C, CL_R = enclosing_circle(CL_PTS)
assert len(CL_IDX) == 20 and len(CL_E) >= 40 and web_weight(CL_PTS).min() > 0.95

# What is drawn: a random fifth of the web's dots (plus the cluster's) with every stick among them.
# The full web has ~19.8k sticks, far too dense to read as sticks (it renders as fog); any subgraph of
# a unit-distance graph is still one, so every drawn stick is still exactly one unit.
_keep = np.random.default_rng(3).random(len(WEB_P)) < 0.2
_keep[CL_IDX] = True
WEB_DE = WEB_E[_keep[WEB_E[:, 0]] & _keep[WEB_E[:, 1]]]
WEB_DP = WEB_M[np.bincount(WEB_DE.ravel(), minlength=len(WEB_P)) > 0]      # dots with at least one stick
_cl = {tuple(sorted(e)) for e in CL_E}
assert _cl <= {tuple(sorted(e)) for e in WEB_DE.tolist()}                    # the trap is part of the drawn web
WEB_A, WEB_B = WEB_M[WEB_DE[:, 0]], WEB_M[WEB_DE[:, 1]]
WEB_MID = (WEB_A + WEB_B) / 2
WEB_WE = np.minimum(web_weight(WEB_A), web_weight(WEB_B))   # by the weaker end: no sticks poking out of the cloud
WEB_SEG = WEB_A[:, None, :] + np.array([0, 1 / 3, 2 / 3, 1])[None, :, None] * (WEB_B - WEB_A)[:, None, :]  # cubics
WEB_STICK_O = 0.4          # stick opacity at the web's middle (the sticks carry the texture)
WEB_STICK_W = 1.0
WEB_DOT_O = 0.42

_K = 0.5523
_ARC = np.array([[1, 0], [1, _K], [_K, 1], [0, 1]], float)
CIRC16 = np.c_[np.concatenate([_ARC @ np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
                               for a in (0, np.pi / 2, np.pi, 3 * np.pi / 2)]), np.zeros(16)]   # unit circle, 4 cubics


def web_mobs():
    """The web as an elliptical cloud, drawn as a few opacity bands (one VMobject each for sticks and dots)."""
    wd = web_weight(WEB_DP)
    bands = [(0.08, 0.3), (0.3, 0.55), (0.55, 0.8), (0.8, 1.01)]
    edges, dots = VGroup(), VGroup()
    for lo, hi in bands:
        sel = (WEB_WE >= lo) & (WEB_WE < hi)
        if sel.any():
            m = VMobject()
            m.set_points(WEB_SEG[sel].reshape(-1, 3))
            m.set_fill(opacity=0).set_stroke(UNIT_COLOR, width=WEB_STICK_W, opacity=WEB_STICK_O * (lo + hi) / 2)
            edges.add(m)
        sel = (wd >= lo) & (wd < hi)
        if sel.any():
            m = VMobject()
            m.set_points((WEB_DP[sel][:, None, :] + 0.026 * CIRC16[None]).reshape(-1, 3))
            m.set_stroke(width=0).set_fill(INK, opacity=WEB_DOT_O * (lo + hi) / 2)
            dots.add(m)
    return VGroup(edges, dots)


def _clip_to_disc(center, radius):
    """Pieces of the drawn web's sticks that lie inside the disc, as (N, 4, 3) straight cubics."""
    c = np.asarray(center, float)
    d = WEB_B - WEB_A
    f = WEB_A - c
    a = (d * d).sum(1)
    b = 2 * (f * d).sum(1)
    cc = (f * f).sum(1) - radius ** 2
    disc = b * b - 4 * a * cc
    ok = (disc > 0) & (WEB_WE > 0.08)
    sq = np.sqrt(np.where(ok, disc, 0.0))
    t0 = np.clip((-b - sq) / (2 * a), 0, 1)
    t1 = np.clip((-b + sq) / (2 * a), 0, 1)
    ok &= t1 > t0 + 1e-3
    P0 = WEB_A[ok] + t0[ok, None] * d[ok]
    P1 = WEB_A[ok] + t1[ok, None] * d[ok]
    return P0[:, None, :] + np.array([0, 1 / 3, 2 / 3, 1])[None, :, None] * (P1 - P0)[:, None, :]


def lens_light(center, radius, strength):
    """The search lens as a magnifier: the parts of the web's sticks inside it, and its dots, drawn
    brighter, clipped exactly at the rim (so nothing pokes out as the lens glides)."""
    c = np.asarray(center, float)
    sticks, dots = VMobject(), VMobject()
    seg = _clip_to_disc(c, radius * 0.985)
    if len(seg):
        sticks.set_points(seg.reshape(-1, 3))
    else:
        sticks.set_points(np.repeat(c[None], 4, axis=0))
    sticks.set_fill(opacity=0).set_stroke(UNIT_COLOR, width=1.6, opacity=0.8 * strength if len(seg) else 0)
    inside = WEB_DP[np.linalg.norm(WEB_DP[:, :2] - c[:2], axis=1) < radius * 0.94]
    if len(inside):
        dots.set_points((inside[:, None, :] + 0.03 * CIRC16[None]).reshape(-1, 3))
    else:
        dots.set_points(np.repeat(c[None], 4, axis=0))
    dots.set_stroke(width=0).set_fill(INK, opacity=0.75 * strength if len(inside) else 0)
    return VGroup(sticks, dots)


# ---------------------------------------------------------------- scene
class S08_Stall(TimedScene):
    def clock(self):
        """Frame-exact scene time of the frame being prepared (valid inside updaters)."""
        return (self._frames + round(self.last_t * self._fps)) / self._fps

    def construct(self):
        t = self.t
        kt = [0.0, t("pinned"), t("hadwiger"), t("seventy"), t("ninety"), t("twenty_ten"), t("p6_end"), t("end") + 5]
        ky = [1950, 1950, 1961, 1970, 1990, 2010, 2017, 2017]
        f_year = PchipInterpolator(kt, ky)
        year_at = lambda s: float(f_year(np.clip(s, kt[0], kt[-1])))   # noqa: E731

        # ---- scoreboard at its home, on a BG backing panel
        bar = BoundsBar(4, 7).scale(0.8).to_edge(DOWN, buff=0.3)
        panel = RoundedRectangle(corner_radius=0.2, width=bar.width + 0.4, height=bar.height + 0.24,
                                 stroke_width=0, fill_color=BG, fill_opacity=1).move_to(bar)
        panel.set_z_index(4)
        bar.set_z_index(6)
        halo5 = Dot(bar.cells[4].get_center(), radius=0.27, color=ACCENT).set_opacity(0.28).set_z_index(5)

        # ---- p1: the timeline, 1950 ------------------------------------------------------------
        ax = Axis()
        self.until("p1", FadeIn(panel), FadeIn(bar))
        self.play(Create(ax.line), LaggedStart(*[GrowFromCenter(tk) for tk in ax.ticks], lag_ratio=0.12),
                  FadeIn(ax.l0, shift=UP * 0.1), FadeIn(ax.l1, shift=UP * 0.1), run_time=1.2)

        # Marker and trail follow the clock. While the timeline parks (p4) they restyle to S09's
        # opening look (dot r 0.085 without halo, trail width 3 at 0.45), so the cut does not jump.
        park = {"t0": 1e9}
        park_s = lambda now: float(smoothstep((now - park["t0"]) / PARK_DUR))   # noqa: E731
        marker = VGroup(Dot(radius=0.2, color=ACCENT).set_opacity(0.25), Dot(radius=0.1, color=ACCENT))
        marker.move_to(ax.at(1950))
        trail = VMobject().set_points_as_corners([ax.at(1950), ax.at(1950)])
        trail.set_stroke(ACCENT, width=4, opacity=0.55).set_z_index(1)   # z: stay above the axis when it moves
        marker.set_z_index(2)

        def marker_upd(m, dt):
            now = self.clock()
            s = park_s(now)
            m[0].set_fill(opacity=0.25 * (1 - s))
            m[1].scale_to_fit_width(2 * (0.1 - 0.015 * s))
            m.move_to(ax.at(year_at(now)))

        def trail_upd(m, dt):
            now = self.clock()
            s = park_s(now)
            m.set_points_as_corners([ax.line.get_start(), ax.at(year_at(now))])
            m.set_stroke(width=4 - s, opacity=0.55 - 0.1 * s)

        # "in nineteen fifty": the marker appears on 1950
        self.at(1.72, GrowFromCenter(marker), ax.l0.animate(rate_func=there_and_back).set_color(ACCENT), run_time=0.5)
        self.add(trail, marker)
        marker.add_updater(marker_upd)
        trail.add_updater(trail_upd)

        # the 1950 tags: at least 4 (Nelson), at most 7 (Isbell's flower)
        row4 = VGroup(T("at least", 28), N("4", 32))
        row4[1].next_to(row4[0], RIGHT, buff=0.12, aligned_edge=DOWN)
        row7 = VGroup(T("at most", 28), N("7", 32), mini_flower(0.11))
        row7[1].next_to(row7[0], RIGHT, buff=0.12, aligned_edge=DOWN)
        row7[2].next_to(row7[1], RIGHT, buff=0.2)
        tags = VGroup(row7, row4).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        tags.move_to([ax.at(1950)[0] + 0.1, TAG_Y, 0])
        stem50 = Line(ax.at(1950) + UP * 0.16, [ax.at(1950)[0], tags.get_bottom()[1] - 0.08, 0],
                      color=DIM, stroke_width=2)
        # "four were needed"
        self.at(3.10, Create(stem50), FadeIn(row4, shift=UP * 0.12),
                Indicate(bar.cells[3], color=ACCENT, scale_factor=1.35), run_time=0.7)
        # "so the answer sat between": the window glows (and the marker sets off)
        g = glow_of(bar.box).set_z_index(5)
        self.at("pinned", FadeIn(g, rate_func=there_and_back), run_time=1.6)
        self.remove(g)
        # "...and seven": at most 7 lands on the word
        self.at(6.44, FadeIn(row7, shift=UP * 0.12), Indicate(bar.cells[6], color=ACCENT, scale_factor=1.35),
                run_time=0.7)

        # ---- p2: the name ------------------------------------------------------------------------
        title = T("The Hadwiger–Nelson problem", 40).move_to([0, -1.4, 0])   # clear of the Hadwiger caption
        self.at("name", Write(title), run_time=1.4)
        self.at(10.80, title[12:18].animate(rate_func=there_and_back).set_color(ACCENT), run_time=0.9)  # "Nelson"
        x61 = ax.at(1961)
        cap_h = VGroup(T("Hugo Hadwiger", 28), T("Swiss mathematician", 24, DIM)).arrange(DOWN, buff=0.12)
        cap_h.move_to([x61[0], 0.02, 0])
        stem61 = DashedLine(x61 + DOWN * 0.14, [x61[0], cap_h.get_top()[1] + 0.1, 0], color=DIM,
                            stroke_width=2, dash_length=0.06)
        self.at("hadwiger", FadeIn(cap_h, shift=DOWN * 0.12), Create(stem61), run_time=0.8)
        # "Hadwiger" (spoken 13.52-14.10): the highlight peaks on the word
        self.at(13.30, title[3:11].animate(rate_func=there_and_back).set_color(ACCENT), run_time=0.95)
        self.at(14.30, FadeOut(title), FadeOut(cap_h), FadeOut(stem61), run_time=0.65)

        # ---- p3: decades pass, the window does not ----------------------------------------------
        ghosts, stems, ylabs = VGroup(), VGroup(), VGroup()
        for i, (mark, year) in enumerate((("seventy", 1970), ("ninety", 1990), ("twenty_ten", 2010))):
            p = ax.at(year)
            gw = mini_window().move_to([p[0], TAG_Y, 0])
            st = Line(p + UP * 0.16, [p[0], gw.get_bottom()[1] - 0.08, 0], color=DIM, stroke_width=2)
            yl = N(str(year), 28, ACCENT).next_to(p, DOWN, buff=0.22)
            ghosts.add(gw)
            stems.add(st)
            ylabs.add(yl)
            prev = [ylabs[i - 1].animate.set_color(DIM)] if i else []   # the last year label cools as the next lands
            self.at(mark, FadeIn(gw, shift=DOWN * 0.15, scale=0.8), Create(st), FadeIn(yl, shift=UP * 0.08),
                    ax.tick(year).animate(rate_func=there_and_back).scale(1.8).set_color(ACCENT), *prev,
                    run_time=0.6)
        # "still four to seven": a flat line through every snapshot; the real window glows
        xs = [tags.get_right()[0]] + [v for gw in ghosts for v in (gw.get_left()[0], gw.get_right()[0])]
        segs = [(xs[0], xs[1])] + [(xs[2 + 2 * i], xs[3 + 2 * i]) for i in range(2)] + [(xs[-1], ax.at(2020)[0] + 0.3)]
        flat = VGroup(*[DashedLine([a + 0.14, TAG_Y, 0], [b - 0.14, TAG_Y, 0], color=ACCENT, stroke_width=2.5,
                                   dash_length=0.1) for a, b in segs])
        flat.set_opacity(0.8)
        g = glow_of(bar.box).set_z_index(5)
        self.at("frozen", LaggedStart(*[Create(s) for s in flat], lag_ratio=0.5),
                FadeIn(g, rate_func=there_and_back), ylabs[-1].animate.set_color(DIM), run_time=1.0)
        self.remove(g)
        # (the pause: the marker creeps on past 2010)

        # ---- p4: why so stuck? -------------------------------------------------------------------
        win = VGroup(bar.box.copy(), *[bar.cells[i].copy() for i in range(3, 7)]).set_z_index(7)
        win_big = win.copy().scale(1.7).move_to([0, 0.4, 0])
        # It starts invisible just above the bar's "colors needed" title and fades in as it rises, so no
        # ghost copy ever overlaps the bar; on the way back it fades out at the same spot.
        win.shift(UP * (bar.title.get_top()[1] + 0.12 - win.get_bottom()[1]))
        win_home = win.copy().set_opacity(0)
        win.set_opacity(0)
        self.add(win)
        # "Why so stuck?": clear the snapshots, park the timeline at the top, lift the window to centre
        self.at("p4", FadeOut(VGroup(tags, stem50, ghosts, stems, ylabs, flat)), run_time=0.4)
        park["t0"] = self.now
        self.play(Transform(ax.body, ax.parked()), Transform(win, win_big), run_time=PARK_DUR)
        wl, wr = win[0].get_left(), win[0].get_right()
        arr_l = Arrow(wl + LEFT * 1.6, wl + LEFT * 0.1, buff=0, color=INK, stroke_width=7,
                      max_tip_length_to_length_ratio=0.28)
        arr_r = Arrow(wr + RIGHT * 1.6, wr + RIGHT * 0.1, buff=0, color=INK, stroke_width=7,
                      max_tip_length_to_length_ratio=0.28)
        # "to push the four up"
        self.at(21.92, GrowArrow(arr_l), Indicate(win[1], color=ACCENT, scale_factor=1.3), run_time=0.6)
        # "you need one finite trap"
        # The spindle only stands for the *kind* of thing needed: S06 showed the real one stops at 4. So it
        # is drawn as a ghost (dashed, dim sticks, faint dots) under a big gold '?': "a trap nobody has".
        sp_P, sp_E = moser_spindle()
        spindle, _ = build_shape(sp_P, sp_E, {k_: 0 for k_ in sp_P}, 1.15, [-4.95, 0.4, 0], dot_r=0.085)
        spindle[0].become(VGroup(*[DashedLine(sk.get_start(), sk.get_end(), color=UNIT_COLOR, stroke_width=3,
                                              dash_length=0.07, dashed_ratio=0.55).set_stroke(opacity=0.5)
                                   for sk in spindle[0]]))
        spindle[1].set_stroke(opacity=0.5)
        qmark = N("?", 64, ACCENT).move_to(spindle.get_center() + UP * 0.12)
        qmark.set_stroke(BG, width=10, background=True)
        lab_trap = VGroup(T("trap", 30), T("· finite", 30, DIM))
        base = lambda m: m.get_bottom()[1]   # noqa: E731
        lab_trap[1].next_to(lab_trap[0], RIGHT, buff=0.14)
        lab_trap[1].shift(UP * (base(lab_trap[0][2]) - base(lab_trap[1])))          # baseline = the 'a' of trap
        lab_trap.move_to([-4.95, -1.2, 0])
        self.at("trap", Create(spindle[0]), FadeIn(spindle[1]), run_time=0.6)
        self.play(FadeIn(lab_trap, shift=UP * 0.1), FadeIn(qmark, scale=0.6), run_time=0.45)
        # "to pull the seven down"
        self.at(25.20, GrowArrow(arr_r), Indicate(win[4], color=ACCENT, scale_factor=1.3), run_time=0.6)
        # "you need a better pattern for the endless plane"
        # a field that runs out of the picture (soft rims, hard frame edge), clear of the arrow and its label
        patch = hex_patch(0.45 * 1.15, [8.7, 0.62, 0], rx=4.6, ry=2.05)
        self.at("pattern", LaggedStart(*[FadeIn(c, scale=0.6) for c in patch], lag_ratio=0.04), run_time=1.2)
        lab_pat = VGroup(T("pattern", 30), T("· endless", 30, DIM)).arrange(RIGHT, buff=0.14)
        lab_pat[1].shift(UP * (base(lab_pat[0][1]) - base(lab_pat[1])))    # baseline = the 'a' of pattern
        lab_pat.move_to([4.9, 0, 0])
        lab_pat.shift(UP * (base(lab_trap[0][2]) - base(lab_pat[0][1])))  # same baseline as 'trap? · finite'
        self.at(28.25, FadeIn(lab_pat, shift=UP * 0.1), run_time=0.5)
        # pause: both arrows strain, the window holds
        strain = lambda a: np.sin(2 * np.pi * a) ** 2   # noqa: E731
        self.at("p4_end", arr_l.animate(rate_func=strain).shift(RIGHT * 0.1),
                arr_r.animate(rate_func=strain).shift(LEFT * 0.1), run_time=0.75)

        # ---- p5: de Bruijn & Erdős, 1951 -----------------------------------------------------------
        self.at("p5", FadeOut(VGroup(spindle, lab_trap, patch, lab_pat, arr_l, arr_r)),
                Transform(win, win_home), run_time=0.75)
        self.remove(win)
        # "nineteen fifty-one": the story jumps back; an INK flag rises at 1951 (clear of the gold trail) and pulses
        p51 = ax.at(1951)
        flag = VGroup(Line(p51 + DOWN * 0.1, p51 + UP * 0.36, color=INK, stroke_width=3.5),
                      pt(p51 + UP * 0.36, INK, r=0.065)).set_z_index(3)
        self.at(30.92, GrowFromEdge(flag, DOWN), run_time=0.35)
        self.play(Flash(flag[1].get_center(), color=INK, line_length=0.12, flash_radius=0.2, num_lines=10),
                  run_time=0.45)
        # "de Bruijn and Erdős": caption centred under the timeline; the plane's endless sticks fill the frame
        cap_dbe = VGroup(T("de Bruijn & Erdős ·", 28), N("1951", 30))
        cap_dbe[1].next_to(cap_dbe[0], RIGHT, buff=0.14)
        cap_dbe[1].shift(UP * (base(cap_dbe[0][0]) - base(cap_dbe[1])))      # on the text's baseline
        cap_dbe.move_to([0, 2.42, 0])
        web = web_mobs()
        self.at("dbe", FadeIn(web), FadeIn(cap_dbe, shift=DOWN * 0.1), run_time=1.2)
        # "hunting for a trap": a search lens glides across the web; the sticks under it light up
        R_SEEK = 1.1
        start = np.array([-4.2, 0.3, 0.0])
        seeker = Circle(radius=R_SEEK, color=ACCENT, stroke_width=3.5).set_fill(ACCENT, 0.04).move_to(start)
        k_light = ValueTracker(0.0)
        light = lens_light(start, R_SEEK, 0.0)
        light.add_updater(lambda m: m.become(lens_light(seeker.get_center(), seeker.width / 2, k_light.get_value())))
        self.add(light)
        self.at("hunt", Create(seeker), k_light.animate.set_value(1.0), run_time=0.45)
        path = VMobject().set_points_smoothly([start, np.array([-2.3, -0.45, 0]), np.array([-0.4, 0.45, 0]),
                                               np.array([0.9, -0.35, 0]), CL_C])
        self.until(36.75, MoveAlongPath(seeker, path, rate_func=smooth))
        # "a fifth color"
        self.at("fifth", Indicate(bar.cells[4], color=ACCENT, scale_factor=1.35),
                FadeIn(halo5, rate_func=there_and_back), run_time=0.9)
        self.remove(halo5)
        # "some finite trap": the lens widens around one cluster of the web while exactly that cluster's own
        # sticks and dots brighten in place (the rest of the lit patch dims back to the web) ...
        # (the cluster starts exactly as the web draws those sticks and dots, so nothing pops in)
        cluster = VGroup(VGroup(*[stick(WEB_M[a], WEB_M[b], width=WEB_STICK_W) for a, b in CL_E])
                         .set_stroke(opacity=WEB_STICK_O * 0.9),
                         VGroup(*[Dot(p, radius=0.026, color=INK).set_opacity(WEB_DOT_O * 0.9) for p in CL_PTS]))
        lit = VGroup(VGroup(*[stick(WEB_M[a], WEB_M[b], width=3) for a, b in CL_E]),
                     VGroup(*[ring(p, r=0.07) for p in CL_PTS]))
        R_LENS = CL_R + 0.27
        self.at("finite", Transform(cluster, lit), k_light.animate.set_value(0.0),
                seeker.animate.scale(R_LENS / R_SEEK).move_to(CL_C), run_time=0.65)
        light.clear_updaters()
        self.remove(light)
        # "... proves it": the rest of the web fades and the found piece lifts out, a little larger
        dest = np.array([0.0, -0.4, 0.0])
        LIFT = 1.07
        R_END = R_LENS * LIFT
        anchor = dest + R_END * np.array([np.cos(0.62), np.sin(0.62), 0])
        lab_q = VGroup(T("trap", 30, ACCENT), N("?", 36, ACCENT))
        lab_q[1].next_to(lab_q[0], RIGHT, buff=0.06)
        lab_q[1].shift(UP * (base(lab_q[0][2]) - base(lab_q[1])))
        lab_q.next_to(anchor, UR, buff=0.1)
        axioms = T("with the usual axioms", 24, DIM).next_to(cap_dbe, DOWN, buff=0.16)
        self.play(FadeOut(web), VGroup(cluster, seeker).animate.scale(LIFT, about_point=CL_C).shift(dest - CL_C),
                  FadeIn(lab_q, shift=DOWN * 0.1), FadeIn(axioms), run_time=1.0)

        # ---- p6: Erdős suspected five; every candidate still 4-colourable ---------------------------
        cap_e = VGroup(T("Erdős:", 28), N("5?", 32, ACCENT)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        cap_e.next_to(panel, RIGHT, buff=0.3).align_to(bar.cells, DOWN)
        halo5.set_opacity(0.16)
        self.at("erdos", FadeIn(cap_e, shift=LEFT * 0.1), bar.cells[4].animate.set_color(GOLD_SOFT),
                FadeIn(halo5), run_time=0.8)
        # "but for decades": the hoped-for trap dissolves
        self.at("p6s2", FadeOut(VGroup(cluster, seeker, lab_q, cap_dbe, axioms), scale=0.92),
                run_time=0.7)
        # "nobody could find the trap": the shapes people tried
        u = 0.9
        shapes, painted = VGroup(), []
        for (P, E, col), x in zip(candidate_shapes(), (-4.95, -1.65, 1.65, 4.95)):
            s, pnt = build_shape(P, E, col, u, [x, 0.45, 0])
            shapes.add(s)
            painted.append(pnt)
        self.at("find", LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in shapes], lag_ratio=0.3), run_time=1.3)
        # "every shape they tried": each gets painted
        self.until("p6s3")
        self.until("tried", LaggedStart(*[
            AnimationGroup(*[Transform(d, pd) for d, pd in zip(s[1], pnt)]) for s, pnt in zip(shapes, painted)],
            lag_ratio=0.35))
        # "still worked with four colors"
        badges = VGroup()
        for x in (-4.95, -1.65, 1.65, 4.95):
            b = VGroup(check_mark(ORIGIN, size=0.13, width=5), N("4", 28), T("colors work", 24, DIM))
            b[1].next_to(b[0], RIGHT, buff=0.16)
            b[2].next_to(b[1], RIGHT, buff=0.1, aligned_edge=DOWN)
            b.move_to([x, -1.3, 0])
            badges.add(b)
        self.at("tried", LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in badges], lag_ratio=0.3), run_time=1.3)

        # ---- tail: everything fades (the marker has stopped at 2017) -------------------------------
        self.until("p6_end")
        self.until("end", *[FadeOut(m) for m in self.mobjects])

