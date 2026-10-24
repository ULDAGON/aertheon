"""S06 - The zeros and the fold.

P1  the plane from S05 (real part -11..3 across the frame, height 0..~52 above the real axis at y -2.3) and the
    error dial fade in; the easy zeros -2, -4, -6, -8, -10 pop in one per spoken number.
P2  the strip 0 < real part < 1 tints, then the whole plane stretches sideways (content transform, not the camera)
    into the DIAL_ALIGNED layout: real part 0 above the dial's 0 tick, 1 above its 1 tick. 'sum works' right of 1.
P3  an input dot climbs the middle line (real part 1/2); an output panel traces zeta(1/2 + it) (exact, topic.zeta_np);
    at t = 14.1347 the output lands exactly on the origin and the first zero dot appears.
P4  the climb continues through 21.02, 25.01, 30.42 (each crossing timed to its spoken number), then the rest of the
    first ten zeros; two hypothetical mirror rings at 0.2 + 35i and 0.8 + 35i; the left half of the strip folds onto
    the right half about the middle line (the rings meet, the real zeros sit on the crease) and opens again.
P5  the ACCENT critical line draws up past the frame; RH caption.
P6  strip floor 0, 1/2, 1 light up with the dial's own 0, 1/2, 1; '?'.
P7  '?' dissolves; links glow; strip dims; everything fades, the dial last.

Plane geometry: P1 maps (re, h) -> (OX + S0*re, Y0 + KY*h); the stretch x -> -2.5 + (x - OX) * 5/S0 lands it exactly
on DIAL_ALIGNED (asserted below). Zero crossings are driven by one ValueTracker (height t); a dt-clock updater makes
each zero dot pop and the output origin flash at the exact frame the climb passes that zero's height.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403
from scipy.interpolate import PchipInterpolator  # noqa: E402

config.disable_caching = True   # rate functions close over scipy/numpy objects that manim's hasher cannot hash

# ---------------------------------------------------------------- geometry
M = DIAL_ALIGNED
Y0 = M.y0                              # real axis / strip floor, y = -2.3
KY = (M.y1 - M.y0) / M.hmax            # 0.114 manim per unit of height (same before and after the stretch)
S0 = 13.2 / 14                         # P1: real part -11..3 across x -6.6..6.6
OX = 6.6 - 3 * S0                      # scene x of real part 0 in P1
KX = (M.x1 - M.x0) / S0                # horizontal stretch factor of the P2 move


def P1(re, h=0.0):
    return np.array([OX + S0 * re, Y0 + KY * h, 0.0])


def stretch_x(x):
    return M.x0 + (x - OX) * KX


def fwd(p):
    return np.array([stretch_x(p[0]), p[1], p[2]])


def inv(p):
    return np.array([OX + (p[0] - M.x0) / KX, p[1], p[2]])


assert np.allclose(fwd(P1(0, 10)), M.p(0, 10)) and np.allclose(fwd(P1(1, 40)), M.p(1, 40))

# output panel for zeta(1/2 + it)
BOX = (3.4, 6.6, -1.25, 2.35)          # x0, x1, y0, y1
SC = 0.56
O_OUT = np.array([4.42, 0.33, 0.0])    # scene point of output 0


def out_pt(z):
    return O_OUT + SC * np.array([z.real, z.imag, 0.0])


GAM = ZEROS[:10]
TS = np.union1d(np.linspace(0, 50, 3001), GAM)
ZS = zeta_np(0.5 + 1j * TS)
OUT_PTS = np.array([out_pt(z) for z in ZS])
assert np.all(np.abs(ZS[np.searchsorted(TS, GAM)]) < 1e-6)
assert OUT_PTS[:, 0].min() > BOX[0] + 0.05 and OUT_PTS[:, 0].max() < BOX[1] - 0.05
assert OUT_PTS[:, 1].min() > BOX[2] + 0.05 and OUT_PTS[:, 1].max() < BOX[3] - 0.45

Z_GRID, Z_TINT, Z_LINE, Z_INPUT, Z_DOT, Z_FLASH = -2, 0, 2, 3, 4, 5   # zero dots sit on top of the input dot


def out_point_at(t):
    return np.array([np.interp(t, TS, OUT_PTS[:, 0]), np.interp(t, TS, OUT_PTS[:, 1]), 0.0])


def dashed_ring(pos, r=0.14):
    return DashedVMobject(Circle(radius=r), num_dashes=12, dashed_ratio=0.55).set_stroke(BAD, 3).move_to(pos)


class LightUp(Animation):
    """Turn a label to `color` while it swells once (scale there-and-back): one number lighting up."""

    def __init__(self, mob, color, scale=1.25, **kw):
        self.to_color, self.k = ManimColor(color), scale
        super().__init__(mob, **kw)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        self.mobject.become(self.starting_mobject)
        self.mobject.set_color(interpolate_color(ManimColor(self.starting_mobject.get_color()), self.to_color, a))
        self.mobject.scale(1 + (self.k - 1) * there_and_back(alpha))


class S06_Zeros(TimedScene):
    def construct(self):
        dial = ErrorDial()

        # ------------------------------------------------ the plane in P1 coordinates
        top = 3.85
        grid_v = VGroup(*[Line(P1(re) , [P1(re)[0], top, 0]) for re in range(-11, 4) if re != 0])
        grid_h = VGroup(*[Line([-7.2, Y0 + KY * h, 0], [7.2, Y0 + KY * h, 0]) for h in (10, 20, 30, 40, 50)])
        grid = VGroup(grid_v, grid_h).set_stroke(FAINT, 1.5).set_z_index(Z_GRID)
        x_axis = Line([-7.2, Y0, 0], [7.2, Y0, 0], color=NEUTRAL, stroke_width=2.5).set_z_index(Z_GRID)
        y_axis = Line(P1(0), [OX, top, 0], color=NEUTRAL, stroke_width=2.5).set_z_index(Z_GRID)
        h_labels = VGroup(*[N(str(h), 24, DIM).next_to(P1(0, h), LEFT, buff=0.12) for h in (10, 20, 30, 40, 50)])

        sg = strip_group(M, 10, tint=False)          # final strip parts (edges, line, dots, floor labels)
        # floor labels: same text as strip_group's, set a little tighter (26 pt, buff 0.08) so they clear the dial's
        # coin/pin row at y -2.9 (the shared DIAL_ALIGNED default is 28 pt, buff 0.12)
        for lab, v in zip(sg.floor_labels, (0, 0.5, 1)):
            lab.scale(26 / 28).next_to(M.p(v, 0), DOWN, buff=0.08).set_z_index(11)
        zero_lab0 = sg.floor_labels[0].copy().shift((OX - M.x0) * RIGHT)   # '0' at the P1 origin

        easy = VGroup()
        easy_labs = VGroup()
        for k in (2, 4, 6, 8, 10):
            easy.add(pt(P1(-k), INK, r=0.08))
            easy_labs.add(N(f"−{k}", 28, INK).next_to(P1(-k), UP, buff=0.12).set_z_index(11))
        more_dots = N("…", 30, DIM).move_to(P1(-10) + LEFT * 0.55 + UP * 0.06)
        easy_cap = T("easy zeros", 24, DIM).move_to([(P1(-2)[0] + P1(-10)[0]) / 2, Y0 + 0.82, 0])
        where_cap = N("where ζ(s) = 0", 26, DIM).to_corner(UL, buff=0.45)

        # ------------------------------------------------ P1
        self.until(0.8, FadeIn(dial), FadeIn(VGroup(grid, x_axis, y_axis, h_labels, zero_lab0)))
        self.until(1.9, FadeIn(where_cap, shift=0.1 * DOWN))
        self.at(3.9, FadeIn(easy_cap, shift=0.1 * UP), run_time=0.6)
        pops = [(5.36, 0), (6.08, 1), (6.66, 2), (7.30, 3), (7.55, 4)]
        for tm, i in pops:
            anims = [GrowFromCenter(easy[i]), FadeIn(easy_labs[i], shift=0.1 * UP)]
            if i == 4:
                anims.append(FadeIn(more_dots))
            self.at(tm - 0.1, *anims, run_time=0.35 if i < 3 else 0.25)

        # ------------------------------------------------ P2: the strip, and the stretch into DIAL_ALIGNED
        half_w = (M.x1 - M.x0) / 2
        tint_l = Rectangle(width=half_w, height=M.y1 - M.y0, stroke_width=0, fill_color=TEAL_P, fill_opacity=0.18)
        tint_l.move_to([(M.x0 + 0) / 2, (M.y0 + M.y1) / 2, 0]).set_z_index(Z_TINT)
        tint_r = tint_l.copy().move_to([(0 + M.x1) / 2, (M.y0 + M.y1) / 2, 0])
        edge_l, edge_r = sg.edges[0], sg.edges[1]
        strip_final = VGroup(tint_l, tint_r, edge_l, edge_r)
        strip_narrow = strip_final.copy().apply_function(inv)
        self.at("strip", FadeIn(strip_narrow), run_time=0.4)
        # hold the narrow strip through '... narrow strip between zero and one': light its two edges on the two words
        one_lab_n = sg.floor_labels[2].copy().shift((P1(1)[0] - M.x1) * RIGHT)   # '1' under the narrow right edge
        n_edge_l, n_edge_r = strip_narrow[2], strip_narrow[3]
        self.at(11.40, n_edge_l.animate(rate_func=there_and_back).set_stroke(ACCENT, 6),
                Indicate(zero_lab0, color=ACCENT, scale_factor=1.35), run_time=0.55)
        self.at(12.20, n_edge_r.animate(rate_func=there_and_back).set_stroke(ACCENT, 6),
                FadeIn(one_lab_n, scale=0.7), run_time=0.45)

        # then one calm move: the plane stretches sideways into the dial-aligned layout
        movers = []
        for mob in (grid, x_axis, y_axis):
            movers.append((mob, mob.copy().apply_function(fwd)))
        dx = stretch_x(OX) - OX
        for mob in (h_labels, zero_lab0):
            movers.append((mob, mob.copy().shift(dx * RIGHT)))
        movers.append((one_lab_n, sg.floor_labels[2].copy()))
        for d, lab in zip(easy, easy_labs):
            sh = (stretch_x(d.get_center()[0]) - d.get_center()[0]) * RIGHT
            movers.append((d, d.copy().shift(sh)))
            movers.append((lab, lab.copy().shift(sh)))
        sh = (stretch_x(more_dots.get_center()[0]) - more_dots.get_center()[0]) * RIGHT
        movers.append((more_dots, more_dots.copy().shift(sh)))
        stretched = VGroup(T("stretched sideways", 24, DIM), N("↔", 30, DIM))
        stretched.arrange(RIGHT, buff=0.15).move_to([-4.75, Y0 + 0.45, 0])
        self.at(12.68, *[Transform(a, b) for a, b in movers], Transform(strip_narrow, strip_final),
                FadeOut(easy_cap), FadeIn(stretched, shift=0.1 * RIGHT), run_time=1.15, rate_func=smooth)
        self.remove(strip_narrow, easy, easy_labs, more_dots)
        self.add(strip_final)
        # after the stretch zero_lab0 / one_lab_n sit exactly on the strip's floor labels '0' / '1'
        self.remove(zero_lab0, one_lab_n)
        self.add(sg.floor_labels[0], sg.floor_labels[2])

        band = Rectangle(width=6.8 - M.x1, height=M.y1 - M.y0, stroke_width=0, fill_color=TEAL_P, fill_opacity=0.09)
        band.move_to([(M.x1 + 6.8) / 2, (M.y0 + M.y1) / 2, 0]).set_z_index(Z_TINT)
        sum_tag = T("sum works", 24, DIM).move_to([4.6, 1.3, 0])
        only_tag = T("only extended ζ", 24, DIM).move_to([0, 1.3, 0])
        self.at(13.86, FadeIn(band), FadeIn(sum_tag), run_time=0.6)     # on 'reach in here'

        self.at(14.96, FadeIn(only_tag, shift=0.1 * UP), run_time=0.5)
        self.until("p3", FadeOut(VGroup(band, sum_tag, only_tag, stretched)))

        # ------------------------------------------------ P3: walk up the middle
        tr = ValueTracker(0.0)
        inp = pt(M.p(0.5, 0), ACCENT, r=0.1).set_z_index(Z_INPUT)
        inp.add_updater(lambda m: m.move_to(M.p(0.5, tr.get_value())))
        trail = Line(M.p(0.5, 0), M.p(0.5, 0.05), color=ACCENT, stroke_width=2.5, stroke_opacity=0.55).set_z_index(Z_LINE)
        trail.add_updater(lambda m: m.put_start_and_end_on(M.p(0.5, 0), M.p(0.5, max(0.05, tr.get_value()))))
        self.add(trail)
        self.at("walk", GrowFromCenter(inp), FadeIn(sg.floor_labels[1], shift=0.1 * UP), run_time=0.35)
        self.add(inp)

        # output panel
        box = RoundedRectangle(corner_radius=0.12, width=BOX[1] - BOX[0], height=BOX[3] - BOX[2],
                               stroke_color=FAINT, stroke_width=2, fill_color=BG, fill_opacity=1)
        box.move_to([(BOX[0] + BOX[1]) / 2, (BOX[2] + BOX[3]) / 2, 0])
        out_axes = VGroup(Line([BOX[0] + 0.1, O_OUT[1], 0], [BOX[1] - 0.1, O_OUT[1], 0]),
                          Line([O_OUT[0], BOX[2] + 0.1, 0], [O_OUT[0], BOX[3] - 0.5, 0])).set_stroke(FAINT, 1.5)
        cross = VGroup(Line(O_OUT + 0.16 * LEFT, O_OUT + 0.16 * RIGHT), Line(O_OUT + 0.16 * DOWN, O_OUT + 0.16 * UP))
        cross.set_stroke(ACCENT, 3, opacity=0.55)          # the target reads as a target from the start
        target = Circle(radius=0.24).set_stroke(ACCENT, 2, opacity=0.35).move_to(O_OUT)
        o_lab = N("0", 24, DIM).move_to(O_OUT + np.array([-0.42, 0.28, 0]))   # left of 0 only the first arc runs
        out_title = T("ζ's output", 24, DIM).move_to([(BOX[0] + BOX[1]) / 2, BOX[3] - 0.27, 0])
        panel = VGroup(box, out_axes, target, cross, o_lab, out_title).set_z_index(6)
        target.set_z_index(9)
        cross.set_z_index(9)

        vis = ValueTracker(0.0)                              # opacity of the output path and dot (they fade in)
        path = VMobject(stroke_color=INK, stroke_width=2.5).set_z_index(7)

        def upd_path(m):
            tv = tr.get_value()
            n = int(np.searchsorted(TS, tv))
            pts = np.vstack([OUT_PTS[:max(1, n)], out_point_at(tv)])
            if len(pts) < 2:
                pts = np.vstack([pts, pts[-1] + 1e-4 * RIGHT])
            m.set_points_as_corners(pts)
            m.set_stroke(opacity=vis.get_value())
        path.add_updater(upd_path)
        upd_path(path)
        out_dot = pt(out_point_at(0), ACCENT, r=0.09).set_z_index(8)
        out_dot.add_updater(lambda m: m.move_to(out_point_at(tr.get_value())).set_opacity(vis.get_value()))

        # zero events: pop the dot, flash the output origin and the new dot, fade in the label
        dots = sg.dots
        for d in dots:
            d.set_z_index(Z_DOT)
        base_w = dots[0].width
        flash_o = VGroup(*[Circle(radius=0.1).set_stroke(ACCENT, 5).move_to(O_OUT) for _ in GAM]).set_z_index(9)
        flash_z = VGroup(*[Circle(radius=0.1).set_stroke(ACCENT, 4).move_to(d.get_center()) for d in dots])
        flash_z.set_z_index(Z_FLASH)
        z_labs = VGroup(N("½ + 14.13 i", 28, INK),
                        *[N(f"{g:.2f}", 24, DIM) for g in GAM[1:4]])
        for k, lab in enumerate(z_labs):
            lab.next_to(dots[k], RIGHT, buff=0.2)
        # clock = scene time; extra = second pulses (scene times) that re-flash a zero after it landed
        state = {"clock": self.now, "trig": [None] * len(GAM), "extra": {0: [25.17]}}

        def upd_events(m, dt):
            state["clock"] += dt
            tv = tr.get_value()
            hot = 0.0
            for k, g in enumerate(GAM):
                if state["trig"][k] is None and tv >= g - 1e-9:
                    state["trig"][k] = state["clock"]
                tk = state["trig"][k]
                a = None if tk is None else state["clock"] - tk
                if a is not None:
                    last = max([tk] + [p for p in state["extra"].get(k, []) if p <= state["clock"]])
                    b = state["clock"] - last
                d, fo, fz = dots[k], flash_o[k], flash_z[k]
                if a is None:
                    d.set_opacity(0)
                    fo.set_stroke(opacity=0)
                    fz.set_stroke(opacity=0)
                    if k < len(z_labs):
                        z_labs[k].set_opacity(0)
                    continue
                f = smooth(min(1.0, a / 0.25))
                bump = 0.5 if b == a else 0.8
                d.set_opacity(1).scale_to_fit_width(max(0.02, base_w * (0.3 + 0.7 * f) * (1 + bump * there_and_back(min(1, b / 0.6)))))
                d.move_to(M.p(0.5, g))
                u = min(1.0, b / (0.6 if b == a else 0.8))
                fo.scale_to_fit_width(0.2 + 0.9 * u).move_to(O_OUT).set_stroke(opacity=1 - u)
                fz.scale_to_fit_width(0.2 + 0.6 * u).move_to(M.p(0.5, g)).set_stroke(opacity=1 - u)
                hot = max(hot, 1 - u)
                if k < len(z_labs):
                    z_labs[k].set_opacity(min(1.0, a / 0.35))
            v = vis.get_value()
            cross.set_stroke(ACCENT, 3 + 2 * hot, opacity=(0.55 + 0.45 * hot) * v)
            target.set_stroke(ACCENT, 2 + 2 * hot, opacity=(0.35 + 0.65 * hot) * v)

        events = VGroup(dots, flash_o, flash_z, z_labs)
        events.add_updater(upd_events)
        upd_events(events, 0)
        self.add(events)

        def climb(fn, t_end, *extra):
            """Move tr along the schedule fn(time) from now until scene time t_end."""
            t0 = self.now
            v0, v1 = float(fn(t0)), float(fn(t_end))
            rf = lambda a: (float(fn(t0 + a * (t_end - t0))) - v0) / (v1 - v0)
            self.until(t_end, tr.animate(rate_func=rf).set_value(v1), *extra)

        T0, T1 = self.now, self.t("first")
        sched3 = lambda tm: GAM[0] * smooth(np.clip((tm - T0) / (T1 - T0), 0, 1))
        climb(sched3, self.t("watch") - 0.1)
        # 'watch where zeta sends you': the panel opens quickly, and a thin arrow says the right-hand dot is where
        # zeta sends the climbing one
        self.add(path, out_dot)
        a0, a1 = np.array([0.32, -1.55, 0]), np.array([BOX[0] - 0.08, -0.05, 0])
        z_arrow = CurvedArrow(a0, a1, angle=-0.55, color=DIM, stroke_width=2.5, tip_length=0.18)
        z_sym = N("ζ", 28, DIM).move_to(z_arrow.point_from_proportion(0.5) + np.array([-0.12, 0.3, 0]))
        z_hint = VGroup(z_arrow, z_sym).set_z_index(6)
        climb(sched3, self.t("watch") + 0.5, FadeIn(panel), vis.animate.set_value(1.0), Create(z_arrow), FadeIn(z_sym))
        climb(sched3, T1 - 0.7)
        climb(sched3, T1, FadeOut(z_hint))
        self.until("more")

        # ------------------------------------------------ P4: more zeros, then the fold
        knots_t = [26.57, 27.45, 28.30, 28.92, 29.65]      # the last six zeros belong to 'and on'
        knots_v = [GAM[0], GAM[1], GAM[2], GAM[3], 50.0]
        sched4 = PchipInterpolator(knots_t, knots_v)
        climb(sched4, 29.65)
        self.until(30.3)                                     # let the last flashes finish
        events.clear_updaters()
        for k, d in enumerate(dots):
            d.set_opacity(1).scale_to_fit_width(base_w).move_to(M.p(0.5, GAM[k]))
        self.remove(flash_o, flash_z)
        inp.clear_updaters()
        trail.clear_updaters()
        path.clear_updaters()
        out_dot.clear_updaters()
        self.until("pairs", FadeOut(VGroup(panel, path, out_dot, inp)), FadeOut(z_labs))

        ring_r = dashed_ring(M.p(0.8, 35)).set_z_index(Z_DOT)
        ring_l = dashed_ring(M.p(0.2, 35)).set_z_index(Z_DOT)
        tag_r = T("hypothetical", 24, DIM).next_to(ring_r, UP, buff=0.14).set_x(1.25)
        tag_l = T("hypothetical", 24, DIM).next_to(ring_l, UP, buff=0.14).set_x(-1.25)
        self.play(Create(ring_l), Create(ring_r), FadeIn(tag_l), FadeIn(tag_r), run_time=0.6)

        left_half = VGroup(tint_l, edge_l, ring_l)
        self.at(32.95, Rotate(left_half, PI, axis=UP, about_point=ORIGIN), FadeOut(tag_l), run_time=1.0)
        self.at(34.63, Indicate(VGroup(ring_l, ring_r), color=BAD, scale_factor=1.35), run_time=0.6)
        self.at(35.37, LaggedStart(*[Indicate(d, color=ACCENT, scale_factor=1.8) for d in dots], lag_ratio=0.12),
                run_time=0.8)
        self.at(36.2, Rotate(left_half, -PI, axis=UP, about_point=ORIGIN), FadeIn(tag_l), run_time=0.75)

        # ------------------------------------------------ P5: the claim
        rh = VGroup(VGroup(T("Riemann", 26, INK, weight=BOLD), T("Hypothesis:", 26, INK, weight=BOLD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12), T("every zero", 26, INK),
                    T("in the strip", 26, INK), T("has real part ½", 26, ACCENT))
        rh.arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UL, buff=0.45)
        self.at(37.3, FadeOut(where_cap), FadeIn(rh[0], shift=0.1 * DOWN), run_time=0.7)
        crit = Line(M.p(0.5, 0), [M.x0 + 0.5 * (M.x1 - M.x0), 4.3, 0], color=ACCENT, stroke_width=4).set_z_index(Z_LINE)
        self.at("claim", FadeOut(VGroup(ring_l, ring_r, tag_l, tag_r)), Create(crit), FadeIn(rh[1:3], shift=0.1 * DOWN),
                run_time=1.3)
        self.remove(trail)
        self.at(40.2, LaggedStart(*[Indicate(d, color=ACCENT, scale_factor=1.9) for d in dots], lag_ratio=0.18),
                run_time=1.5)
        rp = T("real part ½", 24, ACCENT).next_to(M.p(0.5, 46), RIGHT, buff=0.18)
        self.at(41.85, FadeIn(rp, shift=0.1 * LEFT), run_time=0.5)
        self.at(43.1, FadeIn(rh[3], shift=0.1 * DOWN), run_time=0.5)

        # ------------------------------------------------ P6: the floor is the dial
        self.at("p6", rh[:3].animate.set_color(DIM), run_time=0.6)
        links = VGroup()
        for i, v in enumerate((0, 0.5, 1)):
            a = sg.floor_labels[i].get_bottom() + 0.04 * DOWN
            b = dial.ticks[i].get_top() + 0.03 * UP
            links.add(DashedLine(a, b, dash_length=0.06, dashed_ratio=0.55).set_stroke(ACCENT, 3, opacity=0.8)
                      .set_z_index(12))
        for tm, i in ((46.55, 0), (47.27, 1), (47.81, 2)):
            self.at(tm, LightUp(sg.floor_labels[i], ACCENT), LightUp(dial.labels[i], ACCENT),
                    Create(links[i]), run_time=0.45)
        self.at(48.8, dial.ruler.animate(rate_func=there_and_back).set_stroke(ACCENT, 9),
                links.animate.set_stroke(DIM, 2.5, opacity=1), run_time=1.0)
        q = N("?", 110, ACCENT).move_to([4.5, 0.6, 0])
        self.at("coincidence", FadeIn(q, scale=0.6), run_time=0.6)
        self.at(51.8, Indicate(q, color=ACCENT, scale_factor=1.15), run_time=0.7)

        # ------------------------------------------------ P7: it isn't
        self.at(52.9, FadeOut(q, scale=1.3), run_time=0.55)
        strip_all = VGroup(grid, x_axis, y_axis, h_labels, tint_l, tint_r, edge_l, edge_r, crit, dots, rp)
        self.at("goal", strip_all.animate.fade(0.4),
                *[l.animate(rate_func=there_and_back).set_stroke(ACCENT, 5) for l in links], run_time=1.0)
        rest = [m for m in self.mobjects if m is not dial]
        self.until("p7_end")
        self.until("end", AnimationGroup(FadeOut(Group(*rest)), FadeOut(dial), lag_ratio=0.45), min_run_time=0.3)

