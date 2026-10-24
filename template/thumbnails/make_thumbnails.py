"""{{TITLE}}: three thumbnails (1280x720) in the AERTHEON pastel channel style (engine/THUMBNAIL.md).

Three different concepts, one per title suggestion (THUMBNAIL.md "Three thumbnails"), so the user can pick or A/B test:
  1 {{concept 1: the hook question}}
  2 {{concept 2: the surprising mechanism or number}}
  3 {{concept 3: the stakes or the open question}}
Each: left the key visual in PASTEL with one INK-outlined focal element; right two INK headline lines, one tension element,
one INK_SOFT subline. Shared drawing helpers go at the top; each variant asserts that its picture is true to the video.
Run (in src/): python3 thumbnails/make_thumbnails.py   (needs rsvg-convert)
  -> <video>/thumbnails/<name>_thumbnail_1..3.png (top level, next to the mp4); the .svg sources stay here in src/
References: {{ENGINE_DIR}}/reference/*/thumbnail/make_thumbnail.py (single-thumbnail scripts from before this layout)
"""
import sys
from pathlib import Path

sys.path.insert(0, "{{ENGINE_DIR}}/branding")
from brand import *  # noqa: E402,F401,F403

VIDEO = Path(__file__).resolve().parents[2]                     # videos/<slug>
STEM = VIDEO.name.replace("-", "_") + "_thumbnail"


def v1():
    art = ""        # {{key visual, left ~55%: pastel shapes, dissolving toward the edges, one INK-outlined focal element}}
    return art + headline(975, 190, "{{LINE ONE}}") + headline(975, 290, "{{LINE TWO}}") + subline(975, 628, "{{subline}}")


def v2():
    art = ""        # {{a different angle on the same video, not a recolour of v1}}
    return art + headline(975, 190, "{{LINE ONE}}") + headline(975, 290, "{{LINE TWO}}") + subline(975, 628, "{{subline}}")


def v3():
    art = ""        # {{a third angle}}
    return art + headline(975, 190, "{{LINE ONE}}") + headline(975, 290, "{{LINE TWO}}") + subline(975, 628, "{{subline}}")


def main():
    here, out = Path(__file__).parent, VIDEO / "thumbnails"
    out.mkdir(exist_ok=True)
    for n, make in enumerate((v1, v2, v3), 1):
        render(str(here / f"{STEM}_{n}"), svg_doc(THUMB_W, THUMB_H, background(THUMB_W, THUMB_H) + make()),
               THUMB_W, THUMB_H, png=out / f"{STEM}_{n}.png")


if __name__ == "__main__":
    main()
