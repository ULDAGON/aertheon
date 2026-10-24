"""S09_Evidence: 'very probable' was no wild guess. A roll call of the evidence, 1859 to 2026.

Layout (the dial sits at its home, so the camera never moves and everything else stays above y = -2.6):
  * left third: the critical strip in the EVIDENCE layout (topic.EVIDENCE). Its floor labels would sit under the
    dial's panel, so the real-part labels 0, 1/2, 1 go above the strip instead. The strip keeps the state of
    knowledge about the zeros: Hardy's shimmer, Riemann's two hand-computed zeros, the checked column, the share bar.
  * right two thirds: a NEUTRAL timeline at y = 2.8 (1850..2030). Each event gets an ACCENT dot at its year (DIM once
    the story moves on) and a card hanging from it. The area under the timeline is a 'stage' that holds only the
    current paragraph's card and props, so the roll call never piles up into clutter.

Facts (script/research_facts.md, review_facts.md): Hilbert 1900 problem 8 (of 23); Hardy 1914; Siegel 1932 found
Riemann's zeros 14.1386 and 25.31 (first and third zeros; the dots land at the true heights 14.13 and 25.01);
Platt and Trudgian 2021: every zero up to height 3e12 on the line, about 12.36 trillion zeros; Conrey 1989 > 40%,
record about 41.7% (2020); Alpoege and Furman 2026 preprint > 2/3 (67.25%).
The dense column in P4 is the first 1,000 real zeros (topic.ZEROS) squeezed into the strip, tagged 'illustration'
because the real check reaches far higher.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

M = EVIDENCE                        # strip x -6.4..-2.6, y -2.5..3.2, heights 0..50
M_ALL = EVIDENCE.with_hmax(1420)    # squeezed scale for the first 1,000 zeros (the 1000th is at 1419.4)
LINE_X = M.p(0.5, 0)[0]

TL_Y = 2.8                          # the timeline
TL_X0, TL_X1 = -1.9, 6.4
YEAR0, YEAR1 = 1850, 2030
CARD_TOP = 2.3

GLOW = "#FFF1C2"                    # a lighter ACCENT for the travelling shimmer


def yx(year):
    return TL_X0 + (TL_X1 - TL_X0) * (year - YEAR0) / (YEAR1 - YEAR0)


def win(total, start, dur, base=smooth):
    """Rate function for an animation inside a play of length `total` that runs from `start` for `dur` s."""
    s = start / total
    e = min(1.0, (start + dur) / total)

    def f(t):
        return base(float(np.clip((t - s) / max(e - s, 1e-6), 0.0, 1.0)))
    return f


# ------------------------------------------------------------------ builders
def event_dot(year):
    return Dot([yx(year), TL_Y, 0], radius=0.075, color=ACCENT).set_stroke(BG, 2, background=True).set_z_index(3)


def make_card(year, lines, side="left", top=CARD_TOP):
    """Text lines hanging from the year's dot on the timeline, plus the thin leader line."""
    g = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    x = yx(year)
    if side == "left":
        g.align_to(np.array([x - 0.3, 0, 0]), LEFT)
    else:
        g.align_to(np.array([TL_X1, 0, 0]), RIGHT)
    if g.get_right()[0] > TL_X1:
        g.shift(LEFT * (g.get_right()[0] - TL_X1))
    g.align_to(np.array([0, top, 0]), UP)
    leader = Line([x, TL_Y - 0.1, 0], [x, top + 0.1, 0], color=DIM, stroke_width=1.5)
    return g, leader


def paper_icon(center, w=0.95, h=1.25):
    body = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=NEUTRAL, stroke_width=2,
                            fill_color=BG, fill_opacity=1)
    fr = [0.72, 0.64, 0.72, 0.5, 0.68, 0.72, 0.6, 0.38]
    lines = VGroup(*[Line([-w / 2 + 0.14, 0, 0], [-w / 2 + 0.14 + f * (w - 0.28) / 0.72, 0, 0], color=DIM,
                          stroke_width=2) for f in fr])
    for i, ln in enumerate(lines):
        ln.shift(UP * (h / 2 - 0.2 - i * (h - 0.36) / 7))
    g = VGroup(body, lines).move_to(center)
    g.body, g.lines = body, lines
    return g


