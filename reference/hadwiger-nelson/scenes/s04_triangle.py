"""S04 - Two rings cross: at least three colours.

Checkerboard and a cleverer wavy pattern both fail; the reason is the equilateral unit triangle that two
crossing rings force. It needs a third colour (scoreboard -> [3, oo)). Any 2-colouring of the plane paints a
copy of it with a matching pair, so a finite "dots and sticks" drawing that 2 colours can't handle is a trap.

UNIT = 2.0 manim.  P = (-1, -0.2), Q = (1, -0.2), crossings (0, -0.2 +- sqrt 3) (shared with S05).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *  # noqa: E402,F401,F403
from geom import triangle, to_scene  # noqa: E402
import s04_triangle_geo as G  # noqa: E402

U = G.U
Z_PAT, Z_RING, Z_STICK, Z_DOT, Z_UI, Z_PANEL, Z_BAR = 0, 1, 2, 3, 4, 9, 10
VR = 0.11                      # vertex radius
PAIRS = [(0, 1), (2, 1), (2, 0)]   # P-Q, R-Q, R-P   (index 0 = P, 1 = Q, 2 = R)
S_SMALL = 0.5                  # triangle scale on the floor (side = 1 manim unit)
W_BAD = 7                      # width of a rule-breaking stick on the floor
# P5 landings, checked with G.Painting (scratch search): at the start spot (G0, 0 deg) P,Q are yellow and R blue;
# the glide to SPOT_A flips only P (at 34 % of the path), never all three alike; margins >= 0.24 at SPOT_A.
SPOT_A = ((-1.888, -0.173), np.radians(56.9), S_SMALL)


def v3(p):
    return np.array([p[0], p[1], 0.0])


# verified geometry: geom.triangle scaled into the scene must hit the fixed coordinates
_T = [to_scene(p, U, (-1, -0.2, 0)) for p in triangle(0.0)]
assert np.allclose(_T[0], v3(G.P0)) and np.allclose(_T[1], v3(G.Q0)) and np.allclose(_T[2], v3(G.R0))
P0, Q0, R0, R1 = v3(G.P0), v3(G.Q0), v3(G.R0), v3(G.R1)
BLEND = {0: BLUE_P, 1: YELLOW_P}


def blend(c, a):
    return interpolate_color(ManimColor(BG), ManimColor(c), a)


def udir(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


# ---------------------------------------------------------------- small builders
def vertex(pos, r=VR):
    c = Circle(radius=r).move_to(pos)
    c.set_fill(BG, 1).set_stroke(INK, 2.5)
    return c.set_z_index(Z_DOT)


def set_paint(dot, color, t):
    """t = 0 hollow ring, t = 1 painted dot with a dark rim (reads on any floor)."""
    dot.set_fill(interpolate_color(ManimColor(BG), ManimColor(color), t), 1)
    dot.set_stroke(interpolate_color(ManimColor(INK), ManimColor(BG), t), 2.5)
    return dot


def paint(dot, color):
    return dot.animate.set_fill(color, 1).set_stroke(BG, 2.5)


def unpaint(dot):
    return dot.animate.set_fill(BG, 1).set_stroke(INK, 2.5)


def ustick(a, b, width=4, color=UNIT_COLOR):
    ln = Line(a, b, color=color, stroke_width=width)
    ln.set_stroke(BG, width + 5, background=True)
    return ln.set_z_index(Z_STICK)


def pulse(pos, color=ACCENT, r=0.14, grow=3.2, width=4):
    """An expanding ring that fades (use inside play: FadeOut removes it)."""
    c = Circle(radius=r, color=color, stroke_width=width).move_to(pos).set_z_index(Z_UI)
    return FadeOut(c, scale=grow)


def polymob(poly, color, stroke=1.3):
    m = VMobject().set_points_as_corners([v3(p) for p in list(poly) + [poly[0]]])
    m.set_fill(color, 1).set_stroke(color, stroke)
    return m


def one_label(a, b, centroid, buff=0.3, size=30):
    """A '1' just outside the stick a-b, with a dark knock-out so crossing lines never cut the digit."""
    mid = (a + b) / 2
    out = mid - centroid
    out = out / np.linalg.norm(out)
    lab = N("1", size, UNIT_COLOR).set_stroke(BG, 7, background=True)
    return lab.move_to(mid + out * buff).set_z_index(Z_UI)


def swatch(pos, color, r=0.26):
    return Dot(pos, radius=r, color=color).set_stroke(BG, 2, background=True).set_z_index(Z_UI)


def reject_mark(pos, size=0.2):
    """A red cross with a dark under-stroke, so the red never tints the swatch beneath it."""
    return cross_mark(pos, size, width=5).set_stroke(BG, 11, background=True).set_z_index(Z_UI + 0.5)


def home_bar(lo=1, hi=None):
    bar = BoundsBar(lo=lo, hi=hi).scale(0.8).to_edge(DOWN, buff=0.3)
    return bar


class S04_Triangle(TimedScene):
    # ------------------------------------------------------------------ helpers
    def w(self, sid, word, nth=0):
        """Start time of `word` in sentence `sid` (from the timeline's word times)."""
        for s in self.tl["sentences"]:
            if s["id"] == sid:
                hits = [x for x in s["words"] if x["w"].strip(".,:;?!").lower() == word.lower()]
                return hits[nth]["s"]
        raise KeyError((sid, word))

    def rigid(self, dots, sticks, st0, st1, cols0=None, bad0=None, fade_frac=0.35, live=None):
        """Glide + turn + scale the triangle rigidly from state st0 to st1 = (centre, angle, scale).
        live=Painting: every frame each dot takes the colour beneath it and a stick whose ends match is red.
        Otherwise painted dots (cols0) fade to hollow over the first `fade_frac` of the move and a BAD stick
        (bad0) calms down likewise."""
        def f(_, a):
            c = (1 - a) * np.asarray(st0[0]) + a * np.asarray(st1[0])
            th = (1 - a) * st0[1] + a * st1[1]
            s = (1 - a) * st0[2] + a * st1[2]
            ps2 = G.tri_points(c, th, s)
            ps = [v3(p) for p in ps2]
            k = min(1.0, a / fade_frac)
            cols = [BLEND[live.color_at(p)] for p in ps2] if live is not None else None
            for i, d in enumerate(dots):
                d.move_to(ps[i])
                if cols is not None:
                    d.set_fill(cols[i], 1).set_stroke(BG, 2.5)
                elif cols0 is not None and cols0[i] is not None:
                    set_paint(d, cols0[i], 1 - k)
            for n, ((i, j), ln) in enumerate(zip(PAIRS, sticks)):
                ln.put_start_and_end_on(ps[i], ps[j])
                if cols is not None:
                    same = cols[i] == cols[j]
                    ln.set_stroke(BAD if same else UNIT_COLOR, W_BAD if same else 4)
                elif bad0 is not None and n == bad0:
                    ln.set_stroke(interpolate_color(ManimColor(BAD), ManimColor(UNIT_COLOR), k),
                                  W_BAD - (W_BAD - 4) * k)
        return UpdateFromAlphaFunc(VGroup(*dots, *sticks), f)

    def sweep(self, center, a0, run_time, keep_arm=False, extra=()):
        """A unit stick pivots once around `center`, drawing its ring. Returns (ring, arm)."""
        th = ValueTracker(0.0)
        arm = ustick(center, center + U * udir(a0))
        arc = VMobject().set_z_index(Z_RING)

        def upd_arm(m):
            m.put_start_and_end_on(center, center + U * udir(a0 + th.get_value()))

        def upd_arc(m):
            m.become(Arc(radius=U, start_angle=a0, angle=max(th.get_value(), 1e-3), arc_center=center,
                         color=UNIT_COLOR, stroke_width=3, stroke_opacity=0.75).set_z_index(Z_RING))

        upd_arc(arc)
        arm.add_updater(upd_arm)
        arc.add_updater(upd_arc)
        self.add(arc, arm)
        self.play(th.animate.set_value(TAU), *extra, run_time=run_time, rate_func=smooth)
        arm.clear_updaters()
        arc.clear_updaters()
        ring = Circle(radius=U, color=UNIT_COLOR, stroke_width=3, stroke_opacity=0.75).move_to(center)
        ring.set_z_index(Z_RING)
        self.remove(arc)
        self.add(ring)
        if not keep_arm:
            self.remove(arm)
        return ring, arm

    # ------------------------------------------------------------------ scene
    def construct(self):
        w = self.w

        # ---------- scoreboard at its home (bottom), on a BG panel, always on top
        bar = home_bar(1).set_z_index(Z_BAR)
        panel = RoundedRectangle(corner_radius=0.2, width=bar.width + 0.5, height=bar.height + 0.3)
        panel.set_fill(BG, 1).set_stroke(width=0).move_to(bar).set_z_index(Z_PANEL)

        # ---------- P1: the plane, a checkerboard, something cleverer
        grid = VGroup()
        for x in range(-7, 8, 2):
            grid.add(Line([x, G.FLOOR_Y, 0], [x, 4.2, 0]))
        for y in (G.FLOOR_Y + 2, G.FLOOR_Y + 4, G.FLOOR_Y + 6):
            grid.add(Line([-7.4, y, 0], [7.4, y, 0]))
        grid.set_stroke(FAINT, 1.5).set_z_index(Z_PAT)

        board = VGroup()
        cell_x = []
        for i in G.CHECK_COLS:
            for j in G.CHECK_ROWS:
                col = blend(BLEND[G.check_color(i, j)], 0.7)
                board.add(polymob(G.square_outline(i, j), col, stroke=1.0))
                cell_x.append(2 * i)
        board.set_z_index(Z_PAT + 0.5)
        board.set_fill(opacity=0).set_stroke(opacity=0)
        cell_x = np.array(cell_x, float)
        warped = board.copy().set_fill(opacity=1).set_stroke(opacity=1)
        for m in warped:
            m.apply_function(lambda p: G.warp(p))

        def wipe(m, a):
            x = -8.2 + a * 18.5
            for c, cx in zip(m, cell_x):
                o = float(np.clip((x - cx) / 2.2, 0, 1))
                c.set_fill(opacity=o).set_stroke(opacity=o)

        # stick 1: along the diagonal of the central blue square (diagonal 2.83 > stick 2.0)
        d = U / 2 * udir(np.pi / 4)
        c1 = np.array([0.0, 0.5, 0])
        st1 = ustick(c1 - d, c1 + d)
        e1 = VGroup(pt(c1 - d, BLUE_P, VR), pt(c1 + d, BLUE_P, VR)).set_z_index(Z_DOT)
        x1 = cross_mark(c1 + np.array([0.6, -0.6, 0]), size=0.17).set_z_index(Z_UI)
        # stick 2: inside a yellow blob of the warped board (clearance checked in s04_triangle_geo)
        ypoly = np.array([G.warp(p) for p in G.square_outline(-1, 1)])
        a2, b2, _ = G.best_segment(ypoly, near=np.array([0, 0.5]))
        a2, b2 = v3(a2), v3(b2)
        st2 = ustick(a2, b2)
        e2 = VGroup(pt(a2, YELLOW_P, VR), pt(b2, YELLOW_P, VR)).set_z_index(Z_DOT)
        nrm = udir(np.arctan2(*(b2 - a2)[:2][::-1]) - np.pi / 2)
        x2 = cross_mark((a2 + b2) / 2 + 0.75 * nrm, size=0.17).set_z_index(Z_UI)

        self.add(panel)
        self.until(1.2, FadeIn(bar), LaggedStart(*[Create(g) for g in grid], lag_ratio=0.08))
        self.at("two", Indicate(bar.cells[1], color=ACCENT, scale_factor=1.45), run_time=0.9)

        self.add(board)
        # checker: wipe, drop, fail -- red complete ~4.6 s, held until "clever" (5.16)
        self.at("checker", UpdateFromAlphaFunc(board, wipe, rate_func=linear), run_time=0.45)
        self.remove(*grid)
        self.play(FadeIn(VGroup(st1, e1), shift=0.6 * DOWN), run_time=0.25)
        self.play(st1.animate.set_stroke(BAD, 6), Create(x1), run_time=0.25)

        # clever: morph (the failed stick leaves in the first half), drop, fail -- red ~6.3 s, held until 7.0
        first_half = lambda t: smooth(min(1.0, 2 * t))  # noqa: E731
        self.at("clever", Transform(board, warped), FadeOut(VGroup(st1, e1, x1), rate_func=first_half),
                run_time=0.6)
        self.play(FadeIn(VGroup(st2, e2), shift=0.6 * DOWN), run_time=0.25)
        self.play(st2.animate.set_stroke(BAD, 6), Create(x2), run_time=0.25)
        self.at(7.0, FadeOut(VGroup(board, st2, e2, x2)), run_time=0.5)

        # ---------- P2: colour a point blue, draw its ring, any point on it is yellow
        dots = [vertex(P0), vertex(Q0), vertex(R0)]
        dP, dQ, dR = dots
        self.at(w("p2s1", "why"), GrowFromCenter(dP), run_time=0.45)
        self.at("blue", paint(dP, BLUE_P), pulse(P0, BLUE_P), run_time=0.5)

        self.at("first_ring", run_time=0)
        ringP, armP = self.sweep(P0, 0.0, self.left("p2s3") - 0.05, keep_arm=True)
        sPQ = armP                                            # the sweep ends on the stick P-Q
        self.at("q", GrowFromCenter(dQ), pulse(Q0, INK), run_time=0.45)
        extra = VGroup(*[vertex(P0 + U * udir(np.radians(a)), r=0.085) for a in (118, 180, 242)])
        self.at(w("p2s3", "must"), LaggedStart(*[GrowFromCenter(e) for e in extra], lag_ratio=0.3),
                run_time=0.7)
        self.at("yellow", paint(dQ, YELLOW_P), *[paint(e, YELLOW_P) for e in extra], pulse(Q0, YELLOW_P),
                run_time=0.5)

        # ---------- P3: the second ring; the crossings are one unit from both
        self.at("second_ring")
        ringQ, _ = self.sweep(Q0, np.pi, 1.6, extra=[FadeOut(extra, rate_func=rush_from)])
        dR1 = vertex(R1).set_stroke(opacity=0.45)
        self.at("cross", GrowFromCenter(dR), GrowFromCenter(dR1), pulse(R0), pulse(R1), run_time=0.7)

        sRQ, sRP = ustick(R0, Q0), ustick(R0, P0)
        low = VGroup(*[DashedLine(R1, X, dash_length=0.12, color=UNIT_COLOR, stroke_width=3)
                       .set_stroke(opacity=0.45) for X in (Q0, P0)]).set_z_index(Z_STICK)
        self.at(w("p3s2", "each"), Create(sRQ), Create(sRP), Create(low), run_time=0.85)
        sticks = [sPQ, sRQ, sRP]                              # in PAIRS order
        cen = (P0 + Q0 + R0) / 3
        # slanted '1's sit 0.55 out: at 0.3 they would land on the other point's ring (|Q - label| = sqrt3 + buff)
        ones = VGroup(*[one_label(dots[i].get_center(), dots[j].get_center(), cen, buff=0.3 if n == 0 else 0.55)
                        for n, (i, j) in enumerate(PAIRS)])
        self.at(w("p3s2", "one"), LaggedStart(*[FadeIn(o, scale=0.6) for o in ones], lag_ratio=0.25),
                run_time=0.6)
        self.at(w("p3s2", "points") + 0.1, FadeOut(low), dR1.animate.set_stroke(opacity=0.3), run_time=0.5)

        # "neither blue nor yellow": try each colour at the crossing
        # swatch row just above R (full paint colours; the dark-rimmed red cross does the rejecting)
        sw_y = R0[1] + 0.72
        swB, swY, swK = swatch([-0.7, sw_y, 0], BLUE_P), swatch([0, sw_y, 0], YELLOW_P), swatch([0.7, sw_y, 0], PINK_P)
        xB, xY = reject_mark(swB.get_center()), reject_mark(swY.get_center())
        self.at(w("p3s3", "crossing"), dR.animate(rate_func=there_and_back).scale(1.5), pulse(R0, INK),
                run_time=0.6)
        # blue: R-P breaks. yellow (straight from blue, no hollow flicker): R-Q breaks. Yellow holds into the pause.
        self.at("nblue", paint(dR, BLUE_P), sRP.animate.set_stroke(BAD, 6), FadeIn(swB, scale=0.5), run_time=0.3)
        self.play(Create(xB), run_time=0.25)
        self.at("nyellow", paint(dR, YELLOW_P), sRP.animate.set_stroke(UNIT_COLOR, 4),
                sRQ.animate.set_stroke(BAD, 6), FadeIn(swY, scale=0.5), run_time=0.3)
        self.play(Create(xY), run_time=0.25)

        # ---------- P4: a third colour -> at least three
        self.at("p4", unpaint(dR), sRQ.animate.set_stroke(UNIT_COLOR, 4), pulse(R0, BAD, grow=3.6),
                run_time=0.55)
        self.at(w("p4s1", "never"), Indicate(VGroup(xB, xY), color=BAD, scale_factor=1.25), run_time=0.55)
        bar3 = home_bar(3).set_z_index(Z_BAR)
        bar3.shift(bar.cells.get_center() - bar3.cells.get_center())
        self.at("three", FadeIn(swK, scale=0.5), paint(dR, PINK_P), pulse(R0, PINK_P), run_time=0.45)
        # the triangle glows: sticks flash ACCENT while a bright glint runs once around the outline (no fill)
        outline = Polygon(R0, P0, Q0).set_fill(opacity=0).set_stroke(INK, 4).set_z_index(Z_STICK + 0.5)
        outline.joint_type = LineJointType.ROUND
        self.play(*[ln.animate(rate_func=there_and_back).set_stroke(ACCENT, 7) for ln in (sRQ, sRP, sPQ)],
                  ShowPassingFlash(outline, time_width=0.35), Transform(bar, bar3), run_time=0.85)
        glow = bar.box.copy().set_stroke(ACCENT, 10, opacity=0.35).set_z_index(Z_BAR)
        self.at(self.t("p4_end") + 0.15, Indicate(bar.box, color=ACCENT, scale_factor=1.06),
                FadeOut(glow, scale=1.12), run_time=0.75)

        # ---------- P5: every 2-colouring of the plane paints a copy of the triangle
        region = G.rect_poly(*G.REGION)
        S, col, cells = G.mosaic(region, 0.62, 8, field_shift=(-0.8, 1.1))
        painting = G.Painting(S, col)
        for st in ((G.G0, 0.0, S_SMALL), SPOT_A):      # both landings: clear 2:1 split, dots well inside a colour
            pts = G.tri_points(*st)
            assert len({painting.color_at(p) for p in pts}) == 2 and min(painting.margin(p) for p in pts) > 0.18, st
        mos_cols = [blend(BLEND[int(k)], 0.62) for poly, k in zip(cells, col) if len(poly) >= 3]
        mos = VGroup(*[polymob(poly, BG) for poly in cells if len(poly) >= 3]).set_z_index(Z_PAT)

        def tint(out=False):
            # opaque cross-fade BG <-> paint: no seams between cells while fading
            def f(m, a):
                k = 1 - a if out else a
                for c, target in zip(m, mos_cols):
                    cc = interpolate_color(ManimColor(BG), target, k)
                    c.set_fill(cc, 1).set_stroke(cc)
            return f

        self.at("p5", FadeOut(VGroup(ringP, ringQ, dR1, swB, swY, swK, xB, xY, ones)),
                *[unpaint(dd) for dd in dots], run_time=0.8)
        self.at(w("p5s1", "idea") + 0.35,
                *[ln.animate(rate_func=there_and_back).set_stroke(ACCENT, 7) for ln in sticks], run_time=1.0)

        st_full = (G.G0, 0.0, 1.0)
        st0 = (G.G0, 0.0, S_SMALL)
        self.at(w("p5s2", "however"), UpdateFromAlphaFunc(mos, tint()),
                self.rigid(dots, sticks, st_full, st0), run_time=1.3)
        self.at("these", *[pulse(dd.get_center(), ACCENT, r=0.13, grow=2.6) for dd in dots],
                *[dd.animate(rate_func=there_and_back).scale(1.45) for dd in dots], run_time=0.6)

        def colours_at(state):
            return [BLEND[painting.color_at(p)] for p in G.tri_points(*state)]

        def match_stick(cols):
            return [n for n, (i, j) in enumerate(PAIRS) if cols[i] == cols[j]][0]

        def flag(bad, pulse_stick=False):
            """BAD rings on the matching pair (+ a width pulse on its red stick)."""
            i, j = PAIRS[bad]
            anims = [pulse(dots[i].get_center(), BAD, r=0.13, grow=2.8), pulse(dots[j].get_center(), BAD, r=0.13, grow=2.8)]
            if pulse_stick:
                anims.append(sticks[bad].animate(rate_func=there_and_back).set_stroke(width=12))
            else:
                anims.append(sticks[bad].animate.set_stroke(BAD, W_BAD))
            return anims

        # landing 1 (where it already sits): painted by the floor, the matching pair is flagged at once
        cols = colours_at(st0)
        bad = match_stick(cols)
        self.at(w("p5s2", "painted"), *[paint(dd, c) for dd, c in zip(dots, cols)], run_time=0.4)
        self.play(*flag(bad), run_time=0.4)
        # "wherever they land": one glide + turn; the dots take the colour beneath them every frame and
        # whichever stick matches right now is red (it hops from P-Q to R-P on the way, never vanishes)
        self.at(w("p5s3", "wherever"), self.rigid(dots, sticks, st0, SPOT_A, live=painting), run_time=0.8)
        cols = colours_at(SPOT_A)
        bad = match_stick(cols)
        # landing 2: "two of them match" -> pulse the pair and its red stick, then HOLD through the pause
        self.at("match", *flag(bad, pulse_stick=True), run_time=0.5)

        # ---------- P6: dots and sticks; a drawing two colours can't handle is a trap
        G6 = np.array([0.0, 0.75])
        st6 = (G6, 0.0, 1.0)                                # upright again, least turning from SPOT_A
        # "forget the plane": floor and paint drain away together while the triangle returns to full size
        self.at(w("p6s1", "forget"), UpdateFromAlphaFunc(mos, tint(out=True), remover=True),
                self.rigid(dots, sticks, SPOT_A, st6, cols0=cols, bad0=bad, fade_frac=1.0), run_time=1.2)
        cen6 = v3(G6)
        lab1 = T("dots and sticks", 34, INK).move_to([0, -0.95, 0]).set_z_index(Z_UI)
        lab2 = T("stick = exactly 1 apart: different colors", 28, DIM).next_to(lab1, DOWN, buff=0.22)
        lab2.set_z_index(Z_UI)
        self.at("dots", *[pulse(dd.get_center(), INK, r=0.13, grow=2.6) for dd in dots],
                *[dd.animate(rate_func=there_and_back).scale(1.5) for dd in dots],
                FadeIn(lab1, shift=0.15 * UP), run_time=0.6)
        self.at(w("p6s1", "sticks"), *[ln.animate(rate_func=there_and_back).set_stroke(INK, 7) for ln in sticks],
                run_time=0.6)
        self.at(w("p6s1", "stick"), FadeIn(lab2, shift=0.15 * UP), run_time=0.6)
        ones6 = VGroup(*[one_label(dots[i].get_center(), dots[j].get_center(), cen6) for i, j in PAIRS])
        self.at(w("p6s1", "one"), LaggedStart(*[FadeIn(o, scale=0.6) for o in ones6], lag_ratio=0.25),
                run_time=0.6)

        # slide left, then a failed 2-colouring
        G6L = np.array([-3.3, 0.75])
        st6L = (G6L, 0.0, 1.0)
        # labels leave first (no '1' left floating where the triangle was), then the triangle slides
        self.at("p6s2", FadeOut(VGroup(lab1, lab2, ones6)), run_time=0.3)
        self.play(self.rigid(dots, sticks, st6, st6L), run_time=0.6)
        # colour: two blues + one yellow; the blue pair's stick is the bad one
        tri_cols = [BLUE_P, YELLOW_P, BLUE_P]
        self.at(w("p6s2", "colored"), LaggedStart(*[paint(dd, c) for dd, c in zip(dots, tri_cols)], lag_ratio=0.3),
                run_time=0.5)
        bad = match_stick(tri_cols)
        self.at(w("p6s2", "two"), sticks[bad].animate.set_stroke(BAD, 6), run_time=0.3)

        tri_box = VGroup(*dots)
        frame = RoundedRectangle(corner_radius=0.25, width=tri_box.width + 1.0, height=tri_box.height + 0.95,
                                 color=ACCENT, stroke_width=4).move_to(tri_box).set_z_index(Z_UI)
        trap = T("trap", 30, ACCENT).next_to(frame, UP, buff=0.18).set_z_index(Z_UI)
        fail = T("2 colors fail", 24, DIM).next_to(frame, DOWN, buff=0.2).set_z_index(Z_UI)
        self.at("trap", FadeIn(frame, scale=1.12), FadeIn(trap, shift=0.1 * DOWN), FadeIn(fail), run_time=0.4)

        icon_c = np.array([3.45, frame.get_center()[1]])
        ipoly = G.rounded_rect_poly(icon_c[0], icon_c[1], 3.2, 2.2, 0.25)
        iS, icol, icells = G.mosaic(ipoly, 0.3, 3, field_scale=2.0, noise=0.8)
        icon = VGroup(*[polymob(p, blend(BLEND[int(k)], 0.55), stroke=0.8) for p, k in zip(icells, icol)
                        if len(p) >= 3])
        border = RoundedRectangle(corner_radius=0.25, width=3.2, height=2.2, color=DIM, stroke_width=2)
        border.move_to(v3(icon_c))
        plane = VGroup(icon, border).set_z_index(Z_PAT + 1)
        plane_lab = T("the plane", 24, DIM).next_to(border, DOWN, buff=0.2).set_z_index(Z_UI)
        arrow = Arrow(frame.get_right(), border.get_left(), buff=0.15, color=ACCENT, stroke_width=3,
                      max_tip_length_to_length_ratio=0.12).set_z_index(Z_UI)
        pcross = cross_mark(v3(icon_c), size=0.42, width=9).set_z_index(Z_UI + 1)
        self.at(w("p6s2", "the"), GrowArrow(arrow), FadeIn(plane, scale=0.9), FadeIn(plane_lab),
                run_time=0.55)
        self.at(w("p6s2", "can't", 1), Create(pcross), run_time=0.35)

        # ---------- end: everything fades, back to the empty background
        rest = [m for m in self.mobjects]
        self.at(self.t("p6_end") + 0.3, *[FadeOut(m) for m in rest], run_time=0.55)

