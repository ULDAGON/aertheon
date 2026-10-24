# Making a video: the pipeline

You are the orchestrator. The user gives a topic; you deliver a finished video, three thumbnails, three titles and the description
without asking them to explain the style again. Work through the steps in order. Each ends on a completion criterion; move on only when it holds.
Heavy creative work goes to subagents through the two saved workflows. They inherit this session's model (use the newest,
most capable one). Keep the user posted with one short line per step.

**Tell the user the expected duration up front.** A 10-minute video took ~2 h 45 min wall time and ~$130 (RH: script workflow
71 min, 12 agents; timeline ~10 min; foundation ~6 min; scenes workflow 65 min, 66 agents; h build ~10 min). Short videos
save little: the workflows keep every stage (the script workflow alone is ~70 min whatever the length, and scenes are built
in parallel), so tell the user about 2 hours for a 1–5 minute video.

`$E` = this engine (the repository root),
`$P` = `<videos>/<slug>`, where `<videos>` is `$AERTHEON_VIDEOS` or else the `videos/` folder next to `$E` (the video folder: only what the user opens),
`$V` = `$P/src` (the working folder: every command below runs here).
```
$P/<name>.mp4         the final video (build.sh writes it here; no copy in src/)
$P/thumbnails/        the three thumbnail PNGs
$P/youtube.md         three titles + the description (YOUTUBE.md)
$P/src/               everything else: script, research, audio, timeline, scenes, tools, out/ (share copy, .srt, QA, scratch)
```
**Everything a video produces lives in `$P`, all work in `$V`.** Never write into `$E` while making a video (no scratch files, renders, audio or
notes), and never run `render.sh`, `timeline.py` or `build.sh` inside `$E/template/` or `$E/reference/`; engine improvements
are a separate, deliberate change (see AGENTS.md).

**Work without `rm`** (never delete anything, even in the scratchpad): use fresh directory names (`mkdir -p` with a
new suffix), `ffmpeg -y` to overwrite, `NOCACHE=1` instead of clearing Manim caches, and `mv` leftovers into
`$V/out/_scratch/`. Scratch locations: `$V/out/_scratch/<agent>/` for agents, `$V/out/review/<SceneId>_<lens>/` for reviewers,
`$V/out/smoke/` for step 5. Long commands (steps 4 and 7) exceed the 600 s Bash limit: run them with `run_in_background` and
wait with Monitor or an until-loop (foreground `sleep` is blocked). `JOBS=4`–`6` suits a machine with ~48 GB of RAM; use fewer parallel jobs with less memory.

## 1. Scaffold
Pick a kebab-case slug and a working title, then:
```bash
$E/new_video.sh <slug> "<Working title>"
```
This creates `$P` with `src/` (= `$V`, a copy of `$E/template`), `thumbnails/` and `youtube.md`, links the shared Python
environments and runs `$E/setup.sh` if needed. It prints `$V`.
Done when: `$V/tools/render.sh` exists and `$V/.venv/bin/manim --version` runs.

## 2. Brief
Write `$V/brief.md` (model: `$E/reference/riemann-hypothesis/brief.md`): the one-line topic, the length (10 minutes unless the
user says otherwise; under 5 minutes uses the short-form arc in `STYLE.md`), the audience promise (what a non-expert understands
at the end), then these sections:
- `## Content list (teaching order)`: the must-cover ideas, 1–3 optional on-ramps (a simpler warm-up case, a reframing), the
  central argument that must be airtight, and an ending idea that returns to the opening image.
- `## Facts to verify (with sources)`: names, dates, numbers, exact parameters of anything the animation must draw; mark
  uncertain items with `?`.
- `## Recurring motif (suggestion for the drafts)`.
- What `topic.py` can compute (exact curves, counts, datasets), so storyboards may ask for real computed pictures.

Shape it with the arc in `STYLE.md`. If the topic is ambiguous (which aspect? which level?), ask the user one question;
otherwise proceed.
Done when: `brief.md` names every must-cover idea and every fact to verify.

