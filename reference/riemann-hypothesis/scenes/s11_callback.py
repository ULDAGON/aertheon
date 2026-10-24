"""S11_Callback: the hum of the zeros. Back to the opening grid and its staircase; the zeros' waves build it;
Riemann's line; coin-flip error if he is right; twelve trillion checked; very probable, still open.

Layout (camera never moves; the dial is on screen from {#stair} to the end):
  graph   x 0..100 over scene x -6.6..3.4, y 0..26 over scene y -2.4..3.2 (S07's staircase axes)
  inset   strip_group(INSET_240, 100) at the right (x 4.2..6.4), ACCENT line at scene x 5.3
  dial    ErrorDial(best=True) at its home; P3 narrows it to a dashed 'if Riemann is right' glow, P4 undoes it.
Tick labels sit inside the plot (above the x-axis, right of the y-axis) so nothing enters the dial's band.
The strip is built without floor labels (they would fall into the dial's band); the dial carries 0 ½ 1.
Every curve (R, rebuild(k), the ribbons) is sampled on LIN_X[::2] so Transform matches point for point.
Overlapping beats inside one play() are staggered with `win()` rate functions, so the clock stays exact.
The five enlarged waves (P2) are one frame-driven play: `wave_state(t)` gives every ribbon, thread, dot and the
curve at time t, so overlapping waves never fight over the same mobject.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

# ------------------------------------------------------------------ graph mapping (S07's axes)
GX0, GX1, GY0, GY1 = -6.6, 3.4, -2.4, 3.2
XMAX, YMAX = 100.0, 26.0


def gp(x, y):
    return np.array([GX0 + (GX1 - GX0) * x / XMAX, GY0 + (GY1 - GY0) * y / YMAX, 0.0])


def gpts(xs, ys):
    return np.column_stack([GX0 + (GX1 - GX0) * np.asarray(xs) / XMAX, GY0 + (GY1 - GY0) * np.asarray(ys) / YMAX,
                            np.zeros(len(xs))])


XS = LIN_X[::2]                         # 2..100 step 0.05 (1,961 points)
LX = np.log(XS)
BASE = base_lin()[::2]
R_CURVE = BASE + 1 / LX - np.arctan(np.pi / LX) / np.pi     # R(x) exactly (base_curve undone)
CELL = 0.62                             # S01's grid cell
PRIMES = [int(p) for p in primes_upto(100)]
assert len(PRIMES) == 25
STRIP = INSET_240
LINE_X = STRIP.p(0.5, 0)[0]
BAND_Y, BAND_A = 3.3, 0.2               # ribbon band for the enlarged waves (above the graph's top)


def win(total, start, dur, base=smooth):
    """Rate function for an animation inside a play of length `total` that runs from `start` for `dur` s."""
    s = start / total
    e = min(1.0, (start + dur) / total)

    def f(t):
        return base(float(np.clip((t - s) / max(e - s, 1e-6), 0.0, 1.0)))
    return f


def polyline(points, color, width=4, opacity=1.0):
    v = VMobject()
    v.set_points_as_corners(points)
    return v.set_fill(opacity=0).set_stroke(color, width=width, opacity=opacity)


def curve_of(ys, color=CURVE_COLOR, width=3, opacity=1.0):
    return polyline(gpts(XS, ys), color, width, opacity)


def segments(pairs):
    out = []
    for a, b in pairs:
        out += [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]
    return np.array(out)


def rim(m, w=6):
    return m.set_stroke(BG, width=w, background=True)


# ------------------------------------------------------------------ the opening grid (S01 framing)
def cell_pos(n):
    r, c = divmod(n - 1, 10)
    return np.array([(c - 4.5) * CELL, (4.5 - r) * CELL, 0.0])


def build_grid():
    nums = VGroup(*[N(str(n), 26, INK if n in PRIMES else DIM).move_to(cell_pos(n)) for n in range(1, 101)])
    tiles = VGroup(*[RoundedRectangle(corner_radius=0.08, width=CELL - 0.08, height=CELL - 0.08, stroke_width=0,
                                      fill_color=PRIME_COLOR, fill_opacity=0.55).move_to(cell_pos(p)) for p in PRIMES])
    rows = [VGroup(*[m for m in list(tiles) + list(nums) if abs(m.get_center()[1] - (4.5 - r) * CELL) < 0.1])
            for r in range(10)]
    return nums, tiles, rows


def risers():
    """One riser per prime: the step the prime's tile turns into."""
    return VGroup(*[polyline([gp(p, i), gp(p, i + 1)], PRIME_COLOR, 5) for i, p in enumerate(PRIMES)])


