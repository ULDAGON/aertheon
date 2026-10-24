"""Shared style + timeline-driven scene base for every scene.

AUDIO IS THE MASTER. The narration is rendered first (tools/timeline.py), which writes
timeline/<SceneId>.json with the exact time of every sentence, paragraph and {#bookmark}.
Scenes render SILENT video that is frame-exactly as long as the scene's audio; audio is muxed
in at the very end. Never call add_sound().

Usage in a scene file (scenes/s03_triangle.py):

    from common import *

    class S03_Triangle(TimedScene):          # class name == scene id in script/script.json
        def construct(self):
            dot = pt(ORIGIN, BLUE_P)
            self.until("p1", GrowFromCenter(dot))      # animate from now until paragraph 1 starts
            self.until("tri", Create(tri))             # ... until the {#tri} bookmark is spoken
            self.play(Indicate(dot), run_time=0.8)     # plain play() is fine too; the clock tracks it
            self.at("circle", Create(circ), run_time=1.2)  # wait until {#circle}, THEN animate 1.2 s
            # when construct() returns, the scene is padded to the exact audio length.

Timing API (all times in seconds from scene start; names = bookmark names, "p3" = start of paragraph 3,
"p3_end" = end of its last sentence, "p3s2" = start of sentence 2 of paragraph 3, "end" = scene duration):
    self.t(name)          -> float time of a mark
    self.now              -> current frame-exact time
    self.until(m, *anims, **kw)   -> play anims so that they END exactly at mark m (or just wait if no anims)
    self.at(m, *anims, run_time=..)-> wait until mark m, then play anims (they START at m)
    self.left(m)          -> seconds from now until mark m (use to size run_times)
Lateness (an animation that could not start/end in time because earlier animations ran long) is recorded
and reported by the QA tool. Overrunning the scene's audio is an error.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
TIMELINE = ROOT / "timeline"
QA_DIR = ROOT / "out" / "qa"

# ---------------------------------------------------------------- look
BG = "#0E1116"          # near-black blue
INK = "#ECEFF4"         # main text / lines
DIM = "#8A93A3"         # secondary text
FAINT = "#3A4150"       # grid / guides
UNIT_COLOR = "#D5DCE6"  # anything that *is* the forbidden distance 1 (sticks, rulers, unit circles); neutral so paint pops
ACCENT = "#FFD166"      # highlight: scoreboard window, key numbers, emphasis
BAD = "#FF5C5C"         # rule broken / contradiction (never used as paint)
GOOD = "#6BCB77"        # check marks

# The seven paint colours of the plane (index 0..6). Pink instead of red so paint never looks like BAD.
PALETTE = [
    "#4EA8F5",  # 0 blue
    "#F2C14E",  # 1 yellow
    "#EE6BAE",  # 2 pink
    "#6BCB77",  # 3 green
    "#B084F5",  # 4 purple
    "#F29E4C",  # 5 orange
    "#43D9C8",  # 6 teal
]
BLUE_P, YELLOW_P, PINK_P, GREEN_P, PURPLE_P, ORANGE_P, TEAL_P = PALETTE

FONT = "Avenir Next"     # prose / titles
NUM_FONT = "Palatino"    # numbers and math-ish labels. No LaTeX installed: use Text, never MathTex/Tex.

UNIT = 2.0  # manim units per "one unit" of the problem (scenes may use their own scale if they say so)

config.background_color = BG


def T(s, size=40, color=INK, weight=NORMAL, font=FONT, **kw):
    """Prose text."""
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def N(s, size=48, color=INK, slant=NORMAL, **kw):
    """Number / math-style label (Palatino)."""
    return Text(str(s), font=NUM_FONT, font_size=size, color=color, slant=slant, **kw)


def pt(pos, color=INK, r=0.09):
    """A point of the plane: filled dot with a thin dark rim so it reads on any colour."""
    d = Dot(pos, radius=r, color=color)
    d.set_stroke(BG, width=2, background=True)
    return d


def ring(pos, r=0.09, color=INK):
    """An uncoloured (not yet painted) point: hollow ring."""
    return Circle(radius=r, color=color, stroke_width=2.5).move_to(pos).set_fill(BG, 1)


def stick(a, b, color=UNIT_COLOR, width=4):
    """A unit-distance edge between two positions/mobjects."""
    a = a.get_center() if isinstance(a, Mobject) else a
    b = b.get_center() if isinstance(b, Mobject) else b
    return Line(a, b, color=color, stroke_width=width)


def cross_mark(pos, size=0.22, color=BAD, width=6):
    """A drawn ✗ (fonts lack a nice glyph)."""
    return VGroup(Line(pos + size * (UL), pos + size * (DR), color=color, stroke_width=width),
                  Line(pos + size * (UR), pos + size * (DL), color=color, stroke_width=width))


def check_mark(pos, size=0.22, color=GOOD, width=6):
    """A drawn ✓."""
    p = np.array(pos)
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [p + size * np.array([-1, 0.05, 0]), p + size * np.array([-0.35, -0.6, 0]), p + size * np.array([1, 0.75, 0])])


def caption(s, size=30, color=DIM):
    """Small caption pinned to the bottom edge."""
    return T(s, size=size, color=color).to_edge(DOWN, buff=0.45)


# ---------------------------------------------------------------- timeline-driven scene
class TimedScene(MovingCameraScene):
    """Silent scene whose clock is frame-exact and whose length equals its narration audio."""

    SCENE_ID = None  # defaults to the class name

    def setup(self):
        super().setup()
        sid = self.SCENE_ID or type(self).__name__
        path = TIMELINE / f"{sid}.json"
        if not path.exists():
            raise FileNotFoundError(f"{path} missing - run tools/timeline.py first")
        self.tl = json.loads(path.read_text())
        self.marks = dict(self.tl["marks"])
        self.marks["end"] = self.tl["duration"]
        self.duration = None  # set by manim during plays; we don't rely on it outside _count
        self._fps = config["frame_rate"]
        self._frames = 0
        self._late = []   # (mark, seconds late, what)

    # --- clock -------------------------------------------------------------------------
    @property
    def now(self):
        return self._frames / self._fps

    def _count(self):
        """Frames manim just wrote for the last play (mirrors manim's own arithmetic)."""
        dur = self.duration
        if self.animations and self.is_current_animation_frozen_frame():
            return int(dur / (1 / self._fps))
        return len(np.arange(0, dur, 1 / self._fps))

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        self._frames += self._count()

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None, frozen_frame=None):
        if duration <= 0:
            return
        super().wait(duration, stop_condition=stop_condition, frozen_frame=frozen_frame)

    def _rt(self, n_frames):
        # run_time that makes manim write exactly n frames (np.arange(0, (n-.5)/fps, 1/fps) has n items)
        return (n_frames - 0.5) / self._fps

    def _wait_frames(self, n):
        """Wait exactly n frames. Static waits are written as int(d*fps) frozen frames, animated
        waits as len(arange(0, d, 1/fps)) frames, so pick the run_time for the path manim will take."""
        if n <= 0:
            return
        static = not (self.always_update_mobjects or self.updaters or any(
            m.has_time_based_updater() for m in self.get_mobject_family_members()))
        before = self._frames
        self.wait((n + 0.5) / self._fps if static else (n - 0.5) / self._fps)
        if self._frames - before != n:
            print(f"[TimedScene] frame bookkeeping: wanted {n}, wrote {self._frames - before}", file=sys.stderr)

    # --- marks -------------------------------------------------------------------------
    def t(self, mark):
        if isinstance(mark, (int, float)):
            return float(mark)
        if mark not in self.marks:
            raise KeyError(f"unknown mark {mark!r}; known: {sorted(self.marks)}")
        return self.marks[mark]

    def left(self, mark):
        return self.t(mark) - self.now

    def _frames_until(self, mark):
        return round(self.t(mark) * self._fps) - self._frames

    def until(self, mark, *anims, min_run_time=0.2, **kwargs):
        """Play `anims` so they end exactly at `mark` (or wait until it if no anims)."""
        n = self._frames_until(mark)
        if not anims:
            if n > 0:
                self._wait_frames(n)
            elif n < -1:
                self._late.append((str(mark), -n / self._fps, "wait"))
            return
        if n < round(min_run_time * self._fps):
            self._late.append((str(mark), (round(min_run_time * self._fps) - n) / self._fps, "until"))
            n = round(min_run_time * self._fps)
        kwargs["run_time"] = self._rt(n)
        self.play(*anims, **kwargs)

    def at(self, mark, *anims, run_time=1.0, **kwargs):
        """Wait until `mark`, then play `anims` for run_time seconds (they start at the mark)."""
        n = self._frames_until(mark)
        if n > 0:
            self._wait_frames(n)
        elif n < -1:
            self._late.append((str(mark), -n / self._fps, "at"))
        if anims:
            self.play(*anims, run_time=self._rt(max(1, round(run_time * self._fps))), **kwargs)

    # --- end of scene ------------------------------------------------------------------
    def tear_down(self):
        total = round(self.tl["duration"] * self._fps)
        n = total - self._frames
        over = -n / self._fps
        if n > 0:
            self._wait_frames(n)
        report = {
            "scene": self.tl["scene"], "fps": self._fps, "frames": self._frames,
            "target_frames": total, "overrun_s": max(0.0, over),
            "late": [{"mark": m, "late_s": round(s, 3), "kind": k} for m, s, k in self._late],
        }
        QA_DIR.mkdir(parents=True, exist_ok=True)
        (QA_DIR / f"{self.tl['scene']}.timing.{self._fps}.json").write_text(json.dumps(report, indent=1))
        if over > 1.5 / self._fps:
            msg = f"[TimedScene] {self.tl['scene']} OVERRAN its audio by {over:.2f}s - shorten animations"
            print(msg, file=sys.stderr)
            if os.environ.get("HN_STRICT", "1") == "1":
                raise RuntimeError(msg)
        for m, s, k in self._late:
            print(f"[TimedScene] late by {s:.2f}s at mark {m!r} ({k})", file=sys.stderr)
        super().tear_down()


