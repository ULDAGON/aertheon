"""S02_Rule: the fine print, and a ring.

Beats (all synced to timeline/S02_Rule.json; word-level beats use self.w(sentence, word)):
  p1  three same-coloured pairs (0.6, 1.0, 1.4 apart): which break the rule?
  p2  close pair fine, far pair fine, only exactly 1 is forbidden (the middle pair's ruler becomes a stick, BAD)
  p3  that red stick slides down and becomes the '1' reference; if shorter distances were banned too, a tiny disk
      (a ghost of the stick overhangs it on both sides) fills with ever more colours -> infinity
  p4  a small panel: "unit = 1 inch" -> "mile" on the word, then scales up 2.2x: same picture, same puzzle
  p5  a close-up lens on a wavy blue|pink border: every point gets exactly one colour, even on the border
  p6  a blue point, a stick spun around it traces the forbidden ring; four blue attempts on it, each joined to the
      centre by a unit radius that turns BAD, are crossed out and held through the pause
  p7  every point has its own ring: a dense jittered web of dots + rings that overlap everywhere; "how few?"
"""
import colorsys
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

U = UNIT  # 2.0 manim units per problem unit (p1, p2, p6, p7)


# ---------------------------------------------------------------- local helpers
def shake(mob, amp=0.08, cycles=3):
    """One small horizontal 'contradiction' shake that settles back in place."""
    home = mob.get_center().copy()

    def f(m, a):
        m.move_to(home + RIGHT * amp * np.sin(a * cycles * TAU) * (1 - a))
    return UpdateFromAlphaFunc(mob, f)


def ping(pos, color, r0=0.14, grow=3.2, width=4):
    """A ring that expands from a point and fades (a 'flash' on that point)."""
    c = Circle(radius=r0, color=color, stroke_width=width).move_to(pos)
    return c, c.animate(rate_func=rush_from).scale(grow).set_stroke(opacity=0)


def hue_color(i, rng):
    """An ever-new paint colour in the same soft style as the palette (never near BAD red)."""
    h = (0.07 + 0.61803398875 * i) % 1.0
    if h < 0.05 or h > 0.95:
        h = (h + 0.1) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, rng.uniform(0.45, 0.7), rng.uniform(0.85, 1.0))
    return rgb_to_color([r, g, b])


def cruise(t, a=0.1):
    """Constant speed with short eased ramps at both ends (trapezoidal velocity)."""
    v = 1 / (1 - a)
    if t < a:
        return v * t * t / (2 * a)
    if t > 1 - a:
        return 1 - v * (1 - t) ** 2 / (2 * a)
    return v * (t - a / 2)


def bar_home():
    """The scoreboard at its fixed home for the whole video, on a BG backing panel."""
    bar = BoundsBar(lo=1).scale(0.8).to_edge(DOWN, buff=0.3)
    back = RoundedRectangle(corner_radius=0.2, width=bar.width + 0.6, height=bar.height + 0.35,
                            stroke_width=0).set_fill(BG, 0.92).move_to(bar)
    grp = VGroup(back, bar)
    grp.set_z_index(10)
    return grp, bar


def circle_crossings(centers, r, xmax=6.5, ymin=-2.4, ymax=3.5):
    """Crossing points of equal circles (radius r) around the given centres."""
    out = []
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            p, q = centers[i], centers[j]
            d = np.linalg.norm(q - p)
            if 1e-6 < d < 2 * r:
                m = (p + q) / 2
                h = np.sqrt(r * r - (d / 2) ** 2)
                perp = np.array([-(q - p)[1], (q - p)[0], 0]) / d
                for s in (1, -1):
                    x = m + s * h * perp
                    if abs(x[0]) < xmax and ymin < x[1] < ymax:
                        out.append(x)
    return out


