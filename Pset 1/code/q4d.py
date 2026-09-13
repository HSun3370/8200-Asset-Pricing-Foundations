"""
Pset 1, Question 4(d) -- Cochrane and Piazzesi (2005) factor: regression of the average
one-year excess log return across H = 2..5 on the five log forward rates, and a time-series
plot of the factor with NBER recession months shaded grey.

Student specification (as given; decisions recorded 2026-09-13):
  * Series from Question 4(a) (q4a.build_series): excess log returns xr^(H)_t = r^(H)_t - r^(1)_t,
    log forward rates f^(H)_t for H = 2..5, and f^(1)_t = y^(1)_t (the forward-rate formula at
    H = 1).
  * OLS  (1/4) sum_{H=2..5} xr^(H)_{t+1} = theta_0 + sum_{H=1..5} theta_H f^(H)_t + u_t,
    a regression on five forward rates plus an intercept, with t+1 the same month one year
    later (year-month pairing, as in Q4(a)). Every month t with all variables is used
    (June 1952 .. December 2023).
  * Plot the factor over time with NBER recession months shaded grey; recession months are
    those with USREC = 1 in USREC.csv (FRED series USREC), matched by year-month.
  * CP_SERIES (student's decision, see AI_INTERACTIONS.md):
        "cp_no_intercept" -- cp_t = sum_{H=1..5} theta_H f^(H)_t, as in problem set Eq. 4.3
        "fitted"          -- theta_0 + cp_t, the fitted expected average excess return
  * PLOT_RANGE (student's decision, see AI_INTERACTIONS.md):
        "estimation"   -- months t in the regression sample (June 1952 .. December 2023)
        "all_forwards" -- every month with forward rates (June 1952 .. December 2024), using
                          theta estimated on the regression sample

Both cp_t and the fitted value are saved for every month with forward rates, whatever the
plot shows.

Outputs (paths relative to "Pset 1"):
  output/q4d_cp_coefficients.csv, output/q4d_cp_series.csv, output/q4d_summary.csv,
  output/q4d_cp_nber.png
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from q4a import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, PSET_DIR, build_series, load_percent_yields

HORIZONS = [2, 3, 4, 5]
FORWARDS = ["f1", "f2", "f3", "f4", "f5"]
USREC_CSV = PSET_DIR / "USREC.csv"

CP_SERIES = "fitted"  # student decision, 2026-09-13 (AI_INTERACTIONS.md Entry 14)
PLOT_RANGE = "all_forwards"  # student decision, 2026-09-13 (AI_INTERACTIONS.md Entry 14)


def one_year_ahead(series: pd.Series) -> pd.Series:
    """Value of `series` in the same month one year later (NaN past the sample end)."""
    out = series.reindex(series.index + MONTHS_PER_YEAR)
    out.index = series.index
    return out


def load_usrec(path) -> pd.Series:
    u = pd.read_csv(path)
    assert list(u.columns) == ["observation_date", "USREC"], list(u.columns)
    u["month"] = pd.to_datetime(u["observation_date"]).dt.to_period("M")
    assert not u["month"].duplicated().any(), "duplicate months in USREC.csv"
    assert set(u["USREC"].unique()) <= {0, 1}, "USREC values other than 0/1"
    return u.set_index("month")["USREC"]


def recession_spans(flags: pd.Series) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Start/end timestamps of runs of consecutive USREC = 1 months (end = next month's start)."""
    spans, start = [], None
    for month, flag in flags.items():
        if flag == 1 and start is None:
            start = month
        elif flag != 1 and start is not None:
            spans.append((start.to_timestamp(), month.to_timestamp()))
            start = None
    if start is not None:
        spans.append((start.to_timestamp(), (flags.index[-1] + 1).to_timestamp()))
    return spans


