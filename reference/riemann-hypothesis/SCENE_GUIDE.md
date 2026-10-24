# The Riemann Hypothesis: scene guide

An AERTHEON explainer (3Blue1Brown spirit) built with **Manim Community v0.21** (`.venv/bin/manim`).
Local Kokoro TTS narrates it. The audience is curious non-experts. Channel style: `STYLE.md` in the engine.
Gold-standard example of finished scenes: `../hadwiger-nelson/scenes/` (read one or two before you start).

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
  sentences with word-level times. Read it, because it tells you how much time each beat really has.
- `common.py`: style tokens, helpers (`T`, `N`, `pt`, `ring`, `edge`, `cross_mark`, `check_mark`, `caption`) and
  **`TimedScene`**. Read the docstring fully.
- `topic.py`: verified, topic-specific data and constructors (geometry, datasets, recurring motif classes). Use it rather
  than re-deriving anything it offers.
- `common.py`, `topic.py`, `tools/`, the script and the audio are shared and frozen. Put scene-local helpers in your own
  file. If a shared change is truly needed, say so in your report.

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
```
- `until(mark, *anims)` = the animation **ends** on the mark. Use it for things that must be complete when a word is said.
  `at(mark, *anims, run_time)` = the animation **starts** on the mark. Use it for reactions to a word ("…and color it {#blue} blue").
- If earlier animations run long, a later mark comes "late". QA reports this as an error when it is more than 0.25 s late.
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
- **Recurring motif: the error dial** (`ErrorDial` in `topic.py`), fixed home bottom centre: ruler x −2.5..2.5 at y −3.2,
  labels 0 ½ 1, captions left/right, one row above the ruler: `coin flips` (coin) (pin) `Riemann?` (✓ `best possible`).
  Its reading is the power of x in the size of the prime error. State by scene:
  S03 builds it (P5: ruler, ticks, labels, captions, then 'never grows'/'all the digits' labels and the coin; P6: window ½..1
  with 'proven range', pin). Those three extra labels are S03-only. S04, S05: no dial. S06, S07, S08: `ErrorDial()` (window,
  coin, pin), fading in with the scene. S08 P4 adds the check (`dial.check`, `dial.check_label`). S09, S10, S11:
  `ErrorDial(best=True)`. The window never narrows, except S11 P3's dashed "if Riemann is right" glow, which S11 P4 undoes.
  Hypothetical readings use `dial.marker(v)` (BAD). While the dial is on screen: the camera never moves (scale content
  groups instead) and all other content stays above y = −2.6 (`DIAL_TOP`). Every scene fades the dial out last.
- **The critical strip** always comes from `strip_group(StripMap, n_zeros)` with one of the fixed layouts:
  `DIAL_ALIGNED` (S06 from P2, S10; real parts 0..1 sit exactly above the dial's 0..1; its floor is y −2.3, not the script's
  −2.5, so its floor labels clear the dial row), `INSET` / `INSET_240` (S07, S08, S11; right edge), `EVIDENCE` (S09, left third).
  Zeros are INK dots with a BG rim on the ACCENT line at real part ½; heights are `ZEROS` (exact).
- **Colour semantics:** primes, prime tiles and the prime staircase `BLUE_P` (`PRIME_COLOR`). Gauss's curve li, Riemann's
  sharpened curve R and the rebuilt curve `TEAL_P` (`CURVE_COLOR`). The critical line, key numbers, the dial window, coin and pin:
  `ACCENT`. Zero k's wave: `WAVE_COLORS[k-1]` = pink, green, purple, orange, blue (wave 5 is blue everywhere, also in S07 P4,
  where the script says green). Hypothetical zeros: hollow `BAD` dashed rings, always tagged 'hypothetical' or
  'illustration', always with their mirror twin. `GOOD` only for check marks. `NEUTRAL` for axes and rulers.
- **topic.py** (read its docstring): exact primes and staircase, `li`, `R`, the exact recipe (`base_curve`, `zero_wave`,
  `rebuild`, `rogue_wave`, `envelope`) cached on `LIN_X` (2..100) and `LOG_X` (10..10⁶); morph curves by building every stage
  on the same grid so `Transform` matches point for point. `zeta_np` (vectorized ζ, verified against mpmath),
  `spiral_partial_sums`, `zeta_line_path`, `domain_image` (hue = direction of ζ's output, ~2 s per 1M pixels),
  `random_walks`, `block_counts`. Every number the script puts on screen is verified by `python topic.py`; take values from
  these functions, never type them from memory.
- **Scale:** each scene sets its own axes (the storyboard gives ranges). Large staircases: `staircase_points(xmax)` samples
  3,000 exact points above x = 2,000 so the VMobject stays light.
- **Honesty tags stay on screen** wherever the storyboard asks for them ('hypothetical', 'illustration', 'if the Riemann
  Hypothesis is true', 'preprint', 'enlarged', 'log scale').

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
clear, uncluttered, readable, and beautiful. Render only at `l`; the final build renders every scene at `h` at once. Keep heavy
scenes efficient: batch many similar mobjects into one VMobject, and keep animation counts in the dozens, not thousands.
Only one process may render a given scene at a time, because each scene has one media folder. Reviewers never re-render: they
extract extra frames from `out/preview/<SceneId>_480p15.mp4` with ffmpeg into their own folder `out/review/<SceneId>_<name>/`.

Final report (short): the file, class, duration, QA result (paste the report's first lines), what the scene shows, known weaknesses,
and any shared-helper requests.

