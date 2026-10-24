# AERTHEON engine

An engine for calm, 3Blue1Brown-style explainers for non-experts, made with Claude Code: animated with Manim Community and
narrated by local Kokoro TTS. It was built for AERTHEON, which makes educational videos on mathematics, computer science and
engineering. The user names a topic; you deliver the finished video, three thumbnails, three titles and the description **in exactly the established
style**, without asking them to re-explain it.

**New video request → invoke the `aertheon-video` skill** (it runs `PIPELINE.md` step by step). Asking for a video in this
repository is the opt-in to the multi-agent workflows it runs (`.claude/workflows/aertheon-script.js`,
`.claude/workflows/aertheon-scenes.js`): tell the user the expected time and cost up front (PIPELINE.md), then run them
without asking again.

## Paths
- `$E`: this engine, the repository root (wherever it is cloned).
- `$P`: one video's folder, `<videos>/<slug>/`. `<videos>` is `$AERTHEON_VIDEOS` if it is set, else the `videos/` folder
  next to `$E`. `$E/new_video.sh` creates `$P` and prints `$V`.
- `$V`: `$P/src`, the working folder. All commands run here.

## Where things go
- **This directory holds only the engine.** Never write video work here: no scripts, audio, renders, scratch files or notes.
- **Every video lives in `$P`.** Its top level holds only what the user opens: `<name>.mp4` (the only copy), `thumbnails/`
  (three PNGs) and `youtube.md` (three titles + description). Everything else lives in `src/`: script, research, audio,
  timeline, scenes, tools, and `out/` with share copy, subtitles, QA and scratch.
- Never scaffold, smoke-test, render or run `timeline.py`/`build.sh` inside this directory (`template/`, `reference/`
  included); engine self-tests go into a video folder or the session scratchpad.
- Never delete files (no `rm`): use fresh names, `ffmpeg -y`, `NOCACHE=1`, and `mv` leftovers into `$V/out/_scratch/`.
  A stray artifact in the engine would stay, so do not create one.
- When a video is done, `git status` in `$E` is clean (the shared environments and `__pycache__` are git-ignored).

## Layout
- `PIPELINE.md`: the ten steps, commands and completion criteria. The `aertheon-video` skill points here.
- `STYLE.md`: audience, tone, story arc, picture and sound style. Read it before writing a brief or judging any output.
- `SCRIPT_FORMAT.md`: the `script.json` spec the script agents write against.
- `YOUTUBE.md`: the three titles and the description (five parts, the fixed About AERTHEON paragraph, sources as links).
- `THUMBNAIL.md` + `branding/`: the pastel thumbnail style (three per video), brand tokens (`brand.py`), channel banner, profile picture and README header.
- `template/`: copied into every new video's `src/` by `new_video.sh` (`youtube.md` goes to the top level): `common.py` (style tokens, `TimedScene`), `tools/`
  (timeline, pronunciation check, render, QA, validator, share, waveform), `build.sh`, `tts/music.py`, `SCENE_GUIDE.md`, three-thumbnail stub.
- `setup.sh` + `requirements-*.txt`: create the two shared Python environments (`.venv` Manim, `tts/.venv` Kokoro+Whisper).
- `.claude/workflows/`: the script workflow and the scenes workflow. `.claude/skills/`: entry points (below).
- `reference/hadwiger-nelson/`: the pilot and **gold standard** (source code, scenes, scripts, research, thumbnail).
  When a doc leaves a question open, do what the pilot did. It predates the template, so it differs in three ways: `PRON`
  lives in its `tools/timeline.py`, its `common.py` holds its topic helpers (`stick`, `BoundsBar`), and it has `geom.py`
  instead of `topic.py`.
- `reference/riemann-hypothesis/`: the second video, made with this engine (`topic.py` with numerics, shared layouts and
  the `ErrorDial` motif; brief; scripts; scenes; thumbnail).
- The references are source only (rendered media were not kept). Read them for style; never render inside them.

## Skills
- `aertheon-video`: make a new video from a topic (any length; default ~10 minutes).
- `aertheon-scene`: fix or rework one scene of an existing video (render/QA loop).
- `aertheon-thumbnail`: make or redo a video's three thumbnails in the channel style.

## Standing rules
- Audio is the master clock: scenes render silent and frame-exact against `timeline/*.json`; sound is muxed once at the
  end. Manim's `add_sound()` is banned (it silently drops clips after cached animations).
- The voice covers the whole video, with breathing room between sentences: no animation without speech, no wall of
  sentences without pauses. QA (`tools/qa.py`, `tools/final_qa.py`, which also reads the waveform) enforces it; zero ERRORs
  before anything is called done.
- The channel standards are fixed for every video: the voice (Kokoro `af_heart` at speed 0.85), the procedural music bed,
  the palette and the fonts (`STYLE.md`). Change them only as a deliberate engine change.
- Use the newest, most capable model for every agent (the workflows inherit the session model).
- Deliver by opening the mp4 **and** the three thumbnail PNGs (PIPELINE.md step 10), not the video alone.
- Improve the engine only in this directory's `template/`, docs and workflows, and only as a deliberate engine change
  (never as a side effect of making a video). Finished videos keep their own frozen copies of the tools.