## 3. Script (workflow `aertheon-script`)
```
Workflow({ scriptPath: "$E/.claude/workflows/aertheon-script.js",
           args: { root: "$V", engine: "$E", topic: "<one line>", minutes: 10,
                   content: "The full brief is in $V/brief.md: read it completely; it is the authoritative content list. <3–5 line summary>. topic.py can compute: <…>" } })
```
`minutes` is a number (`1`, `10`), never a string. Research (facts + pedagogy) → three drafts (story / puzzle / visual) → two
judges → synthesis → three critics (facts, clarity, measured pacing) → final. Then read `$V/script/CHANGELOG.md` and apply
its "outside the script" items yourself.
**Use the wait** (~70 min): precompute heavy numerics into `$V/data/` in the background (`topic.py --precompute`, loaded by
`topic.py`), and prototype the central visual (real computed curves, a quick PIL/Manim still) to prove it can be shown.
Done when: `python3 $V/tools/validate_script.py --minutes <minutes>` shows zero ERRORs, the script's `target_minutes`
equals the requested length, and you have read the CHANGELOG.

## 4. Voice and timeline
Run in the background (10+ min), filtering the noise:
```bash
cd $V && tts/.venv/bin/python tools/timeline.py 2>&1 | grep -v -i "warning\|deprecat\|Fetching\|KokoroPipeline"
```
Per-sentence Kokoro TTS (cached), Whisper word alignment, pauses, `audio/scenes/*.wav`, `timeline/*.json`, captions.
Never pass `--speed` (the default 0.85 is the contract and part of the cache key). Use the wait to start `topic.py`.
For every WARN (Whisper heard something else), fix the name with a `"pron"` entry in the script and re-run; cached sentences
are reused. The WARNs come from a primed Whisper and miss most mispronunciations, so then run the unprimed check:
```bash
cd $V && tts/.venv/bin/python tools/pron_check.py      # --all for every sentence
```
Read every `SAID / HEARD` pair; for each `CHECK`, add a `pron` key (case-sensitive) and re-run both, or note why it is fine
(e.g. Whisper only spells the name differently). The timeline is now **frozen**: every later script edit shifts the marks the
scenes are built against, so all script changes happen before step 6.
Done when: zero WARN lines, every pron_check `CHECK` resolved, total within ±10 % of the target, every scene 35–90 s (25–90 s
for videos under 5 minutes) (`timeline/_summary.json`).

## 5. Shared scene foundation
Read the final script end to end, then write:
- `$V/topic.py`: every construction, dataset and count more than one scene uses, each asserting its own claims, plus the
  recurring motif as a class (like `BoundsBar` in `$E/reference/hadwiger-nelson/common.py`; for numerics, `data/` caching and
  shared layouts see `$E/reference/riemann-hypothesis/topic.py`). Fixed named layouts for anything that shares the motif's band,
  and a content ceiling/floor. **Every picture a later scene calls back to** (the opening grid, graph boxes, end states) is a
  `topic.py` constant, never re-typed per scene. `.venv/bin/python topic.py` self-checks.
- The "This video" section of `$V/SCENE_GUIDE.md`: motif (class, fixed home, state per scene), colour semantics for this
  topic, what `topic.py` offers, scale.
