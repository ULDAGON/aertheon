"""S06 - The Moser spindle: at least four colors.

Plan first (force a match, then join with a stick); copy the diamond, hinge it at the bottom tip and swing it
open until the copy's top tip lands on the ring around the first top tip (exactly one unit away); join them.
Walk through a three-coloring that gets stuck, explain it with the diamond rule twice, show that any painting
of the plane paints the spindle too, and move the scoreboard to "at least 4".

Geometry: UNIT = 1.8 manim, shared bottom tip A at (0, -2.0). The first diamond is geom.diamond(pi/2 + PHI/2);
the copy is that diamond rotated clockwise about A by theta, and at theta = PHI it is exactly the second
diamond of geom.moser_spindle() (asserted below).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------- geometry (problem units -> scene)
SC = 1.8
A0 = np.array([0.0, -2.0, 0.0])
NAMES = ["A", "B", "C", "D", "B2", "C2", "D2"]
E1 = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
E2 = [("A", "B2"), ("A", "C2"), ("B2", "C2"), ("B2", "D2"), ("C2", "D2")]
EJ = ("D", "D2")

P_SP, E_SP = moser_spindle()
D1 = diamond(np.pi / 2 + PHI / 2)
assert all(np.allclose(D1[k], P_SP[k]) for k in "ABCD")
assert set(E1 + E2 + [EJ]) == set(E_SP)


def S(p):
    return to_scene(p, SC, A0)


def copy_pts(theta):
    """The copy of the first diamond, rotated clockwise by theta about A (problem units)."""
    return {k2: rot(D1[k], -theta) for k, k2 in (("B", "B2"), ("C", "C2"), ("D", "D2"))}


assert all(np.allclose(copy_pts(PHI)[k], P_SP[k]) for k in ("B2", "C2", "D2"))
assert abs(dist(copy_pts(PHI)["D2"], D1["D"]) - 1) < 1e-12


def gap_at(theta):
    return 2 * SQ3 * np.sin(theta / 2)


FULL = {k: S(v) for k, v in P_SP.items()}
CENTER0 = np.array([0.0, (FULL["A"][1] + FULL["D"][1]) / 2, 0.0])


def seg_cross(a, b, c, d):
    r, s = b - a, d - c
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-12:
        return None
    t = ((c - a)[0] * s[1] - (c - a)[1] * s[0]) / den
    u = ((c - a)[0] * r[1] - (c - a)[1] * r[0]) / den
    return a + t * r if (1e-6 < t < 1 - 1e-6 and 1e-6 < u < 1 - 1e-6) else None


CROSSINGS = []
for i, e in enumerate(E_SP):
    for f in E_SP[i + 1:]:
        if set(e) & set(f):
            continue
        x = seg_cross(FULL[e[0]], FULL[e[1]], FULL[f[0]], FULL[f[1]])
        if x is not None:
            CROSSINGS.append(x)
assert len(CROSSINGS) == 4

# ---------------------------------------------------------------- style helpers
R_NODE = 0.11
Z_STICK, Z_FLASH, Z_NODE, Z_MARK = 1, 2, 4, 6
TRIO = [BLUE_P, YELLOW_P, PINK_P]
TINT = interpolate_color(ManimColor(UNIT_COLOR), ManimColor(ACCENT), 0.45)   # the copy's sticks, P1-P2
POSE_S = 1.25                                  # P3 onwards: the finished spindle is shown 1.25x larger ...
POSE_C = CENTER0 + UP * 0.15                   # ... about a point a little above its middle (A stays clear of the bar)


def posed(p):
    return POSE_C + POSE_S * (np.asarray(p) - CENTER0)


def node(pos, rim=INK, r=R_NODE):
    return Circle(radius=r).move_to(pos).set_fill(BG, 1).set_stroke(rim, 3).set_z_index(Z_NODE)


def halo(pos, color=ACCENT, r=R_NODE + 0.02, k=3.6, width=4):
    """An expanding, fading ring (use for 'this dot' flashes)."""
    c = Circle(radius=r).set_stroke(color, width).move_to(pos).set_z_index(Z_MARK)
    return FadeOut(c, scale=k)


def paint(n, color, rim=None):
    return AnimationGroup(n.animate.set_fill(color, 1).set_stroke(rim or color, 3, opacity=1),
                          halo(n.get_center(), color))


def unpaint(n, rim=INK):
    return n.animate.set_fill(BG, 1).set_stroke(rim, 3, opacity=1)


def passing(line, color=ACCENT, width=8, tw=0.6):
    c = line.copy().set_stroke(color, width, opacity=1).set_z_index(Z_FLASH)
    return ShowPassingFlash(c, time_width=tw)


def glow(lines, color=ACCENT, width=7):
    return AnimationGroup(*[l.animate(rate_func=there_and_back).set_stroke(color, width) for l in lines])


def xmark(pos, color=BAD, s=0.15, w=3.5):
    """A cross with a dark under-stroke, so it stays legible on a red stick or a pink swatch."""
    p = np.asarray(pos)
    x = VGroup(Line(p + s * UL, p + s * DR), Line(p + s * UR, p + s * DL)).set_stroke(color, w)
    return x.set_stroke(BG, w + 5, background=True).set_z_index(Z_MARK)


def swatch(pos, color, r=0.15):
    return Circle(radius=r).set_fill(color, 1).set_stroke(BG, 2).move_to(pos).set_z_index(Z_MARK)


def slash(pos, color=INK, s=0.21, w=4):
    """'Taken': one diagonal strike through a swatch (same idea as the scoreboard's strikes)."""
    p = np.asarray(pos)
    return Line(p + s * DL, p + s * UR).set_stroke(color, w).set_z_index(Z_MARK + 1)


def same_arc(a, b, angle, color=ACCENT, size=34):
    """Dashed 'same colour' arc from a to b with an '=' on a BG disc at its apex."""
    arc = ArcBetweenPoints(a, b, angle=angle)
    dashed = DashedVMobject(arc, num_dashes=28, dashed_ratio=0.55).set_stroke(color, 3).set_z_index(Z_FLASH)
    at = arc.point_from_proportion(0.5)
    eq = VGroup(Circle(radius=0.2 * size / 34).set_fill(BG, 1).set_stroke(width=0), N("=", size, color)).move_to(at)
    eq[1].move_to(at + 0.03 * UP)
    return dashed, eq.set_z_index(Z_MARK)


def draw_arcs(scene, pairs):
    """Animations that draw dashed '=' arcs. Each BG disc goes in first (invisible on the background) so the
    dashes never show through a half-faded glyph; only the '=' glyph fades in."""
    anims = []
    for arc, eq in pairs:
        eq[1].set_opacity(0)
        scene.add(eq)
        anims += [Create(arc), eq[1].animate.set_opacity(1)]
    return anims


def cruise(a, e0=0.05, e1=0.12):
    """Near-constant speed with short eases at both ends (so the swing visibly moves while it is described)."""
    v = 1 / (1 - (e0 + e1) / 2)
    if a < e0:
        return v * a * a / (2 * e0)
    if a > 1 - e1:
        return 1 - v * (1 - a) ** 2 / (2 * e1)
    return v * (a - e0 / 2)


def card(*rows, buff=0.1):
    txt = VGroup(*rows).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 0.42, height=txt.height + 0.3)
    box.set_fill(BG, 1).set_stroke(DIM, 1.5).move_to(txt)
    return VGroup(box, txt)


