"""
Pset 1, Question 4(e) -- regressions of the one-year excess log return on the
Cochrane-Piazzesi factor, H = 2..5, with Newey-West (1987, 1994) t-statistics.

Student specification (as given; decisions recorded 2026-09-13):
  * OLS  xr^(H)_{t+1} = a^(H) + b^(H) cp_t + e^(H),  H = 2..5, with xr from Question 4(a)
    (q4a.build_series) and t+1 the same month one year later (year-month pairing).
  * cp_t is the factor from Question 4(d), read from output/q4d_cp_series.csv (run q4d.py
    first). The script checks that the saved series equals the saved Q4(d) coefficients
    applied to the forward rates.
  * Every month t with both variables is used (June 1952 .. December 2023 for every H).
  * Newey-West (1987, 1994) t-statistics exactly as in Q2(b) method (v) and Q4(c): Bartlett
    weights, lag from linearmodels.kernel_optimal_bandwidth on the slope's score, variance
    from q2b.s_hac and q2b.sandwich.
  * CP_REGRESSOR (student's decision, see AI_INTERACTIONS.md):
        "cp_t"   -- cp_t = sum_{H=1..5} theta_H f^(H)_t (problem set Eq. 4.3, no intercept)
        "fitted" -- theta_0 + cp_t, the series plotted in Question 4(d)
    The two series differ by the constant theta_0.

Output (path relative to "Pset 1"): output/q4e_regressions.csv
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv.covariance import kernel_optimal_bandwidth
from statsmodels.stats.sandwich_covariance import weights_bartlett

from q2b import s_hac, sandwich
from q4a import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, build_series, load_percent_yields

HORIZONS = [2, 3, 4, 5]
FORWARDS = ["f1", "f2", "f3", "f4", "f5"]
CP_REGRESSOR = "fitted"  # student decision, 2026-09-13 (AI_INTERACTIONS.md Entry 15)


def one_year_ahead(series: pd.Series) -> pd.Series:
    """Value of `series` in the same month one year later (NaN past the sample end)."""
    out = series.reindex(series.index + MONTHS_PER_YEAR)
    out.index = series.index
    return out


def load_q4d_factor(s: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Q4(d) factor series, checked against the saved Q4(d) coefficients."""
    series = pd.read_csv(OUT_DIR / "q4d_cp_series.csv")
    series["month"] = pd.PeriodIndex(series["month"], freq="M")
    series = series.set_index("month")

    coef = pd.read_csv(OUT_DIR / "q4d_cp_coefficients.csv").set_index("regressor")["estimate"]
    forwards = pd.concat(
        [s["y"][1].rename("f1")] + [s["f"][H].rename(f"f{H}") for H in HORIZONS], axis=1
    ).dropna()
    cp = forwards[FORWARDS] @ coef[FORWARDS]

    gap = float((cp - series["cp_t"].reindex(cp.index)).abs().max())
    assert gap < 1e-12, f"q4d_cp_series.csv does not match the Q4(d) coefficients (gap {gap}); re-run q4d.py"
    gap_fitted = float((series["fitted"] - series["cp_t"] - coef["const"]).abs().max())
    assert gap_fitted < 1e-12, f"fitted column is not theta_0 + cp_t (gap {gap_fitted})"
    return series


def main() -> None:
    if CP_REGRESSOR not in ("cp_t", "fitted"):
        raise ValueError(f"CP_REGRESSOR must be 'cp_t' or 'fitted'; got {CP_REGRESSOR!r}")

    s = build_series(load_percent_yields(DATA_CSV))
    factor = load_q4d_factor(s)[CP_REGRESSOR]

    rows = []
    for H in HORIZONS:
        d = pd.DataFrame(
            {"dep": one_year_ahead(s["xr"][H]), "cp": factor.reindex(s["xr"].index)}
        ).dropna()
        X = sm.add_constant(d["cp"].to_numpy())
        fit = sm.OLS(d["dep"].to_numpy(), X).fit()
        T = len(d)
        h = X * fit.resid[:, None]
        L = int(kernel_optimal_bandwidth(h[:, 1:], kernel="bartlett"))
        V = sandwich(X.T @ X / T, s_hac(h, L, weights_bartlett(L)), T)
        var_b = V[1, 1]
        se_b = float(np.sqrt(var_b)) if var_b > 0 else np.nan
        a, b = fit.params
        rows.append(
            {
                "H": H,
                "n_months": T,
                "first_month": d.index[0],
                "last_month": d.index[-1],
                "nw_lags": L,
                "a": a,
                "b": b,
                "se_b_nw": se_b,
                "t_b_nw": b / se_b if var_b > 0 else np.nan,
                "var_b_positive": bool(var_b > 0),
                "V_positive_definite": bool(np.all(np.linalg.eigvalsh(V) > 0)),
                "cp_regressor": CP_REGRESSOR,
            }
        )
    res = pd.DataFrame(rows)
    res.to_csv(OUT_DIR / "q4e_regressions.csv", index=False)

    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"CP_REGRESSOR = {CP_REGRESSOR}; Newey-West (1987, 1994); xr benchmark from q4a: r1_t")
    print(res.drop(columns=["cp_regressor"]).to_string(index=False))
    print(f"wrote {OUT_DIR / 'q4e_regressions.csv'}")


if __name__ == "__main__":
    main()