def scroll_icon(center, n=23):
    """Hilbert's list: a scroll with 23 faint lines in two columns (12 + 11)."""
    w, h = 2.1, 2.5
    body = Rectangle(width=w, height=h, stroke_color=NEUTRAL, stroke_width=2, fill_color=BG, fill_opacity=1)
    rolls = VGroup(*[RoundedRectangle(corner_radius=0.1, width=w + 0.3, height=0.2, stroke_color=NEUTRAL,
                                      stroke_width=2, fill_color=BG, fill_opacity=1).move_to([0, s * h / 2, 0])
                     for s in (1, -1)])
    lines = VGroup()
    rng = np.random.default_rng(3)
    for i in range(n):
        col, row = divmod(i, 12)
        x0 = -w / 2 + 0.28 + col * (w / 2)
        L = rng.uniform(0.5, 0.72)
        y = h / 2 - 0.3 - row * 0.172
        lines.add(Line([x0, y, 0], [x0 + L, y, 0], color=DIM, stroke_width=2, stroke_opacity=0.8))
    g = VGroup(body, rolls, lines).move_to(center)
    g.body, g.rolls, g.lines = body, rolls, lines
    return g


def notebook_icon(center, w=2.7, h=2.0):
    """Sketch of a notebook page with handwriting squiggles (illustration)."""
    page = Rectangle(width=w, height=h, stroke_color=NEUTRAL, stroke_width=2, fill_color=BG, fill_opacity=1)
    rings = VGroup(*[Circle(radius=0.05, color=DIM, stroke_width=1.5).move_to([-w / 2, h / 2 - 0.25 - k * 0.3, 0])
                     for k in range(6)])
    rng = np.random.default_rng(11)
    squig = VGroup()
    rows = 6
    for r in range(rows):
        y = h / 2 - 0.27 - r * (h - 0.5) / (rows - 1)
        L = w - 0.55 if r not in (1, 4) else 1.1       # rows 1 and 4 leave room for the written numbers
        xs = np.linspace(-w / 2 + 0.25, -w / 2 + 0.25 + L, 60)
        ys = y + 0.045 * np.sin(xs * rng.uniform(16, 22) + rng.uniform(0, 6)) * rng.uniform(0.7, 1.2)
        v = VMobject(stroke_color=DIM, stroke_width=1.6).set_points_smoothly([np.array([a, b, 0]) for a, b in zip(xs, ys)])
        squig.add(v)
    g = VGroup(page, rings, squig).move_to(center)
    g.page, g.rings, g.squig = page, rings, squig
    g.slot = [np.array([center[0] - w / 2 + 1.55, center[1] + h / 2 - 0.27 - r * (h - 0.5) / (rows - 1), 0])
              for r in (1, 4)]
    return g


def shimmer(n=3, gap=0.28, length=0.16):
    """n bright segments travelling up the critical line and out of the top (alpha 0..1)."""
    segs = VGroup(*[VMobject(stroke_color=GLOW, stroke_width=8).set_points_as_corners([M.p(0.5, 0), M.p(0.5, 0.01)])
                    for _ in range(n)])
    segs.set_stroke(opacity=0)

    def upd(m, a):
        for k, seg in enumerate(m):
            head = a * (1 + length + (n - 1) * gap) - k * gap
            lo, hi = float(np.clip(head - length, 0, 1)), float(np.clip(head, 0, 1))
            if hi - lo < 0.004:
                seg.set_stroke(opacity=0)
                continue
            seg.set_points_as_corners([M.p(0.5, lo * M.hmax), M.p(0.5, hi * M.hmax)])
            fade = min(1.0, (1 - lo) / 0.12)
            seg.set_stroke(GLOW, width=8, opacity=0.95 * fade)
    return segs, upd


