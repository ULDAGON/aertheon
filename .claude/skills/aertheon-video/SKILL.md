---
name: aertheon-video
description: Make a new AERTHEON explainer video (Manim + Kokoro voice, the channel's exact style) from a topic. Use whenever the user asks for a video, explainer, short or episode about a topic, at any length ("a 1 minute video about X", "now create a video about Y").
---

# Make an AERTHEON video

You are the orchestrator. Paths: `$E` = this engine (the repository root),
`$P` = `<videos>/<slug>` (`<videos>` = `$AERTHEON_VIDEOS`, else the `videos/` folder next to `$E`; top level: `<name>.mp4`, `thumbnails/`, `youtube.md`),
`$V` = `$P/src` (everything else; all commands run here).

1. Read `$E/PIPELINE.md` fully, then `$E/STYLE.md`. Follow PIPELINE.md step by step; each step ends on a "Done when"
   criterion — move on only when it holds. Keep the user posted with one short line per step. Tell the user the expected
   duration first (~2 h 45 min for 10 minutes; about 2 hours for a short one, since the script workflow alone takes
   ~70 min whatever the length; see PIPELINE.md).
2. Run the two saved workflows exactly as PIPELINE.md shows (asking for a video is the opt-in; do not ask again). Always pass
   `engine: "$E"` and the requested `minutes` as a number; pass `content` as a pointer to `$V/brief.md` plus a summary.
   The scenes workflow applies the builders' shared requests and verifies every scene itself; afterwards act only on its
   return value (`shared_requests_left`, `verify[].unresolved`, `verify[].qa_errors`), as PIPELINE.md step 6 says.
3. All work for the video goes into `$V` (only the final mp4, the thumbnail PNGs and `youtube.md` go to `$P`). Write nothing into `$E` (no scratch, no smoke tests, no renders). Smoke tests live
   in `$V/out/smoke/`, temporary files in `$V/out/_scratch/<agent>/` or the session scratchpad. Never delete (no `rm`): use fresh
   names, `ffmpeg -y`, `NOCACHE=1`; never delete.

## Length
Default ~10 minutes. For other lengths pass `minutes` to the script workflow and to `tools/validate_script.py --minutes`:
the budget scales (135–145 words per minute, about one scene per minute; a 1-minute short may be 1–2 scenes; each scene
25–90 s under 5 minutes). Under 5 minutes keep the pilot's arc compressed (`STYLE.md`, short form): hook image + question in
≤ 10 s (≤ ~15 s above 2 minutes) → the one key idea shown step by step → honest status in one sentence → callback to the
opening image.
Still one recurring motif, still breathing room, still every bookmark synced; same palette, fonts, voice and music.

## Before you call it done
- `tools/final_qa.py` (run by `build.sh`) shows zero ERRORs; you have looked at `out/waveform_overview.png` and a contact
  sheet of the final video.
- The three thumbnails exist in `$P/thumbnails/` (`aertheon-thumbnail` skill / `$E/THUMBNAIL.md`), and `$P/youtube.md`
  holds three titles and the description with no `{{…}}` left (`$E/YOUTUBE.md`).
- No file under `$E` was created or changed by this video (only `.venv`, `tts/.venv`, `__pycache__` may change).
- Deliver per PIPELINE.md step 10: `open` the mp4 and the three thumbnail PNGs.