- A still smoke test in `$V/out/smoke/smoke.py` that imports `common` and `topic` and draws the motif in **every** state plus
  every shared layout that shares its band: `.venv/bin/manim -ql -s --media_dir out/smoke/media out/smoke/smoke.py Smoke`.
  It lives two levels below `$V`, so it starts with
  `import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # $V`
  (the scenes' `parent.parent` header would point at `$V/out`).
  Read the PNG; crop and zoom for overlaps and the ±6.6 × ±3.6 bounds; iterate (new file names, no `rm`).
Done when: the self-check passes, the smoke still is clean in every motif state and layout, and no `{{…}}` placeholder is
left in `SCENE_GUIDE.md`.

## 6. Scenes (workflow `aertheon-scenes`)
```
Workflow({ scriptPath: "$E/.claude/workflows/aertheon-scenes.js",
           args: { root: "$V", engine: "$E", topic: "<one line>", motif: "<motif and its state progression>",
                   scenes: [{ id: "S01_Hook", file: "s01_hook.py" }, …] } })
```
Build (one builder per scene, loops on `tools/render.sh <id> l` until QA is clean) → two reviewers (teaching, technical) →
fix (or a polish pass if both passed with minor issues) → a combined re-review → fix → **Shared** (one owner applies the
deduped builder `shared_requests` and re-renders every scene) → **Continuity** (one reviewer across all scenes; fixes to
shared files by one owner first, then scene-local fixes) → **Verify** (every scene re-rendered, and the open blocking
issues of scenes whose last round ended in `fix` re-checked). Make the thumbnails (step 9) while it runs.
The workflow has already applied the builders' shared requests and re-verified every scene: do not apply them again. After
it, before step 7, act on its return value:
- `shared_requests_left`: apply each entry yourself, once (never by parallel agents), then re-render **every** scene at `l`
  and re-read its QA (not only the one that asked).
- `verify[].unresolved` and every scene with `verify[].qa_errors` > 0: fix it with the `aertheon-scene` loop, or state why
  the item is fine. Read `scenes[].last_verdict`, `shared.rejected` and `continuity` for anything still open.
Done when: every `out/qa/<id>.report.txt` has zero ERROR lines and every remaining WARN has a stated reason.

## 7. Build
Run in the background (~7–10 min):
```bash
cd $V && JOBS=4 ./build.sh > out/build_h.log 2>&1
```
Renders all scenes at 1080p60, concatenates, mixes voice + ducked music bed at −16 LUFS, writes `$P/<name>.mp4` (the only
copy), `out/<name>.srt`, `out/<name>_720p_share.mp4` and `out/waveform_overview.png`, then runs `tools/final_qa.py`.
Expected at `h`: "late" WARNs < 0.15 s on float marks (`self.at(17.942)`) are frame rounding; state that as the reason.
0.15–0.25 s: fix (named mark or `self.word()`); ≥ 0.25 s is an ERROR. After any QA-tool change, re-run final QA.
Done when: final QA prints zero ERRORs (stream lengths agree, every sentence audible, no voice gap > 1.6 s).

## 8. Watch it yourself
Read `out/waveform_overview.png`. Pull a contact sheet from the final video and Read it:
`ffmpeg -y -i ../<name>.mp4 -vf "fps=1/10,scale=384:-1,tile=6x10" -frames:v 1 out/final_sheet.png`.
Spot-check the scene cuts (empty background on both sides) and the motif's progression. Fix anything wrong at scene
level (`tools/render.sh <id> l`, then rebuild).
Done when: you would show it to the user without caveats, or the caveats are listed.

## 9. Thumbnails, titles and description
Thumbnails: follow `$E/THUMBNAIL.md` (best done during step 6): three concepts, script in `$V/thumbnails/`, PNGs in
`$P/thumbnails/`. Titles and description: follow `$E/YOUTUBE.md` and fill in `$P/youtube.md` (three titles paired with the
thumbnails; description = the video, chapters from `tools/chapters.py`, the fixed About AERTHEON paragraph, sources as
checked URLs, hashtags).
Done when: all three PNGs read well at full size and in the 320×180 strip, and `youtube.md` has no `{{…}}` left and every
source URL returned 200.

## 10. Deliver
`open $P/<name>.mp4 $P/thumbnails/<name>_thumbnail_*.png` (video **and** thumbnails: the
user judges both, so never open only the video). Do not send the mp4 as an attachment (> 30 MiB limit); point to the files. Then tell the user, briefly:
- Title, length, "open on your screen".
- Files: `$P/<name>.mp4` + size, `$P/youtube.md`, the three thumbnails (one line each, with the title it pairs with);
  in `src/out/`: 720p share copy + size, `.srt`, waveform + longest pause.
- How it tells the story: one arrow chain, plus the motif.
- How it was made: agent counts, QA numbers, "the on-screen maths is computed".
- Check before you publish: facts newer than the model's knowledge, year-relative phrases ("a hundred and sixty-seven years").
- Engine improvements suggested by this run, and where scratch lives (`out/_scratch/`, `out/review/`, `out/smoke/`).

## Troubleshooting: voice and picture out of sync
```bash
for f in out/media/*/videos/*/1080p60/*.mp4; do ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done
ffprobe -v error -show_entries format=duration -of csv=p=0 audio/scenes/<SceneId>.wav    # must match its video
ffmpeg -i ../<name>.mp4 -af silencedetect=noise=-40dB:d=0.9 -f null - 2>&1 | grep silence_   # voice holes
```
A video stream longer than its audio, or a long silence mid-scene, means a scene drifted from its timeline (a known failure:
42.22 s video vs 33.51 s audio, a 9.08 s hole, caused by `add_sound()`, which is banned). Re-render that scene with
`NOCACHE=1 tools/render.sh <id> l`, then rebuild.
