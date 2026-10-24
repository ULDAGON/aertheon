"""Verified numerics + recurring motifs for "Half the Digits: The Riemann Hypothesis".

Everything here is exact or checked against mpmath; `.venv/bin/python topic.py` runs the self-check
(and `--precompute` fills the data/ cache that scenes load; it is already filled, do not run it while scenes render).

NUMERICS (pure numpy / cached mpmath; x-values are problem units, convert with your own axes)
    ZEROS                     heights γ of the first 1,000 zeta zeros (ρ = ½ + iγ), from mpmath.zetazero
    primes_upto(n), prime_pi(xs)
    staircase_points(xmax, samples=3000)  corner points of the prime staircase π(x) on [0, xmax]
                                           (exact corners up to xmax 2,000; exact values at `samples` x-points above)
    li(xs)                    Gauss's curve = mpmath.li (NOT li - li(2)); li(1e5)=9629.81, li(1e6)=78627.55
    R(xs)                     Riemann's sharpened curve (mpmath.riemannr); R(100)=25.66
    base_curve(xs)            R(x) - 1/ln x + arctan(π/ln x)/π   (the smooth part of the exact recipe, incl. trivial zeros)
    zero_wave(k, xs)          wave of the k-th zero pair: -2 Re Σ_n μ(n)/n · Ei(ρ_k ln x / n)
    rebuild(n, xs)            base_curve + first n zero waves (in height order, conjugate pairs as one wave)
    rogue_wave(beta, gamma, xs), envelope(beta, gamma, xs) = 2 x^β / (|ρ| ln x)
    LIN_X (2..100, step 0.025) and LOG_X (10..1e6, 1,500 log-spaced) are the cached grids for waves;
    any other xs is computed on the fly (slow-ish, mpmath).
    block_counts(starts, width=1000), random_walks(seed=7, n=1_000_000, k=7, samples=2000)
    zeta_np(s)                vectorized ζ for complex arrays (Borwein + functional equation), rel. err < 1e-7 on |Im| ≤ 50
    spiral_partial_sums(s, N) partial sums of Σ 1/n^s (complex array, starts at 0)
    zeta_line_path(t0, t1, n) ζ(½ + it) samples;  domain_color_rgb(re0, re1, im0, im1, w, h) uint8 image, hue = arg ζ

MOTIFS (manim; import after `from common import *`)
    ErrorDial()               the error dial at its fixed home (bottom centre); see class docstring
    StripMap(...)             maps (real part, height) of the critical strip to scene points; layouts
                              DIAL_ALIGNED, INSET, INSET_240, EVIDENCE
    strip_group(m, n_zeros)   the strip (tint, edges, ACCENT line at ½, zero dots, floor labels) for a StripMap
    WAVE_COLORS[k-1]          colour of zero k's wave: pink, green, purple, orange, blue
"""
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ZEROS = np.array(json.loads((DATA / "zeros.json").read_text())["gammas"])

LIN_X = np.round(np.arange(2.0, 100.0 + 1e-9, 0.025), 6)
LOG_X = np.logspace(1, 6, 1500)


