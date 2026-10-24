---
name: aertheon-thumbnail
description: Make or redo the three 1280x720 YouTube thumbnails for an AERTHEON video in the channel's pastel style (or regenerate the channel banner/profile picture). Use when the user asks about a thumbnail, cover image or channel art.
---

# Thumbnails

`$E` = this engine (the repository root), `$P` = `<videos>/<slug>` (`<videos>` = `$AERTHEON_VIDEOS`, else the `videos/`
folder next to `$E`), `$V` = `$P/src`.

1. Read `$E/THUMBNAIL.md` and both reference scripts:
   `$E/reference/hadwiger-nelson/thumbnail/make_thumbnail.py` (the original) and
   `$E/reference/riemann-hypothesis/thumbnail/make_thumbnail.py`.

2. Fill in `$V/thumbnails/make_thumbnails.py` (scaffolded with every video; it imports `brand.py` tokens and helpers):
   **three different concepts** (hook question, surprise, stakes; THUMBNAIL.md "Three thumbnails"), each paired with a
   title suggestion. Each: left the video's key visual in `PASTEL`, dissolving toward the edges, one `INK`-outlined focal
   element; right two short uppercase `INK` headline lines, one bold tension element, one lowercase `INK_SOFT` subline.
   ≤ ~6 words each. Assert in code that each picture is true to the video. Bold ~17 px strokes; fill the left side to its
   corners; keep the bottom-right corner clear (YouTube's duration badge).
3. `cd $V && python3 thumbnails/make_thumbnails.py` (`.venv/bin/python` instead if it imports numpy, mpmath or `topic`) →
   `$P/thumbnails/<name>_thumbnail_{1,2,3}.png`. Read each PNG and the 320×180 strip (command in THUMBNAIL.md); every
   headline and focal element must read at both sizes. Write the three paired titles into `$P/youtube.md`
   (`$E/YOUTUBE.md`). When delivering, `open` all three PNGs and give the three titles.
   Old videos without `src/` (single `thumbnail/` folder): add `thumbnails/` beside it, never move or overwrite the old one.
4. Channel art: `cd $E/branding && python3 make_branding.py` (banner 2560×1440, pfp 800×800, README header 1600×560). Only on request.
