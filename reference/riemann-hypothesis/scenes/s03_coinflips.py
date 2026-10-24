"""S03_CoinFlips - how far off can Gauss's curve be?  Coin flips give the scale; the error dial is built.

Beats (times from timeline/S03_CoinFlips.json):
  p1  {#far} an echo of the staircase (blue) and Gauss's curve (teal) on 0..100 with an ACCENT bracket 'gap?' and a
      big '?'; pause: the '?' pulses, the echo parks as a thumbnail at the top left.
  p2  {#coin} a coin (ACCENT, 'H') at the middle left, axes 'flips' / 'heads minus tails' (20 flips, ±5);
      {#up} heads: the walker steps up; {#down} tails: it steps down; a few more flips.  {#walks} the axes zoom out
      (1,000,000 flips, ±2,000) and seven real random walks (topic.random_walks, seed 7) draw together;
      {#thousand} the DIM dashed ±√n envelope and '≈ 1,000' (INK: the key number).
  p3  'a million' / 'a thousand' light up on the graph; {#root} '1,000,000' and '√1,000,000 = 1,000' at the top
      right; {#half} six zeros against three get ACCENT underlines; 'Pure chance': each walk brightens and settles;
      {#digits} 'half the digits'; pause: all fades.
  p4  the thumbnail returns as the full graph 0..1,000,000 (exact staircase at width 4 under the teal li at 3, so
      both colours show); {#x_mark} an ACCENT 'x' marker slides to 1,000,000, its label moves down to read
      'x = 1,000,000' under the axis; {#miss} a magnifier opens at the curve's end (exact primes 996,000..1,000,000,
      y 77,700..79,700): the gap bracket '129.5' and a DIM bar '√x = 1,000'; {#koch} 'Helge von Koch · 1901';
      {#promise} the RH line; 'staircase' / 'Gauss's curve' pulse and get labels inside the magnifier; {#sqrt} the
      √x bar pulses on 'square root' and the band li ± √x·ln x/(8π) opens (549.7 at a million); right after it,
      both honesty tags and '± 550' appear and the bar dims; the graph shrinks away from p4_end.
  p5  {#dial} the error dial builds at its fixed home; above it, a worked example for x = 1,000,000:
      {#zero} error '1' 'never grows'; {#all} '1,000,000' 'all the digits' (six zeros of six underlined);
      {#coin_mark} '1,000' 'half the digits' (three of six); the big coin from P2 returns and shrinks onto ½
      ('coin flips').
  p6  the example stays; {#window} the proven window ½..1 grows on the dial and a faint ACCENT column grows up from
      it behind the '1,000' and '1,000,000' columns, headed 'proven range'; {#pin} the pin 'Riemann?' drops onto ½
      while a brighter column lights the '1,000' column alone; 'unruly' the pin glows; 'coin flips' the coin and
      '1,000' pulse; end: the example and columns fade, then the dial fades last.
Dial state at the end = ErrorDial() standard state (window, coin, pin), which S06 fades in.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

# ------------------------------------------------------------------ p1 echo: 0..100
E_X0, E_X1, E_Y0, E_Y1 = -2.6, 2.4, -1.1, 1.9          # echo axes box (data 0..100 x 0..32)


def e_pt(x, y):
    return np.array([E_X0 + (E_X1 - E_X0) * x / 100, E_Y0 + (E_Y1 - E_Y0) * y / 32, 0])


# ------------------------------------------------------------------ p2 walks
W_O = np.array([-4.6, -0.4, 0])      # origin of the walk axes
W_LEN = 8.4                          # horizontal axis length
W_H = 2.2                            # half height of the vertical axis
SMALL_N, SMALL_V = 20, 5             # first view: 20 flips, ±5
BIG_N, BIG_V = 1_000_000, 2000       # zoomed-out view: 1,000,000 flips, ±2,000 (all 7 walks stay within ±1,400)


def w_small(i, v):
    return W_O + np.array([W_LEN * i / SMALL_N, W_H * v / SMALL_V, 0])


def w_big(i, v):
    return W_O + np.array([W_LEN * i / BIG_N, W_H * v / BIG_V, 0])


# ------------------------------------------------------------------ p4 graph: 0..1,000,000
G_O = np.array([-5.3, -2.5, 0])
G_W, G_H = 6.0, 4.9                  # 1,000,000 x 80,000


def g_pt(x, y):
    return G_O + np.array([G_W * x / 1e6, G_H * y / 80_000, 0])


# magnifier: data x 996,000..1,000,000, y 77,700..79,700
M_XA, M_XB = 996_000, 1_000_000
M_YA, M_YB = 77_700, 79_700
MP_X0, MP_X1, MP_Y0, MP_Y1 = 1.75, 4.35, -1.6, 2.6
PANEL = dict(x0=1.45, x1=6.45, y0=-1.75, y1=2.75)


def m_pt(x, y):
    return np.array([MP_X0 + (MP_X1 - MP_X0) * (x - M_XA) / (M_XB - M_XA),
                     MP_Y0 + (MP_Y1 - MP_Y0) * (y - M_YA) / (M_YB - M_YA), 0])


def band_w(x):
    """Schoenfeld: |π(x) − li(x)| < √x·ln x/(8π) for x ≥ 2657, if the Riemann Hypothesis is true."""
    x = np.asarray(x, float)
    return np.sqrt(x) * np.log(x) / (8 * np.pi)


def polyline(points, color, width):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(points)
    return m


def coin_mob(face="H", r=0.36):
    disc = Circle(radius=r, color=ACCENT, stroke_width=3).set_fill(ACCENT, 1)
    letter = T(face, int(r * 90), BG, weight=BOLD).move_to(disc)
    return VGroup(disc, letter)


def underlines(glyphs, color=ACCENT, gap=0.09, width=3):
    return VGroup(*[Line(g.get_corner(DL) + DOWN * gap + RIGHT * 0.02, g.get_corner(DR) + DOWN * gap + LEFT * 0.02,
                         color=color, stroke_width=width) for g in glyphs])


def zeros_of(text_mob, src):
    """Glyphs of text_mob that are the character '0' (Text keeps one submobject per non-space character)."""
    chars = [c for c in src if not c.isspace()]
    return [g for g, c in zip(text_mob, chars) if c == "0"]


def pulse(mob, scale=1.3, **kw):
    return mob.animate(rate_func=there_and_back, **kw).scale(scale)


def stroke_pulse(mob, width, **kw):
    w0 = mob.get_stroke_width()

    def upd(m, a):
        m.set_stroke(width=w0 + (width - w0) * there_and_back(a))

    return UpdateFromAlphaFunc(mob, upd, **kw)


class S03_CoinFlips(TimedScene):
    def word(self, sid, w, k=0):
        """Start time of the k-th occurrence of word w (prefix match, punctuation ignored) in sentence sid."""
        s = next(s for s in self.tl["sentences"] if s["id"] == sid)
        hits = [x["s"] for x in s["words"] if x["w"].lower().strip(",.:;?!").startswith(w.lower())]
        return hits[k]

    def construct(self):
        self.p1()
        self.p2()
        self.p3()
        self.p4()
        self.p5_p6()

    # ================================================================ p1: the question
    def p1(self):
        axes = VGroup(Line(e_pt(0, 0), e_pt(100, 0), color=NEUTRAL, stroke_width=3),
                      Line(e_pt(0, 0), e_pt(0, 32), color=NEUTRAL, stroke_width=3))
        stair = polyline([e_pt(x, y) for x, y in staircase_points(100)], PRIME_COLOR, 4)
        xs = np.linspace(2, 100, 120)
        curve = polyline([e_pt(x, y) for x, y in zip(xs, li(xs))], CURVE_COLOR, 4)
        labs = VGroup(N("0", 24, DIM).next_to(e_pt(0, 0), DOWN, buff=0.15),
                      N("100", 24, DIM).next_to(e_pt(100, 0), DOWN, buff=0.15))
        top, bot = e_pt(100, li([100])[0]), e_pt(100, 25)
        bx = 0.16
        bracket = VGroup(Line(bot + RIGHT * bx, top + RIGHT * bx, color=ACCENT, stroke_width=4),
                         Line(bot + RIGHT * (bx - 0.08), bot + RIGHT * (bx + 0.08), color=ACCENT, stroke_width=4),
                         Line(top + RIGHT * (bx - 0.08), top + RIGHT * (bx + 0.08), color=ACCENT, stroke_width=4))
        gap_lab = T("gap?", 26, ACCENT).next_to(bracket, RIGHT, buff=0.15)
        qmark = N("?", 110, ACCENT).move_to([4.6, 0.4, 0])
        echo = VGroup(axes, stair, curve, bracket)

        self.at("far", FadeIn(VGroup(axes, labs)), Create(stair), Create(curve), run_time=0.6)
        self.at(self.word("p1s1", "off"), GrowFromEdge(bracket, DOWN), FadeIn(gap_lab, shift=RIGHT * 0.1), run_time=0.6)
        self.at(self.word("p1s1", "curve"), FadeIn(qmark, scale=0.6), run_time=0.5)
        # pause (1.1 s, a question to the viewer): the '?' pulses once, then the echo parks at the top left
        self.at("p1_end", pulse(qmark, 1.25), run_time=0.55)
        self.thumb = echo
        self.play(echo.animate.scale(0.36).to_corner(UL, buff=0.4), FadeOut(VGroup(labs, gap_lab, qmark)),
                  run_time=1.0)

    # ================================================================ p2: coin flips
    def p2(self):
        xaxis = Line(W_O, W_O + RIGHT * W_LEN, color=NEUTRAL, stroke_width=3)
        yaxis = Line(W_O + DOWN * W_H, W_O + UP * W_H, color=NEUTRAL, stroke_width=3)
        yname = T("heads minus tails", 24, DIM).next_to(W_O + UP * W_H, RIGHT, buff=0.2)
        xn = N("20", 26, DIM).next_to(W_O + RIGHT * W_LEN, RIGHT, buff=0.18)
        xname = T("flips", 24, DIM).next_to(xn, DOWN, buff=0.1, aligned_edge=LEFT)
        yt = N("+5", 26, DIM).next_to(W_O + UP * W_H, LEFT, buff=0.18)
        yb = N("−5", 26, DIM).next_to(W_O + DOWN * W_H, LEFT, buff=0.18)
        coin = coin_mob("H").move_to([-5.95, -0.4, 0])
        walker = pt(W_O, ACCENT, r=0.08).set_z_index(3)
        self.walk_axes = VGroup(xaxis, yaxis, xname, yname)

        self.at("coin", FadeIn(coin, scale=0.5), Create(xaxis), Create(yaxis), run_time=0.8)
        self.play(FadeIn(VGroup(xname, yname, xn, yt, yb)), FadeIn(walker, scale=0.3), run_time=0.5)

        def flip(face_to, half_turns):

            def upd(m, a):
                seg = int(np.floor(a * half_turns + 0.5))
                face = face_to if (half_turns - seg) % 2 == 0 else ("T" if face_to == "H" else "H")
                s = max(0.04, abs(np.cos(np.pi * half_turns * a)))
                m.become(coin_mob(face).stretch(s, 1).move_to([-5.95, -0.4 + 0.55 * np.sin(np.pi * a), 0]))

            return UpdateFromAlphaFunc(coin, upd, rate_func=linear)

        path_pts = [w_small(0, 0)]
        segs = VGroup()

        def step(dv, rt, mark=None):
            i = len(path_pts) - 1
            v = round((path_pts[-1][1] - W_O[1]) / (W_H / SMALL_V))
            p = w_small(i + 1, v + dv)
            seg = Line(path_pts[-1], p, color=ACCENT, stroke_width=4)
            path_pts.append(p)
            segs.add(seg)
            anims = (Create(seg), walker.animate.move_to(p))
            if mark is None:
                self.play(*anims, run_time=rt)
            else:
                self.at(mark, *anims, run_time=rt)

        # heads: the coin lands on 'H' as "step up" is said
        self.until("up", flip("H", 4), min_run_time=0.3)
        step(+1, 0.45, "up")
        self.until("down", flip("T", 3))
        step(-1, 0.45, "down")
        self.play(FadeOut(coin, shift=DOWN * 0.2), run_time=0.2)
        for dv in (+1, +1, -1):              # a few more flips, quickly
            step(dv, 0.16)

        # {#walks}: zoom out to a million flips; seven real walks draw together
        xs, W = random_walks(seed=7, n=BIG_N, k=7)
        # yellow (index 1) is close to the ACCENT walker it replaces: it goes last in the colour order, thinner and at the
        # bottom of the draw order, so no single walk looks highlighted
        order = [0, 2, 3, 4, 5, 6, 1]
        walks = VGroup(*[polyline([w_big(i, v) for i, v in zip(xs, w)], PALETTE[c], 1.8 if c == 1 else 2.2)
                         for c, w in zip(order, W)])
        walks.submobjects = walks.submobjects[-1:] + walks.submobjects[:-1]
        xn2 = N("1,000,000", 26, DIM).next_to(W_O + RIGHT * W_LEN, RIGHT, buff=0.18)
        yt2 = N("+2,000", 26, DIM).next_to(W_O + UP * W_H, LEFT, buff=0.18)
        yb2 = N("−2,000", 26, DIM).next_to(W_O + DOWN * W_H, LEFT, buff=0.18)
        small = VGroup(segs, walker)
        dur = self.t("thousand") - self.t("walks")
        self.at("walks", AnimationGroup(
            small.animate(run_time=0.6).scale(0.02, about_point=W_O).set_opacity(0),
            ReplacementTransform(xn, xn2, run_time=0.6), ReplacementTransform(yt, yt2, run_time=0.6),
            ReplacementTransform(yb, yb2, run_time=0.6),
            Create(walks, lag_ratio=0, rate_func=linear, run_time=dur)), run_time=dur)
        self.remove(small)

        # {#thousand}: ±√n envelope reaching ±1,000 at a million flips
        ts = np.linspace(0, BIG_N, 300)
        env = VGroup(*[DashedVMobject(polyline([w_big(t, sgn * np.sqrt(t)) for t in ts], DIM, 2.5),
                                      num_dashes=40, dashed_ratio=0.55) for sgn in (1, -1)])
        env.set_z_index(2)
        self.approx = N("≈ 1,000", 28, INK).next_to(w_big(BIG_N, 1000), RIGHT, buff=0.18)
        self.at("thousand", Create(env, lag_ratio=0), run_time=0.7)
        self.at(self.word("p2s2", "steps"), FadeIn(self.approx, shift=LEFT * 0.1), run_time=0.5)
        self.walks, self.env, self.xn2 = walks, env, xn2
        self.walk_labels = VGroup(xn2, yt2, yb2)

    # ================================================================ p3: half the digits
    def p3(self):
        self.at(self.word("p3s1", "million"), self.xn2.animate(rate_func=there_and_back).scale(1.25).set_color(ACCENT),
                run_time=0.6)
        self.at(self.word("p3s1", "thousand"), self.approx.animate(rate_func=there_and_back).scale(1.25).set_color(ACCENT),
                run_time=0.6)

        s1, s2 = "1,000,000", "√1,000,000 = 1,000"
        l1 = N(s1, 36, INK)
        l2 = N(s2, 36, ACCENT)
        block = VGroup(l1, l2).arrange(DOWN, buff=0.28).move_to([4.35, 2.95, 0])
        l1.align_to(l2, RIGHT)
        self.at("root", TransformFromCopy(self.xn2, l1), run_time=0.8)
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.5)

        u1 = underlines(zeros_of(l1, s1))
        u2 = underlines(zeros_of(l2, s2)[-3:])
        self.at("half", LaggedStart(*[Create(u) for u in u1], lag_ratio=0.25), run_time=0.7)
        self.at(self.word("p3s1", "zeros"), LaggedStart(*[Create(u) for u in u2], lag_ratio=0.25), run_time=0.5)
        # "Pure chance": the walks brighten once
        self.at("p3s2", *[stroke_pulse(w, 4.0) for w in self.walks], run_time=0.8)
        hd = T("half the digits", 30, ACCENT).next_to(block, DOWN, buff=0.3)
        self.at("digits", FadeIn(hd, shift=UP * 0.1), run_time=0.6)
        # pause: the walks and everything with them fade
        # the thumbnail's 0..100 'gap' bracket leaves with them, so only its axes and curves grow into P4's graph
        bracket = self.thumb[3]
        self.thumb.remove(bracket)
        self.add(bracket)
        self.at("p3_end", FadeOut(VGroup(self.walks, self.env, self.approx, self.walk_axes, self.walk_labels,
                                         block, u1, u2, hd, bracket)), run_time=0.7)

    # ================================================================ p4: von Koch
    def p4(self):
        axes = VGroup(Line(g_pt(0, 0), g_pt(1e6, 0), color=NEUTRAL, stroke_width=3),
                      Line(g_pt(0, 0), g_pt(0, 80_000), color=NEUTRAL, stroke_width=3))
        ticks = VGroup(*[Line(g_pt(x, 0), g_pt(x, 0) + DOWN * 0.1, color=NEUTRAL, stroke_width=2) for x in (5e5, 1e6)],
                       *[Line(g_pt(0, y), g_pt(0, y) + LEFT * 0.1, color=NEUTRAL, stroke_width=2) for y in (4e4, 8e4)])
        xl = VGroup(N("0", 24, DIM).next_to(g_pt(0, 0), DOWN, buff=0.18),
                    N("500,000", 24, DIM).next_to(g_pt(5e5, 0), DOWN, buff=0.18),
                    N("1,000,000", 24, DIM).next_to(g_pt(1e6, 0), DOWN, buff=0.18))
        yl = VGroup(N("40,000", 24, DIM).next_to(g_pt(0, 4e4), LEFT, buff=0.18),
                    N("80,000", 24, DIM).next_to(g_pt(0, 8e4), LEFT, buff=0.18))
        sp = staircase_points(1_000_000)
        stair = polyline([g_pt(x, y) for x, y in sp], PRIME_COLOR, 6.5)   # blue rim around the teal li (3) on top
        cx = np.concatenate([np.linspace(2, 100, 30), np.geomspace(101, 1e6, 170)])
        cy = li(cx)
        curve = polyline([g_pt(x, y) for x, y in zip(cx, cy)], CURVE_COLOR, 3)
        graph = VGroup(axes, stair, curve)

        # the thumbnail returns as the full graph
        # (the thumbnail fades out while it grows toward the graph box; the new graph fades in growing from the
        # thumbnail, so the 0..100 steps are never stretched over the 0..1,000,000 axes)
        k = self.thumb.width / axes.width
        self.until("x_mark", FadeOut(self.thumb, target_position=axes.get_center(), scale=1 / k, rate_func=rush_into),
                   FadeIn(graph, target_position=self.thumb.get_center(), scale=k),
                   FadeIn(VGroup(ticks, xl, yl)), min_run_time=0.8)

        # {#x_mark}: a marker 'x' slides along the axis and stops at 1,000,000
        mline = Line(g_pt(0, 0), g_pt(0, 80_000) + UP * 0.1, color=ACCENT, stroke_width=3)
        mlab = N("x", 32, ACCENT, slant=ITALIC).next_to(mline, UP, buff=0.1)
        marker = VGroup(mline, mlab).set_z_index(3)
        self.at("x_mark", FadeIn(marker), run_time=0.3)
        self.play(marker.animate.shift(RIGHT * G_W), run_time=1.2)
        # the label leaves the line top (the lens goes there) and reads 'x = 1,000,000' under the axis
        xeq = VGroup(N("x", 30, ACCENT, slant=ITALIC), N("=", 26, ACCENT)).arrange(RIGHT, buff=0.1)
        xeq.next_to(xl[2], LEFT, buff=0.12).set_y(xl[2].get_y() + 0.02)
        self.at(self.word("p4s2", "million"), xl[2].animate.set_color(ACCENT), Transform(mlab, xeq), run_time=0.5)

        # {#miss}: magnifier at x = 1,000,000
        L1 = float(li([1e6])[0])
        P1 = int(prime_pi([1e6])[0])
        center = g_pt(1e6, L1)
        lens = Circle(radius=0.3, color=INK, stroke_width=2.5).move_to(center)
        panel = RoundedRectangle(corner_radius=0.12, width=PANEL["x1"] - PANEL["x0"], height=PANEL["y1"] - PANEL["y0"],
                                 stroke_color=INK, stroke_width=2.5, fill_color=BG, fill_opacity=1).move_to(
            [(PANEL["x0"] + PANEL["x1"]) / 2, (PANEL["y0"] + PANEL["y1"]) / 2, 0])
        conn = VGroup(Line(lens.point_at_angle(PI / 2), panel.get_corner(UL) + RIGHT * 0.12, color=DIM, stroke_width=1.5),
                      Line(lens.point_at_angle(-PI / 2), panel.get_corner(DL) + RIGHT * 0.12, color=DIM, stroke_width=1.5))
        # exact staircase from 996,000 to 1,000,000
        P = primes_upto(1_000_000)
        inside = P[P > M_XA]
        c = int(prime_pi([M_XA])[0])
        spts = [m_pt(M_XA, c)]
        for p in inside:
            spts += [m_pt(p, c), m_pt(p, c + 1)]
            c += 1
        spts.append(m_pt(M_XB, c))
        assert c == P1
        mstair = polyline(spts, PRIME_COLOR, 3.5)
        mx = np.linspace(M_XA, M_XB, 41)
        my = li(mx)
        mcurve = polyline([m_pt(x, y) for x, y in zip(mx, my)], CURVE_COLOR, 3.5)
        top, bot = m_pt(M_XB, L1), m_pt(M_XB, P1)
        bx = 0.14
        bracket = VGroup(Line(bot + RIGHT * bx, top + RIGHT * bx, color=ACCENT, stroke_width=4),
                         Line(bot + RIGHT * (bx - 0.07), bot + RIGHT * (bx + 0.07), color=ACCENT, stroke_width=4),
                         Line(top + RIGHT * (bx - 0.07), top + RIGHT * (bx + 0.07), color=ACCENT, stroke_width=4))
        gap_lab = N(f"{L1 - P1:.1f}", 28, ACCENT).next_to(bracket, RIGHT, buff=0.12)
        bar_x = 5.75
        bar = Rectangle(width=0.3, height=m_pt(0, P1 + 1000)[1] - m_pt(0, P1)[1], stroke_color=DIM, stroke_width=2,
                        fill_color=DIM, fill_opacity=0.35)
        bar.move_to([bar_x, (m_pt(0, P1 + 1000)[1] + m_pt(0, P1)[1]) / 2, 0])
        # labelled 'coin flips' so the link to P3 reads without words (the square root is only spoken at {#sqrt})
        bar_lab = VGroup(T("coin flips", 24, DIM), N("√x = 1,000", 26, DIM)).arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        bar_lab.next_to(bar, LEFT, buff=0.14).align_to(bar, UP)
        base = DashedLine(bot + RIGHT * 0.3, [bar_x - 0.15, bot[1], 0], color=FAINT, stroke_width=1.5, dash_length=0.06)

        self.at("miss", Create(lens), run_time=0.4)
        self.play(AnimationGroup(Create(conn, run_time=0.4), FadeIn(panel, run_time=0.4),
                                 AnimationGroup(Create(mcurve), Create(mstair), run_time=0.6), lag_ratio=0.5), run_time=0.9)
        self.at(self.word("p4s2", "hundred"), GrowFromEdge(bracket, DOWN), FadeIn(gap_lab, shift=RIGHT * 0.1),
                run_time=0.6)
        self.at(self.word("p4s2", "thirty") + 0.15, FadeIn(base), GrowFromEdge(bar, DOWN), run_time=0.6)
        self.play(FadeIn(bar_lab, shift=UP * 0.08), run_time=0.35)

        # {#koch}, {#promise}
        k1 = T("Helge von Koch · 1901", 26, INK)
        k2 = VGroup(N("Riemann Hypothesis =", 24, DIM), N("the gap stays within", 24, DIM),
                    N("about √x · log x", 24, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        kblock = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        kblock.move_to([-4.85, 2.5, 0], aligned_edge=UL)
        k3 = VGroup()
        self.at("koch", FadeIn(k1, shift=DOWN * 0.1), run_time=0.7)
        self.at("promise", FadeIn(VGroup(k2, k3), shift=DOWN * 0.1), run_time=0.8)
        # line labels inside the magnifier, each on its word
        teal_y = lambda x: np.interp(x, [m_pt(a, b)[0] for a, b in zip(mx, my)], [m_pt(a, b)[1] for a, b in zip(mx, my)])
        sl = T("staircase", 24, PRIME_COLOR)
        sl.move_to([MP_X0 + 0.1, 0, 0], aligned_edge=LEFT).align_to([0, spts[0][1] - 0.1, 0], UP)
        gl = T("Gauss's curve", 24, CURVE_COLOR)
        gl.move_to([MP_X0 + 0.1, 0, 0], aligned_edge=LEFT)
        gl.align_to([0, teal_y(gl.get_right()[0]) + 0.1, 0], DOWN)
        # on the main graph the two lines overlap at this scale: 'staircase' hides the teal so the line reads pure blue,
        # 'Gauss's curve' swells the teal over the blue, so the viewer sees two curves lying there
        self.at(self.word("p4s4", "staircase"), stroke_pulse(mstair, 8), stroke_pulse(stair, 8), stroke_pulse(curve, 0),
                FadeIn(sl, shift=DOWN * 0.08), run_time=0.8)
        self.at(self.word("p4s4", "Gauss"), stroke_pulse(mcurve, 8), stroke_pulse(curve, 9),
                FadeIn(gl, shift=UP * 0.08), run_time=0.8)

        # {#sqrt}: the band li ± √x·ln x/(8π) opens around the curve (main graph from x = 2,657, and in the magnifier)
        def band_poly(xs, ys, frac, mapper, opacity):
            w = band_w(xs) * frac
            pts = [mapper(x, y + d) for x, y, d in zip(xs, ys, w)] + \
                  [mapper(x, y - d) for x, y, d in zip(xs[::-1], ys[::-1], w[::-1])]
            return Polygon(*pts, stroke_width=0, fill_color=CURVE_COLOR, fill_opacity=opacity)

        gx = np.geomspace(2657, 1e6, 120)
        gy = li(gx)
        gband0, gband = band_poly(gx, gy, 0.001, g_pt, 0.45), band_poly(gx, gy, 1, g_pt, 0.45)
        mband0, mband = band_poly(mx, my, 0.001, m_pt, 0.22), band_poly(mx, my, 1, m_pt, 0.22)
        medges0 = VGroup(*[polyline([m_pt(x, y + s * band_w(x) * 0.001) for x, y in zip(mx, my)], CURVE_COLOR, 1.5)
                           for s in (1, -1)])
        medges = VGroup(*[polyline([m_pt(x, y + s * band_w(x)) for x, y in zip(mx, my)], CURVE_COLOR, 1.5)
                          for s in (1, -1)])
        panel.set_z_index(-2)
        for m in (gband0, gband, mband0, mband, medges0, medges):
            m.set_z_index(-1)
        tag1 = T("if the Riemann Hypothesis is true", 24, DIM)
        tag2 = T("Schoenfeld's exact version (÷ 8π)", 24, DIM)
        tags = VGroup(tag1, tag2).arrange(DOWN, buff=0.08).next_to(panel, DOWN, buff=0.1).align_to(panel, RIGHT)
        pm = N("± 550", 24, CURVE_COLOR).next_to(m_pt(M_XB, L1 + band_w(1e6)), RIGHT, buff=0.1)
        self.add(gband0, mband0, medges0)
        # 'the square root of x': the √x bar answers the word while the band opens beside it
        self.at("sqrt", AnimationGroup(Transform(gband0, gband, run_time=1.1), Transform(mband0, mband, run_time=1.1),
                                       Transform(medges0, medges, run_time=1.1), stroke_pulse(bar, 5, run_time=0.75),
                                       pulse(bar_lab, 1.18, run_time=0.75)), run_time=1.1)
        # the band carries its own number; the √x bar's job is done; both honesty tags together
        self.play(FadeIn(tags, shift=UP * 0.08), FadeIn(pm, shift=LEFT * 0.06),
                  bar.animate.set_fill(opacity=0.1).set_stroke(opacity=0.3), bar_lab.animate.set_opacity(0.3),
                  base.animate.set_opacity(0.3), run_time=0.6)

        # after the sentence: the graph shrinks away
        everything = VGroup(graph, ticks, xl, yl, marker, lens, conn, panel, mband0, medges0, mstair, mcurve, bracket,
                            gap_lab, base, bar, bar_lab, kblock, tags, gband0, sl, gl, pm)
        self.at("p4_end", everything.animate.scale(0.4).set_opacity(0), run_time=self.t("p5") - self.t("p4_end"))
        self.remove(everything)

    # ================================================================ p5 + p6: the error dial
    def p5_p6(self):
        dial = ErrorDial()
        dial.panel.set_z_index(9)
        dial.window.set_z_index(9.5)
        for m in (dial.coin, dial.coin_label, dial.pin, dial.pin_label):
            m.set_z_index(10)

        # {#dial}: ruler, ticks, labels and captions build in ~1.5 s
        self.add(dial.panel)
        self.at("dial", Create(dial.ruler), run_time=0.6)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in dial.ticks], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in dial.labels], lag_ratio=0.3), run_time=0.5)
        self.play(FadeIn(dial.cap_left), FadeIn(dial.cap_right), run_time=0.45)

        # a worked example above the dial: the error sizes each reading stands for, at x = 1,000,000
        ex_y, cap_y = 0.1, -0.55
        head = VGroup(T("the error, when", 28, DIM), N("x = 1,000,000", 40, INK)).arrange(RIGHT, buff=0.25)
        head.move_to([0, 1.7, 0])
        cols = {}
        for v, num, cap, col in ((0, "1", "never grows", INK), (1, "1,000,000", "all the digits", INK),
                                 (0.5, "1,000", "half the digits", ACCENT)):
            n = N(num, 46, col).move_to([dial.x_of(v), ex_y, 0])
            c = T(cap, 26, DIM if col == INK else ACCENT).move_to([dial.x_of(v), cap_y, 0])
            g = DashedLine([dial.x_of(v), cap_y - 0.3, 0], [dial.x_of(v), DIAL_TOP - 0.02, 0], color=FAINT,
                           stroke_width=2, dash_length=0.07)
            u = underlines(zeros_of(n, num), gap=0.07)
            cols[v] = (n, c, g, u)
        self.at(self.word("p5s1", "digits"), FadeIn(head, shift=RIGHT * 0.1), run_time=0.7)

        n0, c0, g0, _ = cols[0]
        self.at("zero", FadeIn(n0, shift=DOWN * 0.1), Create(g0), run_time=0.6)
        self.at(self.word("p5s2", "never"), FadeIn(c0), run_time=0.5)

        n1, c1, g1, u1 = cols[1]
        self.at("all", FadeIn(n1, shift=DOWN * 0.1), Create(g1), run_time=0.6)
        self.at(self.word("p5s3", "many"), LaggedStart(*[Create(u) for u in u1], lag_ratio=0.2), FadeIn(c1),
                run_time=0.7)

        nh, ch, gh, uh = cols[0.5]
        # the big coin from P2 comes back where it flipped, then shrinks onto ½ as 'half the digits' is said
        big = coin_mob("H").move_to([-5.95, -0.4, 0]).set_z_index(10)
        self.at("coin_mark", FadeIn(nh, shift=DOWN * 0.1), Create(gh), FadeIn(big, scale=0.5), run_time=0.6)
        self.at(self.word("p5s4", "half", 1), LaggedStart(*[Create(u) for u in uh], lag_ratio=0.2), FadeIn(ch),
                ReplacementTransform(big, dial.coin, path_arc=-PI / 5), run_time=0.9)
        self.at(self.word("p5s4", "coin"), FadeIn(dial.coin_label, shift=RIGHT * 0.1), pulse(dial.coin, 1.35),
                run_time=0.6)

        # p6: the example stays.  {#window}: the proven window grows over ½..1 on the dial and, above it, a faint
        # column lights the errors it allows at a million: somewhere between 1,000 and 1,000,000
        n1, c1 = cols[1][0], cols[1][1]
        example = VGroup(head, *[m for v in cols for m in cols[v]])
        ybot, ytop, htop = DIAL_TOP + 0.06, 1.18, 0.62

        def column(x0, x1, y1, opacity):
            r = RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=y1 - ybot, stroke_width=0,
                                 fill_color=ACCENT, fill_opacity=opacity)
            return r.move_to([(x0 + x1) / 2, (ybot + y1) / 2, 0]).set_z_index(-1)

        wide = column(min(nh.get_left()[0], ch.get_left()[0]) - 0.22, max(n1.get_right()[0], c1.get_right()[0]) + 0.22,
                      ytop, 0.12)
        narrow = column(min(nh.get_left()[0], ch.get_left()[0]) - 0.12, max(nh.get_right()[0], ch.get_right()[0]) + 0.12,
                        htop, 0.16)
        proven = T("proven range", 24, DIM).move_to([wide.get_x(), (htop + ytop) / 2 + 0.02, 0])
        win = dial.window
        win_start = win.copy().stretch(0.02, 0, about_edge=LEFT)
        self.add(win_start)
        self.at("window", Transform(win_start, win), GrowFromEdge(wide, DOWN), run_time=0.8)
        self.remove(win_start)
        self.add(win)
        self.at(self.word("p6s1", "between"), FadeIn(proven, shift=DOWN * 0.08), run_time=0.4)
        self.at(self.word("p6s1", "half"), pulse(dial.labels[1], 1.35), pulse(nh, 1.15), run_time=0.45)
        self.at(self.word("p6s1", "one", 1), pulse(dial.labels[2], 1.35), pulse(n1, 1.15), run_time=0.45)

        # {#pin}: Riemann's guess drops onto ½; a brighter column picks out '1,000' (the window itself stays wide)
        dial.pin_label.set_stroke(BG, 5, background=True)     # reads cleanly where it meets the window rim
        pin_start = dial.pin.copy().shift(UP * 0.9).set_opacity(0)
        self.at("pin", Transform(pin_start, dial.pin, rate_func=rate_functions.ease_out_bounce),
                GrowFromEdge(narrow, DOWN), run_time=0.6)
        self.remove(pin_start)
        self.add(dial.pin)
        self.play(FadeIn(dial.pin_label, shift=LEFT * 0.1), pulse(VGroup(nh, ch), 1.12), run_time=0.5)
        halo = Circle(radius=0.12, stroke_width=0).set_fill(ACCENT, 0.5).move_to(dial.pin[0]).set_z_index(9.6)
        self.add(halo)
        self.at(self.word("p6s2", "unruly"), halo.animate.scale(4.5).set_fill(opacity=0), pulse(dial.pin, 1.3),
                run_time=0.7)
        self.remove(halo)
        self.at(self.word("p6s2", "coin"), pulse(dial.coin, 1.4), pulse(nh, 1.15), run_time=0.6)

        # scene end: the example and its columns fade, then the dial fades last
        self.at("p6_end", FadeOut(VGroup(example, wide, narrow, proven)), run_time=0.4)
        parts = VGroup(dial.panel, win, dial.ruler, dial.ticks, dial.labels, dial.cap_left, dial.cap_right,
                       dial.coin, dial.coin_label, dial.pin, dial.pin_label)
        self.until("end", FadeOut(parts))