# ------------------------------------------------------------------ primes
@lru_cache(maxsize=4)
def primes_upto(n):
    n = int(n)
    sieve = np.ones(n + 1, bool)
    sieve[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.flatnonzero(sieve)


def prime_pi(xs):
    xs = np.asarray(xs, float)
    P = primes_upto(max(10, int(np.max(xs)) + 1))
    return np.searchsorted(P, xs, side="right")


def staircase_points(xmax, samples=3000):
    """Corner points [(x, π(x)), ...] from x = 0 to xmax, ready for VMobject.set_points_as_corners after scaling."""
    if xmax <= 2000:
        pts, c = [(0.0, 0.0)], 0
        for p in primes_upto(int(xmax)):
            pts += [(float(p), c), (float(p), c + 1)]
            c += 1
        pts.append((float(xmax), c))
        return np.array(pts)
    xs = np.linspace(0, xmax, samples)
    return np.column_stack([xs, prime_pi(xs)])


def _is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True


def block_counts(starts=(1, 1000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000), width=1000):
    """Primes in [s, s + width) for each start (the first block is 1..1000)."""
    return [sum(_is_prime(n) for n in range(s, s + width)) for s in starts]


# ------------------------------------------------------------------ smooth curves (mpmath)
def _mp():
    import mpmath as mp
    mp.mp.dps = 15
    return mp


def li(xs):
    mp = _mp()
    return np.array([float(mp.li(x)) for x in np.atleast_1d(xs)])


def R(xs):
    mp = _mp()
    return np.array([float(mp.riemannr(x)) for x in np.atleast_1d(xs)])


def _mobius(n):
    m, res, d = n, 1, 2
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            res = -res
        d += 1
    return -res if m > 1 else res


def base_curve(xs):
    xs = np.atleast_1d(np.asarray(xs, float))
    lx = np.log(xs)
    return R(xs) - 1 / lx + np.arctan(np.pi / lx) / np.pi


def _wave(rho, xs):
    mp = _mp()
    out = np.empty(len(xs))
    r = mp.mpc(rho.real, rho.imag)
    for i, x in enumerate(xs):
        lx = mp.log(x)
        nmax = int(float(lx) / np.log(2)) + 2
        s = mp.fsum(_mobius(n) / mp.mpf(n) * mp.ei(r * lx / n) for n in range(1, nmax + 1) if _mobius(n))
        out[i] = -2 * float(mp.re(s))
    return out


def _grid_name(xs):
    xs = np.asarray(xs, float)
    if xs.shape == LIN_X.shape and np.allclose(xs, LIN_X):
        return "lin"
    if xs.shape == LOG_X.shape and np.allclose(xs, LOG_X):
        return "log"
    return None


def _cached(name, fn):
    p = DATA / f"{name}.npy"
    if p.exists():
        return np.load(p)
    a = fn()
    tmp = DATA / f".{name}.{os.getpid()}.npy"
    np.save(tmp, a)
    os.replace(tmp, p)
    return a


def zero_wave(k, xs=LIN_X):
    """Wave of the k-th zero pair (k = 1 is γ = 14.1347)."""
    g = _grid_name(xs)
    rho = complex(0.5, ZEROS[k - 1])
    if g:
        return _cached(f"wave_{g}_{k}", lambda: _wave(rho, np.asarray(xs, float)))
    return _wave(rho, np.atleast_1d(np.asarray(xs, float)))


def rogue_wave(beta, gamma, xs=LOG_X):
    """Wave of a HYPOTHETICAL zero pair at beta ± i·gamma (illustration only)."""
    g = _grid_name(xs)
    rho = complex(beta, gamma)
    if g:
        return _cached(f"rogue_{g}_{beta:.3f}_{gamma:.4f}", lambda: _wave(rho, np.asarray(xs, float)))
    return _wave(rho, np.atleast_1d(np.asarray(xs, float)))


def envelope(beta, gamma, xs):
    xs = np.asarray(xs, float)
    return 2 * xs ** beta / (abs(complex(beta, gamma)) * np.log(xs))


def base_lin():
    return _cached("base_lin", lambda: base_curve(LIN_X))


def rebuild(n, xs=LIN_X):
    """Riemann's recipe with the first n zero pairs; on LIN_X it is fully cached (n ≤ 100)."""
    b = base_lin() if _grid_name(xs) == "lin" else base_curve(xs)
    return b + sum((zero_wave(k, xs) for k in range(1, n + 1)), np.zeros_like(b))


# ------------------------------------------------------------------ coin flips
def random_walks(seed=7, n=1_000_000, k=7, samples=2000):
    """(xs, walks[k, samples]): k fair ±1 walks of n steps, sampled at `samples` points (exact values there)."""
    rng = np.random.default_rng(seed)
    idx = np.linspace(0, n, samples).astype(int)
    walks = []
    for _ in range(k):
        s = np.concatenate([[0], np.cumsum(rng.integers(0, 2, n, dtype=np.int8) * 2 - 1, dtype=np.int64)])
        walks.append(s[idx])
    return idx.astype(float), np.array(walks, float)


# ------------------------------------------------------------------ zeta on the plane
_N = 48


@lru_cache(maxsize=1)
def _borwein_coeffs():
    mp = _mp()
    mp.mp.dps = 60
    dd = [_N * mp.fsum(mp.factorial(_N + i - 1) * mp.mpf(4) ** i / (mp.factorial(_N - i) * mp.factorial(2 * i))
                       for i in range(j + 1)) for j in range(_N + 1)]
    mp.mp.dps = 15
    return (-1.0) ** np.arange(_N) * np.array([float((dd[k] - dd[_N]) / dd[_N]) for k in range(_N)])


def _bor(z, chunk=200_000):
    E = _borwein_coeffs()
    out = np.empty(len(z), complex)
    kk = np.arange(_N)[:, None] + 1.0
    for i in range(0, len(z), chunk):
        zz = z[i:i + chunk]
        out[i:i + chunk] = -(E[:, None] / kk ** zz[None, :]).sum(0) / (1 - 2.0 ** (1 - zz))
    return out


def zeta_np(s):
    from scipy.special import gamma
    s = np.asarray(s, complex)
    flat = s.ravel()
    out = np.empty_like(flat)
    left = flat.real < 0.5
    out[~left] = _bor(flat[~left])
    l = flat[left]
    out[left] = 2.0 ** l * np.pi ** (l - 1) * np.sin(np.pi * l / 2) * gamma(1 - l) * _bor(1 - l)
    return out.reshape(s.shape)


def spiral_partial_sums(s, N=200):
    n = np.arange(1, N + 1, dtype=float)
    return np.concatenate([[0], np.cumsum(n ** (-complex(s)))])


def zeta_line_path(t0=0.0, t1=50.0, n=3000):
    t = np.linspace(t0, t1, n)
    return t, zeta_np(0.5 + 1j * t)


def domain_color_rgb(re0, re1, im0, im1, w, h, sat=0.5, val=0.8):
    """uint8 (h, w, 3) image of arg ζ over [re0, re1] × [im0, im1] (row 0 = top = im1). Hue = direction of the output."""
    re = np.linspace(re0, re1, w)
    im = np.linspace(im1, im0, h)
    z = zeta_np(re[None, :] + 1j * im[:, None])
    hue = (np.angle(z) / (2 * np.pi)) % 1.0
    i = np.floor(hue * 6).astype(int) % 6
    f = hue * 6 - np.floor(hue * 6)
    p, q, t = val * (1 - sat), val * (1 - sat * f), val * (1 - sat * (1 - f))
    v = np.full_like(hue, val)
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return (np.stack([r, g, b], -1) * 255).astype(np.uint8)


# ------------------------------------------------------------------ manim motifs
from common import *  # noqa: E402,F401,F403

if True:  # motif block (kept indented for readability)
    PRIME_COLOR = BLUE_P        # prime tiles and the prime staircase
    CURVE_COLOR = TEAL_P        # Gauss's curve li(x) and Riemann's sharpened curve R(x) / rebuilt curve
    WAVE_COLORS = [PINK_P, GREEN_P, PURPLE_P, ORANGE_P, BLUE_P]   # waves of zeros 1..5
    DIAL_TOP = -2.6             # every non-dial element stays above this y while the dial is on screen

    class ErrorDial(VGroup):
        """The error dial at its fixed home: ruler x -2.5..2.5 at y -3.2, ticks and Palatino labels 0, ½, 1.

        Parts (all built, in the S06+ "standard state"; use FadeIn(dial) or animate parts):
            panel, ruler, ticks, labels, cap_left ('error dial'), cap_right ('share of x's digits / in the error'),
            window (ACCENT ½..1), coin (+ coin_label 'coin flips'), pin (+ pin_label 'Riemann?'),
            check (+ check_label 'best possible'; from S08 P4 on, pass best=True)
        dial.x_of(v) -> scene x of reading v;  dial.marker(v, color=BAD) -> a small triangle marker at reading v.
        S03 builds it part by part: ErrorDial(window=False, coin=False, pin=False) then animate the parts in.
        """

        Y = -3.2
        X0, X1 = -2.5, 2.5

        def __init__(self, window=True, coin=True, pin=True, best=False, **kw):
            super().__init__(**kw)
            y = self.Y
            self.panel = Rectangle(width=12.4, height=1.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0.9, y - 0.05, 0])
            self.ruler = Line([self.X0, y, 0], [self.X1, y, 0], color=NEUTRAL, stroke_width=4)
            self.ticks = VGroup(*[Line([self.x_of(v), y - 0.12, 0], [self.x_of(v), y + 0.12, 0], color=NEUTRAL, stroke_width=4)
                                  for v in (0, 0.5, 1)])
            self.labels = VGroup(*[N(t, 28, INK).move_to([self.x_of(v), y - 0.42, 0]) for v, t in ((0, "0"), (0.5, "½"), (1, "1"))])
            self.cap_left = T("error dial", 24, DIM).next_to([self.X0, y, 0], LEFT, buff=0.45)
            self.cap_right = VGroup(T("share of x's digits", 24, DIM), T("in the error", 24, DIM)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            # top at y + 0.02: a clear gap under the row, so 'best possible' reads as the row's verdict, not a caption line
            self.cap_right.next_to([self.X1, y, 0], RIGHT, buff=0.45).align_to([0, y + 0.02, 0], UP)
            self.window = RoundedRectangle(corner_radius=0.08, width=self.x_of(1) - self.x_of(0.5) + 0.16, height=0.42,
                                           stroke_color=ACCENT, stroke_width=2.5, fill_color=ACCENT, fill_opacity=0.25
                                           ).move_to([(self.x_of(0.5) + self.x_of(1)) / 2, y, 0])
            row = y + 0.3   # one row above the ruler: [coin flips] (coin) (pin) [Riemann?] (check) [best possible]
            self.coin = VGroup(Circle(radius=0.11, color=ACCENT, stroke_width=2).set_fill(ACCENT, 1),
                               T("H", 14, BG, weight=BOLD)).move_to([self.x_of(0.5) - 0.18, row, 0])
            self.coin_label = T("coin flips", 24, DIM).next_to(self.coin, LEFT, buff=0.14)
            head = Circle(radius=0.08, color=ACCENT, stroke_width=0).set_fill(ACCENT, 1)
            tip = Triangle(color=ACCENT, stroke_width=0).set_fill(ACCENT, 1).scale(0.08).rotate(PI).next_to(head, DOWN, buff=-0.03)
            self.pin = VGroup(head, tip).move_to([self.x_of(0.5) + 0.18, row, 0])
            self.pin_label = T("Riemann?", 24, ACCENT).next_to(self.pin, RIGHT, buff=0.14)
            # 'Riemann?' sits over the window: lift the whole row so its text clears the ACCENT rim by 0.06
            # (the formula S03 used locally; row ≈ y + 0.39, its top stays below DIAL_TOP)
            lift = self.window.get_top()[1] + 0.06 - self.pin_label.get_bottom()[1]
            VGroup(self.coin, self.coin_label, self.pin, self.pin_label).shift(UP * lift)
            self.check =check_mark(self.pin_label.get_right() + RIGHT * 0.32, size=0.12)
            self.check_label = T("best possible", 24, DIM).next_to(self.check, RIGHT, buff=0.12)
            self.add(self.panel, self.window if window else VGroup(), self.ruler, self.ticks, self.labels, self.cap_left,
                     self.cap_right)
            if coin:
                self.add(self.coin, self.coin_label)
            if pin:
                self.add(self.pin, self.pin_label)
            if best:
                self.add(self.check, self.check_label)
            self.set_z_index(10)

        def x_of(self, v):
            return self.X0 + (self.X1 - self.X0) * v

        def marker(self, v, color=BAD):
            m = Triangle(color=color, stroke_width=0).set_fill(color, 1).scale(0.1).rotate(PI)
            return m.move_to([self.x_of(v), self.Y + 0.1, 0]).set_z_index(11)

    class StripMap:
        """Critical strip coordinates -> scene points: real part re in [0, 1] (or beyond), height h in [0, hmax]."""

        def __init__(self, x0, x1, y0, y1, hmax):
            self.x0, self.x1, self.y0, self.y1, self.hmax = x0, x1, y0, y1, hmax

        def p(self, re, h):
            return np.array([self.x0 + (self.x1 - self.x0) * re, self.y0 + (self.y1 - self.y0) * h / self.hmax, 0.0])

        def with_hmax(self, hmax):
            return StripMap(self.x0, self.x1, self.y0, self.y1, hmax)

    DIAL_ALIGNED = StripMap(-2.5, 2.5, -2.3, 3.4, 50)   # S06, S10: real parts sit exactly above the dial's ticks
    INSET = StripMap(4.2, 6.4, -2.4, 3.2, 50)           # S07, S08: small strip at the right
    INSET_240 = StripMap(4.2, 6.4, -2.4, 3.2, 240)      # S07 P3 on, S11: shows the first 100 zeros
    EVIDENCE = StripMap(-6.4, -2.6, -2.5, 3.2, 50)      # S09: strip at the left third

    def zero_dot(point, r=0.07):
        return pt(point, INK, r=r)

    def strip_group(m, n_zeros=10, labels=True, line=True, tint=True, dot_r=None):
        """VGroup(tint, edges, line, dots, floor_labels) for StripMap m. Access parts by attribute."""
        g = VGroup()
        w = m.x1 - m.x0
        g.tint = Rectangle(width=w, height=m.y1 - m.y0, stroke_width=0, fill_color=TEAL_P,
                           fill_opacity=0.18 if tint else 0).move_to([(m.x0 + m.x1) / 2, (m.y0 + m.y1) / 2, 0])
        g.edges = VGroup(Line(m.p(0, 0), m.p(0, m.hmax), color=NEUTRAL, stroke_width=2),
                         Line(m.p(1, 0), m.p(1, m.hmax), color=NEUTRAL, stroke_width=2))
        g.line = Line(m.p(0.5, 0), m.p(0.5, m.hmax), color=ACCENT, stroke_width=3 if line else 0)
        r = dot_r or (0.07 if n_zeros <= 10 else 0.045)
        g.dots = VGroup(*[zero_dot(m.p(0.5, h), r) for h in ZEROS[:n_zeros] if h <= m.hmax])
        size = 28 if w > 3 else 22
        g.floor_labels = VGroup(*[N(t, size, INK).next_to(m.p(v, 0), DOWN, buff=0.12) for v, t in ((0, "0"), (0.5, "½"), (1, "1"))])
        g.add(g.tint, g.edges, g.line, g.dots)
        if labels:
            g.add(g.floor_labels)
        return g

    def domain_image(re0, re1, im0, im1, x0, x1, y0, y1, px_per_unit=110, opacity=1.0):
        """ImageMobject of arg ζ over [re0, re1] × [im0, im1], stretched onto the scene rectangle [x0, x1] × [y0, y1]."""
        w = max(64, int((x1 - x0) * px_per_unit))
        h = max(64, int((y1 - y0) * px_per_unit))
        img = ImageMobject(domain_color_rgb(re0, re1, im0, im1, w, h))
        img.stretch_to_fit_width(x1 - x0).stretch_to_fit_height(y1 - y0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        img.set_opacity(opacity)
        return img


# ------------------------------------------------------------------ precompute + self-check
def precompute():
    from concurrent.futures import ProcessPoolExecutor
    DATA.mkdir(exist_ok=True)
    base_lin()
    jobs = [("zero", k, "lin") for k in range(1, 101)] + [("zero", k, "log") for k in (1, 2, 3, 4, 5)]
    rogues = [(0.8, ZEROS[0]), (0.2, ZEROS[0]), (0.3, 40.0), (0.7, 40.0)]
    with ProcessPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) - 2)) as ex:
        futs = [ex.submit(_job, j) for j in jobs] + [ex.submit(_rogue_job, b, g) for b, g in rogues]
        for f in futs:
            f.result()
    print("precomputed", len(jobs) + len(rogues), "waves")


