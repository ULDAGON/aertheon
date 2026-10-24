"""S01_Hook: an endless floor, a box of paints, one stick, Nelson's question, and the answer 5, 6 or 7.

Picture beats (all scheduled against timeline/S01_Hook.json):
  P1  a floor patch appears ("a flat floor"), the grid spreads past every edge ({#floor}) while the view eases out;
      a tray of seven paints pops in ({#paints}); a few single points get painted ("paint"), then a paint mosaic
      blooms from the centre over the whole floor ({#every}). The mosaic is an illustration, not a valid colouring.
  P2  mosaic + tray dim ("one rule"); a unit stick drops in ({#stick}), wears a "1", slides ("anywhere"), turns
      ({#angle}); its ends pulse ("two ends"), take the colours of the cells under them ({#differ}) -> check;
      it lifts, glides and lands elsewhere ({#always}) -> new colours, still different -> check.
  P3  the floor sinks further back; a big "?" ("how few paints?") while the swatches are counted; playful tilt +
      swatch wave ({#rainy}); Nelson card, built word by word ({#nelson}, "1950", "18", "student").
  P4  the colors-needed scoreboard arrives at its home ("Today"), its label brightens ("answer") and stays bright
      until {#which}; 5, 6, 7 light
      up in turn while the paint box echoes the count (5 bright paints, then 6, then 7); the "?" parks above them
      ({#which}) and the three digits glow as it lands; everything fades out together in the tail (~0.7 s).

Beat times come from marks or from word start times looked up in the timeline (self.w), never hand-copied.

The mosaic is precomputed (seeded Voronoi). The stick's two landing spots are seeds of hand-coloured cells, so each
end sits in the middle of its cell and the two ends genuinely show two different colours.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

from scipy.spatial import Voronoi  # noqa: E402

# ------------------------------------------------------------------ layout (manim units)
HALF = UNIT / 2                       # half a unit stick
END_R = 0.11                          # stick end dot radius (reads at 480p)
MOSAIC_OP = 0.6                       # mosaic opacity while it is the star (P1)
DIM_OP = 0.22                         # mosaic opacity once the rule is on (~35 %): the stick still needs the cells
BACK_OP = 0.13                        # mosaic opacity from P3 on: context only, so the ?, card and bar stand out
LIT_OP = 0.8                          # a cell under a landed stick end
OFF_OP = 0.3                          # a paint swatch that is "not in the box" for this count (P4)

C0, TH0 = np.array([-1.2, -0.2, 0.0]), 0.0                      # drop pose
C1, TH1 = np.array([0.5, -0.55, 0.0]), 60 * DEGREES             # landing 1 (after "anywhere" + turn)
C2, TH2 = np.array([-2.5, 0.85, 0.0]), 130 * DEGREES            # landing 2 (up-left, turned 70 degrees more)


def ends(c, th):
    d = HALF * np.array([np.cos(th), np.sin(th), 0.0])
    return c - d, c + d


A1, B1 = ends(C1, TH1)
A2, B2 = ends(C2, TH2)
# single points painted on "Your job is to paint" (before the bloom); they become cells of the same colour
DOTS = [(np.array([-4.3, 1.45, 0]), ORANGE_P), (np.array([3.7, 1.25, 0]), TEAL_P),
        (np.array([2.5, -1.95, 0]), YELLOW_P), (np.array([-3.1, -1.7, 0]), GREEN_P)]
SPECIAL = [(A1, BLUE_P), (B1, PINK_P), (A2, PURPLE_P), (B2, YELLOW_P)] + DOTS


# ------------------------------------------------------------------ geometry builders
def build_mosaic(seed=5, spacing=0.62):
    """Voronoi 'paint mosaic' covering the frame. Returns (cells VGroup, seeds (N,3), colors list, special idx)."""
    rng = np.random.default_rng(seed)
    xs = np.arange(-8.2, 8.21, spacing)
    ys = np.arange(-5.0, 5.01, spacing * 0.9)
    pts = []
    for j, y in enumerate(ys):
        for x in xs:
            p = np.array([x + (spacing / 2 if j % 2 else 0), y]) + rng.uniform(-0.2, 0.2, 2)
            pts.append(p)
    pts = np.array(pts)
    sp = np.array([s[0][:2] for s in SPECIAL])
    keep = np.min(np.linalg.norm(pts[:, None, :] - sp[None, :, :], axis=2), axis=1) > 0.45
    pts = np.vstack([sp, pts[keep]])
    n = len(pts)
    far = np.array([[x, y] for x in (-30, 0, 30) for y in (-30, 0, 30) if (x, y) != (0, 0)])
    vor = Voronoi(np.vstack([pts, far]))
    # neighbour-aware random colours (adjacent tiles differ, like a mosaic); the special tiles are fixed
    nb = [set() for _ in range(n)]
    for a, b in vor.ridge_points:
        if a < n and b < n:
            nb[a].add(b)
            nb[b].add(a)
    col = [None] * n
    for i, (_, c) in enumerate(SPECIAL):
        col[i] = PALETTE.index(c)
    order = sorted(range(len(SPECIAL), n), key=lambda i: np.linalg.norm(pts[i]))
    for i in order:
        used = {col[k] for k in nb[i] if col[k] is not None}
        free = [c for c in range(7) if c not in used]
        col[i] = int(rng.choice(free)) if free else int(rng.integers(7))
    for i in range(len(SPECIAL)):
        assert all(col[k] != col[i] for k in nb[i]), "special tile touches its own colour"
    cells = VGroup()
    for i in range(n):
        reg = vor.regions[vor.point_region[i]]
        assert -1 not in reg and reg
        poly = Polygon(*[np.array([*vor.vertices[v], 0.0]) for v in reg])
        poly.set_fill(PALETTE[col[i]], opacity=0).set_stroke(BG, width=1.6, opacity=0)
        cells.add(poly)
    seeds = np.c_[pts, np.zeros(n)]
    return cells, seeds, col


def build_grid(step=1.0, sub=0.5, xr=10.0, yr=6.0):
    """Square floor grid as short segments (so it can grow outward from the centre)."""
    segs = VGroup()
    xs = np.arange(-xr, xr + 1e-9, step)
    ys = np.arange(-yr, yr + 1e-9, step)
    for x in xs:
        for y in np.arange(-yr, yr - 1e-9, sub):
            segs.add(Line([x, y, 0], [x, y + sub, 0]))
    for y in ys:
        for x in np.arange(-xr, xr - 1e-9, sub):
            segs.add(Line([x, y, 0], [x + sub, y, 0]))
    segs.set_stroke(FAINT, width=2.6, opacity=0)
    for s in segs:
        s.base = s.points.copy()
        s.r = float(np.linalg.norm(s.get_center()[:2]))
    return segs


def ramp(t, a, b, f=smooth):
    """0 before a, 1 after b, eased in between."""
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    return f((t - a) / (b - a))


class S01_Hook(TimedScene):
    # ------------------------------------------------------------ helpers
    def w(self, sid, word, nth=1):
        """Start time of the nth occurrence of `word` in sentence `sid` (read from the timeline, never hand-copied)."""
        hits = [x["s"] for s in self.tl["sentences"] if s["id"] == sid
                for x in s["words"] if x["w"].strip(",.?!").lower() == word]
        if len(hits) < nth:
            raise KeyError(f"word {word!r} (#{nth}) not in sentence {sid}")
        return hits[nth - 1]

    @staticmethod
    def dim_cells(cells, to, fast=(), k=1.6):
        """One animation for the whole mosaic: every cell eases to fill opacity `to`; cells in `fast` get there
        k times sooner (so lit cells drop with the stick, while the floor dims more slowly)."""
        op0 = [c.get_fill_opacity() for c in cells]
        fast = set(fast)

        def f(g, a):
            for i, (c, o) in enumerate(zip(g, op0)):
                u = smooth(min(1.0, a * k)) if i in fast else smooth(a)
                c.set_fill(opacity=o + (to - o) * u)
        return UpdateFromAlphaFunc(cells, f, rate_func=linear)

    def clock(self):
        """Absolute scene time of the frame being computed (valid inside updaters)."""
        return self._frames / self._fps + self.last_t

    def track(self, mob, fn):
        """Drive `mob` from the absolute clock every frame: fn(mob, t)."""
        def upd(m, dt):
            fn(m, self.clock())
        mob.add_updater(upd)
        return upd

    # ------------------------------------------------------------ stick
    def make_stick(self):
        line = Line(LEFT * HALF, RIGHT * HALF, color=UNIT_COLOR, stroke_width=5)
        e1 = ring(ORIGIN, r=END_R, color=INK)
        e2 = ring(ORIGIN, r=END_R, color=INK)
        st = VGroup(line, e1, e2)
        st.line, st.e1, st.e2 = line, e1, e2
        return st

    @staticmethod
    def pose(st, c, th, s=1.0):
        """Place the stick (always exactly one unit long). s > 1 = lifted: thicker line, bigger ends."""
        a, b = ends(c, th)
        st.line.put_start_and_end_on(a, b)
        st.line.set_stroke(width=5 * s)
        st.e1.set(width=2 * END_R * s).move_to(a)
        st.e2.set(width=2 * END_R * s).move_to(b)
        return st

    def glide(self, st, c_from, th_from, c_to, th_to, lift=0.0, arc=0.0, unpaint=None, rate_func=smooth):
        """Animation: move the stick between poses; `lift` = extra thickness mid-air, `arc` = sideways bow,
        `unpaint` = (colour1, colour2) the ends lose during the first quarter (they leave the floor)."""
        c_from, c_to = np.array(c_from), np.array(c_to)
        d = c_to - c_from
        nrm = np.array([-d[1], d[0], 0.0])
        nrm = nrm / (np.linalg.norm(nrm) + 1e-9)

        def f(m, a):
            c = c_from + d * a + nrm * arc * np.sin(PI * a)
            self.pose(m, c, th_from + (th_to - th_from) * a, 1 + lift * np.sin(PI * a))
            if unpaint:
                u = float(np.clip(a / 0.25, 0, 1))
                for e, col in zip((m.e1, m.e2), unpaint):
                    e.set_fill(interpolate_color(ManimColor(col), ManimColor(BG), u), 1)
                    e.set_stroke(interpolate_color(ManimColor(BG), ManimColor(INK), u), 2.5)
        return UpdateFromAlphaFunc(st, f, rate_func=rate_func)

    @staticmethod
    def pulse(m, k=1.3, color=None, stroke_only=False, keep_color=False):
        """Scale up and back once; optionally tint towards `color` (stroke only, or kept at the end)."""
        base = m.copy()
        # read the colour from a member that has points: a Text parent has none and reports #000000
        src = (m.family_members_with_points() or [m])[0]
        base_col = src.get_stroke_color() if stroke_only else src.get_color()

        def f(mm, a):
            w = np.sin(PI * a)
            mm.become(base.copy().scale(1 + (k - 1) * w))
            if color is not None:
                u = min(1.0, 2 * a) if keep_color else w
                c = interpolate_color(ManimColor(base_col), ManimColor(color), u)
                if stroke_only:
                    mm.set_stroke(c)
                else:
                    mm.set_color(c)
        return UpdateFromAlphaFunc(m, f)

    # ------------------------------------------------------------ scene
    def construct(self):
        cells, seeds, col = build_mosaic()
        seed_r = np.linalg.norm(seeds[:, :2], axis=1)
        for c, s in zip(cells, seeds):
            c.base = c.points.copy()
            c.seed = s
        grid = build_grid()
        grid.set_z_index(0)
        cells.set_z_index(1)
        idx = {name: i for i, name in enumerate(["A1", "B1", "A2", "B2"])}

        # ============================== P1: the floor, the paints, every point
        self.add(grid)

        def grid_fn(g, t):
            # patch on "a flat floor", then it spreads past every edge from {#floor}; the view eases out 1 -> 0.8
            R = (2.7 * ramp(t, 0.7, 1.9, rate_functions.ease_out_cubic)
                 + 9.0 * ramp(t, self.t("floor"), self.t("floor") + 2.0, rate_functions.ease_in_out_sine))
            z = 1 - 0.2 * ramp(t, self.t("floor"), self.t("p1s1_end"))
            for s in g:
                s.points = s.base * z
                s.set_stroke(opacity=float(np.clip((R - s.r) / 0.9, 0, 1)))
        self.track(grid, grid_fn)
        grid_fn(grid, 0.0)

        # "in every direction": eight faint arrows run outward and fade
        dirs = [rotate_vector(RIGHT, k * TAU / 8) for k in range(8)]
        arrows = VGroup(*[Arrow(ORIGIN, RIGHT * 0.7, buff=0, color=DIM, stroke_width=3,
                                max_tip_length_to_length_ratio=0.3) for _ in dirs])

        t_dir = self.w("p1s1", "in")          # "... in every direction"

        def arrows_fn(g, t):
            p = ramp(t, t_dir - 0.05, t_dir + 1.15, rate_functions.ease_out_sine)
            op = np.sin(PI * p) * 0.9
            for a, v in zip(g, dirs):
                r0 = 1.6 + 3.4 * p
                a.put_start_and_end_on(v * r0, v * (r0 + 0.7))
                a.set_opacity(op)
        arrows.set_z_index(2)
        self.add(arrows)
        self.track(arrows, arrows_fn)
        arrows_fn(arrows, 0.0)

        # box of paints (tray + seven swatches) along the top edge
        swatches = VGroup(*[Circle(radius=0.21).set_fill(c, 1).set_stroke(BG, 2) for c in PALETTE])
        swatches.arrange(RIGHT, buff=0.2)
        tray = RoundedRectangle(corner_radius=0.3, width=swatches.width + 0.5, height=0.72)
        tray.set_fill(BG, 0.9).set_stroke(DIM, 2)
        box = VGroup(tray, swatches).move_to(UP * 3.2)
        box.set_z_index(8)
        # paint always draws above the tray, whatever order animation groups leave the scene list in
        # (same z-index + a restructured family order once put the tray's BG fill over the swatches)
        swatches.set_z_index(9)

        # one AnimationGroup, so the tray keeps its own 0.3 s (a play-level run_time would stretch every child)
        self.at("paints", AnimationGroup(
            FadeIn(tray, scale=0.9, run_time=0.3),
            LaggedStart(*[GrowFromCenter(s, rate_func=rate_functions.ease_out_back) for s in swatches],
                        lag_ratio=0.35, run_time=1.1)), run_time=1.1)
        self.until(self.t("p1s1_end") + 0.3)
        grid.clear_updaters()
        arrows.clear_updaters()
        self.remove(arrows)

        # "Your job is to paint": a few single points get painted
        dots = VGroup(*[pt(p, c, r=0.1) for p, c in DOTS]).set_z_index(3)
        for d in dots:
            d.scale(0.01)
        self.add(dots)   # the group itself must be in the scene, or its bloom updater never runs
        self.until(self.w("p1s2", "job"))
        self.until("every", LaggedStart(*[d.animate(rate_func=rate_functions.ease_out_back).scale(100) for d in dots],
                                        lag_ratio=0.45))

        # {#every}: the mosaic blooms outward from the centre (an expanding disk) and swallows the dots
        self.add(cells)
        t_b = self.t("every")
        span = float(seed_r[seed_r < 9.5].max()) + 1.0
        dot_r = [float(np.linalg.norm(p[:2])) for p, _ in DOTS]

        def bloom(t):
            return span * ramp(t, t_b, t_b + 1.95, rate_functions.ease_in_out_sine)

        def cells_fn(g, t):
            B = bloom(t)
            for c, r in zip(g, seed_r):
                p = float(np.clip((B - r) / 1.0, 0, 1))
                k = 0.3 + 0.7 * rate_functions.ease_out_cubic(p)
                c.points = c.seed + (c.base - c.seed) * k
                c.set_fill(opacity=MOSAIC_OP * p).set_stroke(opacity=p)

        def grid_fade(g, t):
            B = bloom(t)
            z = 0.8
            for s in g:
                s.set_stroke(opacity=float(np.clip(1 - (B - s.r * z) / 1.0, 0.0, 1.0)))

        self.track(cells, cells_fn)
        self.track(grid, grid_fade)
        # per-dot updaters: animation groups restructure the scene, so a group-level updater could be orphaned
        for d, r in zip(dots, dot_r):
            self.track(d, lambda m, t, r=r: m.set_opacity(float(np.clip(1 - (bloom(t) - r) / 1.0, 0, 1))))
        cells_fn(cells, t_b)
        self.until(t_b + 2.0)
        for m in (cells, grid, *dots):
            m.clear_updaters()
        self.remove(grid, *dots)

        # ============================== P2: the one rule
        self.at(self.w("p2s1", "just"), cells.animate.set_fill(opacity=DIM_OP), swatches.animate.set_fill(opacity=0.35),
                tray.animate.set_stroke(opacity=0.35), run_time=0.9)

        st = self.make_stick().set_z_index(6)
        self.pose(st, C0, TH0)
        one = N("1", 34, INK).set_z_index(6)
        # the 1 rides on the stick's normal (not plain UP), so it never slides across the line while the stick turns
        one.add_updater(lambda m: m.move_to(
            st.line.get_center() + 0.42 * rotate_vector(st.line.get_unit_vector(), PI / 2)))

        # {#stick}: it is dropped: starts visibly higher and "lifted" (thicker, bigger ends), then lands on the floor
        st_big = st.copy()
        self.pose(st_big, C0 + UP * 0.7, TH0, 1.7)
        st_big.set_opacity(0.6)
        self.at("stick", Transform(st_big, st.copy(), rate_func=rate_functions.ease_out_cubic), run_time=0.5)
        self.remove(st_big)
        self.add(st, one.set_opacity(0))
        # "exactly one unit long": the 1 appears
        self.at(self.w("p2s2", "one") - 0.05, one.animate.set_opacity(1), run_time=0.4)
        # "anywhere": it slides (the 1 rides along)
        self.at(self.w("p2s2", "anywhere") - 0.05, self.glide(st, C0, TH0, C1, TH0), run_time=0.7)
        # {#angle}: the 1 fades, the stick turns in place 60 degrees and settles
        self.at("angle", AnimationGroup(self.glide(st, C1, TH0, C1, TH1, rate_func=rate_functions.ease_out_back,
                                                   ).set_run_time(1.0), FadeOut(one, run_time=0.3)), run_time=1.0)
        one.clear_updaters()
        self.remove(one)

        # "two ends": the ends pulse
        self.at(self.w("p2s3", "ends") - 0.05,
                *[self.pulse(e, 1.8, ACCENT, stroke_only=True) for e in (st.e1, st.e2)], run_time=0.8)

        # {#differ}: each end takes the colour of its cell; a check pops beside the stick
        def land(a_i, b_i, ca, cb):
            return AnimationGroup(
                cells[a_i].animate.set_fill(opacity=LIT_OP), cells[b_i].animate.set_fill(opacity=LIT_OP),
                st.e1.animate.set_fill(ca, 1).set_stroke(BG, 2.5), st.e2.animate.set_fill(cb, 1).set_stroke(BG, 2.5))

        def check_at(pos):
            disk = Circle(radius=0.3).set_fill(BG, 0.92).set_stroke(GOOD, 2.5)
            return VGroup(disk, check_mark(ORIGIN, size=0.15, width=5)).move_to(pos).set_z_index(7)

        self.at("differ", land(idx["A1"], idx["B1"], BLUE_P, PINK_P), run_time=0.5)
        n1 = np.array([np.sin(TH1), -np.cos(TH1), 0])
        chk1 = check_at(C1 + n1 * 0.62)
        self.at(self.w("p2s3", "colors") - 0.05, GrowFromCenter(chk1, rate_func=rate_functions.ease_out_back),
                run_time=0.4)

        # {#always}: lift (ends lose their paint), glide up-left while turning 70 degrees, land
        self.at("always", AnimationGroup(
            FadeOut(chk1, scale=0.6, run_time=0.3),
            cells[idx["A1"]].animate(run_time=0.4).set_fill(opacity=DIM_OP),
            cells[idx["B1"]].animate(run_time=0.4).set_fill(opacity=DIM_OP),
            self.glide(st, C1, TH1, C2, TH2, lift=0.5, arc=0.35, unpaint=(BLUE_P, PINK_P)).set_run_time(0.8)),
            run_time=0.8)
        # land (0.3 s) and the check (0.3 s, starting mid-landing): "still different" is done on "time", not after it
        n2 = np.array([-np.sin(TH2), np.cos(TH2), 0])
        chk2 = check_at(C2 - n2 * 0.62)
        self.play(AnimationGroup(
            land(idx["A2"], idx["B2"], PURPLE_P, YELLOW_P).set_run_time(0.3),
            GrowFromCenter(chk2, run_time=0.42,     # held at scale 0 for the first 0.12 s, then grows in 0.3 s
                           rate_func=lambda a: rate_functions.ease_out_back(float(np.clip((a * 0.42 - 0.12) / 0.3, 0, 1))))),
            run_time=0.42)
        # pause: only the check pulses
        self.at(self.t("p2_end") + 0.3, self.pulse(chk2, 1.25), run_time=0.6)

        # ============================== P3: how few paints? Nelson
        q = N("?", 150, ACCENT).set_z_index(5)
        q.set_stroke(BG, 10, background=True)
        q.move_to(UP * 0.15)
        # one AnimationGroup keeps the children's own timings: the stick, check and lit cells clear in ~0.4-0.5 s
        # while the ? grows in; the whole floor sinks further back (context only from here on)
        self.at("p3", AnimationGroup(
            FadeOut(st, run_time=0.4), FadeOut(chk2, run_time=0.4),
            self.dim_cells(cells, BACK_OP, fast=(idx["A2"], idx["B2"]), k=1.6).set_run_time(0.8),
            FadeIn(q, scale=0.8, run_time=0.8),
            swatches.animate(run_time=0.8).set_fill(opacity=1), tray.animate(run_time=0.8).set_stroke(opacity=1)),
            run_time=0.8)
        # the swatches are counted: they wobble one after another
        self.play(LaggedStart(*[self.pulse(s, 1.4) for s in swatches], lag_ratio=0.35), run_time=1.6)

        # {#rainy}: playful tilt + a gentle wave through the swatches
        self.at("rainy",
                Rotate(q, angle=-14 * DEGREES, rate_func=there_and_back, about_point=q.get_bottom()),
                LaggedStart(*[s.animate(rate_func=there_and_back).shift(UP * 0.14) for s in swatches],
                            lag_ratio=0.25),
                run_time=1.1)

        # {#nelson}: a caption card at the top left, built as the words come
        name = T("Edward Nelson", 30, INK)
        sub = T("1950  ·  age 18  ·  student", 26, DIM)        # one Text: one shared baseline
        assert len(sub) == 18, len(sub)
        p_year, p_age, p_who = sub[0:4], sub[4:10], sub[10:18]  # "1950" | "· age 18" | "· student"
        text = VGroup(name, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bar_l = Line(UP, DOWN, color=ACCENT, stroke_width=4).scale_to_fit_height(text.height + 0.1)
        bar_l.next_to(text, LEFT, buff=0.22)
        card_in = VGroup(bar_l, text)
        panel = RoundedRectangle(corner_radius=0.16, width=card_in.width + 0.5, height=card_in.height + 0.4)
        panel.set_fill(BG, 0.88).set_stroke(FAINT, 1.5).move_to(card_in)
        card = VGroup(panel, card_in).to_corner(UL, buff=0.55)     # left edge inside the +-6.6 safe area
        card.shift(DOWN * (card.get_top()[1] - (tray.get_bottom()[1] - 0.3))).set_z_index(9)
        self.at("nelson", FadeIn(panel), Create(bar_l), FadeIn(name, shift=RIGHT * 0.15), run_time=0.6)
        self.at(self.w("p3s3", "nineteen") - 0.05, FadeIn(p_year, shift=UP * 0.1), run_time=0.45)
        self.at(self.w("p3s3", "eighteen-year-old"), FadeIn(p_age, shift=UP * 0.1), run_time=0.45)
        self.at(self.w("p3s3", "student"), FadeIn(p_who, shift=UP * 0.1), run_time=0.45)

        # ============================== P4: today: five, six or seven
        # the bar sits at its fixed home (storyboard), built exactly as in every later scene: the shared BoundsBar
        # at 0.8 on a stroke-less BG backing panel (+0.5 / +0.3 padding, as in S04, S10, S11)
        sb = BoundsBar(1).scale(0.8).to_edge(DOWN, buff=0.3)
        back = RoundedRectangle(corner_radius=0.2, width=sb.width + 0.5, height=sb.height + 0.3)
        back.set_fill(BG, 0.94).set_stroke(width=0).move_to(sb)
        board = VGroup(back, sb).set_z_index(10)
        self.at("p4", FadeIn(board, shift=UP * 0.2), card.animate.set_opacity(0.6),
                run_time=0.9)
        # "the answer": the label 'colors needed' brightens and stays bright through five / six / seven
        # (it is what tells the viewer what the row of numbers means); it returns to DIM with {#which}
        self.at(self.w("p4s1", "answer"), self.pulse(sb.title, 1.15, INK, keep_color=True), run_time=0.45)

        # {#five} {#six} {#seven}: each digit lights up, and the paint box echoes it: 5 -> five paints stay bright
        # (orange + teal step back), 6 -> orange returns, 7 -> teal returns, all seven paints again
        # (built per beat: an .animate builder snapshots its target when created, so building all three up front
        #  would let the later targets overwrite the earlier ones)
        tray_echo = {"five": ((5, OFF_OP), (6, OFF_OP)), "six": ((5, 1.0),), "seven": ((6, 1.0),)}
        for mk, i in (("five", 4), ("six", 5), ("seven", 6)):
            self.at(mk, self.pulse(sb.cells[i], 1.45, ACCENT, keep_color=True),
                    *[swatches[k].animate.set_fill(opacity=o) for k, o in tray_echo[mk]], run_time=0.55)

        # {#which}: the big ? shrinks and parks just above the lit 5 6 7; as it lands, the three digits glow once
        trio = VGroup(*sb.cells[4:7])
        q_target = q.copy().scale(0.36).next_to(back, UP, buff=0.1).set_x(trio.get_x())
        glow = AnimationGroup(*[self.pulse(c, 1.25) for c in trio], run_time=0.35)
        self.at("which", AnimationGroup(Transform(q, q_target, rate_func=smooth, run_time=0.45),
                                        sb.title.animate(run_time=0.45).set_color(DIM),
                                        Succession(Wait(0.3), glow)), run_time=0.65)
        # tail: everything fades out together (~0.7 s ease), leaving one clean BG frame before the cut
        self.until(self.t("end") - 0.07, *[FadeOut(m) for m in (cells, box, card, board, q)],
                   rate_func=rate_functions.ease_in_out_sine)

