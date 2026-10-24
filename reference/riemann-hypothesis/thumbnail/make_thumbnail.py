"""Half the Digits: The Riemann Hypothesis thumbnail (1280x720) in the AERTHEON pastel channel style (engine/THUMBNAIL.md).

Left: the prime staircase up to 43 built from pastel treads (each tread spans the gap to the next prime, so the
irregular gaps are visible), with Riemann's smooth curve R(x) riding through it as the INK focal element.
Right: the question, and the dial's three readings 0 · ½ · 1 with ½ lit (Riemann's guess).
Run: ../.venv/bin/python make_thumbnail.py   (needs mpmath and rsvg-convert)
"""
import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "branding"))  # engine/branding
from brand import *  # noqa: E402,F401,F403

STEM = Path(__file__).resolve().parents[1].name.replace("-", "_") + "_thumbnail"

XMAX, YMAX = 43, 14                 # problem units shown
X0, Y0, SX, SY = 58, 655, 13.0, 39.5  # px origin (bottom left) and px per unit


def px(x, y):
    return X0 + SX * x, Y0 - SY * y


def primes(n):
    return [p for p in range(2, n + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def main():
    W, H = THUMB_W, THUMB_H
    P = primes(XMAX + 4)
    art = []
    # the staircase as a bold pastel step line: riser at each prime, tread to the next prime
    for k, (p, q) in enumerate(zip(P, P[1:]), 1):
        if p > XMAX:
            break
        (xa, ya), (_, yb), (xc, _) = px(p, k - 1), px(p, k), px(min(q, XMAX + 2), k)
        fade = min(1.0, 0.3 + 0.12 * k)
        art.append(f'<polyline points="{xa:.1f},{ya:.1f} {xa:.1f},{yb:.1f} {xc:.1f},{yb:.1f}" fill="none" '
                   f'stroke="{PASTEL[(k - 1) % 7]}" stroke-opacity="{fade:.2f}" stroke-width="17" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    # honesty: the treads are the true prime staircase π(x)
    count = lambda x: sum(1 for p in P if p <= x)  # noqa: E731
    assert [count(x) for x in (10, 20, 43)] == [4, 8, 14]
    # focal element: Riemann's sharpened curve R(x), which the video rebuilds exactly from the zeros
    xs = [2 + i * (XMAX + 2 - 2) / 300 for i in range(301)]
    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in (px(x, float(mp.riemannr(x))) for x in xs))
    art.append(f'<polyline points="{pts}" fill="none" stroke="{CREAM}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>')
    art.append(f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    assert abs(float(mp.riemannr(43)) - count(43)) < 1.0   # the curve really rides the staircase
    # the dial's three readings; Riemann's guess ½ lit
    dial = []
    for i, (lab, col, op, ink) in enumerate((("0", PASTEL[0], 0.45, INK_SOFT), ("½", PASTEL[1], 1.0, INK),
                                             ("1", PASTEL[4], 0.45, INK_SOFT))):
        cx, cy = 820 + 165 * i, 468
        stroke = f' stroke="{INK}" stroke-width="8"' if lab == "½" else ""
        dial.append(f'<polygon points="{hex_pts(cx, cy, 84 if lab == "½" else 74)}" fill="{col}" fill-opacity="{op}"{stroke}/>'
                    f'<text x="{cx}" y="{cy + 38}" text-anchor="middle" font-family="{NUM_FONT}" font-weight="bold" '
                    f'font-size="{112 if lab == "½" else 92}" fill="{ink}">{lab}</text>')
    text = (headline(985, 190, "HOW RANDOM", size=70) + headline(985, 285, "ARE PRIMES?", size=70)
            + "".join(dial) + subline(985, 628, "the riemann hypothesis"))
    render(str(Path(__file__).parent / STEM), svg_doc(W, H, background(W, H) + "".join(art) + text), W, H)


if __name__ == "__main__":
    main()
