"""S02_Gauss: a teenager counts primes.

Beats (all synced to timeline/S02_Gauss.json):
  p1  an echo of S01's end (teal curve on the blue staircase) at the top right hands over; Gauss's card; seven bars
      of true prime counts per block of 1,000 (168 ... 54), with the honesty divider 'Gauss's tables reached 3 million'
      and 'counted today' over the 10M / 100M bars
  p2  a dashed trend settles on the bar tops, the bars shrink to a strip; two number lines of 120 numbers at the same
      scale: 19 primes after 1,000 (average gap 6.9), 7 primes after 1,000,000 (average gap 13.8)
  p3  'ln 1,000 = 6.9', 'ln 1,000,000 = 13.8'; then a ladder of gap bars, each rung one digit longer and +2.3 wider
  p4  one-in-fourteen chance (a lit tile hopping in a row of 14); then the chances 1/ln t add up under a sweep line
      while Gauss's curve li(x) draws in step, and the prime staircase fades in under it
  p5  1896, prime number theorem, a check; the fine print table: % error shrinks, the actual gap grows
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403


def fmt(n):
    return f"{int(n):,}"


class Map2:
    """Problem coordinates (x in [0, xmax], y in [0, ymax]) -> scene points in the box [x0, x1] x [y0, y1]."""

    def __init__(self, x0, x1, y0, y1, xmax, ymax):
        self.x0, self.x1, self.y0, self.y1, self.xmax, self.ymax = x0, x1, y0, y1, xmax, ymax

    def p(self, x, y):
        return np.array([self.x0 + (self.x1 - self.x0) * x / self.xmax, self.y0 + (self.y1 - self.y0) * y / self.ymax, 0.0])

    def pts(self, xs, ys):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        return np.column_stack([self.x0 + (self.x1 - self.x0) * xs / self.xmax,
                                self.y0 + (self.y1 - self.y0) * ys / self.ymax, np.zeros(len(xs))])


def polyline(points, color, width):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(points)


def window(a, b, inner=linear):
    """Rate function that runs `inner` only inside [a, b] of the play (clamped outside): lets one play()
    carry animations on different clocks (e.g. text that leaves in the first third while shapes move)."""
    return lambda t: inner(min(1.0, max(0.0, (t - a) / (b - a))))


class S02_Gauss(TimedScene):
    def construct(self):
        self.p1_blocks()
        self.p2_gaps()
        self.p3_log()
        self.p4_curve()
        self.p5_fine_print()

    # ============================================================ p1: Gauss counts primes in blocks of 1,000
    def p1_blocks(self):
        # the echo of S01's end state: teal curve over the blue staircase up to 100,000 (top right, ~3 x 1.5)
        em = Map2(3.3, 6.3, 1.85, 3.35, 1e5, 1e4)
        sc = staircase_points(1e5)
        e_stair = polyline(em.pts(sc[:, 0], sc[:, 1]), BLUE_P, 4)
        xs = np.linspace(2, 1e5, 120)
        e_curve = polyline(em.pts(xs, li(xs)), TEAL_P, 2.5)
        e_axes = VGroup(Line(em.p(0, 0), em.p(1e5, 0)), Line(em.p(0, 0), em.p(0, 1e4))).set_stroke(NEUTRAL, 2)
        echo = VGroup(e_axes, e_stair, e_curve)
        self.until("p1", FadeIn(echo))

        # Gauss's card (top left)
        name = T("Carl Friedrich Gauss", 30, INK)
        sub = T("about 1792 · age 15 or 16", 24, DIM)
        name.to_corner(UL, buff=0.5)
        sub.next_to(name, DOWN, aligned_edge=LEFT, buff=0.14)
        self.at("gauss", FadeIn(name, shift=RIGHT * 0.15), FadeOut(echo), run_time=0.8)
        self.at("year", Write(sub), run_time=0.9)
        self.card = VGroup(name, sub)

        # seven blocks of 1,000: true prime counts
        counts = block_counts()
        assert counts == [168, 135, 106, 81, 75, 61, 54]
        tags = ["1", "1k", "10k", "100k", "1M", "10M", "100M"]
        base, k, bw = -2.2, 0.021, 0.8
        bx = [-5.4 + 1.8 * i for i in range(7)]
        bars = VGroup(*[Rectangle(width=bw, height=c * k, stroke_width=0).set_fill(BLUE_P, 0.9)
                        .move_to([x, base + c * k / 2, 0]) for x, c in zip(bx, counts)])
        nums = VGroup(*[N(c, 26, INK).next_to(b, UP, buff=0.12) for b, c in zip(bars, counts)])
        labs = VGroup(*[N(t, 24, DIM).move_to([x, base - 0.3, 0]) for x, t in zip(bx, tags)])
        floor = Line([-6.4, base, 0], [6.4, base, 0], color=NEUTRAL, stroke_width=2)
        cap = T("primes among the 1,000 numbers starting at …", 24, DIM).move_to([0, -3.15, 0])
        self.bars = bars
        grows = [AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(n, shift=UP * 0.1), FadeIn(l))
                 for b, n, l in zip(bars, nums, labs)]
        self.at("blocks", Create(floor), FadeIn(cap), run_time=0.4)
        self.until(self.t("p1s2_end") - 0.5, LaggedStart(*grows, lag_ratio=0.25))

        # honesty: what Gauss counted himself vs. what was counted today
        dx = (bx[4] + bx[5]) / 2
        divider = DashedLine([dx, base - 0.45, 0], [dx, 1.65, 0], color=DIM, stroke_width=2, dash_length=0.1)
        gt = T("Gauss's tables reached 3 million", 24, DIM).next_to(divider, UP, buff=0.12)
        today = T("counted today", 24, DIM).move_to([(bx[5] + bx[6]) / 2, nums[5].get_top()[1] + 0.35, 0])
        self.play(Create(divider), FadeIn(gt, shift=DOWN * 0.1), FadeIn(today, shift=DOWN * 0.1), run_time=1.0)
        self.p1_rest = VGroup(nums, labs, floor, cap, divider, gt, today)

    # ============================================================ p2: they thin out
    def p2_gaps(self):
        tops = [b.get_top() for b in self.bars]
        trend = VMobject().set_points_smoothly([p + UP * 0.02 for p in tops])
        trend = DashedVMobject(trend.set_stroke(INK, 3), num_dashes=40).set_stroke(INK, 3, opacity=0.75)
        self.at("thin", Create(trend), run_time=0.75)

        strip = VGroup(self.bars, trend)
        target = strip.copy().scale(0.3).move_to([0, 3.0, 0])
        self.play(Transform(strip, target), FadeOut(self.p1_rest), FadeOut(self.card), run_time=0.85)
        self.strip = strip

        rows = []
        for start, y in ((1000, 1.35), (1_000_000, -0.95)):
            def X(n, s=start):
                return -6.0 + 12.0 * (n - s + 0.5) / 120
            line = Line([-6.0, y, 0], [6.0, y, 0], color=NEUTRAL, stroke_width=3)
            small = VGroup(*[Line([X(n), y, 0], [X(n), y + (0.14 if (n - start) % 10 == 0 else 0.07), 0])
                             for n in range(start, start + 120)]).set_stroke(DIM, 1.5)
            P = [int(p) for p in primes_upto(start + 119) if p >= start]
            ticks = VGroup(*[Line([X(p), y, 0], [X(p), y + 0.5, 0], color=BLUE_P, stroke_width=5) for p in P])
            lo = N(fmt(start), 24, DIM).next_to([-6.0, y, 0], DOWN, buff=0.14).align_to([-6.0, 0, 0], LEFT)
            hi = N(fmt(start + 119), 24, DIM).next_to([6.0, y, 0], DOWN, buff=0.14).align_to([6.0, 0, 0], RIGHT)
            rows.append(dict(y=y, primes=P, line=VGroup(line, small, lo, hi), ticks=ticks))
        assert len(rows[0]["primes"]) == 19 and len(rows[1]["primes"]) == 7

        # readouts: average gap measured over a wider window (1,000 / #primes in it)
        P = primes_upto(1_050_000)
        g1 = 1000 / np.count_nonzero((P >= 500) & (P <= 1500))
        g2 = 100_000 / np.count_nonzero((P >= 950_000) & (P <= 1_050_000))
        assert f"{g1:.1f}" == "6.9" and f"{g2:.1f}" == "13.8"
        reads = []
        for r, near, g, note in ((rows[0], "1,000", g1, "measured from 500 to 1,500"),
                                 (rows[1], "1,000,000", g2, "measured from 950,000 to 1,050,000")):
            head = T(f"average gap near {near}:", 28, INK)
            val = N(f"{g:.1f}", 32, INK).next_to(head, RIGHT, buff=0.2)
            val.align_to(head, DOWN).shift(DOWN * 0.03)
            ro = VGroup(head, val).move_to([0, r["y"] - 0.78, 0]).align_to([-6.0, 0, 0], LEFT)
            nt = T(note, 24, DIM).next_to(ro, DOWN, buff=0.1, aligned_edge=LEFT)
            reads.append(dict(head=head, val=val, note=nt, all=VGroup(ro, nt)))
        self.rows, self.reads = rows, reads

        # "near a thousand" -> the first line; "seven" -> its primes sweep in, readout
        self.at(self.t("p2s1") + 1.32, Create(rows[0]["line"]), run_time=0.9)
        self.at(self.t("seven") - 0.2, LaggedStart(*[GrowFromEdge(t, DOWN) for t in rows[0]["ticks"]], lag_ratio=0.12),
                FadeIn(reads[0]["all"], shift=UP * 0.1), run_time=1.1)
        # "near a million" -> the second line; "fourteen" -> its sparse primes, readout
        self.at(self.t("p2s1") + 5.36, Create(rows[1]["line"]), run_time=0.9)
        self.at(self.t("fourteen") - 0.2, LaggedStart(*[GrowFromEdge(t, DOWN) for t in rows[1]["ticks"]], lag_ratio=0.2),
                FadeIn(reads[1]["all"], shift=UP * 0.1), run_time=1.0)

    # ============================================================ p3: the gap is ln x, +2.3 per digit
    def p3_log(self):
        rows, reads = self.rows, self.reads
        # "That typical gap": the two measured gaps light up
        self.at(self.t("p3s1") + 0.6, *[Indicate(r["val"], color=ACCENT, scale_factor=1.25) for r in reads], run_time=0.9)

        lns = []
        for r, near, x in ((reads[0], "1,000", 1e3), (reads[1], "1,000,000", 1e6)):
            lab = N(f"ln {near} = {np.log(x):.1f}", 30, ACCENT)
            lab.move_to(r["head"]).align_to([2.3, 0, 0], LEFT)
            lns.append(lab)
        lncap = T("natural logarithm, ln", 24, DIM).next_to(lns[0], DOWN, buff=0.14, aligned_edge=LEFT)
        lncap.align_to(reads[0]["note"], DOWN)
        self.at("log", LaggedStart(*[FadeIn(l, shift=LEFT * 0.4) for l in lns], lag_ratio=0.3),
                FadeIn(lncap), run_time=1.0)

        # the ladder: one rung per digit; bar length = ln x (0.33 units per unit of gap)
        xs = [1e3, 1e4, 1e5, 1e6]
        ys = [1.25, 0.35, -0.55, -1.45]
        u, bx0 = 0.33, -2.1
        rungs, exts, tags = [], [], []
        for i, (x, y) in enumerate(zip(xs, ys)):
            g = np.log(x)
            lab = N(fmt(x), 28, INK).move_to([0, y, 0]).align_to([bx0 - 0.3, 0, 0], RIGHT)
            prev = np.log(xs[i - 1]) if i else g
            bar = Rectangle(width=prev * u, height=0.3, stroke_width=0).set_fill(DIM, 0.55)
            bar.move_to([bx0 + prev * u / 2, y, 0])
            val = N(f"{g:.1f}", 28, INK).move_to([bx0 + g * u + 0.45, y, 0])
            rungs.append(VGroup(lab, bar, val))
            if i:
                ext = Rectangle(width=(g - prev) * u, height=0.3, stroke_width=0).set_fill(ACCENT, 0.85)
                ext.move_to([bx0 + (prev + g) * u / 2, y, 0])
                tag = N(f"+{g - prev:.1f}", 28, ACCENT).move_to([4.3, (y + ys[i - 1]) / 2, 0])
                exts.append(ext)
                tags.append(tag)
        heads = VGroup(T("near", 24, DIM).move_to([0, 1.95, 0]).align_to(rungs[0][0], RIGHT),
                       T("typical gap, ln x", 24, DIM).move_to([0, 1.95, 0]).align_to([bx0, 0, 0], LEFT))
        # rung 4 is a full bar from the start (it arrives from ln 1,000,000); its extension is drawn on top
        full4 = Rectangle(width=np.log(1e6) * u, height=0.3, stroke_width=0).set_fill(DIM, 0.55).move_to(
            [bx0 + np.log(1e6) * u / 2, ys[3], 0])
        r1 = VGroup(rungs[0][0], rungs[0][1], rungs[0][2])
        r4 = VGroup(rungs[3][0], full4, rungs[3][2])

        old = VGroup(*[r["line"] for r in rows], *[r["ticks"] for r in rows],
                     *[r["all"] for r in reads], lncap)
        self.at("p3s2", FadeOut(old), FadeTransform(lns[0], r1), FadeTransform(lns[1], r4), FadeIn(heads),
                run_time=1.1)
        # rungs 10,000 and 100,000; then every rung's extra piece lights up with +2.3
        mid = VGroup(rungs[1], rungs[2])
        self.until(self.t("digit") - 0.1, FadeIn(mid, shift=RIGHT * 0.2))
        full4.set_fill(DIM, 0.55)
        ext4 = exts[2]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(e, scale=0.8), FadeIn(t, shift=LEFT * 0.3))
                                for e, t in zip(exts, tags)], lag_ratio=0.45), run_time=1.5)
        self.ladder = VGroup(*rungs, full4, *exts, *tags, heads, ext4)
        self.until(self.t("p3_end") + 0.7, FadeOut(self.ladder), FadeOut(self.strip), run_time=None)

    # ============================================================ p4: chance 1/ln x, add up -> Gauss's curve
    def p4_curve(self):
        n = 14
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.66, height=0.66, stroke_color=DIM, stroke_width=2)
                         .set_fill(BG, 1).move_to([(i - (n - 1) / 2) * 0.8, 0, 0]) for i in range(n)])
        head = N("chance ≈ 1 / ln x", 32, INK).move_to([0, 1.2, 0])
        note = T("near a million: ln x ≈ 13.8, so about one number in 14", 24, DIM).move_to([0, -1.0, 0])
        self.until("chance", FadeIn(tiles, lag_ratio=0.03), FadeIn(head, shift=DOWN * 0.1))
        rng = np.random.default_rng(5)
        lit, cur = None, None
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        while self.left("add") > 0.8:
            j = cur
            while j == cur:
                j = int(rng.integers(0, n))
            anims = [tiles[j].animate.set_fill(BLUE_P, 0.95).set_stroke(BLUE_P)]
            if cur is not None:
                anims.append(tiles[cur].animate.set_fill(BG, 1).set_stroke(DIM))
            self.play(*anims, run_time=0.25)
            cur = j
            self.wait(min(0.35, max(0.0, self.left("add") - 0.8)))

        # the graph: main axes 0..1,000,000 x 0..80,000; small panel above with the density 1/ln t (same x mapping)
        M = Map2(-5.0, 1.6, -3.0, 0.6, 1e6, 80_000)
        D = Map2(-5.0, 1.6, 1.35, 2.95, 1e6, 0.25)
        axes = VGroup(Line(M.p(0, 0), M.p(1e6, 0)), Line(M.p(0, 0), M.p(0, 80_000))).set_stroke(NEUTRAL, 2.5)
        xt = VGroup(*[N(s, 24, DIM).next_to(M.p(v, 0), DOWN, buff=0.12) for v, s in ((0, "0"), (5e5, "500,000"),
                                                                                  (1e6, "1,000,000"))])
        yt = VGroup(*[VGroup(Line(M.p(0, v) + LEFT * 0.07, M.p(0, v) + RIGHT * 0.07).set_stroke(NEUTRAL, 2),
                             N(fmt(v), 24, DIM).next_to(M.p(0, v), LEFT, buff=0.14)) for v in (40_000, 80_000)])
        ylab = T("primes up to x", 24, DIM).next_to(M.p(0, 80_000), RIGHT, buff=0.2).shift(UP * 0.15)
        xlab = N("x", 28, DIM).next_to(M.p(1e6, 0), RIGHT, buff=0.2)
        d_axes = VGroup(Line(D.p(0, 0), D.p(1e6, 0)), Line(D.p(0, 0), D.p(0, 0.25))).set_stroke(NEUTRAL, 2)
        ts = np.linspace(2, 1e6, 400)
        dens = np.minimum(1 / np.log(ts), 0.25)   # clipped at the panel top (only t < 55 is cut, invisible here)
        d_curve = polyline(D.pts(ts, dens), DIM, 2.5)
        d_lab = T("chance of a prime near t:  1 / ln t", 24, DIM).move_to(D.p(5.5e5, 0.19))
        panel = VGroup(d_axes, d_curve, d_lab)
        graph = VGroup(axes, xt, yt, ylab, xlab)

        self.at("add", FadeOut(VGroup(tiles, head, note)), run_time=0.4)
        self.play(FadeIn(graph), FadeIn(panel), run_time=0.5)

        # the sweep: area under 1/ln t shades teal, and its running total is Gauss's curve li(x), drawn in step
        L = li(ts)
        tr = ValueTracker(2.0)

        def upto():
            X = tr.get_value()
            k = max(2, int(np.searchsorted(ts, X)))
            return k, X

        def area_m():
            k, X = upto()
            top = D.pts(ts[:k], dens[:k])
            poly = np.vstack([[D.p(ts[0], 0)], top, [D.p(ts[k - 1], 0)]])
            return Polygon(*poly, stroke_width=0).set_fill(TEAL_P, 0.45)

        def curve_m():
            k, X = upto()
            return polyline(M.pts(ts[:k], L[:k]), TEAL_P, 4)

        def sweep_m():
            X = tr.get_value()
            return Line(M.p(X, 0), D.p(X, 0.25), color=ACCENT, stroke_width=3)

        area, curve, sweep = always_redraw(area_m), always_redraw(curve_m), always_redraw(sweep_m)
        self.add(area, d_curve, curve, sweep)
        self.until(self.t("p4s2_end") - 0.55, tr.animate(rate_func=smooth).set_value(1e6))
        for m in (area, curve, sweep):
            m.clear_updaters()
        self.remove(area, curve)
        area, curve = area_m(), curve_m()
        self.add(area, curve)

        # the true prime staircase fades in underneath; the two nearly coincide
        sc = staircase_points(1e6)
        stair = polyline(M.pts(sc[:, 0], sc[:, 1]), BLUE_P, 7)
        stair.set_z_index(-1)
        end = M.p(1e6, L[-1])
        g_lab = T("Gauss's curve", 26, TEAL_P).next_to(end, RIGHT, buff=0.3).shift(UP * 0.12)
        s_lab = T("prime staircase", 24, BLUE_P).next_to(g_lab, DOWN, buff=0.14, aligned_edge=LEFT)
        self.play(FadeIn(stair), FadeOut(sweep), FadeIn(g_lab, shift=LEFT * 0.15), run_time=0.6)
        self.play(FadeIn(s_lab, shift=LEFT * 0.15), run_time=0.5)
        # pause: the upper panel fades
        self.until(self.t("p4_end") + 0.7, FadeOut(panel), FadeOut(area))
        self.graph = VGroup(graph, stair, curve)
        self.g_lab, self.s_lab = g_lab, s_lab

    # ============================================================ p5: proved right - in percentage terms only
    def p5_fine_print(self):
        c1 = VGroup(N("1896", 30, ACCENT), T("·  Hadamard  ·  de la Vallée Poussin", 26, INK)).arrange(RIGHT, buff=0.2)
        c1[0].align_to(c1[1], DOWN).shift(DOWN * 0.02)
        c2 = T("prime number theorem", 24, DIM)
        cap = VGroup(c1, c2).arrange(DOWN, buff=0.14).to_corner(UR, buff=0.5)
        c2.align_to(c1, RIGHT)
        self.at("proof", FadeIn(c1[0], shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(c1[1], shift=LEFT * 0.15), run_time=0.9)
        self.play(FadeIn(c2), run_time=0.6)

        chk = check_mark(self.g_lab.get_right() + RIGHT * 0.35, size=0.17)
        self.at("right", Create(chk), Indicate(self.graph[2], color=TEAL_P, scale_factor=1.0), run_time=0.7)

        # fine print: the graph shrinks to the left third; the table's headers appear
        labs = VGroup(self.g_lab, chk, self.s_lab)
        tgt = self.graph.copy().scale(0.52).move_to([-4.35, -0.15, 0])
        lab_tgt = labs.copy().arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lab_tgt.next_to(tgt, DOWN, buff=0.35).align_to(tgt, LEFT)
        chk_t = lab_tgt[1]
        chk_t.next_to(lab_tgt[0], RIGHT, buff=0.2)
        lab_tgt[2].next_to(lab_tgt[0], DOWN, buff=0.14, aligned_edge=LEFT)

        cx = [0.35, 2.95, 5.25]
        hy, ry = 1.45, [0.35, -0.6, -1.55]
        H = VGroup(T("up to", 24, DIM).move_to([0, hy, 0]).align_to([cx[0] + 0.4, 0, 0], RIGHT),
                   T("off by", 24, DIM).move_to([cx[1], hy, 0]),
                   T("curve − staircase", 24, DIM).move_to([cx[2], hy, 0]))
        hn = T("as % of the curve", 24, DIM).next_to(H[1], DOWN, buff=0.08)
        rule = Line([-1.8, hy - 0.62, 0], [6.5, hy - 0.62, 0], color=FAINT, stroke_width=2)
        self.at("fine", Transform(self.graph, tgt), Transform(labs, lab_tgt), FadeIn(H, shift=DOWN * 0.1), FadeIn(hn),
                Create(rule), run_time=1.0)

        # rows: li(x) against the true prime count
        xs = [1e3, 1e6, 1e8]
        pis = {1e3: 168, 1e6: 78_498, 1e8: 5_761_455}
        assert list(prime_pi([1e3, 1e6])) == [168, 78_498]
        Lx = li(xs)
        rows, pc, gp = [], [], []
        for x, Lv, y in zip(xs, Lx, ry):
            d = Lv - pis[x]
            pct = 100 * d / Lv
            ptxt = f"{pct:.1f}%" if pct >= 1 else (f"{pct:.2f}%" if pct >= 0.1 else f"{pct:.3f}%")
            a = N(fmt(x), 28, INK).move_to([0, y, 0]).align_to([cx[0] + 0.4, 0, 0], RIGHT)
            b = N(ptxt, 28, INK).move_to([cx[1], y, 0])
            c = N(f"{d:.1f}", 28, INK).move_to([cx[2], y, 0])
            rows.append(VGroup(a, b, c))
            pc.append(b)
            gp.append(c)
        assert [m.text for m in pc] == ["5.4%", "0.16%", "0.013%"] and [m.text for m in gp] == ["9.6", "129.5", "754.4"]
        self.at("ratio", LaggedStart(*[FadeIn(r, shift=UP * 0.12) for r in rows], lag_ratio=0.5), run_time=1.2)

        # "the percentage error shrinks toward nothing": the column itself shrinks and fades toward nothing
        w1 = T("shrinks toward 0", 24, DIM).move_to([cx[1], -2.35, 0])
        self.at(self.t("p5s2") + 2.87, *[m.animate.scale(s).set_opacity(o) for m, s, o in zip(pc, (1.15, 0.9, 0.72),
                                                                                             (1, 0.75, 0.5))],
                FadeIn(w1, shift=UP * 0.1), run_time=0.9)
        # "while the actual gap keeps growing": the right column grows, ACCENT
        w2 = T("keeps growing", 24, ACCENT).move_to([cx[2], -2.35, 0])
        self.at("gap", LaggedStart(*[m.animate.scale(s).set_color(ACCENT) for m, s in zip(gp, (0.9, 1.15, 1.45))],
                                   lag_ratio=0.35), FadeIn(w2, shift=UP * 0.1), run_time=1.3)
        self.play(*[Indicate(m, color=ACCENT, scale_factor=1.12) for m in gp], run_time=0.8)

        everything = VGroup(cap, self.graph, labs, H, hn, rule, *rows, w1, w2)
        self.until("end", FadeOut(everything))
