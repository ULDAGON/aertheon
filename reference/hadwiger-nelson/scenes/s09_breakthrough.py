"""S09_Breakthrough: 2018, Aubrey de Grey scales up the spindle's force-and-forbid trick.

Beats (all timed against timeline/S09_Breakthrough.json):
  P1  timeline marker jumps to 2018; a paper icon, "Aubrey de Grey · April 2018", "biologist · math as a hobby"
  P2  the Moser spindle: force (tips match) + forbid (tip stick)
  P3  the wheel (7 dots, 12 sticks); four colors; the alternate triple may match (no sticks join it)
  P4  forcer (cluster of wheels, a match somewhere) and blocker (spindle ball, no match on its central wheel)
  P5  blocker copies snap onto every forcer wheel: forced somewhere, blocked everywhere -> no 4-coloring
  P6  a genuine unit-distance web (illustration) grows while a counter reaches 20,425, then thins to 1,581

Geometry notes (problem units, 1 = the forbidden distance):
  * Every drawn stick is exactly one unit long in its own drawing (asserted below).
  * The forcer is an ILLUSTRATION: wheels that share rim dots, grown by a seeded search. It is not de Grey's
    graph L (52 wheels); no count is shown.
  * The blocker is an ILLUSTRATION: a central wheel with 12 Moser spindles hung on its rim dots, 6-fold symmetric
    so a copy can snap onto any wheel with a small rotation.
  * The P6 web is geom-style H + R(PHI)H: B = its points (lattice radius 9.2) inside the disk of the default
    geom.unit_web() (1,581 points), randomly thinned to exactly 20,425 points while keeping every point of that
    web, so the drawn dots always equal the counter. The fog shows dots only; the trim removes B minus that web
    in random order while the survivors sharpen and the web's own 9,828 unit sticks fade in, so it ends exactly
    on geom.unit_web(), the same web the next scene shows.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

from scipy.spatial import cKDTree  # noqa: E402

# ------------------------------------------------------------------ small geometry helpers (problem units)
RIM_ANG = np.pi / 2 + np.arange(6) * np.pi / 3        # rim dot k of an unrotated wheel (k = 0 on top)


def wheel_pts(center, rot_a=0.0):
    """7 points: centre, then rim 0..5 (counter-clockwise from the top)."""
    c = np.asarray(center, float)
    return np.array([c] + [c + np.array([np.cos(a + rot_a), np.sin(a + rot_a)]) for a in RIM_ANG])


WHEEL_EDGES = [(0, k) for k in range(1, 7)] + [(k, k % 6 + 1) for k in range(1, 7)]
for _a, _b in WHEEL_EDGES:
    _w = wheel_pts((0, 0))
    assert abs(dist(_w[_a], _w[_b]) - 1) < 1e-9


def dedupe(points, tol=1e-6):
    """Unique points (first occurrence kept) + map old index -> new index."""
    out, idx = [], []
    for p in points:
        for j, q in enumerate(out):
            if dist(p, q) < tol:
                idx.append(j)
                break
        else:
            idx.append(len(out))
            out.append(np.asarray(p, float))
    return np.array(out), idx


# ------------------------------------------------------------------ the forcer (illustration)
def build_forcer(n_wheels=8, seed=3, tries=400):
    """Wheels that hang on each other's rim dots (each new wheel shares one rim dot with an old one).
    Returns centres (n,2), rotations (n,), points (m,2), wheel index lists (n,7), unique edges (e,2)."""
    rng = np.random.default_rng(seed)
    centers, rots = [np.zeros(2)], [0.0]
    pts = list(wheel_pts((0, 0), 0.0))
    wheels = [list(range(7))]
    while len(centers) < n_wheels:
        best = None
        for _ in range(tries):
            i = rng.integers(len(centers))
            a = rng.integers(6)
            p_idx = wheels[i][1 + a]
            p = pts[p_idx]
            out_ang = np.arctan2(*(p - centers[i])[::-1])
            psi = out_ang + rng.uniform(-1.0, 1.0)
            c = p + np.array([np.cos(psi), np.sin(psi)])
            back = psi + np.pi                           # direction from the new centre to p
            r = (back - np.pi / 2) % (np.pi / 3)         # rotation that puts a rim dot at p
            w = wheel_pts(c, r)
            if min(dist(c, q) for q in centers) < 1.85:
                continue
            new = [q for q in w if dist(q, p) > 1e-6]
            dmin = min(dist(q, s) for q in new for s in pts)
            if dmin < 0.5:
                continue
            allc = np.array(centers + [c])
            spread = np.linalg.norm(allc - allc.mean(axis=0), axis=1).max() + 0.25 * np.linalg.norm(allc.mean(axis=0))
            if best is None or spread < best[0]:
                best = (spread, c, r, w, p_idx)
        assert best is not None, "forcer search failed"
        _, c, r, w, p_idx = best
        idxs = []
        for q in w:
            hit = [j for j, s in enumerate(pts) if dist(q, s) < 1e-6]
            if hit:
                idxs.append(hit[0])
            else:
                idxs.append(len(pts))
                pts.append(q)
        centers.append(c)
        rots.append(r)
        wheels.append(idxs)
    pts = np.array(pts)
    edges = sorted({tuple(sorted((wl[a], wl[b]))) for wl in wheels for a, b in WHEEL_EDGES})
    for a, b in edges:
        assert abs(dist(pts[a], pts[b]) - 1) < 1e-9
    cen = np.array(centers).mean(axis=0)
    return np.array(centers) - cen, np.array(rots), pts - cen, wheels, edges


F_CENTERS, F_ROTS, F_PTS, F_WHEELS, F_EDGES = build_forcer()


# ------------------------------------------------------------------ the blocker (illustration)
def build_blocker(delta=np.radians(23)):
    """Central wheel at the origin + two Moser spindles hung on each rim dot, pointing outward at ±delta.
    Returns points (m,2) [0..6 = the central wheel], edges (e,2) [first 12 = the wheel]."""
    P0, E0 = moser_spindle()
    names = list(P0)
    raw = list(wheel_pts((0, 0)))
    raw_edges = [(a, b) for a, b in WHEEL_EDGES]
    for k in range(6):
        base = raw[1 + k]
        for s in (-1, 1):
            up = RIM_ANG[k] + s * delta
            P, _ = moser_spindle(up)
            off = len(raw)
            for nme in names:
                raw.append(base + P[nme])
            raw_edges += [(off + names.index(a), off + names.index(b)) for a, b in E0]
    pts, m = dedupe(raw)
    edges = []
    for a, b in raw_edges:
        e = tuple(sorted((m[a], m[b])))
        if e not in edges:
            edges.append(e)
    for a, b in edges:
        assert abs(dist(pts[a], pts[b]) - 1) < 1e-9
    assert edges[:12] == [tuple(sorted(e)) for e in WHEEL_EDGES]
    return pts, edges


B_PTS, B_EDGES = build_blocker()
B_RADIUS = float(np.linalg.norm(B_PTS, axis=1).max())
assert cKDTree(B_PTS).query(B_PTS, k=2)[0][:, 1].min() > 0.2      # no doubled / smudged dots


# ------------------------------------------------------------------ the P6 web (illustration)
N_BIG, N_SMALL = 20425, 1581


def build_web(ball_r=9.2, seed=2018):
    """Dense point set B (H + R H, lattice radius ball_r, inside the default web's disk), randomly thinned to
    exactly N_BIG points but keeping every point of geom.unit_web(). Sorted centre-out.
    Returns B (n,2), keep mask (the 1,581 web), rho, and the web's own points + unit edges."""
    Pf, Ef = unit_web()                                  # the 1,581-point web of the next scene
    rho = np.linalg.norm(Pf, axis=1).max()
    H = lattice_ball(ball_r)
    RH = np.array([rot(p, PHI) for p in H])
    Z = (H[:, None, :] + RH[None, :, :]).reshape(-1, 2)
    Z = np.unique(np.round(Z, 9), axis=0)
    Z = Z[np.linalg.norm(Z, axis=1) <= rho + 1e-9]
    dd, idx = cKDTree(Z).query(Pf)
    assert dd.max() < 1e-6
    keep = np.zeros(len(Z), bool)
    keep[idx] = True
    extra = np.random.default_rng(seed).choice(np.flatnonzero(~keep), len(Z) - N_BIG, replace=False)
    sel = np.ones(len(Z), bool)
    sel[extra] = False
    Z, keep = Z[sel], keep[sel]
    order = np.argsort(np.linalg.norm(Z, axis=1), kind="stable")
    Z, keep = Z[order], keep[order]
    assert len(Z) == N_BIG and keep.sum() == len(Pf) == N_SMALL
    assert np.all(np.abs(np.linalg.norm(Pf[Ef[:, 0]] - Pf[Ef[:, 1]], axis=1) - 1) < 1e-6)
    return Z, keep, rho, Pf, Ef




# ------------------------------------------------------------------ batched drawing (one VMobject per layer)
_T4 = np.array([0, 1 / 3, 2 / 3, 1])[None, :, None]
_K = 0.5523
_ARC = np.array([[1, 0], [1, _K], [_K, 1], [0, 1]], float)
_CIRC = np.concatenate([_ARC @ np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
                        for a in (0, np.pi / 2, np.pi, 3 * np.pi / 2)])
CIRC16 = np.c_[_CIRC, np.zeros(16)]          # unit circle as 4 cubic arcs


def seg_points(a, b):
    return (a[:, None, :] + _T4 * (b - a)[:, None, :]).reshape(-1, 3)


def set_segs(m, a, b):
    if len(a):
        m.set_points(seg_points(a, b))
    else:
        m.clear_points()


def seg_mob(a, b, color=UNIT_COLOR, width=2.0, opacity=1.0):
    m = VMobject()
    set_segs(m, a, b)
    m.set_fill(opacity=0)
    m.set_stroke(color, width=width, opacity=opacity)
    return m


def set_dots(m, c, r):
    if len(c):
        m.set_points((c[:, None, :] + r * CIRC16[None]).reshape(-1, 3))
    else:
        m.clear_points()


def dot_mob(c, r, color=INK, opacity=1.0):
    m = VMobject()
    set_dots(m, c, r)
    m.set_stroke(width=0)
    m.set_fill(color, opacity=opacity)
    return m


def P3(pts2, scale, center):
    """(n,2) problem points -> (n,3) manim points."""
    pts2 = np.asarray(pts2, float)
    return np.asarray(center, float) + scale * np.c_[pts2, np.zeros(len(pts2))]


def fmt(v):
    return f"{int(round(v)):,}"


def clip01(x):
    return float(np.clip(x, 0.0, 1.0))


def shake(grp, amp=0.07, n=2, frac=1.0):
    """The scene's one 'contradiction' shake: a damped left-right shake in the first `frac` of the
    animation; ends exactly where it started."""
    st = {"off": 0.0}

    def upd(m, a):
        u = clip01(a / frac)
        off = amp * np.sin(2 * np.pi * n * u) * (1 - u)
        m.shift(RIGHT * (off - st["off"]))
        st["off"] = off

    return UpdateFromAlphaFunc(grp, upd, rate_func=linear)


# ------------------------------------------------------------------ layout (manim units)
TL_Y, TL_X0, TL_X1 = 3.0, -5.6, 5.6          # P1 timeline at the top edge


def year_x(y):
    return TL_X0 + (TL_X1 - TL_X0) * (y - 1950) / 70


US, SP_A = 1.3, np.array([0.0, -1.95, 0.0])     # P2 spindle (scaled x1.3 about A on "scaled way up")
SP_GROW = 1.3
UW, WC = 1.8, np.array([0.0, 0.1, 0.0])         # P3 wheel (UNIT = 1.8)
RF, FC = 0.4, np.array([-3.2, 0.15, 0.0])       # P4 forcer
RB, BC = 0.56, np.array([3.35, 0.15, 0.0])      # P4 blocker
COMB_C = np.array([0.0, 0.25, 0.0])             # P5 combined shape
WEB_R, WEB_C = 2.55, np.array([0.0, 0.25, 0.0])  # P6 web disk
PAINT = [PURPLE_P, BLUE_P, YELLOW_P, BLUE_P, PINK_P, BLUE_P, YELLOW_P]   # wheel: centre, rim 0..5
TRIPLE = [1, 3, 5]                               # alternate rim dots (rim 0, 2, 4)


class S09_Breakthrough(TimedScene):
    def wt(self, sid, word, k=0):
        """Start time of the k-th occurrence of `word` in sentence `sid`."""
        s = next(x for x in self.tl["sentences"] if x["id"] == sid)
        hits = [w["s"] for w in s["words"] if w["w"].strip(".,:;").lower() == word.lower()]
        return hits[k]

    def construct(self):
        # ============================================================ scoreboard (whole scene)
        bar = BoundsBar(4, 7).scale(0.8).to_edge(DOWN, buff=0.3)
        panel = Rectangle(width=bar.width + 0.5, height=bar.height + 0.3, stroke_width=0) \
            .set_fill(BG, 1).move_to(bar)
        bar_grp = VGroup(panel, bar).set_z_index(10)

        # ============================================================ P1: April 2018, Aubrey de Grey
        axis = Line([TL_X0, TL_Y, 0], [TL_X1, TL_Y, 0], color=FAINT, stroke_width=3)
        ticks = VGroup(*[Line([year_x(y), TL_Y - 0.08, 0], [year_x(y), TL_Y + 0.08, 0],
                              color=DIM if y in (1950, 2020) else FAINT, stroke_width=2)
                         for y in range(1950, 2021, 10)])
        lab0 = N("1950", 24, DIM).next_to([year_x(1950), TL_Y, 0], DOWN, buff=0.16)
        lab1 = N("2020", 24, DIM).next_to([year_x(2020), TL_Y, 0], DOWN, buff=0.16)
        trail = Line([TL_X0, TL_Y, 0], [year_x(2017), TL_Y, 0], color=ACCENT, stroke_width=3, stroke_opacity=0.45)
        marker = Dot([year_x(2017), TL_Y, 0], radius=0.085, color=ACCENT)
        timeline = VGroup(axis, ticks, lab0, lab1, trail, marker)
        y2018 = np.array([year_x(2018), TL_Y, 0])
        lab2018 = N("2018", 28, ACCENT).next_to(y2018, UP, buff=0.14)

        # paper icon (a posted paper; no likeness of anyone)
        pc = np.array([0.0, 0.95, 0.0])
        PW, PH, FO = 1.5, 1.95, 0.32
        sheet = Polygon(pc + [-PW / 2, -PH / 2, 0], pc + [PW / 2, -PH / 2, 0], pc + [PW / 2, PH / 2 - FO, 0],
                        pc + [PW / 2 - FO, PH / 2, 0], pc + [-PW / 2, PH / 2, 0],
                        color=INK, stroke_width=3).set_fill("#1B212B", 1)
        fold = Polygon(pc + [PW / 2 - FO, PH / 2, 0], pc + [PW / 2 - FO, PH / 2 - FO, 0], pc + [PW / 2, PH / 2 - FO, 0],
                       color=INK, stroke_width=2).set_fill("#2A3140", 1)

        def pline(x0, x1, y, color=DIM, w=3):
            return Line(pc + [x0, y, 0], pc + [x1, y, 0], color=color, stroke_width=w)

        doodle_P, doodle_E = moser_spindle()
        dpos = {k: to_scene(v, 0.3, pc + [-0.33, -0.72, 0]) for k, v in doodle_P.items()}
        doodle = VGroup(*[Line(dpos[a], dpos[b], color=DIM, stroke_width=1.5) for a, b in doodle_E],
                        *[Dot(p, radius=0.025, color=DIM) for p in dpos.values()])
        plines = VGroup(pline(-0.55, 0.25, 0.64, INK, 5), pline(-0.55, 0.55, 0.40), pline(-0.55, 0.55, 0.24),
                        pline(-0.55, 0.2, 0.08), doodle,
                        pline(0.05, 0.55, -0.25), pline(0.05, 0.55, -0.41), pline(0.05, 0.4, -0.57),
                        pline(-0.55, 0.45, -0.82))
        paper = VGroup(sheet, fold)
        name = T("Aubrey de Grey · April 2018", 30).move_to([0, -0.5, 0])
        tag_full = VGroup(T("biologist", 26, DIM), T("·", 26, DIM), T("math as a hobby", 26, ACCENT)) \
            .arrange(RIGHT, buff=0.18).move_to([0, -1.1, 0])
        tag_bio = T("biologist", 26, DIM).move_to([0, -1.1, 0])

        self.until(0.45, FadeIn(bar_grp), FadeIn(timeline))
        self.at(0.5, marker.animate.move_to(y2018),
                Transform(trail, Line([TL_X0, TL_Y, 0], y2018, color=ACCENT, stroke_width=3, stroke_opacity=0.45)),
                run_time=0.65)
        self.play(Flash(marker, color=ACCENT, line_length=0.16, flash_radius=0.22),
                  FadeIn(lab2018, shift=DOWN * 0.1), run_time=0.6)
        self.at("degrey", FadeIn(paper, shift=UP * 0.2), FadeIn(name, shift=UP * 0.1), run_time=0.7)
        self.play(LaggedStart(*[Create(m) for m in plines], lag_ratio=0.22), run_time=1.15)
        self.at("bio", FadeIn(tag_bio, shift=UP * 0.1), run_time=0.6)
        self.at("hobby", tag_bio.animate.move_to(tag_full[0]), FadeIn(tag_full[1:], shift=LEFT * 0.2), run_time=0.7)
        self.remove(tag_bio)
        self.add(tag_full)
        self.at("p1_end", FadeOut(VGroup(timeline, lab2018, paper, plines, name, tag_full)), run_time=0.6)

        # ============================================================ P2: the spindle's trick
        SPP, SPE = moser_spindle()
        names = list(SPP)
        spos = {k: to_scene(v, US, SP_A) for k, v in SPP.items()}
        s_sticks = VGroup(*[stick(spos[a], spos[b]) for a, b in SPE])        # index 10 = D-D2
        s_dots = VGroup(*[ring(spos[k], r=0.1) for k in names])
        spindle = VGroup(s_sticks, s_dots)
        badge_txt = VGroup(T("force", 26, ACCENT), T("+", 26, DIM), T("forbid", 26, BAD)).arrange(RIGHT, buff=0.14)
        badge = VGroup(RoundedRectangle(corner_radius=0.14, width=badge_txt.width + 0.45, height=badge_txt.height + 0.32,
                                        color=DIM, stroke_width=2), badge_txt)
        badge_txt.move_to(badge[0])
        badge.to_corner(UL, buff=0.45)

        self.at("p2", Create(s_sticks, lag_ratio=0.08), FadeIn(s_dots, lag_ratio=0.08), run_time=0.85)
        self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.55)
        self.at(self.wt("p2s1", "scaled"), spindle.animate.scale(SP_GROW, about_point=SP_A), run_time=0.8)

        g = {k: s_dots[names.index(k)].get_center() for k in names}           # positions after the zoom
        glow = VGroup(*[Line(g[a], g[b], color=ACCENT, stroke_width=12, stroke_opacity=0)
                        for a, b in SPE[:10]])
        arcL = ArcBetweenPoints(g["A"], g["D"], angle=-1.0)      # bulges outward, stays inside the diamond
        arcR = ArcBetweenPoints(g["A"], g["D2"], angle=1.0)
        arcs = VGroup(*[DashedVMobject(a.set_stroke(ACCENT, 3.5), num_dashes=13, dashed_ratio=0.6) for a in (arcL, arcR)])
        eqL = N("=", 36, ACCENT).move_to(arcL.point_from_proportion(0.62))
        eqR = N("=", 36, ACCENT).move_to(arcR.point_from_proportion(0.62))
        for e in (eqL, eqR):
            e.set_stroke(BG, width=7, background=True)
        # opaque plates so the dashed arc never shows through the '=' (else it reads like '≠' / '÷')
        plL, plR = [RoundedRectangle(corner_radius=0.05, width=e.width + 0.14, height=e.height + 0.14,
                                     stroke_width=0).set_fill(BG, 1).move_to(e) for e in (eqL, eqR)]
        tips = VGroup(*[pt(g[k], PINK_P, r=0.13) for k in ("A", "D", "D2")])
        lab_force = T("force", 32, ACCENT).move_to([-2.75, eqL.get_center()[1], 0])
        tip_stick = s_sticks[10]
        tip_glow = Line(g["D"], g["D2"], color=BAD, stroke_width=16, stroke_opacity=0.35)
        lab_forbid = T("forbid", 32, BAD).next_to(g["D2"], RIGHT, buff=0.75)

        self.at("force", Create(arcs), FadeIn(VGroup(plL, eqL, plR, eqR)), FadeIn(tips, scale=0.5),
                glow.animate(rate_func=there_and_back).set_stroke(opacity=0.45),
                FadeIn(lab_force, shift=RIGHT * 0.2), run_time=0.85)
        self.remove(glow)
        self.at("forbid", tip_stick.animate.set_stroke(BAD, width=7), FadeIn(tip_glow),
                FadeIn(lab_forbid, shift=LEFT * 0.2), run_time=0.6)
        self.bring_to_front(s_dots, tips, plL, eqL, plR, eqR)

        # ============================================================ P3: the wheel
        wp = P3(wheel_pts((0, 0)), UW, WC)
        w_ring = Circle(radius=UW, color=UNIT_COLOR, stroke_width=2.5).move_to(WC)
        w_sticks = VGroup(*[stick(wp[a], wp[b]) for a, b in WHEEL_EDGES])
        w_dots = VGroup(*[ring(p, r=0.11) for p in wp])
        paint = VGroup(*[pt(wp[i], PAINT[i], r=0.13) for i in range(7)])
        x0 = 2.75
        lab_wheel = VGroup(T("wheel", 34), T("7 dots · 12 sticks", 26, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lab_wheel.move_to([x0, 1.45, 0], aligned_edge=LEFT)
        sw_cols = [BLUE_P, YELLOW_P, PINK_P, PURPLE_P]
        swatches = VGroup(*[pt([-4.6, 0.75 - 0.52 * i, 0], c, r=0.17) for i, c in enumerate(sw_cols)])
        sw_lab = T("4 colors", 28, DIM).next_to(swatches, UP, buff=0.35)
        outlines = VGroup(*[Circle(radius=0.25, color=ACCENT, stroke_width=3.5).move_to(wp[i]) for i in TRIPLE])
        ok = VGroup(check_mark([x0 + 0.18, -0.2, 0], size=0.18), T("allowed", 28))
        ok[1].next_to(ok[0], RIGHT, buff=0.25)
        tri = DashedVMobject(Polygon(*[wp[i] for i in TRIPLE], color=DIM, stroke_width=3), num_dashes=45,
                             dashed_ratio=0.5)
        legend = VGroup(DashedLine([x0, -0.85, 0], [x0 + 0.42, -0.85, 0], color=DIM, stroke_width=3, dash_length=0.08),
                        VGroup(T("not sticks", 26, DIM), T("(1.73 apart)", 24, DIM))
                        .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        legend[1].next_to(legend[0], RIGHT, buff=0.22).align_to(legend[0], UP).shift(UP * 0.14)

        self.at("p3", FadeOut(VGroup(spindle, tips, arcs, plL, eqL, plR, eqR, tip_glow, lab_force, lab_forbid, badge)),
                run_time=0.7)
        self.at("wheel", GrowFromCenter(w_dots[0]), Create(w_ring), run_time=0.9)
        self.at("six", LaggedStart(*[GrowFromCenter(d) for d in w_dots[1:]], lag_ratio=0.18), run_time=0.7)
        self.bring_to_front(w_dots)
        self.play(Create(w_sticks, lag_ratio=0.08), run_time=1.0)      # the ring stays bright: "around its ring"
        self.bring_to_front(w_dots)
        self.play(FadeIn(lab_wheel, shift=LEFT * 0.15), run_time=0.6)
        self.at("four", FadeIn(sw_lab), LaggedStart(*[GrowFromCenter(s) for s in swatches], lag_ratio=0.2),
                w_ring.animate.set_stroke(opacity=0.25), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(paint[i], scale=0.4) for i in (0, 2, 4, 6)], lag_ratio=0.2), run_time=0.7)
        self.at("triple", LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.45), run_time=1.2)
        self.at(26.0, LaggedStart(*[FadeIn(paint[i], scale=0.4) for i in TRIPLE], lag_ratio=0.12), run_time=0.65)
        self.at(self.wt("p3s3", "that's"), Create(ok[0]), FadeIn(ok[1], shift=LEFT * 0.1), run_time=0.55)
        self.at("allowed", Create(tri), FadeIn(legend, shift=LEFT * 0.1), run_time=0.8)
        self.at(self.t("p3_end") + 0.05,
                *[paint[i].animate(rate_func=there_and_back).scale(1.35) for i in TRIPLE], run_time=0.75)

        # ============================================================ P4: forcer and blocker
        fpos = P3(F_PTS, RF, FC)
        f_sticks = VGroup(*[stick(fpos[a], fpos[b], width=2.8) for a, b in F_EDGES])
        f_dots = VGroup(*[ring(p, r=0.055, color=INK) for p in fpos])
        for d in f_dots:
            d.set_stroke(width=2)
        f_cent = P3(F_CENTERS, RF, FC)
        w_edges = [[F_EDGES.index(tuple(sorted((wl[a], wl[b])))) for a, b in WHEEL_EDGES] for wl in F_WHEELS]
        w_main = int(np.argmin(np.linalg.norm(F_CENTERS, axis=1)))
        order = sorted((j for j in range(len(F_WHEELS)) if j != w_main),
                       key=lambda j: np.linalg.norm(F_CENTERS[j] - F_CENTERS[w_main]))
        w_lit = int(np.argmax(F_CENTERS[:, 0] + 0.6 * F_CENTERS[:, 1]))
        seen = set(F_WHEELS[w_main])
        grow_groups = []
        for j in order:
            new_dots = [f_dots[i] for i in F_WHEELS[j] if i not in seen]
            seen.update(F_WHEELS[j])
            grow_groups.append(VGroup(*[f_sticks[e] for e in w_edges[j]], *new_dots))
        lab_forcer = T("forcer", 34, ACCENT).move_to([FC[0], 2.1, 0])
        sub_forcer = T("a match somewhere", 26, DIM).move_to([FC[0], -1.85, 0])
        tag_ill = T("illustration", 24, DIM).to_corner(DR, buff=0.35).shift(LEFT * 0.2 + UP * 0.1)

        def lit_marks(center_shift=ORIGIN, r=0.075):
            return VGroup(*[pt(fpos[F_WHEELS[w_lit][i]] + center_shift, BLUE_P, r=r) for i in TRIPLE])

        lit = lit_marks()
        lit_ring = Circle(radius=RF * 1.35, color=ACCENT, stroke_width=2.5).move_to(f_cent[w_lit])

        bpos = P3(B_PTS, RB, BC)
        ea = np.array([bpos[a] for a, b in B_EDGES[12:]])
        eb = np.array([bpos[b] for a, b in B_EDGES[12:]])
        b_wsticks = VGroup(*[stick(bpos[a], bpos[b], width=3) for a, b in B_EDGES[:12]])
        b_wdots = VGroup(*[ring(bpos[i], r=0.07) for i in range(7)])
        b_ssticks = seg_mob(ea, eb, UNIT_COLOR, width=1.6, opacity=0.8)
        b_sdots = dot_mob(bpos[7:], 0.035, INK)
        blocker = VGroup(b_ssticks, b_sdots, b_wsticks, b_wdots)
        lab_blocker = T("blocker", 34, BAD).move_to([BC[0], 2.1, 0])
        sub_blocker = T("no match here", 26, DIM).move_to([BC[0], -1.85, 0])
        one = B_EDGES[12:23]                                   # the first hung spindle (11 sticks)
        one_hl = seg_mob(np.array([bpos[a] for a, b in one]), np.array([bpos[b] for a, b in one]),
                         ACCENT, width=4.5, opacity=0)
        b_trip = VGroup(*[pt(bpos[i], BLUE_P, r=0.085) for i in TRIPLE])
        # the same dashed "allowed" triangle as in P3, here struck out: the cross sits on its centroid
        b_tri = DashedVMobject(Polygon(*[bpos[i] for i in TRIPLE], color=DIM, stroke_width=3), num_dashes=15,
                               dashed_ratio=0.55)
        b_cross = cross_mark(BC, size=0.2, color=BAD, width=6)

        # the big wheel shrinks into the forcer's middle wheel
        shrink = [ReplacementTransform(w_sticks[i], f_sticks[w_edges[w_main][i]]) for i in range(12)]
        shrink += [ReplacementTransform(w_dots[i], f_dots[F_WHEELS[w_main][i]]) for i in range(7)]
        shrink += [paint[i].animate.move_to(fpos[F_WHEELS[w_main][i]]).scale(0.3).set_opacity(0) for i in range(7)]
        self.until("forces", *shrink,
                   FadeOut(VGroup(w_ring, lab_wheel, swatches, sw_lab, outlines, ok, tri, legend)))
        self.remove(paint)
        self.play(LaggedStart(*[FadeIn(gr, scale=0.7) for gr in grow_groups], lag_ratio=0.12),
                  FadeIn(lab_forcer, shift=DOWN * 0.1), FadeIn(tag_ill), run_time=0.8)
        scan_order = sorted(range(len(F_WHEELS)), key=lambda j: F_CENTERS[j, 0] - 0.3 * F_CENTERS[j, 1])
        scan_order.remove(w_lit)
        scan_order.append(w_lit)
        self.at(self.wt("p4s1", "guarantees"),
                LaggedStart(*[Indicate(VGroup(*[f_sticks[e] for e in w_edges[j]]), color=ACCENT, scale_factor=1.08)
                              for j in scan_order], lag_ratio=0.18), run_time=1.0)
        self.at(self.wt("p4s1", "like"), FadeIn(lit, scale=0.4), Create(lit_ring), run_time=0.5)
        self.at(self.wt("p4s1", "some"), FadeIn(sub_forcer, shift=UP * 0.1), run_time=0.5)
        self.at("blocker", Create(b_wsticks), FadeIn(b_wdots), FadeIn(lab_blocker, shift=DOWN * 0.1), run_time=0.7)
        self.at(self.wt("p4s2", "packed"), LaggedStart(Create(b_ssticks), FadeIn(b_sdots), lag_ratio=0.45),
                run_time=1.0)
        self.bring_to_front(b_wsticks, b_wdots)
        self.add(one_hl)
        self.play(one_hl.animate(rate_func=there_and_back).set_stroke(opacity=0.95), run_time=self.left("forbids") - 0.05)
        self.remove(one_hl)
        b_trip.set_z_index(1)
        self.at("forbids", FadeIn(b_trip, scale=0.4), Create(b_tri), run_time=0.45)
        self.play(Create(b_cross), b_tri.animate.set_stroke(BAD), run_time=0.45)
        self.at(self.wt("p4s2", "on"), FadeIn(sub_blocker, shift=UP * 0.1),
                b_wsticks.animate.set_color(ACCENT), run_time=0.6)


        # ============================================================ P5: attach a blocker to every wheel
        # (the blocker's central wheel stays ACCENT from P4: every copy carries that gold wheel onto a forcer wheel)
        self.at("p5", FadeOut(VGroup(sub_forcer, sub_blocker, lit, lit_ring, b_trip, b_tri, b_cross)),
                f_sticks.animate.set_stroke(width=3.5), run_time=0.45)
        nW = len(F_WHEELS)
        BP3 = np.c_[B_PTS, np.zeros(len(B_PTS))]
        EA_W = np.array([a for a, b in B_EDGES[:12]])
        EB_W = np.array([b for a, b in B_EDGES[:12]])
        EA_S = np.array([a for a, b in B_EDGES[12:]])
        EB_S = np.array([b for a, b in B_EDGES[12:]])
        deltas = [((r + np.pi / 6) % (np.pi / 3)) - np.pi / 6 for r in F_ROTS]    # blocker is 6-fold symmetric

        def placed(center, scale, ang):
            c, s = np.cos(ang), np.sin(ang)
            R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])
            return center + scale * BP3 @ R.T

        P0 = placed(BC, RB, 0.0)
        # each copy = spindle sticks, dots, central-wheel sticks (ACCENT); all hidden until it launches,
        # so the source blocker never thickens and no filled dot covers its hollow rings
        copies = VGroup(*[VGroup(seg_mob(P0[EA_S], P0[EB_S], UNIT_COLOR, width=1.6, opacity=0),
                                 dot_mob(P0, 0.035, INK, opacity=0),
                                 seg_mob(P0[EA_W], P0[EB_W], ACCENT, width=2.6, opacity=0))
                          for _ in range(nW)])
        ripples = VGroup(*[VMobject().set_fill(opacity=0).set_stroke(ACCENT, width=4, opacity=0) for _ in range(nW)])
        fly_order = sorted(range(nW), key=lambda j: np.linalg.norm(f_cent[j] - BC))
        wheel_e = [[f_sticks[e] for e in w_edges[j]] for j in range(nW)]

        # schedule (s from the fly start): copy #1 is a slow, clear demo on "a blocker"; the other seven follow
        # on "to every wheel", quick and see-through, so they never smear into one white mass
        T0 = self.wt("p5s1", "a")
        DEMO_D, REST_D, STAG = 0.85, 0.55, 0.15
        rest0 = self.t("attach") + 0.12 - T0
        sched = [(0.0, DEMO_D)] + [(rest0 + STAG * (k - 1), REST_D) for k in range(1, nW)]
        OP = [(0.8, 1.0, 1.0)] + [(0.35, 0.5, 0.75)] * (nW - 1)       # in flight: spindles, dots, gold wheel
        LAND_OP = (0.32, 0.5, 0.0)                                     # landed (gold wheel hides under the forcer)
        FLY_T = sched[-1][0] + REST_D + 0.35

        def flash_k(dt, hold, dec=0.4):
            if dt < -0.1:
                return 0.0
            if dt < 0:
                return (dt + 0.1) / 0.1
            if dt < hold:
                return 1.0
            return clip01(1 - (dt - hold) / dec)

        def fly(_m, alpha):
            t = alpha * FLY_T
            for rank, j in enumerate(fly_order):
                st, du = sched[rank]
                if t < st:
                    continue                                   # not launched yet: stays invisible
                sp, dts, wh = copies[j]
                s = smooth(clip01((t - st) / du))
                P = placed(BC + s * (f_cent[j] - BC), RB + s * (RF - RB), s * deltas[j])
                set_segs(sp, P[EA_S], P[EB_S])
                set_segs(wh, P[EA_W], P[EB_W])
                set_dots(dts, P, 0.035 - 0.01 * s)
                dt = t - st - du                               # time since landing
                u = clip01(dt / 0.3)
                o = [OP[rank][i] * (1 - u) + LAND_OP[i] * u for i in range(3)]
                sp.set_stroke(width=1.6 - 0.5 * s, opacity=o[0])
                dts.set_fill(opacity=o[1])
                wh.set_stroke(width=2.6 - 0.6 * s, opacity=o[2])
                col = interpolate_color(ManimColor(UNIT_COLOR), ManimColor(ACCENT), flash_k(dt, 0.3 if rank == 0 else 0.05))
                for m in wheel_e[j]:
                    m.set_stroke(col)
                rd = 0.6 if rank == 0 else 0.45
                if 0 <= dt <= rd:
                    q = dt / rd
                    ripples[j].set_points(f_cent[j] + RF * (1 + 0.9 * q) * CIRC16)
                    ripples[j].set_stroke(opacity=0.9 * (1 - q))
                else:
                    ripples[j].set_stroke(opacity=0)

        copies.set_z_index(1)
        forcer = VGroup(f_sticks, f_dots).set_z_index(3)               # the forcer stays readable on top
        ripples.set_z_index(4)
        self.add(copies, ripples)
        t_dim = self.t("attach") - T0

        def dim_rate(t):
            return smooth(clip01((t * FLY_T - t_dim) / 0.5))

        self.at(T0, UpdateFromAlphaFunc(VGroup(copies, ripples, f_sticks), fly, rate_func=linear),
                lab_forcer.animate(rate_func=lambda t: smooth(min(1.0, 2 * t))).shift(UP * 0.6),
                b_ssticks.animate(rate_func=dim_rate).set_stroke(opacity=0.8 * 0.4),
                b_sdots.animate(rate_func=dim_rate).set_fill(opacity=0.4),
                b_wsticks.animate(rate_func=dim_rate).set_stroke(opacity=0.45),
                b_wdots.animate(rate_func=dim_rate).set_stroke(opacity=0.4),
                run_time=FLY_T)
        self.remove(ripples)
        combined = VGroup(copies, forcer)
        land = np.concatenate([placed(f_cent[j], RF, deltas[j]) for j in range(nW)])
        lo, hi = land.min(axis=0), land.max(axis=0)
        bb_c = (lo + hi) / 2
        sc = min(1.3, 5.0 / (hi - lo)[1], 8.5 / (hi - lo)[0])

        def to_comb(p):
            return COMB_C + sc * (np.asarray(p) - bb_c)

        combined.generate_target()
        combined.target.scale(sc, about_point=bb_c).shift(COMB_C - bb_c)
        for cp in combined.target[0]:
            cp[0].set_stroke(opacity=0.32)
            cp[1].set_fill(opacity=0.5)
            cp[2].set_stroke(opacity=0)
        combined.target[1][0].set_stroke(UNIT_COLOR, width=3.2)
        self.play(FadeOut(VGroup(blocker, lab_blocker, lab_forcer)), MoveToTarget(combined), run_time=0.85)
        lit2 = VGroup(*[pt(to_comb(fpos[F_WHEELS[w_lit][i]]), BLUE_P, r=0.075) for i in TRIPLE]).set_z_index(4)
        lit_ring2 = Circle(radius=RF * 1.35 * sc, color=ACCENT, stroke_width=3).move_to(to_comb(f_cent[w_lit])) \
            .set_z_index(4)
        crosses = VGroup(*[cross_mark(to_comb(f_cent[j]), size=0.13 * sc, color=BAD, width=5)
                           for j in range(nW)]).set_z_index(5)
        cross_order = sorted(range(nW), key=lambda j: np.linalg.norm(f_cent[j] - f_cent[w_lit]))   # lit wheel first
        lab_no = T("no 4-coloring", 36, BAD).move_to([0, 3.15, 0])

        self.at(self.wt("p5s2", "forced"), FadeIn(lit2, scale=0.4), Create(lit_ring2), run_time=0.5)
        # the first cross lands on the lit wheel itself: forced and blocked at once -> the one contradiction shake
        self.at("blocked", GrowFromCenter(crosses[w_lit]), lit2.animate.set_color(BAD), run_time=0.35)
        lit_grp = VGroup(*wheel_e[w_lit], *[f_dots[i] for i in F_WHEELS[w_lit]], lit2, lit_ring2, crosses[w_lit])
        self.play(shake(lit_grp, amp=0.07, n=2, frac=0.55),
                  LaggedStart(*[GrowFromCenter(crosses[j]) for j in cross_order[1:]], lag_ratio=0.25), run_time=0.95)
        self.at("nowhere", f_sticks.animate(rate_func=there_and_back).set_color(BAD),
                *[cp[0].animate(rate_func=there_and_back).set_stroke(BAD, opacity=0.9) for cp in copies],
                FadeIn(lab_no, scale=1.1), run_time=0.8)

        # ============================================================ P6: 20,425 dots, trimmed to 1,581
        WZ, WKEEP, WRHO, WPF, WEF = build_web()
        WS = WEB_R / WRHO
        WP = P3(WZ, WS, WEB_C)
        nB = len(WZ)
        R0, R1, O0, O1, EDGE_OP = 0.011, 0.02, 0.75, 1.0, 0.18     # fog -> crisp net
        web_d = dot_mob(WP[:0], R0, INK, opacity=O0)
        grow = ValueTracker(0.0)
        cnt = ValueTracker(0.0)          # the counter always shows the number of dots drawn
        cop = ValueTracker(0.0)          # counter opacity (FadeIn would suspend its updater)

        def grow_upd(_m):
            k = int(round(grow.get_value() * nB))
            set_dots(web_d, WP[:k], R0)
            cnt.set_value(k)

        def make_counter():
            num = N(fmt(cnt.get_value()), 44, INK)
            num.shift(RIGHT * (0.3 - num.get_right()[0]) + UP * (3.45 - num.get_top()[1]))
            lab = T("dots", 28, DIM)
            lab.shift(RIGHT * (0.5 - lab.get_left()[0]) + UP * (3.45 - 0.05 - lab.get_top()[1]))
            return VGroup(num, lab).set_opacity(cop.get_value())

        counter = make_counter()
        counter.add_updater(lambda m: m.become(make_counter()))
        tag2 = VGroup(T("illustration,", 24, DIM), T("not the actual graph", 24, DIM)) \
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.08).to_corner(DR, buff=0.35).shift(LEFT * 0.2 + UP * 0.1)
        web_d.add_updater(grow_upd)

        def fast(k):
            return lambda t: smooth(min(1.0, k * t))

        def late(a, b):
            return lambda t: smooth(clip01((t - a) / (b - a)))

        self.at("p6", FadeOut(VGroup(lab_no, crosses, lit2, lit_ring2)),
                *[cp[0].animate.set_stroke(opacity=0.25) for cp in copies],
                *[cp[1].animate.set_fill(opacity=0.3) for cp in copies],
                f_sticks.animate.set_stroke(opacity=0.5), f_dots.animate.set_opacity(0.5), run_time=0.7)
        self.until("big")
        self.add(web_d, counter)
        # the tag slides up one line, then grows a comma + second line (no glyph morph, no overlap)
        self.at("big", grow.animate.set_value(1.0), cop.animate(rate_func=fast(4)).set_value(1),
                FadeOut(combined, rate_func=fast(1.9)),
                tag_ill.animate(rate_func=fast(4)).move_to(tag2[0][:-1]),
                FadeIn(tag2[0][-1], rate_func=late(0.22, 0.55)), FadeIn(tag2[1], rate_func=late(0.26, 0.6)),
                run_time=1.55)
        web_d.clear_updaters()
        self.remove(tag_ill)
        self.add(tag2)

        # trim: the doomed dots vanish in random order; the 1,581 survivors sharpen out of the fog and the
        # web's own unit sticks fade in, so the end state is exactly geom.unit_web()
        drop = np.random.default_rng(2018).permutation(np.flatnonzero(~WKEEP))
        nDrop = len(drop)
        PD, PK = WP[drop], WP[WKEEP]
        web_k = dot_mob(PK, R0, INK, opacity=O0)
        web_e = seg_mob(P3(WPF[WEF[:, 0]], WS, WEB_C), P3(WPF[WEF[:, 1]], WS, WEB_C), UNIT_COLOR, width=0.8, opacity=0)
        set_dots(web_d, PD, R0)                          # same picture: web_d now holds only the doomed dots
        self.remove(web_d)
        self.add(web_e, web_d, web_k, counter)           # counter last so it reads this frame's count
        trim = ValueTracker(0.0)

        def trim_upd(_m):
            p = trim.get_value()
            m = int(round(p * nDrop))
            set_dots(web_d, PD[m:], R0)
            set_dots(web_k, PK, R0 + (R1 - R0) * p)
            web_k.set_fill(opacity=O0 + (O1 - O0) * p)
            web_e.set_stroke(opacity=EDGE_OP * smooth(clip01((p - 0.55) / 0.45)))
            cnt.set_value(nB - m)

        # the updater sits on web_e, the FIRST of the three layers: manim redraws every frame only the mobjects
        # from the first updated one onward, so web_e, web_d and web_k all stay live (else the doomed dots and
        # the sticks freeze into the background and pop when the trim ends)
        web_e.add_updater(trim_upd)
        self.at("trim", trim.animate.set_value(1.0), run_time=1.2)
        web_e.clear_updaters()
        counter.clear_updaters()
        assert int(round(cnt.get_value())) == N_SMALL
        self.remove(web_d)
        self.at(self.t("p6_end") + 0.15, FadeOut(VGroup(web_e, web_k, counter, tag2, bar_grp)), run_time=0.75)

