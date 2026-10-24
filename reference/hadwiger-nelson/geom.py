"""Verified geometry shared by all scenes (pure numpy, problem units: 1.0 = the forbidden distance).

Convert to manim coordinates with `to_scene(p, scale, center)`.
Every constructor asserts its own claims (unit lengths etc.) at import/call time.
"""
import numpy as np

SQ3 = np.sqrt(3.0)
PHI = 2 * np.arcsin(1 / (2 * SQ3))   # Moser spindle opening angle ≈ 33.557°


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    v = np.asarray(v, float)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def to_scene(p, scale=2.0, center=(0, 0, 0)):
    """2D problem coords -> 3D manim point."""
    p = np.asarray(p, float)
    c = np.asarray(center, float)
    return np.array([c[0] + scale * p[0], c[1] + scale * p[1], 0.0])


def dist(a, b):
    return float(np.linalg.norm(np.asarray(a, float) - np.asarray(b, float)))


# ------------------------------------------------------------------ equilateral triangle
def triangle(base_angle=0.0):
    """Unit equilateral triangle with vertex 0 at the origin: [A, B, C]."""
    A = np.zeros(2)
    B = rot([1, 0], base_angle)
    C = rot([0.5, SQ3 / 2], base_angle)
    return [A, B, C]


# ------------------------------------------------------------------ Moser spindle
def diamond(angle):
    """Two unit triangles sharing an edge. Tip A at origin, far tip D at distance √3 in direction `angle`.
    Returns dict A, B, C, D (B, C = the middle pair)."""
    u = rot([1, 0], angle)
    D = SQ3 * u
    mid = D / 2
    n = rot(u, np.pi / 2) * 0.5
    return {"A": np.zeros(2), "B": mid + n, "C": mid - n, "D": D}


def moser_spindle(up=np.pi / 2):
    """The Moser spindle: two diamonds sharing tip A, rotated ±PHI/2 about `up` so their far tips are 1 apart.
    Returns (points dict: A, B, C, D, B2, C2, D2), (edges: list of name pairs, 11 of them)."""
    d1, d2 = diamond(up + PHI / 2), diamond(up - PHI / 2)
    P = {"A": d1["A"], "B": d1["B"], "C": d1["C"], "D": d1["D"], "B2": d2["B"], "C2": d2["C"], "D2": d2["D"]}
    E = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
         ("A", "B2"), ("A", "C2"), ("B2", "C2"), ("B2", "D2"), ("C2", "D2"),
         ("D", "D2")]
    for a, b in E:
        assert abs(dist(P[a], P[b]) - 1) < 1e-9, (a, b)
    names = list(P)
    unit_pairs = {(a, b) for i, a in enumerate(names) for b in names[i + 1:] if abs(dist(P[a], P[b]) - 1) < 1e-9}
    assert unit_pairs == {tuple(sorted(e, key=names.index)) for e in E}, "spindle has hidden extra unit pairs"
    return P, E


# ------------------------------------------------------------------ hexagon 7-colouring (Isbell)
HEX_SIDE = 0.45   # diameter 0.9 < 1; closest same-coloured hexagons are √7·s ≈ 1.19 apart (> 1). Valid for s in (1/√7, 1/2).


def hex_center(q, r, s=HEX_SIDE):
    """Flat-top axial coordinates -> centre."""
    return np.array([s * 1.5 * q, s * SQ3 * (r + q / 2)])


def hex_color(q, r):
    """Colour index 0..6 of hexagon (q, r). Centre = 0, its six neighbours = six different colours."""
    return (q + 3 * r) % 7


def hex_vertices(center, s=HEX_SIDE):
    return [np.asarray(center) + s * np.array([np.cos(np.pi / 3 * k), np.sin(np.pi / 3 * k)]) for k in range(6)]


def hex_cells(radius_units, s=HEX_SIDE):
    """All (q, r, center, color) whose centre lies within radius_units of the origin."""
    out = []
    R = int(radius_units / s) + 2
    for q in range(-R, R + 1):
        for r in range(-R, R + 1):
            c = hex_center(q, r, s)
            if np.linalg.norm(c) <= radius_units:
                out.append((q, r, c, hex_color(q, r)))
    return out


# ------------------------------------------------------------------ one-dimensional warm-up
def line_color(x):
    """2-colouring of the line: half-open unit intervals [k, k+1) alternate colours 0/1."""
    return int(np.floor(x)) % 2


# ------------------------------------------------------------------ big unit-distance webs (illustrations)
def lattice_ball(r):
    """Triangular-lattice points (unit spacing) within distance r of the origin."""
    pts = []
    R = int(r) + 2
    for i in range(-2 * R, 2 * R + 1):
        for j in range(-2 * R, 2 * R + 1):
            p = np.array([i + j / 2, j * SQ3 / 2])
            if np.linalg.norm(p) <= r + 1e-9:
                pts.append(p)
    return np.array(pts)


def unit_web(n_points=1581, lattice_r=SQ3 * 2, angle=PHI):
    """Genuine unit-distance graph: Minkowski sum H + R(angle)·H of a triangular-lattice patch H,
    keeping the n_points closest to the origin. Returns (points (N,2), edges (M,2) index pairs).
    Every edge has length exactly 1 (asserted). Illustration only - not de Grey's actual graph."""
    H = lattice_ball(lattice_r)
    RH = np.array([rot(p, angle) for p in H])
    P = (H[:, None, :] + RH[None, :, :]).reshape(-1, 2)
    P = np.unique(np.round(P, 9), axis=0)
    P = P[np.argsort(np.linalg.norm(P, axis=1), kind="stable")][:n_points]
    from scipy.spatial import cKDTree
    tree = cKDTree(P)
    pairs = np.array(sorted(tree.query_pairs(1 + 1e-6)))
    d = np.linalg.norm(P[pairs[:, 0]] - P[pairs[:, 1]], axis=1)
    E = pairs[np.abs(d - 1) < 1e-6]
    assert np.all(np.abs(np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1) - 1) < 1e-6)
    return P, E


if __name__ == "__main__":
    P, E = moser_spindle()
    print("spindle ok:", len(P), "points,", len(E), "sticks, |D D2| =", round(dist(P["D"], P["D2"]), 12))
    cells = hex_cells(3)
    same = [(a, b) for a in cells for b in cells if a[3] == b[3] and (a[0], a[1]) < (b[0], b[1])]
    print("hex cells:", len(cells), "min same-colour centre distance", round(min(dist(a[2], b[2]) for a, b in same), 4))
    Pw, Ew = unit_web()
    print("web:", len(Pw), "points,", len(Ew), "unit sticks")
