"""
Pset 1, Question 4(c) -- regressions of the one-year excess log return on the excess log
forward rate, H = 2..5, with Newey-West t-statistics.

Student specification (as given; decisions recorded 2026-09-12):
  * Series from Question 4(a) (q4a.build_series): xr^(H)_t = r^(H)_t - r^(1)_t and
    xf^(H)_t = f^(H)_t - y^(1)_t.
  * OLS   xr^(H)_{t+1} = a^(H) + b^(H) xf^(H)_t + e^(H),  H = 2..5, where t+1 is the same
    month one year later (year-month pairing, as in Q4(a)). Every month t with both
    variables is used (June 1952 .. December 2023 for every H).
  * Report b^(H) with Newey-West t-statistics, using the Q2(b) formulas (q2b.s_hac and
    q2b.sandwich with Bartlett weights w_l = 1 - l/(L+1)).
  * NW_METHOD (student's decision, see AI_INTERACTIONS.md):
        "nw1987_1994" -- L chosen by the Newey-West (1994) rule exactly as in Q2(b) method (v):
                         linearmodels.kernel_optimal_bandwidth on the slope's score e_t * xf_t
        "nw1987_11"   -- L = 11, as in Q2(b) method (iii)

Check (problem set footnote 13): b^(2) here must equal b^(2) from Q4(b); if
output/q4b_regressions.csv exists, the script stops when the two differ by more than 1e-10.

Output (path relative to "Pset 1"): output/q4c_regressions.csv
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv.covariance import kernel_optimal_bandwidth
from statsmodels.stats.sandwich_covariance import weights_bartlett

from q2b import s_hac, sandwich
from q4a import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, build_series, load_percent_yields

HORIZONS = [2, 3, 4, 5]
NW_METHOD = "nw1987_1994"  # student decision, 2026-09-13 (AI_INTERACTIONS.md Entry 13)


def one_year_ahead(series: pd.Series) -> pd.Series:
    """Value of `series` in the same month one year later (NaN past the sample end)."""
    out = series.reindex(series.index + MONTHS_PER_YEAR)
    out.index = series.index
    return out


def main() -> None:
    if NW_METHOD not in ("nw1987_1994", "nw1987_11"):
        raise ValueError(f"NW_METHOD must be 'nw1987_1994' or 'nw1987_11'; got {NW_METHOD!r}")

    s = build_series(load_percent_yields(DATA_CSV))

    rows = []
    for H in HORIZONS:
        d = pd.DataFrame({"dep": one_year_ahead(s["xr"][H]), "xf": s["xf"][H]}).dropna()
        X = sm.add_constant(d["xf"].to_numpy())
        fit = sm.OLS(d["dep"].to_numpy(), X).fit()
        T = len(d)
        h = X * fit.resid[:, None]
        if NW_METHOD == "nw1987_1994":
            L = int(kernel_optimal_bandwidth(h[:, 1:], kernel="bartlett"))
        else:
            L = 11
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
                "nw_rule": NW_METHOD,
            }
        )
    res = pd.DataFrame(rows)

    q4b_csv = OUT_DIR / "q4b_regressions.csv"
    if q4b_csv.exists():
        b2_q4b = float(pd.read_csv(q4b_csv).set_index("H").loc[2, "b"])
        b2_here = float(res.set_index("H").loc[2, "b"])
        assert abs(b2_q4b - b2_here) < 1e-10, (
            f"footnote 13 check failed: b^(2) = {b2_here} here vs {b2_q4b} in Q4(b)"
        )
        print(f"footnote 13 check: b^(2) = {b2_here:.6f} here and {b2_q4b:.6f} in Q4(b)")

    res.to_csv(OUT_DIR / "q4c_regressions.csv", index=False)

    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"NW_METHOD = {NW_METHOD}; xr benchmark from q4a: r1_t")
    print(res.drop(columns=["nw_rule"]).to_string(index=False))
    print(f"wrote {OUT_DIR / 'q4c_regressions.csv'}")


if __name__ == "__main__":
    main()
