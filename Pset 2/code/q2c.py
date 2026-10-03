"""
Pset 2, Question 2(c) -- the SDF M*_t = a - b' xR_t that prices the excess returns of
the 20 portfolios in the merge of the BM and MOM datasets, and the Sharpe ratios of
xR*_t = b' xR_t from Questions 2(a), 2(b) and 2(c).

Student specification (as given, 2026-10-03):
  "Repeat Question (2a), but this time using the excess returns of the 20 portfolios in
   the merge of the BM Dataset and the MOM Dataset. For the scatterplot, still have the
   portfolio deciles (1 to 10) in the x-axis, but use different colors for the dots
   associated with different sorting variables (blue for BM portfolios and red for MOM
   portfolios). Calculate and report the Sharpe ratios of the xR*_t = b' xR_t portfolios
   obtained in Questions (2a), (2b) and (2c)."

"Repeat Question (2a)" carries over every Q2(a) choice (see code/q2a.py): value-weighted
monthly returns, 1927:07 to 2026:08, xR_t = (R_t - RF_t) / 100, E[M* xR] = 0 and
E[M*] = 1, two-step GMM, Newey-West S with the automatic Newey-West (1994) lag.
xR_t stacks the 10 BM deciles (b_1..b_10) and then the 10 MOM deciles (b_11..b_20).
Both datasets cover every month of the sample, so the merge drops no months.

Decision made by the student when AI flagged it (2026-10-03):
  * Sharpe ratio: annualized only, SR = sqrt(12) * mean(xR*_t) / sd(xR*_t), from the
    monthly series; sd is the sample standard deviation (divisor T - 1).

Outputs (paths relative to "Pset 2"):
  output/q2c_gmm.csv, output/q2c_gmm_table.md, output/q2c_b_scatter.png,
  output/q2c_sharpe.csv, output/q2c_sharpe_table.md
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from q2a import (DECILES, OUT_DIR, estimate_sdf, load_excess_returns, print_summary,
                 save_results)
from q2b import MOM_CSV, MOM_DECILES

MONTHS_PER_YEAR = 12


def annualized_sharpe(fit: dict, xr: pd.DataFrame) -> float:
    """SR of xR*_t = b' xR_t: sqrt(12) * mean / sd (sd with divisor T - 1)."""
    xr_star = xr.to_numpy() @ fit["theta"][1:]
    return np.sqrt(MONTHS_PER_YEAR) * xr_star.mean() / xr_star.std(ddof=1)


def main() -> None:
    xr_bm = load_excess_returns()
    xr_mom = load_excess_returns(MOM_CSV, MOM_DECILES)
    xr_all = pd.concat([xr_bm, xr_mom], axis=1, join="inner")
    assert len(xr_all) == len(xr_bm) == len(xr_mom), "merge dropped months"
    columns = DECILES + MOM_DECILES

    fit = estimate_sdf(xr_all)
    res = save_results(fit, xr_all, columns, "q2c", plot=False)
    print_summary(fit, xr_all, res)

    b = fit["theta"][1:]
    deciles = np.arange(1, 11)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.scatter(deciles, b[:10], color="blue", label="BM portfolios", zorder=3)
    ax.scatter(deciles, b[10:], color="red", label="MOM portfolios", zorder=3)
    ax.axhline(0.0, color="grey", linewidth=0.8)
    ax.set_xticks(deciles)
    ax.set_xlabel("Portfolio decile (1 = Lo, 10 = Hi)")
    ax.set_ylabel(r"$b$ coefficient")
    ax.set_title(r"Q2(c): $b$ in $M^*_t = a - b'xR_t$, BM + MOM deciles")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "q2c_b_scatter.png", dpi=200)
    plt.close(fig)

    fits = {
        "2(a)": ("10 BM deciles", estimate_sdf(xr_bm), xr_bm),
        "2(b)": ("10 MOM deciles", estimate_sdf(xr_mom), xr_mom),
        "2(c)": ("20 BM + MOM deciles", fit, xr_all),
    }
    sharpe = pd.DataFrame(
        [{"question": q, "portfolios": desc, "sharpe_annualized": annualized_sharpe(f, x)}
         for q, (desc, f, x) in fits.items()]
    )
    sharpe.to_csv(OUT_DIR / "q2c_sharpe.csv", index=False)

    rows = ["| Question | Test assets | Annualized Sharpe ratio of $xR^*_t = b'xR_t$ |",
            "|---|---|---:|"]
    rows += [f"| {r.question} | {r.portfolios} | {r.sharpe_annualized:.4f} |"
             for r in sharpe.itertuples()]
    note = (f"\nMonthly {xr_all.index[0].strftime('%Y:%m')}–{xr_all.index[-1].strftime('%Y:%m')} "
            f"(T = {len(xr_all)}); Sharpe ratio = $\\sqrt{{12}}$ × mean / s.d. of the monthly "
            f"$xR^*_t$ series.\n")
    (OUT_DIR / "q2c_sharpe_table.md").write_text("\n".join(rows) + "\n" + note, encoding="utf-8")

    print()
    print(sharpe.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
