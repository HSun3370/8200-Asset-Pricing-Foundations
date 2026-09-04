"""
Pset 1, Question 2(a) -- long-horizon predictive regressions of excess equity
returns on the dividend-price ratio.

Student specification (as given):
  xR_t   = exp(re_t) - exp(rf_t)          (simple excess return)
  D/P_t  = exp(dp_t)                      (level dividend-price ratio)
  For H = 1, 2, ..., 15 (years), form the average future excess return
      y_t^{(H)} = (1/H) * sum_{h=1}^{H} xR_{t+h}
  and estimate by OLS (with intercept)
      y_t^{(H)} = a^{(H)} + b^{(H)} * (D/P)_t + e_t^{(H)}.
  Collect the sample-size-adjusted R^2 of each regression and plot R^2_adj
  (y-axis) against H (x-axis).

Timing (student decision, recorded 2026-09-04): the dataset holds monthly
observations of ANNUAL variables, so "h years ahead" is the row observed
12*h months after t -- the same convention the student specified for Q1(b) in
code/q1b.py. An observation is kept only if every required future row exists,
so horizon H uses N - 12*H observations.

Adjusted R^2 uses the usual degrees-of-freedom correction with k = 1 regressor:
      R^2_adj = 1 - (1 - R^2) * (n - 1) / (n - 2).

Outputs: output/q2a_r2adj.csv and output/q2a_r2adj.png (paths relative to "Pset 1").
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 1
DATA_CSV = PSET_DIR / "EQ Dataset.csv"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

H_MAX = 15
MONTHS_PER_YEAR = 12


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(
        dict(year=df["YEAR"], month=df["MONTH"], day=1)
    ).dt.to_period("M")
    df = df.sort_values("date").set_index("date")
    # Overlapping monthly timing shifts by rows; require a gap-free monthly index.
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly date index has gaps; row-shift timing invalid"
    return df


def ols_fit(x: np.ndarray, y: np.ndarray) -> dict:
    """OLS of y on [1, x]; returns slope, intercept, R^2 and adjusted R^2."""
    n = len(y)
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (intercept + slope * x)
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    r2_adj = 1.0 - (1.0 - r2) * (n - 1) / (n - 2)      # k = 1 regressor
    return {
        "n_obs": n,
        "a": float(intercept),
        "b": float(slope),
        "r2": r2,
        "r2_adj": r2_adj,
    }


def horizon_regressions(df: pd.DataFrame) -> pd.DataFrame:
    xr = np.exp(df["re"]) - np.exp(df["rf"])          # xR_t = e^{re} - e^{rf}
    dp_level = np.exp(df["dp"])                        # D/P_t = e^{dp}

    rows = []
    for h in range(1, H_MAX + 1):
        # (1/H) * sum_{j=1}^{H} xR_{t+j years}, with "j years" = 12*j months of rows
        y = sum(xr.shift(-MONTHS_PER_YEAR * j) for j in range(1, h + 1)) / h

        reg = pd.DataFrame({"dp_level": dp_level, "y": y}).dropna()
        fit = ols_fit(reg["dp_level"].to_numpy(), reg["y"].to_numpy())
        rows.append({"H": h, **fit})
    return pd.DataFrame(rows)


def make_figure(res: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(res["H"], res["r2_adj"], "o-", color="C0", zorder=2)
    ax.set_xlabel("Horizon $H$ (years)")
    ax.set_ylabel("$R^2_{adj}$")
    ax.set_title(
        "Q2(a): long-horizon regressions of average excess returns on $D_t/P_t$"
    )
    ax.set_xticks(range(1, H_MAX + 1))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_CSV)
    res = horizon_regressions(df)

    csv_path = OUT_DIR / "q2a_r2adj.csv"
    png_path = OUT_DIR / "q2a_r2adj.png"
    res.to_csv(csv_path, index=False)
    make_figure(res, png_path)

    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"N monthly obs : {len(df)}  ({df.index[0]} .. {df.index[-1]})")
    print()
    print(res.to_string(index=False))
    print()
    print(f"wrote {csv_path}")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
