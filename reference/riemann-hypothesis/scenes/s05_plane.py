"""S05 - Zeta on a plane.

P1  the input plane (1 unit = 1.1, origin at (-4.3, -1.6)); the dot 2 across, 3 up: 2 + 3i.
P2  the right part becomes an output panel. The terms 1/n^s are arrows laid tip to tail (s = 2: the S04 bar).
    As the input climbs from 2 to 2 + 3i every term spins by -t ln n (exact), so the chain curls into a spiral;
    zooming in shows it settling on zeta(2 + 3i). Left of 1 (s = 0.6 + 3i) 2,000 exact terms keep looping outward.
P3  a side demo (many smooth continuations on a line); on the plane, a patch of real domain colouring spreads
    over the whole region right of 1 (zeta_np, verified against mpmath).
P4  the view widens to real part -10..3, height -30..30 (non-uniform scale of the plane content, no camera move);
    the colouring flows across 1 to fill the plane; a ring marks the pole at 1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from topic import *  # noqa: E402,F401,F403

FW, FH = config.frame_width / 2, config.frame_height / 2
CACHE = ROOT / "out" / "cache"


# ---------------------------------------------------------------- the input plane: problem coords -> scene
class View:
    """Problem point (cx, cy) sits at the scene origin; sx, sy = scene units per problem unit."""

    def __init__(self, cx, cy, sx, sy):
        self.cx, self.cy, self.sx, self.sy = cx, cy, sx, sy

    def x(self, re):
        return (re - self.cx) * self.sx

    def y(self, im):
        return (im - self.cy) * self.sy

    def p(self, re, im=0.0):
        return np.array([self.x(re), self.y(im), 0.0])

    def inv(self, x, y):
        return x / self.sx + self.cx, y / self.sy + self.cy


def lerp_view(a, b, t):
    return View(a.cx + (b.cx - a.cx) * t, a.cy + (b.cy - a.cy) * t,
                a.sx * (b.sx / a.sx) ** t, a.sy * (b.sy / a.sy) ** t)


V1 = View(4.3 / 1.1, 1.6 / 1.1, 1.1, 1.1)          # origin at (-4.3, -1.6), 1 unit = 1.1
V2 = View(-3.5, 0.0, 13.2 / 13, 7.2 / 60)          # real part -10..3 across x -6.6..6.6, height -30..30 in y -3.6..3.6
assert np.allclose(V1.p(0, 0), [-4.3, -1.6, 0]) and np.allclose([V2.x(-10), V2.x(3)], [-6.6, 6.6])


def segs_mob(segs, color, width, opacity=1.0):
    """One VMobject made of many straight segments (light to rebuild every frame)."""
    m = VMobject()
    pts = []
    for a, b in segs:
        a, b = np.asarray(a, float), np.asarray(b, float)
        pts += [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]
    if pts:
        m.set_points(np.array(pts))
    return m.set_stroke(color, width, opacity=opacity).set_fill(opacity=0)


def grid_segs(view, dre, dim, re_rng, im_rng, squash=1.0):
    """Grid lines every dre (vertical lines) and dim (horizontal lines); squash < 1 pulls them toward the real axis."""
    y0 = view.y(0)
    segs = []
    for re in np.arange(re_rng[0], re_rng[1] + 1e-9, dre):
        x = view.x(re)
        if -FW - 0.2 < x < FW + 0.2:
            segs.append(([x, y0 + squash * (-FH - 0.2 - y0), 0], [x, y0 + squash * (FH + 0.2 - y0), 0]))
    for im in np.arange(im_rng[0], im_rng[1] + 1e-9, dim):
        if abs(im) < 1e-9:
            continue
        y = y0 + squash * (view.y(im) - y0)
        if -FH - 0.2 < y < FH + 0.2:
            segs.append(([-FW - 0.2, y, 0], [FW + 0.2, y, 0]))
    return segs


def tick_labels(view, res, ims, size=26, opacity=1.0):
    g = VGroup()
    ax_y, ax_x = view.y(0), view.x(0)
    for re in res:
        s = "0" if re == 0 else (f"{re}".replace("-", "−"))
        if re == 0:
            continue
        g.add(N(s, size, DIM).move_to([view.x(re), ax_y - 0.33, 0]))
    for im, s in ims:
        g.add(N(s, size, DIM).next_to([ax_x, view.y(im), 0], LEFT, buff=0.16))
    return VGroup(*[VGroup(bg_rect(m, 0.05, 0.75 * opacity), m.set_opacity(opacity)) for m in g])


def tick_marks(view, res, ims):
    ax_y, ax_x = view.y(0), view.x(0)
    segs = [([view.x(r), ax_y - 0.08, 0], [view.x(r), ax_y + 0.08, 0]) for r in res]
    segs += [([ax_x - 0.08, view.y(i), 0], [ax_x + 0.08, view.y(i), 0]) for i in ims]
    return segs_mob(segs, NEUTRAL, 3)


RES1, IMS1 = list(range(-2, 5)), [(1, "i"), (2, "2i"), (3, "3i")]
RES2 = list(range(-10, 3, 2))
IMS2 = [(10, "10i"), (20, "20i"), (-10, "−10i"), (-20, "−20i")]


def plane_state(view, g1=1.0, g2=0.0, l1=1.0, l2=0.0, grid_op=1.0):
    """Grid(s), axes, ticks, tick labels for a view. g1/l1: the fine grid + labels of V1, g2/l2: those of V2."""
    g = VGroup()
    if g1 > 0.01:
        g.add(segs_mob(grid_segs(view, 1, 1, (-12, 12), (-36, 36)), FAINT, 1.6, g1 * grid_op))
    if g2 > 0.01:
        g.add(segs_mob(grid_segs(view, 1, 5, (-12, 12), (-35, 35)), FAINT, 1.6, g2 * grid_op))
    g.add(segs_mob([([-FW - 0.2, view.y(0), 0], [FW + 0.2, view.y(0), 0]),
                    ([view.x(0), -FH - 0.2, 0], [view.x(0), FH + 0.2, 0])], NEUTRAL, 3))
    if l1 > 0.01:
        g.add(tick_marks(view, RES1, [i for i, _ in IMS1]).set_stroke(opacity=l1), tick_labels(view, RES1, IMS1, opacity=l1))
    if l2 > 0.01:
        g.add(tick_marks(view, RES2, [i for i, _ in IMS2]).set_stroke(opacity=l2), tick_labels(view, RES2, IMS2, 24, l2))
    return g.set_z_index(0.5)


def unit_line(view, opacity=1.0):
    """The dashed line 'real part 1'."""
    x = view.x(1)
    return DashedLine([x, -FH - 0.2, 0], [x, FH + 0.2, 0], dash_length=0.14, dashed_ratio=0.55).set_stroke(INK, 2.2, opacity)


def hatch(x0, x1, y0=-FH - 0.1, y1=FH + 0.1, gap=0.36):
    """Diagonal hatching clipped to the rectangle [x0, x1] x [y0, y1]."""
    segs = []
    step = gap * np.sqrt(2)
    for c in np.arange(y0 - x1, y1 - x0, step):     # lines y = x + c
        xa, xb = max(x0, y0 - c), min(x1, y1 - c)
        if xb > xa + 0.02:
            segs.append(([xa, xa + c, 0], [xb, xb + c, 0]))
    return segs_mob(segs, DIM, 1.6, 0.55)


def swap(m, new):
    """Replace a dynamic group's content (lighter and safer than become for changing structure).
    manim keeps the family list it saw when the play began, so the old children are blanked, never left stale."""
    for old in m.submobjects:
        for f in old.get_family():
            f.points = np.zeros((0, 3))
    m.submobjects = [new]
    return m


def bg_rect(mob, buff=0.12, opacity=0.9):
    return RoundedRectangle(corner_radius=0.08, width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                            stroke_width=0).set_fill(BG, opacity).move_to(mob.get_center())


def card(mob, pad=0.12, opacity=0.9):
    """A BG backing card behind a label so it reads over grid or colour."""
    return VGroup(bg_rect(mob, pad, opacity), mob)


# ---------------------------------------------------------------- domain colouring (hue = direction of zeta's output)
SAT = 0.7          # this scene's domain colouring saturation (hue changes must read at 480p)


def hsv_rgb(hue, sat=SAT, val=0.8):
    i = np.floor(hue * 6).astype(int) % 6
    f = hue * 6 - np.floor(hue * 6)
    p, q, t = val * (1 - sat), val * (1 - sat * f), val * (1 - sat * (1 - f))
    v = np.full_like(hue, val)
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return (np.stack([r, g, b], -1) * 255).astype(np.uint8)


class Field:
    """Real domain colouring of zeta over [re0, re1] x [im0, im1], drawn through a View with a per-pixel alpha mask.
    Only the part inside the frame is cropped and drawn, so a strongly stretched view stays light."""

    def __init__(self, name, re0, re1, im0, im1, w, h, alpha=0.9, sat=SAT):
        CACHE.mkdir(parents=True, exist_ok=True)
        f = CACHE / f"s05_{name}_{w}x{h}_s{int(sat * 100)}.npy"
        if f.exists():
            self.rgb = np.load(f)
        else:
            self.rgb = domain_color_rgb(re0, re1, im0, im1, w, h, sat=sat)
            np.save(f, self.rgb)
        self.re = np.linspace(re0, re1, w)
        self.im = np.linspace(im1, im0, h)          # row 0 = top
        self.dre, self.dim = self.re[1] - self.re[0], self.im[0] - self.im[1]
        self.a = alpha
        self.mob = ImageMobject(np.zeros((2, 2, 4), np.uint8)).set_z_index(0.2)
        self.mob.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

    def draw(self, view, mask, opacity=1.0):
        a0, b0 = view.inv(-FW - 0.1, -FH - 0.1)
        a1, b1 = view.inv(FW + 0.1, FH + 0.1)
        c0 = max(0, int(np.searchsorted(self.re, a0)) - 1)
        c1 = min(len(self.re), int(np.searchsorted(self.re, a1)) + 1)
        r0 = max(0, int(np.searchsorted(-self.im, -b1)) - 1)
        r1 = min(len(self.im), int(np.searchsorted(-self.im, -b0)) + 1)
        if c1 - c0 < 2 or r1 - r0 < 2:
            self.mob.pixel_array = np.zeros((2, 2, 4), np.uint8)
            return self.mob
        RE, IM = self.re[None, c0:c1], self.im[r0:r1, None]
        A = np.broadcast_to(np.clip(mask(RE, IM), 0, 1), (r1 - r0, c1 - c0)) * (255 * self.a * opacity)
        self.mob.pixel_array = np.dstack([self.rgb[r0:r1, c0:c1], A.astype(np.uint8)])
        left, right = self.re[c0] - self.dre / 2, self.re[c1 - 1] + self.dre / 2
        top, bot = self.im[r0] + self.dim / 2, self.im[r1 - 1] - self.dim / 2
        self.mob.points = np.array([view.p(left, top), view.p(right, top), view.p(left, bot), view.p(right, bot)])
        return self.mob


def color_wheel(r=0.3, px=96):
    u = np.linspace(-1, 1, px)
    X, Y = np.meshgrid(u, -u)
    hue = (np.arctan2(Y, X) / (2 * np.pi)) % 1.0
    rgb = hsv_rgb(hue)
    a = (np.clip((1 - np.hypot(X, Y)) * px / 3, 0, 1) * 255).astype(np.uint8)
    img = ImageMobject(np.dstack([rgb, a])).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    img.stretch_to_fit_width(2 * r).stretch_to_fit_height(2 * r)
    return img


# ---------------------------------------------------------------- the output panel: sums of arrows
OUT_X0 = 0.35                   # panel's left border; output content is clipped to x >= OUT_CLIP
OUT_CLIP = 0.45


def out_map(c, k, anchor):
    anchor = np.asarray(anchor, float)
    return lambda z: np.array([anchor[0] + k * (z.real - c.real), anchor[1] + k * (z.imag - c.imag), 0.0])


def arrow_mob(a, b, color, width=4.0, tip_max=0.22, clip=OUT_CLIP):
    a, b = np.asarray(a, float), np.asarray(b, float)
    tip = True
    if clip is not None:
        if a[0] < clip and b[0] < clip:
            return VGroup()
        if a[0] < clip:
            a = a + (clip - a[0]) / (b[0] - a[0]) * (b - a)
        if b[0] < clip:
            b = a + (clip - a[0]) / (b[0] - a[0]) * (b - a)
            tip = False
    L = np.linalg.norm(b - a)
    if L < 1e-3:
        return VGroup()
    u = (b - a) / L
    n = np.array([-u[1], u[0], 0.0])
    tl = min(tip_max, 0.42 * L) if tip else 0.0
    g = VGroup(Line(a, b - u * tl * 0.7, stroke_width=width, color=color))
    if tip and tl > 0.02:
        g.add(Polygon(b, b - u * tl + n * tl * 0.55, b - u * tl - n * tl * 0.55, stroke_width=0).set_fill(color, 1))
    return g


def chain_mob(sums, f, m=None, n_arrows=7, width=4.0):
    """Arrows for the first n_arrows terms (PALETTE colours cycling, as in S04's bar), a thin INK path for the rest.
    m (float) = how many terms are shown (fractional: the next term is partly drawn)."""
    m = len(sums) - 1 if m is None else m
    whole = int(np.floor(m))
    pts = [f(z) for z in sums[:whole + 1]]
    if whole < len(sums) - 1 and m > whole:
        pts.append(f(sums[whole] + (m - whole) * (sums[whole + 1] - sums[whole])))
    g = VGroup()
    for n in range(1, min(n_arrows, len(pts) - 1) + 1):
        g.add(arrow_mob(pts[n - 1], pts[n], PALETTE[(n - 1) % 7], width if n <= 3 else width * 0.8))
    if len(pts) - 1 > n_arrows:
        tail = VMobject().set_points_as_corners(np.array(pts[n_arrows:])).set_stroke(INK, 2.2).set_fill(opacity=0)
        g.add(tail)
    return g.set_z_index(6)


def out_axes(f, op=1.0):
    o, one = f(0j), f(1 + 0j)
    segs = [([OUT_CLIP, o[1], 0], [FW + 0.2, o[1], 0])]
    if o[0] >= OUT_CLIP:
        segs.append(([o[0], -FH - 0.2, 0], [o[0], FH + 0.2, 0]))
    g = VGroup(segs_mob(segs, DIM, 1.6, 0.55 * op))
    if OUT_CLIP < one[0] < FW - 0.3:
        g.add(segs_mob([([one[0], o[1] - 0.08, 0], [one[0], o[1] + 0.08, 0])], DIM, 2.5, op))
        g.add(N("1", 24, DIM).set_opacity(op).next_to([one[0], o[1], 0], UP, buff=0.14))
    return g.set_z_index(5.5)


# ---------------------------------------------------------------- side demo: a curve on a line, many continuations
SD_X, SD_W = -4.9, 3.3             # side-demo box: x -6.55..-3.25, stays left of the line 'real part 1' (x -3.2)


def side_demo():
    box = RoundedRectangle(corner_radius=0.12, width=SD_W, height=2.55).set_stroke(FAINT, 2).set_fill(BG, 1)
    box.move_to([SD_X, 1.75, 0])
    ax_y = 1.05
    axis = Line([SD_X - SD_W / 2 + 0.1, ax_y, 0], [SD_X + SD_W / 2 - 0.1, ax_y, 0], color=NEUTRAL, stroke_width=2.5)
    x0 = SD_X - SD_W / 2 + 0.15
    xj = x0 + np.pi / 1.6                     # join at the curve's inflection point

    def base(x):
        u = x - x0
        return ax_y + 0.85 + 0.35 * np.sin(1.6 * u) + 0.12 * u

    h = 1e-3
    yj, sj = base(xj), (base(xj + h) - base(xj - h)) / (2 * h)
    cj = (base(xj + h) - 2 * base(xj) + base(xj - h)) / h ** 2
    known = FunctionGraph(base, x_range=[x0, xj], color=INK, stroke_width=4)
    conts = VGroup()
    x_end = SD_X + SD_W / 2 - 0.12
    # every branch matches value, slope and curvature at the join (2nd-order Taylor); they differ from the cubic term on
    for c, col in ((0.5, PINK_P), (0.0, GREEN_P), (-0.36, PURPLE_P)):
        g = FunctionGraph(lambda x, c=c: yj + sj * (x - xj) + 0.5 * cj * (x - xj) ** 2 + c * (x - xj) ** 3,
                          x_range=[xj, x_end], color=col, stroke_width=4)
        assert min(g.get_all_points()[:, 1]) > ax_y + 0.1 and max(g.get_all_points()[:, 1]) < 2.9, c
        conts.add(DashedVMobject(g, num_dashes=10, dashed_ratio=0.6))
    cap = T("on a line: many ways", 24, DIM).move_to([SD_X, 0.72, 0])
    for m in (box, axis, known, conts, cap):
        m.set_z_index(8)
    return box, axis, known, conts, cap


def ping(pos, color=ACCENT, r0=0.1, r1=0.55, width=4):
    c = Circle(radius=r0).set_stroke(color, width).move_to(pos).set_z_index(9)
    base = c.copy()

    def f(m, a):
        m.become(base.copy().scale((r0 + (r1 - r0) * a) / r0).set_stroke(color, width * (1 - 0.5 * a), opacity=1 - a))
    return UpdateFromAlphaFunc(c, f, remover=True, rate_func=rate_functions.ease_out_cubic)


class S05_Plane(TimedScene):
    def construct(self):
        ph = config.pixel_height / config.frame_height          # pixels per scene unit
        S1 = complex(2, 3)
        S2 = complex(0.6, 3)
        Z1 = complex(zeta_np(np.array([S1]))[0])                # 0.798 - 0.114i
        L = Z1

        # ============================================================ P1: the plane
        cap_riemann = T("Riemann · 1859", 24, DIM).to_corner(UL, buff=0.45).set_z_index(9)
        self.until("p1", FadeIn(cap_riemann))

        # 'feed zeta ...': the number line (the old inputs) draws, with ticks -2..4
        axis_h = Line([-FW - 0.2, V1.y(0), 0], [FW + 0.2, V1.y(0), 0], color=NEUTRAL, stroke_width=3).set_z_index(1)
        ticks_h = tick_marks(V1, RES1, []).set_z_index(1)
        labs_h = tick_labels(V1, RES1, []).set_z_index(1)
        self.at(1.46, Create(axis_h), FadeIn(ticks_h), FadeIn(labs_h, lag_ratio=0.1), run_time=0.64)

        # {#plane}: the grid spreads up and down from the line; the vertical axis appears
        grid = segs_mob(grid_segs(V1, 1, 1, (-12, 12), (-36, 36)), FAINT, 1.6).set_z_index(0.4)
        axis_v = Line([V1.x(0), -FH - 0.2, 0], [V1.x(0), FH + 0.2, 0], color=NEUTRAL, stroke_width=3).set_z_index(1)
        ticks_v = tick_marks(V1, [], [1, 2, 3]).set_z_index(1)
        labs_v = tick_labels(V1, [], IMS1).set_z_index(1)
        spread = VGroup()
        self.add(spread)

        def grow_grid(m, a):
            swap(m, segs_mob(grid_segs(V1, 1, 1, (-12, 12), (-36, 36), squash=max(a, 0.002)), FAINT, 1.6,
                             min(1, 0.3 + a)).set_z_index(0.4))
        self.at("plane", UpdateFromAlphaFunc(spread, grow_grid), GrowFromCenter(axis_v), run_time=1.1)
        self.remove(spread)
        self.add(grid)
        self.play(FadeIn(ticks_v), FadeIn(labs_v), run_time=0.3)
        # '... not numbers on a line': the old line glows once
        self.at(3.62, axis_h.animate(rate_func=there_and_back).set_stroke(ACCENT, 6), run_time=0.9)

        # {#right}: the input dot, 2 across
        dot = pt(V1.p(0, 0), ACCENT, r=0.11).set_z_index(7)
        arr_h = arrow_mob(V1.p(0, 0) + UP * 0.3, V1.p(2, 0) + UP * 0.3, DIM, 3, 0.18, clip=None).set_z_index(6)
        lab_h = T("2 across", 24, DIM).next_to(arr_h, UP, buff=0.1).set_z_index(6)
        self.add(dot)
        self.at("right", dot.animate.move_to(V1.p(2, 0)), GrowFromPoint(arr_h, V1.p(0, 0) + UP * 0.3),
                FadeIn(lab_h, shift=UP * 0.1), run_time=0.9)

        # {#up}: 3 up -> 2 + 3i; the note on complex numbers settles while the move ends
        arr_v = arrow_mob(V1.p(2, 0) + RIGHT * 0.3, V1.p(2, 3) + RIGHT * 0.3, DIM, 3, 0.18, clip=None).set_z_index(6)
        lab_v = T("3 up", 24, DIM).next_to(arr_v, RIGHT, buff=0.12).set_z_index(6)
        s_lab = N("2 + 3i", 30, INK).next_to(V1.p(2, 3), UR, buff=0.12).set_z_index(7)
        s_lab.set_stroke(BG, 5, background=True)
        note_a = T("points like 2 + 3i: ", 24, INK)
        note_c = T("complex numbers", 24, ACCENT)
        note1 = VGroup(note_a, note_c).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        note2 = T("i marks the up-part", 24, DIM)
        notes = VGroup(note1, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DL, buff=0.45)
        notes_bg = bg_rect(notes, 0.14)
        VGroup(notes_bg, notes).set_z_index(8)
        up_rt = self.t("p1_end") - self.t("up")                       # 6.44 -> 7.24
        nwin = dict(rate_func=squish_rate_func(smooth, 0.35, 1.0))     # notes: ~6.72 -> 7.24
        self.at("up", dot.animate(rate_func=squish_rate_func(smooth, 0, 0.8)).move_to(V1.p(2, 3)),
                GrowFromPoint(arr_v, V1.p(2, 0) + RIGHT * 0.3, rate_func=squish_rate_func(smooth, 0, 0.8)),
                FadeIn(lab_v, shift=RIGHT * 0.1, rate_func=squish_rate_func(smooth, 0, 0.8)),
                FadeIn(s_lab, shift=UR * 0.1, rate_func=squish_rate_func(smooth, 0.4, 0.9)),
                FadeIn(notes_bg, **nwin), FadeIn(notes, shift=UP * 0.1, **nwin), run_time=up_rt)

        # ============================================================ P2: spinning terms, spirals
        panel = Rectangle(width=FW + 0.3 - OUT_X0, height=2 * FH + 0.4, stroke_width=0).set_fill(BG, 1)
        panel.move_to([(OUT_X0 + FW + 0.3) / 2, 0, 0]).set_z_index(5)
        border = Line([OUT_X0, -FH - 0.2, 0], [OUT_X0, FH + 0.2, 0], color=FAINT, stroke_width=2.5).set_z_index(5.2)
        header = VGroup(T("the sum", 24, DIM), N("1 + 1/2ˢ + 1/3ˢ + …", 26, INK)).arrange(RIGHT, buff=0.22)
        header.next_to([OUT_X0 + 0.3, FH - 0.45, 0], RIGHT, buff=0).set_z_index(7)
        # live readout: which input the panel shows (ACCENT = the input dot's colour)
        in_word = T("input", 24, DIM)
        in_word.next_to(header, DOWN, buff=0.2).align_to(header, LEFT).set_z_index(7)

        def in_val(txt):
            return N(txt, 24, ACCENT).next_to(in_word, RIGHT, buff=0.18).align_to(in_word, DOWN).set_z_index(7)
        readout = VGroup(in_val("2"))

        f0 = out_map(L, 3.4, np.array([0.95, 0.4, 0]) + 3.4 * np.array([L.real, L.imag, 0]))   # origin at (0.95, 0.4)
        f_zoom = (L, 12.0, np.array([3.75, 0.3, 0]))
        oax = out_axes(f0)
        sums2 = spiral_partial_sums(2.0, 200)
        chain = chain_mob(sums2, f0)
        ghost = Circle(radius=0.13).set_stroke(ACCENT, 2.5).move_to(V1.p(2, 3)).set_z_index(6.5)

        # pause after P1: the dot leaves a ring at 2 + 3i (the target) and reappears at 2 (never visibly moves down);
        # the output panel opens with the terms for s = 2 laid tip to tail (S04's bar)
        dot2 = pt(V1.p(2, 0), ACCENT, r=0.11).set_z_index(7)
        q = lambda a, b: dict(rate_func=squish_rate_func(smooth, a, b))   # noqa: E731
        self.at("p1_end", FadeOut(arr_h, **q(0, 0.45)), FadeOut(lab_h, **q(0, 0.45)), FadeOut(arr_v, **q(0, 0.45)),
                FadeOut(lab_v, **q(0, 0.45)), FadeOut(dot, **q(0, 0.4)), FadeIn(ghost, **q(0, 0.4)),
                FadeIn(dot2, scale=1.6, **q(0.3, 0.7)),
                FadeIn(panel, **q(0.3, 0.8)), FadeIn(border, **q(0.3, 0.8)), FadeIn(header, **q(0.3, 0.8)),
                FadeIn(in_word, **q(0.3, 0.8)), FadeIn(readout, **q(0.3, 0.8)), FadeIn(oax, **q(0.3, 0.8)),
                LaggedStart(*[Create(a) for a in chain], lag_ratio=0.12, rate_func=squish_rate_func(linear, 0.45, 1)),
                run_time=self.left("p2"))
        dot = dot2
        self.remove(chain)
        chain = VGroup(chain)
        self.add(chain)

        # 'Moving up makes {#spin} each term spin': the input climbs from 2 to 2 + 3i with the words;
        # every term turns by -t ln n (exact), live. Small t barely turns the terms, so the visible spin lands on 'spin'.
        def spin(m, a):
            swap(m, chain_mob(spiral_partial_sums(complex(2, 3.0 * a), 200), f0))

        def read_up(m, a):
            t = 3.0 * a
            swap(m, in_val("2" if t < 0.05 else ("2 + 3i" if a > 0.985 else f"2 + {t:.1f}i")))
        self.at("p2", UpdateFromAlphaFunc(chain, spin, rate_func=smooth),
                UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(V1.p(2, 3.0 * a)), rate_func=smooth),
                UpdateFromAlphaFunc(readout, read_up, rate_func=smooth), run_time=2.9)
        self.remove(ghost)
        sums = spiral_partial_sums(S1, 200)

        # {#spiral}: zoom into the curl (output content only; the input plane stays put)
        def zoom(m, a):
            k = 3.4 * (f_zoom[1] / 3.4) ** a
            anc = (1 - a) * (np.array([0.95, 0.4, 0]) + 3.4 * np.array([L.real, L.imag, 0])) + a * f_zoom[2]
            f = out_map(L, k, anc)
            swap(m, VGroup(out_axes(f), chain_mob(sums, f)))
        zgroup = VGroup(VGroup(oax.copy(), chain.copy()))
        self.remove(oax, chain)
        self.add(zgroup)
        self.at("spiral", UpdateFromAlphaFunc(zgroup, zoom, rate_func=smooth), run_time=1.2)
        fz = out_map(*f_zoom)

        # pause after the sentence: the P1 notes step back into a small 'complex numbers' tag at the top left
        tag = T("complex numbers", 24, DIM).to_corner(UL, buff=0.45).set_z_index(9)
        tag_bg = bg_rect(tag, 0.1).set_z_index(8.9)
        self.at("p2s1_end", FadeOut(cap_riemann, **q(0, 0.5)), FadeOut(notes_bg), FadeOut(notes),
                FadeIn(tag_bg, **q(0.4, 1)), FadeIn(tag, **q(0.4, 1)), run_time=0.5)

        # 'Far enough right': the line real part 1
        uline = unit_line(V1).set_z_index(1.2)
        u_lab = T("real part 1", 24, INK).next_to([V1.x(1), FH - 0.45, 0], RIGHT, buff=0.15).set_z_index(9)
        u_lab_bg = bg_rect(u_lab, 0.08, 0.85).set_z_index(8.9)
        self.at("p2s2", Create(uline), FadeIn(u_lab_bg), FadeIn(u_lab), run_time=0.8)

        # {#settle}: the right of 1 tints; a runner walks the spiral (log pace) and comes to rest: zeta(2 + 3i)
        tint = Rectangle(width=FW + 0.3 - V1.x(1), height=2 * FH + 0.4, stroke_width=0).set_fill(TEAL_P, 0.13)
        tint.move_to([(V1.x(1) + FW + 0.3) / 2, 0, 0]).set_z_index(0.1)
        pts = np.array([fz(z) for z in sums[1:]])
        runner = Dot(pts[0], radius=0.07, color=INK).set_z_index(7)

        def run(m, a):
            u = np.exp(a * np.log(len(pts))) - 1
            i = int(min(len(pts) - 2, np.floor(u)))
            m.move_to(pts[i] + (u - i) * (pts[i + 1] - pts[i]))
        self.add(runner)
        self.at("settle", FadeIn(tint), UpdateFromAlphaFunc(runner, run, rate_func=linear), run_time=1.2)
        val = pt(fz(Z1), ACCENT, r=0.1).set_z_index(8)
        self.play(FadeOut(runner), GrowFromCenter(val), ping(fz(Z1)), run_time=0.6)
        vtxt = f"ζ(2 + 3i) ≈ {Z1.real:.2f} − {abs(Z1.imag):.2f}i"
        assert vtxt == "ζ(2 + 3i) ≈ 0.80 − 0.11i", vtxt
        v_lab = N(vtxt, 28, INK).move_to([3.75, -2.55, 0]).set_z_index(8)
        self.at(16.05, FadeIn(v_lab, shift=UP * 0.1), run_time=0.6)

        # 'Left of one': the input slides to 0.6 + 3i; the old spiral clears; the output frame widens
        s_lab2 = card(N("0.6 + 3i", 30, INK), 0.08).next_to(V1.p(0.6, 3), UP, buff=0.3).set_z_index(7)
        s_lab2.set_x(V1.x(0.6))
        big = spiral_partial_sums(S2, 2000)
        lo, hi = np.array([big.real.min(), big.imag.min()]), np.array([big.real.max(), big.imag.max()])
        cw = complex(*(lo + hi) / 2)
        kw = min(5.9 / (hi[0] - lo[0]), 5.6 / (hi[1] - lo[1]))
        fw = out_map(cw, kw, [3.75, -0.3, 0])               # top stays below the 'input' readout
        oax_w = out_axes(fw)

        def read_left(m, a):
            swap(m, in_val("0.6 + 3i" if a > 0.985 else f"{2 - 1.4 * a:.1f} + 3i"))
        self.at("p2s3", dot.animate.move_to(V1.p(0.6, 3)), FadeOut(zgroup), FadeOut(val), FadeOut(v_lab),
                FadeOut(s_lab, **q(0, 0.5)), FadeIn(s_lab2, **q(0.5, 1)), FadeIn(oax_w),
                UpdateFromAlphaFunc(readout, read_left, rate_func=smooth), run_time=0.85)

        # {#wander}: 2,000 exact terms, drawn at a log pace; the loops keep growing
        grow = VGroup()
        tipdot = Dot(fw(0j), radius=0.06, color=INK).set_z_index(7)
        counter = VGroup().set_z_index(8)
        self.add(grow, tipdot, counter)

        def u_of(a):
            return np.exp(a * np.log(2001)) - 1

        def wander(m, a):
            swap(m, chain_mob(big, fw, m=max(u_of(a), 1e-3), width=3.5))

        def tip_at(m, a):
            u = u_of(a)
            whole = int(np.floor(u))
            m.move_to(fw(big[whole] + (u - whole) * (big[min(whole + 1, 2000)] - big[whole])))

        def count(m, a):
            n = max(1, int(round(u_of(a))))
            swap(m, VGroup(T("terms:", 24, DIM), N(f"{n:,}", 26, INK)).arrange(RIGHT, buff=0.14)
                 .move_to([5.4, -3.45, 0]).set_z_index(8))
        rf = rate_functions.ease_in_out_sine
        never = T("never settles", 24, DIM).move_to([1.85, -3.45, 0]).set_z_index(8)
        # 'the sum stops working' (20.63): hatching left of 1, inside the same 2.5 s move
        hat = hatch(-FW - 0.2, V1.x(1)).set_z_index(0.3)
        fails = card(T("sum fails here", 24, INK)).move_to([-5.25, -2.9, 0]).set_z_index(8)
        W0, WR = self.t("wander"), 2.5

        def win(t0, t1):
            return dict(rate_func=squish_rate_func(smooth, (t0 - W0) / WR, (t1 - W0) / WR))
        self.at("wander", UpdateFromAlphaFunc(grow, wander, rate_func=rf), UpdateFromAlphaFunc(tipdot, tip_at, rate_func=rf),
                UpdateFromAlphaFunc(counter, count, rate_func=rf), FadeIn(never, **win(19.7, 20.2)),
                Create(hat, **win(20.6, 21.5)), FadeIn(fails, **win(20.8, 21.5)), run_time=WR)

        # ============================================================ P3: smoothness is rigid
        out_all = VGroup(panel, border, header, in_word, readout, oax_w, grow, tipdot, counter, never)
        self.at("p3", FadeOut(out_all), FadeOut(dot), FadeOut(s_lab2), run_time=0.7)

        box, sd_axis, known, conts, sd_cap = side_demo()
        self.at("strict", FadeIn(box), Create(sd_axis), FadeIn(sd_cap), run_time=0.45)
        self.play(Create(known), run_time=0.45)
        for c in conts:
            self.play(Create(c), run_time=0.9)

        # 'But with complex inputs': the tag lights up
        self.at(27.18, tag.animate(rate_func=there_and_back).set_color(ACCENT).scale(1.12), run_time=0.9)

        # {#patch}: a 1 x 1 patch next to the pole shows zeta's real colouring (hue spans ~130 deg there:
        # magenta, pink, yellow); a legend explains the colour
        pxu = ph * V1.sx
        PX, PY = 1.6, 0.0                                         # the patch: real part 1.1..2.1, height -0.5..0.5
        A = Field("A", 1.0, 10.45, -2.25, 5.15, int(9.45 * pxu), int(7.4 * pxu))

        def sq(RE, IM):
            return ((np.abs(RE - PX) <= 0.5) & (np.abs(IM - PY) <= 0.5) & (RE >= 1.05)).astype(float)
        fA = A.draw(V1, sq, opacity=0.0)
        self.add(fA)
        outline = Square(side_length=V1.sx).move_to(V1.p(PX, PY)).set_stroke(INK, 2.5).set_z_index(1.5)
        wr = 0.26
        wheel = color_wheel(wr).move_to([1.2, FH - 0.66, 0]).set_z_index(9)
        # an output that points (almost) right, like zeta(2 + 3i) = 0.80 - 0.11i, gets the colour it points into
        ang = np.angle(Z1)
        w_arrow = arrow_mob(wheel.get_center(), wheel.get_center() + 0.9 * wr * np.array([np.cos(ang), np.sin(ang), 0]),
                            ACCENT, 3.5, 0.11, clip=None)
        w_arrow[0].set_stroke(BG, 6.5, background=True)
        w_arrow.set_z_index(9.5)
        leg = T("colour = direction of ζ's output", 24, DIM).next_to(wheel, RIGHT, buff=0.18).set_z_index(9)
        leg_bg = bg_rect(Group(wheel, leg), 0.12).set_z_index(8.9)
        patch_rt = 1.4                                            # 29.56 -> 30.96: the reveal ends on the word 'patch'
        self.at("patch", UpdateFromAlphaFunc(fA, lambda m, a: A.draw(V1, sq, opacity=a)), Create(outline),
                run_time=patch_rt)
        self.until(self.t("locked") - 0.05, FadeIn(leg_bg), FadeIn(wheel), FadeIn(leg), GrowFromCenter(w_arrow))

        # {#locked}: the colouring spreads like ink over everything right of 1 (real values everywhere)
        rmax = np.hypot(10.45 - PX, 5.15 - PY) + 0.5

        def ink(r):
            def mask(RE, IM):
                d = np.hypot(RE - PX, IM - PY)
                th = np.arctan2(IM - PY, RE - PX)
                rr = r * (1 + 0.05 * np.sin(3 * th + 1) + 0.03 * np.sin(7 * th + 2))
                disc = np.clip((rr - d) / 0.35 + 0.5, 0, 1)
                return np.maximum(disc, sq(RE, IM)) * (RE >= 1)
            return mask
        cap2 = VGroup(T("complex inputs:", 24, INK), T("only one way", 24, INK)).arrange(DOWN, buff=0.1)
        cap2.move_to([SD_X, 1.0, 0]).set_z_index(9)
        self.at("locked", UpdateFromAlphaFunc(fA, lambda m, a: A.draw(V1, ink(0.5 + a * rmax)),
                                              rate_func=rate_functions.ease_in_quad),
                FadeOut(conts), FadeOut(known), FadeOut(sd_axis), FadeOut(sd_cap, **q(0, 0.35)), FadeIn(cap2, **q(0.35, 0.7)),
                outline.animate.set_stroke(opacity=0.5), run_time=1.4)
        full_right = lambda RE, IM: (RE >= 1).astype(float)   # noqa: E731
        A.draw(V1, full_right)
        self.play(Transform(box, bg_rect(cap2, 0.14, 0.95).set_stroke(FAINT, 2).set_z_index(8)), run_time=0.6)

        # ============================================================ P4: the one extension, the pole
        # {#one_way}: the hatching lifts away
        self.at("one_way", hat.animate.shift(UP * 0.5).set_stroke(opacity=0), FadeOut(fails, shift=UP * 0.3),
                run_time=0.8)

        # the plane widens to -10..3 x -30..30 (content rescales, no camera move); the colour right of 1 comes along
        bw = int(21.1 * ph * V2.sx)
        bh = int(67.0 * ph * V2.sy * 2.2)
        B = Field("B", -10.6, 10.5, -33.5, 33.5, bw, bh)
        fB = B.draw(V1, full_right, opacity=0.0)
        fB.set_z_index(0.15)
        self.add(fB)
        for m in (axis_h, axis_v, ticks_h, ticks_v, labs_h, labs_v, grid, tint):
            self.remove(m)
        pl = VGroup(plane_state(V1))
        uline2 = VGroup(uline.copy())
        self.remove(uline)
        self.add(pl, uline2)

        # the line keeps its name: a bottom label rides along with the line (the top one would meet the legend)
        u_lab_b = card(T("real part 1", 24, INK), 0.08).set_z_index(9)

        def place_ub(m, v):
            m.next_to([v.x(1), -FH + 0.42, 0], RIGHT, buff=0.12)
        place_ub(u_lab_b, V1)
        u_lab_b.set_opacity(0)

        def widen(m, a):
            v = lerp_view(V1, V2, a)
            e = smooth(a)
            swap(m, plane_state(v, g1=1 - e, g2=e, l1=max(0, 1 - 3 * a), l2=max(0, 3 * a - 2)))
            swap(uline2, unit_line(v).set_z_index(1.2))
            A.draw(v, full_right)
            B.draw(v, full_right)

        def ride(m, a):
            place_ub(m, lerp_view(V1, V2, a))
            op = float(np.clip((a - 0.25) / 0.3, 0, 1))
            m[0].set_fill(BG, 0.9 * op)
            m[1].set_opacity(op)
        self.at(34.95, UpdateFromAlphaFunc(pl, widen), UpdateFromAlphaFunc(fA, lambda m, a: None),
                UpdateFromAlphaFunc(fB, lambda m, a: None), UpdateFromAlphaFunc(uline2, lambda m, a: None),
                UpdateFromAlphaFunc(u_lab_b, ride),
                FadeOut(outline), FadeOut(u_lab, **q(0, 0.3)), FadeOut(u_lab_bg, **q(0, 0.3)),
                FadeOut(box), FadeOut(cap2), FadeOut(tag), FadeOut(tag_bg), run_time=self.left("whole") - 0.05)
        self.remove(fA)

        # {#whole}: the colouring flows across the line at 1 and fills the whole plane
        def flow(m, a):
            e = 1 - a * 12.2

            def mask(RE, IM):
                return np.where(RE >= 1, 1.0, np.clip((RE - e) / 0.5, 0, 1))
            B.draw(V2, mask)
        self.at("whole", UpdateFromAlphaFunc(fB, flow, rate_func=rate_functions.ease_in_out_sine), run_time=1.6)
        B.draw(V2, lambda RE, IM: np.ones_like(RE * IM))

        # 'and Riemann found it'
        cap_r2 = card(T("Riemann · 1859", 24, INK)).to_corner(UL, buff=0.35).set_z_index(9)
        self.at(38.68, FadeIn(cap_r2), run_time=0.6)

        # {#pole}: the one point where it blows up
        pole = Circle(radius=0.16).set_stroke(INK, 3.5).move_to(V2.p(1, 0)).set_z_index(9)
        pole_bg = Circle(radius=0.16).set_stroke(BG, 7.5).move_to(V2.p(1, 0)).set_z_index(8.9)
        pole_lab = card(T("blows up at 1", 24, INK)).move_to(V2.p(1, 0) + np.array([0.25, 0.72, 0])).set_z_index(9)
        echo = card(N("1 + 1/2 + 1/3 + … grows forever", 24, DIM)).set_z_index(9)
        echo.move_to([0.6, -1.8, 0])          # clear band between the -10i and -20i rows, left of the vertical axis
        self.at("pole", Create(pole_bg), Create(pole), FadeIn(pole_lab, shift=UP * 0.1), ping(V2.p(1, 0), INK),
                FadeOut(u_lab_b), run_time=0.7)
        self.at(41.66, FadeIn(echo, shift=RIGHT * 0.1), run_time=0.6)

        # end: everything fades to the empty background
        rest = [m for m in self.mobjects if m is not fB]

        def fade_field(m, a):
            B.draw(V2, lambda RE, IM: np.ones_like(RE * IM), opacity=1 - a)
        self.at("p4_end", *[FadeOut(m) for m in rest], UpdateFromAlphaFunc(fB, fade_field), run_time=0.8)
        self.remove(fB)

