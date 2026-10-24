# {{TITLE}}: scene guide

An AERTHEON explainer (3Blue1Brown spirit) built with **Manim Community v0.21** (`.venv/bin/manim`).
Local Kokoro TTS narrates it. The audience is curious non-experts. Channel style: `{{ENGINE_DIR}}/STYLE.md`.
Gold-standard example of finished scenes: `{{ENGINE_DIR}}/reference/hadwiger-nelson/scenes/` and `{{ENGINE_DIR}}/reference/riemann-hypothesis/scenes/` (read one or two before you start).

## Why the engine works this way (read this)
Two failures this engine is built to prevent:
1. Parts of it had **animation with no voice**. One cause was a Manim bug: `add_sound()` is silently dropped after a
   cached animation. The other cause was scenes animating long after their narration ended.
2. The narration was a wall of sentences with **no breathing room**.

The engine fixes both by design:
- **Audio is the master clock.** `tools/timeline.py` renders every sentence separately and puts natural pauses between
  them (0.55 s between sentences, and 0.55–1.5 s between paragraphs as the script says). It writes the exact time of every
  paragraph, sentence and `{#bookmark}` to `timeline/<SceneId>.json`.
- **Scenes are silent video, frame-exact to the audio.** `TimedScene` keeps a frame-exact clock. You schedule animations
  *against the narration marks*, and the scene is padded to exactly the audio length. Audio is muxed in at the end.
  **Never call `add_sound()`.**

## Files
- `script/script.json`: the script. Your scene is `scenes[i]` with your id. Each paragraph has `sentences` (with
  `{#bookmark}` markers), a `visual` storyboard, and `pause_after`. **The storyboard is your spec.** Improve on it where it
  helps clarity, and keep the picture in agreement with the narration at every moment.
- `timeline/<SceneId>.json`: the times of `marks` (bookmarks, `p1`, `p1_end`, `p2s3`, …, `end`), plus paragraphs and
  sentences with word-level times. Read it, because it tells you how much time each beat really has. Schema (seconds):
  `{scene, title, duration, marks: {name: sec}, paragraphs: [{id: "p1", start, end, …}], sentences: [{id: "p1s1", start,
  end, text, words: [{w, s, e}]}]}`. Word keys are `w`/`s`/`e`. Never index words by position (a re-voice breaks it); use
  `self.word()`.
- `common.py`: style tokens, helpers (`T`, `N`, `pt`, `ring`, `edge`, `cross_mark`, `check_mark`, `caption`) and
  **`TimedScene`**. Read the docstring fully.
- `topic.py`: verified, topic-specific data and constructors (geometry, datasets, recurring motif classes). Use it rather
  than re-deriving anything it offers.
- `common.py`, `topic.py`, `tools/`, the script and the audio are shared and frozen. Put scene-local helpers in your own
  file. If a shared change is truly needed, list it under `shared_requests` in your report (file, change, reason); the
  orchestrator applies it once and re-renders every scene.

## Timing API (`TimedScene`)
```python
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import *
from topic import *

class S04_Example(TimedScene):            # class name == scene id
    def construct(self):
        self.until("p1", FadeIn(title))               # ends exactly when paragraph 1 starts speaking
        self.until("glue", Create(shape))             # ends exactly on the word after {#glue}
        self.at("tip", Indicate(tip), run_time=0.8)   # waits for {#tip}, then plays 0.8 s
        self.play(FadeOut(x), run_time=0.4)           # plain play()/wait() are fine; the clock tracks them
        self.left("p3")                               # seconds from now until p3 (use it to size run_times)
        t = self.word("p2s1", "triangle")             # start of that word (end=True: its end; nth=1: 2nd occurrence)
        self.at(t, Create(tri), run_time=0.8)         # at()/until() take a mark name or float seconds
```
- `word(sentence_id, word, nth=0, end=False)`: case- and punctuation-insensitive, 0-based `nth`; a miss raises with the
  sentence's word list. Prefer named marks and `word()` over typed float seconds (typed floats drift and come late at `h`).
- `until(mark, *anims)` = the animation **ends** on the mark. Use it for things that must be complete when a word is said.
  `at(mark, *anims, run_time)` = the animation **starts** on the mark. Use it for reactions to a word ("…and color it {#blue} blue").
- If earlier animations run long, a later mark comes "late". QA reports this as an error when it is more than 0.25 s late
  (at `h`, < 0.15 s late on a float mark is frame rounding; named marks and `word()` avoid it).
  Overrunning the scene's audio makes the render fail. Budget your run_times with `self.left()`.

## Pacing rules (QA-enforced; see `tools/qa.py`)
1. **No animation without voice.** Motion during a pause is fine only as a short payoff (the pause after a paragraph is
   0.55–1.5 s). QA fails any silent stretch with motion > 1.6 s.
2. **No dead picture while talking.** Something meaningful should change at least every ~5 s of narration (QA warns).
   Use progressive builds, highlights, camera moves, labels appearing and so on. Motion always carries meaning; no random jiggle.
3. **Every bookmark gets a visible change** within [-0.3, +1.0] s (QA warns). The words and the picture must agree.
4. **Scene boundaries.** Start with a nearly empty background. The first element may fade in during the ~0.3 s lead-in.
   **End with everything faded out** during the final pause (`self.until("end", FadeOut(...))` or start the fade at
   `p<last>_end`). The next scene starts from the same empty background, which makes cuts seamless.
5. Keep motion calm and purposeful: 3Blue1Brown pacing, with ease-in-out. Transitions are quiet fades and transforms;
   the one allowed "effect" is a small shake for a contradiction.

