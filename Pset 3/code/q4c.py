"""
Pset 3, Question 4(c) -- simulate the Campbell-Cochrane economy (500,000 months, Equations
4.9-4.13) given PD(s) from Question 4(a), and report E[r - rf], sigma[r - rf] and their ratio
for annual log returns. Model, student decisions and numerical method: code/q4_model.py.

  * Shocks: (dc_t, dd_t) jointly normal (Equation 4.5), numpy default_rng(SEED); s_0 = sbar, no
    burn-in (footnote 11).
  * Annual returns: sums of 12 monthly log returns over non-overlapping years. 500,000 months
    are 41,666 full years; the last 8 months are dropped. sigma uses divisor (years - 1).
  * Comparison row (student's decision): the same shocks with PD solved on 500 even points in S,
    linear interpolation in S and PD = 0 at S = 0.

Outputs (paths relative to "Pset 3"): output/q4c_moments.csv, output/q4c_table.md
"""

from math import sqrt

import numpy as np
import pandas as pd

import q4_model as m

T_MONTHS = 500_000
SEED = 8200


def simulate_shocks(seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    z = np.random.default_rng(seed).standard_normal((T_MONTHS, 2))
    dc = m.SIG_C * z[:, 0]
    dd = m.SIG_D * (m.RHO * z[:, 0] + np.sqrt(1 - m.RHO ** 2) * z[:, 1])
    return dc, dd


def simulate_state(dc: np.ndarray) -> np.ndarray:
    """s_0 = sbar and Equation 4.9 for t = 1..T."""
    s_bar, s_max = m.s_bar_max()
    s = np.empty(len(dc) + 1)
    s[0] = cur = s_bar
    const = (1 - m.PHI) * s_bar
    for t, e in enumerate(dc.tolist()):
        l = sqrt(1 - 2 * (cur - s_bar)) / m.S_BAR - 1 if cur <= s_max else 0.0
        cur = const + m.PHI * cur + l * e
        s[t + 1] = cur
    return s


def annual_moments(s: np.ndarray, dd: np.ndarray, pd_fn) -> dict:
    PD = pd_fn(s)
    re = m.G + dd + np.log1p(PD[1:]) - np.log(PD[:-1])            # Equations 4.10-4.12
    years = len(re) // 12
    xr = re[: 12 * years].reshape(years, 12).sum(axis=1) - 12 * m.RF
    mean, sd = xr.mean(), xr.std(ddof=1)
    return dict(mean_pct=100 * mean, sd_pct=100 * sd, ratio=mean / sd, years=years,
                exp_mean_pd_annual=float(np.exp(np.log(PD).mean()) / 12))


def main() -> None:
    main_fn, comp_fn = m.solve()["fn"], m.solve_even_S(500)["fn"]
    dc, dd = simulate_shocks()
    s = simulate_state(dc)
    rows = {"converged": annual_moments(s, dd, main_fn), "even_S_500_PD0": annual_moments(s, dd, comp_fn)}
    pd.DataFrame(rows).T.rename_axis("solution").to_csv(m.OUT_DIR / "q4c_moments.csv")

    a, b = rows["converged"], rows["even_S_500_PD0"]
    md = ["| $PD(s)$ solution | $\\mathbb{E}[r - r_f]$ (%) | $\\sigma[r - r_f]$ (%) | $\\mathbb{E}[r - r_f]/\\sigma[r - r_f]$ |",
          "|---|---:|---:|---:|",
          f"| Converged (main result) | {a['mean_pct']:.2f} | {a['sd_pct']:.2f} | {a['ratio']:.3f} |",
          f"| Comparison: 500 even points in $S$, $PD = 0$ at $S = 0$ | {b['mean_pct']:.2f} | {b['sd_pct']:.2f} | {b['ratio']:.3f} |",
          "", f"Annual log returns (sums over 12 months, non-overlapping) from {T_MONTHS:,} simulated months "
              f"({a['years']:,} full years), $s_0 = \\bar s$; annual $r_f$ = {1200 * m.RF:.2f}%. Both rows use the same "
              f"simulated shocks. The comparison row solves Equation 4.1 on a grid that is even in $S$ with $PD$ "
              f"interpolated linearly in $S$ down to $PD = 0$ at $S = 0$; it changes with the number of grid points."]
    (m.OUT_DIR / "q4c_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    s_bar, s_max = m.s_bar_max()
    print(pd.DataFrame(rows).T.round(4).to_string())
    print(f"s - sbar from {s.min() - s_bar:.3f} to {s.max() - s_bar:.3f}; share above s_max {np.mean(s > s_max):.4f}; "
          f"corr(dc, dd) = {np.corrcoef(dc, dd)[0, 1]:.4f}, sd {dc.std() / m.SIG_C:.4f}, {dd.std() / m.SIG_D:.4f} of target")
    reps = {"converged": [], "even_S_500_PD0": []}
    for seed in range(20):
        dc_, dd_ = simulate_shocks(seed)
        s_ = simulate_state(dc_)
        for nm, fn in (("converged", main_fn), ("even_S_500_PD0", comp_fn)):
            r = annual_moments(s_, dd_, fn)
            reps[nm].append((r["mean_pct"], r["sd_pct"], r["ratio"]))
    for nm, v in reps.items():
        v = np.array(v)
        print(f"  20 other seeds, {nm}: mean {v.mean(0).round(3)}, s.d. across seeds {v.std(0, ddof=1).round(3)}")


if __name__ == "__main__":
    main()
