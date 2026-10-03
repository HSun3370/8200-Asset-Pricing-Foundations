"""
Pset 2, Question 2(d) -- pricing errors of the 20 BM + MOM decile portfolios under each
of the three SDFs M*_t from Questions 2(a), 2(b) and 2(c).

Student specification (as given, 2026-10-03):
  "for each 20 portfolios, calculate pricing error using three SDF. pricing errors are
   alpha_p = E[xR_p] - Cov(-M*, xR_p), E[xR_p] should using realized average."

Carried over from Questions 2(a)-2(c) (see code/q2a.py, q2b.py, q2c.py): the three M*_t
series are the fitted two-step GMM SDFs; value-weighted monthly returns,
1927:07 to 2026:08, xR_t = (R_t - RF_t) / 100.

Decisions made by the student when AI flagged them (2026-10-03):
  * Cov divisor: T, i.e. Cov(-M, x) = (1/T) sum_t (-M_t + M_bar)(x_t - x_bar).
  * Units of the reported alpha: percent per month (monthly decimal alpha x 100).

Outputs (paths relative to "Pset 2"):
  output/q2d_pricing_errors.csv, output/q2d_pricing_errors_table.md
"""

import numpy as np
import pandas as pd

from q2a import DECILES, OUT_DIR, estimate_sdf, load_excess_returns
from q2b import MOM_CSV, MOM_DECILES

PCT = 100.0


def pricing_errors(m: pd.Series, xr: pd.DataFrame) -> pd.Series:
    """alpha_p = mean(xR_p) - Cov(-M, xR_p), Cov with divisor T (monthly decimals)."""
    assert m.index.equals(xr.index)
    neg_m = -m.to_numpy()
    x = xr.to_numpy()
    cov = ((neg_m - neg_m.mean())[:, None] * (x - x.mean(axis=0))).mean(axis=0)
    return pd.Series(x.mean(axis=0) - cov, index=xr.columns)


def portfolio_labels() -> list:
    return [f"BM {c}" for c in DECILES] + [f"MOM {c}" for c in MOM_DECILES]


def fmt(v: float) -> str:
    return f"{v + 0.0:.4f}" if abs(v) >= 5e-5 else "0.0000"


def main() -> None:
    xr_bm = load_excess_returns()
    xr_mom = load_excess_returns(MOM_CSV, MOM_DECILES)
    xr_all = pd.concat([xr_bm, xr_mom], axis=1, join="inner")
    assert len(xr_all) == len(xr_bm) == len(xr_mom)

    sdfs = {
        "M* from 2(a) (BM)": estimate_sdf(xr_bm)["m_star"],
        "M* from 2(b) (MOM)": estimate_sdf(xr_mom)["m_star"],
        "M* from 2(c) (BM + MOM)": estimate_sdf(xr_all)["m_star"],
    }
    alpha = pd.DataFrame({k: pricing_errors(m, xr_all) * PCT for k, m in sdfs.items()})
    alpha.index = portfolio_labels()
    alpha.index.name = "portfolio"
    alpha.to_csv(OUT_DIR / "q2d_pricing_errors.csv")

    cols = list(alpha.columns)
    rows = ["| Portfolio | " + " | ".join(f"$\\hat\\alpha_p$, {c.replace('M*', '$M^*$')}" for c in cols) + " |",
            "|---|" + "---:|" * len(cols)]
    rows += [f"| {p} | " + " | ".join(fmt(v) for v in r) + " |" for p, r in alpha.iterrows()]
    note = (f"\nPricing errors $\\hat\\alpha_p = \\hat E[xR_p] - \\widehat{{Cov}}[-M^*, xR_p]$ in percent "
            f"per month; monthly {xr_all.index[0].strftime('%Y:%m')}–{xr_all.index[-1].strftime('%Y:%m')} "
            f"(T = {len(xr_all)}); covariance with divisor T.\n")
    (OUT_DIR / "q2d_pricing_errors_table.md").write_text("\n".join(rows) + "\n" + note, encoding="utf-8")

    pd.set_option("display.width", 140)
    print(alpha.to_string(float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