## Look
- Background `BG`, text `INK`/`DIM`, guides `FAINT`. Content colours = `PALETTE` (blue, yellow, pink, green, purple, orange,
  teal, always in that order). Structural lines use `NEUTRAL`. **`BAD` red is only for something wrong/contradicted**, and
  `GOOD` green only for check marks. `ACCENT` gold is for emphasis, key numbers and the recurring motif's highlight.
- Text: short labels and titles only, never whole narration sentences. Minimum font size is about 24 (it must read at 480p).
  Fonts: `T()` is Avenir Next for prose and `N()` is Palatino for numbers. **No LaTeX** (not installed): use `Text`, never
  `MathTex`/`Tex`. Unicode `≤ ≥ χ √ π ∑ ∞` in `Text` is fine.
- Safe area: about ±6.6 × ±3.6 manim units. Nothing may be clipped or overlap unintentionally.
- Content must be **faithful**: geometry exact, data real, counts right, and anything claimed valid really is valid. Viewers pause.
- If the recurring motif (see below) is on screen, keep the camera still and "zoom" by scaling the content group instead,
  so the motif keeps its fixed home.

## This video
<!-- Filled in per video by the orchestrator after the script is final. Keep it short and specific. -->
- **Recurring motif:** {{MOTIF: what it is, its class in topic.py, its fixed home on screen, its state progression by scene}}
- **Colour semantics for this topic:** {{what PALETTE / NEUTRAL / ACCENT mean here}}
- **topic.py contents:** {{list of constructors and what they guarantee}}
- **Scale:** {{manim units per problem unit, if relevant}}

## Workflow
```bash
cd {{VIDEO_DIR}}
tools/render.sh <SceneId> l     # 480p15: silent render -> preview with voice -> QA report + images
```
The QA step prints a report and writes three images you **must look at** with the Read tool:
- `out/qa/<Scene>.timeline.png`: the narration waveform (blue), picture motion (orange; red = motion while silent),
  sentences, bookmarks and flagged spans (dark red background).
- `out/qa/<Scene>.marks.png`: one frame 0.9 s after each bookmark, labeled with the words just spoken. Check that the picture
  shows what those words say.
- `out/qa/<Scene>.sheet.png`: a frame every 2.5 s, labeled with the words being spoken.

Iterate until there are **zero ERRORs**. Fix every WARN, or justify it in your report. The scene must also *look* good:
clear, uncluttered, readable, and beautiful. Render only at `l`; the final build renders every scene at `h` at once. Keep heavy
scenes efficient: batch many similar mobjects into one VMobject, and keep animation counts in the dozens, not thousands.
Only one process may render a given scene at a time, because each scene has one media folder. Reviewers never re-render: they
extract extra frames from `out/preview/<SceneId>_480p15.mp4` with ffmpeg into their own folder `out/review/<SceneId>_<name>/`.
Other scratch goes to `out/_scratch/<your name>/`. Never delete (no `rm`): use fresh file/dir names and `ffmpeg -y`, never delete caches.
- **Stale or crashing cache:** `NOCACHE=1 tools/render.sh <SceneId> l` passes `--disable_caching`. Scenes driven by
  updaters, `ValueTracker`s, `always_redraw` or the scene clock can replay stale partial movies; a `rate_func`/updater closing
  over numpy/scipy functions crashes the hasher (`TypeError: <cyfunction …> is not a Python function`). For those, put
  `config.disable_caching = True` at module top.

## Manim pitfalls
- Build `.animate` animations only after the previous `play` finished (they snapshot the state when created).
- FadeIn and FadeOut of the same object in one `play` leaves it invisible; FadeOut of an already faded object re-adds it.
- `Indicate` restores the start colour. Set `z_index` before animating. `VGroup.get_stroke_width()` returns 4, not the
  children's width. In `LaggedStart`, a lower `lag_ratio` means **more** overlap.
- `ReplacementTransform` between number strings garbles them: use `FadeTransform`.

## What reviewers flag most (avoid it the first time)
- The payoff image is never held still: hold it complete ≥ 0.8–1.0 s; intermediate readouts ≥ 0.4 s.
- Picture leads or lags the word: resets go in the pause *before* a paragraph; labels and counts land when their build
  completes; names appear on their spoken word.
- Several big moves at once: one focal area moves at a time. In a swap, old text leaves in the first 40 %
  (`rate_func=squish_rate_func(smooth, 0, 0.4)`) and new content arrives in the rest (`squish_rate_func(smooth, 0.4, 1)`).
- Two nearly coincident curves merge: draw the base as a wide low-opacity band (stroke 9–12, opacity 0.3–0.45) under a
  thin solid curve (~2.5–3) with a label; a dark rim does not read at 480p.
- Effective text size after any scaling stays ≥ 24; a motif part with a narrated action is ≥ 0.4 units.
- Safe area: measure the top edge, not the centre (a size-44 title at y = 3.5 reaches 3.72); corners with `buff` ≥ 0.5.
- Honesty: `BAD` never marks a region that is still possible; illustrations on real axes are tagged
  "illustration · not to scale"; quotation marks only for verbatim quotes; never reuse a reserved colour for something unrelated.
- Endings: fades of ≈ 0.6–0.9 s with the motif last; start dimming a bright full-frame image during the last words.

Final report (short): the file, class, duration, QA result (paste the report's first lines), what the scene shows, known weaknesses,
and any `shared_requests` (file, change, reason).
