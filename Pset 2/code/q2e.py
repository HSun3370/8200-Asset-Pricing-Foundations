"""
Pset 2, Question 2(e) -- out-of-sample pricing errors of the 20 BM + MOM decile
portfolios under the SDF estimated with data until December 1989.

Student specification (as given, 2026-10-03):
  "Repeat the M* construction in Question (2c), but using data until December 1989.
   Then, apply the a_hat and b_hat obtained from this exercise to construct the
   out-of-sample SDF M*_OS,t = a_hat - b_hat' xR_t from January 1990 to the end of the
   sample. For each portfolio p (covering the 20 portfolios from Question (2c)),
   calculate (and report in a table) the pricing error
   alpha_OS,p = E[xR_p] - Cov[-M*_OS, xR_p] using data from January 1990 to the end of
   the sample to estimate alpha_OS,p. report results."

Carried over from Question 2(c) (see code/q2c.py): the 20 portfolios (10 BM deciles then
10 MOM deciles), value-weighted monthly returns, xR_t = (R_t - RF_t) / 100, E[M* xR] = 0
and E[M*] = 1, two-step GMM, Newey-West S with the automatic Newey-West (1994) lag.
  * Estimation sample: 1927:07 (the start used in 2(a)-2(c)) to 1989:12.
  * Out-of-sample period: 1990:01 to 2026:08. E[xR_p] and Cov are both computed over
    this period only.

Decisions made by the student when AI flagged them (2026-10-03):
  * Cov divisor: T (here the number of out-of-sample months).
  * Units of the reported alpha: percent per month.
  * Report the 1927:07-1989:12 estimates (a_hat, b_hat with s.e.) as well.

Outputs (paths relative to "Pset 2"):
  output/q2e_gmm.csv, output/q2e_gmm_table.md (1927:07-1989:12 estimates),
  output/q2e_pricing_errors.csv, output/q2e_pricing_errors_table.md
"""

import pandas as pd

from q2a import DECILES, OUT_DIR, estimate_sdf, load_excess_returns, print_summary, save_results
from q2b import MOM_CSV, MOM_DECILES
from q2d import PCT, fmt, portfolio_labels, pricing_errors

IS_END = pd.Period("1989-12", freq="M")
OS_START = pd.Period("1990-01", freq="M")


def main() -> None:
    xr_all = pd.concat(
        [load_excess_returns(), load_excess_returns(MOM_CSV, MOM_DECILES)],
        axis=1, join="inner",
    )
    columns = DECILES + MOM_DECILES
    xr_is = xr_all.loc[:IS_END]
    xr_os = xr_all.loc[OS_START:]
    assert len(xr_is) + len(xr_os) == len(xr_all)

    fit = estimate_sdf(xr_is)
    res = save_results(fit, xr_is, columns, "q2e", plot=False)
    print_summary(fit, xr_is, res)

    a_hat, b_hat = fit["theta"][0], fit["theta"][1:]
    m_os = pd.Series(a_hat - xr_os.to_numpy() @ b_hat, index=xr_os.index, name="M_star_OS")
    alpha = (pricing_errors(m_os, xr_os) * PCT).to_frame("alpha_OS_pct_per_month")
    alpha.index = portfolio_labels()
    alpha.index.name = "portfolio"
    alpha.to_csv(OUT_DIR / "q2e_pricing_errors.csv")

    rows = ["| Portfolio | $\\hat\\alpha_{OS,p}$ |", "|---|---:|"]
    rows += [f"| {p} | {fmt(v)} |" for p, v in alpha.iloc[:, 0].items()]
    note = (f"\nOut-of-sample pricing errors $\\hat\\alpha_{{OS,p}} = \\hat E[xR_p] - "
            f"\\widehat{{Cov}}[-M^*_{{OS}}, xR_p]$ in percent per month, computed over "
            f"{xr_os.index[0].strftime('%Y:%m')}–{xr_os.index[-1].strftime('%Y:%m')} (T = {len(xr_os)}), "
            f"covariance with divisor T. $M^*_{{OS,t}} = \\hat a - \\hat b'xR_t$ with $\\hat a, \\hat b$ "
            f"estimated over {xr_is.index[0].strftime('%Y:%m')}–{xr_is.index[-1].strftime('%Y:%m')}.\n")
    (OUT_DIR / "q2e_pricing_errors_table.md").write_text("\n".join(rows) + "\n" + note, encoding="utf-8")

    print()
    print(f"Estimation sample {xr_is.index[0]} to {xr_is.index[-1]} (T = {len(xr_is)}); "
          f"out-of-sample {xr_os.index[0]} to {xr_os.index[-1]} (T = {len(xr_os)})")
    print(alpha.to_string(float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
