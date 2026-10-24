"""S10_Check: the trap is checked by computer (forced colors, not brute force), confirmed by others,
the scoreboard moves to [5, 7], then the trap shrinks: 1,581 -> 874 (Heule) -> 509 (Parts).

Everything that moves continuously (the web, its zoom, the colour cascade, the cursors, the counter)
is a pure function of the scene time `self.st`, which is exact for every rendered frame (see
update_to_time). Discrete beats (text, panels, the scoreboard) are ordinary animations on the marks.

Honesty notes (viewers pause):
- The web is geom.unit_web(): a genuine unit-distance graph (every stick has length 1) but NOT
  de Grey's graph, so an 'illustration' tag is on screen whenever it is.
- The zoomed search in paragraph 2 is a real run of "fix, follow the forced colors, back up" on the
  part of that web that is on screen: every forced dot really sees the other three colors (its three
  flashed sticks), the dead end really sees all four, and the resumed cascade is recomputed after the
  changed choice (all asserted below).
- 4^1581 has 952 digits (the digit wall in paragraph 1 is the real number); 10^80 is a 1 and 80 zeros.
- Terminal panels (paragraph 3) use Menlo on purpose: it is the one "program output" look in the video.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *  # noqa: E402,F401,F403
from geom import *  # noqa: E402,F401,F403

# ================================================================== the web (problem units)
WP, WE = unit_web()
NW = len(WP)
RMAX = float(np.linalg.norm(WP, axis=1).max())
ADJ = [[] for _ in range(NW)]
for _a, _b in WE:
    ADJ[_a].append(int(_b))
    ADJ[_b].append(int(_a))
WP3 = np.c_[WP, np.zeros(NW)]
DIGITS = str(4 ** 1581)
assert NW == 1581 and len(DIGITS) == 952

COLS4 = [BLUE_P, YELLOW_P, PINK_P, PURPLE_P]   # no green: GOOD checks share the palette green

# ================================================================== screen mapping
WEB_C = np.array([-3.3, 0.05, 0.0])     # the web's home (left half)
S0 = 2.2 / RMAX                          # manim units per problem unit at home (web radius 2.2)
# S09 ends on this same web at centre stage; S10 fades it in at exactly that pose and style, then glides it home
C9 = np.array([0.0, 0.25, 0.0])          # S09 WEB_C
S9 = 2.55 / RMAX                         # S09 WEB_R = 2.55
DOT_R9, EDGE_OP9, EDGE_W9 = 0.02, 0.18, 0.8   # S09's final web: crisp dots, faint unit sticks
S1 = 2.2                                 # zoomed-in scale (unit stick = 2.2 manim units)
PC = np.array([0.0, 0.0, 0.0])           # zoom patch centre (problem coords)
T1 = np.array([-0.4, 0.1, 0.0])          # where the patch centre sits when zoomed
COL_X = 3.4                              # right-hand column

# ================================================================== the search shown in paragraph 2
# the part of the web that is on screen when zoomed (above the scoreboard); propagation only uses it
_QZ = T1[:2] + S1 * (WP - PC[:2])
ONSCREEN = (np.abs(_QZ[:, 0]) < 6.9) & (_QZ[:, 1] > -2.45) & (_QZ[:, 1] < 3.75)
SEEDS = [67, 400, 286, 123, 92]          # the few fixed colours (the last one is the choice that fails)
SEED_COLS = [0, 1, 2, 2, 0]
ALT = 2                                  # the different choice after backing up


def _options(u, col):
    return {0, 1, 2, 3} - {col[w] for w in ADJ[u] if w in col}


def _propagate(col):
    """Breadth-first forced colours. Returns (layers [[(dot, colour)]], dead-end dot or None)."""
    col = dict(col)
    layers = []
    while True:
        cand = sorted({u for v in col for u in ADJ[v] if u not in col and ONSCREEN[u]})
        layer = []
        for u in cand:
            o = _options(u, col)
            if not o:
                return layers, u
            if len(o) == 1:
                layer.append(u)
        if not layer:
            return layers, None
        cur = []
        for u in layer:
            o = _options(u, col)
            if not o:
                layers.append(cur)
                return layers, u
            c = o.pop()
            col[u] = c
            cur.append((u, c))
        layers.append(cur)


_seedcol = dict(zip(SEEDS, SEED_COLS))
for _s in SEEDS:   # every fixed colour is a legal choice
    assert _seedcol[_s] not in {_seedcol[w] for w in ADJ[_s] if w in _seedcol}
TRACE1, DEAD = _propagate(_seedcol)
assert DEAD is not None and [len(_l) for _l in TRACE1] == [1, 2, 4]
_alt = {k: v for k, v in _seedcol.items() if k != SEEDS[-1]}
assert {SEED_COLS[-1], ALT} <= _options(SEEDS[-1], _alt)   # the last seed really was a choice
_alt[SEEDS[-1]] = ALT
TRACE2, _dead2 = _propagate(_alt)
assert _dead2 is None and [len(_l) for _l in TRACE2] == [1, 1]
_final1 = dict(_seedcol)
for _l in TRACE1:
    _final1.update(dict(_l))
assert {_final1[w] for w in ADJ[DEAD] if w in _final1} == {0, 1, 2, 3}   # the dead end sees all four
PART = np.zeros(NW, bool)                # dots that take part in the search (drawn brighter)
PART[SEEDS + [u for _l in TRACE1 + TRACE2 for u, _ in _l] + [DEAD]] = True

# ================================================================== the trimming plan (paragraphs 5-6)
_rng = np.random.default_rng(7)
_prio = np.linalg.norm(WP, axis=1) / RMAX + 0.30 * _rng.random(NW)
_ORDER = np.argsort(-_prio, kind="stable")
PLUCK1 = _ORDER[:707]                    # 1,581 -> 874
PLUCK2 = _ORDER[707:707 + 365]           # 874 -> 509
KEEP = _ORDER[707 + 365:]
assert NW - 707 == 874 and 874 - 365 == 509 and len(KEEP) == 509

# ================================================================== drawing helpers
_K = 0.5523
_ARC = np.array([[1, 0], [1, _K], [_K, 1], [0, 1]], float)
_CIRC = np.concatenate([_ARC @ np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
                        for a in (0, np.pi / 2, np.pi, 3 * np.pi / 2)])
CIRC = np.c_[_CIRC, np.zeros(16)]
_T4 = np.array([0, 1 / 3, 2 / 3, 1])[None, :, None]


def seg_points(A, B):
    A, B = np.atleast_2d(A), np.atleast_2d(B)
    return (A[:, None, :] + _T4 * (B - A)[:, None, :]).reshape(-1, 3)


def circ_points(C, r):
    C = np.atleast_2d(C)
    r = np.broadcast_to(np.asarray(r, float), (len(C),))
    return (C[:, None, :] + r[:, None, None] * CIRC[None]).reshape(-1, 3)


def set_pts(m, pts):
    if len(pts):
        m.set_points(pts)
    else:
        m.clear_points()


def smooth01(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ramp(t, a, b):
    return smooth01((t - a) / (b - a))


def ease_out_back(x):
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def life(t, on, off=None, d_in=0.26, d_out=0.14):
    """Pop-in (with a little overshoot) at `on`, shrink away at `off`."""
    if t < on:
        return 0.0
    s = ease_out_back(min(1.0, (t - on) / d_in))
    if off is not None and t > off:
        s *= 1 - smooth01((t - off) / d_out)
    return max(0.0, s)


def inv_smooth(q):
    """Inverse of smoothstep 3x^2 - 2x^3 on [0, 1]."""
    return 0.5 - np.sin(np.arcsin(1 - 2 * np.asarray(q)) / 3)


def power(b, e, size=48, color=INK):
    base = N(b, size, color)
    ex = N(e, round(size * 0.58), color)
    ex.next_to(base, RIGHT, buff=0.04).align_to(base, UP).shift(UP * base.height * 0.34)
    return VGroup(base, ex)


def baseline_row(items, digit_ref, buff=0.2):
    """Lay items out left to right; align every item on the digits' baseline (first glyph's bottom),
    except operators like ≈ which are centred on the digits."""
    row = VGroup()
    x = 0.0
    y_base = 0.0
    y_mid = digit_ref.height / 2
    for it, mode in items:
        it.move_to([x + it.width / 2, 0, 0])
        if mode == "base":   # it[0]: the base number of a power, or the first glyph of a word
            it.shift(UP * (y_base - it[0].get_bottom()[1]))
        else:
            it.shift(UP * (y_mid - it.get_center()[1]))
        row.add(it)
        x += it.width + buff
    return row


def digit_rows(s, per_row, glyph_w, pitch, color, left_top):
    """The digits of `s` written out, `per_row` to a line (one Text per line, same glyph scale)."""
    rows = VGroup()
    ref = N("0" * per_row, 24, color)
    k = glyph_w * per_row / ref.width
    for i in range(0, len(s), per_row):
        r = N(s[i:i + per_row], 24, color).scale(k)
        r.move_to(left_top + np.array([r.width / 2, -pitch * (i // per_row) - r.height / 2, 0]))
        rows.add(r)
    return rows


POINTER = np.array([[0, 0], [0, -0.30], [0.075, -0.228], [0.13, -0.345], [0.178, -0.323],
                    [0.124, -0.208], [0.218, -0.208], [0, 0]]) * 0.95


def pointer_points(tips):
    """Classic mouse pointers (closed polygons) with their tips at `tips` (k, 3)."""
    if len(tips) == 0:
        return np.zeros((0, 3))
    poly = np.c_[POINTER, np.zeros(len(POINTER))]
    A = poly[:-1][None] + tips[:, None, :]
    B = poly[1:][None] + tips[:, None, :]
    return (A[:, :, None, :] + _T4[None] * (B - A)[:, :, None, :]).reshape(-1, 3)


def term_panel(title, result):
    W, H = 4.5, 1.2
    box = RoundedRectangle(corner_radius=0.14, width=W, height=H, stroke_color=FAINT, stroke_width=2,
                           fill_color="#161B23", fill_opacity=1)
    lights = VGroup(*[Dot(radius=0.045, color=FAINT) for _ in range(3)]).arrange(RIGHT, buff=0.09)
    lights.move_to(box.get_corner(UL) + np.array([0.33, -0.27, 0]))
    ttl = T(title, 24, INK).next_to(lights, RIGHT, buff=0.28)
    ttl.shift(UP * (lights.get_center()[1] - ttl.get_center()[1]))
    c = box.get_corner(DL) + np.array([0.45, 0.36, 0])
    spin = Arc(radius=0.13, start_angle=0, angle=1.45 * PI, stroke_width=3.5, color=DIM, arc_center=c)
    status = T("checking…", 24, DIM, font="Menlo").next_to(spin, RIGHT, buff=0.28)
    status.shift(UP * (c[1] - status.get_center()[1]))
    tick = check_mark(c + np.array([-0.02, 0.02, 0]), size=0.15, width=5)
    res = T(result, 24, INK, font="Menlo").next_to(spin, RIGHT, buff=0.28)
    res.shift(UP * (c[1] - res.get_center()[1]))
    frame = VGroup(box, lights, ttl, spin, status)
    return frame, spin, status, tick, res, c


def paper_stack():
    pages = VGroup()
    for k, ang in enumerate([-0.12, 0.06, -0.03]):
        pg = RoundedRectangle(corner_radius=0.05, width=1.1, height=1.42, fill_color="#CDD4DE", fill_opacity=1,
                              stroke_color="#7D8696", stroke_width=1.5)
        pg.rotate(ang).shift(np.array([0.07 * k, -0.05 * k, 0]))
        pages.add(pg)
    top = pages[-1]
    lines = VGroup(*[Line(LEFT * 0.36, RIGHT * (0.36 - 0.2 * (i % 3 == 2)), stroke_width=2.4, color="#6B7484")
                     .shift(UP * (0.46 - 0.155 * i)) for i in range(7)])
    lines.rotate(-0.03).move_to(top).shift(LEFT * 0.02)
    body = Rectangle(width=0.95, height=0.12, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
    ferrule = Rectangle(width=0.1, height=0.12, stroke_width=0, fill_color=DIM, fill_opacity=1)
    ferrule.next_to(body, LEFT, buff=0)
    eraser = Rectangle(width=0.1, height=0.12, stroke_width=0, fill_color=PINK_P, fill_opacity=1)
    eraser.next_to(ferrule, LEFT, buff=0)
    wood = Polygon(body.get_corner(UR), body.get_corner(DR), body.get_right() + RIGHT * 0.2,
                   stroke_width=0, fill_color="#E9D2A8", fill_opacity=1)
    lead = Polygon(body.get_right() + RIGHT * 0.13 + UP * 0.022, body.get_right() + RIGHT * 0.13 + DOWN * 0.022,
                   body.get_right() + RIGHT * 0.2, stroke_width=0, fill_color="#3A4150", fill_opacity=1)
    pencil = VGroup(eraser, ferrule, body, wood, lead).rotate(-0.95)
    pencil.next_to(top, RIGHT, buff=-0.35).shift(DOWN * 0.1)
    return VGroup(pages, lines, pencil)


class S10_Check(TimedScene):
    # ---------------------------------------------------------------- exact per-frame scene time
    def update_to_time(self, t):
        self.st = self._frames / self._fps + t
        super().update_to_time(t)

    def drive(self, mob, fn):
        """Attach a time-driven updater: fn(mob, scene_time). dt-based so waits keep rendering it."""
        mob.add_updater(lambda m, dt: fn(m, self.st))
        return mob

    def construct(self):
        self.st = 0.0
        M = self.t

        # ============================================================ timing plan (scene seconds)
        z_in = (M("p2") + 0.45, M("fix") - 0.05)
        z_out = (M("p3") + 0.25, M("p3") + 1.55)
        ov_fade = (M("p3") + 0.25, M("p3") + 0.8)
        seed_on = [M("fix") + 0.25 * k for k in range(len(SEEDS))]
        l1_on = [M("follow") + 0.12 + 0.42 * k for k in range(len(TRACE1))]   # one layer per 0.42 s
        STAG = 0.07                                    # dots of one layer pop one after another
        dead_on, dead_off = M("back"), M("back") + 1.05   # the dead end holds through "dead ends"
        rew0, rew_dt = dead_off + 0.05, 0.07              # then (in the pause) the rewind ...
        l1_off = [rew0 + rew_dt * (len(TRACE1) - 1 - k) for k in range(len(TRACE1))]
        swap0 = rew0 + rew_dt * len(TRACE1) + 0.02        # ... the last choice is flagged and changed ...
        seed_last_off = swap0 + 0.08
        alt_on = swap0 + 0.26
        l2_on = [alt_on + 0.26 + 0.2 * k for k in range(len(TRACE2))]   # ... and the cascade resumes

        pl1 = (M("together") + 1.0, M("shrunk") + 0.38)     # counter lands on 874 inside the number
        pl2 = (M("p6s1") + 1.95, M("record") - 0.05)       # plucked during "found one with just"

        rm_t = np.full(NW, np.inf)
        rm_t[PLUCK1] = pl1[0] + (pl1[1] - pl1[0]) * inv_smooth((np.arange(707) + 0.5) / 707)
        rm_t[PLUCK2] = pl2[0] + (pl2[1] - pl2[0]) * inv_smooth((np.arange(365) + 0.5) / 365)
        rm_sorted = np.sort(rm_t[np.isfinite(rm_t)])

        def alive_count(t):
            return NW - int(np.searchsorted(rm_sorted, t, side="right"))

        fade_in = 0.5                        # lead-in: web, counter, bar and tag fade in at S09's end pose ...
        glide = (fade_in, M("not"))           # ... then web + counter glide home, landing as the formula appears

        def web_op(t):
            return (ramp(t, 0.0, fade_in) * (1 - ramp(t, M("p4"), M("p4") + 0.7))
                    + ramp(t, M("p5"), M("p5") + 0.8) * (1 - ramp(t, M("p6_end") + 0.1, M("end") - 0.08)))

        def zoom_u(t):
            return ramp(t, *z_in) - ramp(t, *z_out)

        def cam(t):
            g = ramp(t, *glide)
            S_home = S9 * (S0 / S9) ** g
            A_home = C9 + g * (WEB_C - C9) + S_home * PC
            u = zoom_u(t)
            S = S_home * (S1 / S_home) ** u
            A = (1 - u) * A_home + u * T1
            return A, S, u

        # ============================================================ the web (time-driven, added first)
        web_edges = VMobject(z_index=0).set_fill(opacity=0).set_stroke(UNIT_COLOR, width=EDGE_W9, opacity=0)
        web_dots = VMobject(z_index=1).set_stroke(width=0).set_fill(INK, opacity=0)
        part_dots = VMobject(z_index=1).set_stroke(width=0).set_fill(INK, opacity=0)
        web = VGroup(web_edges, web_dots, part_dots)

        def web_fn(m, t):
            op = web_op(t)
            if op < 0.004:
                for mob in web:
                    set_pts(mob, [])
                return
            A, S, u = cam(t)
            Q = A + S * (WP3 - PC)
            alive = rm_t > t
            inside = alive & (np.abs(Q[:, 0]) < 7.5) & (np.abs(Q[:, 1]) < 4.3)
            eop = op * EDGE_OP9 * (1 - u)      # zoomed in, the web's own sticks go away entirely
            if eop > 0.003:
                ek = alive[WE[:, 0]] & alive[WE[:, 1]] & (inside[WE[:, 0]] | inside[WE[:, 1]])
                set_pts(web_edges, seg_points(Q[WE[ek, 0]], Q[WE[ek, 1]]))
            else:
                set_pts(web_edges, [])
            web_edges.set_stroke(opacity=eop)
            # S09's dot size at S09's scale, shrinking gently with the web; the zoomed look is unchanged
            r0 = DOT_R9 * (S / S9) ** 0.5 * (1 - u) + 0.0145 * (S / S0) ** 0.5 * u
            set_pts(web_dots, circ_points(Q[inside & ~PART], r0))
            set_pts(part_dots, circ_points(Q[inside & PART], r0 * (1 + 0.7 * u)))
            web_dots.set_fill(opacity=op * (1 - 0.85 * u))    # bystanders fade back when zoomed
            part_dots.set_fill(opacity=op * (1 - 0.1 * u))    # the dots in the search stay

        self.drive(web, web_fn)
        self.add(web)

        # ============================================================ scoreboard (fixed home, on top)
        bar = BoundsBar(lo=4, hi=7).scale(0.8).to_edge(DOWN, buff=0.3)
        backing = RoundedRectangle(corner_radius=0.2, width=bar.width + 0.5, height=bar.height + 0.3,
                                   stroke_width=0, fill_color=BG, fill_opacity=1).move_to(bar)
        board = VGroup(backing, bar).set_z_index(30)
        tag_t = VGroup(T("illustration,", 24, DIM), T("not the actual graph", 24, DIM)) \
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.08).to_corner(DR, buff=0.35).shift(LEFT * 0.2 + UP * 0.1)  # = S09
        tag_bg = RoundedRectangle(corner_radius=0.12, width=tag_t.width + 0.34, height=tag_t.height + 0.26,
                                  stroke_width=0, fill_color=BG, fill_opacity=1).move_to(tag_t)
        tag = VGroup(tag_bg, tag_t).set_z_index(30)

        # the counter exactly as S09 leaves it (top centre), later gliding to its home above the web
        small_cnt = VGroup(N("1,581", 44, INK), T("dots", 28, DIM))
        small_cnt[0].shift(RIGHT * (0.3 - small_cnt[0].get_right()[0]) + UP * (3.45 - small_cnt[0].get_top()[1]))
        small_cnt[1].shift(RIGHT * (0.5 - small_cnt[1].get_left()[0]) + UP * (3.40 - small_cnt[1].get_top()[1]))
        cnt_home = WEB_C + UP * 2.78

        # ============================================================ P1: not every coloring
        self.until(fade_in, FadeIn(board), FadeIn(small_cnt), FadeIn(tag))
        self.until("not", small_cnt.animate(rate_func=smooth01).move_to(cnt_home))

        x0 = -0.35
        row1 = baseline_row([(power("4", "1581", 50), "base"), (N("≈", 46, DIM), "mid"),
                             (power("10", "952", 50), "base"), (T("colorings", 32, DIM), "base")],
                            N("0", 50))
        row1.move_to([x0 + row1.width / 2, 3.0, 0])
        four, expo = row1[0][0], row1[0][1]
        paints = VGroup(*[Dot(radius=0.075, color=c).set_stroke(BG, width=2, background=True) for c in COLS4])
        paints.arrange(RIGHT, buff=0.07).next_to(four, DOWN, buff=0.2)
        # the number itself, all 952 digits, 68 to a line (a wall) ...
        GW, PITCH = 0.0985, 0.166
        wall = digit_rows(DIGITS, 68, GW, PITCH, DIM, np.array([x0, 2.45, 0]))
        lab1 = T("952 digits", 26, ACCENT).next_to(wall, DOWN, buff=0.14).align_to(wall, RIGHT)
        # ... against the atoms: a 1 and 80 zeros, just over one line at the same size
        row2 = baseline_row([(T("atoms in the universe", 32, INK), "base"), (N("≈", 46, DIM), "mid"),
                             (power("10", "80", 50), "base")], N("0", 50))
        row2.move_to([x0 + row2.width / 2, -0.76, 0])
        atoms = digit_rows("1" + "0" * 80, 68, GW, PITCH, INK, np.array([x0, -1.22, 0]))
        lab2 = T("81 digits", 26, INK).next_to(atoms, DOWN, buff=0.14).align_to(wall, RIGHT)

        cnt_copy = small_cnt[0].copy()
        self.at("not", FadeIn(VGroup(four, row1[1:]), shift=0.15 * DOWN),
                ReplacementTransform(cnt_copy, expo, path_arc=-0.35),
                LaggedStart(*[GrowFromCenter(p) for p in paints], lag_ratio=0.2), run_time=0.9)
        self.at(M("not") + 1.5, FadeOut(paints, scale=0.6), run_time=0.4)
        self.at("atoms", LaggedStart(*[FadeIn(r, shift=0.05 * DOWN) for r in wall], lag_ratio=0.1),
                FadeIn(lab1, rate_func=lambda a: smooth(min(1.0, max(0.0, (a - 0.5) / 0.5)))), run_time=1.1)
        self.at(M("atoms") + 1.2, FadeIn(row2, shift=0.15 * DOWN), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r, shift=0.05 * DOWN) for r in atoms], lag_ratio=0.3),
                  FadeIn(lab2), run_time=0.5)

        # ============================================================ P2: fix, follow, back up (time-driven)
        self.at("p2", FadeOut(VGroup(row1, wall, lab1, row2, atoms, lab2, small_cnt)), run_time=0.6)

        def witnesses_of(u, c, known):
            """One already-coloured neighbour for each of the other colours (most recent first)."""
            out = []
            for cc in range(4):
                if cc == c:
                    continue
                nb = [w for w in ADJ[u] if w in known and known[w][1] == cc]
                out.append(max(nb, key=lambda w: (known[w][0], -w)))
            return out

        events = []   # dict(i, c, on, off, wit, pop)
        known = {}
        for k, (s, c) in enumerate(zip(SEEDS, SEED_COLS)):
            off = seed_last_off if k == len(SEEDS) - 1 else None
            events.append(dict(i=s, c=c, on=seed_on[k], off=off, wit=[], pop=0.0))
            known[s] = (seed_on[k], c)
        for k, layer in enumerate(TRACE1):
            for j, (u, c) in enumerate(layer):
                events.append(dict(i=u, c=c, on=l1_on[k] + STAG * j, off=l1_off[k], wit=witnesses_of(u, c, known),
                                   pop=0.0))
            for j, (u, c) in enumerate(layer):
                known[u] = (l1_on[k] + STAG * j, c)
        dead_wit = []
        for c in range(4):
            nb = [w for w in ADJ[DEAD] if w in known and known[w][1] == c]
            dead_wit.append(max(nb, key=lambda w: known[w][0]))
        known2 = {s: (seed_on[k], SEED_COLS[k]) for k, s in enumerate(SEEDS)}
        known2[SEEDS[-1]] = (alt_on, ALT)
        events.append(dict(i=SEEDS[-1], c=ALT, on=alt_on, off=None, wit=[], pop=0.3))
        for k, layer in enumerate(TRACE2):
            for j, (u, c) in enumerate(layer):
                events.append(dict(i=u, c=c, on=l2_on[k] + STAG * j, off=None, wit=witnesses_of(u, c, known2),
                                   pop=0.0))
            for j, (u, c) in enumerate(layer):
                known2[u] = (l2_on[k] + STAG * j, c)

        R_PAINT = 0.105
        ev_mobs = []
        for e in events:
            dot = VMobject().set_fill(COLS4[e["c"]], opacity=1).set_stroke(BG, width=2.5, background=True)
            dot.set_stroke(width=0)
            flash = VMobject().set_fill(opacity=0).set_stroke(COLS4[e["c"]], width=3, opacity=0)
            stks = [VMobject().set_fill(opacity=0).set_stroke(UNIT_COLOR, width=3, opacity=0) for _ in e["wit"]]
            ev_mobs.append((dot, flash, stks))
        seed_rings = [VMobject().set_fill(opacity=0).set_stroke(INK, width=2.5, opacity=0) for _ in SEEDS]
        dead_dot = VMobject().set_fill(BAD, opacity=0).set_stroke(width=0)
        dead_ring = VMobject().set_fill(opacity=0).set_stroke(BAD, width=4, opacity=0)
        dead_x = VMobject().set_fill(opacity=0).set_stroke(BG, width=3.5, opacity=0)
        dead_sticks = [VMobject().set_fill(opacity=0).set_stroke(UNIT_COLOR, width=3.4, opacity=0) for _ in dead_wit]
        overlay = VGroup(*[s for trio in ev_mobs for s in trio[2]],       # sticks under dots
                         *dead_sticks, *[trio[1] for trio in ev_mobs], *seed_rings,
                         *[trio[0] for trio in ev_mobs], dead_ring, dead_dot, dead_x).set_z_index(5)
        wit_set = set(dead_wit)
        ring_col = [ManimColor(INK), ManimColor(ACCENT)]

        def overlay_fn(m, t):
            ov = 1 - ramp(t, *ov_fade)
            A, S, u = cam(t)
            if ov <= 0.001 or u < 0.02:
                for mob in overlay:
                    mob.set_stroke(opacity=0).set_fill(opacity=0)
                return
            r = R_PAINT * (S / S1) ** 0.75
            focus = ramp(t, dead_on, dead_on + 0.15) * (1 - ramp(t, dead_off, dead_off + 0.15))
            dimmed = ov * (1 - 0.6 * focus)
            pos = lambda i: A + S * (WP3[i] - PC)  # noqa: E731
            for e, (dot, flash, stks) in zip(events, ev_mobs):
                p = pos(e["i"])
                s = life(t, e["on"], e["off"])
                if e["pop"]:    # the changed choice pops in a little larger, then settles
                    s *= 1 + e["pop"] * (1 - ramp(t, e["on"] + 0.2, e["on"] + 0.55))
                if e["i"] in wit_set and dead_on <= t <= dead_off + 0.2:
                    s *= 1 + 0.28 * np.sin(np.pi * min(1.0, (t - dead_on) / 0.5))
                if s > 0.002:
                    o = ov if e["i"] in wit_set else dimmed
                    set_pts(dot, circ_points(p, r * s))
                    dot.set_fill(opacity=o).set_stroke(opacity=o, background=True)
                else:
                    set_pts(dot, circ_points(p, 1e-4))
                    dot.set_fill(opacity=0).set_stroke(opacity=0, background=True)
                x = (t - e["on"]) / 0.42
                if 0 <= x <= 1 and (e["off"] is None or t < e["off"]):
                    set_pts(flash, circ_points(p, r * (1.2 + 1.5 * x)))
                    flash.set_stroke(opacity=0.85 * (1 - x) * ov)
                else:
                    flash.set_stroke(opacity=0)
                # why it is forced: it sees the three other colours. Sticks flash in, then settle faint.
                for w, stk in zip(e["wit"], stks):
                    f = smooth01((t - (e["on"] - 0.2)) / 0.2)
                    if e["off"] is not None:
                        f *= 1 - smooth01((t - e["off"]) / 0.12)
                    if f > 0.002:
                        q = pos(w)
                        set_pts(stk, seg_points(q, q + f * (p - q)))
                        bright = 0.2 + 0.72 * (1 - ramp(t, e["on"] + 0.2, e["on"] + 0.5))
                        stk.set_stroke(opacity=bright * dimmed)
                    else:
                        stk.set_stroke(opacity=0)
            for k, ring_m in enumerate(seed_rings):
                s = life(t, seed_on[k])
                col = ring_col[0]
                if k == len(SEEDS) - 1:   # the choice that failed: flagged in ACCENT while it changes
                    a = ramp(t, swap0, swap0 + 0.12) * (1 - ramp(t, swap0 + 0.45, swap0 + 0.7))
                    s *= 1 + 0.35 * np.sin(np.pi * min(1.0, max(0.0, (t - swap0) / 0.55)))
                    col = interpolate_color(ring_col[0], ring_col[1], a)
                set_pts(ring_m, circ_points(pos(SEEDS[k]), r * 1.75 * max(s, 1e-3)))
                ring_m.set_stroke(col, width=2.5 + 1.5 * (k == len(SEEDS) - 1 and swap0 <= t <= swap0 + 0.7),
                                  opacity=(0.9 if s > 0.002 else 0) * dimmed)
            # dead end: a dot with no colour left, and the four colours it sees
            s = life(t, dead_on, dead_off, d_out=0.2)
            p = pos(DEAD)
            set_pts(dead_dot, circ_points(p, 1.25 * r * max(s, 1e-3)))
            dead_dot.set_fill(opacity=ov if s > 0.002 else 0)
            pulse = 0.5 - 0.5 * np.cos(2 * np.pi * max(0.0, t - dead_on) / 0.3)
            set_pts(dead_ring, circ_points(p, r * (1.95 + 0.4 * pulse * (t < dead_on + 0.6)) * max(s, 1e-3)))
            dead_ring.set_stroke(opacity=(0.95 if s > 0.002 else 0) * ov)
            h = 0.5 * r * max(s, 1e-3)
            set_pts(dead_x, np.concatenate([seg_points(p + h * (UL), p + h * (DR)), seg_points(p + h * (UR), p + h * (DL))]))
            dead_x.set_stroke(opacity=(1 if s > 0.002 else 0) * ov)
            for w, stk in zip(dead_wit, dead_sticks):
                f = smooth01((t - dead_on) / 0.2) * (1 - smooth01((t - dead_off) / 0.15))
                if f > 0.002:
                    q = pos(w)
                    set_pts(stk, seg_points(p, p + f * (q - p)))
                    stk.set_stroke(opacity=0.95 * ov)
                else:
                    stk.set_stroke(opacity=0)

        self.drive(overlay, overlay_fn)
        self.add(overlay)
        self.until("p3")

        # ============================================================ P3: others confirm it
        self.at(z_out[1] - 0.65, FadeIn(small_cnt), run_time=0.5)
        overlay.clear_updaters()
        self.remove(overlay)

        panels = []
        specs = [("program A", "no 4-coloring"), ("program B", "no 4-coloring"),
                 ("stick lengths", "all sticks = 1")]
        for k, (ttl, res) in enumerate(specs):
            frame, spin, status, tick, resm, c = term_panel(ttl, res)
            VGroup(frame, tick, resm).shift(np.array([COL_X, 2.25 - 1.45 * k, 0]))
            spin.rotate(-0.9 * k, about_point=spin.get_arc_center())
            # spins in place about its own centre, so it travels with its panel as that slides in
            spin.add_updater(lambda m, dt: m.rotate(-5.0 * dt, about_point=m.get_arc_center()))
            panels.append((frame, spin, status, tick, resm))

        self.at("confirm", LaggedStart(*[FadeIn(p[0], shift=0.6 * LEFT) for p in panels], lag_ratio=0.22),
                run_time=1.0)
        for k, (frame, spin, status, tick, resm) in enumerate(panels):
            self.at(M("held") + 0.24 * k, FadeOut(spin, scale=0.5), FadeOut(status),
                    Create(tick), FadeIn(resm, shift=0.08 * RIGHT), run_time=0.3)
            spin.clear_updaters()
            frame.remove(spin, status)   # gone for good (FadeOut resets them to full opacity)
        self.at(M("held") + 0.24 * 2 + 0.38, *[Indicate(p[3], color=GOOD, scale_factor=1.35) for p in panels],
                run_time=0.45)

        # ============================================================ P4: the scoreboard moves
        yrs = VGroup(N("68", 72, INK), T("years", 36, DIM))
        yrs[1].next_to(yrs[0], RIGHT, buff=0.2).align_to(yrs[0], DOWN)
        span = N("1950 – 2018", 30, DIM)
        yrs_grp = VGroup(yrs, span).arrange(DOWN, buff=0.25).move_to(UP * 2.55)
        late_in = lambda a: smooth(min(1.0, max(0.0, (a - 0.33) / 0.67)))  # noqa: E731  starts on "sixty-eight"
        early_out = lambda a: smooth(min(1.0, a / 0.65))  # noqa: E731
        self.at("p4", FadeOut(VGroup(*[VGroup(p[0], p[3], p[4]) for p in panels]), small_cnt, tag,
                              rate_func=early_out),
                FadeIn(yrs_grp, shift=0.1 * UP, rate_func=late_in), run_time=1.05)
        board_home = board.get_center()
        BIG = 1.7
        # the big reveal plays centre stage: the scoreboard rises and grows ...
        self.at("moved", board.animate.scale(BIG).move_to(UP * 0.25), run_time=0.9)
        self.at("p4s2", Indicate(bar.cells[3], color=BAD, scale_factor=1.45), run_time=0.8)
        bar.strikes[3].set_stroke(color=BAD, width=5)
        self.at("five", bar.set_bounds(5, 7), FadeOut(yrs_grp), run_time=0.7)
        self.play(bar.box.animate(rate_func=there_and_back).set_stroke(width=9),
                  *[Indicate(bar.cells[i], color=ACCENT, scale_factor=1.25) for i in (4, 5, 6)], run_time=0.5)
        # ... and after the hold eases back to its home at the bottom edge
        home = board.copy().scale(1 / BIG).move_to(board_home)
        home[1].strikes[3].set_stroke(color=DIM, width=3)
        self.at(M("p4_end") + 0.3, Transform(board, home), run_time=0.7)

        # ============================================================ P5: shrinking it together
        # the counter lives in the right-hand column from here on
        cnt_cache = {}

        def cnt_text(v):
            if v not in cnt_cache:
                cnt_cache[v] = N(f"{v:,}", 92, INK)
            return cnt_cache[v]

        counter = VMobject()
        CNT_Y = 1.3

        def cnt_fn(m, t):
            v = alive_count(t)
            op = ramp(t, M("p5"), M("p5") + 0.7) * (1 - ramp(t, M("p6_end") + 0.1, M("end") - 0.08))
            txt = cnt_text(v).copy()
            a = ramp(t, pl2[1] - 0.1, pl2[1] + 0.4)      # only the landed 509 turns gold
            txt.set_color(interpolate_color(ManimColor(INK), ManimColor(ACCENT), a))
            txt.scale(1 + 0.12 * a).move_to([COL_X, CNT_Y, 0]).set_opacity(op)
            m.become(txt)

        self.drive(counter, cnt_fn)
        self.add(counter)
        dots_lab = T("dots", 28, DIM).move_to([COL_X, CNT_Y - 0.9, 0])
        self.at("p5", FadeIn(tag), FadeIn(dots_lab), run_time=0.7)

        # the original 1,581-dot outline stays as a faint ghost, so the shrinking is always measured against it
        ghost = DashedVMobject(Circle(radius=2.26, stroke_width=2.5, color=DIM), num_dashes=64,
                               dashed_ratio=0.45).move_to(WEB_C).set_stroke(opacity=0.55).set_z_index(-1)

        # cursors: people plucking dots off the web
        NC = 26
        rng = np.random.default_rng(3)
        ang = np.arctan2(WP[PLUCK1, 1], WP[PLUCK1, 0])
        cuts = np.sort(-np.pi + (np.arange(NC) + 0.5 * rng.random(NC)) * 2 * np.pi / NC)
        sector = (np.searchsorted(cuts, ang) - 1) % NC
        home_pts = WEB_C + S0 * WP3                   # web is static at home in paragraph 5
        cur_t, cur_p, cur_start = [], [], []
        for k in range(NC):
            idx = PLUCK1[sector == k]
            idx = idx[np.argsort(rm_t[idx])]
            cur_t.append(rm_t[idx])
            cur_p.append(home_pts[idx])
            th = np.arctan2(*(cur_p[k].mean(0) - WEB_C)[[1, 0]]) + 0.35 * (rng.random() - 0.5)
            d = np.array([np.cos(th), np.sin(th), 0])
            lam = min((7.6 - WEB_C[0]) / d[0] if d[0] > 1e-6 else np.inf,
                      (-7.6 - WEB_C[0]) / d[0] if d[0] < -1e-6 else np.inf,
                      4.4 / d[1] if d[1] > 1e-6 else np.inf,
                      -4.4 / d[1] if d[1] < -1e-6 else np.inf)
            st = WEB_C + lam * d
            if d[0] > 0.25:        # would cross the text column: come in from the top edge instead
                st = np.array([-1.6 + 2.6 * rng.random(), 4.45, 0.0])
            elif st[1] < -4.0:     # bottom edge: stay left of the scoreboard
                st[0] = min(st[0], -3.6 - 0.8 * rng.random())
            cur_start.append(st)
        phase = rng.random((NC, 2)) * 2 * np.pi
        t_in = [M("together") + 0.55 * rng.random() for k in range(NC)]
        t_dur = [0.85 + 0.4 * rng.random() for k in range(NC)]
        SIG = 0.33

        def track(k, t):
            ts, ps = cur_t[k], cur_p[k]
            tc = min(max(t, ts[0]), ts[-1])          # hold at the ends of the plucking window
            w = np.exp(-((tc - ts) / SIG) ** 2)
            return (w[:, None] * ps).sum(0) / w.sum()

        def cursor_pos(k, t):
            wander = 0.07 * np.array([np.sin(0.9 * t + phase[k, 0]), np.cos(0.75 * t + phase[k, 1]), 0])
            p = track(k, t) + wander * ramp(t, pl1[1] - 1.0, pl1[1] + 0.5)
            a0, a1 = t_in[k], t_in[k] + t_dur[k]
            if t < a1:
                x = smooth01((t - a0) / (a1 - a0))
                x = 1 - (1 - x) ** 2
                p = cur_start[k] + x * (track(k, a1) - cur_start[k])
            b0 = M("p6") + 0.3 * phase[k, 0] / (2 * np.pi)
            if t > b0:
                x = smooth01((t - b0) / 0.8)
                p = p + x * x * (cur_start[k] - p)
            return p

        halos = VMobject().set_fill(INK, opacity=0).set_stroke(width=0)
        arrows = VMobject().set_fill(INK, opacity=0).set_stroke(BG, width=1.6, opacity=0)
        cursors = VGroup(halos, arrows).set_z_index(10)

        def cursors_fn(m, t):
            if t < M("together") - 0.05 or t > M("p6") + 1.0:
                set_pts(halos, [])
                set_pts(arrows, [])
                return
            tips = np.array([cursor_pos(k, t) for k in range(NC)])
            set_pts(halos, circ_points(tips, 0.075))
            set_pts(arrows, pointer_points(tips))
            op = 1 - ramp(t, M("p6") + 0.35, M("p6") + 0.9)
            halos.set_fill(opacity=0.32 * op)
            arrows.set_fill(opacity=0.95 * op).set_stroke(opacity=op)

        self.drive(cursors, cursors_fn)
        self.add(cursors)

        poly = VGroup(T("Polymath16", 34, INK), T("open online project", 26, DIM)).arrange(DOWN, buff=0.16)
        poly.move_to([COL_X, 2.85, 0])
        self.at("together", FadeIn(poly, shift=0.1 * DOWN), run_time=0.7)
        self.at(pl1[0] + 0.1, Create(ghost), run_time=0.9)
        heule = T("Marijn Heule · April 2018", 28, INK).move_to([COL_X, CNT_Y - 1.55, 0])
        self.at("shrunk", FadeIn(heule, shift=0.1 * UP), run_time=0.7)

        # ============================================================ P6: 509, by hand
        self.at("p6", FadeOut(poly), FadeOut(heule), run_time=0.6)
        parts = T("Jaan Parts · 2020", 34, INK).move_to([COL_X, 2.8, 0])
        self.at(M("p6s1") + 1.25, FadeIn(parts, shift=0.1 * DOWN), run_time=0.6)
        sticks_lab = T("2,442 sticks", 28, DIM).move_to(dots_lab).shift(DOWN * 0.45)
        self.at(M("record") + 0.75, FadeIn(sticks_lab, shift=0.08 * UP), run_time=0.6)
        known_tag = T("smallest known as of 2026", 26, ACCENT)
        known_box = SurroundingRectangle(known_tag, buff=0.14, corner_radius=0.14, color=ACCENT, stroke_width=2)
        known_grp = VGroup(known_box, known_tag).move_to([COL_X, CNT_Y - 1.95, 0])
        self.at("known", FadeIn(known_grp, scale=0.9), run_time=0.6)
        cursors.clear_updaters()
        self.remove(cursors)

        stack = paper_stack().scale(0.9).move_to([COL_X - 0.05, -1.82, 0])
        self.at("hand", FadeIn(stack, shift=0.2 * UP), run_time=0.5)
        # check marks over regions of the 509-dot web (it stays small: it is the smallest known)
        kept = WP[KEEP]
        R_in = np.percentile(np.linalg.norm(kept, axis=1), 80)
        centers = [np.zeros(2)] + [0.6 * R_in * np.array([np.cos(a), np.sin(a)])
                                   for a in np.pi / 2 + np.arange(6) * np.pi / 3]
        checks, ck_anims = [], []
        for c in centers:
            p = WEB_C + S0 * np.array([c[0], c[1], 0])
            ck = check_mark(p + np.array([0.0, 0.015, 0]), size=0.14, width=5)
            ck.set_stroke(BG, width=10, background=True)
            glow = Circle(radius=0.15, color=GOOD, stroke_width=3).move_to(p).set_stroke(opacity=0)
            base = glow.copy()

            def glow_fn(m, a, base=base):
                m.become(base.copy().scale(1 + 1.2 * a).set_stroke(opacity=(1 - a) if a > 0 else 0))
            checks.append((ck, glow))
            ck_anims.append(AnimationGroup(Create(ck), UpdateFromAlphaFunc(glow, glow_fn)))
        t_ck = M("hand") + 0.55
        spacing, dur = 0.22, 0.4
        lag = spacing / dur
        self.at(t_ck, LaggedStart(*ck_anims, lag_ratio=lag), run_time=dur * (1 + (len(ck_anims) - 1) * lag))
        self.remove(*[g for _, g in checks])
        # final pause: everything fades out (the web and the counter fade by themselves)
        rest = VGroup(parts, dots_lab, sticks_lab, known_grp, stack, tag, board, ghost, *[c for c, _ in checks])
        self.at(M("p6_end") + 0.1, FadeOut(rest), run_time=M("end") - M("p6_end") - 0.18)

