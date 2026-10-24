"""S08_OneHalf: why one half is the best the primes can do.

Layout (dial on screen all scene, camera still):
  left   the S07 log-scale wave graph (x = 10 .. 1,000,000 across x -5.7 .. 2.6), baseline y -0.1,
         a y-axis whose ticks (10, 500) slide when the vertical scale changes, the staircase thumbnail
         in the graph's empty upper-left corner;
  right  the INSET strip (first ten zeros); p5 moves it to the DIAL_ALIGNED layout above the dial.

  p1  a zero slides off the line to 0.8 (its mirror twin to 0.2, both hollow BAD rings, 'hypothetical'),
      the dial's BAD marker follows; the rogue wave x^0.8 draws and runs off the top of the chart.
  p2  the vertical scale zooms out (geometric) until the rogue wave fits; the pink wave from the line
      flattens; an ACCENT bracket at a million: '≈ 63 ×'; the thumbnail staircase turns lumpy (illustration).
  p3  the rings swap sides; the twin lands at 0.8 (the marker never moves); the tiny x^0.2 wave draws:
      the louder one wins.
  p4  scale back; the rings converge on ½ while their envelopes close in on the √x funnel; they merge into
      the real zero; a sweep line reads the rightmost zero (½), a hypothetical 0.3/0.7 pair shows the
      reading is always the right-hand twin; check 'best possible'; the pin glows.
  p5  the graph fades, the strip moves above the dial; 1896: right edge lights; the S02 table echo
      (percentages ✓, gap ?); the middle line glows; the coin flips; everything fades, the dial last.

All graph curves are redrawn every frame from a few ValueTrackers (scale, envelope power, per-curve
draw fraction / opacity / width), so rescaling and converging are exact, not morphs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: F401,F403,E402
from topic import *  # noqa: F401,F403,E402

config.disable_caching = True   # trackers + updaters: never reuse cached partial movies

G1 = float(ZEROS[0])
# ---------------------------------------------------------------- log graph geometry
# Exactly S07's final log graph (S07: LX0, LX1 = -6.0, 2.8; LAXIS_Y -1.95; LYC -0.2; LS 0.158), so the cut is seamless.
GX0, GX1 = -6.0, 2.8            # log10 x = 1 .. 6
Y0, H = -0.2, 1.65              # baseline and the largest |offset| the chart shows
YB = -1.95                      # x-axis line
EX = np.logspace(1, 6, 260)     # envelope grid
LX, LEX = np.log10(LOG_X), np.log10(EX)
S1 = 0.158                                        # S07's common wave scale: the √x funnel reaches 1.62
S2 = (H - 0.1) / float(envelope(0.8, G1, [1e6])[0])   # the x^0.8 funnel fills the chart
W1 = zero_wave(1, LOG_X)
W8 = rogue_wave(0.8, G1, LOG_X)
W2 = rogue_wave(0.2, G1, LOG_X)
RATIO = float(envelope(0.8, G1, [1e6])[0] / envelope(0.5, G1, [1e6])[0])
assert 62.5 < RATIO < 63.5, RATIO


def gx(lx):
    return GX0 + (np.asarray(lx) - 1) * (GX1 - GX0) / 5


def scale_of(u):
    return S1 * (S2 / S1) ** u


def cut_log(beta, s, frac):
    """log10 x where the drawn curve stops: its draw fraction, or where its funnel leaves the chart."""
    lim = 1 + 5 * frac
    e = envelope(beta, G1, EX) * s
    idx = np.nonzero(e > H)[0]
    if idx.size:
        i = idx[0]
        c = 1.0 if i == 0 else LEX[i - 1] + (H - e[i - 1]) / (e[i] - e[i - 1]) * (LEX[i] - LEX[i - 1])
        lim = min(lim, c)
    return lim


def poly(lx, y, lim):
    keep = lx < lim
    L, Y = lx[keep], y[keep]
    if lim < lx[-1] and L.size:
        L = np.append(L, lim)
        Y = np.append(Y, np.interp(lim, lx, y))
    if L.size < 2:
        return None
    return np.column_stack([gx(L), Y0 + np.clip(Y, -H, H), np.zeros(L.size)])


def dashed(paths, color, width, opacity, dash=0.1, gap=0.07):
    """One VMobject holding dashes along each polyline in `paths` (dash pattern anchored at the left end)."""
    vm = VMobject()
    for P in paths:
        if P is None:
            continue
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
        a = 0.0
        while a < s[-1] - 1e-3:
            b = min(a + dash, s[-1])
            inner = P[(s > a) & (s < b)]
            pa = np.array([np.interp(a, s, P[:, k]) for k in range(3)])
            pb = np.array([np.interp(b, s, P[:, k]) for k in range(3)])
            pts = np.vstack([pa, inner, pb])
            vm.start_new_path(pts[0])
            vm.add_points_as_corners(pts[1:])
            a += dash + gap
    vm.set_stroke(color, width=width, opacity=opacity)
    vm.set_fill(opacity=0)
    return vm


def solid(P, color, width, opacity):
    vm = VMobject()
    if P is not None:
        vm.set_points_as_corners(P)
    return vm.set_stroke(color, width=width, opacity=opacity).set_fill(opacity=0)


def pow_label(exp, size=30, color=INK):
    b = N("x", size, color, slant=ITALIC)
    e = N(exp, int(size * 0.62), color).next_to(b, UR, buff=0.02).shift(DOWN * 0.1)
    return VGroup(b, e)


def dashed_ring(center, r=0.13, color=BAD):
    return DashedVMobject(Circle(radius=r, color=color, stroke_width=3), num_dashes=10).move_to(center)


def tag_box(text_mob, opacity=0.9):
    box = BackgroundRectangle(text_mob, color=BG, fill_opacity=opacity, buff=0.06)
    return VGroup(box, text_mob)


def halo(m, color=ACCENT):
    return VGroup(*[m.copy().set_fill(opacity=0).set_stroke(color, width=w, opacity=o)
                    for w, o in ((20, 0.08), (12, 0.16), (6, 0.35))])


# ---------------------------------------------------------------- thumbnail (staircase 0..100)
def _s07_thumb_box():
    """S07 shrinks its full staircase graph (x 0..100 -> -6..3.4, y 0..26 -> -2..2.75) by 0.25 into the top-left
    corner (to_corner(UL, buff=0.5)); return where its axes' corners land, so S08 opens on the same thumbnail."""
    o, xe, ye = np.array([-6.0, -2.0, 0]), np.array([3.4, -2.0, 0]), np.array([-6.0, 2.75, 0])
    ax = VGroup(Line(o, xe), Line(o, ye),
                *[Line(o + [9.4 * v / 100, 0, 0] + DOWN * 0.07, o + [9.4 * v / 100, 0, 0] + UP * 0.07) for v in (50, 100)],
                *[Line(o + [0, 4.75 * v / 26, 0] + LEFT * 0.07, o + [0, 4.75 * v / 26, 0] + RIGHT * 0.07) for v in (10, 20)])
    ax.scale(0.25).to_corner(UL, buff=0.5)
    return ax[0].get_start()[0], ax[0].get_end()[0], ax[0].get_start()[1], ax[1].get_end()[1]


