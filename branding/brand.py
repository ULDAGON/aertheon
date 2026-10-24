"""AERTHEON brand tokens + SVG helpers for thumbnails and channel art (single source of truth).

    import sys; sys.path.insert(0, "<engine>/branding"); from brand import *

PASTEL[i] is the pastel twin of the video PALETTE[i] in engine/template/common.py
(blue, yellow, pink, green, purple, orange, teal), so a thumbnail and its video share one colour story.
"""
import math
import subprocess

PASTEL = ["#A9D3F7", "#F9E1A0", "#F6B6D4", "#B6E2BB", "#D3C0F8", "#F8CBA1", "#A6E8DF"]
P_BLUE, P_YELLOW, P_PINK, P_GREEN, P_PURPLE, P_ORANGE, P_TEAL = PASTEL
CREAM, LAVENDER = "#FCF8F3", "#EFEAF8"       # background gradient, top-left -> bottom-right
INK, INK_SOFT = "#3A3D5C", "#8E8AA8"         # headline / subline
FONT, NUM_FONT = "Avenir Next", "Palatino"

THUMB_W, THUMB_H = 1280, 720


def hex_pts(cx, cy, r, inset=0.0):
    """Flat-top hexagon points, shrunk by `inset` px for the gaps between tiles."""
    r -= inset
    return " ".join(f"{cx + r*math.cos(math.radians(60*k)):.1f},{cy + r*math.sin(math.radians(60*k)):.1f}"
                    for k in range(6))


def background(w, h):
    """<defs> + full-size rect with the cream -> lavender diagonal gradient."""
    return (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{LAVENDER}"/>'
            f'</linearGradient></defs><rect width="{w}" height="{h}" fill="url(#bg)"/>')


def headline(x, y, text, size=82, anchor="middle", weight=800, fill=INK):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}">{text}</text>')


def subline(x, y, text, size=36, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="600" '
            f'font-size="{size}" letter-spacing="3" fill="{INK_SOFT}">{text}</text>')


def svg_doc(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


def render(stem, svg, w, h, png=None):
    """Write <stem>.svg and rasterize it with rsvg-convert to `png` (default <stem>.png)."""
    with open(f"{stem}.svg", "w") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), f"{stem}.svg", "-o", str(png or f"{stem}.png")],
                   check=True)