class S02_Rule(TimedScene):
    def construct(self):
        self.p12_pairs()
        self.p3_disk()
        self.p4_zoom()
        self.p5_border()
        self.p6_ring()
        self.p7_web()

    # ------------------------------------------------------------ word times
    def w(self, sid, word, nth=0):
        """Start time of the nth occurrence of `word` in sentence `sid` (punctuation/case ignored)."""
        key = word.lower()
        for s in self.tl["sentences"]:
            if s["id"] == sid:
                hits = [x["s"] for x in s["words"] if re.sub(r"[^\w'-]", "", x["w"]).lower() == key]
                if len(hits) > nth:
                    return hits[nth]
                raise KeyError(f"word {word!r} #{nth} not in {sid}: {s['text']!r}")
        raise KeyError(f"unknown sentence {sid!r}")

    # ============================================================ p1 + p2: which pairs break the rule?
    def p12_pairs(self):
        cx = -1.0
        ys, ds, cols = [1.6, 0.2, -1.2], [0.6, 1.0, 1.4], [BLUE_P, YELLOW_P, PINK_P]
        check_x = 2.1
        self.pairs, rulers, ticks, reads = [], [], [], []
        for y, d, c in zip(ys, ds, cols):
            a, b = np.array([cx - d * U / 2, y, 0]), np.array([cx + d * U / 2, y, 0])
            pair = VGroup(pt(a, c, r=0.15), pt(b, c, r=0.15)).set_z_index(3)
            ry = y - 0.42
            main = Line([a[0], ry, 0], [b[0], ry, 0], stroke_width=2.5, color=DIM)
            tk = VGroup(Line([a[0], ry - 0.1, 0], [a[0], ry + 0.1, 0]),
                        Line([b[0], ry - 0.1, 0], [b[0], ry + 0.1, 0])).set_stroke(DIM, 2.5)
            read = N(f"{d:.1f}", 36, DIM).next_to(main, RIGHT, buff=0.25)
            self.pairs.append(pair); rulers.append(main); ticks.append(tk); reads.append(read)

        # {#pairs}: the three pairs arrive top to bottom, then their rulers and readouts
        self.at("pairs", LaggedStart(*[
            AnimationGroup(GrowFromCenter(p[0]), GrowFromCenter(p[1])) for p in self.pairs], lag_ratio=0.4),
            run_time=1.2)
        self.play(LaggedStart(*[
            AnimationGroup(Create(m), FadeIn(t), FadeIn(r, shift=LEFT * 0.15))
            for m, t, r in zip(rulers, ticks, reads)], lag_ratio=0.3), run_time=1.0)

        # {#which}: a big question mark, and the pairs pulse one after another
        q = N("?", 150, ACCENT).move_to([5.0, 0.2, 0])
        pulses = [AnimationGroup(*[Indicate(d, scale_factor=1.45, color=c) for d in p])
                  for p, c in zip(self.pairs, cols)]
        quick = lambda t: smooth(min(1.0, t / 0.35))   # the ? lands at once; the pulses take the whole play
        self.at("which", FadeIn(q, scale=0.6, rate_func=quick), LaggedStart(*pulses, lag_ratio=0.45), run_time=1.45)
        # pause: the question hangs; the ? pulses once
        self.play(q.animate(rate_func=there_and_back).scale(1.15), run_time=0.5)

        # "Just one."
        self.at("p2", FadeOut(q, scale=0.8), run_time=0.45)
        # {#close} / {#far}: checks
        chk = [check_mark([check_x, y - 0.18, 0], size=0.2) for y in ys]
        self.at("close", Create(chk[0]), *[Indicate(d, scale_factor=1.3, color=cols[0]) for d in self.pairs[0]],
                run_time=0.55)
        self.at(self.t("far") + 0.1, Create(chk[2]), *[Indicate(d, scale_factor=1.3, color=cols[2])
                                                       for d in self.pairs[2]], run_time=0.55)

        # {#exact}: the middle ruler rises into a unit stick, the pair flashes BAD, a cross, one shake
        mid = self.pairs[1]
        stk = stick(mid[0], mid[1], width=5)
        self.at("exact", FadeOut(ticks[1]), rulers[1].animate.become(stk),
                reads[1].animate.set_color(ACCENT), run_time=0.5)
        cross = cross_mark(np.array([check_x, 0.02, 0]), size=0.17)
        pa, pa_anim = ping(mid[0].get_center(), BAD)
        pb, pb_anim = ping(mid[1].get_center(), BAD)
        others = VGroup(self.pairs[0], self.pairs[2], rulers[0], rulers[2], ticks[0], ticks[2],
                        reads[0], reads[2], chk[0], chk[2])
        self.at(self.w("p2s3", "one"), rulers[1].animate.set_color(BAD), Create(cross), pa_anim, pb_anim,
                others.animate.set_opacity(0.35), run_time=0.5)
        self.remove(pa, pb)
        self.at(self.w("p2s3", "forbidden"), shake(VGroup(mid, rulers[1], reads[1], cross)), run_time=0.45)
        # the red stick and its "1.0" carry over into p3 as the reference '1'
        self.red_stick, self.red_read = rulers[1], reads[1]
        self.p12_rest = VGroup(*self.pairs, rulers[0], rulers[2], *ticks, reads[0], reads[2], *chk, cross)

    # ============================================================ p3: if shorter distances were banned too
    def p3_disk(self):
        S = 4.6                                   # manim units per problem unit in this paragraph
        R = 0.3 * S                               # a disk of radius 0.3: every two of its points < 1 apart
        dc = np.array([-2.2, 0.45, 0])
        disk = Circle(radius=R).move_to(dc).set_stroke(INK, 3)
        disk_fill = Circle(radius=R).move_to(dc).set_stroke(width=0).set_fill(INK, 0.05)
        cap = T("shorter distances banned too?", 32, DIM).move_to([0, 3.05, 0])
        y_ref = dc[1] - R - 0.55
        x0 = dc[0] - R
        ref_line = Line([x0, y_ref, 0], [x0 + S, y_ref, 0], color=UNIT_COLOR, stroke_width=5)
        ends = VGroup(ring([x0, y_ref, 0], r=0.07, color=UNIT_COLOR),
                      ring([x0 + S, y_ref, 0], r=0.07, color=UNIT_COLOR))
        ref_lbl = N("1", 34, INK).next_to(ref_line, DOWN, buff=0.18)

        # the forbidden stick from p2 slides down and stretches into this paragraph's '1' reference
        self.at("p3", FadeOut(self.p12_rest, run_time=0.5),
                ReplacementTransform(self.red_stick, ref_line, run_time=1.05),
                FadeTransform(self.red_read, ref_lbl, run_time=1.05),
                FadeIn(cap, shift=DOWN * 0.1, run_time=0.6, lag_ratio=0), run_time=1.05)
        # each end marker grows in place (scaling the pair as a group would slide them along the stick)
        self.play(*[GrowFromCenter(e) for e in ends], Create(disk), FadeIn(disk_fill), run_time=0.85)

        # ---- the filling: every new dot needs a new colour, and clashes with a few earlier dots
        rng = np.random.default_rng(11)
        K, sep, lim = 46, 0.19, R - 0.14
        pos = []
        tries = 0
        while len(pos) < K and tries < 20000:
            tries += 1
            p = rng.uniform(-lim, lim, 2)
            if np.linalg.norm(p) <= lim and all(np.linalg.norm(p - q) > sep for q in pos):
                pos.append(p)
        K = len(pos)
        P = [dc + np.array([p[0], p[1], 0]) for p in pos]
        colors = [PALETTE[i] if i < 7 else hue_color(i, rng) for i in range(K)]
        t_disk = self.t("disk")
        T_fill = self.t("endless") - t_disk
        ti = [0.97 * T_fill * (i / (K - 1)) ** (1 / 2.2) for i in range(K)]
        dot_base = [pt(P[i], colors[i], r=0.095) for i in range(K)]
        dots = VGroup(*[d.copy().set_opacity(0) for d in dot_base]).set_z_index(3)
        lines, line_t = VGroup(), []
        for i in range(1, K):
            js = list(range(i)) if i < 7 else sorted(rng.choice(i, size=4, replace=False))
            for j in js:
                lines.add(Line(P[i], P[j], stroke_width=2.2, color=DIM, stroke_opacity=0))
                line_t.append(ti[i])
        lines.set_z_index(2)
        ctr_pos = np.array([3.55, 0.75, 0])
        texts = [N(str(k), 110, INK).move_to(ctr_pos) for k in range(1, K + 1)]
        texts.append(N("∞", 150, ACCENT).move_to(ctr_pos))
        counter = texts[0].copy().set_opacity(0)
        lbl_pos = ctr_pos + DOWN * 1.2
        lbl_one, lbl_many = T("color", 30, DIM).move_to(lbl_pos), T("colors", 30, DIM).move_to(lbl_pos)
        ctr_lbl = lbl_one.copy().set_opacity(0)
        n_sp = 520
        rr = (R - 0.05) * np.sqrt(rng.uniform(0, 1, n_sp))
        th = rng.uniform(0, TAU, n_sp)
        speck = VGroup(*[Dot(dc + np.array([rr[k] * np.cos(th[k]), rr[k] * np.sin(th[k]), 0]), radius=0.03,
                             color=hue_color(k + 100, rng)).set_opacity(0) for k in range(n_sp)]).set_z_index(1)
        # on "tiny": a ghost of the '1' stick slides up across the disk's diameter -- it overhangs both sides
        ghost = VGroup(ref_line.copy(), ends.copy()).set_opacity(0).set_z_index(4)
        g_from, g_to = ghost.get_center().copy(), dc.copy()
        g0 = self.w("p3s1", "tiny") - t_disk
        g_fade = self.w("p3s1", "with") - t_disk
        state = {"idx": -1, "lbl": 0}
        total = T_fill + 0.6

        def fill(_, alpha):
            tau = alpha * total
            for i in range(K):
                s = (tau - ti[i]) / 0.14
                if s <= 0:
                    continue
                s = min(1.0, s)
                dots[i].become(dot_base[i].copy().scale(0.3 + 0.7 * s + 0.35 * np.sin(PI * s)))
            for ln, t0 in zip(lines, line_t):
                if tau >= t0:
                    ln.set_stroke(opacity=0.1 + 0.9 * np.exp(-(tau - t0) / 0.35))
            idx = K if tau >= T_fill else max(0, sum(1 for x in ti if x <= tau) - 1)
            if idx != state["idx"]:
                state["idx"] = idx
                counter.become(texts[idx])
            want = 0 if idx == 0 else 1
            if want != state["lbl"]:
                state["lbl"] = want
                ctr_lbl.become(lbl_many if want else lbl_one)
            ctr_lbl.set_opacity(min(1.0, tau / 0.3))
            # ghost stick
            a = np.clip((tau - g0) / 0.6, 0, 1)
            if tau >= g0:
                o = min(1.0, (tau - g0) / 0.2) * np.clip(1 - (tau - g_fade) / 0.4, 0, 1)
                ghost.move_to(interpolate(g_from, g_to, smooth(a)))
                ghost.set_opacity(0.75 * o)
                ghost[1].set_fill(opacity=0)
            if tau >= T_fill:
                k_on = int(n_sp * min(1.0, (tau - T_fill) / 0.45))
                for k in range(k_on):
                    speck[k].set_opacity(1)

        grp = VGroup(speck, lines, dots, ghost, counter, ctr_lbl)
        self.at("disk", UpdateFromAlphaFunc(grp, fill, rate_func=linear), run_time=total)
        self.remove(ghost)
        # the disk glows once, then everything clears in the pause
        self.play(disk.animate(rate_func=there_and_back).set_stroke(ACCENT, 7), run_time=0.7)
        self.at(self.t("p4") - 0.52, FadeOut(VGroup(disk, disk_fill, speck, lines, dots, counter, ctr_lbl,
                                                     cap, ref_line, ends, ref_lbl)), run_time=0.45)

    # ============================================================ p4: an inch or a mile
    def p4_zoom(self):
        pc = np.array([0, 0.35, 0])
        panel = RoundedRectangle(corner_radius=0.16, width=2.4, height=1.6).move_to(pc)
        panel.set_stroke(DIM, 1.5).set_fill("#161B24", 1)
        u = 0.78
        B = np.array([0.0, 0.0, 0])
        dirv = lambda deg: np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
        A, C = B + u * dirv(-128), B + u * dirv(-42)
        dots = VGroup(pt(A, PINK_P, r=0.085), pt(B, BLUE_P, r=0.085), pt(C, YELLOW_P, r=0.085)).set_z_index(3)
        sticks = VGroup(stick(A, B, width=3.5), stick(B, C, width=3.5))
        art = VGroup(sticks, dots)
        art.move_to(pc)
        content = VGroup(panel, art)
        lbl_a = T("unit = 1", 30, DIM)
        w_inch = T("inch", 30, INK)
        lbl = VGroup(lbl_a, w_inch).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        lbl.next_to(panel, DOWN, buff=0.35)
        w_mile = T("mile", 30, INK)
        w_mile.next_to(lbl_a, RIGHT, buff=0.16).align_to(lbl_a, DOWN)

        self.at("p4", FadeIn(panel, scale=0.9), run_time=0.4)
        self.play(Create(sticks), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=0.5)
        self.at(self.w("p4s1", "inch"), FadeIn(lbl, shift=UP * 0.12), run_time=0.45)
        # "...or a mile": a clean vertical word swap on the spoken word
        self.at(self.w("p4s1", "mile"), FadeOut(w_inch, shift=UP * 0.2), FadeIn(w_mile, shift=UP * 0.2),
                run_time=0.45)

        # {#zoom}: everything scales up 2.2x about the centre; proportions (and colours) unchanged
        k = 2.2
        big_bottom = pc[1] - panel.height * k / 2
        lbl2 = VGroup(lbl_a, w_mile)
        tag = T("same picture, same puzzle", 30, DIM).move_to([0, pc[1] + panel.height * k / 2 + 0.55, 0])
        late = lambda t: smooth(np.clip((t - 0.62) / 0.38, 0, 1))   # the tag lands on "change the puzzle"
        self.at("zoom", content.animate(rate_func=smooth).scale(k, about_point=pc, scale_stroke=True),
                lbl2.animate(rate_func=smooth).move_to([0, big_bottom - 0.35 - lbl2.height / 2, 0]),
                FadeIn(tag, shift=DOWN * 0.1, rate_func=late), run_time=1.35)
        self.at(self.t("p4_end") + 0.04, FadeOut(VGroup(content, lbl2, tag)), run_time=0.45)

    # ============================================================ p5: one colour per point, even on a border
    def p5_border(self):
        lc = np.array([-1.35, 0.15, 0])
        LR = 2.65
        f = lambda y: 0.34 * np.sin(1.25 * y + 0.5) + 0.1 * np.sin(2.9 * y + 1.0)
        ys = np.linspace(-LR - 0.3, LR + 0.3, 90)
        curve = [lc + np.array([f(y), y, 0]) for y in ys]
        lens = Circle(radius=LR).move_to(lc)
        left = Polygon(*curve, lc + np.array([-LR - 1, LR + 0.3, 0]), lc + np.array([-LR - 1, -LR - 0.3, 0]))
        right = Polygon(*curve, lc + np.array([LR + 1, LR + 0.3, 0]), lc + np.array([LR + 1, -LR - 0.3, 0]))
        blue = Intersection(lens, left, stroke_width=0, fill_color=BLUE_P, fill_opacity=0.5)
        pink = Intersection(lens, right, stroke_width=0, fill_color=PINK_P, fill_opacity=0.5)
        inside = [p for p in curve if np.linalg.norm(p - lc) < LR - 0.02]
        border = VMobject().set_points_smoothly(inside).set_stroke(INK, 2, opacity=0.55)
        rim = lens.copy().set_stroke(DIM, 3).set_fill(opacity=0)

        self.at("p5", FadeIn(blue), FadeIn(pink), Create(rim), run_time=0.6)
        self.play(Create(border), run_time=0.3)

        # "exactly one color": a few ordinary points each take the colour of their region
        samples = [(np.array([-1.55, 1.0, 0]), BLUE_P), (np.array([-1.2, -1.2, 0]), BLUE_P),
                   (np.array([1.5, 1.75, 0]), PINK_P), (np.array([1.5, -0.75, 0]), PINK_P)]
        rings = [ring(lc + p, r=0.12) for p, _ in samples]
        fills = [pt(lc + p, c, r=0.12) for p, c in samples]
        self.at(self.w("p5s1", "exactly"), LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.2),
                run_time=0.5)
        self.play(LaggedStart(*[ReplacementTransform(r, fl) for r, fl in zip(rings, fills)], lag_ratio=0.2),
                  run_time=0.6)

        # {#border}: a point exactly on the border; it takes one colour, no blending
        yb = 0.35
        bp = lc + np.array([f(yb), yb, 0])
        bring = ring(bp, r=0.14).set_z_index(3)
        bfill = pt(bp, BLUE_P, r=0.14).set_z_index(3)
        self.at("border", border.animate.set_stroke(INK, 3.5, opacity=0.95), GrowFromCenter(bring), run_time=0.45)
        label = T("one color, even here", 28, INK).move_to([3.9, bp[1] + 0.9, 0])
        l0 = label.get_left() + LEFT * 0.12 + DOWN * 0.05
        dvec = bp - l0
        l1 = bp - dvec / np.linalg.norm(dvec) * 0.3          # stop short of the point, with a small gap
        lead = Line(l0, l1, stroke_width=2, color=DIM)
        # the point fills blue, and with it the whole border line joins the blue side (no third, unpainted thing)
        self.at(self.w("p5s1", "right"), ReplacementTransform(bring, bfill), Create(lead),
                border.animate.set_stroke(BLUE_P, 3.5, opacity=0.9),
                FadeIn(label, shift=LEFT * 0.1), run_time=0.5)
        self.play(Indicate(bfill, scale_factor=1.5, color=BLUE_P), run_time=0.45)
        self.at(self.t("p5_end") + 0.05, FadeOut(VGroup(blue, pink, rim, border, *fills, bfill, lead, label)),
                run_time=0.5)

    # ============================================================ p6: the forbidden ring
    def p6_ring(self):
        c6 = np.array([0, 0.2, 0])
        self.c6 = c6
        hollow = ring(c6, r=0.12).set_z_index(5)
        self.hero = pt(c6, BLUE_P, r=0.12).set_z_index(5)
        self.at("p6", FadeIn(hollow, scale=0.5), run_time=0.4)
        self.at("blue", ReplacementTransform(hollow, self.hero), run_time=0.4)

        # {#spin}: a unit stick pinned at the dot; one full sweep at constant speed whose far end draws the
        # ring. It ends on "ring," so the tracing is still visibly going on while "traces" is spoken.
        end = c6 + RIGHT * U
        arm = VGroup(Line(c6, end, color=UNIT_COLOR, stroke_width=5),
                     ring(end, r=0.08, color=UNIT_COLOR)).set_z_index(4)
        self.circ = Circle(radius=U).move_to(c6).set_stroke(UNIT_COLOR, 3.5).set_z_index(1)
        self.at("spin", GrowFromPoint(arm, c6), run_time=0.35)
        t_ring_end = self.w("p6s2", "ring") + 0.13
        self.play(Rotate(arm, TAU, about_point=c6), Create(self.circ), run_time=self.left(t_ring_end),
                  rate_func=cruise)
        self.play(FadeOut(arm), run_time=0.35)

        label = T("no blue on this ring", 28, DIM).move_to([4.3, c6[1], 0])
        self.at(self.w("p6s2", "no"), FadeIn(label, shift=LEFT * 0.12), run_time=0.5)

        # {#noblue}: four blue attempts on the ring, each joined to the blue centre by a unit radius
        # (same colour, exactly 1 apart) -> the radii turn BAD and each attempt is crossed out; held through the pause
        angs = np.radians([38, 128, 214, 302])
        P = [c6 + U * np.array([np.cos(a), np.sin(a), 0]) for a in angs]
        tries = [pt(p, BLUE_P, r=0.12).set_z_index(5) for p in P]
        radii = [stick(c6, p, width=3).set_z_index(2) for p in P]
        crosses = [cross_mark(p, size=0.21).set_z_index(6) for p in P]
        self.at("noblue", LaggedStart(*[AnimationGroup(GrowFromPoint(rd, c6), GrowFromCenter(t))
                                        for rd, t in zip(radii, tries)], lag_ratio=0.15), run_time=0.5)
        self.at(self.w("p6s2", "blue"), *[rd.animate.set_color(BAD) for rd in radii],
                LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.2), run_time=0.4)
        # pause: the ring glows once underneath the rejected attempts
        self.at(self.t("p6_end") + 0.2, self.circ.animate(rate_func=there_and_back).set_stroke(ACCENT, 6),
                run_time=0.5)
        self.p6_label = label
        self.p6_rejects = VGroup(*radii, *tries, *crosses)

    # ============================================================ p7: every point has its own ring
    def p7_web(self):
        c6, k = self.c6, 0.42
        r = U * k                                   # 0.84: the unit ring at the web's scale
        # the rejected attempts shrink in with the ring while they fade (never left floating off it)
        self.at("rings", FadeOut(self.p6_label),
                self.p6_rejects.animate.scale(k, about_point=c6).set_opacity(0),
                self.circ.animate.scale(k, about_point=c6).set_stroke(UNIT_COLOR, 2.5, opacity=0.6),
                self.hero.animate.scale(0.85), run_time=0.75)
        self.remove(self.p6_rejects)

        # a dense jittered triangular arrangement: every ring crosses ~6 neighbours; no dot sits on a ring
        rng = np.random.default_rng(5)
        sp, h = 1.04, 0.9
        cand = []
        for j in range(-2, 3):
            off = 0.0 if j % 2 == 0 else sp / 2
            for i in range(-6, 7):
                x = i * sp + off
                if abs(x) <= 5.3 and not (i == 0 and j == 0):
                    cand.append(c6 + np.array([x, j * h, 0]))
        spots = []
        for base in sorted(cand, key=lambda p: np.linalg.norm(p - c6)):
            for _ in range(60):
                p = base + np.array([*rng.uniform(-0.11, 0.11, 2), 0])
                if base[1] < c6[1] - 1.5 * h:
                    p[1] = max(p[1], base[1])       # bottom row never dips toward the scoreboard
                if all(abs(np.linalg.norm(p - q) - r) > 0.16 for q in spots + [c6]):
                    break
            spots.append(p)
        # colours: close neighbours differ; no blue next to the (blue) hero so it stays readable
        pal = []
        for i, p in enumerate(spots):
            near = {pal[j] for j in range(i) if np.linalg.norm(spots[j] - p) < 1.4}
            if np.linalg.norm(p - c6) < 1.4:
                near.add(BLUE_P)
            choices = [c for c in PALETTE if c not in near] or PALETTE[1:]
            pal.append(choices[rng.integers(len(choices))])
        dots = [pt(p, c, r=0.09).set_z_index(5) for p, c in zip(spots, pal)]
        rings_ = [Circle(radius=r).move_to(p).set_stroke(UNIT_COLOR, 2.2, opacity=0.35).set_z_index(1)
                  for p in spots]
        self.play(LaggedStart(*[Succession(GrowFromCenter(d), Create(rg, run_time=2.0))
                                for d, rg in zip(dots, rings_)], lag_ratio=0.04),
                  run_time=self.left("overlap") - 0.08)

        # {#overlap}: where rings cross, the web lights up; hold, then settle
        centers = [c6] + spots
        xs = circle_crossings(centers, r)
        sparks = VGroup(*[Dot(x, radius=0.065, color=ACCENT) for x in xs]).set_z_index(3)
        allrings = VGroup(self.circ, *rings_)
        self.at("overlap", LaggedStart(*[FadeIn(s, scale=0.3) for s in sparks], lag_ratio=0.004),
                allrings.animate.set_stroke(opacity=0.8), run_time=0.8)
        self.at(self.t("overlap") + 1.25, FadeOut(sparks), allrings.animate.set_stroke(opacity=0.42),
                run_time=0.5)

        # "how few colors": the painted points pulse once, a gentle wave from the centre outwards
        self.at(self.w("p7s2", "how"), LaggedStart(*[Indicate(d, scale_factor=1.6, color=c) for d, c in
                                                     zip([self.hero] + dots, [BLUE_P] + pal)], lag_ratio=0.02),
                run_time=0.8)

        # {#board}: the scoreboard returns, window still wide open, with a question
        grp, bar = bar_home()
        qm = N("?", 36, ACCENT).next_to(bar.title, RIGHT, buff=0.12).set_z_index(11)
        qm.align_to(bar.title, DOWN)
        self.at("board", FadeIn(grp, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(qm, scale=0.4), run_time=0.4)
        web = VGroup(allrings, self.hero, *dots)
        self.at(self.t("p7_end") + 0.25, FadeOut(web), FadeOut(grp), FadeOut(qm), run_time=0.6)
