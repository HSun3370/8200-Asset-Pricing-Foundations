"""
Pset 2, Question 4(e) -- Fama-MacBeth regressions for the linear beta pricing model implied
by M_t = a - b R_w,t: lambda and alpha_j with Newey-West standard errors.

Student specification: "do 4e" (2026-10-24), i.e. the problem-set text: estimate lambda and
alpha_j for each asset in Question 4(b) using Fama-MacBeth regressions; report lambda with
its standard error and each alpha_j with its t-stat; standard errors from time-series
regressions of lambda_t (alpha_j,t) on a constant with Newey-West (1987, 1994).

Decisions made by the student when AI flagged them (2026-10-24):
  * Factor R_w,t (gross market return) and the 21 test assets of 4(b), sample 1940:12 to
    2021:12 -- as in code/q4d.py.
  * First stage: full-sample time-series betas from Question 4(d) (constant over time).
  * Second stage: for each month t, a cross-sectional OLS regression with no intercept,
        xR_j,t = lambda_t beta_j + alpha_j,t,   j = 1..21,
    so alpha_j,t are the cross-sectional residuals.
  * lambda = mean of lambda_t, alpha_j = mean of alpha_j,t; standard errors from a
    regression of each series on a constant with Newey-West S (automatic Newey-West (1994)
    lag per series; same S as code/q4d.py's nw_mean).

Outputs (paths relative to "Pset 2"): output/q4e_fm.csv, output/q4e_fm_table.md,
output/q4e_lambda_series.csv
"""

import numpy as np
import pandas as pd

from q2a import OUT_DIR
from q4b import SAMPLE, load_inputs
from q4d import asset_label, nw_mean, ts_results


def main() -> None:
    rw, Xdf = load_inputs()
    T = len(rw)
    ts, _ = ts_results(rw, Xdf)
    beta = ts["beta"].to_numpy()
    Y = Xdf.to_numpy()                                         # T x J

    lam_t = Y @ beta / (beta @ beta)                           # no-intercept CS OLS each month
    alpha_t = Y - np.outer(lam_t, beta)                        # T x J residuals

    lam, se_lam, L_lam = nw_mean(lam_t)
    rows = []
    for j, c in enumerate(Xdf.columns):
        a, se, L = nw_mean(alpha_t[:, j])
        rows.append({"asset": c, "beta": beta[j], "alpha": a, "se_alpha": se,
                     "t_alpha": a / se, "L": L})
    out = pd.DataFrame(rows).set_index("asset")
    out.to_csv(OUT_DIR / "q4e_fm.csv")
    pd.DataFrame({"lambda_t": lam_t}, index=SAMPLE.astype(str)).rename_axis("month").to_csv(
        OUT_DIR / "q4e_lambda_series.csv")

    md = ["| | Estimate | Std. error | t-stat |", "|---|---:|---:|---:|",
          f"| $\\lambda$ | {lam:.5f} | {se_lam:.5f} | {lam / se_lam:.2f} |"]
    md += [f"| $\\alpha_j$: {asset_label(c)} | {r.alpha:.5f} | {r.se_alpha:.5f} | {r.t_alpha:.2f} |"
           for c, r in out.iterrows()]
    md += ["", f"Fama-MacBeth: $\\hat\\beta_j$ from the full-sample time-series regressions of 4(d) "
               f"(factor $R_{{w,t}} = e^{{r_{{e,t}}}}$); each month a no-intercept cross-sectional regression "
               f"$xR_{{j,t}} = \\lambda_t \\hat\\beta_j + \\alpha_{{j,t}}$ over the 21 assets. $\\hat\\lambda$ and "
               f"$\\hat\\alpha_j$ are time-series means; standard errors from regressions on a constant with "
               f"Newey-West (1987, 1994) S and the automatic lag (L = {L_lam} for $\\lambda_t$). Monthly "
               f"observations of annual returns, {SAMPLE[0].strftime('%Y:%m')}–{SAMPLE[-1].strftime('%Y:%m')} (T = {T})."]
    (OUT_DIR / "q4e_fm_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    pd.set_option("display.width", 140)
    print(f"lambda = {lam:.6f} (s.e. {se_lam:.6f}, L = {L_lam})")
    print(out.to_string(float_format=lambda v: f"{v:.5f}"))
    # identity check: mean residuals are orthogonal to beta (no-intercept OLS)
    print(f"beta' alpha_bar = {beta @ out['alpha'].to_numpy():.2e}")


if __name__ == "__main__":
    main()