TX0, TX1, TY0, TY1 = _s07_thumb_box()


def thumb_axes():
    """S07's thumbnail axes (with its small ticks at x 50, 100 and y 10, 20), NEUTRAL width 2."""
    o = tpt(0, 0)
    return VGroup(Line(o, tpt(100, 0)), Line(o, tpt(0, 26)),
                  *[Line(tpt(v, 0) + DOWN * 0.0175, tpt(v, 0) + UP * 0.0175) for v in (50, 100)],
                  *[Line(tpt(0, v) + LEFT * 0.0175, tpt(0, v) + RIGHT * 0.0175) for v in (10, 20)]
                  ).set_stroke(NEUTRAL, 2, opacity=1)


def tpt(x, y):
    return np.array([TX0 + (TX1 - TX0) * x / 100, TY0 + (TY1 - TY0) * y / 26, 0.0])


def corners(pts):
    return VMobject().set_points_as_corners([tpt(x, y) for x, y in pts])


def lumpy_points(k=4.0):
    """Illustration: primes placed where R(x) + k·(rogue x^0.8 wave) passes each whole number (running max)."""
    xs = np.linspace(2, 100, 400)
    f = np.maximum.accumulate(R(xs) + k * rogue_wave(0.8, G1, xs))
    pts, c = [(0.0, 0.0)], 0
    for x, v in zip(xs, f):
        while v >= c + 1 and c < 26:
            pts += [(x, c), (x, c + 1)]
            c += 1
    pts.append((100.0, c))
    return pts


