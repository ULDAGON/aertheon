"""S04_Zeta: Euler's bridge.

Beats (all synced to timeline/S04_Zeta.json; word-level beats use self.w(sentence, word)):
  p1  'Riemann's tool' caption; an input box 's = [ ]'; the row 1 + 1/2ˢ + 1/3ˢ + ... writes in word by word
  p2  s = 2: the row becomes 1 + 1/4 + 1/9 + ..., a bar of coloured segments (one per term, same colour as its term)
      settles on the π²/6 tick (readouts 10 / 100 / 1,000 terms, exact); s = 1: a second bar runs off the frame
      (2.93, 5.19, 7.49, 14.39 at a million terms) and '... forever'
  p3  Euler · 1737; the row becomes 30 tiles 1 .. 1/30ˢ; factor (1 − 1/2ˢ) joins a column on the left, the one-line
      reason flashes above, the even tiles flash blue and fade; (1 − 1/3ˢ) removes 3, 9, 15, 21, 27
  p4  the other prime factors up to 29 remove their tiles (sieve of Eratosthenes); only '1' survives; the display
      condenses to (1 − 1/2ˢ)(1 − 1/3ˢ)(1 − 1/5ˢ)⋯ × (1 + 1/2ˢ + ...) = 1; undoing: every factor lifts off, crosses the
      '=' and lands as the denominator of its reciprocal: 1 + 1/2ˢ + 1/3ˢ + ⋯ = 1/(1 − 1/2ˢ) × ... (s > 1)
  p5  the left side collapses into ζ(s); a bridge arcs from 1 2 3 4 5 6 … to 2 3 5 7 11 … under the formula; fade out
Everything exact: partial sums computed here with numpy (match the storyboard's values); the tile removals are
computed (each prime removes exactly the surviving multiples of itself).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

SUP = "ˢ"
LATE = lambda t: smooth(float(np.clip((t - 0.55) / 0.45, 0, 1)))   # noqa: E731  (last 45% of a play)
EARLY = lambda t: smooth(float(np.clip(t / 0.35, 0, 1)))          # noqa: E731  (first 35% of a play)
TILE_FILL = "#1A202B"


# ---------------------------------------------------------------- local helpers
def chunks(parts, size, color=INK, font=NUM_FONT):
    """One Text (shared baseline) sliced into a VGroup of per-part glyph groups."""
    t = Text("".join(parts), font=font, font_size=size, color=color)
    out, i = VGroup(), 0
    for p in parts:
        n = sum(1 for c in p if not c.isspace())
        out.add(VGroup(*t.submobjects[i:i + n]))
        i += n
    assert i == len(t.submobjects), (parts, i, len(t.submobjects))
    return out


def row_parts(kind):
    """Chunks of the sum row: 'gen' (1/nˢ), 2 (1/n²-values), 1 (1/n)."""
    parts = []
    for n in range(1, 7):
        if n > 1:
            parts.append(" + ")
        if n == 1:
            parts.append("1")
        elif kind == "gen":
            parts.append(f"1/{n}{SUP}")
        elif kind == 2:
            parts.append(f"1/{n * n}")
        else:
            parts.append(f"1/{n}")
    parts += [" + ", "…"]
    return parts


def term_color(n):
    """Colour of the n-th term of the sum and of its bar segment. Cycles PALETTE without blue (blue means 'prime' in
    this video) and without yellow (too close to the ACCENT π²/6 target the bar runs toward)."""
    return PALETTE[2 + (n - 1) % 5]


def factor_color(i):
    """Colour of the i-th prime factor (2, 3, 5, ...): 2 is blue as the storyboard asks; the cycle for the later
    primes skips blue so no second 'blue' factor appears."""
    return PALETTE[0] if i == 0 else PALETTE[1 + (i - 1) % 6]


def term_ids():
    """Indices of the 6 terms inside row_parts (0, 2, 4, ...); the '…' is the last part."""
    return [0, 2, 4, 6, 8, 10]


class S04_Zeta(TimedScene):
    def construct(self):
        self.p1_sum()
        self.p2_values()
        self.p3_euler()
        self.p4_sieve_and_product()
        self.p5_zeta()

    # ------------------------------------------------------------ word times
    def w(self, sid, word, nth=0):
        key = word.lower()
        for s in self.tl["sentences"]:
            if s["id"] == sid:
                hits = [x["s"] for x in s["words"] if re.sub(r"[^\w'-]", "", x["w"]).lower() == key]
                if len(hits) > nth:
                    return hits[nth]
                raise KeyError(f"word {word!r} #{nth} not in {sid}: {s['text']!r}")
        raise KeyError(f"unknown sentence {sid!r}")

    def make_row(self, kind, y, size=34):
        r = chunks(row_parts(kind), size)
        r.move_to([0, y, 0])
        return r

    # ============================================================ p1: pick s, add 1 + 1/2ˢ + ...
    def p1_sum(self):
        tool = T("Riemann's tool", 28, DIM).move_to([0, 3.15, 0])
        self.until(self.t("p1") + 0.6, FadeIn(tool, shift=DOWN * 0.1))
        self.at(self.w("p1s1", "tool") + 0.3, FadeOut(tool), run_time=0.5)

        # {#pick}: input box, top left
        lab = N("s =", 36, INK)
        slot = RoundedRectangle(corner_radius=0.1, width=0.78, height=0.64, stroke_color=DIM, stroke_width=2.5)
        box = VGroup(lab, slot).arrange(RIGHT, buff=0.2)
        box.to_corner(UL, buff=0.55)
        self.lab, self.slot, self.box = lab, slot, box
        self.at("pick", FadeIn(lab, shift=RIGHT * 0.15), Create(slot), run_time=0.6)
        self.at(self.w("p1s2", "s"), slot.animate(rate_func=there_and_back).set_stroke(ACCENT, 4), run_time=0.6)

        # {#terms}: the row writes in, term by term, with the words
        row = self.make_row("gen", 0.3)
        self.row = row
        self.at("terms", FadeIn(row[0], scale=0.8), run_time=0.35)
        self.at(self.w("p1s3", "plus"), FadeIn(row[1]), run_time=0.3)
        self.at(self.w("p1s3", "one", 1), Write(row[2]), run_time=0.95)
        self.at(self.w("p1s3", "plus", 1), FadeIn(row[3]), run_time=0.3)
        self.at(self.w("p1s3", "one", 2), Write(row[4]), run_time=0.95)
        rest = row[5:]
        self.at(self.w("p1s3", "forever"),
                LaggedStart(*[FadeIn(m, shift=RIGHT * 0.12) for m in rest], lag_ratio=0.25), run_time=1.0)

    # ============================================================ p2: s = 2 settles, s = 1 grows forever
    def slot_value(self, v):
        t = N(v, 36, ACCENT).move_to(self.slot)
        return t

    def bar(self, v, S, y, max_seg, colours=True):
        X0, K = self.X0, self.K
        g = VGroup()
        for n in range(1, max_seg + 1):
            a, b = S[n - 1], min(S[n], v)
            if b <= a:
                break
            xa, xb = X0 + K * a, min(X0 + K * b, 7.6)
            if xb - xa < 1e-4 or xa > 7.6:
                break
            r = Rectangle(width=xb - xa, height=0.24, stroke_width=0,
                          fill_color=term_color(n), fill_opacity=0.95)
            r.move_to([(xa + xb) / 2, y, 0])
            g.add(r)
        if v > S[max_seg]:
            xa, xb = X0 + K * S[max_seg], min(X0 + K * v, 7.6)
            if xb > xa + 1e-4:
                g.add(Rectangle(width=xb - xa, height=0.24, stroke_width=0, fill_color=DIM, fill_opacity=0.9)
                      .move_to([(xa + xb) / 2, y, 0]))
        return g

    TX = 1.9   # readout tables: 'N terms' right-aligned at TX, the value left-aligned just after it

    def readout(self, n_terms, value, y):
        """One row of a readout table. Rows stay on screen (older ones dim), so no value flashes by unread."""
        lab = T(f"{n_terms} terms", 24, DIM)
        val = N(value, 30, INK)
        lab.move_to([self.TX, y, 0], aligned_edge=RIGHT)
        val.next_to(lab, RIGHT, buff=0.3).align_to(lab, DOWN)
        return VGroup(lab, val)

    def p2_values(self):
        self.X0, self.K = -5.6, 2.4
        X0, K = self.X0, self.K
        n = np.arange(1, 1_000_001, dtype=float)
        S1 = np.concatenate([[0.0], np.cumsum(1 / n)])
        S2 = np.concatenate([[0.0], np.cumsum(1 / n[:1000] ** 2)])
        y1, y2 = 0.3, -1.55

        # the row moves up to make room for the bars
        self.at("p2", self.row.animate.move_to([0, 1.95, 0]), run_time=0.8)

        # "two": slot shows 2, row becomes 1 + 1/4 + 1/9 + ...
        v2 = self.slot_value("2")
        row2 = self.make_row(2, 1.95)
        self.at(self.w("p2s1", "two"), FadeIn(v2, scale=1.3),
                *[ReplacementTransform(a, b) for a, b in zip(self.row, row2)], run_time=0.6)
        self.row = row2

        # bar 1 furniture: origin tick, s = 2 label, the π²/6 target
        tick0 = Line([X0, y1 - 0.25, 0], [X0, y1 + 0.25, 0], color=NEUTRAL, stroke_width=3)
        lab1 = T("s = 2", 24, DIM).next_to([X0, y1 + 0.25, 0], UP, buff=0.12, aligned_edge=LEFT)
        lab1.align_to([X0, 0, 0], LEFT)
        xt = X0 + K * np.pi ** 2 / 6
        tgt = Line([xt, y1 - 0.32, 0], [xt, y1 + 0.32, 0], color=ACCENT, stroke_width=4)
        tgt_lab = N("π²/6 = 1.6449…", 28, ACCENT).next_to(tgt, UP, buff=0.12)
        euler35 = T("Euler · 1735", 24, DIM).move_to([0, y1 + 0.62, 0]).align_to([6.4, 0, 0], RIGHT)

        vt = ValueTracker(0.0)
        bar1 = always_redraw(lambda: self.bar(vt.get_value(), S2, y1, 40))
        self.add(bar1)
        r10 = self.readout("10", "1.5498", y1 + 0.38)
        r100 = self.readout("100", "1.6350", y1)
        r1000 = self.readout("1,000", "1.6439", y1 - 0.38)
        terms = [self.row[i] for i in term_ids()]
        # {#two}: the bar grows term by term (each segment has its term's colour) toward the π²/6 tick;
        # each table row arrives with its bar step and stays (the digits visibly settle: 1.5498, 1.6350, 1.6439)
        self.at("two", FadeIn(VGroup(tick0, lab1, tgt, tgt_lab, euler35)),
                vt.animate(rate_func=linear).set_value(S2[10]), FadeIn(r10, shift=UP * 0.1),
                LaggedStart(*[t.animate.set_color(term_color(i + 1)) for i, t in enumerate(terms)], lag_ratio=0.35),
                run_time=0.5)
        self.at(self.w("p2s1", "settles"), vt.animate.set_value(S2[100]), r10[1].animate.set_color(DIM),
                FadeIn(r100, shift=UP * 0.1), run_time=0.4)
        self.at(self.w("p2s1", "on"), vt.animate.set_value(S2[1000]), r100[1].animate.set_color(DIM),
                FadeIn(r1000, shift=UP * 0.1), run_time=0.4)
        self.at(self.w("p2s1", "squared") + 0.2, Indicate(VGroup(tgt, tgt_lab), color=ACCENT, scale_factor=1.12),
                run_time=0.9)
        bar1.clear_updaters()

        # "equal to one": slot shows 1, row becomes 1 + 1/2 + 1/3 + ...
        v1 = self.slot_value("1")
        row1 = self.make_row(1, 1.95)
        for i, t in enumerate([row1[j] for j in term_ids()]):
            t.set_color(term_color(i + 1))
        self.at(self.w("p2s2", "equal"), ReplacementTransform(v2, v1),
                *[ReplacementTransform(a, b) for a, b in zip(self.row, row1)], run_time=0.4)
        self.row = row1

        tick0b = tick0.copy().move_to([X0, y2, 0])
        lab2 = T("s = 1", 24, DIM).next_to([X0, y2 + 0.25, 0], UP, buff=0.12).align_to([X0, 0, 0], LEFT)
        vu = ValueTracker(0.0)
        bar2 = always_redraw(lambda: self.bar(vu.get_value(), S1, y2, 130))
        self.add(bar2)
        q = [self.readout(a, b, y2 - 0.58 - 0.38 * i) for i, (a, b) in
             enumerate((("10", "2.93"), ("100", "5.19"), ("1,000", "7.49"), ("1,000,000", "14.39")))]
        forever = T("… forever", 26, DIM).next_to(q[3], RIGHT, buff=0.35)
        # 'one' .. 'forever' and the pause: the second bar grows in calm steps (10 -> 100 -> 1,000 -> 1,000,000 terms)
        # and runs off the frame's right edge; each table row lands with its step and stays
        self.at(self.w("p2s2", "one"), FadeIn(VGroup(tick0b, lab2)), FadeIn(q[0], shift=UP * 0.1),
                vu.animate(rate_func=smooth).set_value(S1[10]), run_time=0.45)
        self.at("one", vu.animate(rate_func=smooth).set_value(S1[100]), q[0][1].animate.set_color(DIM),
                FadeIn(q[1], shift=UP * 0.1), run_time=0.45)
        self.at(self.w("p2s2", "forever"), vu.animate(rate_func=smooth).set_value(S1[1000]),
                q[1][1].animate.set_color(DIM), FadeIn(q[2], shift=UP * 0.1), run_time=0.45)
        self.at(self.w("p2s2", "forever") + 0.55, vu.animate(rate_func=smooth).set_value(S1[1_000_000]),
                q[2][1].animate.set_color(DIM), FadeIn(q[3], shift=UP * 0.1),
                FadeIn(forever, shift=RIGHT * 0.2, rate_func=LATE), run_time=0.6)
        bar2.clear_updaters()
        self.p2_stuff = VGroup(bar1, bar2, tick0, tick0b, lab1, lab2, tgt, tgt_lab, euler35, r10, r100, r1000, *q,
                               forever, self.box, v1)

    # ============================================================ p3: Euler 1737, the tiles, (1 − 1/2ˢ), (1 − 1/3ˢ)
    def col_pos(self, j, n):
        """Home of factor j in a column of n factors: right-aligned against the '×', centred on the × row (y = 0)."""
        return np.array([self.FX_RIGHT, 0.21 * (n - 1) - 0.42 * j, 0])

    def place_factor(self, f, j, n):
        f.move_to(self.col_pos(j, n), aligned_edge=RIGHT)
        return f

    def p3_euler(self):
        euler = T("Euler · 1737", 24, DIM).to_corner(UL, buff=0.55)
        gen = self.make_row("gen", 1.95)
        self.at("euler", FadeOut(self.p2_stuff), FadeIn(euler, shift=DOWN * 0.1),
                *[ReplacementTransform(a, b) for a, b in zip(self.row, gen)], run_time=1.0)
        self.row = gen
        self.euler = euler

        # {#bridge}: the row becomes 30 tiles, three rows of ten (wide pitch so neighbouring labels stay apart)
        self.GX0, self.PX, self.GY = -3.55, 1.06, [0.8, 0.0, -0.8]
        tiles = {}
        for k in range(1, 31):
            r, c = divmod(k - 1, 10)
            pos = np.array([self.GX0 + c * self.PX, self.GY[r], 0])
            box = RoundedRectangle(corner_radius=0.09, width=0.98, height=0.6, stroke_width=0,
                                   fill_color=TILE_FILL, fill_opacity=1).move_to(pos)
            txt = N("1" if k == 1 else f"1/{k}{SUP}", 26, INK).move_to(pos)
            tiles[k] = VGroup(box, txt)
        self.tiles = tiles
        grid = VGroup(*tiles.values())
        self.grid_center = grid.get_center()
        # z-order is fixed BEFORE the play: the moving terms are drawn above the boxes fading in under them
        for k in range(1, 31):
            tiles[k][0].set_z_index(0)
            tiles[k][1].set_z_index(1)
        for i in term_ids():
            self.row[i].set_z_index(1)
        moves = [ReplacementTransform(self.row[i], tiles[j + 1][1]) for j, i in enumerate(term_ids())]
        others = [self.row[i] for i in range(len(self.row)) if i not in term_ids()]
        # the boxes start a moment after the terms, so the eye follows the terms down into the grid
        self.at("bridge", *moves, *[FadeOut(m) for m in others],
                Succession(Wait(0.25), LaggedStart(*[FadeIn(tiles[k][0]) for k in range(1, 31)], lag_ratio=0.04,
                                                   run_time=1.05)),
                Succession(Wait(0.6), LaggedStart(*[FadeIn(tiles[k][1], scale=0.8) for k in range(7, 31)],
                                                  lag_ratio=0.06, run_time=0.7)),
                run_time=1.3)

        # the factor column on the left, a '×' between it and the tiles; each factor joins on the × row
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        self.FX_RIGHT = -4.72
        self.fcol = {}
        for i, p in enumerate(self.primes):
            self.fcol[p] = chunks(["(", f"1 − 1/{p}{SUP}", ")"], 28, factor_color(i))
        times = T("×", 36, DIM).move_to([-4.42, 0, 0])
        self.times = times
        self.alive = set(range(1, 31))

        # {#factor}: (1 − 1/2ˢ) sits on the × row: 'multiply the sum by this'
        self.place_factor(self.fcol[2], 0, 1)
        self.at("factor", FadeIn(self.fcol[2], shift=RIGHT * 0.3), FadeIn(times), run_time=0.7)
        # the whole step in one line, above the tiles: the minus is what removes the evens
        reason = chunks([f"(1 − 1/2{SUP})", " × sum = sum − ", f"(1/2{SUP} + 1/4{SUP} + 1/6{SUP} + …)"], 26, INK)
        reason[0].set_color(PALETTE[0])
        reason.move_to([self.grid_center[0], 1.75, 0])
        self.at(self.w("p3s2", "two") - 0.1, FadeIn(reason, shift=DOWN * 0.1), run_time=0.6)
        # {#evens}: the subtracted evens get the same neutral highlight as the even tiles, then the tiles fade
        evens = [k for k in range(2, 31, 2)]
        hl = SurroundingRectangle(reason[2], buff=0.08, corner_radius=0.08, stroke_color=PALETTE[0], stroke_width=2.5,
                                  fill_color=NEUTRAL, fill_opacity=0.18)
        self.at("evens", FadeIn(hl), *[self.flash(k, PALETTE[0]) for k in evens], run_time=0.6)
        self.at(self.w("p3s2", "drops"), *[self.dim(k) for k in evens], run_time=0.7)
        self.alive -= set(evens)
        self.play(FadeOut(VGroup(reason, hl), shift=UP * 0.1), run_time=0.5)

        # "Then three": the column re-centres on the × row as (1 − 1/3ˢ) joins; {#threes}: 3, 9, 15, 21, 27 go
        self.place_factor(self.fcol[3], 1, 2)
        self.at(self.w("p3s3", "three"), FadeIn(self.fcol[3], shift=RIGHT * 0.3),
                self.fcol[2].animate.move_to(self.col_pos(0, 2), aligned_edge=RIGHT), run_time=0.5)
        th = sorted(k for k in self.alive if k % 3 == 0)
        self.at("threes", *[self.flash(k, YELLOW_P) for k in th], run_time=0.55)
        self.at(self.w("p3s3", "drop"), *[self.dim(k) for k in th], run_time=0.7)
        self.alive -= set(th)
        # pause: the survivors 1, 5, 7, 11, ... wait
        self.survivor_check = sorted(self.alive)

    def flash(self, k, color):
        """A tile about to be removed: neutral highlight fill, outline in the colour of the factor removing it
        (never a coloured fill: blue fills would read as 'prime' in this video)."""
        box, txt = self.tiles[k]
        return AnimationGroup(box.animate.set_fill(NEUTRAL, 0.3).set_stroke(color, 3),
                              txt.animate.set_color(INK).scale(1.08))

    def dim(self, k):
        box, txt = self.tiles[k]
        return AnimationGroup(box.animate.set_fill(TILE_FILL, 0.35).set_stroke(width=0),
                              txt.animate.set_color(FAINT).scale(1 / 1.08))

    # ============================================================ p4: the sieve, the lone '1', undo the product
    def frac(self, j):
        p = (2, 3, 5)[j]
        den = chunks([f"1 − 1/{p}{SUP}"], 30, PALETTE[j])[0]
        num = N("1", 30)
        bar = Line(LEFT, RIGHT, stroke_width=2.5, color=INK)
        bar.width = den.width + 0.14
        num.next_to(bar, UP, buff=0.1)
        den.next_to(bar, DOWN, buff=0.1)
        g = VGroup(num, bar, den)
        g.num, g.bar, g.den = num, bar, den
        return g

    def stage(self, k):
        """The equation after k factors have crossed the '=' (k = 3: 2, 3, 5 crossed; k = 4: the '⋯' too).
        Every stage is a true equation: (remaining factors) × (sum) = product of the reciprocals that crossed.
        Returns {tag: mobject}; the whole line is centred at x = 0 with the '=' at height Y_EQ."""
        sum_s = f"1 + 1/2{SUP} + 1/3{SUP} + ⋯"
        parts, tags = [], []
        for j in range(k, 3):
            parts += ["(", f"1 − 1/{(2, 3, 5)[j]}{SUP}", ")"]
            tags += [("fo", j), ("f", j), ("fc", j)]
        if k <= 3:
            parts += [" ⋯ ", " × ", "(", sum_s, ")"]
            tags += ["dots", "x", "lb", "sum", "rb"]
        else:
            parts += [sum_s]
            tags += ["sum"]
        parts += [" = "]
        tags += ["eq"]
        if k == 0:
            parts += ["1"]
            tags += ["one"]
        left = chunks(parts, 30)
        d = dict(zip(tags, left))
        for j in range(k, 3):
            VGroup(d[("fo", j)], d[("f", j)], d[("fc", j)]).set_color(PALETTE[j])
        if "dots" in d:
            d["dots"].set_color(DIM)
        if "one" in d:
            d["one"].set_color(ACCENT)
        whole = VGroup(left)
        if k >= 1:
            right = VGroup()
            for j in range(min(k, 3)):
                if j:
                    d[("x", j)] = N("×", 30)
                    right.add(d[("x", j)])
                d[("fr", j)] = self.frac(j)
                right.add(d[("fr", j)])
            if k == 4:
                d[("x", 3)] = N("×", 30)
                d["dots"] = N("⋯", 30)
                right.add(d[("x", 3)], d["dots"])
            right.arrange(RIGHT, buff=0.28)
            right.next_to(d["eq"], RIGHT, buff=0.28)
            ey = d["eq"].get_center()[1]
            for m in right:
                c = m.bar.get_center()[1] if hasattr(m, "bar") else m.get_center()[1]
                m.shift(UP * (ey - c))
            whole.add(right)
        whole.shift(RIGHT * -whole.get_center()[0] + UP * (self.Y_EQ - d["eq"].get_center()[1]))
        return d

    @staticmethod
    def hop(h=-0.85):
        """Path for a factor crossing the '=': dip (h < 0: below the line), travel, rise into place."""
        def f(s, e, a):
            ax = smooth(float(np.clip((a - 0.22) / 0.56, 0, 1)))
            up = smooth(float(np.clip(min(a / 0.22, (1 - a) / 0.22), 0, 1)))
            return s + (e - s) * ax + np.array([0.0, h, 0.0]) * up
        return f

    def cross(self, d0, d1, k, run_time):
        """Play stage k -> k+1: factor k (or the '⋯' when k = 3) hops over the '=' and becomes a reciprocal."""
        anims, gone = [], []
        moving = {("f", k), ("fo", k), ("fc", k), "dots", "one", "x", "lb", "rb"} if k == 3 else \
            {("f", k), ("fo", k), ("fc", k), "one"}
        for tag, m in d0.items():
            if tag in d1 and tag not in moving:
                anims.append(ReplacementTransform(m, d1[tag]))
        if k < 3:
            fr = d1[("fr", k)]
            anims.append(ReplacementTransform(d0[("f", k)], fr.den, path_func=self.hop(), rate_func=linear))
            for tag, side in ((("fo", k), fr.den.get_left()), (("fc", k), fr.den.get_right())):
                anims.append(d0[tag].animate(path_func=self.hop(), rate_func=linear).move_to(side).set_opacity(0))
                gone.append(d0[tag])
            # new pieces appear only once the line has re-flowed, so they never sit on top of moving ones
            anims.append(GrowFromCenter(fr.bar, rate_func=LATE))
            if k == 0:   # the lone '1' becomes the numerator of the first reciprocal: never orphaned
                anims.append(ReplacementTransform(d0["one"], fr.num))
            else:
                anims += [FadeIn(fr.num, shift=DOWN * 0.15, rate_func=LATE), FadeIn(d1[("x", k)], rate_func=LATE)]
        else:
            # the '⋯' (all the other factors) leaves on the left and reappears at the far right: no long zip
            anims.append(FadeOut(d0["dots"], shift=DOWN * 0.3, rate_func=EARLY))
            anims.append(FadeIn(d1["dots"], shift=UP * 0.3, rate_func=LATE))
            anims.append(FadeIn(d1[("x", 3)], rate_func=LATE))
            anims += [FadeOut(d0[t], rate_func=EARLY) for t in ("x", "lb", "rb")]
        self.play(*anims, run_time=run_time)
        for m in gone:
            self.remove(m)

    def p4_sieve_and_product(self):
        assert self.survivor_check == [1, 5, 7, 11, 13, 17, 19, 23, 25, 29], self.survivor_check
        sieve_cap = T("like the sieve of Eratosthenes", 24, DIM).move_to([self.grid_center[0], -1.6, 0])
        n = len(self.primes)
        for i, p in enumerate(self.primes[2:], start=2):
            self.place_factor(self.fcol[p], i, n)
        steps = []
        for i, p in enumerate(self.primes[2:], start=2):
            hit = sorted(k for k in self.alive if k % p == 0)
            self.alive -= set(hit)
            col = factor_color(i)
            steps.append(Succession(
                FadeIn(self.fcol[p], shift=RIGHT * 0.3, run_time=0.35),
                AnimationGroup(*[self.flash(k, col) for k in hit], run_time=0.35),
                AnimationGroup(*[self.dim(k) for k in hit], run_time=0.4)))
        assert self.alive == {1}
        # {#sieve}: the column makes room, then factors 5, 7, 11, ..., 29 join, each removing its tiles
        self.at("sieve", FadeIn(sieve_cap, shift=UP * 0.1),
                *[self.fcol[p].animate.move_to(self.col_pos(i, n), aligned_edge=RIGHT) for i, p in enumerate((2, 3))],
                run_time=0.4)
        self.until(self.t("lone") - 0.15, LaggedStart(*steps, lag_ratio=0.28))

        # {#lone}: only '1' is left, glowing; the removed tiles fold away at once
        one_box, one_txt = self.tiles[1]
        dead = VGroup(*[self.tiles[k] for k in range(2, 31)])
        self.at("lone", one_box.animate.set_fill(ACCENT, 0.22).set_stroke(ACCENT, 3),
                one_txt.animate.set_color(ACCENT).scale(1.3),
                FadeOut(dead, scale=0.85), FadeOut(sieve_cap), run_time=0.45)

        # hold: the factor column, the '×' and the lone glowing '1' stay still through 'only the first term'.
        # 'survives': condense into one line (1 − 1/2ˢ)(1 − 1/3ˢ)(1 − 1/5ˢ) ⋯ × (1 + 1/2ˢ + 1/3ˢ + ⋯) = 1.
        # Factors 7..29 fade first (the '⋯' stands for them); 5, 3, 2 move one after another (the farthest-travelling
        # first) so they never overlap; the sum fades in where the tiles were (the sum WAS the grid); only the lone '1'
        # (the result) arcs above the line to the right of '=', which appears as it arrives.
        self.Y_EQ = 0.3
        st = [self.stage(k) for k in range(5)]
        d0 = st[0]
        f_moves = []
        for j, p in reversed(list(enumerate((2, 3, 5)))):
            f_moves.append(AnimationGroup(*[ReplacementTransform(self.fcol[p][q], d0[(tag, j)])
                                            for q, tag in enumerate(("fo", "f", "fc"))]))
        rest_f = VGroup(*[self.fcol[p] for p in self.primes[3:]])
        src = self.grid_center
        t0 = self.w("p4s1", "survives")
        cond_rt = self.t("p4s1_end") + 0.05 - t0
        self.at(t0, FadeOut(rest_f, rate_func=EARLY), FadeIn(d0["dots"], rate_func=LATE),
                LaggedStart(*f_moves, lag_ratio=0.3),
                FadeOut(self.times, rate_func=EARLY), FadeIn(d0["x"], rate_func=LATE),
                FadeIn(VGroup(d0["lb"], d0["sum"], d0["rb"]), target_position=src, scale=0.6),
                FadeOut(one_box, rate_func=EARLY),
                ReplacementTransform(one_txt, d0["one"], path_arc=-0.6),
                FadeIn(d0["eq"], rate_func=LATE), run_time=cond_rt)
        # '= 1' gets a small nod in the pause just before 'Undo'
        self.until("product", Indicate(VGroup(d0["eq"], d0["one"]), color=ACCENT, scale_factor=1.15))

        # {#product} "Undo those multiplications": one factor at a time dips under the line, crosses the '=' and
        # rises into place as the denominator of its reciprocal (never through its own numerator or bar).
        # Every in-between frame is a true equation.
        self.at("product")
        self.cross(st[0], st[1], 0, 0.85)
        self.at(self.w("p4s2", "multiplications") + 0.2)
        self.cross(st[1], st[2], 1, 0.8)
        self.cross(st[2], st[3], 2, 0.8)
        self.at(self.now + 0.1)
        self.cross(st[3], st[4], 3, self.left(self.w("p4s2", "numbers")))
        d4 = st[4]

        fr = [d4[("fr", j)] for j in range(3)]
        xs = [d4[("x", j)] for j in (1, 2, 3)]
        sumP, eqP, dotsP = d4["sum"], d4["eq"], d4["dots"]
        P = VGroup(sumP, eqP, *fr, *xs, dotsP)
        self.P, self.fr, self.sumP, self.eqP, self.xs, self.dotsP = P, fr, sumP, eqP, xs, dotsP

        # labels as they are spoken
        right = VGroup(*fr, *xs, dotsP)
        ylab = right.get_bottom()[1] - 0.35
        lab_all = T("all whole numbers", 24, DIM).move_to([sumP.get_center()[0], ylab, 0])
        lab_pr = T("only primes", 24, DIM).move_to([right.get_center()[0], ylab, 0])
        self.lab_all, self.lab_pr = lab_all, lab_pr
        self.at(self.w("p4s2", "numbers"), FadeIn(lab_all, shift=UP * 0.1), run_time=0.6)
        self.at(self.w("p4s2", "built"),
                LaggedStart(*[Indicate(g.den, color=PALETTE[j], scale_factor=1.12) for j, g in enumerate(fr)],
                            lag_ratio=0.25), run_time=0.55)
        self.at(self.w("p4s2", "primes"), FadeIn(lab_pr, shift=UP * 0.1), run_time=0.45)
        cond = N("s > 1", 24, DIM).next_to(P, UP, buff=0.5).align_to(P, RIGHT)
        self.cond = cond
        self.at(self.w("p4s2", "alone"), FadeIn(cond, shift=DOWN * 0.1), run_time=0.6)

    # ============================================================ p5: zeta knows the primes
    def p5_zeta(self):
        # 'named': clear the side labels first so the {#zeta} beat has the stage to itself
        self.at(self.w("p5s1", "named"), FadeOut(self.lab_all), FadeOut(self.euler), run_time=0.4)
        zeta = N("ζ(s)", 48, INK)
        zeta.move_to(self.sumP).align_to(self.sumP, RIGHT)
        zword = T("zeta", 24, DIM).next_to(zeta, DOWN, buff=0.2)
        # {#zeta}: the left side collapses into ζ(s); the formula re-centres
        rest = VGroup(self.eqP, *self.fr, *self.xs, self.dotsP, self.lab_pr, self.cond)
        dx = -VGroup(zeta, rest).get_center()[0]
        zeta.shift(RIGHT * dx)
        zword.shift(RIGHT * dx)
        self.at("zeta", FadeTransform(self.sumP, zeta), FadeIn(zword, shift=UP * 0.1),
                rest.animate.shift(RIGHT * dx), run_time=0.8)

        # {#knows}: a bridge from all whole numbers to the primes, passing under the formula
        left = VGroup(*[N(t, 30, DIM) for t in "1 2 3 4 5 6 …".split()]).arrange(RIGHT, buff=0.22)
        right = VGroup(*[N(t, 30, PRIME_COLOR) for t in "2 3 5 7 11 …".split()]).arrange(RIGHT, buff=0.22)
        for g in (left, right):
            for m in g[:-1]:
                m.align_to(g[0], DOWN)
            g[-1].align_to(g[0], DOWN)
        left.move_to([-4.2, -2.3, 0])
        right.move_to([4.2, -2.3, 0])
        a = left.get_top() + UP * 0.15
        b = right.get_top() + UP * 0.15
        arc = ArcBetweenPoints(a, b, angle=-1.1, color=NEUTRAL, stroke_width=3)
        # the arc lands on 'the'; the primes arrive on 'primes' and the finished picture is held
        self.at("knows", FadeIn(left, shift=UP * 0.15), FadeOut(self.lab_pr), run_time=0.4)
        self.until(self.w("p5s1", "the"), Create(arc))
        self.at(self.w("p5s1", "primes"), FadeIn(right, shift=UP * 0.15),
                Indicate(zeta, color=ACCENT, scale_factor=1.1), run_time=0.4)

        # scene end: the finished picture holds until the last word ends, then fades through the whole final pause
        # (p5_end -> end, about 0.95 s, the same calm fade as the neighbouring scenes)
        everything = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)])
        self.at("p5_end")
        self.until("end", FadeOut(everything))