def _job(j):
    _, k, g = j
    zero_wave(k, LIN_X if g == "lin" else LOG_X)


def _rogue_job(b, g):
    rogue_wave(b, g, LOG_X)


def self_check():
    mp = _mp()
    assert abs(ZEROS[0] - 14.134725141734693) < 1e-9 and abs(ZEROS[99] - 236.5242296658) < 1e-6
    assert list(prime_pi([100, 1000, 100_000, 1_000_000])) == [25, 168, 9592, 78498]
    assert block_counts() == [168, 135, 106, 81, 75, 61, 54], block_counts()
    L = li([1e5, 1e6, 1e8])
    assert np.allclose(L, [9629.809, 78627.549, 5762209.375], atol=0.01), L
    assert abs(R([100])[0] - 25.6616) < 1e-3
    z = zeta_np(np.array([2, 2 + 3j, 0.6 + 3j, 0.5, complex(0.5, ZEROS[0]), -2]))
    assert abs(z[0] - np.pi ** 2 / 6) < 1e-12 and abs(z[1] - (0.79802 - 0.11374j)) < 1e-4
    assert abs(z[2] - (0.55196 - 0.08592j)) < 1e-4 and abs(z[3] + 1.46035) < 1e-4 and abs(z[4]) < 1e-9 and abs(z[5]) < 1e-12
    for s in (0.3 + 20j, -5 + 11j, 4 - 25j):
        assert abs(zeta_np(np.array([s]))[0] - complex(mp.zeta(s))) < 1e-6 * abs(complex(mp.zeta(s)))
    half = np.arange(2.5, 100, 1.0)
    idx = np.searchsorted(LIN_X, half)
    err = np.abs(rebuild(100)[idx] - prime_pi(half))
    assert err.max() < 0.2, err.max()
    err10 = np.abs(rebuild(10)[idx] - prime_pi(half)).max()
    ratio = envelope(0.8, ZEROS[0], [1e6])[0] / envelope(0.5, ZEROS[0], [1e6])[0]
    assert 60 < ratio < 66, ratio
    xs, W = random_walks()
    print(f"topic.py ok: rebuild(100) max err {err.max():.3f}, rebuild(10) {err10:.3f}; rogue/line envelope at 1e6 = {ratio:.1f}x;"
          f" walk ends {np.round(W[:, -1]).astype(int).tolist()}")


if __name__ == "__main__":
    if "--precompute" in sys.argv:
        precompute()
    self_check()