def main() -> None:
    if CP_SERIES not in ("cp_no_intercept", "fitted"):
        raise ValueError(f"CP_SERIES must be 'cp_no_intercept' or 'fitted'; got {CP_SERIES!r}")
    if PLOT_RANGE not in ("estimation", "all_forwards"):
        raise ValueError(f"PLOT_RANGE must be 'estimation' or 'all_forwards'; got {PLOT_RANGE!r}")

    s = build_series(load_percent_yields(DATA_CSV))
    forwards = pd.concat(
        [s["y"][1].rename("f1")] + [s["f"][H].rename(f"f{H}") for H in HORIZONS], axis=1
    ).dropna()
    dep = sum(one_year_ahead(s["xr"][H]) for H in HORIZONS) / len(HORIZONS)

    d = pd.concat([dep.rename("avg_xr_next"), forwards], axis=1).dropna()
    fit = sm.OLS(d["avg_xr_next"], sm.add_constant(d[FORWARDS])).fit()
    theta = fit.params

    cp = forwards[FORWARDS] @ theta[FORWARDS]
    fitted = theta["const"] + cp
    months = d.index if PLOT_RANGE == "estimation" else forwards.index
    shown = (cp if CP_SERIES == "cp_no_intercept" else fitted).loc[months]

    usrec = load_usrec(USREC_CSV)
    flags = usrec.reindex(months)
    assert flags.notna().all(), "USREC missing for some plotted months"
    spans = recession_spans(flags.astype(int))

    coef = pd.DataFrame(
        {
            "parameter": ["theta0"] + [f"theta{H}" for H in range(1, 6)],
            "regressor": ["const"] + FORWARDS,
            "estimate": theta[["const"] + FORWARDS].to_numpy(),
        }
    )
    coef.to_csv(OUT_DIR / "q4d_cp_coefficients.csv", index=False)

    series = pd.DataFrame(
        {
            "cp_t": cp,
            "fitted": fitted,
            "avg_xr_next": d["avg_xr_next"].reindex(cp.index),
            "in_regression_sample": cp.index.isin(d.index),
            "usrec": usrec.reindex(cp.index).astype(int),
        }
    )
    series.index.name = "month"
    series.to_csv(OUT_DIR / "q4d_cp_series.csv")

    summary = pd.DataFrame(
        [
            ("cp_series", CP_SERIES),
            ("plot_range", PLOT_RANGE),
            ("n_regression", len(d)),
            ("regression_first", d.index[0]),
            ("regression_last", d.index[-1]),
            ("r_squared", fit.rsquared),
            ("n_plot", len(months)),
            ("plot_first", months[0]),
            ("plot_last", months[-1]),
            ("recession_months_plotted", int(flags.sum())),
            ("recession_spans_plotted", len(spans)),
            ("shown_mean", float(shown.mean())),
            ("shown_min", float(shown.min())),
            ("shown_max", float(shown.max())),
        ],
        columns=["parameter", "value"],
    )
    summary.to_csv(OUT_DIR / "q4d_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    for start, end in spans:
        ax.axvspan(start, end, color="0.85", lw=0, zorder=0)
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    if CP_SERIES == "cp_no_intercept":
        label = r"$cp_t = \sum_{H=1}^{5} \hat{\theta}_H f^{(H)}_t$"
    else:
        label = r"$\hat{\theta}_0 + cp_t$ (fitted value)"
    ax.plot(shown.index.to_timestamp(), 100 * shown, color="C0", lw=1.2, zorder=2)
    ax.set_xlabel("Month $t$")
    ax.set_ylabel(r"Percent ($\times 100$)")
    ax.set_title("Q4(d): Cochrane-Piazzesi factor with NBER recessions")
    ax.legend(
        handles=[Line2D([], [], color="C0", lw=1.2, label=label),
                 Patch(color="0.85", label="NBER recession (USREC = 1)")],
        loc="best",
    )
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "q4d_cp_nber.png", dpi=150)
    plt.close(fig)

    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"CP_SERIES = {CP_SERIES}, PLOT_RANGE = {PLOT_RANGE}")
    print(f"Regression: N = {len(d)} ({d.index[0]} .. {d.index[-1]}), R^2 = {fit.rsquared:.4f}")
    print(coef.to_string(index=False))
    print(f"Plot: {len(months)} months ({months[0]} .. {months[-1]}); {int(flags.sum())} recession "
          f"months in {len(spans)} spans; shown series mean {shown.mean():.4f}, "
          f"min {shown.min():.4f}, max {shown.max():.4f}")
    for name in ("q4d_cp_coefficients.csv", "q4d_cp_series.csv", "q4d_summary.csv", "q4d_cp_nber.png"):
        print(f"wrote {OUT_DIR / name}")


if __name__ == "__main__":
    main()
