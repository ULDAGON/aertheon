"""S10_WhyHard: why checking isn't proving.

  p1  Dial (best=True) and the DIAL_ALIGNED strip with its ten zeros fade in, a DIM 'height' arrow on its right.
      '≈ 12.36 trillion zeros checked ?' on the question; it leaves on "infinitely many", when the strip's height
      range grows from 50 (readout 'height shown' at its top right): the exact zeros slide down and crowd into a
      dense column. The race ends exactly at height 3 × 10¹² on "leaves": the whole view turns green ('✓ checked /
      12.36 trillion zeros', with a 'height 3 × 10¹²' tick riding its top), then shrinks to a sliver while the
      readout races on to 10¹⁰⁰ and the line above turns DIM and dashed: 'unchecked'.
  p2  li(x) − π(x) (exact, x = 10 … 10⁸, log scales) stays above zero (line first, then its fill); Littlewood 1914;
      an ACCENT arrow 'must cross' into a faint staircase-blue zone 'below 0: staircase on top'; the axis
      compresses, a '…' break, and a dashed illustrative curve ('illustration / not to scale') starts where the
      data ended, keeps growing, then plunges across zero near '≈ 10³¹⁶ ?' (a 317-digit number).
  p3  The strip returns. The share-on-the-line bar as in S09 (> 40% solid, '> 67%' half), dashed DIM to 100%
      'even this'; a hypothetical rogue at height 45 (0.8) and 'its mirror' (0.2) split off the line; a BAD marker
      under the dial's ruler slides from ½ to 0.8 ('0.8'), a dashed drop links the rogue to it, 'Riemann?' dims
      meanwhile. Then the window pulses: 'proven: somewhere in here' with a bracket over ½..1 pointing down at it;
      an 'enlarged' callout of the window's right end (0.95 .. 1) marks 0.99 and hatches the 0.99..1 sliver
      'ruled out? ✗'.
  p4  'Guth and Maynard · 2024'; soft 'room for rebels' shading (growing from nothing at ½ toward the edges,
      right side and its 'mirror'), which thins to half: 'less room for rebels'; 'beats Ingham's 1940 bound (near
      real part ¾)'. Everything fades, the dial last.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: F401,F403,E402
from topic import *  # noqa: F401,F403,E402

# p1's strip is driven by trackers through always_redraw; never reuse a cached partial movie.
config.disable_caching = True

M = DIAL_ALIGNED                      # real part 0..1 over x -2.5..2.5, height over y -2.3..3.4
SX0, SX1, SY0, SY1 = M.x0, M.x1, M.y0, M.y1
CHECKED = 3e12                        # Platt and Trudgian: every zero up to this height is on the line
L_CK = float(np.log10(CHECKED))
L50 = np.log10(50)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def sup(n):
    return str(n).translate(SUP)


def dashed_ring(pos, r=0.2, color=BAD):
    c = Circle(radius=r, color=color, stroke_width=4).move_to(pos)
    return DashedVMobject(c, num_dashes=10, dashed_ratio=0.6)


def height_text(L):
    """Readout for the top of the view: plain digits (one significant digit) up to 10¹², then 10ⁿ."""
    if L < 12.95:
        v = 10 ** L
        e = int(np.floor(np.log10(v)))
        m = int(round(v / 10 ** e))
        if m == 10:
            m, e = 1, e + 1
        return f"{m * 10 ** e:,}"
    return "10" + sup(int(np.floor(L + 1e-9)))


# ------------------------------------------------------------------ p2 graph (li − π on log scales)
GX0, GX1 = -5.3, 4.9                  # log10 x = 1 .. 8
GX1C = 0.1                            # after the compression at {#cross}
GY0, GK = -1.05, 1.1                  # zero line; units per decade of the gap (symmetric log scale)


def gy(v):
    v = np.asarray(v, float)
    return GY0 + GK * np.sign(v) * np.log10(1 + np.abs(v))


def gap_data():
    xs = np.logspace(1, 8, 320)
    P = primes_upto(100_000_001)
    g = li(xs) - np.searchsorted(P, xs, side="right")
    assert g.min() > 0 and abs(g[-1] - 754.38) < 0.05
    return np.log10(xs), g


def gap_curve(lx, g, x1):
    X = GX0 + (x1 - GX0) * (lx - 1) / 7
    pts = [np.array([a, b, 0]) for a, b in zip(X, gy(g))]
    line = VMobject(stroke_color=CURVE_COLOR, stroke_width=3.5).set_points_as_corners(pts)
    fill = Polygon(*([np.array([X[0], GY0, 0])] + pts[::4] + [pts[-1], np.array([X[-1], GY0, 0])]),
                   stroke_width=0, fill_color=CURVE_COLOR, fill_opacity=0.14)
    return line, fill


def x_ticks(x1):
    g = VGroup()
    for k in range(1, 9):
        x = GX0 + (x1 - GX0) * (k - 1) / 7
        tick = Line([x, GY0 - 0.08, 0], [x, GY0 + 0.08, 0], color=NEUTRAL, stroke_width=2)
        lab = N("10" + (sup(k) if k > 1 else ""), 24, DIM).move_to([x, GY0 - 0.34, 0])
        g.add(VGroup(tick, lab))
    return g


class S10_WhyHard(TimedScene):
    def construct(self):
        dial = ErrorDial(best=True)

        # ============================================================ P1: infinitely many zeros
        sg = strip_group(M, 10, labels=False)   # floor labels would sit under the dial panel; the dial's own 0 ½ 1 are right below
        # the vertical direction is height: a DIM arrow on the strip's right side
        h_ax = Arrow([SX1 + 0.3, SY0 + 0.25, 0], [SX1 + 0.3, 2.25, 0], buff=0, color=DIM, stroke_width=3,
                     max_tip_length_to_length_ratio=0.07)
        h_ax_lab = T("height", 24, DIM).rotate(PI / 2).next_to(h_ax, RIGHT, buff=0.12)
        self.until(1.0, FadeIn(dial), FadeIn(sg), FadeIn(h_ax), FadeIn(h_ax_lab))

        q_num = N("≈ 12.36 trillion", 30, INK)
        q_sub = T("zeros checked", 24, DIM)
        q_grp = VGroup(q_num, q_sub).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.0, 0]).align_to([3.55, 0, 0], LEFT)
        q_mark = N("?", 60, ACCENT).next_to(q_grp, RIGHT, buff=0.3)
        self.at(1.05, FadeIn(q_grp, shift=0.15 * UP), run_time=0.6)
        self.at(1.62, GrowFromCenter(q_mark), run_time=0.5)

        # --- the dynamic strip: height range 0..10^L
        L = ValueTracker(L50)
        band_op = ValueTracker(0.0)
        unck_op = ValueTracker(0.0)

        def H():
            return 10 ** L.get_value()

        def y_ck():
            """Scene y of the top of the checked part (heights up to 3e12)."""
            return min(SY1, SY0 + (SY1 - SY0) * CHECKED / H())

        def dens():
            return float(np.clip((L.get_value() - 2.1) / 0.7, 0, 1))

        def make_dots():
            h = H()
            if dens() >= 1:
                return VGroup()
            r = 0.07 * float(np.clip((50 / h) ** 0.35, 0.4, 1))
            op = 1 - dens()
            g = VGroup()
            for z in ZEROS[ZEROS < h]:
                d = Dot(M.p(0.5, 0) + UP * (SY1 - SY0) * z / h, radius=r, color=INK, fill_opacity=op)
                if r > 0.05:
                    d.set_stroke(BG, width=2, background=True, opacity=op)
                g.add(d)
            return g

        def make_line():
            yc = y_ck()
            g = VGroup(Line(M.p(0.5, 0), [0, max(yc, SY0 + 0.02), 0], color=ACCENT, stroke_width=3))
            if dens() > 0:   # the zeros crowd into a dense column of checked zeros
                g.add(Line(M.p(0.5, 0), [0, max(yc, SY0 + 0.02), 0], color=INK, stroke_width=6,
                           stroke_opacity=0.9 * dens()))
            if SY1 - yc > 0.1:
                g.add(DashedLine([0, yc, 0], [0, SY1, 0], color=DIM, stroke_width=3, dash_length=0.12))
            return g

        def make_band():
            top = max(y_ck(), SY0 + 0.07)
            return Rectangle(width=SX1 - SX0, height=top - SY0, stroke_width=0, fill_color=GOOD,
                             fill_opacity=0.28 * band_op.get_value()).move_to([0, (top + SY0) / 2, 0])

        # the band's labels (left of the strip): a height tick riding on the band's top, the zero count under it
        tick_lab = VGroup(T("height", 24, DIM), N("3 × 10¹²", 26, DIM)).arrange(RIGHT, buff=0.12)
        ck_mark = check_mark(ORIGIN, size=0.11)
        cnt_lab = VGroup(VGroup(ck_mark, T("checked", 24, DIM)).arrange(RIGHT, buff=0.14),
                         VGroup(N("12.36 trillion", 26, INK), T("zeros", 24, DIM)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
                         ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        LAB_R = SX0 - 0.32

        def make_ck_label():
            yc = y_ck()
            yt = max(yc, SY0 + 1.05)            # the stack stops at the floor; a leader then reaches the tick
            tl = tick_lab.copy().move_to([0, yt, 0]).align_to([LAB_R, 0, 0], RIGHT)
            cl = cnt_lab.copy().next_to(tl, DOWN, buff=0.2).align_to([LAB_R, 0, 0], RIGHT)
            lead = Line([LAB_R + 0.06, yt, 0], [SX0 - 0.02, max(yc, SY0 + 0.02), 0], color=DIM, stroke_width=2)
            return VGroup(lead, tl, cl).set_opacity(band_op.get_value())

        unck = T("unchecked", 24, DIM)

        def make_unck():
            yc = y_ck()
            lab = unck.copy().move_to([0, max((yc + SY1) / 2, yc + 0.5), 0]).align_to([SX0 - 0.25, 0, 0], RIGHT)
            return lab.set_opacity(unck_op.get_value())

        h_lab = T("height shown", 24, DIM)
        h_tick = Line([SX1, SY1, 0], [SX1 + 0.25, SY1, 0], color=DIM, stroke_width=2)

        def make_readout():
            n = N(height_text(L.get_value()), 30, INK)
            return n.next_to(h_lab, DOWN, buff=0.1, aligned_edge=LEFT)

        h_lab.move_to([0, SY1, 0]).align_to([SX1 + 0.4, 0, 0], LEFT)
        band = always_redraw(make_band)
        dline = always_redraw(make_line)
        ddots = always_redraw(make_dots)
        ck_live = always_redraw(make_ck_label)
        unck_live = always_redraw(make_unck)
        readout = always_redraw(make_readout)
        # identical swap: the static line and dots give way to the live ones
        self.remove(sg.line, sg.dots)
        sg.remove(sg.line, sg.dots)
        self.add(band, dline, ddots, ck_live, unck_live)

        # "infinitely many zeros": the zero count leaves (heights only from here on); slow start
        # (50, 500, 5,000 readable), then faster, ending exactly at the checked height 3 × 10¹²
        self.at("infinite", FadeOut(q_grp), FadeOut(q_mark), FadeIn(h_lab), FadeIn(h_tick), FadeIn(readout),
                run_time=0.4)
        self.until("left_over", L.animate.set_value(L_CK), rate_func=lambda t: t ** 2.1)
        # "any check leaves": the whole view is checked ...
        self.at("left_over", band_op.animate.set_value(1.0), run_time=0.3)
        # "... infinitely many unchecked": the checked band shrinks to a sliver
        self.play(L.animate.set_value(13.2), run_time=0.55, rate_func=rate_functions.ease_in_sine)
        self.play(L.animate(rate_func=linear).set_value(14.6), run_time=0.5)
        self.until(7.5, L.animate(rate_func=rate_functions.ease_in_sine).set_value(100),
                   unck_op.animate(rate_func=linear).set_value(1.0))
        up_arrow = Arrow([0, SY1 - 0.35, 0], [0, SY1 + 0.25, 0], buff=0, color=DIM, stroke_width=3,
                         max_tip_length_to_length_ratio=0.35)
        self.until("p1_end", FadeIn(up_arrow, shift=0.1 * UP))

        # ============================================================ P2: the primes fooled us before
        p1_live = VGroup(band, dline, ddots, ck_live, unck_live, readout)
        for m in p1_live:
            m.clear_updaters()
        p1_all = VGroup(sg, p1_live, h_lab, h_tick, h_ax, h_ax_lab, up_arrow)
        self.until(9.2, FadeOut(p1_all))
        self.remove(p1_live)

        lx, gv = gap_data()
        zero_line = Line([GX0, GY0, 0], [5.6, GY0, 0], color=NEUTRAL, stroke_width=3)
        y_axis = Line([GX0, GY0, 0], [GX0, gy(1000) + 0.15, 0], color=NEUTRAL, stroke_width=2)
        y_ticks = VGroup()
        for v, s in ((0, "0"), (10, "10"), (100, "100"), (1000, "1,000")):
            yy = float(gy(v))
            y_ticks.add(VGroup(Line([GX0 - 0.08, yy, 0], [GX0 + 0.08, yy, 0], color=NEUTRAL, stroke_width=2),
                               N(s, 24, DIM).next_to([GX0 - 0.1, yy, 0], LEFT, buff=0.12)))
        xt = x_ticks(GX1)
        title = VGroup(T("Gauss's curve", 26, CURVE_COLOR), T("−", 26, INK), T("staircase", 26, PRIME_COLOR)
                       ).arrange(RIGHT, buff=0.15).move_to([0, 3.2, 0]).align_to([GX0 - 0.9, 0, 0], LEFT)
        logtag = T("log scales", 24, DIM).move_to([-3.6, GY0 - 0.78, 0])
        axes = VGroup(zero_line, y_axis, y_ticks, xt)
        self.until(10.3, FadeIn(axes), FadeIn(title, shift=0.1 * DOWN), FadeIn(logtag))

        g_line, g_fill = gap_curve(lx, gv, GX1)
        self.at("below", Create(g_line), run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
        below_tag = T("every x checked: staircase below", 24, DIM).move_to([-2.3, 2.62, 0])
        self.until(14.3, FadeIn(g_fill), FadeIn(below_tag, shift=0.1 * UP))
        self.at(14.3, Indicate(g_line, color=CURVE_COLOR, scale_factor=1.0), run_time=0.8)

        lw = VGroup(T("Littlewood · 1914", 26, INK), T("staircase must cross above", 24, DIM)
                    ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        lw.move_to([0, 3.05, 0]).align_to([6.55, 0, 0], RIGHT)
        self.at("littlewood", FadeIn(lw[0], shift=0.1 * DOWN), run_time=0.6)

        # below the zero line = the staircase is on top: a faint staircase-coloured zone, named once
        zone_y1 = -2.45
        st_zone = Rectangle(width=6.3 - GX0, height=GY0 - zone_y1, stroke_width=0, fill_color=PRIME_COLOR,
                            fill_opacity=0.12).move_to([(GX0 + 6.3) / 2, (GY0 + zone_y1) / 2, 0])
        below0 = VGroup(T("below 0:", 24, DIM), T("staircase on top", 24, PRIME_COLOR)).arrange(RIGHT, buff=0.14)
        below0.move_to([0, -2.2, 0]).align_to([6.4, 0, 0], RIGHT)
        end_pt = g_line.get_end()
        arrow = Arrow(end_pt + RIGHT * 0.45 + DOWN * 0.1, [end_pt[0] + 0.45, GY0 - 0.3, 0], buff=0,
                      color=ACCENT, stroke_width=5, max_tip_length_to_length_ratio=0.12).set_z_index(2)
        self.at("must", GrowArrow(arrow), FadeIn(lw[1], shift=0.1 * DOWN), FadeIn(st_zone), FadeIn(below0),
                run_time=0.8)
        self.at(19.9, Indicate(arrow, color=ACCENT, scale_factor=1.15), run_time=0.8)   # "cross above"

        # {#cross}: compress 10..10^8, insert a break, draw the illustrative far-out dip
        g_line2, g_fill2 = gap_curve(lx, gv, GX1C)
        xt2 = x_ticks(GX1C)
        zero_a = Line([GX0, GY0, 0], [GX1C + 0.45, GY0, 0], color=NEUTRAL, stroke_width=3)
        zero_b = Line([GX1C + 1.05, GY0, 0], [6.3, GY0, 0], color=NEUTRAL, stroke_width=3)
        brk = VGroup(*[Line([x - 0.07, GY0 - 0.14, 0], [x + 0.07, GY0 + 0.14, 0], color=NEUTRAL, stroke_width=3)
                       for x in (GX1C + 0.45, GX1C + 1.05)])
        dots3 = N("…", 36, DIM).move_to([GX1C + 0.75, GY0 + 0.05, 0])
        y_labs = VGroup(*[t[1] for t in y_ticks])
        self.at("cross", Transform(g_line, g_line2), Transform(g_fill, g_fill2), Transform(xt, xt2),
                Transform(zero_line, zero_a), FadeOut(arrow), y_labs.animate.set_opacity(0.3),
                FadeIn(brk), FadeIn(dots3), logtag.animate.move_to([(GX0 + GX1C) / 2, GY0 - 0.78, 0]), run_time=1.0)

        # the illustration starts where the real data ended (gap ≈ 754, ~2.9 decades), keeps growing, then plunges
        fx0, fx1 = GX1C + 1.35, 6.2
        ctrl = [(0.0, 2.92), (0.07, 2.8), (0.14, 3.05), (0.22, 2.85), (0.3, 3.1), (0.37, 2.95), (0.43, 2.3),
                (0.5, 0.0), (0.58, -0.6), (0.66, 0.0), (0.74, 1.5), (0.82, 2.5), (0.91, 2.75), (1.0, 3.05)]
        far_pts = [np.array([fx0 + (fx1 - fx0) * s, GY0 + GK * v, 0]) for s, v in ctrl]
        far = VMobject(stroke_color=CURVE_COLOR, stroke_width=4).set_points_smoothly(far_pts)
        far_d = DashedVMobject(far, num_dashes=70, dashed_ratio=0.55)
        xc = fx0 + (fx1 - fx0) * 0.5
        cross_dot = pt([xc, GY0, 0], ACCENT, r=0.08)
        c_lab = N("≈ 10³¹⁶ ?", 26, INK).next_to([xc - 0.12, GY0 - 0.12, 0], DL, buff=0.05)
        c_sub = T("a 317-digit number", 24, DIM).next_to(c_lab, DOWN, buff=0.12).align_to(c_lab, RIGHT)
        illu = VGroup(T("illustration", 24, DIM), T("not to scale", 24, DIM)).arrange(DOWN, buff=0.08)
        illu.move_to([(fx0 + xc) / 2 - 0.1, 0.45, 0])
        self.play(FadeIn(zero_b), Create(far_d), FadeIn(illu), run_time=1.2)
        self.play(GrowFromCenter(cross_dot), FadeIn(c_lab, shift=0.1 * UP), run_time=0.5)
        self.at(23.9, FadeIn(c_sub, shift=0.1 * UP), run_time=0.6)            # "seventeen digits"
        self.at(24.9, Flash(cross_dot, color=ACCENT, line_length=0.18, flash_radius=0.2), run_time=0.6)

        p2_all = VGroup(axes, zero_b, brk, dots3, title, logtag, g_line, g_fill, below_tag, lw, far_d,
                        cross_dot, c_lab, c_sub, illu, st_zone, below0)
        self.until("p3", FadeOut(p2_all, run_time=0.8))

        # ============================================================ P3: one rogue would move the dial
        sg3 = strip_group(M, 10, labels=False)

        # the share-on-the-line bar, as S09 left it: > 40% solid, up to 67.25% half (a preprint)
        bx, by0, by1 = -4.55, -1.95, 2.55
        bar_out = Rectangle(width=0.5, height=by1 - by0, stroke_color=NEUTRAL, stroke_width=2.5
                            ).move_to([bx, (by0 + by1) / 2, 0])
        y40 = by0 + 0.40 * (by1 - by0)
        y67 = by0 + 0.6725 * (by1 - by0)
        fill40 = Rectangle(width=0.5, height=y40 - by0, stroke_width=0, fill_color=ACCENT, fill_opacity=0.9
                           ).move_to([bx, (by0 + y40) / 2, 0])
        fill67 = Rectangle(width=0.5, height=y67 - y40, stroke_width=0, fill_color=ACCENT, fill_opacity=0.5
                           ).move_to([bx, (y40 + y67) / 2, 0])
        fills = VGroup(fill40, fill67)
        lab67 = N("> 67%", 24, ACCENT).next_to([bx - 0.25, y67, 0], LEFT, buff=0.12)
        pre67 = T("preprint", 24, DIM).next_to(lab67, DOWN, buff=0.1).align_to(lab67, RIGHT)
        lab40 = N("40%", 24, ACCENT).next_to([bx - 0.25, y40, 0], LEFT, buff=0.12)
        bar_labs = VGroup(lab67, pre67, lab40)
        bar_cap = T("zeros on the line", 24, DIM).next_to(bar_out, DOWN, buff=0.15)
        self.play(FadeIn(sg3), FadeIn(bar_out), FadeIn(bar_cap), GrowFromEdge(fills, DOWN), FadeIn(bar_labs), run_time=0.9)
        ext = DashedVMobject(Rectangle(width=0.5, height=by1 - y67, stroke_color=DIM, stroke_width=2.5),
                             num_dashes=22).move_to([bx, (y67 + by1) / 2, 0])
        ext_fill = Rectangle(width=0.5, height=by1 - y67, stroke_width=0, fill_color=DIM, fill_opacity=0.3
                             ).move_to([bx, (y67 + by1) / 2, 0])
        lab100 = N("100%", 24, DIM).next_to([bx - 0.25, by1, 0], LEFT, buff=0.12)
        even = T("even this", 24, DIM).next_to([bx + 0.25, by1 - 0.1, 0], RIGHT, buff=0.2)
        self.at(27.45, GrowFromEdge(ext_fill, DOWN), Create(ext), run_time=1.5)   # "almost all"
        self.until("almost", FadeIn(lab100), FadeIn(even, shift=0.1 * DOWN))

        H_R = 45.0
        on_line = M.p(0.5, H_R)
        rog, twin = dashed_ring(on_line), dashed_ring(on_line)
        r_tag = VGroup(T("one rogue?", 24, INK), T("hypothetical", 24, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        r_tag.next_to([SX1, on_line[1], 0], RIGHT, buff=0.3)
        mirror_tag = T("its mirror", 24, DIM).next_to(M.p(0.2, H_R), DOWN, buff=0.36)
        mirror_bg = BackgroundRectangle(mirror_tag, color=BG, fill_opacity=0.75, buff=0.06)
        mirror = VGroup(mirror_bg, mirror_tag)
        self.at("almost", FadeIn(rog), FadeIn(twin), run_time=0.25)
        self.play(rog.animate.move_to(M.p(0.8, H_R)), twin.animate.move_to(M.p(0.2, H_R)),
                  FadeIn(r_tag, shift=0.1 * LEFT), run_time=0.7, rate_func=rate_functions.ease_out_back)
        self.play(FadeIn(mirror, shift=0.1 * UP), run_time=0.3)
        self.at(30.87, Indicate(rog, color=BAD, scale_factor=1.3), Indicate(twin, color=BAD, scale_factor=1.3),
                run_time=0.6)   # "rogue"

        # {#moves}: a hypothetical reading, drawn under the ruler (clear of the caption row), slides ½ -> 0.8
        Y = dial.Y
        mk = dial.marker(0.5).rotate(PI).scale(1.6)          # points up at the ruler
        mk.move_to([dial.x_of(0.5), Y - 0.01 - mk.height / 2, 0]).set_z_index(12)
        m08 = N("0.8", 26, BAD).move_to([dial.x_of(0.8), Y - 0.42, 0]).set_z_index(12)
        drop = DashedLine(M.p(0.8, H_R) + DOWN * 0.24, [dial.x_of(0.8), Y, 0], color=BAD,
                          stroke_width=2.5, dash_length=0.1).set_z_index(11)
        riemann = VGroup(dial.pin, dial.pin_label)
        self.at("moves", FadeIn(mk, scale=0.5), riemann.animate.set_opacity(0.35), run_time=0.25)
        self.play(mk.animate.move_to([dial.x_of(0.8), mk.get_y(), 0]), Create(drop), run_time=0.55)
        self.play(FadeIn(m08, shift=0.05 * DOWN), run_time=0.3)

        # {#window}: the rogue business fades; the window pulses
        rogue_all = VGroup(rog, twin, r_tag, mirror, mk, m08, drop, bar_out, fills, bar_labs, bar_cap, ext, ext_fill,
                           lab100, even)
        self.at(self.t("window") + 0.2, FadeOut(rogue_all), riemann.animate.set_opacity(1.0), run_time=0.35)
        somewhere = VGroup(T("proven:", 24, INK), T("somewhere", 24, DIM), T("in here", 24, DIM)).arrange(DOWN, buff=0.08)
        # a DIM bracket over real parts ½..1 on the strip floor, its legs pointing down at the window's two ends
        by_b, by_tip = SY0 + 0.2, DIAL_TOP - 0.02
        xa, xb = dial.x_of(0.5) + 0.06, dial.x_of(1) - 0.06
        somewhere.move_to([(xa + xb) / 2, by_b + 0.18 + somewhere.height / 2 + 0.1, 0])
        sw_bg = BackgroundRectangle(somewhere, color=BG, fill_opacity=0.8, buff=0.1, corner_radius=0.08)
        leg = dict(buff=0, color=DIM, stroke_width=3, max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=20)
        sw_arrow = VGroup(Line([xa, by_b, 0], [xb, by_b, 0], color=DIM, stroke_width=3),
                          Arrow([xa, by_b, 0], [xa, by_tip, 0], **leg), Arrow([xb, by_b, 0], [xb, by_tip, 0], **leg)
                          ).set_z_index(11)
        sw = VGroup(sw_bg, somewhere, sw_arrow)
        glow = dial.window.copy().set_z_index(12)
        self.at(34.3, FadeIn(VGroup(sw_bg, somewhere), shift=0.1 * DOWN), Create(sw_arrow),
                glow.animate(rate_func=there_and_back).set_stroke(width=7).set_fill(opacity=0.55),
                run_time=0.9)
        self.remove(glow)
        self.at(35.2, Indicate(dial.window, color=ACCENT, scale_factor=1.06), run_time=0.8)   # "never narrowed"

        # {#below_one}: an enlarged view of the window's right end, 0.95 .. 1, with the 0.99 .. 1 sliver
        x99 = dial.x_of(0.99)
        t99 = Line([x99, Y - 0.24, 0], [x99, Y + 0.18, 0], color=INK, stroke_width=3).set_z_index(12)
        bx0, bx1, byb, byt = 2.85, 6.25, -2.35, -0.6
        box = RoundedRectangle(corner_radius=0.1, width=bx1 - bx0, height=byt - byb, stroke_color=DIM, stroke_width=1.5,
                               fill_color=BG, fill_opacity=1).move_to([(bx0 + bx1) / 2, (byb + byt) / 2, 0])
        ry = -1.55

        def xr(v):
            return 3.2 + (v - 0.95) / 0.05 * 2.6
        wr = xr(1) + 0.08
        win_fill = Rectangle(width=wr - (bx0 + 0.1), height=0.42, stroke_width=0, fill_color=ACCENT, fill_opacity=0.25
                             ).move_to([(bx0 + 0.1 + wr) / 2, ry, 0])
        win_edge = VMobject(stroke_color=ACCENT, stroke_width=2.5).set_points_as_corners(
            [[bx0 + 0.1, ry + 0.21, 0], [wr, ry + 0.21, 0], [wr, ry - 0.21, 0], [bx0 + 0.1, ry - 0.21, 0]])
        z_ruler = Line([bx0 + 0.1, ry, 0], [xr(1), ry, 0], color=NEUTRAL, stroke_width=3)
        z_ticks = VGroup(*[Line([xr(v), ry - 0.12, 0], [xr(v), ry + 0.12, 0], color=NEUTRAL, stroke_width=3) for v in (0.95, 1)])
        z_labs = VGroup(N("0.95", 24, INK).move_to([xr(0.95), ry - 0.4, 0]), N("1", 24, INK).move_to([xr(1), ry - 0.4, 0]))
        enl = T("enlarged", 24, DIM).next_to([bx0 + 0.1, byt, 0], UP, buff=0.12, aligned_edge=LEFT)
        lens = VGroup(Line([dial.x_of(0.95), DIAL_TOP - 0.06, 0], [bx0, byb, 0]),
                      Line([dial.x_of(1) + 0.08, DIAL_TOP - 0.06, 0], [bx1, byb, 0]),
                      Line([dial.x_of(0.95), DIAL_TOP - 0.06, 0], [dial.x_of(1) + 0.08, DIAL_TOP - 0.06, 0])
                      ).set_stroke(DIM, 1.5, opacity=0.7)
        zoom = VGroup(lens, box, win_fill, z_ruler, win_edge, z_ticks, z_labs, enl)
        z99 = Line([xr(0.99), ry - 0.27, 0], [xr(0.99), ry + 0.27, 0], color=INK, stroke_width=4)
        n99 = N("0.99", 24, INK).move_to([xr(0.99), ry - 0.4, 0])
        sx0, sx1, sy0, sy1 = xr(0.99), xr(1), ry - 0.21, ry + 0.21
        hatch = VGroup()
        for k in range(-6, 8):
            c = sx0 + k * 0.11                       # lines x - y = const, clipped to the sliver
            a = np.array([max(sx0, c), 0, 0]); a[1] = sy0 + (a[0] - c)
            b = np.array([min(sx1, c + (sy1 - sy0)), 0, 0]); b[1] = sy0 + (b[0] - c)
            if b[0] - a[0] > 0.02:
                hatch.add(Line(a, b, color=BAD, stroke_width=2))
        sliver = VGroup(Rectangle(width=sx1 - sx0, height=sy1 - sy0, stroke_width=0, fill_color=BAD, fill_opacity=0.22
                                  ).move_to([(sx0 + sx1) / 2, ry, 0]), hatch)
        ro_x = cross_mark(ORIGIN, size=0.09, width=5)
        ro = VGroup(T("ruled out?", 24, DIM), ro_x).arrange(RIGHT, buff=0.14)
        ro.move_to([0, byt - 0.3, 0]).align_to([bx1 - 0.15, 0, 0], RIGHT)
        self.at("below_one", FadeIn(zoom), run_time=0.6)
        self.at(38.85, Create(z99), FadeIn(n99), FadeIn(t99), run_time=0.4)                  # "point nine nine"
        self.at(39.3, FadeIn(sliver), FadeIn(ro[0], shift=0.1 * LEFT), GrowFromCenter(ro_x), run_time=0.6)

        # ============================================================ P4: Guth and Maynard
        p3_extra = VGroup(sw, zoom, z99, n99, t99, sliver, ro)
        gm = VGroup(T("Guth and Maynard", 26, INK), N("2024", 26, INK)).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        gm.move_to([0, 3.0, 0]).align_to([6.55, 0, 0], RIGHT)
        self.at("p4", FadeOut(p3_extra), FadeIn(gm, shift=0.1 * DOWN), run_time=0.7)

        def soft_zone(side, n=18, top=0.5):
            """Thin slices whose shading grows from nothing at ½ toward the strip's edge (side +1 right, -1 left)."""
            g = VGroup()
            for i in range(n):
                a, b = 0.5 + side * 0.5 * i / n, 0.5 + side * 0.5 * (i + 1) / n
                xa, xb = sorted((M.p(a, 0)[0], M.p(b, 0)[0]))
                g.add(Rectangle(width=xb - xa + 0.004, height=SY1 - SY0, stroke_width=0, fill_color=DIM,
                                fill_opacity=top * ((i + 0.5) / n) ** 1.6).move_to([(xa + xb) / 2, (SY0 + SY1) / 2, 0]))
            return g
        zr, zl = soft_zone(+1), soft_zone(-1)
        zr.set_z_index(-1), zl.set_z_index(-1)
        t34 = Line(M.p(0.75, M.hmax), M.p(0.75, M.hmax) + DOWN * 0.2, color=INK, stroke_width=2.5)
        q34 = N("¾", 26, DIM).next_to(t34, RIGHT, buff=0.1).shift(DOWN * 0.14)
        rb_room = T("room for rebels", 24, INK)
        rebels = VGroup(rb_room, T("illustration", 24, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rebels.next_to([SX1, 0.3, 0], RIGHT, buff=0.35)
        rb_less = T("less room for rebels", 24, INK).move_to(rb_room).align_to(rb_room, LEFT)
        mir4 = T("mirror", 24, DIM).move_to([0, 0.3, 0]).align_to([SX0 - 0.3, 0, 0], RIGHT)
        self.at("few", FadeIn(zr), FadeIn(zl), FadeIn(t34), FadeIn(q34), FadeIn(rebels, shift=0.1 * LEFT),
                FadeIn(mir4), run_time=0.7)
        self.at(45.9, zr.animate.fade(0.5), zl.animate.fade(0.5), Transform(rb_room, rb_less), run_time=1.4)
        ing = VGroup(T("beats Ingham's", 24, DIM), T("1940 bound", 24, DIM), T("(near real part ¾)", 24, DIM)
                     ).arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        ing.next_to(gm, DOWN, buff=0.15).align_to(gm, RIGHT)
        self.at("ingham", FadeIn(ing, shift=0.1 * DOWN), run_time=0.6)
        self.at(50.15, Indicate(q34, color=INK, scale_factor=1.3), run_time=0.8)     # "nineteen forty"

        # end: everything fades, the dial last
        self.at("p4_end", FadeOut(VGroup(sg3, gm, ing, zr, zl, t34, q34, rebels, mir4)), run_time=0.5)
        self.until("end", FadeOut(dial))

