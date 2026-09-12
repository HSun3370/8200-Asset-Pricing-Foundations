"""
Pset 1, Question 4(b) -- regressions of the average annual hold-to-maturity excess return
on the excess log yield, H = 2..5, with Hansen-Hodrick (1980) t-statistics.

Student specification (as given; decisions recorded 2026-09-12):
  * Series from Question 4(a) (q4a.build_series): log yields y^(H)_t, excess log yields
    xy^(H)_t = y^(H)_t - y^(1)_t and excess log returns xr^(H)_t = r^(H)_t - r^(1)_t.
    The one-year bond's excess return is zero: xr^(1)_t = 0.
  * Hold-to-maturity excess return, for each month t and H = 2..5:
        xr^(H)_{t:t+H} = sum_{h=1..H} xr^(H-h+1)_{t+h}
    where t+h is the same month h years later (year-month pairing, as in Q4(a)).
  * OLS   (1/H) xr^(H)_{t:t+H} = a^(H) + b^(H) xy^(H)_t + e^(H)_t
  * Report b^(H) and its t-statistic with Hansen-Hodrick (1980) standard errors as in
    Q2(b): Var = (1/T) Q^{-1} S Q^{-1}, S = Om_0 + sum_{l=1..L} (Om_l + Om_l'),
    Om_l = 1/(T-l) sum_t e_t x_t x_{t-l}' e_{t-l} (q2b.s_hac and q2b.sandwich with
    uniform weights).
  * HH_LAGS (student's decision, see AI_INTERACTIONS.md):
        "overlap_months" -- L = 12H - 1, the months of overlap of the H-year dependent variable
        "q2b_11"         -- L = 11 for every H, as in Q2(b)
  * SAMPLE (student's decision, see AI_INTERACTIONS.md):
        "own"    -- each H uses every month t with both variables available
        "common" -- every H uses the months available for all H

Check: the summed excess returns are compared with the same quantity computed directly
from log yields; the script stops if they differ by more than 1e-12.

Outputs (paths relative to "Pset 1"):
  output/q4b_hold_to_maturity.csv, output/q4b_regressions.csv
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import weights_uniform

from q2b import s_hac, sandwich
from q4a import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, build_series, load_percent_yields

HORIZONS = [2, 3, 4, 5]
HH_LAGS = "overlap_months"  # student decision, 2026-09-12 (AI_INTERACTIONS.md Entry 12)
SAMPLE = "own"  # student decision, 2026-09-12 (AI_INTERACTIONS.md Entry 12)


def years_ahead(series: pd.Series, years: int) -> pd.Series:
    """Value of `series` in the same month `years` years later (NaN past the sample end)."""
    out = series.reindex(series.index + MONTHS_PER_YEAR * years)
    out.index = series.index
    return out


def hold_to_maturity(s: dict[str, pd.DataFrame]) -> pd.DataFrame:
    xr = s["xr"]
    y = s["y"]

    out = {}
    for H in HORIZONS:
        # The h = H term is xr^(1)_{t+H} = r^(1)_{t+H} - r^(1)_{t+H} = 0 by definition and needs
        # no data. It is left out of the sum rather than filled with 0 on the data's own months,
        # which would wrongly drop every t whose month t+H lies past the end of the sample.
        total = sum(years_ahead(xr[H - h + 1], h) for h in range(1, H))

        # the same quantity built directly from log yields, as an implementation check
        from_yields = H * y[H] - sum(years_ahead(y[1], h - 1) for h in range(1, H + 1))
        ok = total.notna()
        gap = float((total[ok] - from_yields[ok]).abs().max())
        assert gap < 1e-12, f"H={H}: summed excess returns differ from yield-based value by {gap}"

        out[H] = total
    return pd.DataFrame(out)


def hh_lags(H: int) -> int:
    return {"overlap_months": MONTHS_PER_YEAR * H - 1, "q2b_11": 11}[HH_LAGS]


def main() -> None:
    if HH_LAGS not in ("overlap_months", "q2b_11"):
        raise ValueError(f"HH_LAGS must be 'overlap_months' or 'q2b_11'; got {HH_LAGS!r}")
    if SAMPLE not in ("own", "common"):
        raise ValueError(f"SAMPLE must be 'own' or 'common'; got {SAMPLE!r}")

    s = build_series(load_percent_yields(DATA_CSV))
    htm = hold_to_maturity(s)

    frames = {
        H: pd.DataFrame({"dep": htm[H] / H, "xy": s["xy"][H]}).dropna() for H in HORIZONS
    }
    if SAMPLE == "common":
        common = frames[HORIZONS[0]].index
        for H in HORIZONS[1:]:
            common = common.intersection(frames[H].index)
        frames = {H: f.loc[common] for H, f in frames.items()}

    rows = []
    for H in HORIZONS:
        f = frames[H]
        L = hh_lags(H)
        X = sm.add_constant(f["xy"].to_numpy())
        fit = sm.OLS(f["dep"].to_numpy(), X).fit()
        a, b = fit.params
        T = len(f)
        V = sandwich(X.T @ X / T, s_hac(X * fit.resid[:, None], L, weights_uniform(L)), T)
        var_b = V[1, 1]
        se_b = float(np.sqrt(var_b)) if var_b > 0 else np.nan
        rows.append(
            {
                "H": H,
                "n_months": T,
                "first_month": f.index[0],
                "last_month": f.index[-1],
                "hh_lags": L,
                "a": a,
                "b": b,
                "se_b_hh": se_b,
                "t_b_hh": b / se_b if var_b > 0 else np.nan,
                "var_b_positive": bool(var_b > 0),
                "V_positive_definite": bool(np.all(np.linalg.eigvalsh(V) > 0)),
                "hh_lags_rule": HH_LAGS,
                "sample_rule": SAMPLE,
            }
        )
    res = pd.DataFrame(rows)

    htm_out = htm.rename(columns=lambda H: f"xr_htm{H}")
    htm_out.index.name = "month"
    htm_out.to_csv(OUT_DIR / "q4b_hold_to_maturity.csv")
    res.to_csv(OUT_DIR / "q4b_regressions.csv", index=False)

    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"HH_LAGS = {HH_LAGS}, SAMPLE = {SAMPLE}; xr benchmark from q4a: r1_t")
    print(res.drop(columns=["hh_lags_rule", "sample_rule"]).to_string(index=False))
    print(f"wrote {OUT_DIR / 'q4b_hold_to_maturity.csv'}")
    print(f"wrote {OUT_DIR / 'q4b_regressions.csv'}")


if __name__ == "__main__":
    main()
