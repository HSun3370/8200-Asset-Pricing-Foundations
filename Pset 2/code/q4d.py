"""
Pset 2, Question 4(d) -- time-series regressions for the linear beta pricing model implied
by M_t = a - b R_w,t: lambda, alpha_j (Newey-West) and the GRS test.

Student specification: "do 4d" (2026-10-24), i.e. the problem-set text: estimate lambda and
alpha_j for each asset in Question 4(b) using time-series regressions; lambda and its
standard error from a time-series regression of R_w,t on a constant (Newey-West 1987, 1994);
alpha_j and its t-stat from the respective time-series factor regression (Newey-West 1987,
1994); p-value of the GRS test that the pricing errors are jointly zero.

Decisions made by the student when AI flagged them (2026-10-24):
  * Factor f_t = R_w,t = exp(re_t) (gross market return, as written in the problem), so
    lambda_hat = sample mean of R_w. (AI noted that alpha_j are pricing errors and
    lambda = E[f] when the factor is an excess return; the student chose R_w.)
  * Test assets: the 21 assets of 4(b): xR_w and the 20 BM/MOM 12-month compounded excess
    returns.
  * Sample 1940:12 to 2021:12 (T = 973).
Implementation (carried over / course formulas):
  * Time-series regression per asset: xR_j,t = alpha_j + beta_j f_t + e_j,t (OLS).
    aVar[(alpha, beta)] = (1/T) Q^-1 S Q^-1 with Q = (1/T) sum x_t x_t', and S the Newey-West
    S of h_t = x_t e_t (Bartlett weights 1 - l/(L+1), Om_l = 1/(T-l) sum, as in Q2-Q4).
    Lag L: Newey-West (1994) rule (linearmodels.kernel_optimal_bandwidth) applied to the
    slope regressor's score e_t f_t, the convention used in Pset 1/code/q2b.py.
  * lambda: the same with x_t = 1 (S of R_w,t - Rbar_w; lag from the NW(1994) rule on
    that series).
  * GRS (course slides, Module 2 p. 43; Cochrane 2005 eq. 12.5):
        GRS = (T - J - K)/J * (1 + E_T[f]' Sigma_f^-1 E_T[f])^-1 * alpha' Sigma_e^-1 alpha
              ~ F(J, T - J - K),
    J = 21 assets, K = 1 factor, Sigma_e = (1/T) sum e_t e_t', Sigma_f = (1/T) sum (f_t - fbar)^2.

Outputs (paths relative to "Pset 2"): output/q4d_ts.csv, output/q4d_ts_table.md
"""

import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth
from scipy.stats import f as f_dist

from q2a import OUT_DIR, newey_west_s
from q4b import SAMPLE, load_inputs


def nw_lag(series: np.ndarray) -> int:
    return int(kernel_optimal_bandwidth(series - series.mean(), kernel="bartlett"))


def nw_mean(series: np.ndarray) -> tuple[float, float, int]:
    """Mean of a series and its Newey-West standard error (regression on a constant)."""
    T = len(series)
    u = series - series.mean()
    L = nw_lag(series)
    S = newey_west_s(u[:, None], L)[0, 0]
    return float(series.mean()), float(np.sqrt(S / T)), L


def ts_regression(y: np.ndarray, f: np.ndarray) -> dict:
    T = len(y)
    x = np.column_stack([np.ones(T), f])
    coef, *_ = np.linalg.lstsq(x, y, rcond=None)
    e = y - x @ coef
    h = x * e[:, None]
    L = nw_lag(h[:, 1])
    Qinv = np.linalg.inv(x.T @ x / T)
    V = Qinv @ newey_west_s(h, L) @ Qinv / T
    se = np.sqrt(np.diag(V))
    return dict(alpha=coef[0], beta=coef[1], se_alpha=se[0], se_beta=se[1], resid=e, L=L)


def ts_results(rw: np.ndarray, Xdf: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    rows, resid = [], []
    for c in Xdf.columns:
        r = ts_regression(Xdf[c].to_numpy(), rw)
        resid.append(r.pop("resid"))
        rows.append({"asset": c, **r})
    return pd.DataFrame(rows).set_index("asset"), np.column_stack(resid)


def asset_label(c: str) -> str:
    return "$xR_{w}$ (market)" if c == "xR_w" else c


def main() -> None:
    rw, Xdf = load_inputs()
    T, J, K = len(rw), Xdf.shape[1], 1
    lam, se_lam, L_lam = nw_mean(rw)
    ts, E = ts_results(rw, Xdf)

    alpha = ts["alpha"].to_numpy()
    sigma_e = E.T @ E / T
    sigma_f = rw.var(ddof=0)
    grs = (T - J - K) / J * (alpha @ np.linalg.solve(sigma_e, alpha)) / (1 + rw.mean() ** 2 / sigma_f)
    p_grs = float(f_dist.sf(grs, J, T - J - K))

    out = ts.assign(t_alpha=ts["alpha"] / ts["se_alpha"])
    out.to_csv(OUT_DIR / "q4d_ts.csv")
    pd.DataFrame([{"lambda": lam, "se_lambda": se_lam, "L_lambda": L_lam,
                   "GRS": grs, "df1": J, "df2": T - J - K, "p_GRS": p_grs}]).to_csv(
        OUT_DIR / "q4d_summary.csv", index=False)

    md = ["| | Estimate | Std. error | t-stat |", "|---|---:|---:|---:|",
          f"| $\\lambda$ | {lam:.4f} | {se_lam:.4f} | {lam / se_lam:.2f} |"]
    md += [f"| $\\alpha_j$: {asset_label(c)} | {r.alpha:.5f} | {r.se_alpha:.5f} | {r.alpha / r.se_alpha:.2f} |"
           for c, r in ts.iterrows()]
    p_txt = f"= {p_grs:.4f}" if p_grs >= 1e-4 else "< 0.0001"
    md += ["", f"GRS test that the $\\alpha_j$ are jointly zero: GRS = {grs:.3f} "
               f"$\\sim F({J}, {T - J - K})$, p-value {p_txt}.", "",
           f"Time-series regressions $xR_{{j,t}} = \\alpha_j + \\beta_j R_{{w,t}} + \\varepsilon_{{j,t}}$ "
           f"with factor $R_{{w,t}} = e^{{r_{{e,t}}}}$; $\\hat\\lambda$ from a regression of $R_{{w,t}}$ on a "
           f"constant (NW lag {L_lam}). Newey-West (1987, 1994) standard errors with the automatic lag "
           f"chosen per regression. Monthly observations of annual returns, "
           f"{SAMPLE[0].strftime('%Y:%m')}–{SAMPLE[-1].strftime('%Y:%m')} (T = {T})."]
    (OUT_DIR / "q4d_ts_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    pd.set_option("display.width", 140)
    print(f"lambda = {lam:.6f} (s.e. {se_lam:.6f}, L = {L_lam}); GRS = {grs:.4f} ~ F({J},{T - J - K}), p = {p_grs:.3e}")
    print(out.to_string(float_format=lambda v: f"{v:.5f}"))


if __name__ == "__main__":
    main()