# ---------------------------------------------------------------- the spindle as a posable drawing
class Spindle:
    """Seven nodes and eleven sticks placed from the geometry. The copy follows `theta`; the whole drawing can be
    posed (scale s, rotation r, centre c) without shrinking the dots to nothing."""

    def __init__(self):
        self.nodes = {k: node(ORIGIN, ACCENT if k in ("B2", "C2", "D2") else INK) for k in NAMES}
        self.sticks = {e: Line(LEFT, RIGHT, color=UNIT_COLOR, stroke_width=4).set_z_index(Z_STICK) for e in E1 + E2}
        self.join = None
        self.shadow = None   # optional BG under-strokes (one per stick) so the sticks cut through a painted plane
        self.theta = 0.0
        self.apply(0.0)

    def make_shadow(self, sw=4.0, extra=6.0):
        self.shadow_extra = extra
        self.shadow = {e: Line(l.get_start(), l.get_end()).set_stroke(BG, sw + extra)
                       .set_z_index(Z_STICK - 0.5) for e, l in self.all_sticks().items()}
        return VGroup(*self.shadow.values())

    def pts(self, theta, s=1.0, r=0.0, c=None):
        P = {k: D1[k] for k in "ABCD"}
        P.update(copy_pts(theta))
        out = {k: S(v) for k, v in P.items()}
        if s != 1.0 or r != 0.0 or c is not None:
            c = CENTER0 if c is None else np.asarray(c)
            out = {k: c + s * rotate_vector(v - CENTER0, r) for k, v in out.items()}
        return out

    def apply(self, theta, s=1.0, r=0.0, c=None, rn=R_NODE, sw=4.0):
        self.theta = theta
        p = self.pts(theta, s, r, c)
        for k, n in self.nodes.items():
            n.scale(rn / (n.width / 2)).move_to(p[k])
        for (a, b), l in self.all_sticks().items():
            l.put_start_and_end_on(p[a], p[b])
            l.set_stroke(width=sw)
            if self.shadow is not None:
                self.shadow[(a, b)].put_start_and_end_on(p[a], p[b]).set_stroke(width=sw + self.shadow_extra)
        return p

    def all_sticks(self):
        d = dict(self.sticks)
        if self.join is not None:
            d[EJ] = self.join
        return d

    def n(self, *ks):
        return [self.nodes[k] for k in ks]

    def s(self, *es):
        return [self.all_sticks()[e] for e in es]

    @property
    def first(self):
        return VGroup(*self.s(*E1), *self.n("A", "B", "C", "D"))

    @property
    def copy_nodes(self):
        return VGroup(*self.n("B2", "C2", "D2"))

    @property
    def copy_sticks(self):
        return VGroup(*self.s(*E2))

    @property
    def group(self):
        return VGroup(*self.all_sticks().values(), *self.nodes.values())


# ---------------------------------------------------------------- the three-colour mosaic (scene P6)
def clip_halfplane(poly, n, c):
    """Keep the part of polygon `poly` with n . p <= c (Sutherland-Hodgman)."""
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = n @ p - c, n @ q - c
        if fp <= 0:
            out.append(p)
        if fp * fq < 0:
            out.append(p + (q - p) * (fp / (fp - fq)))
    return out


