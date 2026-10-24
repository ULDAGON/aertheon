"""S05 - The diamond rule.

With only three colors, the two tips of a diamond (two unit triangles sharing the edge B-C) always
get the same color: the middle dots B, C take two different colors, and each tip is joined to both,
so each tip gets the one leftover color. The tips are sqrt(3) ~ 1.73 apart, so matching is allowed.

Coordinates (manim, UNIT = 2.0) are the same as in S04: B = (-1, -0.2), C = (1, -0.2),
D = (0, 1.532) (top tip), A = (0, -1.932) (bottom tip); this is geom.diamond(pi/2) scaled and shifted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------- geometry
U = 2.0
SHIFT = np.array([0.0, -0.2 - U * SQ3 / 2, 0.0])
P = {k: to_scene(v, U, SHIFT) for k, v in diamond(PI / 2).items()}
assert np.allclose(P["B"], [-1, -0.2, 0]) and np.allclose(P["C"], [1, -0.2, 0])
EDGES = [("B", "C"), ("D", "B"), ("D", "C"), ("A", "B"), ("A", "C")]
for _a, _b in EDGES:
    assert abs(np.linalg.norm(P[_a] - P[_b]) - U) < 1e-9
ORDER = "BCDA"
CENTER = (P["A"] + P["D"]) / 2           # (0, -0.2)

BL, YE, PK = BLUE_P, YELLOW_P, PINK_P
C1 = dict(B=BL, C=YE, D=PK, A=PK)
C2 = dict(B=PK, C=BL, D=YE, A=YE)
C3 = dict(B=YE, C=PK, D=BL, A=BL)
C4 = dict(B=BL, C=PK, D=YE, A=YE)
for _c in (C1, C2, C3, C4):                # every coloring is valid (sticks join different colors)
    assert all(_c[a] != _c[b] for a, b in EDGES)

R_NODE = 0.13
R_MINI = 0.14
EQ_ANGLE = 3.50                            # '=' arc A->D bows right, apex x ~ 2.07 (clear of C, left of the card)

# gallery of earlier tries (right edge)
TH_S = 0.36
SLOTS = [np.array([5.25, 2.2, 0.0]), np.array([5.25, 0.5, 0.0]), np.array([5.25, -1.2, 0.0])]


# ---------------------------------------------------------------- helpers
def node(pos):
    return Circle(radius=R_NODE).set_fill(BG, 1).set_stroke(INK, 3).move_to(pos).set_z_index(3)


def paint(n, c):
    return n.animate.set_fill(c, 1).set_stroke(c, opacity=1)


def recolor(n, c, delay=0.0):
    """Repaint a painted dot without blending hues: it pops small, swaps color, pops back."""
    base = n.copy()
    old = n.get_fill_color()

    def f(m, a):
        a = min(1.0, max(0.0, (a - delay) / (1 - delay)))
        a = smooth(a)
        col = old if a < 0.5 else c
        m.become(base.copy().set_fill(col, 1).set_stroke(col, opacity=1).scale(0.2 + 0.8 * abs(1 - 2 * a)))
    return UpdateFromAlphaFunc(n, f, rate_func=linear)


def unpaint(n):
    return n.animate.set_fill(BG, 1).set_stroke(INK, opacity=1)


def ping(pos, color=ACCENT, r0=0.17, r1=0.5, width=4):
    """An expanding, fading ring around a point (removes itself)."""
    c = Circle(radius=r0).set_stroke(color, width).move_to(pos).set_z_index(6)
    base = c.copy()

    def f(m, a):
        m.become(base.copy().scale((r0 + (r1 - r0) * a) / r0)
                 .set_stroke(color, width * (1 - 0.5 * a), opacity=1 - a))
    return UpdateFromAlphaFunc(c, f, remover=True, rate_func=rate_functions.ease_out_cubic)


def glow(line, color=ACCENT, width=8):
    return line.animate(rate_func=there_and_back).set_stroke(color, width=width, opacity=1)


def travel(m, pts, end_scale=1.0):
    """Move m along the polyline pts, scaling it by end_scale on the way."""
    path = VMobject().set_points_as_corners([np.asarray(p, float) for p in pts])
    base = m.copy()

    def f(mob, a):
        mob.become(base.copy().scale(1 + (end_scale - 1) * a).move_to(path.point_from_proportion(a)))
    return UpdateFromAlphaFunc(m, f)


def eq_arc(a, d, angle=EQ_ANGLE, width=3, dashed=True):
    arc = ArcBetweenPoints(a, d, angle=angle)
    apex = arc.point_from_proportion(0.5)
    if dashed:
        arc = DashedVMobject(arc, num_dashes=30, dashed_ratio=0.55)
    arc.set_stroke(ACCENT, width).set_z_index(1.5)
    return arc, apex


def eq_badge(pos):
    b = VGroup(Circle(radius=0.25).set_fill(BG, 1).set_stroke(ACCENT, 2.5), N("=", 36, ACCENT))
    return b.move_to(pos).set_z_index(5)


def tpos(k, slot):
    return slot + TH_S * (P[k] - CENTER)


def thumb(coloring, slot):
    """Small copy of the coloured diamond: VGroup(sticks, nodes, tip rings) - same structure as the main one."""
    sticks = VGroup(*[Line(tpos(a, slot), tpos(b, slot), color=UNIT_COLOR, stroke_width=2.2) for a, b in EDGES])
    nodes = VGroup(*[Circle(radius=0.075).set_fill(coloring[k], 1).set_stroke(coloring[k], 1.5).move_to(tpos(k, slot))
                     for k in ORDER])
    rings = VGroup(*[Circle(radius=0.13).set_stroke(ACCENT, 1.8).move_to(tpos(k, slot)) for k in "DA"])
    return VGroup(sticks, nodes, rings).set_z_index(8)


class S05_Diamond(TimedScene):
    def construct(self):

        # ============================================================ lead-in + P1
        bar = BoundsBar(lo=3).scale(0.8).to_edge(DOWN, buff=0.3)   # the scoreboard's fixed home (as in S04/S06)
        self.until("p1", FadeIn(bar))
        # "Can three colors do it?"  (word 'three' at 0.56 s)
        self.at(0.56, bar.cells[2].animate(rate_func=there_and_back).scale(1.4).set_color(ACCENT), run_time=0.9)

        nodes = {k: node(P[k]) for k in ORDER}
        sticks = {a + b: stick(P[a], P[b]).set_z_index(1) for a, b in EDGES}
        # "Go back to ..." - the two middle dots and their stick
        self.at("p1s2", FadeIn(nodes["B"]), FadeIn(nodes["C"]), Create(sticks["BC"]), run_time=0.55)

        # {#rings}: both unit rings redraw at once, each swept by a unit stick (mirror-symmetric)
        ringB = Arc(radius=U, start_angle=0, angle=TAU, arc_center=P["B"]).set_stroke(UNIT_COLOR, 2.5).set_z_index(0)
        ringC = Arc(radius=U, start_angle=PI, angle=-TAU, arc_center=P["C"]).set_stroke(UNIT_COLOR, 2.5).set_z_index(0)
        swB = stick(P["B"], P["C"]).set_z_index(2)
        swC = stick(P["C"], P["B"]).set_z_index(2)

        def sweeper(line, c, a0, sgn):
            def f(m, a):
                ang = a0 + sgn * TAU * a
                m.put_start_and_end_on(c, c + U * np.array([np.cos(ang), np.sin(ang), 0.0]))
            return UpdateFromAlphaFunc(line, f)
        self.at("rings", Create(ringB), Create(ringC), sweeper(swB, P["B"], 0, 1), sweeper(swC, P["C"], PI, -1),
                run_time=1.3)

        # {#both}: both crossing points appear and pulse
        self.at("both", FadeOut(swB), FadeOut(swC), GrowFromCenter(nodes["D"]), GrowFromCenter(nodes["A"]),
                ping(P["D"]), ping(P["A"]), run_time=0.8)

        # {#diamond}: four sticks from the tips; the rings recede
        self.at("diamond", *[Create(sticks[k]) for k in ("DB", "DC", "AB", "AC")],
                ringB.animate.set_stroke(opacity=0.2), ringC.animate.set_stroke(opacity=0.2), run_time=0.8)
        # "two triangles" - upper, then lower tints
        up_tri = Polygon(P["B"], P["C"], P["D"]).set_stroke(width=0).set_fill(INK, 0.13).set_z_index(0.5)
        lo_tri = Polygon(P["B"], P["C"], P["A"]).set_stroke(width=0).set_fill(INK, 0.13).set_z_index(0.5)
        self.at(7.77, FadeIn(up_tri), run_time=0.35)
        self.at(8.08, FadeIn(lo_tri), run_time=0.35)
        # "glued together" - the shared stick
        self.at(8.6, glow(sticks["BC"]), run_time=0.7)
        # "five sticks" (word 'five' at 9.51) - all five sticks glow together once, label at the right
        count = T("5 sticks", 28, DIM).move_to([4.6, 0.3, 0])
        self.at(9.5, FadeOut(up_tri), FadeOut(lo_tri), *[glow(sticks[a + b]) for a, b in EDGES],
                FadeIn(count, shift=LEFT * 0.2), run_time=0.85)

        # ============================================================ P2: try colorings
        swatches = VGroup(*[Dot(radius=0.2, color=c) for c in (BL, YE, PK)]).arrange(DOWN, buff=0.45)
        swatches.move_to([-5.7, -0.1, 0])
        sw_label = T("3 colors", 26, DIM).next_to(swatches, UP, buff=0.35)
        self.at("color", FadeOut(count), FadeOut(ringB), FadeOut(ringC),
                FadeIn(sw_label), LaggedStart(*[GrowFromCenter(s) for s in swatches], lag_ratio=0.25),
                run_time=0.65)

        # paint drops fly from the palette into the dots (coloring 1)
        src = {BL: swatches[0], YE: swatches[1], PK: swatches[2]}
        drops = []
        for k in ORDER:
            d = nodes[k].copy().set_fill(C1[k], 1).set_stroke(C1[k]).move_to(src[C1[k]]).set_z_index(7)
            drops.append((k, d))
        self.at(11.8, LaggedStart(*[d.animate(path_arc=-0.35).move_to(P[k]) for k, d in drops], lag_ratio=0.22),
                run_time=1.05)
        for k, d in drops:
            nodes[k].set_fill(C1[k], 1).set_stroke(C1[k])
            self.remove(d)

        # "any way the rule allows" - every stick joins two different colors
        checks = VGroup()
        for a, b in EDGES:
            mid = (P[a] + P[b]) / 2
            off = UP * 0.3 if a + b == "BC" else normalize(mid - CENTER) * 0.36
            checks.add(check_mark(mid + off, size=0.15, width=5).set_stroke(BG, 9, background=True).set_z_index(6))
        self.at(13.4, LaggedStart(*[Create(c) for c in checks], lag_ratio=0.15), run_time=0.5)
        self.at(14.2, FadeOut(checks), run_time=0.4)

        # {#tips}: ACCENT rings mark the two tips
        tip_rings = {k: Circle(radius=0.26).set_stroke(ACCENT, 3).move_to(P[k]).set_z_index(3.5) for k in "DA"}
        self.at("tips", Create(tip_rings["D"]), Create(tip_rings["A"]), ping(P["D"]), ping(P["A"]), run_time=0.55)

        # {#again}: each try is kept in a gallery at the right (a small copy fades in at its slot, drifting in
        # from the left) while the main diamond is recolored. No copy flies across the frame, so nothing
        # half-size ever hovers beside the main diamond.
        # tries on 'Try' (16.25), 17.12 and 'What' (17.99): ~0.87 s apart, the last lands on the question
        thumbs = []
        for i, (old, new, when) in enumerate([(C1, C2, "p2s2"), (C2, C3, 17.12), (C3, C4, "p2s3")]):
            th = thumb(old, SLOTS[i])
            self.at(when, FadeIn(th, shift=RIGHT * 0.5), *[recolor(nodes[k], new[k], delay=0.15) for k in ORDER],
                    run_time=0.75)
            thumbs.append(th)
        gallery = VGroup(*thumbs)

        # pause after "What do you notice?": the tips pulse together, everywhere (each ring about its own centre)
        tip_pulse = [tip_rings[k].animate(rate_func=there_and_back).scale(1.35).set_stroke(width=5) for k in "DA"]
        tip_pulse += [r.animate(rate_func=there_and_back).scale(1.35).set_stroke(width=2.8)
                      for th in thumbs for r in th[2]]
        tip_pulse += [th[1][j].animate(rate_func=there_and_back).scale(1.3)       # ORDER 'BCDA': 2 = D, 3 = A
                      for th in thumbs for j in (2, 3)]
        self.at(19.25, *tip_pulse, run_time=0.8)

        # ============================================================ P3: they always match; start of the why
        arc, apex = eq_arc(P["A"], P["D"])
        badge = eq_badge(apex)
        mini_arcs = VGroup(*[eq_arc(tpos("A", s), tpos("D", s), width=2, dashed=False)[0].set_z_index(8)
                             for s in SLOTS])
        self.at("p3", Create(arc), GrowFromCenter(badge), LaggedStart(*[Create(m) for m in mini_arcs], lag_ratio=0.2),
                run_time=0.75)
        # clear back to hollow
        self.at("p3s1_end", FadeOut(arc), FadeOut(badge), FadeOut(gallery), FadeOut(mini_arcs),
                FadeOut(tip_rings["D"]), FadeOut(tip_rings["A"]), *[unpaint(nodes[k]) for k in ORDER], run_time=0.55)
        # "Here's why:" - the tips step back, the middle comes forward
        outer = [sticks[k] for k in ("DB", "DC", "AB", "AC")]
        self.at("p3s2", *[s.animate.set_stroke(opacity=0.3) for s in outer],
                *[nodes[k].animate.set_stroke(opacity=0.3) for k in "DA"], run_time=0.5)
        # {#middle}: the middle dots
        self.at("middle", ping(P["B"]), ping(P["C"]), run_time=0.7)
        # "joined by a stick"
        self.at(24.1, glow(sticks["BC"]), run_time=0.8)
        # "so they need two different colors"
        self.at(25.6, LaggedStart(paint(nodes["B"], BL), paint(nodes["C"], YE), lag_ratio=0.35), run_time=0.75)

        # ============================================================ P4: each tip gets the leftover
        def rule_out(tip):
            """Blue from B and yellow from C travel up the sticks, then step off them to park beside the tip
            (outside the diamond, clear of the stick lines, so they don't read as new points of the graph)."""
            minis = []
            anims = []
            vy = DOWN if tip == "D" else UP
            for k, c, side in (("B", BL, LEFT), ("C", YE, RIGHT)):
                m = Circle(radius=R_NODE).set_fill(c, 1).set_stroke(c, 3).move_to(P[k]).set_z_index(7)
                on_stick = P[tip] + 0.62 * normalize(P[k] - P[tip])
                park = P[tip] + 0.58 * side + 0.25 * vy
                anims.append(travel(m, [P[k], on_stick, park], end_scale=R_MINI / R_NODE))
                minis.append((m, park))
            return minis, anims

        def leftover_drop(tip, arc):
            """The one palette colour left (pink) flies from its swatch into the tip - the drop grammar of 11.8 s."""
            d = nodes[tip].copy().set_fill(PK, 1).set_stroke(PK, opacity=1).move_to(swatches[2]).set_z_index(7)
            return d, d.animate(path_arc=arc).move_to(P[tip])

        def dim_used(op):
            return [swatches[i].animate.set_opacity(op) for i in (0, 1)]

        # "Each tip" - the top tip comes back
        self.at("p4", nodes["D"].animate.set_stroke(opacity=1), ping(P["D"]), run_time=0.55)
        # {#tip} "both middle dots": its two sticks light up, and their colors travel up to it
        minisD, travD = rule_out("D")
        self.at("tip", sticks["DB"].animate.set_stroke(opacity=1), sticks["DC"].animate.set_stroke(opacity=1),
                *travD, run_time=0.9)
        crossD = VGroup(*[cross_mark(p, size=0.17, width=5).set_stroke(BG, 10, background=True).set_z_index(8) for _, p in minisD])
        # "so": blue and yellow are crossed out beside the tip, and dim on the palette too
        self.at(29.87, *[Create(c) for c in crossD], *dim_used(0.3), run_time=0.4)
        # {#last} "the only color left": the pink swatch pulses and its paint flies into the tip
        pinkD, flyD = leftover_drop("D", -1.5)
        self.at("last", flyD, swatches[2].animate(rate_func=there_and_back).scale(1.3), run_time=0.85)
        nodes["D"].set_fill(PK, 1).set_stroke(PK, opacity=1)
        self.remove(pinkD)
        self.at(31.48, ping(P["D"], PK), run_time=0.5)
        self.at("p4s1_end", *[FadeOut(m) for m, _ in minisD], FadeOut(crossD), *dim_used(1), run_time=0.4)

        # "Both tips get that same leftover" - same at the bottom tip, quicker
        self.at("p4s2", nodes["A"].animate.set_stroke(opacity=1), ping(P["A"]),
                sticks["AB"].animate.set_stroke(opacity=1), sticks["AC"].animate.set_stroke(opacity=1), run_time=0.45)
        minisA, travA = rule_out("A")
        self.at(33.13, *travA, run_time=0.5)
        crossA = VGroup(*[cross_mark(p, size=0.17, width=5).set_stroke(BG, 10, background=True).set_z_index(8) for _, p in minisA])
        self.at(33.66, *[Create(c) for c in crossA], *dim_used(0.3), run_time=0.3)
        # "leftover" (33.97): pink again, a quicker flight (bowing below, clear of the parked minis)
        pinkA, flyA = leftover_drop("A", 0.9)
        self.at(33.95, flyA, run_time=0.5)
        nodes["A"].set_fill(PK, 1).set_stroke(PK, opacity=1)
        self.remove(pinkA)
        self.at(34.45, ping(P["A"], PK, r1=0.42), run_time=0.28)
        # {#match}: the tips match
        arc, apex = eq_arc(P["A"], P["D"])
        badge = eq_badge(apex)
        self.at("match", *[FadeOut(m) for m, _ in minisA], FadeOut(crossA), *dim_used(1), Create(arc),
                GrowFromCenter(badge), run_time=0.6)
        self.at(35.35, ping(P["D"]), ping(P["A"], r1=0.42), badge.animate(rate_func=there_and_back).scale(1.25), run_time=0.7)

        # ============================================================ P5: no problem - 1.73 > 1; the diamond rule
        RX = -1.75
        yA, yD = P["A"][1], P["D"][1]
        ext = VGroup(DashedLine([-0.25, yD, 0], [RX - 0.18, yD, 0], dash_length=0.08),
                     DashedLine([-0.25, yA, 0], [RX - 0.18, yA, 0], dash_length=0.08)).set_stroke(DIM, 1.5, opacity=0.6)
        ruler = DashedLine([RX, yA, 0], [RX, yD, 0], dash_length=0.14).set_stroke(DIM, 3)
        ticks = VGroup(*[Line([RX - 0.14, y, 0], [RX + 0.14, y, 0]).set_stroke(DIM, 3) for y in (yA, yD)])
        self.at("p5", LaggedStart(Create(ext), AnimationGroup(Create(ruler), FadeIn(ticks)), lag_ratio=0.45),
                run_time=1.1)
        # {#dist}: the readout labels the ruler at its mid-height; then a unit stick of length 1 stands on the
        # same floor further left (two bars: a tall '≈ 1.73' and a short '1'); then a check under the readout
        yM = (yA + yD) / 2
        readout = N("≈ 1.73", 34).move_to([RX - 0.22, yM, 0], aligned_edge=RIGHT)
        ok = check_mark(readout.get_center() + DOWN * 0.5, size=0.14, width=5)
        UX = RX - 2.2
        ustick = stick([UX, yA, 0], [UX, yA + U, 0]).set_z_index(1)
        one = N("1", 30, UNIT_COLOR).next_to(ustick, LEFT, buff=0.16)
        floor = DashedLine([RX - 0.18, yA, 0], [UX - 0.2, yA, 0], dash_length=0.08).set_stroke(DIM, 1.5, opacity=0.6)
        self.at("dist", FadeIn(readout, shift=RIGHT * 0.15), run_time=0.45)
        self.at(39.98, Create(floor), GrowFromPoint(ustick, ustick.get_start()), FadeIn(one), run_time=0.65)
        self.at(40.98, Create(ok), run_time=0.4)

        # {#rule}: the card
        body = VGroup(T("diamond rule", 32, ACCENT), T("3 colors: tips match", 26, INK)).arrange(DOWN, buff=0.22)
        box = RoundedRectangle(corner_radius=0.2, width=body.width + 0.6, height=body.height + 0.5)
        box.set_stroke(ACCENT, 2).set_fill(BG, 0.9)
        card = VGroup(box, body).move_to([4.6, 0.45, 0])
        self.at("rule", FadeIn(card, shift=LEFT * 0.5), run_time=0.7)
        # "with any three colors"
        self.at(44.0, LaggedStart(*[s.animate(rate_func=there_and_back).scale(1.35) for s in swatches],
                                  lag_ratio=0.25), run_time=0.85)
        # {#any}: reshuffle twice - the tips still match
        for when, col in (("any", C2), (46.05, C3)):
            self.at(when, *[recolor(nodes[k], col[k]) for k in ORDER],
                    badge.animate(rate_func=there_and_back).scale(1.25), run_time=0.5)

        # ============================================================ out
        self.at(self.t("p5_end") + 0.05, *[FadeOut(m) for m in self.mobjects], run_time=0.85)

