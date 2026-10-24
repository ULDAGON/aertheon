# {{TITLE}}: YouTube text

Rules: engine/YOUTUBE.md. new_video.sh moves this file to the top of the video folder (next to the mp4 and thumbnails/).

## Titles (pick one)
1. {{title 1, pairs with thumbnails/…_thumbnail_1.png}}
2. {{title 2, pairs with thumbnails/…_thumbnail_2.png}}
3. {{title 3, pairs with thumbnails/…_thumbnail_3.png}}

## Description (paste everything inside the block)
```text
{{2–3 short paragraphs: the hook in the video's own opening image, what the viewer will see and understand, and one line on honesty (e.g. "Every number on screen was computed …").}}

CHAPTERS
{{output of: python3 src/tools/chapters.py, titles rewritten for viewers}}

ABOUT AERTHEON
AERTHEON makes educational videos on mathematics, computer science and engineering. Every idea is built up from simple examples and explained step by step, so anyone can follow along, no background needed.

SOURCES
{{Short label: https://… (one per line, primary sources the video's claims rest on, each checked to load)}}

{{#Hashtag #Hashtag … (5–8)}}
```