class S09_Evidence(TimedScene):
    def construct(self):
        # ---------------------------------------------------------------- persistent parts
        dial = ErrorDial(best=True)
        strip = strip_group(M, 0, labels=False)
        top_labels = VGroup(*[N(t, 24, DIM).move_to([M.p(v, 0)[0], 3.43, 0]) for v, t in ((0, "0"), (0.5, "½"), (1, "1"))])

        tl_line = Line([TL_X0, TL_Y, 0], [TL_X1, TL_Y, 0], color=NEUTRAL, stroke_width=2)
        ticks, tlabs = VGroup(), VGroup()
        for yr in range(YEAR0, YEAR1 + 1, 10):
            big = yr % 50 == 0
            h = 0.12 if big else 0.07
            ticks.add(Line([yx(yr), TL_Y - h, 0], [yx(yr), TL_Y + h, 0], color=NEUTRAL if big else DIM,
                           stroke_width=2 if big else 1.5))
            if big:
                tlabs.add(N(str(yr), 24, DIM).move_to([yx(yr), TL_Y + 0.34, 0]))
        timeline = VGroup(tl_line, ticks, tlabs)

        # ================================================================ P1: Riemann's hint, Hilbert's list
        d1859 = event_dot(1859)
        r_card, r_lead = make_card(1859, [T("Riemann · 1859", 28, INK), T("1826 to 1866", 24, DIM)])
        paper = paper_icon([-1.35, 0.75, 0])
        quote = VGroup(T("his one hint:", 24, DIM),
                       T("“about as many zeros on the line", 28, INK, slant=ITALIC),
                       T("as expected”", 28, INK, slant=ITALIC)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        quote.next_to(paper, RIGHT, buff=0.4)
        hint_line = paper.lines[4]

        self.until(1.0, FadeIn(dial), FadeIn(strip), FadeIn(top_labels), FadeIn(timeline))
        self.until("hint", FadeIn(d1859, scale=0.4), Create(r_lead), FadeIn(r_card, shift=DOWN * 0.1), FadeIn(paper))
        self.play(hint_line.animate.set_stroke(ACCENT, width=4), FadeIn(quote, shift=RIGHT * 0.15), run_time=0.8)

        d1900 = event_dot(1900)
        h_card, h_lead = make_card(1900, [T("Hilbert · 1900", 28, INK)])
        riemann_stage = VGroup(r_card, r_lead, paper, quote)
        tot = 1.0
        self.at("hilbert",
                FadeOut(riemann_stage, rate_func=win(tot, 0, 0.5)),
                d1859.animate(rate_func=win(tot, 0, 0.5)).set_color(DIM),
                FadeIn(d1900, scale=0.4, rate_func=win(tot, 0.3, 0.5)),
                Create(h_lead, rate_func=win(tot, 0.35, 0.4)),
                FadeIn(h_card, shift=DOWN * 0.1, rate_func=win(tot, 0.45, 0.55)), run_time=tot)

        scroll = scroll_icon([1.05, 0.2, 0])
        lit = scroll.lines[7]
        p8 = VGroup(T("problem 8", 28, ACCENT), T("of 23", 24, DIM)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        p8.next_to(scroll, RIGHT, buff=0.35).set_y(lit.get_y())
        self.until("list", FadeIn(scroll.body), GrowFromCenter(scroll.rolls))
        self.play(LaggedStart(*[Create(l) for l in scroll.lines], lag_ratio=0.08), run_time=0.8)
        self.play(lit.animate.set_stroke(ACCENT, width=4.5, opacity=1), FadeIn(p8, shift=LEFT * 0.15), run_time=0.6)

        # ================================================================ P2: Hardy, infinitely many on the line
        d1914 = event_dot(1914)
        hd_card, hd_lead = make_card(1914, [T("Hardy · 1914", 28, INK)])
        hilbert_stage = VGroup(h_card, h_lead, scroll, p8)
        tot = 1.0
        self.at("hardy",
                FadeOut(hilbert_stage, rate_func=win(tot, 0, 0.5)),
                d1900.animate(rate_func=win(tot, 0, 0.5)).set_color(DIM),
                FadeIn(d1914, scale=0.4, rate_func=win(tot, 0.3, 0.5)),
                Create(hd_lead, rate_func=win(tot, 0.35, 0.4)),
                FadeIn(hd_card, shift=DOWN * 0.1, rate_func=win(tot, 0.45, 0.55)), run_time=tot)

        inf_lab = VGroup(T("proved: infinitely many", 28, INK), T("zeros on the line", 28, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        inf_lab.align_to(np.array([M.x1 + 0.35, 0, 0]), LEFT).set_y(1.1)
        arrow = Arrow(inf_lab.get_left() + LEFT * 0.08, [LINE_X + 0.12, inf_lab.get_y(), 0], buff=0.05, color=DIM,
                      stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
        open_lab = T("all of them? open", 24, DIM).next_to(inf_lab, DOWN, buff=0.28, aligned_edge=LEFT)
        segs, upd = shimmer()
        self.add(segs)
        t0 = self.t("p2s1") + 0  # shimmer runs on "proved infinitely many zeros sit on the line"
        start = 12.46
        tot = self.t("notall") - 0.2 - start
        self.at(start,
                UpdateFromAlphaFunc(segs, upd, rate_func=linear),
                strip.line.animate(rate_func=win(tot, 0.2, 1.2)).set_stroke(width=5),
                FadeIn(inf_lab, shift=RIGHT * 0.1, rate_func=win(tot, 0.5, 0.8)),
                GrowArrow(arrow, rate_func=win(tot, 0.9, 0.7)), run_time=tot)
        self.remove(segs)
        self.at("notall", FadeIn(open_lab, shift=DOWN * 0.1), run_time=0.7)

        # ================================================================ P3: Siegel finds Riemann's own zeros
        d1932 = event_dot(1932)
        s_card, s_lead = make_card(1932, [T("Siegel · 1932", 28, INK)])
        hardy_stage = VGroup(hd_card, hd_lead, inf_lab, arrow, open_lab)
        tot = 1.0
        self.at("siegel",
                FadeOut(hardy_stage, rate_func=win(tot, 0, 0.5)),
                strip.line.animate(rate_func=win(tot, 0, 0.5)).set_stroke(width=3),
                d1914.animate(rate_func=win(tot, 0, 0.5)).set_color(DIM),
                FadeIn(d1932, scale=0.4, rate_func=win(tot, 0.3, 0.5)),
                Create(s_lead, rate_func=win(tot, 0.35, 0.4)),
                FadeIn(s_card, shift=DOWN * 0.1, rate_func=win(tot, 0.45, 0.55)), run_time=tot)

        book = notebook_icon(np.array([2.6, 0.55, 0]))
        book_cap = T("Riemann's notes · sketch", 24, DIM).next_to(book, DOWN, buff=0.15)
        self.at("notes", FadeIn(book.page), Create(book.rings),
                LaggedStart(*[Create(s) for s in book.squig], lag_ratio=0.25),
                FadeIn(book_cap, rate_func=win(1.4, 0.6, 0.8)), run_time=1.4)

        vals = [("14.1386", 1), ("25.31", 3)]            # Riemann's values for the first and third zeros
        written = VGroup(*[N(v, 28, ACCENT, slant=ITALIC).move_to(book.slot[i]).align_to(book.slot[i] + LEFT * 0.0, LEFT)
                           for i, (v, _) in enumerate(vals)])
        self.at("hand", LaggedStart(*[Write(w) for w in written], lag_ratio=0.5), run_time=0.8)

        rdots = VGroup(*[Dot(written[i].get_left() + LEFT * 0.12, radius=0.08, color=ACCENT).set_stroke(BG, 2, background=True)
                         for i in range(2)])
        targets = [M.p(0.5, ZEROS[k - 1]) for _, k in vals]
        slabels = VGroup(*[N(v, 24, ACCENT).next_to(targets[i], RIGHT, buff=0.18) for i, (v, _) in enumerate(vals)])
        self.play(*[FadeIn(d, scale=0.4) for d in rdots], run_time=0.3)
        self.play(*[rdots[i].animate(path_arc=0.5).move_to(targets[i]) for i in range(2)],
                  *[TransformFromCopy(written[i], slabels[i], path_arc=0.5) for i in range(2)], run_time=1.1)
        self.until("p3s2_end", rdots.animate.set_color(INK), slabels.animate.set_color(DIM))

        sehr = VGroup(T("sehr wahrscheinlich", 30, ACCENT, slant=ITALIC), T("very probable", 24, DIM)).arrange(
            DOWN, buff=0.12)
        sehr.move_to([2.35, -1.55, 0])
        chk = check_mark(sehr[0].get_right() + RIGHT * 0.45, size=0.2)
        self.at("wild", FadeIn(sehr, shift=UP * 0.1), Indicate(d1859, color=ACCENT, scale_factor=1.8), run_time=0.8)
        self.play(Create(chk), run_time=0.5)

        # ================================================================ P4: Platt and Trudgian, 12 trillion
        d2021 = event_dot(2021)
        pt_card, pt_lead = make_card(2021, [T("Platt and Trudgian · 2021", 28, INK)], side="right")
        siegel_stage = VGroup(s_card, s_lead, book, book_cap, written, sehr, chk, slabels)
        tot = 0.9
        self.at("p4",
                FadeOut(siegel_stage, rate_func=win(tot, 0, 0.5)),
                d1932.animate(rate_func=win(tot, 0, 0.5)).set_color(DIM),
                FadeIn(d2021, scale=0.4, rate_func=win(tot, 0.3, 0.5)),
                Create(pt_lead, rate_func=win(tot, 0.4, 0.5)), run_time=tot)
        self.at("p4s1", run_time=0)
        self.at(32.12, FadeIn(pt_card, shift=DOWN * 0.1), run_time=0.9)

        cpos = np.array([2.3, 0.85, 0])
        v = ValueTracker(0.0)
        TARGET = 12e12

        def counter_text():
            e = v.get_value()
            n = 0 if e <= 0 else int(round(10 ** (e * np.log10(TARGET))))
            if e >= 1:
                n = int(TARGET)
            return N(f"{n:,}", 44, INK).move_to(cpos)
        counter = always_redraw(counter_text)
        checked = T("zeros checked", 24, DIM).move_to(cpos + DOWN * 0.6)
        height_tag = T("every zero up to height 3,000,000,000,000", 24, DIM).move_to(cpos + DOWN * 1.0)

        col = VGroup(*[Dot(M_ALL.p(0.5, h), radius=0.032, color=INK) for h in ZEROS[:1000]])
        col_a, col_b = col[:420], col[420:]
        illus = T("illustration", 24, DIM).move_to([(M.x0 + LINE_X) / 2, 2.95, 0])
        self.add(counter)
        tot = self.t("zeros") if "zeros" in self.marks else 35.9
        tot = 35.9 - self.t("trillion")
        self.at("trillion",
                v.animate(rate_func=linear).set_value(1.0),
                FadeIn(checked, rate_func=win(tot, 0, 0.6)),
                *[rdots[i].animate(rate_func=win(tot, 0, 0.9)).move_to(M_ALL.p(0.5, ZEROS[k - 1]))
                  for i, (_, k) in enumerate(vals)],
                ShowIncreasingSubsets(col_a, rate_func=win(tot, 0.5, tot - 0.5, linear)),
                FadeIn(illus, rate_func=win(tot, 0.6, 0.6)), run_time=tot)
        counter.clear_updaters()
        settled = VGroup(N("≈ 12.36", 44, INK), T("trillion", 36, INK)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        settled.move_to(cpos)
        self.remove(rdots)
        self.until("every", ReplacementTransform(counter, settled),
                   ShowIncreasingSubsets(col_b, rate_func=linear), FadeIn(height_tag, shift=UP * 0.05))

        chk2 = check_mark(settled.get_right() + RIGHT * 0.5, size=0.24)
        on_line = T("all on the line", 28, INK).next_to(height_tag, DOWN, buff=0.45)
        glow = Line(M.p(0.5, 0), M.p(0.5, M.hmax), color=ACCENT, stroke_width=14, stroke_opacity=0.35)
        self.at("every", Create(chk2), FadeIn(on_line, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(glow, rate_func=there_and_back), col.animate(rate_func=there_and_back).set_color(ACCENT),
                  run_time=1.0)
        self.remove(glow)

        # ================================================================ P5: the proven share, 40% then > 2/3
        p4_stage = VGroup(pt_card, pt_lead, settled, checked, height_tag, chk2, on_line)
        self.at("p5", FadeOut(p4_stage), d2021.animate.set_color(DIM), run_time=0.6)

        bx, bw, by0, by1 = -1.4, 0.55, -1.85, 1.35
        yv = lambda f: by0 + (by1 - by0) * f
        bar = Rectangle(width=bw, height=by1 - by0, stroke_color=NEUTRAL, stroke_width=2).move_to([bx, (by0 + by1) / 2, 0])
        bar_title = T("proven on the line", 24, DIM).move_to([bx + 0.5, by1 + 0.62, 0])
        l100 = N("100%", 24, DIM).move_to([bx, by1 + 0.25, 0])
        note = T("a share, not all", 24, DIM).move_to([bx + 0.5, by0 - 0.33, 0])
        self.at("p5s1", run_time=0)
        self.at(40.64, Create(bar), FadeIn(bar_title), FadeIn(l100), FadeIn(note), run_time=0.9)

        d1989 = event_dot(1989)
        c_card, c_lead = make_card(1989, [T("Conrey · 1989 · > 40%", 28, INK),
                                          T("1989 to 2020: about 40% to 42%", 24, DIM)], side="right")
        c_card.align_to(np.array([yx(1989) + 0.5, 0, 0]), RIGHT)
        fill40 = Rectangle(width=bw, height=(by1 - by0) * 0.40, stroke_width=0, fill_color=ACCENT, fill_opacity=0.9)
        fill40.align_to(bar, DOWN).set_x(bx)
        l40 = N("40%", 24, ACCENT).move_to([bx + bw / 2 + 0.42, yv(0.40), 0])
        band = Line([yx(1989), TL_Y, 0], [yx(2020), TL_Y, 0], color=ACCENT, stroke_width=7, stroke_opacity=0.55)
        tot = 1.4
        self.at("forty",
                FadeIn(d1989, scale=0.4, rate_func=win(tot, 0, 0.4)),
                Create(c_lead, rate_func=win(tot, 0.1, 0.4)),
                FadeIn(c_card[0], shift=DOWN * 0.1, rate_func=win(tot, 0.2, 0.5)),
                GrowFromEdge(fill40, DOWN, rate_func=win(tot, 0.1, 1.0)),
                FadeIn(l40, rate_func=win(tot, 0.8, 0.5)), run_time=tot)
        self.until("p5s2", Create(band), FadeIn(c_card[1], shift=DOWN * 0.05))

        d2026 = event_dot(2026)
        a_card, a_lead = make_card(2026, [T("Alpöge and Furman · 2026", 28, INK)], side="right", top=1.3)
        tag = T("preprint · under review", 24, DIM)
        tag_box = SurroundingRectangle(tag, buff=0.1, corner_radius=0.08, color=DIM, stroke_width=1.5)
        tagg = VGroup(tag_box, tag).next_to(a_card, DOWN, buff=0.18).align_to(a_card, RIGHT)
        tot = 1.0
        self.at("thirds",
                d1989.animate(rate_func=win(tot, 0, 0.5)).set_color(DIM),
                band.animate(rate_func=win(tot, 0, 0.5)).set_stroke(opacity=0.3),
                FadeIn(d2026, scale=0.4, rate_func=win(tot, 0.1, 0.5)),
                Create(a_lead, rate_func=win(tot, 0.2, 0.5)),
                FadeIn(a_card, shift=DOWN * 0.1, rate_func=win(tot, 0.4, 0.6)), run_time=tot)
        self.at(47.56, FadeIn(tagg, shift=UP * 0.05), run_time=0.7)

        fill67 = Rectangle(width=bw, height=(by1 - by0) * 0.27, stroke_width=0, fill_color=ACCENT, fill_opacity=0.5)
        fill67.move_to([bx, yv(0.535), 0])
        l67 = N("> 67%", 24, ACCENT).move_to([bx + bw / 2 + 0.55, yv(0.67), 0])
        self.at(49.0, GrowFromEdge(fill67, DOWN), FadeIn(l67, rate_func=win(1.2, 0.6, 0.6)), run_time=1.2)

        # ---------------------------------------------------------------- end: everything out, the dial last
        rest = [m for m in self.mobjects if m is not dial]
        self.until(self.t("end") - 0.45, *[FadeOut(m) for m in rest])
        self.until("end", FadeOut(dial))
