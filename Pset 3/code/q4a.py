"""
Pset 3, Question 4(a) -- solve PD(s) by function iteration on Equation 4.1 and plot it against
S = e^s. Model, student specification, decisions and numerical method: code/q4_model.py.

Outputs (paths relative to "Pset 3"): output/q4a_pd.csv, output/q4a_pd.png, output/q4a_summary.md
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import q4_model as m


def monte_carlo_pd(Sb: float, n_paths: int = 60000, years: int = 200, seed: int = 1) -> tuple[float, float]:
    """PD(sbar) as the sum of simulated dividend-strip prices under the measure with density
    M/E[M]; independent of the grid solution. Needs the exact Sbar, for which E[M] = exp(-rf)
    holds at every s <= s_max."""
    rng = np.random.default_rng(seed)
    sb, sm = m.s_bar_max(Sb)
    x = np.zeros(n_paths)
    log_v, total = np.zeros(n_paths), np.zeros(n_paths)
    for _ in range(12 * years):
        l = m.lam(sb + x, Sb)
        dc = -m.GAMMA * (1 + l) * m.SIG_C ** 2 + m.SIG_C * rng.standard_normal(n_paths)
        log_em = np.where(x <= sm - sb, -m.RF, np.log(m.DELTA) - m.GAMMA * m.G + m.GAMMA * (1 - m.PHI) * x
                          + 0.5 * m.GAMMA ** 2 * (1 + l) ** 2 * m.SIG_C ** 2)
        log_v += log_em + m.G + m.RHO * m.SIG_D / m.SIG_C * dc + 0.5 * (1 - m.RHO ** 2) * m.SIG_D ** 2
        x = m.PHI * x + l * dc
        total += np.exp(log_v)
    return total.mean(), total.std() / np.sqrt(n_paths)


def main() -> None:
    sol = m.solve()
    s, PD = sol["s"], sol["PD"]
    s_bar, s_max = m.s_bar_max()
    at = lambda S: float(sol["fn"](np.log(S)))
    pd.DataFrame({"s": s, "S": np.exp(s), "PD": PD, "PD_annualized": PD / 12, "lambda": m.lam(s)}).to_csv(
        m.OUT_DIR / "q4a_pd.csv", index=False)

    S = np.linspace(1e-4, np.exp(s_max), 1500)
    fig, ax = plt.subplots(figsize=(6.5, 4.0), facecolor=m.SURFACE)
    m.style(ax)
    ax.plot(S, sol["fn"](np.log(S)), color=m.BLUE, linewidth=2, solid_capstyle="round")
    ax.plot([m.S_BAR], [at(m.S_BAR)], "o", color=m.BLUE, markersize=8, markeredgecolor=m.SURFACE, markeredgewidth=2)
    ax.annotate(rf"$\bar S = {m.S_BAR}$: {at(m.S_BAR):.1f}", (m.S_BAR, at(m.S_BAR)), xytext=(8, -18),
                textcoords="offset points", color=m.INK2, fontsize=9)
    ax.set_xlim(0, np.exp(s_max) * 1.03)
    ax.set_ylim(0, None)
    ax.set_xlabel("Surplus consumption ratio $S = e^s$")
    ax.set_ylabel("$PD(s) = P_t / D_t$, monthly dividends")
    ax.set_title("Q4(a): price-dividend ratio", fontsize=11, loc="left")
    fig.tight_layout()
    fig.savefig(m.OUT_DIR / "q4a_pd.png", dpi=200, facecolor=m.SURFACE)
    plt.close(fig)

    pts = [0.005, 0.01, 0.02, 0.04, m.S_BAR, 0.08, np.exp(s_max)]
    md = ["| $S$ | 0.005 | 0.01 | 0.02 | 0.04 | 0.057 ($\\bar S$) | 0.08 | 0.0938 ($S_{max}$) |",
          "|---|" + "---:|" * len(pts),
          "| $PD(s)$ | " + " | ".join(f"{at(v):.1f}" for v in pts) + " |",
          "| $PD(s)/12$ | " + " | ".join(f"{at(v) / 12:.2f}" for v in pts) + " |", "",
          f"$PD(s)$ from function iteration on Equation 4.1 ({sol['n_iter']:,} iterations, largest relative change "
          f"below $10^{{-11}}$) with numerical integration over both shocks. The grid for $s$ extends far below the "
          f"simulated range, until its lower bound no longer affects the solution. $PD(s)/12$ is the price relative "
          f"to annual dividends."]
    (m.OUT_DIR / "q4a_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---- convergence and cross-checks ----------------------------------------------------
    rel = lambda alt: max(abs(float(alt["fn"](np.log(v))) / at(v) - 1) for v in pts)
    print(f"{len(s)} grid points, {sol['n_iter']} iterations; PD/12 at S_bar = {at(m.S_BAR) / 12:.4f}")
    print(f"  vs direct linear solve:                 {rel(m.solve(direct=True)):.1e}")
    print(f"  PD = 0 (instead of held) below grid:    {rel(m.solve(zero_below=True, direct=True)):.1e}")
    print(f"  lower bound -3000, +/-30 s.d.:          {rel(m.solve(lower=-3000.0, zmax=30.0, n_c=1801, direct=True)):.1e}")
    print(f"  grid x0.6:                              {rel(m.solve(scale=0.6, direct=True)):.1e}")
    print(f"  grid x1.4:                              {rel(m.solve(scale=1.4, direct=True)):.1e}")
    print(f"  dc nodes x2:                            {rel(m.solve(n_c=2401, direct=True)):.1e}")
    for lower in (-13.0, -60.0, -250.0, -1000.0):
        v = [float(m.solve(lower=lower, zero_below=z, direct=True)["fn"](s_bar)) / 12 for z in (False, True)]
        print(f"  bound {lower:7.0f}: PD/12 at S_bar, held {v[0]:.3f}, zero {v[1]:.3f}")
    exact = m.SIG_C * np.sqrt(m.GAMMA / (1 - m.PHI))
    grid_exact = float(m.solve(Sb=exact, direct=True)["fn"](np.log(exact))) / 12
    mc, se = monte_carlo_pd(exact)
    print(f"  exact S_bar = {exact:.6f}: grid PD/12 = {grid_exact:.3f}, Monte Carlo = {mc / 12:.3f} (s.e. {se / 12:.3f})")


if __name__ == "__main__":
    main()
