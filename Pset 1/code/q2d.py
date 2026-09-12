"""
Pset 1, Question 2(d) -- out-of-sample (OS) expanding-window forecasts of the
one-year-ahead excess equity return from D/P, the full-period R^2_OS, and a 50-year
rolling R^2_OS.

Student specification (as given; decisions recorded 2026-09-12):
  Variables, as in Q2(a)-(c): xR_t = exp(re_t) - exp(rf_t), (D/P)_t = exp(dp_t);
  "t+1" is one year after t = 12 rows ahead in the monthly dataset.

  1. OS forecasts.  xR_{e,t+1} = a_t + b_t (D/P)_t + eps_{t+1}.
     First forecast: t = Dec 1939, t+1 = Dec 1940. For each forecast, a_t and b_t are
     estimated by OLS on the expanding window of pairs from (t, t+1) = (Dec 1927,
     Dec 1928) through the pair one month before the forecast pair -- for the first
     forecast, through (Nov 1939, Nov 1940), 144 pairs. [Student's decision, taken
     after AI pointed out that the last pairs' returns are realized after the Dec 1939
     forecast origin and overlap the forecasted return.]
         E_OS = a_t + b_t (D/P)_t
     Historical mean xR_bar_t = mean of the dependent-variable values in the same
     window (first forecast: xR from Dec 1928 through Nov 1940).
     In-sample forecast E_IS = a_hat + b_hat (D/P)_t, with a_hat, b_hat from the
     full-sample Equation 2.2 regression of Q2(b).
     Plot E_OS, E_IS and xR_bar against the month of xR_{e,t+1}, Dec 1940 .. end.

  2. R^2_OS = 1 - SSE/SST over the forecasts with t+1 from Dec 1940 to the end of the
     sample, no degrees-of-freedom adjustment:
         SSE = sum (xR_{e,t+1} - E_OS)^2
         SST = sum (xR_{e,t+1} - mu)^2,  mu = sample mean of xR_{e,t+1} over the same
               months [student's decision].

  3. Rolling R^2_OS over 600-month (50-year) windows of the forecast errors, reported at
     the window's last month from Dec 1990 to the end of the sample, so the first window
     is Jan 1941 .. Dec 1990 [student's decision]. a_t and b_t are unchanged; SST uses
     the sample mean of xR_{e,t+1} within each window.

Outputs (paths relative to "Pset 1"):
  output/q2d_forecasts.csv, output/q2d_rolling_r2os.csv, output/q2d_summary.csv,
  output/q2d_forecasts.png, output/q2d_rolling_r2os.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from q2b import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, load_data

FIRST_TARGET = pd.Period("1940-12", freq="M")       # first xR_{e,t+1} forecasted
ROLL_MONTHS = 50 * MONTHS_PER_YEAR                   # 600 forecast errors per window
ROLL_FIRST_END = pd.Period("1990-12", freq="M")      # first rolling window ends here


def ols(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Intercept and slope of y = a + b x (OLS)."""
    b, a = np.polyfit(x, y, 1)
    return float(a), float(b)


