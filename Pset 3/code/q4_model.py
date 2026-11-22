"""
Pset 3, Question 4 -- Campbell-Cochrane (1999) habit model: parameters, state dynamics and the
numerical solution of Equation 4.1, shared by q4a.py, q4b.py and q4c.py.

Parameters and equations: Problem Set 3, Question 4 (monthly values):
    PD(s)  = E[ f(s, dc, dd) (1 + PD(s')) ],   s' = (1-phi) sbar + phi s + lambda(s) dc   (4.1)
    f      = exp{ log(delta) + (1-gamma) g + gamma (1-phi)(s - sbar)
                  - gamma (1 + lambda(s)) dc + dd }                                       (4.2)
    lambda = (1/Sbar) sqrt(1 - 2 (s - sbar)) - 1 for s <= s_max, 0 for s >= s_max         (4.3)
    s_max  = sbar + (1 - Sbar^2)/2                                                        (4.4)
    (dc, dd) iid jointly normal, mean zero, s.d. sigma_c, sigma_d, correlation rho        (4.5)

Student specification (2026-11-22): numerical integration for the expectation (dc and dd
normal) and function iteration on Equation 4.1.

Decision made by the student when AI flagged it (2026-11-22): how PD is treated near S = 0.
  * Main results: the converged solution. The grid for s extends down until its lower bound no
    longer matters. (The s process rarely visits that region, but the expectation in 4.1 puts a
    large weight on it. With the grid cut at s - sbar = -13, i.e. S = 1.3e-7, PD(sbar)/12 is 34.0
    if PD is held constant below the grid and 21.2 if it is set to zero; with the cut at -1000
    the two agree at 27.80.)
  * Comparison row in 4(c) only: 500 even points in S, linear interpolation in S, PD = 0 at S = 0.

Numerical implementation (programming choices; convergence is checked in q4a.py):
  * Expectation: two-dimensional numerical integration. dc by the trapezoid rule over +/- 20
    standard deviations (wide because the weight f is centered near z = -gamma (1 + lambda)
    sigma_c, which is -6.8 at the bottom of the grid); dd given dc, normal with mean
    rho (sigma_d/sigma_c) dc and variance (1 - rho^2) sigma_d^2, by Gauss-Hermite quadrature.
  * PD is interpolated linearly between grid points, so one application of the right-hand side
    of 4.1 is PD_{n+1} = k0 + K PD_n, with k0(s) = E[f]. Function iteration starts from
    PD_0 = 0 and stops when the largest relative change is below 1e-11.
  * s can exceed s_max; the grid extends to s - sbar = 0.8 (from s <= s_max an 8-s.d. shock
    reaches at most 0.646).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 3
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

# ---- Problem Set 3, Question 4 calibration (monthly) ------------------------------------
G = 0.0189 / 12
SIG_C = 0.0150 / np.sqrt(12)
SIG_D = 0.112 / np.sqrt(12)
RHO = 0.2
PHI = 0.87 ** (1 / 12)
DELTA = 0.89 ** (1 / 12)
GAMMA = 2.00
S_BAR = 0.057
RF = -np.log(DELTA) + GAMMA * G - GAMMA / 2 * (1 - PHI)          # Equations 4.8 / 4.13

# ---- chart style -------------------------------------------------------------------------
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def s_bar_max(Sb: float = S_BAR) -> tuple[float, float]:
    sb = np.log(Sb)
    return sb, sb + 0.5 * (1 - Sb ** 2)


def lam(s: np.ndarray, Sb: float = S_BAR) -> np.ndarray:
    sb, sm = s_bar_max(Sb)
    return np.where(s <= sm, np.sqrt(np.maximum(1 - 2 * (s - sb), 0.0)) / Sb - 1, 0.0)


def next_state(s: np.ndarray, dc: np.ndarray, Sb: float = S_BAR) -> np.ndarray:
    sb, _ = s_bar_max(Sb)
    return (1 - PHI) * sb + PHI * s[:, None] + lam(s, Sb)[:, None] * dc[None, :]


def shocks_c(zmax: float = 20.0, n: int = 1201) -> tuple[np.ndarray, np.ndarray]:
    """Trapezoid nodes and probability weights for dc on [-zmax, zmax] standard deviations."""
    z = np.linspace(-zmax, zmax, n)
    w = np.exp(-0.5 * z ** 2)
    w[[0, -1]] *= 0.5
    return SIG_C * z, w / w.sum()


def dd_nodes(dc: np.ndarray, n: int = 21) -> tuple[np.ndarray, np.ndarray]:
    """Gauss-Hermite nodes (len(dc) x n) and weights for dd given dc."""
    x, w = np.polynomial.hermite_e.hermegauss(n)
    return RHO * SIG_D / SIG_C * dc[:, None] + SIG_D * np.sqrt(1 - RHO ** 2) * x[None, :], w / w.sum()


def f_weights(s: np.ndarray, dc: np.ndarray, w: np.ndarray, Sb: float = S_BAR) -> np.ndarray:
    """w_k E[f(s_i, dc_k, dd) | dc_k], integrating dd numerically (Equation 4.2)."""
    sb, _ = s_bar_max(Sb)
    dd, wd = dd_nodes(dc)
    e_dd = np.exp(dd) @ wd
    log_f = (np.log(DELTA) + (1 - GAMMA) * G + GAMMA * (1 - PHI) * (s - sb)[:, None]
             - GAMMA * (1 + lam(s, Sb))[:, None] * dc[None, :])
    return np.exp(log_f + np.log(w * e_dd)[None, :])


def interpolation_matrix(W: np.ndarray, q: np.ndarray, nodes: np.ndarray, zero_below: bool) -> np.ndarray:
    """sum_k W_ik v(q_ik) as a matrix in v, v linear between `nodes`; below nodes[0], v is held
    at its first value or set to zero."""
    qc = np.clip(q, nodes[0], nodes[-1])
    j = np.clip(np.searchsorted(nodes, qc, side="right") - 1, 0, len(nodes) - 2)
    t = (qc - nodes[j]) / (nodes[j + 1] - nodes[j])
    Wq = np.where(q < nodes[0], 0.0, W) if zero_below else W
    K = np.zeros((W.shape[0], len(nodes)))
    rows = np.broadcast_to(np.arange(W.shape[0])[:, None], j.shape)
    np.add.at(K, (rows, j), Wq * (1 - t))
    np.add.at(K, (rows, j + 1), Wq * t)
    return K


def iterate(k0: np.ndarray, K: np.ndarray, tol: float = 1e-11, max_iter: int = 60000) -> tuple[np.ndarray, int]:
    """Function iteration on Equation 4.1 from PD_0 = 0."""
    pd_old = np.zeros(len(k0))
    for n in range(1, max_iter + 1):
        pd_new = k0 + K @ pd_old
        if n > 1 and np.max(np.abs(pd_new / pd_old - 1.0)) < tol:
            return pd_new, n
        pd_old = pd_new
    raise RuntimeError("function iteration did not converge")


def s_grid(lower: float = -1000.0, scale: float = 1.0, Sb: float = S_BAR) -> np.ndarray:
    """Grid for s: geometric spacing below s - sbar = -2, dense around s_max."""
    sb, sm = s_bar_max(Sb)
    n = lambda k: int(round(k * scale))
    x = np.concatenate([
        -np.geomspace(-lower, 2.0, n(350 * np.log(-lower / 2.0)), endpoint=False),
        np.linspace(-2.0, 0.40, n(600), endpoint=False),
        np.linspace(0.40, 0.55, n(450), endpoint=False),
        np.linspace(0.55, 0.80, n(50)),
        [0.0, sm - sb],
    ])
    return sb + np.unique(x)


def solve(lower: float = -1000.0, scale: float = 1.0, zmax: float = 20.0, n_c: int = 1201,
          zero_below: bool = False, Sb: float = S_BAR, direct: bool = False) -> dict:
    """PD(s) on the s-grid: by function iteration, or (direct=True) by one linear solve."""
    s = s_grid(lower, scale, Sb)
    dc, w = shocks_c(zmax, n_c)
    W = f_weights(s, dc, w, Sb)
    K = interpolation_matrix(W, next_state(s, dc, Sb), s, zero_below)
    k0 = W.sum(axis=1)
    if direct:
        pd, n = np.linalg.solve(np.eye(len(s)) - K, k0), 0
    else:
        pd, n = iterate(k0, K)
    fn = (lambda q: np.interp(q, s, pd, left=0.0)) if zero_below else (lambda q: np.interp(q, s, pd))
    return dict(s=s, PD=pd, n_iter=n, fn=fn)


def solve_even_S(n_points: int = 500) -> dict:
    """Comparison for 4(c): n_points even points in S, PD linear in S, PD = 0 at S = 0."""
    S = np.unique(np.r_[np.linspace(0, np.exp(s_bar_max()[1]) * 1.17, n_points + 1)[1:],
                        np.exp(s_bar_max()[1]), S_BAR])
    dc, w = shocks_c(10.0, 801)
    W = f_weights(np.log(S), dc, w)
    nodes = np.r_[0.0, S]
    K = interpolation_matrix(W, np.exp(next_state(np.log(S), dc)), nodes, zero_below=False)[:, 1:]
    pd, n = iterate(W.sum(axis=1), K)
    return dict(S=S, PD=pd, n_iter=n, fn=lambda q: np.interp(np.exp(q), nodes, np.r_[0.0, pd]))


def style(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK2, length=0)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)
    ax.title.set_color(INK)
