"""S07_Hexagons: "how many colors are always enough?" -> a pattern for the whole plane.

Squares (side 2/3) manage it with nine colors; Isbell's hexagon flower (side 0.45, geom.HEX_SIDE) with seven.
Scale: SC = 1.6 manim units per problem unit (the storyboard's UNIT = 1.6). Every ruler, stick and ring is drawn
at that scale, so the pictured lengths are the true ones (0.94 < 1 < 1.33, 0.90 < 1 < 1.19).
Hexagon orientation, centres and colours come from geom (flat-top axial grid, colour (q + 3r) mod 7).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

SC = 1.6                              # manim units per problem unit in this scene
BAND_TOP = -2.05                      # the pattern lives above this line; the scoreboard lives below it
C0 = np.array([0.0, 0.95, 0.0])       # centre of the pattern area = centre of hexagon (0, 0)
FILL = 0.88                           # paint opacity of tiles
DIMMED = 0.28                         # paint opacity of dimmed (non-blue) hexagons
NINE = PALETTE + ["#9AA33B", "#A0673F"]   # 7 paints + olive + brown (square pattern only)
SQ = 2 / 3                            # square side (problem units)
SQM = SQ * SC                         # square side (manim)
S1 = np.array([-1.6, C0[1], 0.0])     # first blue square; its twin sits 2 units to the right
HS = HEX_SIDE * SC                    # hexagon side (manim)


def P(u, center=C0):
    """problem coords (2D) -> scene point around `center`."""
    return to_scene(u, SC, center)


def lab(s, size=30, color=INK, num=True):
    t = (N if num else T)(s, size, color)
    t.set_stroke(BG, width=7, background=True)
    return t


def panel(mob, pad=0.2, op=0.92):
    r = RoundedRectangle(corner_radius=0.14, width=mob.width + 2 * pad, height=mob.height + 2 * pad,
                         stroke_color=FAINT, stroke_width=1.5).set_fill(BG, op).move_to(mob)
    return VGroup(r, mob)


def measure(a, b, color=INK, width=3, tick=0.1, dashed=True):
    """Dimension line a->b with end ticks (dashed = a measured distance, solid = a unit stick)."""
    a, b = np.array(a, float), np.array(b, float)
    u = (b - a) / np.linalg.norm(b - a)
    n = np.array([-u[1], u[0], 0.0])
    if dashed:
        line = DashedLine(a, b, color=color, stroke_width=width, dash_length=0.07, dashed_ratio=0.55)
    else:
        line = Line(a, b, color=color, stroke_width=width)
    ticks = VGroup(Line(a - n * tick, a + n * tick, color=color, stroke_width=width),
                   Line(b - n * tick, b + n * tick, color=color, stroke_width=width))
    g = VGroup(line, ticks)
    g.set_stroke(BG, width=width + 4, background=True)
    return g


def unit_ruler(a, direction):
    d = np.array(direction, float)
    d = d / np.linalg.norm(d)
    return measure(a, np.array(a, float) + SC * d, color=UNIT_COLOR, width=5, tick=0.11, dashed=False)


def hex_at(x, y):
    """Axial (q, r) of the geom hexagon containing problem point (x, y)."""
    s = HEX_SIDE
    q = x / (1.5 * s)
    r = y / (SQ3 * s) - q / 2
    cx, cz = q, r
    cy = -cx - cz
    rx, ry, rz = round(cx), round(cy), round(cz)
    dx, dy, dz = abs(rx - cx), abs(ry - cy), abs(rz - cz)
    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return int(rx), int(rz)


def ring_runs(c, n=720):
    """Constant-colour runs of the unit circle about problem point c: [(a0, a1, colour index)]."""
    angs = np.linspace(0, TAU, n, endpoint=False)
    cols = [hex_color(*hex_at(c[0] + np.cos(a), c[1] + np.sin(a))) for a in angs]
    runs_ = []
    start = 0
    for i in range(1, n + 1):
        if i == n or cols[i] != cols[start]:
            runs_.append([angs[start], angs[i] if i < n else TAU, cols[start]])
            start = i
    if len(runs_) > 1 and runs_[0][2] == runs_[-1][2]:        # merge the wrap-around run
        last = runs_.pop()
        runs_[0][0] = last[0] - TAU
    return runs_


def ring_arcs(c, colored=True, width=6, opacity=1.0):
    g = VGroup()
    for a0, a1, col in ring_runs(c):
        arc = Arc(radius=SC, start_angle=a0, angle=a1 - a0, arc_center=P(c),
                  color=PALETTE[col] if colored else UNIT_COLOR, stroke_width=width, stroke_opacity=opacity)
        arc.set_stroke(BG, width=width + 5, opacity=opacity, background=True)
        arc.col = col
        g.add(arc)
    return g.set_z_index(3)


def clip_halfplane(poly, a, b):
    """Keep the part of convex polygon `poly` with a.x <= b."""
    out = []
    for i in range(len(poly)):
        p1, p2 = poly[i], poly[(i + 1) % len(poly)]
        d1, d2 = a @ p1 - b, a @ p2 - b
        if d1 <= 0:
            out.append(p1)
        if d1 * d2 < 0:
            out.append(p1 + d1 / (d1 - d2) * (p2 - p1))
    return out


def mosaic(seed=4):
    """A soft, irregular painted mosaic (Voronoi cells) filling the frame above the bar."""
    rng = np.random.default_rng(seed)
    sites = []
    for x in np.arange(-7.8, 8.0, 1.3):
        for y in np.arange(BAND_TOP - 0.4, 4.6, 1.2):
            sites.append(np.array([x + rng.uniform(-0.5, 0.5), y + rng.uniform(-0.45, 0.45)]))
    rect = [np.array(p, float) for p in [(-7.3, BAND_TOP - 0.3), (7.3, BAND_TOP - 0.3), (7.3, 4.2), (-7.3, 4.2)]]
    polys, nbrs = [], []
    for i, p in enumerate(sites):
        poly, nb = rect, set()
        for j, q in enumerate(sites):
            if i == j or np.linalg.norm(p - q) > 4:
                continue
            a, b = 2 * (q - p), q @ q - p @ p
            poly = clip_halfplane(poly, a, b)
            if not poly:
                break
        for j, q in enumerate(sites):
            if i != j and poly and sum(abs(2 * (q - p) @ v - (q @ q - p @ p)) < 1e-6 for v in poly) >= 2:
                nb.add(j)
        polys.append(poly)
        nbrs.append(nb)
    cols = [None] * len(sites)
    for i in rng.permutation(len(sites)):
        free = [k for k in range(7) if k not in {cols[j] for j in nbrs[i]}]
        cols[i] = int(rng.choice(free)) if free else int(rng.integers(7))
    cells = VGroup()
    for poly, col, p in zip(polys, cols, sites):
        if len(poly) < 3:
            continue
        c = Polygon(*[np.array([v[0], v[1], 0.0]) for v in poly])
        c.set_fill(PALETTE[col], 0.5).set_stroke(BG, 4)
        c.site_x = p[0]
        cells.add(c)
    return cells


def spindle_mob(scale=0.8, center=np.array([-4.9, 0.55, 0.0])):
    Pd, E = moser_spindle()
    arr = np.array(list(Pd.values()))
    mid = (arr.min(0) + arr.max(0)) / 2
    pts = {k: to_scene(v - mid, scale, center) for k, v in Pd.items()}
    sticks = VGroup(*[stick(pts[a], pts[b], width=3) for a, b in E])
    dots = VGroup(*[ring(p, r=0.075) for p in pts.values()])
    return VGroup(sticks, dots)


# axial neighbour k sits across edge k (vertex k -> vertex k+1) of a flat-top geom hexagon
NBR = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def flower_of(q, r):
    """Axial coords of the blue centre of the Isbell flower that contains hexagon (q, r).
    The six neighbours of any hexagon carry the six other colours, so exactly one of them is blue."""
    if hex_color(q, r) == 0:
        return (q, r)
    blues = [(q + dq, r + dr) for dq, dr in NBR if hex_color(q + dq, r + dr) == 0]
    assert len(blues) == 1, (q, r, blues)
    return blues[0]


def flower_outline(bq, br, **style):
    """Closed 18-gon around the flower (blue centre (bq, br) + its six petals)."""
    members = {(bq, br)} | {(bq + dq, br + dr) for dq, dr in NBR}
    nxt = {}
    for q, r in members:
        vs = hex_vertices(hex_center(q, r))
        for k, (dq, dr) in enumerate(NBR):
            if (q + dq, r + dr) not in members:
                a, b = vs[k], vs[(k + 1) % 6]
                nxt[tuple(np.round(a, 6))] = (a, tuple(np.round(b, 6)))
    start = next(iter(nxt))
    pts, key = [], start
    for _ in range(len(nxt)):
        a, key = nxt[key]
        pts.append(P(a))
        if key == start:
            break
    assert len(pts) == 18, len(pts)
    return Polygon(*pts, **style)




class S07_Hexagons(TimedScene):
    # ------------------------------------------------------------------ timing helper
    def span(self, end, *items):
        """One play() from now until `end`; items = (anim, t0, t1) run inside [t0, t1] (absolute seconds).

        Each anim is wrapped in an AnimationGroup whose own rate_func maps scene time into [t0, t1]. The inner
        animation keeps its easing and lag. (Squishing the inner rate_func instead breaks lagged animations such
        as Create on dashed lines: manim applies rate_func per submobject after the lag, which smears the drawing
        over the whole span.)"""
        t_now, t_end = self.now, self.t(end)
        total = max(t_end - t_now, 1e-3)
        anims = []
        for anim, a, b in items:
            if hasattr(anim, "build"):
                anim = anim.build()
            a = min(max(self.t(a), t_now), t_end)
            b = min(max(self.t(b), a + 1e-3), t_end)
            anims.append(AnimationGroup(anim, rate_func=squish_rate_func(linear, (a - t_now) / total,
                                                                         (b - t_now) / total)))
        self.until(end, *anims)

    def construct(self):
        t = self.t
        band = Rectangle(width=16, height=BAND_TOP + 4.6, stroke_width=0).set_fill(BG, 1)
        band.move_to([0, (BAND_TOP - 4.6) / 2, 0]).set_z_index(5)
        self.add(band)
        bar = BoundsBar(lo=4).to_edge(DOWN).set_z_index(6)

        # ============================================================ P1: flip it around -> a pattern
        spin = spindle_mob()
        trap = T("trap", 28, DIM).next_to(spin, UP, buff=0.3)
        self.until("p1", FadeIn(bar))
        self.span(t("p1") + 0.9, (FadeIn(spin, scale=0.92), t("p1"), t("p1") + 0.9),
                  (FadeIn(trap, shift=DOWN * 0.1), t("p1") + 0.3, t("p1") + 0.9))

        arrow = Arrow(bar.box.get_right() + RIGHT * 1.05, bar.box.get_right() + RIGHT * 0.12, buff=0,
                      color=ACCENT, stroke_width=6, max_tip_length_to_length_ratio=0.35).set_z_index(7)
        qm = N("?", 40, ACCENT).next_to(arrow, UP, buff=0.12).set_z_index(7)
        ell = bar.cells[8]
        self.at("enough", GrowArrow(arrow), Indicate(ell, color=ACCENT, scale_factor=1.6), run_time=0.7)
        self.play(arrow.animate(rate_func=there_and_back).shift(LEFT * 0.22), FadeIn(qm, shift=DOWN * 0.1),
                  run_time=0.6)
        self.play(arrow.animate(rate_func=there_and_back).shift(LEFT * 0.22), run_time=0.6)

        mos = mosaic()
        order = sorted(mos, key=lambda c: -c.site_x)
        mos_lab = panel(T("pattern: the whole plane", 30, DIM)).move_to([0, 3.15, 0]).set_z_index(4)
        self.span("p1_end",
                  (FadeOut(VGroup(spin, trap)), "pattern", t("pattern") + 0.5),
                  (LaggedStart(*[FadeIn(c) for c in order], lag_ratio=0.04), "pattern", t("pattern") + 1.25),
                  (FadeIn(mos_lab, shift=DOWN * 0.1), t("pattern") + 0.25, t("pattern") + 0.75))
        self.until("p2", FadeOut(mos), FadeOut(mos_lab), FadeOut(arrow), FadeOut(qm))

        # ============================================================ P2: squares, nine colors
        tiles = {}
        for i in range(-7, 11):
            for j in range(-6, 6):
                c = S1 + np.array([i * SQM, j * SQM, 0])
                if abs(c[0]) > 7.11 + SQM / 2 or c[1] > 4 + SQM / 2 or c[1] < BAND_TOP - SQM / 2:
                    continue
                sq = Square(side_length=SQM).move_to(c)
                sq.set_fill(NINE[(i % 3) + 3 * (j % 3)], FILL).set_stroke(BG, 3)
                tiles[(i, j)] = sq
        sq1, sq2 = tiles[(0, 0)], tiles[(3, 0)]
        self.span(t("p2") + 0.8, (GrowFromCenter(sq1), "p2", t("p2") + 0.8))

        # "too small to hold a stick": a unit stick pivoting on a corner always pokes out
        bl, tr = sq1.get_corner(DL), sq1.get_corner(UR)
        ang = ValueTracker(0.0)
        tip = lambda: bl + SC * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])  # noqa: E731
        stk = always_redraw(lambda: VGroup(stick(bl, tip(), width=5), pt(tip(), UNIT_COLOR, r=0.07),
                                           pt(bl, UNIT_COLOR, r=0.07)).set_z_index(3))
        trail = always_redraw(lambda: Arc(radius=SC, start_angle=0, angle=max(ang.get_value(), 1e-3), arc_center=bl,
                                          color=UNIT_COLOR, stroke_width=2.5, stroke_opacity=0.55).set_z_index(2))
        self.at("small", FadeIn(stk), run_time=0.3)
        self.add(trail)
        self.play(ang.animate.set_value(PI / 2), run_time=0.9, rate_func=smooth)
        self.play(ang.animate.set_value(PI / 4), run_time=0.4, rate_func=smooth)
        stk.clear_updaters()
        trail.clear_updaters()
        # the stick slides off the diagonal and lies beside it: diagonal 0.94 < stick 1
        dgv = np.array([1, 1, 0]) / np.sqrt(2)
        nrm = np.array([-1, 1, 0]) / np.sqrt(2)
        off = -nrm * 0.95
        stk_to = VGroup(stick(bl + off, bl + off + SC * dgv, width=5), pt(bl + off + SC * dgv, UNIT_COLOR, r=0.07),
                        pt(bl + off, UNIT_COLOR, r=0.07)).set_z_index(3)
        diag = measure(bl, tr, color=INK, width=3, tick=0.09).set_z_index(2)
        diag_l = lab("0.94", 30).rotate(PI / 4).move_to(sq1.get_center() + nrm * 0.3).set_z_index(3)
        one_l = lab("1", 30, UNIT_COLOR).move_to(bl + off + SC * dgv * 0.5 - nrm * 0.32)
        guides = VGroup(*[DashedLine(p, p + off * 1.0, color=DIM, stroke_width=2, dash_length=0.05)
                          for p in (bl, tr)]).set_z_index(1)
        t0 = self.now
        self.span("p2s2", (FadeOut(trail), t0, t0 + 0.3), (Transform(stk, stk_to), t0, t0 + 0.55),
                  (Create(diag), t0 + 0.1, t0 + 0.55),
                  (AnimationGroup(*[Create(g) for g in guides]), t0 + 0.3, t0 + 0.7),
                  (FadeIn(diag_l), t0 + 0.2, t0 + 0.6), (FadeIn(one_l), t0 + 0.35, t0 + 0.75))

        # "same-colored patches ...": the comparison stays readable while the twin square grows
        self.span(t("p2s2") + 1.7, (GrowFromCenter(sq2), t("p2s2") + 0.15, t("p2s2") + 0.9),
                  (FadeOut(VGroup(stk, diag, diag_l, one_l, guides)), t("p2s2") + 1.3, t("p2s2") + 1.7))
        # "... more than one unit apart"
        ga, gb = sq1.get_right(), sq2.get_left()
        gap = measure(ga, gb, color=INK, width=3)
        gap_l = lab("1.33", 30).next_to(gap, UP, buff=0.14)
        ur = unit_ruler(ga + DOWN * 0.42, RIGHT)
        ur_l = lab("1", 30, UNIT_COLOR).next_to(ur, DOWN, buff=0.12)
        self.span(t("apart") + 1.1, (Create(gap), "apart", t("apart") + 0.5),
                  (FadeIn(gap_l), t("apart") + 0.2, t("apart") + 0.6),
                  (GrowFromPoint(ur, ga + DOWN * 0.42), t("apart") + 0.55, t("apart") + 1.0),
                  (FadeIn(ur_l), t("apart") + 0.6, t("apart") + 1.1))

        # "squares manage both with nine colors"
        block = [tiles[(i, j)] for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]
        nine = [tiles[(i, j)] for j in (1, 0, -1) for i in (-1, 0, 1)]
        for m in nine:
            m.set_z_index(1)
        rest = sorted([v for k, v in tiles.items() if v not in block and k not in ((0, 0), (3, 0))],
                      key=lambda m: np.linalg.norm(m.get_center() - S1))
        blk_box = SurroundingRectangle(VGroup(*block), buff=0.03, color=ACCENT, stroke_width=6, corner_radius=0.05)
        blk_box.set_z_index(3)
        self.span(t("p2s3") + 1.36,
                  (FadeOut(VGroup(gap, gap_l, ur, ur_l)), "block", t("block") + 0.35),
                  (LaggedStart(*[FadeIn(m, scale=0.6) for m in block], lag_ratio=0.12), "block", t("block") + 0.85))
        # "nine colors": outline the block and count its nine squares (each pops once, in reading order)
        self.span(t("p2s3_end") + 0.05, (Create(blk_box), self.now, self.now + 0.5),
                  (LaggedStart(*[m.animate(rate_func=there_and_back).scale(1.14) for m in nine], lag_ratio=0.3),
                   self.now, t("p2s3_end") + 0.05))
        # ... the block repeats across the plane; every blue square gets an outline, so the twin blue square
        # reads as simply the next block's blue
        blue_t = sorted([v for (i, j), v in tiles.items() if i % 3 == 0 and j % 3 == 0],
                        key=lambda m: np.linalg.norm(m.get_center() - S1))
        blue_ol = VGroup(*[Square(side_length=SQM - 0.04).move_to(m).set_fill(opacity=0).set_stroke(INK, 4.5)
                           for m in blue_t]).set_z_index(2)
        nine_q = panel(N("9?", 80, ACCENT), pad=0.22).move_to([5.3, 2.8, 0]).set_z_index(4)
        self.span(t("beat") + 0.55,
                  (LaggedStart(*[FadeIn(m) for m in rest], lag_ratio=0.02), self.now, t("beat") - 0.3),
                  (LaggedStart(*[Create(o) for o in blue_ol], lag_ratio=0.12), t("beat") - 0.5, t("beat") + 0.25),
                  (FadeIn(nine_q, scale=0.8), "beat", t("beat") + 0.55))

        # ============================================================ P3: hexagons
        BIG = 1.6   # the shape comparison is shown enlarged; the hexagon shrinks to true size for the "1" ruler
        tile_grp = VGroup(*tiles.values())
        hex0 = Polygon(*[P(v) for v in hex_vertices((0, 0))]).scale(BIG).set_stroke(INK, 3).set_fill(INK, 0.22)
        hex0.set_z_index(2)
        self.span(t("hex") + 1.1, (FadeOut(VGroup(tile_grp, blk_box, nine_q, blue_ol)), "hex", t("hex") + 0.55),
                  (Create(hex0), t("hex") + 0.3, t("hex") + 1.1))
        # "cover more area for their width": same circle, same corner-to-corner width, hexagon vs square
        off = RIGHT * 1.75
        R = HS * BIG
        circ_h = DashedVMobject(Circle(radius=R, color=DIM, stroke_width=3), num_dashes=48).move_to(C0 + off)
        circ_s = circ_h.copy().move_to(C0 - off)
        # the square stands on a corner, so its left and right corners touch the circle like the hexagon's do
        sqc = Square(side_length=R * np.sqrt(2)).rotate(PI / 4).move_to(C0 - off)
        sqc.set_stroke(INK, 3).set_fill(INK, 0.22).set_z_index(2)
        yb = C0[1] - R - 0.3
        cs = (C0 - off, C0 + off)
        wid = VGroup(*[measure([c[0] - R, yb, 0], [c[0] + R, yb, 0], color=DIM, width=2.5, tick=0.08) for c in cs])
        drops = VGroup(*[DashedLine([c[0] + sg * R, c[1], 0], [c[0] + sg * R, yb, 0], color=DIM, stroke_width=2,
                                    dash_length=0.05) for c in cs for sg in (-1, 1)])
        tag = T("same width, more area", 30, INK).move_to([0, yb - 0.55, 0])
        self.span("p3s1_end", (hex0.animate.shift(off), "cover", t("cover") + 0.6),
                  (Create(circ_h), t("cover") + 0.3, t("cover") + 0.95),
                  (Create(circ_s), t("cover") + 0.3, t("cover") + 0.95),
                  (DrawBorderThenFill(sqc), t("cover") + 0.45, t("cover") + 1.1),
                  (AnimationGroup(*[Create(d) for d in drops]), t("cover") + 0.85, t("cover") + 1.2),
                  (AnimationGroup(*[Create(w) for w in wid]), t("cover") + 0.95, t("cover") + 1.4),
                  (FadeIn(tag, shift=UP * 0.1), t("cover") + 1.05, t("cover") + 1.5))
        # "just under one unit across, corner to corner"
        self.span(t("p3s2") + 0.9, (FadeOut(VGroup(circ_h, circ_s, sqc, tag, wid, drops)), "p3s2", t("p3s2") + 0.5),
                  (hex0.animate.scale(1 / BIG).move_to(C0), t("p3s2") + 0.1, t("p3s2") + 0.9))
        lv, rv = P((-HEX_SIDE, 0)), P((HEX_SIDE, 0))
        y_r = C0[1] - SQ3 / 2 * HS - 0.42
        u1 = unit_ruler(np.array([lv[0], y_r, 0]), RIGHT)
        u1_l = lab("1", 30, UNIT_COLOR).next_to(u1, DOWN, buff=0.12)
        self.at(t("p3s2") + 1.14, GrowFromPoint(u1, np.array([lv[0], y_r, 0])), FadeIn(u1_l), run_time=0.55)
        dg = measure(lv, rv, color=INK, width=3, tick=0.09)
        dg_l = lab("0.90", 28).move_to(C0 + UP * 0.3)
        hguides = VGroup(DashedLine(lv, [lv[0], y_r, 0], color=DIM, stroke_width=2, dash_length=0.05),
                         DashedLine(rv, [rv[0], y_r, 0], color=DIM, stroke_width=2, dash_length=0.05))
        self.at("corner", Create(dg), FadeIn(dg_l), AnimationGroup(*[Create(h) for h in hguides]), run_time=0.7)

        # "a flower of seven colors, repeated forever"
        cells = {}
        for q, r, c, col in hex_cells(5.8):
            pc = P(c)
            if abs(pc[0]) > 7.11 + HS or pc[1] > 4 + HS or pc[1] < BAND_TOP - HS:
                continue
            poly = Polygon(*[P(v) for v in hex_vertices(c)]).set_fill(PALETTE[col], 0).set_stroke(FAINT, 2)
            poly.q, poly.r, poly.col, poly.c = q, r, col, c
            cells[(q, r)] = poly
        c00 = cells[(0, 0)]
        petals = [cells[k] for k in NBR]
        outer = [m for k, m in cells.items() if m is not c00 and m not in petals]
        flowers = {}
        for k, m in cells.items():
            flowers.setdefault(flower_of(*k), []).append(m)
        hexes = VGroup(*cells.values())
        paint = lambda m, op=FILL: m.animate.set_fill(PALETTE[m.col], op).set_stroke(BG, 3)  # noqa: E731
        c00_target = c00.copy().set_fill(PALETTE[0], FILL).set_stroke(BG, 3)
        self.span(t("flower") + 0.5, (FadeOut(VGroup(u1, u1_l, dg, dg_l, hguides)), "flower", t("flower") + 0.35),
                  (FadeIn(VGroup(*petals, *outer)), "flower", t("flower") + 0.5),
                  (ReplacementTransform(hex0, c00_target), "flower", t("flower") + 0.5))
        self.remove(c00_target)
        c00.set_fill(PALETTE[0], FILL).set_stroke(BG, 3)
        self.add(c00)
        self.span(t("repeat") - 0.05, (LaggedStart(*[paint(m) for m in petals], lag_ratio=0.3),
                                        self.now, t("repeat") - 0.1))
        # "repeated": the flower is stamped outward as a unit, each copy flashing its outline as it lands
        def fkey(b):
            h = hex_center(*b)
            return (round(float(np.linalg.norm(h)), 3), (np.arctan2(h[1], h[0]) - PI / 2) % TAU)
        stamps, flashes = [], VGroup()
        for b in sorted([b for b in flowers if b != (0, 0)], key=fkey):
            ol = flower_outline(*b).set_fill(opacity=0).set_stroke(INK, 5, opacity=0).set_z_index(2)
            flashes.add(ol)
            stamps.append(AnimationGroup(*[paint(m) for m in flowers[b]],
                                         ol.animate(rate_func=there_and_back).set_stroke(opacity=1.0)))
        self.span(t("p3_end") + 0.45, (LaggedStart(*stamps, lag_ratio=0.3), "repeat", t("p3_end") + 0.45))
        self.remove(flashes, *flashes)

        # ============================================================ P4: the ring from a blue hexagon
        blues = [m for m in cells.values() if m.col == 0]
        others = [m for m in cells.values() if m.col != 0]
        self.until(t("p4") + 0.4, *[m.animate.set_fill(opacity=DIMMED) for m in others])
        pos = [(-0.16, 0.13), (0.1, -0.12)]
        me = pt(P(pos[0]), INK, r=0.08).set_z_index(4)
        self.at("stand", FadeIn(me, scale=0.4), run_time=0.35)
        self.at(t("stand") + 0.55, me.animate.move_to(P(pos[1])), run_time=1.0)
        # stick sweeps its unit ring
        c1 = np.array(pos[1])
        a0 = PI * 0.62
        sw = ValueTracker(0.0)
        stip = lambda: P(c1) + SC * np.array([np.cos(a0 + sw.get_value()), np.sin(a0 + sw.get_value()), 0])  # noqa: E731
        sstk = always_redraw(lambda: VGroup(stick(P(c1), stip(), width=5), pt(stip(), UNIT_COLOR, r=0.07)).set_z_index(3))
        grow = always_redraw(lambda: Arc(radius=SC, start_angle=a0, angle=max(sw.get_value(), 1e-3), arc_center=P(c1),
                                         color=UNIT_COLOR, stroke_width=5).set_stroke(BG, 10, background=True).set_z_index(3))
        self.at(t("p4s1") + 2.08, FadeIn(sstk), run_time=0.3)
        self.add(grow)
        self.at(t("p4s1") + 2.4, sw.animate.set_value(TAU), run_time=1.25, rate_func=smooth)
        sstk.clear_updaters()
        grow.clear_updaters()
        arcs = ring_arcs(c1, colored=False)
        assert all(a.col != 0 for a in arcs), "unit ring touches blue"
        self.remove(grow)
        self.add(arcs)
        # "it lands only on other colors"
        self.at("other", FadeOut(sstk),
                LaggedStart(*[a.animate.set_color(PALETTE[a.col]).set_stroke(BG, 10, background=True)
                              for a in sorted(arcs, key=lambda a: (a.get_start()[1] < P(c1)[1], -a.get_start()[0]))],
                            lag_ratio=0.25), run_time=0.8)
        # "... because all other blue hexagons ...": the six nearest blue hexagons get a white outline, drawn on
        # top of their neighbours' edges; the coloured ring stays at full strength in the moat between them
        near_blue = sorted([m for m in blues if m is not c00 and np.linalg.norm(m.c) < 2.2],
                           key=lambda m: (np.arctan2(m.c[1], m.c[0]) - PI / 2) % TAU)
        assert len(near_blue) == 6
        for m in near_blue:
            m.set_z_index(2)
        self.at(t("p4s2") + 2.84, LaggedStart(*[m.animate.set_stroke(INK, 5) for m in near_blue], lag_ratio=0.18),
                run_time=0.9)
        # "... are a bit more than one unit away"
        V = np.array([HEX_SIDE, 0.0])
        W = hex_vertices(hex_center(3, -1))[3]
        assert abs(dist(V, W) - np.sqrt(7) * HEX_SIDE) < 1e-9
        twin = cells[(3, -1)]
        gm = measure(P(V), P(W), color=INK, width=3.5)
        uu = (P(W) - P(V)) / np.linalg.norm(P(W) - P(V))
        nn = np.array([-uu[1], uu[0], 0])
        gm_l = lab("≈ 1.19", 30).move_to((P(V) + P(W)) / 2 + nn * 0.36).set_z_index(4)
        gu = unit_ruler(P(V) - nn * 0.36, uu).set_z_index(4)
        gu_l = lab("1", 30, UNIT_COLOR).move_to(P(V) - nn * 0.36 + uu * SC * 0.5 - nn * 0.3).set_z_index(4)
        gm.set_z_index(4)
        self.until("gap")
        self.span(t("gap") + 0.85,
                  (twin.animate.set_stroke(INK, 7), "gap", t("gap") + 0.6),
                  (arcs.animate.set_stroke(opacity=0.5).set_stroke(BG, 10, opacity=0.5, background=True),
                   "gap", t("gap") + 0.6),
                  (Create(gm), "gap", t("gap") + 0.6), (FadeIn(gm_l), t("gap") + 0.2, t("gap") + 0.6),
                  (GrowFromPoint(gu, P(V) - nn * 0.36), t("gap") + 0.35, t("gap") + 0.85),
                  (FadeIn(gu_l), t("gap") + 0.45, t("gap") + 0.85))
        # end of sentence + pause: the ring comes back to full strength and follows the dot to the worst corner;
        # it still touches no blue and stops just short of the twin
        corner = V
        for k in np.linspace(0, 1, 41):
            cc = np.array(pos[1]) * (1 - k) + corner * k
            assert all(r[2] != 0 for r in ring_runs(cc, 360)), cc
        rop = ValueTracker(0.5)
        live = always_redraw(lambda: ring_arcs((me.get_center() - C0)[:2] / SC, opacity=rop.get_value()))
        self.remove(arcs, *arcs)
        self.add(live)
        self.span(t("p4_end") + 0.5,
                  (FadeOut(VGroup(gu, gu_l)), t("p4_end") - 0.15, t("p4_end") + 0.2),
                  (rop.animate.set_value(1), t("p4_end") - 0.35, t("p4_end")),
                  (me.animate.move_to(P(corner)), t("p4_end") - 0.25, t("p4_end") + 0.5))
        live.clear_updaters()

        # ============================================================ P5: why it works + border points
        l1 = panel(T("too small to hold a stick", 30, INK)).move_to([-3.9, 3.12, 0]).set_z_index(6)
        l2 = panel(T("too far to reach a twin", 30, INK)).move_to([3.9, 3.12, 0]).set_z_index(6)
        a1 = Arrow(l1.get_bottom() + RIGHT * 0.9, C0 + np.array([-0.35, 0.3, 0]), buff=0.08, color=INK, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12).set_z_index(6)
        a2 = Arrow(l2.get_bottom() + LEFT * 0.9, (P(V) + P(W)) / 2 + nn * 0.62, buff=0.08, color=INK, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12).set_z_index(6)
        for a in (a1, a2):
            a.set_stroke(BG, 9, background=True)
        self.at("both", FadeIn(l1, shift=DOWN * 0.1), GrowArrow(a1), run_time=0.6)
        self.at("far", FadeIn(l2, shift=DOWN * 0.1), GrowArrow(a2), run_time=0.6)

        # "border points just take a neighbor's color": zoom 4x about a triple point
        Pz = P(V)
        hexes.generate_target()
        for m in hexes.target:
            m.set_fill(opacity=FILL).set_stroke(BG, 3)
        hexes.target.scale(4, about_point=Pz)
        self.span(t("border") + 0.25,
                  (FadeOut(VGroup(l1, l2, a1, a2, gm, gm_l, live, me)), "p5s1_end", t("p5s1_end") + 0.4),
                  (MoveToTarget(hexes), "p5s1_end", t("border") + 0.25))
        L = 4 * HS
        dirs = [(PI * 2 / 3, 0), (PI * 4 / 3, 5), (0.0, 1)]   # (direction, colour it takes)
        edges = VGroup(*[Line(Pz, Pz + L * np.array([np.cos(d), np.sin(d), 0]), color=INK, stroke_width=21)
                         .set_stroke(BG, 29, background=True) for d, _ in dirs]).set_z_index(3)
        corner_pt = Circle(radius=0.17, color=INK, stroke_width=4).move_to(Pz).set_fill(BG, 1).set_z_index(4)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.2), FadeIn(corner_pt, scale=0.5), run_time=0.4)
        # each edge joins the hexagon that owns it: it takes that tile's paint and loses its dark rim, so it reads
        # as a slightly brighter seam of the owner's colour; then the corner point turns blue
        self.at(t("p5s2") + 1.42,
                LaggedStart(*[e.animate.set_stroke(PALETTE[k]).set_stroke(BG, 0, background=True)
                              for e, (_, k) in zip(edges, dirs)], lag_ratio=0.35),
                run_time=0.6)
        self.play(corner_pt.animate.set_fill(PALETTE[0], 1).set_stroke(BG, 4), run_time=0.35)

        # "enough slack that nothing breaks"
        hexes.generate_target()
        hexes.target.scale(0.25, about_point=Pz)
        r1 = panel(N("0.90 < 1", 36)).move_to([-2.3, 3.15, 0]).set_z_index(6)
        r2 = panel(N("1.19 > 1", 36)).move_to([2.3, 3.15, 0]).set_z_index(6)
        self.span(t("slack") + 0.55, (FadeOut(VGroup(edges, corner_pt)), t("p5s3") - 0.15, t("p5s3") + 0.25),
                  (MoveToTarget(hexes), t("p5s3") + 0.05, t("slack") + 0.1),
                  (FadeIn(r1, scale=1.25), "slack", t("slack") + 0.45),
                  (FadeIn(r2, scale=1.25), t("slack") + 0.1, t("slack") + 0.55))

        # ============================================================ P6: seven is enough
        # the two margins stay up; one flower (seven colours) is outlined, then the scoreboard closes at 7
        fl_ol = flower_outline(0, 0).set_fill(opacity=0).set_stroke(ACCENT, 6).set_z_index(3)
        fl_ol.set_stroke(BG, 11, background=True)
        in_fl = set(map(id, flowers[(0, 0)]))
        rest_hex = [m for m in cells.values() if id(m) not in in_fl]
        self.span(t("seven") + 1.2,
                  (Create(fl_ol), "seven", t("seven") + 0.6),
                  (AnimationGroup(*[m.animate.set_fill(opacity=0.5) for m in rest_hex]), "seven", t("seven") + 0.6),
                  (bar.set_bounds(4, 7), t("seven") + 0.35, t("seven") + 1.2))
        self.play(Indicate(bar.box, color=ACCENT, scale_factor=1.08), Indicate(bar.cells[6], color=ACCENT),
                  run_time=0.7)
        self.until("p6_end")
        self.span(t("p6_end") + 0.7, (FadeOut(VGroup(r1, r2, fl_ol)), "p6_end", t("p6_end") + 0.6),
                  (AnimationGroup(*[m.animate.set_fill(opacity=FILL) for m in rest_hex]), "p6_end", t("p6_end") + 0.7))

        # ============================================================ P7: Isbell
        name = T("John Isbell", 30, INK)
        yr = N("1950 ·", 24, DIM)
        age = T("age 20", 24, DIM)
        sub = VGroup(yr, age).arrange(RIGHT, buff=0.14)
        body = VGroup(name, sub).arrange(DOWN, buff=0.14)
        card = panel(body, pad=0.24).move_to([0, 2.9, 0]).set_z_index(6)
        box = card[0]
        age_final = age.get_center().copy()
        age.move_to([name.get_center()[0], age_final[1], 0])   # alone on its line: centred under the name
        self.at("isbell", FadeIn(box), FadeIn(name, shift=DOWN * 0.08), run_time=0.6)
        self.at(58.02, FadeIn(age, shift=UP * 0.08), run_time=0.45)
        self.at(60.45, age.animate.move_to(age_final), FadeIn(yr, shift=RIGHT * 0.08), run_time=0.45)
        self.until("p7_end")
        self.until("end", FadeOut(VGroup(hexes, bar, box, name, sub)))
        left = [m for m in self.get_mobject_family_members() if m is not band and isinstance(m, VMobject)
                and len(m.points) and (m.get_fill_opacity() > 0.01 or m.get_stroke_opacity() > 0.01)]
        if left:
            print(f"[S07] WARNING: {len(left)} visible mobjects left at the end: {[type(m).__name__ for m in left][:8]}",
                  file=sys.stderr)