def r2_os(y: np.ndarray, forecast: np.ndarray) -> tuple[float, float, float]:
    """R^2_OS = 1 - SSE/SST, with SST around the sample mean of y."""
    sse = float(((y - forecast) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    return 1.0 - sse / sst, sse, sst


def os_forecasts(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    dates = df.index
    xr = (np.exp(df["re"]) - np.exp(df["rf"])).to_numpy()
    dp = np.exp(df["dp"]).to_numpy()
    N, H = len(df), MONTHS_PER_YEAR

    # full-sample Equation 2.2 (Q2(b)): regressor rows 0..N-1-H, target rows H..N-1
    a_is, b_is = ols(dp[: N - H], xr[H:])

    rows = []
    for j in range(dates.get_loc(FIRST_TARGET), N):   # j = row of xR_{e,t+1}
        s0 = j - H                                     # row of t (forecast origin)
        # expanding window: pairs s = 0 .. s0-1, i.e. regressors dp[0:s0], targets xr[H:j]
        x_tr, y_tr = dp[:s0], xr[H:j]
        a_t, b_t = ols(x_tr, y_tr)
        rows.append(
            {
                "target": dates[j],
                "origin": dates[s0],
                "n_train": len(y_tr),
                "last_train_regressor": dates[s0 - 1],
                "last_train_target": dates[j - 1],
                "a_t": a_t,
                "b_t": b_t,
                "xR_actual": xr[j],
                "E_OS": a_t + b_t * dp[s0],
                "E_IS": a_is + b_is * dp[s0],
                "xR_bar": float(y_tr.mean()),
            }
        )
    return pd.DataFrame(rows).set_index("target"), a_is, b_is


def rolling_r2_os(fc: pd.DataFrame) -> pd.DataFrame:
    y = fc["xR_actual"].to_numpy()
    f = fc["E_OS"].to_numpy()
    k0 = fc.index.get_loc(ROLL_FIRST_END)
    assert k0 - ROLL_MONTHS + 1 >= 0, "first rolling window starts before Dec 1940"

    rows = []
    for k in range(k0, len(fc)):
        w = slice(k - ROLL_MONTHS + 1, k + 1)
        r2, _, _ = r2_os(y[w], f[w])
        rows.append(
            {
                "window_end": fc.index[k],
                "window_start": fc.index[k - ROLL_MONTHS + 1],
                "n": ROLL_MONTHS,
                "r2_os": r2,
            }
        )
    return pd.DataFrame(rows).set_index("window_end")


def plot_forecasts(fc: pd.DataFrame, path: Path) -> None:
    t = fc.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(t, fc["E_OS"], color="C0", lw=1.2,
            label=r"$\hat{E}^{OS}_t[xR_e]$  (expanding-window OLS)")
    ax.plot(t, fc["E_IS"], color="C1", lw=1.2,
            label=r"$\hat{E}^{IS}_t[xR_e]$  (full-sample OLS, Eq. 2.2)")
    ax.plot(t, fc["xR_bar"], color="C2", lw=1.8,
            label=r"$\overline{xR}_{e,t}$  (expanding-window mean)")
    ax.set_xlabel(r"Month of $xR_{e,t+1}$")
    ax.set_ylabel("Forecast of one-year excess return")
    ax.set_title("Q2(d): in-sample, out-of-sample and historical-mean forecasts")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_rolling(roll: pd.DataFrame, path: Path) -> None:
    t = roll.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(t, roll["r2_os"], color="C0", lw=1.4)
    ax.set_xlabel("Last month of the 600-month window")
    ax.set_ylabel(r"$R^2_{OS}$")
    ax.set_title(r"Q2(d): 50-year (600-month) rolling $R^2_{OS}$")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_CSV)
    fc, a_is, b_is = os_forecasts(df)

    r2, sse, sst = r2_os(fc["xR_actual"].to_numpy(), fc["E_OS"].to_numpy())
    roll = rolling_r2_os(fc)

    first = fc.iloc[0]
    summary = pd.DataFrame(
        [
            ("n_forecasts", len(fc)),
            ("first_target", fc.index[0]),
            ("last_target", fc.index[-1]),
            ("n_train_first", int(first["n_train"])),
            ("first_last_train_regressor", first["last_train_regressor"]),
            ("first_last_train_target", first["last_train_target"]),
            ("a_is", a_is),
            ("b_is", b_is),
            ("sse", sse),
            ("sst", sst),
            ("r2_os", r2),
            ("roll_months", ROLL_MONTHS),
            ("roll_first_start", roll["window_start"].iloc[0]),
            ("roll_first_end", roll.index[0]),
            ("roll_last_end", roll.index[-1]),
            ("roll_n_windows", len(roll)),
            ("roll_r2_min", roll["r2_os"].min()),
            ("roll_r2_min_end", roll["r2_os"].idxmin()),
            ("roll_r2_max", roll["r2_os"].max()),
            ("roll_r2_max_end", roll["r2_os"].idxmax()),
        ],
        columns=["parameter", "value"],
    )

    fc.to_csv(OUT_DIR / "q2d_forecasts.csv")
    roll.to_csv(OUT_DIR / "q2d_rolling_r2os.csv")
    summary.to_csv(OUT_DIR / "q2d_summary.csv", index=False)
    plot_forecasts(fc, OUT_DIR / "q2d_forecasts.png")
    plot_rolling(roll, OUT_DIR / "q2d_rolling_r2os.png")

    print(f"In-sample Eq. 2.2    : a_hat = {a_is:.6f}, b_hat = {b_is:.6f}")
    print(
        f"OS forecasts         : {len(fc)} ({fc.index[0]} .. {fc.index[-1]}); first forecast "
        f"trained on {int(first['n_train'])} pairs, last pair "
        f"({first['last_train_regressor']}, {first['last_train_target']})"
    )
    print(f"First / last a_t,b_t : ({fc['a_t'].iloc[0]:.4f}, {fc['b_t'].iloc[0]:.4f}) / "
          f"({fc['a_t'].iloc[-1]:.4f}, {fc['b_t'].iloc[-1]:.4f})")
    print(f"SSE, SST             : {sse:.6f}, {sst:.6f}")
    print(f"R^2_OS               : {r2:.6f}")
    print(
        f"Rolling R^2_OS       : {len(roll)} windows of {ROLL_MONTHS} months, ends "
        f"{roll.index[0]} .. {roll.index[-1]} (first window starts "
        f"{roll['window_start'].iloc[0]}); min {roll['r2_os'].min():.4f} "
        f"({roll['r2_os'].idxmin()}), max {roll['r2_os'].max():.4f} ({roll['r2_os'].idxmax()})"
    )
    for name in ("q2d_forecasts.csv", "q2d_rolling_r2os.csv", "q2d_summary.csv",
                 "q2d_forecasts.png", "q2d_rolling_r2os.png"):
        print(f"wrote {OUT_DIR / name}")


if __name__ == "__main__":
    main()
