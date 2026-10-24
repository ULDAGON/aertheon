---
name: aertheon-scene
description: Fix, rework or polish one scene of an existing AERTHEON video (sync, pacing, visuals, QA errors), then rebuild. Use when the user points at a moment or scene in a finished or in-progress video in the videos folder.
---

# Rework one scene

`$V` = the video's working folder (`<videos>/<slug>/src`, where `<videos>` is `$AERTHEON_VIDEOS` or else the `videos/` folder next to
the engine; videos made before the `src/` layout have no `src/`: then it is `<videos>/<slug>`). Work only inside `$V`; `build.sh` writes the final mp4 one level
up (`../<name>.mp4`).

1. Read `$V/SCENE_GUIDE.md` (rules, `TimedScene` API, QA workflow, "This video"), `$V/common.py`, `$V/topic.py`, the
   scene's paragraphs in `$V/script/script.json` and `$V/timeline/<SceneId>.json`.
2. The voice and timeline are frozen. Do not edit the script unless the user asks; a script change means re-running
   `tts/.venv/bin/python tools/timeline.py` and re-checking every scene whose marks moved.
3. Edit `scenes/<file>.py`, then loop `tools/render.sh <SceneId> l` and Read `out/qa/<SceneId>.timeline.png`,
   `.marks.png` and `.sheet.png` each round until QA has zero ERRORs and the scene is clear and calm. Time beats with
   named marks or `self.word()`, not typed floats. Stale or crashing cache: `NOCACHE=1 tools/render.sh <SceneId> l`.
   A change to `common.py`/`topic.py` means re-rendering every scene at `l` and re-reading its QA.
4. Compare against the gold standard if unsure how it should look: `reference/hadwiger-nelson/scenes/` in the engine.
5. Rebuild in the background (> 600 s): `cd $V && JOBS=4 ./build.sh > out/build_h.log 2>&1`; final QA must show zero
   ERRORs (late < 0.15 s on a float mark at `h` is frame rounding). Report what changed.
