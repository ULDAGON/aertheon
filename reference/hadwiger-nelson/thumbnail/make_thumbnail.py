"""Hadwiger-Nelson thumbnail (1280x720), in the AERTHEON pastel channel style.

Left: the 7-colour hexagon tiling with a unit stick whose ends land on two
different colours. Right: the open question, 5, 6 or 7?
Run: python3 make_thumbnail.py   (needs rsvg-convert)
"""
import math, random, subprocess

# Same palette as ../../aertheon-branding/make_branding.py
PASTEL = ["#A9D3F7", "#F9E1A0", "#F6B6D4", "#B6E2BB", "#D3C0F8", "#F8CBA1", "#A6E8DF"]
CREAM, LAVENDER, INK, INK_SOFT = "#FCF8F3", "#EFEAF8", "#3A3D5C", "#8E8AA8"
FONT = "Avenir Next"

W, H, R = 1280, 720, 62
FIELD = (360, 370)          # centre of the tiling patch
STICK = ((228, 452), (486, 300))


def hex_pts(cx, cy, r, inset=0.0):
    r -= inset
    return " ".join(f"{cx + r*math.cos(math.radians(60*k)):.1f},{cy + r*math.sin(math.radians(60*k)):.1f}"
                    for k in range(6))


def axial_to_px(q, r):
    return FIELD[0] + 1.5 * R * q, FIELD[1] + math.sqrt(3) * R * (r + q / 2)


def colour_at(x, y):
    """Colour index of the tile containing (x, y): nearest tile centre."""
    q, r = min(((q, r) for q in range(-8, 9) for r in range(-8, 9)),
               key=lambda c: math.dist(axial_to_px(*c), (x, y)))
    return (q + 3 * r) % 7


def main():
    rng = random.Random(3)
    tiles = []
    for q in range(-8, 9):
        for r in range(-8, 9):
            x, y = axial_to_px(q, r)
            d = math.dist((x, y), FIELD) / 330 + rng.uniform(-0.12, 0.12)
            if d >= 1:
                continue
            op = min(1.0, 1.9 * (1 - d) + 0.15)
            tiles.append(f'<polygon points="{hex_pts(x, y, R, 4)}" fill="{PASTEL[(q + 3*r) % 7]}" '
                         f'fill-opacity="{op:.2f}"/>')

    (ax, ay), (bx, by) = STICK
    ca, cb = colour_at(ax, ay), colour_at(bx, by)
    assert ca != cb, "stick ends must land on different colours"
    mx, my = (ax + bx) / 2, (ay + by) / 2
    nx, ny = (ay - by), (bx - ax)                       # normal to the stick, for the "1" label
    n = math.hypot(nx, ny); nx, ny = nx / n, ny / n

    choices = []
    for i, (digit, col) in enumerate(zip("567", (PASTEL[2], PASTEL[1], PASTEL[0]))):
        cx, cy = 808 + 172 * i, 470
        choices.append(f'<polygon points="{hex_pts(cx, cy, 84, 0)}" fill="{col}"/>'
                       f'<text x="{cx}" y="{cy + 38}" text-anchor="middle" font-family="{FONT}" '
                       f'font-weight="800" font-size="112" fill="{INK}">{digit}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{LAVENDER}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {"".join(tiles)}
  <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{CREAM}" stroke-width="24" stroke-linecap="round"/>
  <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
  <circle cx="{ax}" cy="{ay}" r="22" fill="{PASTEL[ca]}" stroke="{INK}" stroke-width="8"/>
  <circle cx="{bx}" cy="{by}" r="22" fill="{PASTEL[cb]}" stroke="{INK}" stroke-width="8"/>
  <text x="{mx + 42*nx:.0f}" y="{my + 42*ny + 22:.0f}" text-anchor="middle" font-family="Palatino"
        font-style="italic" font-weight="bold" font-size="64" fill="{INK}" stroke="{CREAM}" stroke-width="10"
        paint-order="stroke">1</text>
  <text x="975" y="190" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="82"
        fill="{INK}">HOW MANY</text>
  <text x="975" y="290" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="82"
        fill="{INK}">COLORS?</text>
  {"".join(choices)}
  <text x="975" y="628" text-anchor="middle" font-family="{FONT}" font-weight="600" font-size="36"
        letter-spacing="3" fill="{INK_SOFT}">nobody knows which</text>
</svg>'''
    with open("hadwiger_nelson_thumbnail.svg", "w") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "hadwiger_nelson_thumbnail.svg",
                    "-o", "hadwiger_nelson_thumbnail.png"], check=True)


if __name__ == "__main__":
    main()
