"""
Pset 3, Question 4(b) -- expected log equity return E r_e(s), Equation 4.6, given PD(s) from
Question 4(a), plotted with r_f (Equation 4.8) against S = e^s; both annualized by multiplying
by 12 (footnote 10). Model and numerical method: code/q4_model.py.

The expectation is computed with the same numerical integration as in 4(a): trapezoid rule for
dc (here over +/- 8 standard deviations, because 4.6 has no f weight) and Gauss-Hermite for dd.

Outputs (paths relative to "Pset 3"): output/q4b_er.csv, output/q4b_er.png, output/q4b_summary.md
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import q4_model as m


def expected_return(s: np.ndarray, pd_fn, zmax: float = 8.0, n_c: int = 1601) -> np.ndarray:
    """E r_e(s) of Equation 4.6 (monthly)."""
    dc, w = m.shocks_c(zmax, n_c)
    dd, wd = m.dd_nodes(dc)
    growth = (w[:, None] * (m.G + dd) * wd[None, :]).sum()
    log_1_pd = np.log1p(pd_fn(m.next_state(s, dc)))
    return growth + log_1_pd @ w - np.log(pd_fn(s))


def main() -> None:
    sol = m.solve()
    _, s_max = m.s_bar_max()
    S = np.unique(np.r_[np.linspace(5e-4, np.exp(s_max), 1500), m.S_BAR])
    er = expected_return(np.log(S), sol["fn"])
    pd.DataFrame({"S": S, "Er_monthly": er, "Er_annualized": 12 * er, "rf_annualized": 12 * m.RF}).to_csv(
        m.OUT_DIR / "q4b_er.csv", index=False)

    fig, ax = plt.subplots(figsize=(6.5, 4.0), facecolor=m.SURFACE)
    m.style(ax)
    ax.plot(S, 1200 * er, color=m.BLUE, linewidth=2, label=r"$12 \times \mathbb{E}r_e(s)$", solid_capstyle="round")
    ax.plot(S, np.full_like(S, 1200 * m.RF), color=m.ORANGE, linewidth=2, label=r"$12 \times r_f$", solid_capstyle="round")
    ax.set_xlim(0, np.exp(s_max) * 1.03)
    ax.set_ylim(0, None)
    ax.set_xlabel("Surplus consumption ratio $S = e^s$")
    ax.set_ylabel("Percent per year")
    ax.set_title("Q4(b): expected log equity return and risk-free rate", fontsize=11, loc="left")
    ax.legend(frameon=False, labelcolor=m.INK2)
    fig.tight_layout()
    fig.savefig(m.OUT_DIR / "q4b_er.png", dpi=200, facecolor=m.SURFACE)
    plt.close(fig)

    pts = [0.005, 0.01, 0.02, 0.04, m.S_BAR, 0.08, np.exp(s_max)]
    val = 1200 * expected_return(np.log(np.array(pts)), sol["fn"])
    md = ["| $S$ | 0.005 | 0.01 | 0.02 | 0.04 | 0.057 ($\\bar S$) | 0.08 | 0.0938 ($S_{max}$) |",
          "|---|" + "---:|" * len(pts),
          "| $12 \\times \\mathbb{E}r_e(s)$ (%) | " + " | ".join(f"{v:.2f}" for v in val) + " |",
          "| $12 \\times r_f$ (%) | " + " | ".join([f"{1200 * m.RF:.2f}"] * len(pts)) + " |", "",
          "Expected log equity return (Equation 4.6) given the $PD(s)$ of 4(a), and $r_f$ (Equation 4.8), both "
          "multiplied by 12."]
    (m.OUT_DIR / "q4b_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("12 x Er_e (%) at S =", dict(zip([round(float(p), 4) for p in pts], np.round(val, 4))), "; 12 x rf = %.4f" % (1200 * m.RF))
    for nm, alt in (("more dc nodes, wider", 1200 * expected_return(np.log(np.array(pts)), sol["fn"], 10.0, 4001)),
                    ("PD grid x1.4", 1200 * expected_return(np.log(np.array(pts)), m.solve(scale=1.4, direct=True)["fn"])),
                    ("PD zero below grid", 1200 * expected_return(np.log(np.array(pts)), m.solve(zero_below=True, direct=True)["fn"]))):
        print(f"  {nm}: max change {np.abs(alt - val).max():.1e} percentage points")


if __name__ == "__main__":
    main()