def make_mosaic(rect, spacing=0.9, seed=29):
    x0, x1, y0, y1 = rect
    rng = np.random.RandomState(seed)
    seeds = []
    for j, y in enumerate(np.arange(y0 - spacing, y1 + spacing, spacing * 0.87)):
        for x in np.arange(x0 - spacing, x1 + spacing, spacing):
            seeds.append([x + (0.5 * spacing if j % 2 else 0) + rng.uniform(-0.32, 0.32) * spacing,
                          y + rng.uniform(-0.32, 0.32) * spacing])
    seeds = np.array(seeds)
    cols = rng.randint(0, 3, len(seeds))
    cells = []
    box = [np.array(v, float) for v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    for i, s in enumerate(seeds):
        poly = box
        d = np.linalg.norm(seeds - s, axis=1)
        for j in np.argsort(d)[1:28]:
            n = seeds[j] - s
            poly = clip_halfplane(poly, n, n @ ((s + seeds[j]) / 2))
            if len(poly) < 3:
                break
        if len(poly) >= 3:
            cells.append((poly, cols[i]))
    return seeds, cols, cells


def sample(seeds, cols, p):
    """Colour index under point p and its distance to the nearest cell border."""
    p = np.asarray(p)[:2]
    d2 = np.sum((seeds - p) ** 2, axis=1)
    i = int(np.argmin(d2))
    others = np.delete(np.arange(len(seeds)), i)
    margin = np.min((d2[others] - d2[i]) / (2 * np.linalg.norm(seeds[others] - seeds[i], axis=1)))
    return int(cols[i]), float(margin)


class S06_Spindle(TimedScene):
    def w(self, sid, word, nth=0):
        """Start time of a spoken word (first match in sentence `sid`)."""
        for s in self.tl["sentences"]:
            if s["id"] == sid:
                hits = [x["s"] for x in s["words"] if x["w"].strip(".,:;?!'").lower() == word.lower()]
                return hits[nth]
        raise KeyError((sid, word))

    def construct(self):
        sp = Spindle()
        nd = sp.nodes

        # ------------------------------------------------------------ persistent furniture
        bar = BoundsBar(lo=3).scale(0.8).to_edge(DOWN, buff=0.3).set_z_index(10)
        panel_top = bar.get_top()[1] + 0.2
        panel = Rectangle(width=config.frame_width + 0.2, height=panel_top + config.frame_height / 2 + 0.1)
        panel.set_fill(BG, 1).set_stroke(width=0).set_z_index(9)
        panel.move_to([0, (panel_top - config.frame_height / 2 - 0.1) / 2, 0])

        badge = card(T("diamond rule", 28, ACCENT), T("3 colors: tips match", 24, INK)).to_corner(UL, buff=0.35)
        plan_h = T("plan", 24, DIM)
        plan1 = T("1. force a match", 24, INK)
        plan2 = T("2. join them with a stick", 24, INK)
        plan = VGroup(plan_h, plan1, plan2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        plan.next_to(badge, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 0.12)

        # ============================================================ P1: the plan, the copy, the hinge, the ring
        first = sp.first
        self.until(0.85, FadeIn(bar), FadeIn(badge), FadeIn(first))
        self.add(panel)
        self.at("plan_match", FadeIn(plan_h, shift=RIGHT * 0.15), FadeIn(plan1, shift=RIGHT * 0.15), run_time=0.6)
        self.at("plan_stick", FadeIn(plan2, shift=RIGHT * 0.15), run_time=0.6)
        # "Take the diamond"
        self.at(self.w("p1s2", "diamond") - 0.05, glow(sp.s(*E1)), run_time=0.7)

        # "copy it": an identical copy lifts off with a glow and settles exactly on top. Its sticks keep a faint
        # gold tint (until P3) so the swing reads as a second object opening, not as a white tangle.
        cp_sticks, cp_nodes = sp.copy_sticks, sp.copy_nodes
        cpA = node(nd["A"].get_center(), ACCENT)
        mover = VGroup(cp_sticks, cp_nodes)
        self.add(mover, cpA)
        cpA.save_state()
        off = UP * 0.3 + RIGHT * 0.35
        self.at("copy", mover.animate.shift(off).set_stroke(ACCENT), cpA.animate.shift(off), run_time=0.55)
        self.play(cp_sticks.animate.shift(-off).set_stroke(TINT), cp_nodes.animate.shift(-off), Restore(cpA),
                  run_time=0.6)
        self.remove(cpA)
        # "hinged at the bottom tip": a pin on A
        pin = VGroup(Circle(radius=0.24).set_stroke(ACCENT, 3),
                     Dot(radius=0.035, color=ACCENT)).move_to(nd["A"]).set_z_index(Z_MARK)
        self.at(self.w("p1s2", "hinged") + 0.5, GrowFromCenter(pin), run_time=0.45)
        # "like scissors": the copy opens a little and closes
        wig = ValueTracker(0.0)
        gt = ValueTracker(0.0)  # global time, drives the swing
        t_sw, t_re = self.t("swing"), self.t("reach")

        def copy_angle():
            a = np.clip((gt.get_value() - t_sw) / (t_re - t_sw), 0, 1)
            return wig.get_value() + PHI * cruise(a)

        def upd_copy(m):
            p = sp.pts(copy_angle())
            for k in ("B2", "C2", "D2"):
                nd[k].move_to(p[k])
            for (a, b) in E2:
                sp.sticks[(a, b)].put_start_and_end_on(p[a], p[b])

        mover.add_updater(upd_copy)
        self.at("scissors", wig.animate(rate_func=there_and_back).set_value(5 * DEGREES), run_time=0.9)

        # "the ring around its top tip": a radius stick sweeps once round D
        Dp = nd["D"].get_center()
        ring = Circle(radius=SC, color=UNIT_COLOR, stroke_width=2.5).move_to(Dp).set_z_index(0)
        ring.set_stroke(opacity=0.8)
        radius = Line(Dp, Dp + RIGHT * SC, color=UNIT_COLOR, stroke_width=3).set_z_index(Z_STICK)
        self.at("ring", Create(ring), Rotate(radius, TAU, about_point=Dp), run_time=1.3)
        self.play(FadeOut(radius), run_time=0.3)

        # ============================================================ P2: swing it open until the tip lands on the ring
        trail = VMobject()
        gap_line = VMobject()
        gap_lab = T("gap", 26, DIM)
        gap_num = N("0.00", 32, INK)
        readout = VGroup(gap_lab, gap_num).arrange(RIGHT, buff=0.16)
        readout.move_to([FULL["D2"][0] + 0.45, FULL["D2"][1], 0], aligned_edge=LEFT).set_z_index(Z_MARK)
        center_halo = Circle(radius=R_NODE + 0.02).set_stroke(ACCENT, 4).move_to(Dp).set_z_index(Z_MARK)
        center_halo.set_stroke(opacity=0)
        ones = VGroup(*[N("1", 28, TINT).set_stroke(BG, 6, background=True).set_z_index(Z_MARK) for _ in E2])
        t_keeps = self.t("keeps")
        t_center = self.w("p2s3", "ring's") - 0.05
        TH_D = np.arctan2(Dp[1] - A0[1], Dp[0] - A0[0])

        def ramp(t, a, b):
            return float(np.clip((t - a) / (b - a), 0, 1))

        def upd_swing(m):
            t = gt.get_value()
            th = copy_angle()
            p = sp.pts(th)
            # trail of the moving tip: arc of radius sqrt(3) about A
            if th > 1e-3:
                trail.become(Arc(radius=SQ3 * SC, start_angle=TH_D, angle=-th, arc_center=A0)
                             .set_stroke(DIM, 2.5, opacity=0.55))
            if np.linalg.norm(p["D2"] - p["D"]) > 0.12:
                gap_line.become(DashedLine(p["D"], p["D2"], dash_length=0.08, dashed_ratio=0.5)
                                .set_stroke(DIM, 2.5).set_z_index(Z_FLASH))
            o = ramp(t, t_sw, t_sw + 0.4)
            gap_num.become(N(f"{gap_at(th):.2f}", 32, INK).next_to(gap_lab, RIGHT, buff=0.16).set_z_index(Z_MARK))
            readout.set_opacity(o)
            # "Every stick keeps its length": 1-labels ride on the copy's sticks
            lo = ramp(t, t_keeps, t_keeps + 0.35) * (1 - ramp(t, t_keeps + 2.8, t_keeps + 3.2))
            cc = (p["A"] + p["D2"]) / 2
            for lab, (a, b) in zip(ones, E2):
                mid = (p[a] + p[b]) / 2
                dv = p[b] - p[a]
                nrm = np.array([-dv[1], dv[0], 0]) / np.linalg.norm(dv)
                ref = p["D2"] if (a, b) == ("B2", "C2") else cc
                side = -1 if np.dot(nrm, (mid - ref) if (a, b) != ("B2", "C2") else (ref - mid)) < 0 else 1
                lab.move_to(mid + side * 0.28 * nrm).set_opacity(lo)
            # "the ring's centre": a soft ring on D
            h = ramp(t, t_center, t_center + 0.7)
            center_halo.scale_to_fit_width(2 * (R_NODE + 0.02) * (1 + 2.2 * h)).move_to(Dp)
            center_halo.set_stroke(opacity=(1 - h) if h > 0 else 0)

        swing_grp = VGroup(trail, gap_line, readout, ones, center_halo)
        swing_grp.add_updater(upd_swing)
        self.add(swing_grp)
        gt.set_value(self.now)
        self.until("reach", gt.animate(rate_func=linear).set_value(t_re))
        swing_grp.clear_updaters()
        mover.clear_updaters()
        sp.apply(PHI)
        self.remove(ones, center_halo)

        # landing: the tip is on the ring, the gap reads 1.00
        D2p = nd["D2"].get_center()
        self.at("reach", halo(D2p, ACCENT, k=4.2, width=5), gap_num.animate.set_color(ACCENT),
                ring.animate.set_stroke(opacity=1), run_time=0.6)
        # "Stop there": the readout pulses (about its left edge, so it never runs into the 'gap' label)
        self.at("p2s4", gap_num.animate(rate_func=there_and_back).scale(1.35, about_edge=LEFT), run_time=0.6)
        # "exactly one unit": the gap itself and the unit ring light up together
        self.at(self.w("p2s4", "one") - 0.05, gap_line.animate(rate_func=there_and_back).set_stroke(ACCENT, 5),
                ring.animate(rate_func=there_and_back).set_stroke(width=6), run_time=0.7)
        sp.join = Line(Dp, D2p, color=UNIT_COLOR, stroke_width=4).set_z_index(Z_STICK)
        self.at("join", Create(sp.join), FadeOut(gap_line),
                plan2.animate(rate_func=there_and_back_with_pause).set_color(ACCENT), run_time=0.7)

        # ------------------------------------------------------------ posing the whole spindle
        pose = {"s": 1.0, "r": 0.0, "c": CENTER0.copy(), "rn": R_NODE, "sw": 4.0}
        HOME = {"s": POSE_S, "r": 0.0, "c": POSE_C.copy(), "rn": R_NODE, "sw": 4.0}

        def glide(to, hollow=False, **anim_kw):
            """Move/scale/rotate the whole spindle (dots keep a readable size); optionally clear its paint."""
            fr = dict(pose)
            n0 = {k: (nd[k].get_fill_color(), nd[k].get_stroke_color(), nd[k].get_stroke_width()) for k in NAMES}
            l0 = {e: l.get_stroke_color() for e, l in sp.all_sticks().items()}

            def f(m, a):
                a = smooth(a)
                q = {k: fr[k] + (to[k] - fr[k]) * a for k in ("s", "r", "rn", "sw")}
                sp.apply(PHI, q["s"], q["r"], fr["c"] + (to["c"] - fr["c"]) * a, q["rn"], q["sw"])
                if hollow:
                    for k in NAMES:
                        f0, s0, w0 = n0[k]
                        nd[k].set_fill(interpolate_color(f0, ManimColor(BG), a), 1)
                        nd[k].set_stroke(interpolate_color(s0, ManimColor(INK), a), w0 + (3 - w0) * a, opacity=1)
                    for e, l in sp.all_sticks().items():
                        l.set_stroke(interpolate_color(l0[e], ManimColor(UNIT_COLOR), a))
            pose.update(to)
            return UpdateFromAlphaFunc(sp.group, f, **anim_kw)

        # pause after P2: the ring and readout fade while the finished spindle grows 1.25x (dots keep their size),
        # so the crowded middle is easier to read for the colouring story
        self.at("p2_end", FadeOut(readout), glide(HOME),
                *[m.animate.scale(POSE_S, about_point=CENTER0).shift(POSE_C - CENTER0).set_stroke(opacity=0)
                  for m in (ring, trail)],
                FadeOut(pin, shift=posed(A0) - A0), run_time=0.85)
        self.remove(ring, trail)

        # ============================================================ P3: seven dots, eleven sticks, crossings
        cnt7 = VGroup(N("7", 36), T("dots", 28, DIM)).arrange(RIGHT, buff=0.2)
        cnt11 = VGroup(N("11", 36), T("sticks", 28, DIM)).arrange(RIGHT, buff=0.2)
        VGroup(cnt7, cnt11).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([4.6, 1.55, 0])
        cnt7.shift(RIGHT * (cnt11[0].get_right()[0] - cnt7[0].get_right()[0]))
        self.at("p3", LaggedStart(*[halo(nd[k].get_center(), ACCENT) for k in NAMES], lag_ratio=0.12),
                *[nd[k].animate.set_stroke(INK) for k in ("B2", "C2", "D2")],
                *[l.animate.set_stroke(UNIT_COLOR) for l in sp.s(*E2)],
                FadeIn(cnt7, shift=LEFT * 0.2), run_time=0.9)
        order = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), EJ,
                 ("C2", "D2"), ("B2", "D2"), ("B2", "C2"), ("A", "C2"), ("A", "B2")]
        self.at("count", LaggedStart(*[passing(l) for l in sp.s(*order)], lag_ratio=0.1),
                FadeIn(cnt11, shift=LEFT * 0.2), run_time=0.9)
        # "where sticks cross, there's no dot": the real dots turn solid; each crossing gets a dashed, empty
        # ring (bigger than a dot, and broken, so it cannot read as one); the tag points at the isolated top one
        CR = [posed(x) for x in CROSSINGS]
        xs = VGroup(*[DashedVMobject(Circle(radius=0.165), num_dashes=10, dashed_ratio=0.55)
                      .set_stroke(DIM, 3).move_to(x).set_z_index(Z_MARK) for x in CR])
        top_x = max(CR, key=lambda p: p[1])
        leader = Line([2.0, top_x[1], 0], top_x + RIGHT * 0.21).set_stroke(DIM, 2).set_z_index(Z_MARK)
        not_dot = T("not a dot", 26, DIM).next_to(leader.get_start(), RIGHT, buff=0.12)
        self.at("crossings", LaggedStart(*[GrowFromCenter(c) for c in xs], lag_ratio=0.15),
                *[n.animate.set_fill(INK, 1) for n in sp.nodes.values()],
                Create(leader), FadeIn(not_dot, shift=LEFT * 0.15), run_time=0.6)
        self.at(self.w("p3s1", "dot") - 0.05, *[FadeOut(c) for c in xs], FadeOut(not_dot), FadeOut(leader),
                *[n.animate.set_fill(BG, 1) for n in sp.nodes.values()], run_time=0.45)

        sw_lab = T("3 colors", 26, DIM)
        sws = VGroup(*[Circle(radius=0.2).set_fill(c, 1).set_stroke(BG, 2) for c in TRIO]).arrange(RIGHT, buff=0.24)
        VGroup(sw_lab, sws).arrange(DOWN, buff=0.22).move_to([-5.3, -0.9, 0])
        self.at("p3s2", FadeIn(sw_lab), LaggedStart(*[GrowFromCenter(s) for s in sws], lag_ratio=0.2), run_time=0.7)
        pause_icon = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.16, height=0.52)
                              .set_fill(ACCENT, 1).set_stroke(width=0) for _ in range(2)]).arrange(RIGHT, buff=0.14)
        pause_icon.to_corner(UR, buff=0.55)
        self.at("try", FadeIn(pause_icon, scale=0.8), run_time=0.5)
        self.at("p3_end", LaggedStart(*[s.animate(rate_func=there_and_back).scale(1.18) for s in sws],
                                      lag_ratio=0.25), run_time=0.9)

        # ============================================================ P4: a three-colouring gets stuck
        cp_all = [*sp.s(*E2), sp.join, *sp.n("B2", "C2", "D2")]
        a_ring = Circle(radius=0.24).set_stroke(ACCENT, 3).move_to(nd["A"]).set_z_index(Z_MARK)
        self.at("p4", FadeOut(pause_icon), FadeOut(cnt7), FadeOut(cnt11),
                *[m.animate.set_stroke(opacity=0.3) for m in cp_all], Create(a_ring), run_time=0.5)
        self.at(self.w("p4s1", "pink") - 0.05, paint(nd["A"], PINK_P), FadeOut(a_ring), run_time=0.45)
        # "the first diamond's middle dots": rings on B and C, each fading as its dot is painted
        mid_rings = {k: Circle(radius=0.24).set_stroke(ACCENT, 3).move_to(nd[k]).set_z_index(Z_MARK) for k in "BC"}
        self.at(self.w("p4s2", "middle") - 0.05, *[Create(r) for r in mid_rings.values()], run_time=0.4)
        self.at(self.w("p4s2", "blue") - 0.12, paint(nd["B"], BLUE_P), FadeOut(mid_rings["B"]), run_time=0.4)
        self.at(self.w("p4s2", "yellow") - 0.12, paint(nd["C"], YELLOW_P), FadeOut(mid_rings["C"]), run_time=0.4)
        # "its top tip gets the leftover": blue and yellow are taken
        Dp = nd["D"].get_center()
        d_sw = VGroup(swatch(Dp + LEFT * 1.12, BLUE_P), swatch(Dp + LEFT * 0.66, YELLOW_P))
        d_x = VGroup(*[slash(s.get_center()) for s in d_sw])
        self.at("first_top", glow(sp.s(("B", "D"), ("C", "D")), INK, 8),
                LaggedStart(*[GrowFromCenter(s) for s in d_sw], lag_ratio=0.3), run_time=0.6)
        self.play(LaggedStart(*[Create(x) for x in d_x], lag_ratio=0.3), run_time=0.45)
        self.at(self.w("p4s2", "pink") - 0.05, paint(nd["D"], PINK_P), run_time=0.45)
        # the second diamond goes the same way ...
        self.at("second", *[m.animate.set_stroke(opacity=1) for m in cp_all if m is not sp.join],
                *[FadeOut(m) for m in (*d_sw, *d_x)], run_time=0.5)
        self.play(paint(nd["B2"], YELLOW_P), paint(nd["C2"], BLUE_P),
                  *[passing(l, INK, width=8) for l in sp.s(("A", "B2"), ("A", "C2"), ("B2", "C2"))], run_time=0.6)
        D2p = nd["D2"].get_center()
        e_sw = VGroup(swatch(D2p + RIGHT * 0.66, YELLOW_P), swatch(D2p + RIGHT * 1.12, BLUE_P))
        e_x = VGroup(*[slash(s.get_center()) for s in e_sw])
        need = swatch(D2p + RIGHT * 1.78, PINK_P)
        need_lab = T("needs", 24, DIM).next_to(need, UP, buff=0.16)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in e_sw], lag_ratio=0.3),
                  glow(sp.s(("B2", "D2"), ("C2", "D2")), INK, 8), run_time=0.55)
        self.play(LaggedStart(*[Create(x) for x in e_x], lag_ratio=0.3), GrowFromCenter(need), FadeIn(need_lab),
                  run_time=0.5)
        # ... but the new stick rules out pink: pink travels from D along the new stick to D2
        self.at(self.w("p4s3", "new") - 0.05, sp.join.animate.set_stroke(INK, 7, opacity=1),
                passing(sp.join, PINK_P, width=11, tw=0.55), run_time=0.6)
        qm = N("?", 38, BAD).next_to(nd["D2"], UP, buff=0.2).set_z_index(Z_MARK)
        need_x = xmark(need.get_center(), BAD, s=0.21, w=6)
        self.at("stuck", Create(need_x), halo(D2p, BAD, k=4, width=5), FadeIn(qm, scale=0.6),
                nd["D2"].animate.set_stroke(BAD), sp.join.animate.set_stroke(UNIT_COLOR, 4), run_time=0.6)

        # ============================================================ P5: it's the diamond rule, twice
        self.at("p5", *[unpaint(n) for n in sp.n("B", "C", "D", "B2", "C2", "D2")],
                *[FadeOut(m) for m in (*e_sw, *e_x, need, need_lab, need_x, qm)], run_time=0.6)
        lit = badge.copy().scale(1.08)
        lit[0].set_stroke(ACCENT, 3)
        self.at(self.w("p5s2", "diamond") - 0.05, Transform(badge, lit, rate_func=there_and_back), run_time=0.7)
        self.at("twice", Succession(glow(sp.s(*E1), ACCENT, 7), glow(sp.s(*E2), ACCENT, 7)), run_time=0.9)
        tip_rings = VGroup(*[Circle(radius=0.24).set_stroke(ACCENT, 3).move_to(nd[k]).set_z_index(Z_MARK)
                             for k in ("D", "D2")])
        self.at("both_tips", *[Create(r) for r in tip_rings], run_time=0.5)
        Ap = nd["A"].get_center()
        arcL, eqL = same_arc(Ap, Dp, -3.0)
        arcR, eqR = same_arc(Ap, D2p, 3.0)
        self.at("bottom_tip", *draw_arcs(self, [(arcL, eqL), (arcR, eqR)]), run_time=0.8)
        self.play(paint(nd["D"], PINK_P), paint(nd["D2"], PINK_P), run_time=0.45)
        # "so they match each other": a clear arch over the join, and the two pink tips pulse together
        arcT, eqT = same_arc(Dp, D2p, -2.2, size=40)
        self.at("same", *draw_arcs(self, [(arcT, eqT)]),
                *[nd[k].animate(rate_func=there_and_back).scale(1.3) for k in ("D", "D2")],
                plan1.animate(rate_func=there_and_back_with_pause).set_color(ACCENT), run_time=0.9)
        self.at(self.w("p5s4", "joined") - 0.05, sp.join.animate.set_stroke(INK, 7), run_time=0.5)
        clash_x = xmark((Dp + D2p) / 2, BAD, s=0.2, w=6)
        whole = VGroup(sp.group, tip_rings, arcL, arcR, arcT, eqL, eqR, eqT)
        self.at("clash", sp.join.animate.set_stroke(BAD, 7), Create(clash_x), run_time=0.35)
        self.play(VGroup(whole, clash_x).animate(rate_func=wiggle).shift(RIGHT * 0.09), run_time=0.45)

        # ============================================================ P6: every painting paints the spindle
        M_RECT = (-3.5, 7.3, panel.get_top()[1], 4.2)
        X_CUT = -2.3   # patches whose centre lies left of this are left out: a ragged edge, clear of the plan text
        seeds, cols, cells = make_mosaic(M_RECT)
        soft = [interpolate_color(ManimColor(BG), ManimColor(c), 0.74) for c in TRIO]
        mosaic = VGroup(*[Polygon(*[np.array([x, y, 0]) for x, y in poly]).set_fill(soft[c], 1)
                          .set_stroke(soft[c], 1.5) for poly, c in cells
                          if np.mean(np.array(poly)[:, 0]) >= X_CUT]).set_z_index(-2)
        # dark under-strokes so the sticks and dots cut cleanly through the painted plane
        shadow = sp.make_shadow(sw=pose["sw"], extra=6)
        for n in sp.nodes.values():
            n.set_stroke(BG, 8, background=True)
        self.add(shadow)
        self.at("p6", *[FadeOut(m) for m in (*tip_rings, arcL, arcR, arcT, eqL, eqR, eqT, clash_x)],
                sp.join.animate.set_stroke(UNIT_COLOR, 4), *[unpaint(n) for n in sp.n("A", "D", "D2")],
                FadeIn(mosaic), run_time=0.8)

        # two landing poses where exactly one stick gets matching ends and every dot sits clearly inside a patch;
        # prefer an outer stick (easy to see), and a different one each time
        SMALL = 0.65
        OUTER = {("A", "B"), ("B", "D"), EJ, ("C2", "D2"), ("A", "C2")}

        def evaluate(c, r):
            p = sp.pts(PHI, SMALL, r, c)
            cm = {k: sample(seeds, cols, v) for k, v in p.items()}
            bad = [e for e in E_SP if cm[e[0]][0] == cm[e[1]][0]]
            return min(m for _, m in cm.values()), bad, {k: v[0] for k, v in cm.items()}

        def best(xr, yr, rr, avoid=()):
            found = None
            for x in np.arange(*xr, 0.1):
                for y in np.arange(*yr, 0.1):
                    for r in rr:
                        m, bad, cm = evaluate(np.array([x, y, 0]), r)
                        if len(bad) != 1 or m < 0.08 or bad[0] in avoid:
                            continue
                        score = m + (0.2 if bad[0] in OUTER else 0)
                        if found is None or score > found[0]:
                            found = (score, np.array([x, y, 0]), r, bad, cm)
            assert found is not None
            return found

        land1 = best((-1.1, 1.2), (0.8, 2.45), np.radians(np.arange(10, 51, 5)))
        land2 = best((2.8, 5.45), (-1.35, 1.0), np.radians(np.arange(-50, -9, 5)), avoid=land1[3])

        def land(found):
            _, c, r, bad, cm = found
            return {"s": SMALL, "r": r, "c": c, "rn": 0.1, "sw": 3.5}, bad, cm

        to1, bad1, cm1 = land(land1)
        to2, bad2, cm2 = land(land2)

        def broken(bad):
            """The offending stick turns BAD (thick, over a dark under-stroke) and gets the P5 'rule broken' cross."""
            anims, marks = [], VGroup()
            for e in bad:
                l = sp.all_sticks()[e]
                marks.add(xmark(l.get_center(), BAD, s=0.22, w=5))
                anims += [l.animate.set_stroke(BAD, 9), sp.shadow[e].animate.set_stroke(width=15),
                          *[nd[k].animate(rate_func=there_and_back).scale(1.5) for k in e],   # same colour, both ends
                          FadeOut(l.copy().set_stroke(BAD, 18, opacity=0.6).set_z_index(Z_FLASH), scale=1.25)]
            return anims + [Create(marks)], marks   # one group: FadeOut(marks) later removes it for good

        def paint_all(cm):
            return [nd[k].animate.set_fill(TRIO[cm[k]], 1).set_stroke(INK, 2) for k in NAMES]

        self.at(self.w("p6s1", "plane"), glide(to1), run_time=0.6)
        self.at("sits", *paint_all(cm1), run_time=0.35)
        an1, x1 = broken(bad1)
        self.at(self.w("p6s1", "seven"), *an1, run_time=0.4)
        self.at(66.0, glide(to2, hollow=True), FadeOut(x1), run_time=0.55)
        self.play(*paint_all(cm2), run_time=0.3)
        an2, x2 = broken(bad2)
        self.at(66.9, *an2, run_time=0.4)
        self.at(68.0, FadeOut(mosaic), FadeOut(sw_lab), *[FadeOut(s) for s in sws], FadeOut(x2),
                glide(HOME, hollow=True), run_time=0.9)
        self.remove(shadow)
        sp.shadow = None
        for n in sp.nodes.values():
            n.set_stroke(BG, 0, background=True)
        # the scoreboard: at least four
        bar4 = BoundsBar(lo=4).scale(0.8).to_edge(DOWN, buff=0.3).set_z_index(10)
        moves = [Transform(bar.box, bar4.box)]
        for c, s, c4, s4 in zip(bar.cells, bar.strikes, bar4.cells, bar4.strikes):
            moves += [c.animate.set_color(c4.get_color()), s.animate.set_stroke(opacity=s4.get_stroke_opacity())]
        bar.lo = 4
        self.at("four", AnimationGroup(*moves), run_time=0.6)
        self.play(FadeOut(bar4.box.copy().set_stroke(ACCENT, 6).set_z_index(11), scale=1.18),
                  bar.cells[3].animate(rate_func=there_and_back).scale(1.3).set_color(ACCENT), run_time=0.6)

        # ============================================================ P7: the Moser spindle; force + forbid
        title = T("Moser spindle", 36).move_to([0, 3.25, 0])
        who = T("Leo and William Moser", 26, DIM)
        yr = VGroup(T("·", 26, DIM), N("1961", 28, DIM)).arrange(RIGHT, buff=0.15)
        cap = VGroup(who.copy(), yr).arrange(RIGHT, buff=0.18).next_to(title, DOWN, buff=0.22)
        who.next_to(title, DOWN, buff=0.22)
        self.at("moser", FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        self.at("brothers", FadeIn(who, shift=DOWN * 0.1), run_time=0.6)
        self.at("year", who.animate.move_to(cap[0]), FadeIn(yr, shift=LEFT * 0.15), run_time=0.6)
        arcL, eqL = same_arc(Ap, Dp, -3.0)
        arcR, eqR = same_arc(Ap, D2p, 3.0)
        lab_force = T("force", 30, ACCENT).next_to(eqL, LEFT, buff=0.3).set_z_index(Z_MARK + 1)
        lab_forbid = T("forbid", 30, BAD).next_to(nd["D2"], RIGHT, buff=0.45).shift(UP * 0.18).set_z_index(Z_MARK + 1)
        self.at("force", glow(sp.s(*E1, *E2), ACCENT, 7), *draw_arcs(self, [(arcL, eqL), (arcR, eqR)]),
                FadeIn(lab_force, shift=RIGHT * 0.15), run_time=0.8)
        self.at("forbid", sp.join.animate.set_stroke(BAD, 7), FadeIn(lab_forbid, shift=LEFT * 0.15), run_time=0.6)
        plus = T("+", 26, DIM)
        trick_row = VGroup(T("force", 26, ACCENT), plus, T("forbid", 26, BAD)).arrange(RIGHT, buff=0.16)
        trick = card(trick_row).next_to(badge, DOWN, buff=0.3, aligned_edge=LEFT)
        trick[0].set_z_index(Z_MARK)
        trick_row.set_z_index(Z_MARK + 1)
        # "Remember that trick": the plan clears in the pause, the two words fly to the corner ('forbid' arcs
        # above the spindle), then the card forms around them
        self.at("p7s2_end", *[FadeOut(m) for m in plan], run_time=0.45)
        self.at("p7s3", ReplacementTransform(lab_force, trick_row[0]),
                ReplacementTransform(lab_forbid, trick_row[2], path_arc=0.3), run_time=0.5)
        self.play(FadeIn(trick[0]), FadeIn(plus), run_time=0.25)

        # ------------------------------------------------------------ end on the empty background
        everything = [m for m in self.mobjects if m is not panel and not isinstance(m, ValueTracker)]
        self.at("p7_end", *[FadeOut(m) for m in everything], run_time=0.8)