def treads():
    """The flat parts of the staircase: 0..2 at height 0, then p_i..p_{i+1} at height i+1 (last one to 100)."""
    spans = [(0.0, 2.0, 0)] + [(p, PRIMES[i + 1] if i + 1 < len(PRIMES) else XMAX, i + 1) for i, p in enumerate(PRIMES)]
    return VGroup(*[polyline([gp(a, h), gp(b, h)], PRIME_COLOR, 5) for a, b, h in spans])


def ramp(t, s, d):
    return float(np.clip((t - s) / d, 0.0, 1.0))


class S11_Callback(TimedScene):
    def construct(self):
        # ============================================================ P1: grid -> staircase, then strip, dial
        nums, tiles, rows = build_grid()
        self.at("grid", LaggedStart(*[FadeIn(r, shift=DOWN * 0.08) for r in rows], lag_ratio=0.12), run_time=1.2)

        pieces = risers()
        flats = treads()
        stair = polyline([gp(x, y) for x, y in staircase_points(100)], PRIME_COLOR, 5)
        axes = VGroup(Line(gp(0, 0), gp(XMAX, 0), color=NEUTRAL, stroke_width=2.5),
                      Line(gp(0, 0), gp(0, YMAX), color=NEUTRAL, stroke_width=2.5))
        ticks = VGroup(*[Line(gp(x, 0), gp(x, 0) + UP * 0.1, color=NEUTRAL, stroke_width=2.5) for x in (50, 100)],
                       *[Line(gp(0, y), gp(0, y) + RIGHT * 0.1, color=NEUTRAL, stroke_width=2.5) for y in (10, 20)])
        tlabels = VGroup(*[N(str(x), 24, DIM).next_to(gp(x, 0), UP, buff=0.16) for x in (50, 100)],
                         *[N(str(y), 24, DIM).next_to(gp(0, y), RIGHT, buff=0.18) for y in (10, 20)])
        graph_frame = VGroup(axes, ticks, tlabels)
        strip = strip_group(STRIP, 100, labels=False)
        dots = strip.dots
        dots.set_z_index(3)                      # zeros stay on top of the brightened line and its glow
        w0 = dots[0].width                       # every dot's rest size (captured once, never re-read)
        dial = ErrorDial(best=True)

        # 'and' (3.82): numbers fade, tiles stay. {#stair}: tiles climb onto their risers in prime order (2, 3, 5, ...),
        # each tread follows its riser; the axis is drawn only once the numbers are gone. Then (pause, 'The primes
        # look scattered') the strip and the dial fade in, so only the staircase moves while 'their staircase' is said.
        tot, t0, lag, fly = 2.2, 0.12, 0.022, 0.5
        anims = [FadeOut(nums, rate_func=win(tot, 0, 0.4)),
                 Create(flats[0], rate_func=win(tot, t0, 0.3))]
        for i, (tile, pc) in enumerate(zip(tiles, pieces)):
            s = t0 + lag * i
            anims.append(ReplacementTransform(tile, pc, path_arc=-0.5, rate_func=win(tot, s, fly)))
            anims.append(Create(flats[i + 1], rate_func=win(tot, s + fly - 0.1, 0.3)))
        anims += [Create(axes, rate_func=win(tot, 0.45, 0.6)),
                  FadeIn(VGroup(ticks, tlabels), rate_func=win(tot, 0.95, 0.5)),
                  FadeIn(strip, rate_func=win(tot, 1.2, 0.7)),
                  FadeIn(dial, rate_func=win(tot, 1.4, 0.8))]
        self.at(3.82, *anims, run_time=tot)
        self.remove(*pieces, *flats)
        self.add(stair)

        # ============================================================ P2: scattered -> waves -> hum
        prime_ticks = VGroup(*[Line(gp(p, 0), gp(p, 0) + UP * 0.16, color=PRIME_COLOR, stroke_width=3) for p in PRIMES])
        self.at(6.3, LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in prime_ticks], lag_ratio=0.08), run_time=1.0)

        # {#evenly}: R draws; wave 1 rises from its zero while it draws, holds, and sinks into the curve (slow, once);
        # waves 2..5 follow overlapped (each rises while the previous sinks), all done by 13.3 s.
        waves = [zero_wave(k)[::2] for k in range(1, 6)]
        stages = [R_CURVE]
        acc = BASE.copy()
        for w in waves:
            acc = acc + w
            stages.append(acc.copy())
        sched = [(0.3, 0.6, 0.45, 0.65)] + [(2.0 + 0.8 * j, 0.45, 0.35, 0.5) for j in range(4)]   # start, rise, hold, sink
        T_w = max(s + r + h + d for s, r, h, d in sched)                                            # 5.7 s
        rib_pts, sink_pts, small_pts, thread_full = [], [], [], []
        for k, w in enumerate(waves):
            ys = BAND_Y + BAND_A * w / np.max(np.abs(w))
            rp = np.column_stack([gpts(XS, np.zeros_like(XS))[:, 0], ys, np.zeros(len(XS))])[::-1]
            c = dots[k].get_center()
            rib_pts.append(rp)
            sink_pts.append(gpts(XS, stages[k + 1])[::-1])
            small_pts.append(c + 0.03 * (rp - rp.mean(axis=0)))
            thread_full.append(Line(c, rp[0], color=WAVE_COLORS[k], stroke_width=1.8))
        curve = curve_of(R_CURVE).set_stroke(opacity=0)
        ribbons = VGroup(*[polyline(rib_pts[k], WAVE_COLORS[k], 3, opacity=0) for k in range(5)])
        threads = VGroup(*[thread_full[k].copy().set_stroke(opacity=0) for k in range(5)])
        self.add(curve, ribbons, threads)
        n_xs = len(XS)

        def draw_waves(m, a):
            t = a * T_w
            ys = R_CURVE.copy()
            for k, (s0, r, h, d) in enumerate(sched):
                ru, su = ramp(t, s0, r), ramp(t, s0 + r + h, d)
                re, se = smooth(ru), smooth(su)
                ys = ys + se * (stages[k + 1] - stages[k])
                rb, th = ribbons[k], threads[k]
                if ru <= 0 or su >= 1:
                    rb.set_stroke(opacity=0)
                else:
                    pts = small_pts[k] + re * (rib_pts[k] - small_pts[k]) if su <= 0 else \
                        rib_pts[k] + se * (sink_pts[k] - rib_pts[k])
                    rb.set_points_as_corners(pts)
                    rb.set_stroke(opacity=min(1.0, 3 * re) * (1 - se ** 2))
                tp = ramp(t, s0, 0.8 * r)
                fade = ramp(t, s0 + r + h, 0.7 * d)
                if tp <= 0 or fade >= 1:
                    th.set_stroke(opacity=0)
                else:
                    th.pointwise_become_partial(thread_full[k], 0, smooth(tp))
                    th.set_stroke(opacity=0.8 * (1 - fade))
            n = int(round(smooth(ramp(t, 0, 0.9)) * (n_xs - 1))) + 1
            pts = gpts(XS, ys)
            if n < 2:
                curve.set_points_as_corners(pts[:2]).set_stroke(opacity=0)
            else:
                curve.set_points_as_corners(pts[:n]).set_stroke(opacity=1)

        def pump_dots(m, a):
            t = a * T_w
            for k, (s0, r, h, d) in enumerate(sched):
                e = smooth(ramp(t, s0, r)) * (1 - smooth(ramp(t, s0 + r + h, d)))
                m[k].width = w0 * (1 + 1.6 * e)
                m[k].set_color(interpolate_color(ManimColor(INK), ManimColor(WAVE_COLORS[k]), e))

        tag = rim(T("waves enlarged", 24, DIM)).move_to([GX0 + 0.3, BAND_Y - 1.0, 0], aligned_edge=LEFT)
        s5, r5, h5, d5 = sched[-1]
        self.at("evenly",
                UpdateFromAlphaFunc(VGroup(curve, ribbons, threads), draw_waves, rate_func=linear),
                UpdateFromAlphaFunc(dots, pump_dots, rate_func=linear),
                FadeIn(tag, rate_func=win(T_w, 0.3, 0.5)),
                FadeOut(tag, rate_func=win(T_w, s5 + r5 + h5, d5)),
                run_time=T_w)
        self.remove(ribbons, threads)

        # {#hum}: the staircase dims, the rebuilt curve (100 zeros) locks onto it; the zeros ripple up, glints run along it
        full = curve_of(rebuild(100)[::2])
        n_d = len(dots)
        glint_xy = gpts(XS, rebuild(100)[::2])

        def ripple(m, a):
            c = -0.15 + 1.3 * a
            for i, d in enumerate(m):
                b = 0.0 if a >= 1 else np.exp(-(((i / (n_d - 1)) - c) / 0.07) ** 2)
                d.width = w0 * (1 + 1.3 * b)
                d.set_color(interpolate_color(ManimColor(INK), ManimColor(ACCENT), b))

        glints = VGroup(*[Dot(radius=0.07, color=INK).set_stroke(ACCENT, width=6, background=True) for _ in range(2)])
        glints.set_opacity(0)
        self.add(glints)

        def run_glints(m, a):
            c = -0.15 + 1.3 * a
            for j, g in enumerate(m):
                s = c - 0.12 * j
                if 0 <= s <= 1 and 0 < a < 1:
                    g.move_to(glint_xy[int(s * (len(glint_xy) - 1))])
                    g.set_opacity(min(1.0, 6 * min(s, 1 - s)) * 0.9)
                else:
                    g.set_opacity(0)

        tot = self.t("p3") - 0.35 - self.t("hum")
        self.at("hum",
                stair.animate(rate_func=win(tot, 0, 0.8)).set_stroke(opacity=0.35),
                Transform(curve, full, rate_func=win(tot, 0, 1.3)),
                UpdateFromAlphaFunc(dots, ripple, rate_func=win(tot, 0.4, tot - 0.4, linear)),
                UpdateFromAlphaFunc(glints, run_glints, rate_func=win(tot, 0.4, tot - 0.4, linear)),
                run_time=tot)
        self.remove(glints)

        # ============================================================ P3: one line; coin-flip error if right
        self.at("p3", stair.animate.set_stroke(opacity=1), run_time=0.6)
        self.at(17.4, dots.animate(rate_func=there_and_back).set_color(ACCENT), run_time=0.7)
        top = STRIP.p(0.5, STRIP.hmax)
        ext = Line(top, top + UP * 1.3, color=ACCENT, stroke_width=5)
        glow = Line(STRIP.p(0.5, 0), top + UP * 1.3, color=ACCENT, stroke_width=16, stroke_opacity=0.22)
        self.add(glow)
        glow.set_stroke(opacity=0)
        self.at("line", strip.line.animate.set_stroke(width=5), Create(ext),
                glow.animate.set_stroke(opacity=0.22), run_time=0.9)

        # 'the primes stray from Gauss's curve': back to the smooth curve (labelled), the gap between them as a hatch
        smooth_curve = curve_of(R_CURVE)
        hx = np.arange(2.0, 100.0, 0.25) + 0.125
        hy_c = np.interp(hx, XS, R_CURVE)
        hy_s = prime_pi(hx)
        gaps = VMobject().set_points(segments([(gp(x, a), gp(x, b)) for x, a, b in zip(hx, hy_s, hy_c)
                                               if abs(a - b) > 0.04]))
        gaps.set_fill(opacity=0).set_stroke(ACCENT, width=2.6, opacity=0.6)
        curve_tag = rim(T("smooth curve", 24, CURVE_COLOR))
        curve_tag.next_to(gp(XMAX, R_CURVE[-1]), UP, buff=0.14).align_to(gp(XMAX, 0), RIGHT)
        self.at(20.7, Transform(curve, smooth_curve), run_time=0.75)
        self.at(21.45, Create(gaps, rate_func=linear), FadeIn(curve_tag, rate_func=win(0.9, 0.2, 0.6)), run_time=0.9)

        # {#coins}: the window glides down to a dashed glow on ½ with a tag tied to it; the coin flips
        win_orig = dial.window.copy()
        narrow = RoundedRectangle(corner_radius=0.08, width=0.36, height=0.44).move_to([dial.x_of(0.5), dial.Y, 0])
        narrow_solid = narrow.copy().set_stroke(ACCENT, width=0).set_fill(ACCENT, 0.3).set_z_index(10)
        dashed = DashedVMobject(narrow.copy().set_stroke(ACCENT, width=3), num_dashes=14).set_z_index(10)
        if_tag = T("if Riemann is right", 24, DIM).move_to([dial.x_of(0.5), -1.66, 0])
        rim(if_tag, 6)
        leader = Line([dial.x_of(0.5), if_tag.get_bottom()[1] - 0.06, 0], [dial.x_of(0.5), DIAL_TOP - 0.02, 0],
                      color=DIM, stroke_width=2)
        self.at("coins", Transform(dial.window, narrow_solid), FadeIn(dashed), FadeIn(if_tag, shift=DOWN * 0.05),
                Create(leader), FadeOut(curve_tag), run_time=1.0)

        coin0 = dial.coin.copy()

        def flip(m, a):
            m.become(coin0.copy().scale(1 + 0.8 * np.sin(PI * a)).rotate(TAU * smooth(a), axis=UP)).set_z_index(11)

        self.at(23.5, UpdateFromAlphaFunc(dial.coin, flip, rate_func=linear),
                dial.coin_label.animate(rate_func=there_and_back).set_color(ACCENT), run_time=0.8)
        dial.coin.set_z_index(10)

        # ============================================================ P4: checked, very probable, still open
        chk = check_mark(ORIGIN, size=0.13)
        readout = VGroup(N("≈ 12.36 trillion zeros", 26, INK), chk).arrange(RIGHT, buff=0.18)
        readout.move_to([LINE_X - 0.8, 3.35, 0], aligned_edge=RIGHT)
        rim(readout[0])
        self.at("checked", FadeIn(readout[0], shift=DOWN * 0.1), Create(chk), run_time=0.8)
        self.at(27.66, glow.animate(rate_func=there_and_back).set_stroke(opacity=0.55), run_time=0.9)

        year = N("1859", 26, DIM)
        german = T("sehr wahrscheinlich", 28, ACCENT, slant=ITALIC)
        english = T("very probable", 24, DIM)
        head = VGroup(year, german).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        card = VGroup(head, english)
        english.next_to(german, DOWN, buff=0.1, aligned_edge=LEFT)
        card.move_to([GX0 + 0.35, 3.3, 0], aligned_edge=UL)
        for m in (year, german, english):
            rim(m)
        self.at("probable", FadeIn(card, shift=DOWN * 0.1), run_time=0.9)

        yl = year.get_left()

        def tick_year(m, a):
            y = int(round(1859 + (2026 - 1859) * a))
            m.become(rim(N(str(y), 26, ACCENT if a >= 1 else DIM)).move_to(yl, aligned_edge=LEFT)
                     .align_to(german, DOWN))

        self.at(31.3, UpdateFromAlphaFunc(year, tick_year, rate_func=smooth), run_time=1.6)

        qmark = rim(N("?", 40, ACCENT), 8).move_to(top + UP * 0.22)
        self.at("open", Transform(dial.window, win_orig), FadeOut(dashed), FadeOut(if_tag), FadeOut(leader),
                FadeIn(qmark, scale=0.6), run_time=1.0)

        # ============================================================ final pause: fade out, dial then '?' last
        content = VGroup(stair, curve, gaps, prime_ticks, graph_frame, strip, ext, glow, readout, card)
        tot = 1.5
        self.at(34.75,
                FadeOut(content, rate_func=win(tot, 0, 0.9)),
                FadeOut(dial, rate_func=win(tot, 0.35, 0.9)),
                FadeOut(qmark, rate_func=win(tot, 0.6, 0.9)),
                run_time=tot)

