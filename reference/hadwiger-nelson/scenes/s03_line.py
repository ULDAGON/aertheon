"""S03_Line - Warm-up: a line needs two colors.

Beats (times come from timeline/S03_Line.json, never hard-coded except word-relative offsets):
  p1  the number line draws; a blue point's unit stick grows and sweeps a full ring (calm, ~1.3 s); the two
      crossings with the line are marked while the whole ring is still visible, then the ring fades and the
      two unit sticks remain.  "either side": both markers try blue -> a red cross each; pause: back to hollow.
  p2  one color: the whole line turns blue, the ring points turn blue -> sticks BAD.  Two colors: alternating unit
      stripes [k, k+1); zoom on a border point: it belongs to the stripe on its right (solid / hollow ends)
  p3  a floating stick glides along, its ends always in neighboring stripes; it comes to rest with its left end
      exactly on the zoomed border point (both pulse yellow).  "line: exactly 2"
  p4  stripes stretch into full-height bands = the plane; the stick turns upright inside one band -> ends match, BAD
  p5  the stick pivots about its lower end through a full turn; the ring it draws is red wherever the free end
      lands in the pinned end's own band; the red arcs pulse on "hard"; fade out.
Scale: UNIT = 2.0 manim units per problem unit.  No BoundsBar in this scene (the camera zoom returns to home).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403
from manim.animation.animation import prepare_animation  # noqa: E402

U = UNIT                 # 2.0 manim per unit
BAR_H = 0.14             # thickness of the line / stripes
EDGES_U = [-3.25, -3, -2, -1, 0, 1, 2, 3, 3.25]           # the visible line: x = -6.5 .. 6.5 manim
SEGS = [(a * U, b * U, int(np.floor(a + 1e-9))) for a, b in zip(EDGES_U[:-1], EDGES_U[1:])]
TICKS_U = [-3, -2, -1, 0, 1, 2, 3]
BAND_OPACITY = 0.86
BAND_LIFT = 0.06         # bands are the paint lifted slightly towards white, so they stay clearly blue / yellow
LINE_OPACITY = 0.55   # the unpainted line: dim, so unit sticks on it stand out
FRAME_W = config.frame_width
ZOOM = 3.0
BORDER_X = 1 * U         # the zoomed border point x = 1 unit
SPLIT = 0.18             # half gap when the stripes are pulled apart at the zoom


def paint(k):
    return PALETTE[k % 2]           # even stripe blue, odd stripe yellow (== geom.line_color)


def band_paint(k):
    return interpolate_color(ManimColor(paint(k)), ManimColor(WHITE), BAND_LIFT)


def color_at(x):
    """Paint of the stripe / band under manim x (a border point takes the stripe on its right)."""
    return PALETTE[line_color(round(x / U, 9))]


def rect(l, r, y0, y1, color, opacity=1.0):
    m = Polygon([l, y0, 0], [r, y0, 0], [r, y1, 0], [l, y1, 0], stroke_width=0)
    return m.set_fill(color, opacity)


def set_rect(m, l, r, y0, y1):
    m.set_points_as_corners([[l, y0, 0], [r, y0, 0], [r, y1, 0], [l, y1, 0], [l, y0, 0]])


def make_bars(colors, opacity=1.0):
    return VGroup(*[rect(l, r, -BAR_H / 2, BAR_H / 2, c, opacity) for (l, r, _), c in zip(SEGS, colors)])


def wipe(layer, x0, x1, ticks=None, **kw):
    """Reveal `layer` (bars matching SEGS) from x0 to x1, left to right; optional ticks appear as the front passes.
    Add `layer` to the scene only right before playing this (its first frame hides every bar)."""
    full = [(l, r) for l, r, _ in SEGS]
    ops = [b.get_fill_opacity() for b in layer]
    group = VGroup(layer, ticks) if ticks is not None else layer

    def upd(_, a):
        f = x0 + a * (x1 - x0)
        for part, (l, r), op in zip(layer, full, ops):
            rr = min(r, f)
            if rr <= l + 1e-4:
                set_rect(part, l, l + 1e-4, -BAR_H / 2, BAR_H / 2)
                part.set_fill(opacity=0)
            else:
                set_rect(part, l, rr, -BAR_H / 2, BAR_H / 2)
                part.set_fill(opacity=op)
        if ticks is not None:
            for tk in ticks:
                tk.set_stroke(opacity=1.0 if tk.get_center()[0] <= f else 0.0)

    return UpdateFromAlphaFunc(group, upd, **kw)


def glide(e=0.2):
    """Rate function with constant speed in the middle and short, gentle ramps (length e) at both ends."""
    v = 1 / (1 - e)

    def f(t):
        if t < e:
            return v * t * t / (2 * e)
        if t > 1 - e:
            return 1 - v * (1 - t) ** 2 / (2 * e)
        return v * (t - e / 2)
    return f


def timed(*items):
    """Overlapping animations on one private clock: items are (start, anim, duration) in seconds relative to the
    group start.  Late items only begin (and only join the scene) at their start.  Returns (group, total)."""
    parts, total = [], 0.0
    for t0, anim, dur in items:
        anim = prepare_animation(anim)
        anim.run_time = dur
        parts.append(Succession(Wait(t0), anim) if t0 > 1e-6 else anim)
        total = max(total, t0 + dur)
    # introducer=True: stops Scene.play from adding every member mobject up front (they would show at full
    # state before their start); each sub-animation adds its own mobject when it begins.  Mobjects of
    # non-introducing sub-animations must already be in the scene.
    return AnimationGroup(*parts, introducer=True), total


class Stick(VGroup):
    """A unit stick whose two end dots always show the paint beneath them."""

    def __init__(self, a, b, r=0.1, width=5, halo=False, rim=False):
        super().__init__()
        self.line = Line(a, b, color=UNIT_COLOR, stroke_width=width)
        if halo:
            self.line.set_stroke(BG, width + 5, background=True)
        self.da, self.db = pt(a, color_at(a[0]), r), pt(b, color_at(b[0]), r)
        if rim:   # a thin light outer ring so a blue dot still reads on a blue band
            for d in (self.da, self.db):
                d.add(Circle(radius=r + 0.035, color=INK, stroke_width=1.6).move_to(d))
        self.add(self.line, self.da, self.db)

    def place(self, a, b):
        self.line.put_start_and_end_on(a, b)
        self.da.move_to(a)
        self._paint(self.da, a)
        self.db.move_to(b)
        self._paint(self.db, b)
        return self

    @staticmethod
    def _paint(d, p):
        d.set_fill(color_at(p[0]), 1, family=False)


def shake(mob, amp=0.07, **kw):
    start = mob.get_center().copy()

    def upd(m, a):
        m.move_to(start + RIGHT * amp * np.sin(a * 6 * PI) * (1 - a))

    return UpdateFromAlphaFunc(mob, upd, **kw)


def pulse(mobs, scale=1.4, **kw):
    """Each mobject grows and shrinks about its own centre."""
    return AnimationGroup(*[m.animate(rate_func=there_and_back).scale(scale) for m in mobs], **kw)


def pulse_fill(mobs, fill, scale=1.4):
    """Pulse each mobject once while its fill drains to `fill` (one updater, so the two changes never fight)."""
    base = [(m.width, ManimColor(m.get_fill_color())) for m in mobs]
    target = ManimColor(fill)

    def upd(_, a):
        for m, (w, c0) in zip(mobs, base):
            m.set_fill(interpolate_color(c0, target, smooth(a)), 1)
            m.scale_to_fit_width(w * (1 + (scale - 1) * there_and_back(a)))

    return UpdateFromAlphaFunc(VGroup(*mobs), upd)


class S03_Line(TimedScene):
    def construct(self):
        frame = self.camera.frame
        words = [s["words"] for s in self.tl["sentences"]]

        # ------------------------------------------------------------ p1: the line, a point's ring = two points
        title = T("warm-up: a line", 30, DIM).to_edge(UP, buff=0.45)
        self.at("p1", FadeIn(title, shift=DOWN * 0.15), run_time=0.6)

        bars = make_bars([DIM] * len(SEGS), LINE_OPACITY)
        ticks = VGroup(*[Line([k * U, -0.1, 0], [k * U, -0.3, 0], color=DIM, stroke_width=2.5) for k in TICKS_U])
        ticks.set_z_index(-1)
        for tk in ticks:
            tk.set_stroke(opacity=0)
        self.until("line")
        self.add(ticks, bars)
        self.at("line", wipe(bars, -6.5, 6.5, ticks, rate_func=smooth), run_time=1.0)

        P = np.array([0.3 * U, 0, 0])
        L_pt, R_pt = P + LEFT * U, P + RIGHT * U            # x = -0.7 and 1.3 units
        hollow = ring(P, r=0.11).set_z_index(3)
        blue = pt(P, BLUE_P, r=0.11).set_z_index(3)

        # the stick grows from the blue point and sweeps once around it; its free end draws the unit ring
        arm = Line(P, R_pt, color=UNIT_COLOR, stroke_width=6).set_z_index(2)
        arc = Arc(radius=U, start_angle=0, angle=1e-3, arc_center=P, color=UNIT_COLOR, stroke_width=3)
        arc.set_stroke(opacity=0)

        def sweep(_, a):
            ang = TAU * a
            arm.put_start_and_end_on(P, P + U * np.array([np.cos(ang), np.sin(ang), 0]))
            arc.become(Arc(radius=U, start_angle=0, angle=max(ang, 1e-3), arc_center=P,
                           color=UNIT_COLOR, stroke_width=3))
            arc.set_stroke(opacity=1.0 if ang > 0.02 else 0.0)

        # only the two points where the ring meets the line remain: marked on "two" while the ring is still whole
        mL, mR = ring(L_pt, r=0.11).set_z_index(3), ring(R_pt, r=0.11).set_z_index(3)
        t0 = 2.45
        w_here, w_two = words[1][0]["s"], words[1][6]["s"]            # "Here", "two"
        sweep_start, sweep_rt = 3.25, 1.33                            # arm grows on "point's"; sweep ends ~4.58
        grp, total = timed(
            (0.0, GrowFromCenter(hollow), 0.3),
            (w_here - 0.05 - t0, FadeIn(blue), 0.3),
            (sweep_start - 0.25 - t0, GrowFromPoint(arm, P), 0.25),
            (sweep_start - t0, UpdateFromAlphaFunc(VGroup(arm, arc), sweep, rate_func=glide(0.2)), sweep_rt),
            (w_two - t0, AnimationGroup(GrowFromCenter(mL), GrowFromCenter(mR)), 0.35),
            (w_two + 0.45 - t0, pulse([mL, mR], 1.45), 0.45),
        )
        self.add(arc)
        self.at(t0, grp, run_time=total)
        self.remove(hollow)

        # one unit to either side: the second stick draws, the ring (whole until now) fades
        stick_R = arm
        stick_L = Line(P, L_pt, color=UNIT_COLOR, stroke_width=6).set_z_index(2)
        one_L = N("1", 30, UNIT_COLOR).move_to((P + L_pt) / 2 + UP * 0.38)
        one_R = N("1", 30, UNIT_COLOR).move_to((P + R_pt) / 2 + UP * 0.38)
        w_one = words[1][8]["s"]          # "one" (unit)
        self.at(w_one, Create(stick_L), FadeIn(one_L), FadeIn(one_R), FadeOut(arc), run_time=0.5)

        # ... and neither may be blue: try blue, cross it out while still blue; back to hollow in the pause
        crosses = VGroup(cross_mark(L_pt + UP * 0.4, size=0.11, width=5),
                         cross_mark(R_pt + UP * 0.4, size=0.11, width=5))
        w_either = words[1][11]["s"]
        self.at(w_either - 0.1, mL.animate.set_fill(BLUE_P, 1), mR.animate.set_fill(BLUE_P, 1), run_time=0.3)
        self.play(*[Create(c, lag_ratio=0.4) for c in crosses], run_time=0.35)
        self.at(self.t("p1_end") + 0.05, pulse_fill([mL, mR], BG), run_time=0.5)

        # ------------------------------------------------------------ p2: one color fails; two colors = stripes
        blue_line = make_bars([BLUE_P] * len(SEGS))
        blue_mL, blue_mR = pt(L_pt, BLUE_P, r=0.11).set_z_index(3), pt(R_pt, BLUE_P, r=0.11).set_z_index(3)
        self.until("one")
        self.add(blue_line)                               # added only now: the wipe's first frame hides it
        self.at("one", wipe(blue_line, -6.5, 6.5, rate_func=smooth),
                Transform(mL, blue_mL), Transform(mR, blue_mR), run_time=0.5)
        self.remove(bars)
        bars = blue_line

        sticks = VGroup(stick_L, stick_R)
        self.at("fails", sticks.animate.set_color(BAD),
                Flash(L_pt, color=BAD, flash_radius=0.28, line_length=0.16),
                Flash(R_pt, color=BAD, flash_radius=0.28, line_length=0.16),
                *[Indicate(c, color=BAD, scale_factor=1.5) for c in crosses], run_time=0.5)
        clash = VGroup(sticks, mL, mR, blue, crosses, one_L, one_R)

        # clear, back to an unpainted line
        self.at("p2s1_end", FadeOut(clash), *[b.animate.set_fill(DIM, LINE_OPACITY) for b in bars], run_time=0.5)

        striped = make_bars([paint(k) for _, _, k in SEGS])
        self.until("stripes")
        self.add(striped)                                 # added only now: the wipe's first frame hides it
        self.at("stripes", wipe(striped, -6.5, 6.5, rate_func=smooth), run_time=1.1)
        self.remove(bars)
        bars = striped

        # "one unit long": a dimension bracket over the stripe [0, 1)
        y_b = 0.34
        bracket = VGroup(Line([0, y_b, 0], [U, y_b, 0]), Line([0, y_b - 0.12, 0], [0, y_b + 0.12, 0]),
                         Line([U, y_b - 0.12, 0], [U, y_b + 0.12, 0])).set_stroke(DIM, 2.5)
        bracket_lab = N("1", 30, DIM).next_to(bracket, UP, buff=0.12)
        w_unit = words[3][5]["s"]         # "one" unit long
        self.at(w_unit, GrowFromCenter(bracket), FadeIn(bracket_lab), run_time=0.4)
        # clear the bracket and title in the sentence gap, so only the camera moves at {#left}
        self.at("p2s2_end", FadeOut(bracket), FadeOut(bracket_lab), FadeOut(title), run_time=0.4)

        # zoom onto the border point x = 1: it belongs to the stripe on its right
        self.at("left", frame.animate.move_to([BORDER_X, 0, 0]).set(width=FRAME_W / ZOOM),
                run_time=0.7, rate_func=smooth)
        bp = Circle(radius=0.075, color=INK, stroke_width=1.6).set_fill(BG, 1).move_to([BORDER_X, 0, 0])
        bp.set_z_index(4)
        self.play(GrowFromCenter(bp), run_time=0.25)

        left_side = VGroup(*[b for b, (l, r, _) in zip(bars, SEGS) if r <= BORDER_X + 1e-6],
                           *[t for t, k in zip(ticks, TICKS_U) if k * U < BORDER_X - 1e-6])
        right_side = VGroup(*[b for b, (l, r, _) in zip(bars, SEGS) if l >= BORDER_X - 1e-6],
                            *[t for t, k in zip(ticks, TICKS_U) if k * U >= BORDER_X - 1e-6])
        solid = Dot([BORDER_X + SPLIT, 0, 0], radius=0.075, color=YELLOW_P).set_z_index(4)
        solid.set_stroke(BG, width=2, background=True)
        open_end = Circle(radius=0.07, color=BLUE_P, stroke_width=1.8).set_fill(BG, 1)
        open_end.move_to([BORDER_X - SPLIT, 0, 0]).set_z_index(4)
        w_belongs = words[4][3]["s"]
        self.at(w_belongs, left_side.animate.shift(LEFT * SPLIT), right_side.animate.shift(RIGHT * SPLIT),
                Transform(bp, solid), FadeIn(open_end, shift=LEFT * SPLIT), run_time=0.6)

        arrow = CurvedArrow([BORDER_X + SPLIT + 0.06, 0.16, 0], [BORDER_X + SPLIT + 0.62, 0.1, 0],
                            angle=-PI / 2, color=DIM, stroke_width=2, tip_length=0.09)
        w_right = words[4][7]["s"]        # "on" its right
        self.at(w_right - 0.35, Create(arrow), run_time=0.45)

        # pause: rejoin and zoom back out to the home frame
        self.at("p2_end", FadeOut(arrow), FadeOut(open_end),
                left_side.animate.shift(RIGHT * SPLIT), right_side.animate.shift(LEFT * SPLIT),
                bp.animate.move_to([BORDER_X, 0, 0]),
                frame.animate.move_to(ORIGIN).set(width=FRAME_W), run_time=0.75)

        # ------------------------------------------------------------ p3: slide a stick along
        y_s = 0.62
        c0, c1 = -2.6 * U, BORDER_X + U / 2          # comes to rest with its left end exactly on x = 1
        A0 = np.array([c0 - U / 2, y_s, 0])
        stick = Stick(A0, A0 + RIGHT * U, r=0.1, width=5).set_z_index(3)
        plumbs = VGroup(*[Line(ORIGIN, UP, color=DIM, stroke_width=1.5, stroke_opacity=0.8) for _ in range(2)])
        check = check_mark(ORIGIN, size=0.17).move_to([c0, y_s + 0.5, 0]).set_stroke(opacity=0)

        def place_all(c):
            A = np.array([c - U / 2, y_s, 0])
            B = A + RIGHT * U
            stick.place(A, B)
            for pl, e in zip(plumbs, (A, B)):
                pl.put_start_and_end_on([e[0], y_s - 0.11, 0], [e[0], BAR_H / 2 + 0.02, 0])
            check.move_to([c, y_s + 0.5, 0])

        place_all(c0)
        self.at("p3", FadeIn(stick), FadeIn(plumbs), run_time=0.45)
        self.add(check)

        # glide on "stick along" through "neighboring stripes", at an even, readable speed
        slide_start = self.now
        slide_end = self.t("p3s1_end") + 0.15
        slide_rt = slide_end - slide_start
        t_check = 0.4   # the check fades in over the first part of the slide
        ease = glide(0.2)

        def slide(_, a):
            place_all(c0 + ease(a) * (c1 - c0))
            check.set_stroke(opacity=min(1.0, a * slide_rt / t_check))

        self.play(UpdateFromAlphaFunc(VGroup(stick, plumbs, check), slide, rate_func=linear), run_time=slide_rt)
        # landing: its left end sits exactly on the border point, and takes the right-hand (yellow) stripe
        self.play(Indicate(bp, color=YELLOW_P, scale_factor=2.0), Indicate(stick.da, color=YELLOW_P, scale_factor=1.7),
                  run_time=0.55)

        lab_txt, lab_two = T("line: exactly", 40, ACCENT), N("2", 46, ACCENT)
        lab_two.next_to(lab_txt, RIGHT, buff=0.18).align_to(lab_txt[0], DOWN)    # on the baseline ("l"), not the "y"
        label = VGroup(lab_txt, lab_two).move_to([0, 2.2, 0])
        self.at("exactly", FadeIn(label, shift=DOWN * 0.15), run_time=0.5)
        self.at(self.t("p3_end") + 0.1, Indicate(check, color=GOOD, scale_factor=1.35), run_time=0.55)

        # ------------------------------------------------------------ p4: bands = the plane; the stick turns
        self.at("p4", FadeOut(VGroup(stick, plumbs, check, label, bp)), run_time=0.5)

        bands = VGroup(*[rect(k * U, (k + 1) * U, -4.3, 4.3, band_paint(k), BAND_OPACITY) for _, _, k in SEGS])
        self.at("bands", *[Transform(b, bd) for b, bd in zip(bars, bands)], FadeOut(ticks),
                run_time=1.5, rate_func=smooth)

        cap_txt = T("the plane", 30, INK)
        cap_bg = RoundedRectangle(corner_radius=0.12, width=cap_txt.width + 0.5, height=cap_txt.height + 0.35,
                                  stroke_width=0).set_fill(BG, 0.85)
        cap = VGroup(cap_bg, cap_txt).to_corner(UL, buff=0.6)
        self.at("plane", FadeIn(cap), run_time=0.4)

        C = np.array([0.75 * U, 1.0, 0])            # inside the blue band [0, 1)
        stick2 = Stick(C + LEFT * U / 2, C + RIGHT * U / 2, r=0.13, width=6, halo=True, rim=True).set_z_index(3)
        self.at("p4s2", FadeIn(stick2), FadeOut(cap), run_time=0.45)

        def turn_to(th0, th1):
            def upd(_, a):
                th = th0 + a * (th1 - th0)
                d = (U / 2) * np.array([np.cos(th), np.sin(th), 0])
                stick2.place(C - d, C + d)
            return UpdateFromAlphaFunc(stick2, upd)

        self.at("turn", turn_to(0, PI / 6), run_time=0.7)
        self.at("p4s3", turn_to(PI / 6, PI / 2), run_time=1.1)   # upright: both ends in one blue band

        low, top = C + DOWN * U / 2, C + UP * U / 2
        cross = cross_mark(C + LEFT * 0.62, size=0.2, width=6)
        cross.set_stroke(BG, 10, background=True)
        self.at("same", Flash(low, color=BAD, flash_radius=0.32, line_length=0.18),
                Flash(top, color=BAD, flash_radius=0.32, line_length=0.18), Create(cross, lag_ratio=0.4),
                stick2.line.animate.set_stroke(BAD), run_time=0.5)
        self.play(shake(stick2, amp=0.06), run_time=0.35)      # the scene's one contradiction shake

        # ------------------------------------------------------------ p5: the freedom to turn
        pin = Circle(radius=0.22, color=UNIT_COLOR, stroke_width=2.5).move_to(low).set_z_index(2)
        pin.set_stroke(BG, 6, background=True)
        self.at("p5", FadeOut(cross), stick2.line.animate.set_stroke(UNIT_COLOR), GrowFromCenter(pin), run_time=0.4)

        # the ring the free end traces, cut where it enters the pinned end's own (blue) band [0, 2):
        # x = 1.5 + 2 cos(th) in [0, 2)  <=>  cos(th) in [-0.75, 0.25)
        a_in, a_out = np.arccos(0.25), np.arccos(-0.75)          # ~75.5 deg, ~138.6 deg
        start = PI / 2
        breaks = [start, a_out, TAU - a_out, TAU - a_in, TAU + a_in, start + TAU]
        seg_cols = [BAD, UNIT_COLOR, BAD, UNIT_COLOR, BAD]
        assert all((color_at(low[0] + U * np.cos((s + e) / 2)) == BLUE_P) == (c == BAD)
                   for s, e, c in zip(breaks[:-1], breaks[1:], seg_cols))
        trace = VGroup(*[Arc(radius=U, start_angle=s, angle=1e-3, arc_center=low) for s in breaks[:-1]])

        def seg_arc(s, e, col, width=4):
            m = Arc(radius=U, start_angle=s, angle=max(e - s, 1e-3), arc_center=low)
            return m.set_stroke(col, width).set_stroke(BG, width + 4, background=True)

        for seg in trace:
            seg.set_stroke(opacity=0).set_stroke(opacity=0, background=True)
        self.add(trace)

        def pivot(_, a):
            ph = start + TAU * a
            stick2.place(low, low + U * np.array([np.cos(ph), np.sin(ph), 0]))
            for seg, s, e, col in zip(trace, breaks[:-1], breaks[1:], seg_cols):
                if ph <= s + 1e-4:
                    seg.set_stroke(opacity=0).set_stroke(opacity=0, background=True)
                else:
                    seg.become(seg_arc(s, min(e, ph), col))

        w_hard = words[10][10]["s"]
        pivot_start = self.t("p5") + 0.45                          # on "freedom"
        pivot_end = w_hard - 0.15                                  # the ring closes just before "hard"
        self.at(pivot_start, UpdateFromAlphaFunc(VGroup(stick2, trace), pivot, rate_func=glide(0.15)),
                run_time=pivot_end - pivot_start)

        # "so hard": the arcs where turning runs back into its own color pulse
        bad = VGroup(trace[0], trace[2], trace[4])

        def throb(_, a):
            w = 4 + 2 * smooth(a) + 4 * there_and_back(a)     # swells, then settles a little thicker (6)
            bad.set_stroke(width=w).set_stroke(width=w + 4, background=True)

        self.at(w_hard - 0.05, UpdateFromAlphaFunc(bad, throb), run_time=0.6)

        # final pause: everything fades out to the empty background
        self.at(self.t("p5_end") + 0.16, FadeOut(VGroup(bars, stick2, trace, pin)), run_time=0.7)

