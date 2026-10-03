"""
Pset 2, Question 2(b) -- the SDF M*_t = a - b' xR_t that prices the excess returns of
the 10 momentum decile portfolios, and its correlation with the Q2(a) SDF.

Student specification (as given, 2026-10-03):
  "Data/10_Portfolios_Prior_12_2.csv has return of 10 portfolios, MOM. do the same as
   2a and report the same figures and tables. after that, calculate and report the
   correlation between two SDF you constructed."

"The same as 2a" carries over every Q2(a) choice (see code/q2a.py):
  * Data: block "Value Weight Returns -- Monthly", columns Lo PRIOR, PRIOR 2, ...,
    PRIOR 9, Hi PRIOR; RF from Data/F-F_Research_Data_Factors.csv.
  * Sample 1927:07 to 2026:08; xR_t = (R_t - RF_t) / 100 (decimals).
  * M*_t = a - b' xR_t with E[M* xR] = 0 and E[M*] = 1; two-step GMM;
    Newey-West S with the automatic Newey-West (1994) lag.
  * Same outputs: estimates table (csv + md) and scatterplot of b by decile.

Correlation: sample correlation between the fitted M*_t series from Q2(a) (BM) and
from Q2(b) (MOM), over their common months (1927:07 to 2026:08).

Outputs (paths relative to "Pset 2"):
  output/q2b_gmm.csv, output/q2b_gmm_table.md, output/q2b_b_scatter.png,
  output/q2b_sdf_series.csv (both M*_t series), output/q2b_sdf_corr.csv
"""

import numpy as np
import pandas as pd

from q2a import (DECILES, OUT_DIR, PSET_DIR, estimate_sdf, load_excess_returns,
                 print_summary, save_results)

MOM_CSV = PSET_DIR / "Data" / "10_Portfolios_Prior_12_2.csv"
MOM_DECILES = ["Lo PRIOR", "PRIOR 2", "PRIOR 3", "PRIOR 4", "PRIOR 5",
               "PRIOR 6", "PRIOR 7", "PRIOR 8", "PRIOR 9", "Hi PRIOR"]


def main() -> None:
    xr_mom = load_excess_returns(MOM_CSV, MOM_DECILES)
    fit_mom = estimate_sdf(xr_mom)
    res = save_results(
        fit_mom, xr_mom, MOM_DECILES, "q2b",
        xlabel="Momentum decile (1 = Lo PRIOR, 10 = Hi PRIOR)",
        title=r"Q2(b): $b$ in $M^*_t = a - b'xR_t$, MOM deciles",
    )
    print_summary(fit_mom, xr_mom, res)

    # Q2(a) SDF, re-estimated with the same code so both series come from one run.
    fit_bm = estimate_sdf(load_excess_returns())
    m = pd.concat({"M_star_BM": fit_bm["m_star"], "M_star_MOM": fit_mom["m_star"]},
                  axis=1, join="inner")
    assert len(m) == len(fit_bm["m_star"]) == len(fit_mom["m_star"])
    corr = np.corrcoef(m["M_star_BM"], m["M_star_MOM"])[0, 1]

    m.index = m.index.astype(str)
    m.index.name = "month"
    m.to_csv(OUT_DIR / "q2b_sdf_series.csv")
    pd.DataFrame(
        {"corr_M_BM_M_MOM": [corr], "T": [len(m)],
         "start": [m.index[0]], "end": [m.index[-1]]}
    ).to_csv(OUT_DIR / "q2b_sdf_corr.csv", index=False)

    print()
    print(f"corr(M*_BM, M*_MOM) = {corr:.4f}  over {m.index[0]} to {m.index[-1]} (T = {len(m)})")
    print(m.describe().loc[["mean", "std", "min", "max"]].to_string(float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
