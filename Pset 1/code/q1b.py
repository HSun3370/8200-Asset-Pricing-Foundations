"""
Pset 1, Question 1(b) -- variance-decomposition slopes from Equation 1.4.

Student construction (as specified):
  kappa   = 1 / (1 + exp(dp_bar)),  dp_bar = full-sample mean of the monthly `dp` column.
  For each horizon h = 1..20 (years), regress (with intercept) each of the three
  variables below on dp_t, and keep the slope:
    1.  sum_{j=1}^{h} kappa^{j-1} * re_{t+j}
    2. -sum_{j=1}^{h} kappa^{j-1} * dg_{t+j}
    3.  kappa^h * dp_{t+h}
  Timing: overlapping monthly. Every month tau is a start point; a "year-j" value is
  the annual variable observed 12*j months after tau (dataset is monthly observations
  of annual variables). Observation kept only if every required future row exists, so
  horizon h uses about N - 12h observations.

Univariate OLS slope with intercept = Cov(x, y) / Var(x); computed here via np.polyfit.
Outputs: output/q1b_slopes.csv and output/q1b_slopes.png (paths relative to "Pset 1").
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

H_MAX = 20
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


def ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    """Slope of y = a + b*x + e (intercept included)."""
    slope, _intercept = np.polyfit(x, y, 1)
    return float(slope)


def horizon_slopes(df: pd.DataFrame, kappa: float) -> pd.DataFrame:
    re = df["re"]
    dg = df["dg"]
    dp = df["dp"]

    rows = []
    for h in range(1, H_MAX + 1):
        # future annual variables observed 12*j months ahead of each start month
        re_sum = sum(
            kappa ** (j - 1) * re.shift(-MONTHS_PER_YEAR * j) for j in range(1, h + 1)
        )
        dg_sum = sum(
            kappa ** (j - 1) * dg.shift(-MONTHS_PER_YEAR * j) for j in range(1, h + 1)
        )
        y_re = re_sum
        y_dg = -dg_sum
        y_dp = kappa ** h * dp.shift(-MONTHS_PER_YEAR * h)

        reg = pd.DataFrame({"dp_t": dp, "y_re": y_re, "y_dg": y_dg, "y_dp": y_dp}).dropna()
        x = reg["dp_t"].to_numpy()

        b_re = ols_slope(x, reg["y_re"].to_numpy())
        b_dg = ols_slope(x, reg["y_dg"].to_numpy())
        b_dp = ols_slope(x, reg["y_dp"].to_numpy())

        rows.append(
            {
                "h": h,
                "n_obs": len(reg),
                "b_re": b_re,
                "b_dg": b_dg,
                "b_dp": b_dp,
                "sum": b_re + b_dg + b_dp,
            }
        )
    return pd.DataFrame(rows)


def make_figure(res: pd.DataFrame, kappa: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(1.0, color="0.6", lw=1, ls="--", zorder=1)
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(res["h"], res["b_re"], "o-", label=r"$b_{re}^{(H)}$  (returns)")
    ax.plot(res["h"], res["b_dg"], "s-", label=r"$b_{\Delta d}^{(H)}$  ($-$dividend growth)")
    ax.plot(res["h"], res["b_dp"], "^-", label=r"$b_{dp}^{(H)}$  ($\kappa^{H} dp_{t+H}$)")
    ax.set_xlabel("Horizon $H$ (years)")
    ax.set_ylabel("Slope coefficient")
    ax.set_title(f"Q1(b): Equation 1.4 variance decomposition  ($\\kappa = {kappa:.4f}$)")
    ax.set_xticks(range(2, H_MAX + 1, 2))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_CSV)
    dp_bar = df["dp"].mean()
    kappa = 1.0 / (1.0 + np.exp(dp_bar))

    res = horizon_slopes(df, kappa)

    csv_path = OUT_DIR / "q1b_slopes.csv"
    png_path = OUT_DIR / "q1b_slopes.png"
    res.to_csv(csv_path, index=False)
    make_figure(res, kappa, png_path)

    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"N monthly obs        : {len(df)}  ({df.index[0]} .. {df.index[-1]})")
    print(f"dp_bar (sample mean) : {dp_bar:.6f}")
    print(f"kappa                : {kappa:.6f}")
    print()
    print(res.to_string(index=False))
    print()
    print(f"wrote {csv_path}")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
