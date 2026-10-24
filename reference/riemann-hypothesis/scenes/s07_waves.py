"""S07_Waves: Riemann's exact recipe. Staircase = sharpened curve + one wave per zero; a zero's height sets how fast
its wave wiggles, its position across the strip sets how big the swings grow (about x^position), and on the middle
line that is x^½ = √x: the dial's ½.

Data (all from topic.py, nothing typed from memory):
  staircase      staircase_points(100) (exact corners)
  sharpened R    R(x) on LIN_X, computed as base_lin() + 1/ln x - arctan(π/ln x)/π (base = R - 1/ln x + arctan/π)
  rebuilt curve  rebuild(10), rebuild(100) on LIN_X (includes the trivial-zero term; overshoots at risers are real)
  "all zeros"    the exact staircase sampled on LIN_X (value at a prime = the midpoint, where the series converges)
  waves          zero_wave(k) on LIN_X (P2 lanes, each with its own enlarged scale) and on LOG_X (P4, one common scale)
  funnel         envelope(0.5, γ1, LOG_X) = 2√x / (|ρ1| ln x)
Layouts: the dial at its home (standard S06-S08 state); the strip as INSET (P1-P2) then INSET_240 (P3 on, 100 zeros).
Every non-dial element stays above y = -2.6, except the inset's floor labels (drawn above the dial panel, clear of
its captions; the INSET floor is fixed at y -2.4).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------- linear graph (x 0..100, y 0..26)
GX0, GX1 = -6.0, 3.4
FULL = (GX0, GX1, -2.0, 2.75)          # full-height staircase graph
SMALL = (GX0, GX1, 0.5, 2.75)          # P2: graph shrinks upward, lanes below
LANES = [-2.1, -1.4, -0.7]             # lane centres, bottom-up: zero 1, 2, 3 (same order as the zeros in the strip)
LANE_H = 0.26                          # half-height of a lane

# ---------------------------------------------------------------- log graph (x 10..1e6)
LX0, LX1 = -6.0, 3.4
LAXIS_Y = -2.05                        # bottom axis
LYC = -0.2                             # wave centre line (full graph)
LS = 0.158                             # manim units per unit of wave value (one common scale)
HLANES = [(0.8, 0), (-1.2, 4)]         # (centre, zero index) for the height comparison: zero 1 and zero 5
HS = 0.088                             # common scale in the two height lanes


def gp(x, y, M):
    x0, x1, y0, y1 = M
    return np.column_stack([x0 + (x1 - x0) * np.asarray(x) / 100.0, y0 + (y1 - y0) * np.asarray(y) / 26.0,
                            np.zeros(len(np.atleast_1d(x)))])


def poly(points, color, width):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(points)
    return m


def lxs(x):
    return LX0 + (LX1 - LX0) * (np.log10(np.asarray(x, float)) - 1) / 5.0


def graph_parts(M):
    """Axes lines + tick labels of the linear graph for mapping M."""
    o = gp([0], [0], M)[0]
    xa = Line(o, gp([100], [0], M)[0], color=NEUTRAL, stroke_width=2.5)
    ya = Line(o, gp([0], [26], M)[0], color=NEUTRAL, stroke_width=2.5)
    ticks = VGroup(*[Line(gp([v], [0], M)[0] + DOWN * 0.07, gp([v], [0], M)[0] + UP * 0.07, color=NEUTRAL, stroke_width=2.5)
                     for v in (50, 100)],
                   *[Line(gp([0], [v], M)[0] + LEFT * 0.07, gp([0], [v], M)[0] + RIGHT * 0.07, color=NEUTRAL, stroke_width=2.5)
                     for v in (10, 20)])
    xl = VGroup(*[N(str(v), 24, DIM).next_to(gp([v], [0], M)[0], DOWN, buff=0.13) for v in (50, 100)])
    yl = VGroup(*[N(str(v), 24, DIM).next_to(gp([0], [v], M)[0], LEFT, buff=0.13) for v in (10, 20)])
    return VGroup(xa, ya, ticks), xl, yl


def sup(base, exp, color, bs=32, es=24, font_base=N, font_exp=N):
    b = font_base(base, bs, color)
    e = font_exp(exp, es, color)
    e.next_to(b, RIGHT, buff=0.05).align_to(b, UP).shift(UP * 0.14)
    return VGroup(b, e)


class S07_Waves(TimedScene):
    def construct(self):
        # ============================================================ data
        X = LIN_X
        base = base_lin()
        lx = np.log(X)
        Rv = base + 1 / lx - np.arctan(np.pi / lx) / np.pi            # R(x), sharpened curve
        r10, r100 = rebuild(10), rebuild(100)
        pi_x = prime_pi(X).astype(float)
        on_prime = np.isin(np.round(X, 6), primes_upto(100).astype(float))
        exact = pi_x - 0.5 * on_prime                                   # midpoint at each jump
        stair_pts = staircase_points(100)

        # ============================================================ P1: dial + inset, staircase, sharpened curve
        dial = ErrorDial()
        strip = strip_group(INSET, 10)
        strip.floor_labels.set_z_index(11)
        top_tick = VGroup(Line(INSET.p(0, 50) + LEFT * 0.08, INSET.p(0, 50), color=DIM, stroke_width=2),
                          N("50", 22, DIM).next_to(INSET.p(0, 50) + LEFT * 0.08, LEFT, buff=0.08))

        self.until("p1s1", FadeIn(dial), FadeIn(strip), FadeIn(top_tick), run_time=0.3) if self.left("p1s1") > 0.25 else None
        self.play(FadeIn(dial), FadeIn(strip), FadeIn(top_tick), run_time=0.8) if dial not in self.mobjects else None

        axes, xl, yl = graph_parts(FULL)
        stair = poly(gp(stair_pts[:, 0], stair_pts[:, 1], FULL), PRIME_COLOR, 5)
        curve = poly(gp(X, Rv, FULL), CURVE_COLOR, 3.5).set_z_index(2)

        cap = VGroup(T("Riemann 1859:", 26, DIM), T("staircase", 26, PRIME_COLOR), T("=", 26, DIM),
                     T("sharpened curve", 26, CURVE_COLOR), T("+", 26, DIM), T("one wave per zero", 26, INK)
                     ).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        cap.to_corner(UL, buff=0.35).shift(RIGHT * 0.1)
        cap2 = T("fully proved by von Mangoldt, 1895", 24, DIM).next_to(cap, DOWN, buff=0.14, aligned_edge=LEFT)

        self.at("recipe", FadeIn(axes), FadeIn(xl), FadeIn(yl), FadeIn(cap[0]), FadeIn(cap[1]), run_time=0.6)
        self.until("p1s1_end", Create(stair, rate_func=linear), FadeIn(cap2, shift=UP * 0.1))
        self.at("smooth", FadeIn(cap[2]), FadeIn(cap[3]), Create(curve), run_time=1.6)

        # ============================================================ P2: every zero adds one wave
        self.at("p2", LaggedStart(*[Indicate(d, color=ACCENT, scale_factor=1.8) for d in strip.dots], lag_ratio=0.12),
                run_time=1.2)
        axes_s, xl_s, yl_s = graph_parts(SMALL)
        lane_lines = VGroup(*[Line(gp([2], [0], FULL)[0] * [1, 0, 0] + [0, c, 0], gp([100], [0], FULL)[0] * [1, 0, 0] + [0, c, 0],
                                   color=FAINT, stroke_width=2) for c in LANES])
        enl = T("waves enlarged", 24, DIM).move_to([0, 0.14, 0]).align_to([GX0, 0, 0], LEFT)
        self.at("wave", Transform(axes, axes_s), Transform(yl, yl_s), FadeOut(xl),
                Transform(stair, poly(gp(stair_pts[:, 0], stair_pts[:, 1], SMALL), PRIME_COLOR, 5)),
                Transform(curve, poly(gp(X, Rv, SMALL), CURVE_COLOR, 3.5)),
                FadeIn(cap[4]), FadeIn(cap[5]), run_time=1.0)
        self.play(FadeIn(lane_lines), FadeIn(enl), run_time=0.5)

        waves, rings, threads = VGroup(), VGroup(), VGroup()
        for k, mark in ((1, "first"), (2, "second"), (3, "third")):
            w = zero_wave(k)
            c = WAVE_COLORS[k - 1]
            ys = LANES[k - 1] + w * (LANE_H / np.abs(w).max())
            wx = gp(X, np.zeros_like(X), FULL)[:, 0]
            wave = poly(np.column_stack([wx, ys, np.zeros_like(ys)]), c, 2.5)
            dot = strip.dots[k - 1]
            rg = Circle(radius=0.13, color=c, stroke_width=3).move_to(dot)
            end = np.array([GX1 + 0.08, LANES[k - 1], 0])
            th = Line(rg.get_left(), end, color=c, stroke_width=1.6, stroke_opacity=0.75)
            waves.add(wave), rings.add(rg), threads.add(th)
            rt = 1.1 if k < 3 else 1.0
            self.at(mark, AnimationGroup(FadeIn(rg, scale=2.2), dot.animate.set_fill(c),
                                         Create(th), Create(wave, rate_func=linear), lag_ratio=0.12), run_time=rt)

        # ============================================================ P3: 10 zeros, 100 zeros, all
        axes_f, xl_f, yl_f = graph_parts(FULL)
        counter = VGroup(T("zeros:", 28, DIM), N("10", 32, ACCENT)).arrange(RIGHT, buff=0.15)
        counter.move_to([0, 2.2, 0]).align_to([GX0 + 0.35, 0, 0], LEFT)
        self.at("p3", Transform(axes, axes_f), Transform(yl, yl_f), FadeIn(xl_f),
                Transform(stair, poly(gp(stair_pts[:, 0], stair_pts[:, 1], FULL), PRIME_COLOR, 5)),
                Transform(curve, poly(gp(X, Rv, FULL), CURVE_COLOR, 3.5)),
                *[w.animate.shift(UP * 1.2).set_stroke(opacity=0.5) for w in waves],
                FadeOut(lane_lines), FadeOut(enl), FadeOut(threads), FadeOut(rings),
                *[d.animate.set_fill(INK) for d in strip.dots[:3]],
                FadeIn(counter, shift=DOWN * 0.1), run_time=1.0)
        target10 = poly(gp(X, r10, FULL), CURVE_COLOR, 3.5)
        self.play(Transform(curve, target10),
                  *[Transform(w, target10.copy().set_stroke(WAVE_COLORS[i], opacity=0)) for i, w in enumerate(waves)],
                  LaggedStart(*[Indicate(d, color=ACCENT, scale_factor=1.8) for d in strip.dots], lag_ratio=0.15),
                  run_time=min(1.6, self.left("p3s1_end") - 1.2))
        self.remove(waves)

        # {#hundred}: inset -> 0..240 with 100 zeros; curve -> rebuild(100)
        strip240 = strip_group(INSET_240, 100)
        new_top = VGroup(Line(INSET_240.p(0, 240) + LEFT * 0.08, INSET_240.p(0, 240), color=DIM, stroke_width=2),
                         N("240", 22, DIM).next_to(INSET_240.p(0, 240) + LEFT * 0.08, LEFT, buff=0.08))
        c100 = N("100", 32, ACCENT).move_to(counter[1]).align_to(counter[1], LEFT)
        self.at("hundred", *[Transform(strip.dots[i], strip240.dots[i]) for i in range(10)],
                LaggedStart(*[FadeIn(d, scale=0.5) for d in strip240.dots[10:]], lag_ratio=0.02),
                Transform(top_tick, new_top), Transform(counter[1], c100), run_time=0.9)
        dots = VGroup(*strip.dots, *strip240.dots[10:])
        self.play(Transform(curve, poly(gp(X, r100, FULL), CURVE_COLOR, 3.5)), run_time=1.2)

        # {#exact}: all zeros -> the staircase itself
        call = T("all", 30, ACCENT).move_to(counter[1]).align_to(counter[1], LEFT)
        limit = T("in the limit", 24, DIM).next_to(counter, RIGHT, buff=0.3)
        self.at("exact", Transform(counter[1], call), FadeIn(limit, shift=LEFT * 0.1),
                Transform(curve, poly(gp(X, exact, FULL), CURVE_COLOR, 3.5)), run_time=0.8)
        halo = VGroup(stair.copy(), curve.copy()).set_stroke(ACCENT, width=14, opacity=0.35).set_z_index(-1)
        self.play(FadeIn(halo), run_time=0.5)
        self.play(FadeOut(halo), run_time=0.7)

        # ============================================================ P4: height -> wiggle rate, position -> size
        G = VGroup(axes, stair, curve)
        self.at("p4", G.animate.scale(0.25).to_corner(UL, buff=0.3).set_stroke(width=2),
                FadeOut(xl), FadeOut(xl_f), FadeOut(yl), FadeOut(cap), FadeOut(cap2), FadeOut(counter), FadeOut(limit),
                run_time=0.9)

        laxis = Line([LX0, LAXIS_Y, 0], [LX1, LAXIS_Y, 0], color=NEUTRAL, stroke_width=2.5)
        dec = ["10", "100", "1,000", "10,000", "100,000", "1,000,000"]
        lticks = VGroup(*[Line([lxs(10 ** (i + 1)), LAXIS_Y - 0.07, 0], [lxs(10 ** (i + 1)), LAXIS_Y + 0.07, 0],
                               color=NEUTRAL, stroke_width=2.5) for i in range(6)])
        llabels = VGroup(*[N(s, 24, DIM).next_to([lxs(10 ** (i + 1)), LAXIS_Y, 0], DOWN, buff=0.13) for i, s in enumerate(dec)])
        logtag = T("log scale", 24, DIM).next_to([LX0, LAXIS_Y, 0], UR, buff=0.12)
        hl_lines = VGroup(*[Line([LX0, c, 0], [LX1, c, 0], color=FAINT, stroke_width=2) for c, _ in HLANES])
        self.play(Create(laxis), FadeIn(lticks), FadeIn(llabels), FadeIn(logtag), FadeIn(hl_lines),
                  run_time=min(1.0, self.left("height") - 0.05))

        LXS = lxs(LOG_X)
        lw = {}
        for c, k in HLANES:
            w = zero_wave(k + 1, LOG_X)
            lw[k] = (w, poly(np.column_stack([LXS, c + HS * w, np.zeros_like(w)]), WAVE_COLORS[k], 2.5))
        hlab = VGroup(*[T(f"height {ZEROS[k]:.2f}", 26, WAVE_COLORS[k]).move_to([0, c + 0.42, 0]).align_to([LX0, 0, 0], LEFT)
                        for c, k in HLANES])
        hrings = VGroup(*[Circle(radius=0.1, color=WAVE_COLORS[k], stroke_width=3).move_to(dots[k]) for _, k in HLANES])
        self.at("height", Create(lw[0][1], rate_func=linear), Create(lw[4][1], rate_func=linear),
                FadeIn(hlab), FadeIn(hrings, scale=2.2), *[dots[k].animate.set_fill(WAVE_COLORS[k]) for _, k in HLANES],
                run_time=1.3)

        # {#across}: wave 5 goes, wave 1 fills the graph; position across the strip
        w1 = lw[0][0]
        wave1 = lw[0][1]
        wave1_full = poly(np.column_stack([LXS, LYC + LS * w1, np.zeros_like(w1)]), WAVE_COLORS[0], 2.5)
        cline = Line([LX0, LYC, 0], [LX1, LYC, 0], color=FAINT, stroke_width=2)
        y1 = INSET_240.p(0, ZEROS[0])[1]
        parrow = DoubleArrow(INSET_240.p(0, ZEROS[0]), INSET_240.p(0.5, ZEROS[0]) + LEFT * 0.07, buff=0,
                             color=INK, stroke_width=3, tip_length=0.13, max_tip_length_to_length_ratio=0.2)
        plabel = T("position", 22, INK).next_to(parrow, UP, buff=0.1)
        self.at("across", FadeOut(lw[4][1]), FadeOut(hlab), FadeOut(hrings[1]), dots[4].animate.set_fill(INK),
                Transform(wave1, wave1_full), Transform(hl_lines, VGroup(cline, cline.copy())), run_time=1.0)
        self.play(GrowFromCenter(parrow), FadeIn(plabel, shift=UP * 0.1), run_time=0.6)

        env = envelope(0.5, ZEROS[0], LOG_X)
        up = DashedVMobject(poly(np.column_stack([LXS, LYC + LS * env, np.zeros_like(env)]), DIM, 2.5), num_dashes=70)
        dn = DashedVMobject(poly(np.column_stack([LXS, LYC - LS * env, np.zeros_like(env)]), DIM, 2.5), num_dashes=70)
        funnel = VGroup(up, dn)
        self.until("p4s2_end", Wait(0.01)) if False else None
        self.at(32.0, Create(up), Create(dn), run_time=1.5)

        size_lab = VGroup(T("size ≈", 28, DIM), sup("x", "position", DIM, bs=30, es=24, font_exp=T)).arrange(
            RIGHT, buff=0.14, aligned_edge=DOWN)
        size_lab.move_to([-2.4, 1.05, 0])
        self.at("power", FadeIn(size_lab, shift=UP * 0.1), run_time=0.7)
        self.at(36.3, Indicate(plabel, color=ACCENT, scale_factor=1.2), Indicate(parrow, color=ACCENT, scale_factor=1.1),
                run_time=0.8)

        # ============================================================ P5: on the line: x^½ = √x = the dial's ½
        glow = strip240.line.copy().set_stroke(ACCENT, width=12, opacity=0.4)
        self.at("p5", FadeIn(glow), run_time=0.5)
        self.play(FadeOut(glow), run_time=0.6)

        half_lab = N("½", 30, ACCENT).move_to(plabel)
        xhalf = sup("x", "½", ACCENT, bs=34, es=26)
        tip = np.array([LX1, LYC + LS * env[-1], 0])
        xhalf.next_to(tip, UL, buff=0.12)
        self.at("half", Indicate(strip.floor_labels[1], color=ACCENT, scale_factor=1.8),
                Transform(plabel, half_lab), parrow.animate.set_color(ACCENT),
                funnel.animate.set_color(ACCENT), FadeIn(xhalf, shift=UP * 0.1), run_time=0.9)
        root = N("√x", 34, ACCENT).move_to(xhalf).align_to(xhalf, DOWN)
        self.at("root", ReplacementTransform(xhalf, root), run_time=0.8)

        # {#digits}: the inset's ½ drops to the dial's ½
        fl = strip.floor_labels[1]
        yb = -2.64
        drop = DashedVMobject(VMobject(stroke_color=ACCENT, stroke_width=2.5).set_points_as_corners(
            [fl.get_bottom() + DOWN * 0.02, [fl.get_x(), yb, 0], [dial.x_of(0.5), yb, 0], [dial.x_of(0.5), dial.Y + 0.13, 0]]),
            num_dashes=48).set_z_index(12)
        self.at("digits", Create(drop), run_time=1.0)
        self.at(46.05, Indicate(dial.labels[1], color=ACCENT, scale_factor=1.6),
                Indicate(VGroup(dial.pin, dial.pin_label), color=ACCENT, scale_factor=1.25), run_time=0.8)
        self.at(46.95, Rotate(dial.coin, TAU, axis=UP, about_point=dial.coin.get_center()), run_time=0.8)

        # ============================================================ end: fade out, the dial last
        rest = [m for m in self.mobjects if m is not dial]
        self.at("p5_end", *[FadeOut(m) for m in rest], run_time=0.5)
        self.until("end", FadeOut(dial))