class S08_OneHalf(TimedScene):
    def construct(self):
        M = INSET
        # ------------------------------------------------ trackers
        u = ValueTracker(0.0)          # 0: √x scale, 1: x^0.8 scale (geometric in between)
        eb = ValueTracker(0.8)         # power of the louder funnel (the quieter one is 1 - eb)
        beta = ValueTracker(0.5)       # real part of the slid zero (its twin sits at 1 - beta)
        mk = ValueTracker(0.5)         # dial marker reading
        lab_o = ValueTracker(0.0)      # ring value labels
        tr = {k: ValueTracker(v) for k, v in dict(
            pink_w=1.0, pink_o=1.0, r8_f=0.0, r8_o=1.0, r8_w=1.0, r2_f=0.0, r2_o=0.45,
            e8_f=0.0, e8_o=0.9, e2_f=0.0, e2_o=0.45, pe_o=0.8).items()}

        def v(k):
            return tr[k].get_value()

        def sc():
            return scale_of(u.get_value())

        # ------------------------------------------------ static graph frame
        xaxis = Line([GX0, YB, 0], [GX1 + 0.1, YB, 0], color=NEUTRAL, stroke_width=2.5)
        yaxis = Line([GX0, YB, 0], [GX0, Y0 + H + 0.05, 0], color=NEUTRAL, stroke_width=2.5)
        base = Line([GX0, Y0, 0], [GX1, Y0, 0], color=FAINT, stroke_width=2)
        zero_lab = N("0", 24, DIM).next_to([GX0, Y0, 0], LEFT, buff=0.14)
        xticks, xlabs = VGroup(), VGroup()
        for d, txt in enumerate(["10", "100", "1,000", "10,000", "100,000", "1,000,000"]):
            X = float(gx(d + 1))
            xticks.add(Line([X, YB - 0.08, 0], [X, YB + 0.08, 0], color=NEUTRAL, stroke_width=2))
            xlabs.add(N(txt, 24, DIM).next_to([X, YB, 0], DOWN, buff=0.12))
        log_tag = T("log scale", 24, DIM).move_to([1.75, 2.45, 0])
        frame = VGroup(xaxis, yaxis, base, zero_lab, xticks, xlabs, log_tag)

        # y ticks that slide with the scale
        yt = {}
        for val in (10, 500):
            mark = VGroup(Line([GX0 - 0.08, 0, 0], [GX0 + 0.08, 0, 0], color=NEUTRAL, stroke_width=2),
                          N(str(val), 24, DIM))
            yt[val] = mark

            def upd(m, val=val):
                y = val * sc()
                a = float(np.clip((H + 0.08 - y) / 0.15, 0, 1) * np.clip((y - 0.25) / 0.3, 0, 1))
                m[0].move_to([GX0, Y0 + y, 0])
                m[1].next_to(m[0], LEFT, buff=0.08)
                m.set_opacity(a * yo.get_value())
            mark.add_updater(upd)
            upd(mark)

        # ------------------------------------------------ dynamic curves
        def pink():
            s = sc()
            return solid(poly(LX, W1 * s, 7), PINK_P, 3 * v("pink_w"), v("pink_o"))

        def pink_env():
            e = envelope(0.5, G1, EX) * sc()
            return dashed([poly(LEX, e, 7), poly(LEX, -e, 7)], DIM, 2, v("pe_o"))

        def r8():
            s = sc()
            return solid(poly(LX, W8 * s, cut_log(0.8, s, v("r8_f"))), BAD, 3 * v("r8_w"), v("r8_o"))

        def r2():
            s = sc()
            return solid(poly(LX, W2 * s, 1 + 5 * v("r2_f")), BAD, 3, v("r2_o"))

        def env(b, fk, ok):
            s = sc()
            lim = cut_log(b, s, v(fk))
            e = envelope(b, G1, EX) * s
            return dashed([poly(LEX, e, lim), poly(LEX, -e, lim)], BAD, 2.5, v(ok))

        c_pink = always_redraw(pink)
        c_pe = always_redraw(pink_env)
        c_r8 = always_redraw(r8)
        c_r2 = always_redraw(r2)
        c_e8 = always_redraw(lambda: env(eb.get_value(), "e8_f", "e8_o"))
        c_e2 = always_redraw(lambda: env(1 - eb.get_value(), "e2_f", "e2_o"))
        dyn = [c_pe, c_e2, c_r2, c_pink, c_e8, c_r8]

        def env_end(b):
            s = sc()
            lim = cut_log(b, s, 1.0)
            y = min(float(envelope(b, G1, [10 ** lim])[0]) * s, H)
            return np.array([float(gx(lim)), Y0 + y, 0.0])

        lab_sqrt = N("√x", 30, ACCENT)
        lab_sqrt.add_updater(lambda m: m.next_to(env_end(0.5), RIGHT, buff=0.14))
        lab8 = pow_label("0.8", 30, BAD)
        lab8.add_updater(lambda m: m.move_to(env_end(0.8) + np.array([0.42, 0.2, 0])))
        lab2 = pow_label("0.2", 30, BAD).set_opacity(0.6).move_to([3.05, Y0 - 0.32, 0])

        # ------------------------------------------------ thumbnail
        tframe = RoundedRectangle(corner_radius=0.1, width=TX1 - TX0 + 0.5, height=TY1 - TY0 + 0.45,
                                  stroke_color=FAINT, stroke_width=2, fill_color=BG, fill_opacity=1
                                  ).move_to([(TX0 + TX1) / 2 + 0.02, (TY0 + TY1) / 2 + 0.05, 0])
        taxes = VGroup(Line(tpt(0, 0), tpt(100, 0), color=NEUTRAL, stroke_width=2),
                       Line(tpt(0, 0), tpt(0, 26), color=NEUTRAL, stroke_width=2))
        t_stair = corners(staircase_points(100)).set_stroke(PRIME_COLOR, 2.5)
        t_curve = VMobject().set_points_as_corners([tpt(x, y) for x, y in zip(LIN_X, rebuild(100))]
                                                   ).set_stroke(CURVE_COLOR, 2)
        thumb = VGroup(tframe, taxes, t_stair, t_curve)
        ghost = t_stair.copy().set_stroke(PRIME_COLOR, 2, opacity=0.3)
        lumpy = corners(lumpy_points()).set_stroke(BAD, 3)
        ill_tag = T("illustration", 24, DIM).next_to(tpt(0, 26), RIGHT, buff=0.12).shift(DOWN * 0.05)

        # ------------------------------------------------ strip + dial
        strip = strip_group(M, 10)
        strip.floor_labels.set_z_index(11)
        dot1 = strip.dots[0]
        dial = ErrorDial()
        marker = dial.marker(0.5)
        marker.add_updater(lambda m: m.set_x(dial.x_of(mk.get_value())))

        ring_a = dashed_ring(M.p(0.5, G1))      # the slid zero
        ring_b = dashed_ring(M.p(0.5, G1))      # its mirror twin
        ring_a.add_updater(lambda m: m.move_to(M.p(beta.get_value(), G1)))
        ring_b.add_updater(lambda m: m.move_to(M.p(1 - beta.get_value(), G1)))

        def ring_label(ring, val):
            return always_redraw(lambda: N(f"{val():.1f}", 24, INK).set_opacity(lab_o.get_value())
                                 .next_to(ring, UP, buff=0.1))
        rl_a = ring_label(ring_a, lambda: beta.get_value())
        rl_b = ring_label(ring_b, lambda: 1 - beta.get_value())
        hypo = tag_box(T("hypothetical", 24, DIM)).move_to(M.p(0.5, 5.0))

        # ================================================= P1
        snaps = [d.copy().clear_updaters() for d in dyn] + [lab_sqrt.copy().clear_updaters()]
        yt_snap = yt[10].copy().clear_updaters()
        self.until(0.9, FadeIn(VGroup(dial, strip, frame, thumb, yt_snap, *snaps)))
        self.remove(*snaps, yt_snap)
        self.add(*dyn, lab_sqrt, yt[10], yt[500])
        self.at(1.15, Indicate(dot1, scale_factor=1.9, color=ACCENT), run_time=0.65)

        self.at("rogue", FadeIn(VGroup(ring_a, ring_b)), FadeIn(marker), FadeIn(hypo),
                dot1.animate.set_fill(opacity=0.12).set_stroke(opacity=0.12, background=True), run_time=0.4)
        self.add(rl_a, rl_b)
        self.until(4.75, beta.animate.set_value(0.8), mk.animate.set_value(0.8),
                   lab_o.animate(rate_func=lambda t: smooth(np.clip((t - 0.35) / 0.4, 0, 1))).set_value(1.0))

        self.at("faster", tr["r8_f"].animate.set_value(1.0), tr["e8_f"].animate.set_value(1.0),
                run_time=1.2, rate_func=linear)
        lab8_snap = lab8.copy()
        self.play(FadeIn(lab8), run_time=0.5)

        # ================================================= P2
        self.at(9.75, Indicate(xlabs[5], color=ACCENT, scale_factor=1.15), run_time=0.7)
        self.at(10.45, u.animate.set_value(1.0), run_time=1.3)
        s2 = scale_of(1.0)
        yp = Y0 + float(envelope(0.5, G1, [1e6])[0]) * s2
        yr = Y0 + float(envelope(0.8, G1, [1e6])[0]) * s2
        bx = GX1 + 0.14
        bracket = VGroup(Line([bx, yp, 0], [bx, yr, 0], color=ACCENT, stroke_width=3),
                         Line([bx - 0.08, yp, 0], [bx, yp, 0], color=ACCENT, stroke_width=3),
                         Line([bx - 0.08, yr, 0], [bx, yr, 0], color=ACCENT, stroke_width=3))
        lab63 = N("≈ 63 ×", 30, ACCENT).next_to(bracket, RIGHT, buff=0.14).set_y((yp + yr) / 2)
        self.play(Create(bracket), FadeIn(lab63, shift=LEFT * 0.1), run_time=0.6)
        self.at(12.85, tr["pink_w"].animate(rate_func=there_and_back).set_value(2.6),
                Indicate(lab_sqrt, color=PINK_P), run_time=0.8)

        self.at("lumpy", FadeIn(ghost), Transform(t_stair, lumpy), FadeOut(t_curve), FadeIn(ill_tag), run_time=1.1)
        tint = Polygon(*([tpt(x, y) for x, y in lumpy_points()] + [tpt(100, 0)]), stroke_width=0,
                       fill_color=BAD, fill_opacity=0.35)
        self.play(FadeIn(tint, rate_func=there_and_back), run_time=0.8)
        self.remove(tint)

        # ================================================= P3
        self.at("p3", beta.animate.set_value(0.2),
                FadeOut(VGroup(bracket, lab63), rate_func=lambda t: smooth(min(1.0, t * 4))),
                tr["pink_o"].animate(rate_func=lambda t: smooth(min(1.0, t * 4))).set_value(0.35),
                run_time=2.6)
        self.play(Indicate(ring_b, color=BAD, scale_factor=1.6), Indicate(marker, color=BAD, scale_factor=1.6),
                  run_time=0.7)

        self.at("louder", tr["r2_f"].animate.set_value(1.0), tr["e2_f"].animate.set_value(1.0),
                FadeIn(lab2), run_time=0.9, rate_func=linear)
        louder = T("the louder one wins", 24, DIM).move_to([-0.3, 1.45, 0])
        self.at(23.35, tr["r8_w"].animate(rate_func=there_and_back).set_value(2.3), FadeIn(louder), run_time=0.9)

        # ================================================= P4
        self.at("p4", u.animate.set_value(0.0), tr["pink_o"].animate.set_value(1.0),
                FadeOut(VGroup(louder, lab2)), FadeOut(lab8), run_time=1.1)
        early = lambda t: smooth(min(1.0, t * 3))  # noqa: E731
        self.at("equal", beta.animate.set_value(0.5), eb.animate.set_value(0.5), mk.animate.set_value(0.5),
                tr["r8_o"].animate(rate_func=early).set_value(0.0), tr["r2_o"].animate(rate_func=early).set_value(0.0),
                tr["e2_o"].animate(rate_func=early).set_value(0.9), lab_o.animate(rate_func=early).set_value(0.0),
                run_time=1.8)
        self.remove(rl_a, rl_b)
        self.play(FadeOut(VGroup(ring_a, ring_b)), FadeOut(marker), FadeOut(hypo),
                  dot1.animate.set_fill(opacity=1).set_stroke(opacity=1, background=True),
                  tr["e8_o"].animate.set_value(0.0), tr["e2_o"].animate.set_value(0.0),
                  tr["pink_w"].animate(rate_func=there_and_back).set_value(2.2),
                  Indicate(lab_sqrt, color=ACCENT), run_time=0.6)
        self.remove(c_r8, c_r2, c_e8, c_e2)

        # sweep: the dial reads the rightmost zero
        sweep = DashedLine(M.p(1, 0), M.p(1, 50), color=DIM, stroke_width=3, dash_length=0.1).set_z_index(3)
        self.at("reads", FadeIn(sweep), run_time=0.25)
        self.play(sweep.animate.set_x(M.p(0.5, 0)[0]), run_time=0.85)
        half = strip.floor_labels[1].copy().set_color(ACCENT).set_z_index(12)
        self.at(31.15, half.animate.move_to(dial.labels[1]).scale(28 / 22), run_time=0.65)
        self.play(FadeOut(half), Indicate(dial.labels[1], color=ACCENT, scale_factor=1.35), run_time=0.45)

        pair_l = dashed_ring(M.p(0.3, 40.0))
        pair_r = dashed_ring(M.p(0.7, 40.0))
        pair_lab = VGroup(N("0.3", 24, INK).next_to(pair_l, LEFT, buff=0.08),
                          N("0.7", 24, INK).next_to(pair_r, RIGHT, buff=0.08))
        hypo2 = T("hypothetical", 24, DIM).next_to(M.p(0.5, 50), UP, buff=0.12)
        marker2 = dial.marker(0.7)
        self.at(32.3, FadeIn(VGroup(pair_l, pair_r, pair_lab, hypo2)), run_time=0.45)
        lit = Circle(radius=0.13, stroke_width=0, fill_color=BAD, fill_opacity=0.55).move_to(pair_r)
        self.at(33.05, FadeIn(lit), Indicate(pair_r, color=BAD, scale_factor=1.5),
                sweep.animate.set_x(M.p(0.7, 0)[0]), FadeIn(marker2), run_time=0.65)
        self.at(34.85, FadeOut(VGroup(pair_l, pair_r, pair_lab, hypo2, lit, marker2)),
                sweep.animate.set_x(M.p(0.5, 0)[0]), run_time=0.7)

        self.at("best", Indicate(dial.labels[1], color=ACCENT, scale_factor=1.4), run_time=0.8)
        self.at(36.72, Create(dial.check), FadeIn(dial.check_label, shift=LEFT * 0.1), run_time=0.7)
        pin_halo = halo(Circle(radius=0.2).move_to(dial.pin))
        self.at("guessed", Indicate(VGroup(dial.pin, dial.pin_label), color=ACCENT, scale_factor=1.25),
                FadeIn(pin_halo, rate_func=there_and_back), run_time=0.9)
        self.remove(pin_halo)
        dial.add(dial.check, dial.check_label)

        # ================================================= P5
        for m in (c_pink, c_pe, lab_sqrt, yt[10], yt[500]):
            m.clear_updaters()
        target = strip_group(DIAL_ALIGNED, 10)
        target.floor_labels.set_z_index(11)
        self.at("p5", FadeOut(VGroup(c_pink, c_pe, lab_sqrt, yt[10], yt[500], frame, thumb, ghost, ill_tag, sweep)),
                Transform(strip, target), run_time=1.6)
        D = DIAL_ALIGNED
        edge_lit = Line(D.p(1, 0), D.p(1, 50), color=ACCENT, stroke_width=5)
        edge_lab = VGroup(N("1896", 28, INK), T("no zeros on the right edge", 24, DIM)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(D.p(1, 44), RIGHT, buff=0.25)
        self.at("edge", Create(edge_lit), FadeIn(edge_lab, rate_func=lambda t: smooth(np.clip(t * 2 - 0.4, 0, 1))),
                run_time=1.1)

        row1 = VGroup(T("percentage off", 24, DIM), N("5.4%  →  0.013%", 28, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        row2 = VGroup(T("the gap", 24, DIM), N("9.6  →  754.4", 28, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        head = T("up to 1,000 → 100,000,000", 24, DIM)
        table = VGroup(head, row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-4.6, 0.9, 0])
        chk = check_mark(row1[1].get_right() + RIGHT * 0.38, size=0.16)
        qm = N("?", 34, DIM).next_to(row2[1], RIGHT, buff=0.3)
        self.at("enough", FadeIn(VGroup(head, row1), shift=UP * 0.1), Indicate(dial.window, color=ACCENT,
                scale_factor=1.08), run_time=0.6)
        self.at(47.18, Create(chk), run_time=0.45)
        self.at(48.12, FadeIn(row2, shift=UP * 0.1), run_time=0.5)
        self.at(48.75, FadeIn(qm, scale=1.4), run_time=0.4)

        mid_glow = halo(Line(D.p(0.5, 0), D.p(0.5, 50)))
        self.at("middle", FadeOut(VGroup(table, chk, qm, edge_lab, edge_lit)), Create(mid_glow),
                run_time=1.2)
        self.at(53.28, Indicate(VGroup(dial.coin, dial.coin_label), color=ACCENT, scale_factor=1.2), run_time=0.6)
        self.at("coins", Rotate(dial.coin, angle=TAU, axis=UP), run_time=0.7)

        self.until(55.35, FadeOut(VGroup(strip, mid_glow)))
        self.until("end", FadeOut(dial))
