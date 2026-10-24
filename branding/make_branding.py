"""AERTHEON channel art: YouTube banner (2560x1440), profile picture (800x800) and the README header (1600x560).

Motif: the 7-colour hexagon tiling of the plane (the classic upper bound for the
Hadwiger-Nelson problem), in pastel versions of the video paint palette.
Writes SVG, renders PNG with rsvg-convert.  Run: python3 make_branding.py
"""
import math, random

from brand import CREAM, FONT, INK, INK_SOFT, LAVENDER, PASTEL, hex_pts, render


def color_of(q, r):
    # (q + 3r) mod 7: every hexagon's six neighbours get six different colours
    return PASTEL[(q + 3 * r) % 7]


def axial_to_px(q, r, R):
    return 1.5 * R * q, math.sqrt(3) * R * (r + q / 2)


TAGLINE = "MATHEMATICS, COMPUTER SCIENCE, ENGINEERING"


def hero(stem, W, H, R, clear, scale=1.0):
    """The name on a hexagon field that dissolves into an elliptical clear zone (rx, ry = `clear`)."""
    cx, cy = W / 2, H / 2
    rng = random.Random(7)
    tiles = []
    for q in range(-20, 21):
        for r in range(-20, 20):
            x, y = axial_to_px(q, r, R)
            if abs(x) > W / 2 + R or abs(y) > H / 2 + R:
                continue
            # elliptical clear zone around the name; tiles dissolve in as you move out
            d = math.hypot(x / clear[0], y / clear[1])
            t = d - 1 + rng.uniform(-0.18, 0.18)
            if t <= 0:
                continue
            op = min(1.0, 0.25 + t * 1.6)
            tiles.append(f'<polygon points="{hex_pts(cx + x, cy + y, R, 5)}" fill="{color_of(q, r)}" '
                         f'fill-opacity="{op:.2f}"/>')
    k = scale
    dots = "".join(f'<circle cx="{cx + k * (50*i - 150):.0f}" cy="{cy + k * 150:.0f}" r="{k * 11:.1f}" fill="{c}"/>'
                   for i, c in enumerate(PASTEL))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{LAVENDER}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {"".join(tiles)}
  <text x="{cx + k * 14:.0f}" y="{cy + k * 48:.0f}" text-anchor="middle" font-family="{FONT}" font-weight="600"
        font-size="{k * 176:.0f}" letter-spacing="{k * 28:.0f}" fill="{INK}">AERTHEON</text>
  <text x="{cx + k * 5:.0f}" y="{cy - k * 105:.0f}" text-anchor="middle" font-family="{FONT}" font-weight="500"
        font-size="{k * 34:.0f}" letter-spacing="{k * 9:.0f}" fill="{INK_SOFT}">{TAGLINE}</text>
  {dots}
</svg>'''
    render(stem, svg, W, H)


def banner():
    hero("aertheon_banner", 2560, 1440, 74, (700, 330))


def readme_header():
    hero("aertheon_header", 1600, 560, 46, (660, 205), scale=0.75)


def pfp():
    S, R = 800, 124
    c = S / 2
    cells = [(0, 0)] + [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    hexes = []
    for q, r in cells:
        x, y = axial_to_px(q, r, R)
        fill = INK if (q, r) == (0, 0) else color_of(q, r)
        hexes.append(f'<polygon points="{hex_pts(c + x, c + y, R, 6)}" fill="{fill}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <radialGradient id="bg" cx="0.5" cy="0.45" r="0.7">
      <stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{LAVENDER}"/>
    </radialGradient>
  </defs>
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  {"".join(hexes)}
  <text x="{c}" y="{c + 50}" text-anchor="middle" font-family="{FONT}" font-weight="600"
        font-size="150" fill="{CREAM}">A</text>
</svg>'''
    render("aertheon_pfp", svg, S, S)


if __name__ == "__main__":
    banner()
    pfp()
    readme_header()