# ---------------------------------------------------------------- recurring motif
class BoundsBar(VGroup):
    """The running scoreboard "colors needed":  1 2 3 4 5 6 7 8 …

    Ruled-out numbers go faint + get a strike; the still-possible range sits inside a rounded
    ACCENT box. The window narrows over the video: [1,∞) -> [3,∞) -> [4,∞) -> [4,7] -> [5,7].

        bar = BoundsBar(lo=3).to_edge(DOWN)
        self.play(FadeIn(bar))
        self.until("four", bar.set_bounds(4))       # returns an Animation
    """

    TOKENS = ["1", "2", "3", "4", "5", "6", "7", "8", "…"]

    def __init__(self, lo=1, hi=None, size=44, spacing=0.78, label=True, **kw):
        super().__init__(**kw)
        self.cells = VGroup(*[N(t, size) for t in self.TOKENS])
        for i, c in enumerate(self.cells):
            c.move_to(RIGHT * spacing * i)
        self.cells.center()
        self.strikes = VGroup(*[
            Line(c.get_corner(DL) + DL * 0.06, c.get_corner(UR) + UR * 0.06, color=DIM, stroke_width=3)
            for c in self.cells
        ])
        self.box = RoundedRectangle(corner_radius=0.18, color=ACCENT, stroke_width=3)
        self.add(self.cells, self.strikes, self.box)
        if label:
            self.title = T("colors needed", 30, DIM).next_to(self.cells, UP, buff=0.3)
            self.add(self.title)
        self.lo, self.hi = lo, hi
        self._apply(lo, hi)

    def _is_more(self, i):
        return self.TOKENS[i] == "…"  # "…" just dims; a strike on it reads as a stray dash

    def _possible(self, i, lo, hi):
        n = i + 1  # index 8 is "…" (anything above 8)
        return n >= lo and (hi is None or n <= hi)

    def _target_box(self, lo, hi):
        idx = [i for i in range(len(self.cells)) if self._possible(i, lo, hi)]
        grp = VGroup(*[self.cells[i] for i in idx])
        b = RoundedRectangle(corner_radius=0.18, color=ACCENT, stroke_width=3,
                             width=grp.width + 0.45, height=self.cells.height + 0.4)
        return b.move_to([grp.get_center()[0], self.cells.get_center()[1], 0])

    def _apply(self, lo, hi):
        for i, (c, s) in enumerate(zip(self.cells, self.strikes)):
            ok = self._possible(i, lo, hi)
            c.set_color(INK if ok else FAINT)
            s.set_stroke(opacity=0 if ok or self._is_more(i) else 0.9)
        self.box.become(self._target_box(lo, hi))

    def set_bounds(self, lo, hi=None, **anim_kw):
        """Animation that moves the window to [lo, hi] (hi=None means unbounded)."""
        self.lo, self.hi = lo, hi
        anims = [Transform(self.box, self._target_box(lo, hi))]
        for i, (c, s) in enumerate(zip(self.cells, self.strikes)):
            ok = self._possible(i, lo, hi)
            anims.append(c.animate.set_color(INK if ok else FAINT))
            anims.append(s.animate.set_stroke(opacity=0 if ok or self._is_more(i) else 0.9))
        return AnimationGroup(*anims, **anim_kw)
