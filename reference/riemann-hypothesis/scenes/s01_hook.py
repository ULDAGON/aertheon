"""S01_Hook: the numbers 1..100 with the primes lit, no visible rule, 101 found by checking; the primes become a
staircase that blurs into a smooth curve from far away; how precise is that curve? Riemann 1859; prize, checks, no proof.

Picture beats (scheduled against timeline/S01_Hook.json; word times via self.w, never hand-copied):
  P1  10x10 grid fades in row by row ({#grid}); the 25 primes light up in reading order ({#primes}); 7 and 13 pulse
      on their words; the ledger at the right shows '6 = 2 x 3' ("can't") and '7  no split' ({#split}).
  P2  prime tiles ripple ("atoms"); 12, 45, 91 flash and their factorisations (prime factors in blue) appear in the
      ledger one by one while the prime tiles used brighten ({#atoms}); the 24 gaps between neighbouring primes grow as
      uneven bars in the ledger column ("pattern?") and hold; 97 gets an ACCENT outline ("ninety-seven"); a big ACCENT '?' sits in the
      slot after 100 ("where"); it pulses in the 1.2 s pause.
  P3  grid shifts up half a row, the row 101..110 fades in; the '?' drops into the 101 slot ("you check"); ledger:
      98, 100 ({#even}), 99 ({#nines}) are crossed off (cells go FAINT), 101 lights blue ({#found}).
  P4  the 26 lit tiles crackle like static, two passes on/off ({#noise}); the digits go and each prime tile drops onto
      the number line at x = p ({#count}); from "one" each bar rises to its step, the count ticking 1..25; the finished
      staircase holds, then zooms out to 100,000 ({#back}); a magnifier at 50,000 shows the tiny exact steps ({#blur},
      open until "smooth"); the thin teal curve li(x) draws on a wide blue staircase band ({#curve}), 'smooth curve'
      on "follows".
  P5  a magnifier at the right end shows the gap between curve and staircase ("Exactly how precise?"); title
      ({#precise}); graph slides left and dims, Riemann card: 1859, Berlin Academy, about 8 pages ({#riemann}), name,
      'sehr wahrscheinlich' / 'very probable' ({#probable}).
  P6  '$1,000,000' + 'Clay Millennium Prize' ({#prize}); counter to 12,000,000,000,000+ ({#checked}), check on
      "never failed"; 'proof' with an empty box ({#never}); everything fades out in the final pause.

All numbers are exact: primes from topic.primes_upto, staircase from topic.staircase_points / exact corners,
curve = topic.li (li(100,000) = 9,629.8 vs 9,592 primes).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

# ------------------------------------------------------------------ layout
CELL = 0.62
GX = -0.9                       # grid centre x
NUM_SIZE = 24
TILE = 0.54
LEDGER_X = 3.25                 # left edge of the ledger column at the right of the grid
PRIMES100 = [int(p) for p in primes_upto(100)]
LIT = PRIMES100 + [101]

# graph (P4..P5): x 0..X over scene x -6..6, y 0..Y(X) over scene y -3..3
GX0, GX1, GY0, GY1 = -6.0, 6.0, -3.0, 3.0
K_Y = np.log(400) / np.log(1000)      # Y(X) = 26 (X/100)^K_Y: 26 at X = 100, 10,400 at X = 100,000


def Ymax(X):
    return 26.0 * (X / 100.0) ** K_Y


def to_scene(x, y, X, Y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    return np.column_stack([GX0 + (GX1 - GX0) * x / X, GY0 + (GY1 - GY0) * y / Y, np.zeros_like(x)])


def cell_pos(n, lift=0.0):
    r, c = (n - 1) // 10, (n - 1) % 10
    return np.array([GX + (c - 4.5) * CELL, (4.5 - r) * CELL + lift, 0.0])


def eq(*parts, size=30):
    """A ledger line from (text, colour) parts; primes are blue, everything else INK/DIM."""
    g = VGroup(*[(N(s, size, c) if f == "n" else T(s, size - 4, c)) for s, c, f in parts])
    g.arrange(RIGHT, buff=0.14)
    for m in g:
        m.set_y(g.get_y())
    return g


def P(s):
    return (s, BLUE_P, "n")


def I(s):
    return (s, INK, "n")


def D(s):
    return (s, DIM, "n")


def pulse(mob, s=1.25):
    return mob.animate(rate_func=there_and_back).scale(s)


def dense(points, step=0.01):
    """Resample a polyline so every segment is <= step long (corners kept exactly)."""
    out = [points[0]]
    for a, b in zip(points[:-1], points[1:]):
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / step)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * i / n)
    return np.array(out)


def clipped(points, C, R, color, width):
    """The part of a (monotone) polyline inside the circle (C, R) as one VMobject."""
    pts = dense(points)
    keep = np.linalg.norm(pts - C, axis=1) < R
    idx = np.flatnonzero(keep)
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts[idx[0]: idx[-1] + 1])
    return m


def magnifier(Pt, C, R, content, r0=0.13):
    """Small circle at Pt on the graph, a big BG disc at C with the zoomed content, and two tangent connectors."""
    Pt, C = np.array(Pt, float), np.array(C, float)
    d = C - Pt
    D_ = np.linalg.norm(d)
    u = d / D_
    phi = np.arccos((r0 - R) / D_)
    conns = VGroup()
    for sgn in (1, -1):
        n = rotate_vector(u, sgn * phi)
        conns.add(Line(Pt + r0 * n, C + R * n, color=DIM, stroke_width=1.5))
    small = Circle(radius=r0, color=NEUTRAL, stroke_width=2).move_to(Pt)
    disc = Circle(radius=R, stroke_width=0).set_fill(BG, 1).move_to(C)
    rim = Circle(radius=R, color=NEUTRAL, stroke_width=2.5).move_to(C)
    g = VGroup(conns, small, disc, content, rim)
    g.conns, g.small, g.disc, g.content, g.rim = conns, small, disc, content, rim
    g.set_z_index(6)
    return g


def dimmed(mob, amt=0.62):
    """Copy of mob with every colour pulled towards BG (a dim that keeps BG discs opaque)."""
    c = mob.copy()
    bg = ManimColor(BG)
    for m in c.get_family():
        if isinstance(m, VMobject) and len(m.points):
            m.set_stroke(interpolate_color(ManimColor(m.get_stroke_color()), bg, amt))
            m.set_fill(interpolate_color(ManimColor(m.get_fill_color()), bg, amt))
    return c


class S01_Hook(TimedScene):
    def w(self, sid, word, nth=1):
        hits = [x["s"] for s in self.tl["sentences"] if s["id"] == sid
                for x in s["words"] if x["w"].strip(",.?!;:").lower() == word]
        if len(hits) < nth:
            raise KeyError(f"word {word!r} (#{nth}) not in sentence {sid}")
        return hits[nth - 1]

    def construct(self):
        w = self.w
        # ============================================================ P1: the grid and its primes
        digits = {n: N(str(n), NUM_SIZE, DIM).move_to(cell_pos(n)).set_z_index(3) for n in range(1, 111)}
        tiles = {}
        for n in LIT:
            tiles[n] = RoundedRectangle(corner_radius=0.08, width=TILE, height=TILE, stroke_width=0,
                                        fill_color=BLUE_P, fill_opacity=0.55).move_to(cell_pos(n)).set_z_index(1)
        rows = [VGroup(*[digits[n] for n in range(10 * r + 1, 10 * r + 11)]) for r in range(10)]

        self.at("grid", LaggedStart(*[FadeIn(r, shift=DOWN * 0.08) for r in rows], lag_ratio=0.18), run_time=1.6)

        # primes light up in reading order, 0.06 s apart
        r1 = 0.46
        self.at("primes", LaggedStart(*[AnimationGroup(FadeIn(tiles[p], scale=0.6), digits[p].animate.set_color(INK))
                                        for p in PRIMES100], lag_ratio=0.06 / r1), run_time=r1 + 24 * 0.06)

        def cellg(n):
            return VGroup(tiles[n], digits[n]) if n in tiles else digits[n]

        self.at(w("p1s2", "seven"), pulse(cellg(7)), run_time=0.5)
        self.at(w("p1s2", "thirteen"), pulse(cellg(13)), run_time=0.5)

        six = eq(I("6"), D("="), P("2"), D("×"), P("3")).move_to([LEDGER_X, 0.95, 0], aligned_edge=LEFT)
        seven = VGroup(N("7", 30, BLUE_P), T("no split", 24, DIM)).arrange(RIGHT, buff=0.3)
        seven.move_to([LEDGER_X, 0.3, 0], aligned_edge=LEFT)
        self.at(w("p1s2", "can't"), FadeIn(six, shift=LEFT * 0.15),
                digits[6].animate(rate_func=there_and_back).set_color(INK).scale(1.3), run_time=0.55)
        self.at("split", FadeIn(seven, shift=LEFT * 0.15), pulse(cellg(7), 1.2), run_time=0.55)
        self.at(self.t("p1_end") + 0.25, FadeOut(six), FadeOut(seven), run_time=0.5)

        # ============================================================ P2: atoms, no pattern, the next prime?
        self.at(w("p2s1", "atoms"), LaggedStart(*[pulse(tiles[p], 1.12) for p in PRIMES100], lag_ratio=0.08),
                run_time=1.0)
        facts = [
            (12, [I("12"), D("="), P("2"), D("×"), P("2"), D("×"), P("3")], (2, 3), "atoms", None),
            (45, [I("45"), D("="), P("3"), D("×"), P("3"), D("×"), P("5")], (3, 5), None, "number"),
            (91, [I("91"), D("="), P("7"), D("×"), P("13")], (7, 13), None, "one"),
        ]
        ledger = VGroup()
        for i, (n, parts, used, mark, word) in enumerate(facts):
            line = eq(*parts).move_to([LEDGER_X, 1.2 - 0.65 * i, 0], aligned_edge=LEFT)
            ledger.add(line)
            t0 = mark if mark else w("p2s1", word)
            self.at(t0, FadeIn(line, shift=LEFT * 0.15),
                    digits[n].animate(rate_func=there_and_back).set_color(INK).scale(1.35),
                    *[tiles[p].animate(rate_func=there_and_back).set_fill(opacity=1.0) for p in used], run_time=0.6)
        self.at(w("p2s1", "them"), FadeOut(ledger), run_time=0.5)

        # "But is there a pattern?": the gaps between neighbouring primes (1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, ...) grow as
        # bars in the ledger column, in order, clearly uneven. (A line through the grid read as crossing numbers out.)
        gaps = [b - a for a, b in zip(PRIMES100[:-1], PRIMES100[1:])]
        GAP_BASE, GAP_UNIT, GAP_PITCH = -1.0, 0.2, 0.133
        bars = VGroup(*[Rectangle(width=0.075, height=g * GAP_UNIT, stroke_width=0, fill_color=DIM, fill_opacity=0.9)
                        .move_to([LEDGER_X + 0.04 + i * GAP_PITCH, GAP_BASE + g * GAP_UNIT / 2, 0])
                        for i, g in enumerate(gaps)])
        gbase = Line([LEDGER_X - 0.04, GAP_BASE, 0], [LEDGER_X + 0.12 + 23 * GAP_PITCH, GAP_BASE, 0],
                     color=NEUTRAL, stroke_width=2)
        glab = T("gaps between primes", 24, DIM).next_to(gbase, DOWN, buff=0.18).align_to(gbase, LEFT)
        snake = VGroup(gbase, bars, glab)
        self.at("p2s2", FadeIn(gbase), FadeIn(glab, shift=UP * 0.1),
                LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), run_time=1.0)

        outline97 = RoundedRectangle(corner_radius=0.08, width=TILE + 0.06, height=TILE + 0.06, stroke_color=ACCENT,
                                     stroke_width=4).move_to(cell_pos(97)).set_z_index(2)
        self.at(w("p2s2", "ninety-seven"), FadeOut(snake), Create(outline97), pulse(cellg(97), 1.15), run_time=0.6)
        q = N("?", 60, ACCENT).move_to(cell_pos(100) + RIGHT * (CELL + 0.12)).set_z_index(4)
        self.at(w("p2s2", "where"), FadeIn(q, scale=0.4), run_time=0.5)
        self.at(self.t("p2_end") + 0.15, pulse(q, 1.3), run_time=0.7)

        # ============================================================ P3: you check
        lift = CELL / 2
        grid_now = VGroup(*[digits[n] for n in range(1, 101)], *[tiles[p] for p in PRIMES100], outline97)
        new_row = VGroup(*[digits[n].shift(UP * lift) for n in range(102, 111)])
        self.at("p3", grid_now.animate.shift(UP * lift), q.animate.shift(UP * lift), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d) for d in new_row], lag_ratio=0.1), run_time=1.0)
        slot = cell_pos(101, lift)
        self.at(w("p3s1", "you", 2), q.animate.scale(0.55).move_to(slot), run_time=0.6)

        def cross(n, parts, y):
            line = eq(*parts).move_to([LEDGER_X, y, 0], aligned_edge=LEFT)
            return line, AnimationGroup(FadeIn(line, shift=LEFT * 0.15), digits[n].animate.set_color(FAINT))

        l98, a98 = cross(98, [I("98"), D("="), P("2"), D("×"), I("49")], -0.55)
        l99, a99 = cross(99, [I("99"), D("="), I("9"), D("×"), P("11")], -1.2)
        l100, a100 = cross(100, [I("100"), D("="), P("2"), D("×"), I("50")], -1.85)
        self.at("even", a98, run_time=0.55)
        self.at(w("p3s2", "hundred"), a100, run_time=0.55)
        self.at("nines", a99, run_time=0.55)
        l101 = VGroup(N("101", 30, INK), T("prime", 26, BLUE_P)).arrange(RIGHT, buff=0.25)
        l101.move_to([LEDGER_X, -2.5, 0], aligned_edge=LEFT)
        digits[101].shift(UP * lift).set_color(INK)
        tiles[101].shift(UP * lift)
        self.at("found", FadeOut(q, scale=0.5), FadeIn(digits[101], scale=0.5), FadeIn(tiles[101], scale=0.6),
                FadeOut(outline97), run_time=0.5)
        ring101 = tiles[101].copy().set_fill(opacity=0).set_stroke(ACCENT, 4).set_z_index(2)
        self.play(FadeIn(l101, shift=LEFT * 0.15), ShowPassingFlash(ring101, time_width=1.0),
                  pulse(VGroup(tiles[101], digits[101]), 1.3), run_time=0.7)

        # ============================================================ P4: noise, staircase, zoom out, the curve
        ledger3 = VGroup(l98, l99, l100, l101)
        self.at("p4", FadeOut(ledger3), run_time=0.5)
        # static: each tile flashes bright once (full fill + INK rim) and drops nearly dark once; the events are short
        # plateaus spread over the clause so that about 5-8 tiles are mid-flash at any moment
        rng = np.random.default_rng(3)
        NOISE_T, RISE, HOLD = 1.4, 0.05, 0.2
        FL = 2 * RISE + HOLD
        passes = [rng.permutation(len(LIT)), rng.permutation(len(LIT))]

        def bump(t, t0):
            u = t - t0
            if u <= 0 or u >= FL:
                return 0.0
            return min(1.0, u / RISE, (FL - u) / RISE)

        def flicker(tile, i):
            t1 = 0.02 + passes[0][i] / len(LIT) * 0.55          # event 1 starts in [0.02, 0.57] s
            t2 = 0.64 + passes[1][i] / len(LIT) * 0.42          # event 2 starts in [0.64, 1.06] s
            tb, td = (t1, t2) if i % 2 == 0 else (t2, t1)

            def f(m, a):
                t = a * NOISE_T
                hb, hd = bump(t, tb), bump(t, td)
                m.set_fill(opacity=0.55 + 0.45 * hb - 0.40 * hd)
                m.set_stroke(INK, width=3 * hb, opacity=hb)
            return UpdateFromAlphaFunc(tile, f, rate_func=linear)

        self.at("noise", *[flicker(tiles[n], i) for i, n in enumerate(LIT)], run_time=NOISE_T)

        # --- tiles become the 25 steps of the staircase up to 100
        X0 = 100.0
        Y0 = Ymax(X0)
        corners = staircase_points(X0)                         # (0,0),(2,0),(2,1),(3,1),...,(97,25),(100,25)
        sc = to_scene(corners[:, 0], corners[:, 1], X0, Y0)
        base_seg = Line(sc[0], sc[1], color=BLUE_P, stroke_width=4)
        step_h = (GY1 - GY0) / Y0
        pieces, onaxis = [], []
        for k, p in enumerate(PRIMES100):
            a, b, c = sc[1 + 2 * k], sc[2 + 2 * k], sc[3 + 2 * k]
            pieces.append((Rectangle(width=0.045, height=b[1] - a[1], stroke_width=0, fill_color=BLUE_P,
                                     fill_opacity=1).move_to((a + b) / 2),
                           Line(b, c, color=BLUE_P, stroke_width=4)))
            # move 1: tile p lands on the number line at x = p, as a one-step-high bar
            onaxis.append(RoundedRectangle(corner_radius=0.025, width=0.1, height=step_h, stroke_width=0,
                                           fill_color=BLUE_P, fill_opacity=0.85)
                          .move_to([a[0], GY0 + step_h / 2, 0]))
        axes = VGroup(Line([GX0, GY0, 0], [GX1 + 0.25, GY0, 0], color=NEUTRAL, stroke_width=3),
                      Line([GX0, GY0, 0], [GX0, GY1 + 0.15, 0], color=NEUTRAL, stroke_width=3))
        ticks = VGroup(*[Line([x, GY0 - 0.08, 0], [x, GY0 + 0.08, 0], color=NEUTRAL, stroke_width=3)
                         for x in (0.0, GX1)])
        zero_lab = N("0", 26, DIM).next_to([GX0, GY0, 0], DOWN, buff=0.18)

        xv = ValueTracker(2.0)   # log10 of the horizontal range

        def xlabels():
            X = 10 ** xv.get_value()
            g = VGroup()
            for frac, x in ((0.5, 0.0), (1.0, GX1)):
                v = int(round(frac * X))
                g.add(N(f"{v:,}", 26, DIM).move_to([x, GY0 - 0.36, 0]))
            return g

        def countlab():
            X = 10 ** xv.get_value()
            n = int(prime_pi([X])[0])
            end = to_scene([X], [n], X, Ymax(X))[0]
            g = VGroup(N(f"{n:,}", 30, BLUE_P), T("primes", 24, DIM)).arrange(RIGHT, buff=0.14)
            g[1].align_to(g[0], DOWN)
            return g.next_to(end, UP + LEFT, buff=0.12).shift(DOWN * 0.05)

        xl = xlabels()
        cl = countlab()
        rest = VGroup(*[digits[n] for n in range(1, 111)], tiles[101])
        # move 1 ("count"): the digits go, and every prime tile drops onto the number line at its own x = p
        self.at("count", FadeOut(rest), Create(axes), FadeIn(ticks), FadeIn(zero_lab), FadeIn(xl), Create(base_seg),
                *[Transform(tiles[p], onaxis[k]) for k, p in enumerate(PRIMES100)], run_time=0.68)

        # move 2 ("one step up per prime"): in order, each bar rises to its riser and draws its tread; the first steps
        # (2, 3, 5, 7) go clearly one after another, later ones speed up; the build ends on 'and'.
        # The count ticks 1..25 as the risers land.
        BUILD = w("p4s2", "and") - w("p4s2", "one")
        RISE_T, TREAD_T = 0.2, 0.07
        gaps_s = [0.03 + 0.13 * np.exp(-k / 3.5) for k in range(len(PRIMES100) - 1)]
        starts = np.concatenate([[0.0], np.cumsum(gaps_s)])
        starts *= (BUILD - RISE_T - TREAD_T) / starts[-1]
        land = [(s + RISE_T) / BUILD for s in starts]
        cnt4 = ValueTracker(0.0)
        cl_right = cl.get_right()

        def ticklab():
            n = sum(1 for f in land if f <= cnt4.get_value() + 1e-9)
            g = VGroup(N(f"{max(n, 1)}", 30, BLUE_P), T("prime" if n == 1 else "primes", 24, DIM))
            g.arrange(RIGHT, buff=0.14)
            g[1].align_to(g[0], DOWN)
            g.move_to(cl, coor_mask=[0, 1, 0]).align_to(cl_right, RIGHT)
            return g.set_opacity(1.0 if n else 0.0)

        tick = ticklab()
        tick.add_updater(lambda m: m.become(ticklab()))
        self.add(tick)
        def step_rf(k, frac0, frac1):
            a0, a1 = (starts[k] + frac0) / BUILD, (starts[k] + frac1) / BUILD
            return lambda t: min(1.0, max(0.0, (t - a0) / (a1 - a0)))

        steps = []
        for k, p in enumerate(PRIMES100):
            r_rise = step_rf(k, 0.0, RISE_T)
            r_tread = step_rf(k, RISE_T, RISE_T + TREAD_T)
            steps.append(ReplacementTransform(tiles[p], pieces[k][0], rate_func=lambda t, r=r_rise: smooth(r(t))))
            steps.append(Create(pieces[k][1], rate_func=r_tread))
        self.at(w("p4s2", "one"), *steps, cnt4.animate(rate_func=linear).set_value(1.0), run_time=BUILD)
        tick.clear_updaters()
        self.remove(tick)
        self.add(cl)
        self.until("back")              # hold the finished staircase to 100 with '25 primes' for a beat

        stair = VMobject(stroke_color=BLUE_P, stroke_width=4)
        stair.set_points_as_corners(sc)
        self.remove(base_seg, *[m for pc in pieces for m in pc])
        self.add(stair)

        def upd_stair(m):
            X = 10 ** xv.get_value()
            pts = staircase_points(X)
            m.set_points_as_corners(to_scene(pts[:, 0], pts[:, 1], X, Ymax(X)))

        stair.add_updater(upd_stair)
        xl.add_updater(lambda m: m.become(xlabels()))
        cl.add_updater(lambda m: m.become(countlab()))
        self.until("blur", xv.animate.set_value(5.0))
        for m in (stair, xl, cl):
            m.clear_updaters()

        XF, YF = 1e5, Ymax(1e5)

        # --- magnifier at 50,000: the tiny exact steps
        x50 = 50000.0
        P1 = to_scene([x50], prime_pi([x50]), XF, YF)[0]
        C1, R1, k1 = np.array([-3.3, 1.55, 0.0]), 1.2, 220.0
        half = R1 / k1 * XF / (GX1 - GX0) * 1.2
        pr = [int(p) for p in primes_upto(int(x50 + half) + 1) if p > x50 - half]
        c0 = int(prime_pi([x50 - half])[0])
        cs = [(x50 - half, c0)]
        for i, p in enumerate(pr):
            cs += [(p, c0 + i), (p, c0 + i + 1)]
        cs.append((x50 + half, c0 + len(pr)))
        cs = np.array(cs, float)
        z1 = C1 + k1 * (to_scene(cs[:, 0], cs[:, 1], XF, YF) - P1)
        mag1 = magnifier(P1, C1, R1, clipped(z1, C1, R1 * 0.97, BLUE_P, 4))
        self.at("blur", Create(mag1.small), Create(mag1.conns), FadeIn(mag1.disc, scale=0.3),
                FadeIn(mag1.content, scale=0.3), FadeIn(mag1.rim, scale=0.3), run_time=0.6)

        # --- the smooth curve (Gauss's li), drawn from the origin along the blue line
        xs = np.concatenate([np.linspace(2, 200, 60), np.geomspace(200, 1e5, 240)[1:]])
        # The staircase softens into a wide, faint blue halo and a full-strength teal line runs down its middle,
        # so at any resolution the viewer sees two things: the blurred staircase and the smooth curve inside it.
        curve = VMobject(stroke_color=TEAL_P, stroke_width=5).set_points_smoothly(to_scene(xs, li(xs), XF, YF))
        curve.set_z_index(2)
        CURVE_T = 1.9
        m_t0 = w("p4s3", "smooth") - self.t("curve")           # the magnifier stays open until 'smooth', then 0.4 s fade
        x70 = 70000.0
        on_line = to_scene([x70], li([x70]), XF, YF)[0]
        sc_lab = T("smooth curve", 26, TEAL_P)
        sc_lab.move_to(on_line + np.array([0.75, -0.75, 0]), aligned_edge=UL)
        lead_dir = sc_lab.get_corner(UL) + np.array([-0.06, 0.06, 0]) - on_line
        leader = Line(on_line + 0.2 * lead_dir / np.linalg.norm(lead_dir), sc_lab.get_corner(UL) + np.array([-0.06, 0.06, 0]),
                      color=NEUTRAL, stroke_width=2)
        sc_lab = VGroup(leader, sc_lab)
        l_t0 = w("p4s3", "follows") - self.t("curve")           # label fades in on 'follows'

        def window(t0, d):
            return lambda t: smooth(min(1.0, max(0.0, (t * CURVE_T - t0) / d)))

        self.at("curve", Create(curve, rate_func=smooth),
                stair.animate(run_time=CURVE_T).set_stroke(width=20, opacity=0.3),
                FadeOut(mag1, rate_func=window(m_t0, 0.4)), FadeIn(sc_lab, rate_func=window(l_t0, 0.5)),
                run_time=CURVE_T)
        # pause: both lines hold together

        # ============================================================ P5: how precise? Riemann 1859
        xc = 99830.0
        pic = float(prime_pi([xc])[0])
        lic = float(li([xc])[0])
        P2 = to_scene([xc], [(pic + lic) / 2], XF, YF)[0]
        C2, R2, k2 = np.array([3.55, -1.15, 0.0]), 1.35, 70.0
        half2 = R2 / k2 * XF / (GX1 - GX0) * 1.25
        pr2 = [int(p) for p in primes_upto(int(xc + half2) + 1) if p > xc - half2]
        c2 = int(prime_pi([xc - half2])[0])
        cs2 = [(xc - half2, c2)]
        for i, p in enumerate(pr2):
            cs2 += [(p, c2 + i), (p, c2 + i + 1)]
        cs2.append((xc + half2, c2 + len(pr2)))
        cs2 = np.array(cs2, float)
        zs = C2 + k2 * (to_scene(cs2[:, 0], cs2[:, 1], XF, YF) - P2)
        xl2 = np.linspace(xc - half2, xc + half2, 40)
        zl = C2 + k2 * (to_scene(xl2, li(xl2), XF, YF) - P2)
        in_stair = clipped(zs, C2, R2 * 0.97, BLUE_P, 4)
        in_curve = clipped(zl, C2, R2 * 0.97, TEAL_P, 4)
        ya = C2[1] + k2 * (to_scene([xc], [pic], XF, YF)[0][1] - P2[1])
        yb = C2[1] + k2 * (to_scene([xc], [lic], XF, YF)[0][1] - P2[1])
        bx = C2[0]
        bracket = VGroup(Line([bx, ya + 0.06, 0], [bx, yb - 0.06, 0], color=ACCENT, stroke_width=3),
                         Line([bx - 0.1, ya + 0.06, 0], [bx + 0.1, ya + 0.06, 0], color=ACCENT, stroke_width=3),
                         Line([bx - 0.1, yb - 0.06, 0], [bx + 0.1, yb - 0.06, 0], color=ACCENT, stroke_width=3))
        mag2 = magnifier(P2, C2, R2, VGroup(in_stair, in_curve, bracket))
        gap_lab = VGroup(T("how big", 24, DIM), T("is this gap?", 24, DIM)).arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        gap_lab.next_to(mag2.rim, LEFT, buff=0.3).set_y(C2[1] - 0.2)
        self.at("p5", FadeOut(sc_lab), cl.animate.shift(LEFT * 0.4 + DOWN * 0.05), Create(mag2.small), Create(mag2.conns), FadeIn(mag2.disc, scale=0.3),
                FadeIn(VGroup(in_stair, in_curve), scale=0.3), FadeIn(mag2.rim, scale=0.3), run_time=0.75)
        self.at(w("p5s1", "precise"), GrowFromCenter(bracket), FadeIn(gap_lab, shift=RIGHT * 0.15), run_time=0.6)

        title = T("The Riemann Hypothesis", 44, INK).move_to([0, 3.3, 0])
        self.at("precise", Write(title), FadeOut(cl), run_time=1.0)   # the title takes over the top edge

        # the dimmed half-size graph keeps no text (it would be far below readable size): axes, the two lines and the
        # magnifier with its gold bracket stay as a silent reminder of 'the gap'
        graph = VGroup(axes, ticks, stair, curve, mag2)
        target = dimmed(graph).scale(0.5).move_to([-3.35, 0.0, 0])
        graph_text = VGroup(zero_lab, xl, gap_lab)      # cl already faded out on 'precise'
        paper = RoundedRectangle(corner_radius=0.08, width=1.0, height=1.3, stroke_color=NEUTRAL, stroke_width=2.5,
                                 fill_color=BG, fill_opacity=1)
        lines_ = VGroup(*[Line(LEFT * 0.33, RIGHT * (0.33 if i % 3 != 2 else 0.1), color=DIM, stroke_width=2,
                               stroke_opacity=0.7) for i in range(8)]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        lines_.move_to(paper)
        icon = VGroup(paper, lines_).move_to([1.75, 1.35, 0])
        facts5 = VGroup(N("1859", 44, ACCENT), T("Berlin Academy", 24, DIM), T("about 8 pages", 24, DIM))
        facts5.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(icon, RIGHT, buff=0.4)
        # the graph clears the right half in the first 0.75 s; the card fades in only after that has mostly happened
        def win(a0, a1):
            return lambda t: smooth(min(1.0, max(0.0, (t - a0) / (a1 - a0))))

        self.at("riemann", FadeOut(title, rate_func=win(0.0, 0.6)), FadeOut(graph_text, rate_func=win(0.0, 0.5)),
                Transform(graph, target, rate_func=win(0.0, 0.75)),
                FadeIn(icon, shift=LEFT * 0.2, rate_func=win(0.4, 1.0)),
                FadeIn(facts5[0], shift=LEFT * 0.2, rate_func=win(0.4, 1.0)), run_time=1.1)
        self.play(FadeIn(facts5[1:], shift=LEFT * 0.1), run_time=0.5)
        name = T("Bernhard Riemann", 36, INK).move_to([3.55, -0.2, 0])
        self.at(w("p5s2", "bernhard"), Write(name), run_time=0.8)
        sehr = T("“sehr wahrscheinlich”", 30, ACCENT, slant=ITALIC).move_to([3.55, -1.35, 0])
        vp = T("very probable", 24, DIM).next_to(sehr, DOWN, buff=0.18)
        self.at("probable", FadeIn(sehr, shift=UP * 0.15), run_time=0.42)
        self.at(w("p5s2", "very"), FadeIn(vp, shift=UP * 0.1), run_time=0.5)

        # ============================================================ P6: prize, checks, no proof
        self.at("p6", FadeOut(graph), FadeOut(icon), FadeOut(facts5), FadeOut(name), FadeOut(sehr), FadeOut(vp),
                run_time=0.75)
        prize = N("$1,000,000", 60, ACCENT).move_to([0, 2.45, 0])
        clay = T("Clay Millennium Prize", 28, DIM).next_to(prize, DOWN, buff=0.2)
        self.at("prize", FadeIn(prize, scale=0.8), run_time=0.6)
        self.play(FadeIn(clay, shift=UP * 0.1), run_time=0.5)

        cv = ValueTracker(0.0)
        TARGET = 12_000_000_000_000
        cy = 0.2

        def counter():
            a = cv.get_value()
            v = int(round(TARGET * (10 ** (4 * a) - 1) / (10 ** 4 - 1)))
            return N(f"{v:,}", 48, INK).move_to([0, cy, 0])

        cnt = counter()
        cnt.add_updater(lambda m: m.become(counter()))
        final = N(f"{TARGET:,}+", 48, INK).move_to([0, cy, 0])
        chk = check_mark(final.get_right() + RIGHT * 0.5, size=0.2)
        passed = VGroup(T("checks", 24, DIM), T("·  all passed", 24, DIM)).arrange(RIGHT, buff=0.18)
        passed[1].align_to(passed[0], DOWN)
        passed.next_to(final, DOWN, buff=0.25)
        self.until("checked")
        self.add(cnt)
        # the roll starts on 'more' and ends on 'trillion'; the final figure is complete by 'times'
        self.until(w("p6s2", "trillion"), cv.animate(rate_func=linear).set_value(1.0), FadeIn(passed[0], shift=UP * 0.1))
        cnt.clear_updaters()
        self.until(w("p6s2", "times"), Transform(cnt, final))
        self.at(w("p6s2", "never"), Create(chk), FadeIn(passed[1], shift=UP * 0.1), run_time=0.6)

        proof = T("proof", 32, DIM)
        box = Square(0.62, color=NEUTRAL, stroke_width=3)
        prow = VGroup(proof, box).arrange(RIGHT, buff=0.35).move_to([0, -2.1, 0])
        self.at("never", FadeIn(proof, shift=UP * 0.1), run_time=0.5)
        self.at(w("p6s3", "proved"), Create(box), run_time=0.6)

        self.until("p6_end")
        self.until("end", FadeOut(VGroup(prize, clay, cnt, chk, passed, prow)))

