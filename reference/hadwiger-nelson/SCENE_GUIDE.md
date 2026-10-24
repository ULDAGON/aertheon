# Hadwiger–Nelson explainer v2: scene guide

A 10-minute educational explainer (3Blue1Brown spirit) built with **Manim Community v0.21** (`.venv/bin/manim`).
Local Kokoro TTS narrates it. The audience is curious non-mathematicians.

## Why the engine works this way (read this)
Two failures this guide is built to prevent:
1. Parts of a first draft had **animation with no voice**. One cause was a Manim bug: `add_sound()` is silently dropped after a
   cached animation. The other cause was scenes animating long after their narration ended.
2. The narration was a wall of sentences with **no breathing room**.

This version fixes both by design:
- **Audio is the master clock.** `tools/timeline.py` renders every sentence separately and puts natural pauses between
  them (0.55 s between sentences, and 0.55–1.5 s between paragraphs as the script says). It writes the exact time of every
  paragraph, sentence and `{#bookmark}` to `timeline/<SceneId>.json`.
- **Scenes are silent video, frame-exact to the audio.** `TimedScene` keeps a frame-exact clock. You schedule animations
  *against the narration marks*, and the scene is padded to exactly the audio length. Audio is muxed in at the end.
  **Never call `add_sound()`.**

## Files
- `script/script.json`: the script. Your scene is `scenes[i]` with your id. Each paragraph has `sentences` (with
  `{#bookmark}` markers), a `visual` storyboard, and `pause_after`. **The storyboard is your spec.** Improve on it where it
  helps clarity, but never contradict the narration.
- `timeline/<SceneId>.json`: the times of `marks` (bookmarks, `p1`, `p1_end`, `p2s3`, …, `end`), plus paragraphs and
  sentences with word-level times. Read it, because it tells you how much time each beat really has.
- `common.py`: style tokens, helpers (`T`, `N`, `pt`, `ring`, `stick`, `cross_mark`, `check_mark`, `BoundsBar`) and
  **`TimedScene`**. Read the docstring fully.
- `geom.py`: verified geometry. Use it, don't re-derive it: `triangle`, `diamond`, `moser_spindle`, the hexagon
  7-coloring (`hex_cells`, `hex_color`, `hex_vertices`, `HEX_SIDE`), `line_color`, `unit_web` (a genuine unit-distance
  graph, for illustration), and `to_scene`.
- Don't edit `common.py`, `geom.py`, the `tools/` files, the script or the audio. Put scene-local helpers in your own file. If a
  shared change is truly needed, say so in your report.

## Timing API (`TimedScene`)
```python
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *
from geom import *

class S04_Spindle(TimedScene):            # class name == scene id
    def construct(self):
        self.until("p1", FadeIn(title))               # ends exactly when paragraph 1 starts speaking
        self.until("glue", Create(diamond_mob))       # ends exactly on the word after {#glue}
        self.at("tip", Indicate(tip), run_time=0.8)   # waits for {#tip}, then plays 0.8 s
        self.play(FadeOut(x), run_time=0.4)           # plain play()/wait() are fine; the clock tracks them
        self.left("p3")                               # seconds from now until p3 (use it to size run_times)
```
- `until(mark, *anims)` = the animation **ends** on the mark. Use it for things that must be complete when a word is said.
  `at(mark, *anims, run_time)` = the animation **starts** on the mark. Use it for reactions to a word ("…and color it {#blue} blue").
- If earlier animations run long, a later mark comes "late". QA reports this as an error when it is more than 0.25 s late.
  Overrunning the scene's audio makes the render fail. Budget your run_times with `self.left()`.

## Pacing rules (QA-enforced; see `tools/qa.py`)
1. **No animation without voice.** Motion during a pause is fine only as a short payoff (the pause after a paragraph is
   0.55–1.5 s). QA fails any silent stretch with motion > 1.6 s.
2. **No dead picture while talking.** Something meaningful should change at least every ~5 s of narration (QA warns).
   Use progressive builds, highlights, camera moves, labels appearing and so on. Don't add random jiggle.
3. **Every bookmark gets a visible change** within [-0.3, +1.0] s (QA warns). The words and the picture must agree.
4. **Scene boundaries.** Start with a nearly empty background. The first element may fade in during the ~0.3 s lead-in.
   **End with everything faded out** during the final pause (`self.until("end", FadeOut(...))` or start the fade at
   `p<last>_end`). The next scene starts from the same empty background, which makes cuts seamless.
5. Keep motion calm and purposeful: 3Blue1Brown pacing, with ease-in-out, and no flashy transitions, strobing or shaking except
   one small "contradiction" shake.

## Look
- Background `BG`, text `INK`/`DIM`. Paint = `PALETTE` (blue, yellow, pink, green, purple, orange, teal). **Unit sticks and unit
  circles use `UNIT_COLOR`** (neutral). **`BAD` red is only for rule-breaking**, and `GOOD` green only for check marks. `ACCENT`
  gold is for emphasis and the scoreboard window.
- An unpainted point is `ring()`, and a painted point is `pt(pos, color)`. A pair exactly 1 apart is `stick()`. Label a stick `N("1")` only
  when it teaches something.
- Scoreboard: `BoundsBar(lo, hi)`, which keeps one consistent look across scenes. Its state narrows over the video as the script says.
- Text: short labels and titles only, never whole narration sentences. Minimum font size is about 24 (it must read at 480p).
  Fonts: `T()` is Avenir Next for prose and `N()` is Palatino for numbers. **No LaTeX** (not installed). Unicode `≤ ≥ χ √` in `Text` is fine.
- Safe area: about ±6.6 × ±3.6 manim units. Nothing may be clipped or overlap unintentionally.
- Geometry must be **faithful**: unit sticks are equal length, the spindle tips are really 1 apart, and so on. Viewers pause.

## Workflow
```bash
cd <videos>/<slug>/src
tools/render.sh <SceneId> l     # 480p15: silent render -> preview with voice -> QA report + images
```
The QA step prints a report and writes three images you **must look at** with the Read tool:
- `out/qa/<Scene>.timeline.png`: the narration waveform (blue), picture motion (orange; red = motion while silent),
  sentences, bookmarks and flagged spans (dark red background).
- `out/qa/<Scene>.marks.png`: one frame 0.9 s after each bookmark, labeled with the words just spoken. Check that the picture
  shows what those words say.
- `out/qa/<Scene>.sheet.png`: a frame every 2.5 s, labeled with the words being spoken.

Iterate until there are **zero ERRORs**. Fix every WARN, or justify it in your report. The scene must also *look* good:
clear, uncluttered, readable, and beautiful. Don't render at `h`, because the final build does that for all scenes at once. Keep heavy
scenes efficient: batch many similar mobjects into one VMobject, and don't use thousands of separate animations.
Only one process may render a given scene at a time, because each scene has one media folder. Reviewers must not re-render. They extract
extra frames from `out/preview/<SceneId>_480p15.mp4` with ffmpeg into their own folder `out/review/<SceneId>_<name>/`.

Final report (short): the file, class, duration, QA result (paste the report's first lines), what the scene shows, known weaknesses,
and any shared-helper requests.
