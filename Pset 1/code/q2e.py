"""
Pset 1, Question 2(e) -- repeat Question 2(d) with the out-of-sample forecast restricted
by the steady-state valuation model: a_t = G_t - 1 and b_t = G_t.

Student specification (as given; decisions recorded 2026-09-12):
  "everything keeps the sample, but change how to calculate E_OS [xR_{e,t}]";
  G_t is the historical average of exp(Delta d_t), a_t = G_t - 1, b_t = G_t.

  * Sample, forecast dates (t+1 = Dec 1940 .. end), expanding windows, the historical
    mean xR_bar_t and the in-sample forecast E_IS are those of Question 2(d); they are
    taken from q2d.os_forecasts, so they are identical by construction.
  * E_OS = (G_t - 1) + G_t * (D/P)_t, with G_t the average of exp(dg) over the same
    expanding window of (t, t+1) pairs used for xR_bar_t. G_WINDOW records which months
    of Delta d that window covers (student's decision, see AI_INTERACTIONS.md):
      "xr_months"        -- the months of the xR_{e,t+1} values averaged in xR_bar_t
                            (first forecast: Dec 1928 .. Nov 1940)
      "regressor_months" -- the regressor months t of the same pairs
                            (first forecast: Dec 1927 .. Nov 1939)
  * R^2_OS = 1 - SSE/SST over the same forecasts, SST around the evaluation-period
    sample mean, no degrees-of-freedom adjustment; rolling R^2_OS over 600-month windows
    reported Dec 1990 .. end. Both computed with q2d.r2_os / q2d.rolling_r2_os.

Outputs (paths relative to "Pset 1"):
  output/q2e_forecasts.csv, output/q2e_rolling_r2os.csv, output/q2e_summary.csv,
  output/q2e_forecasts.png, output/q2e_rolling_r2os.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from q2b import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, load_data
from q2d import ROLL_MONTHS, os_forecasts, r2_os, rolling_r2_os

G_WINDOW = "regressor_months"  # student decision, 2026-09-12 (AI_INTERACTIONS.md Entry 9)
G_OFFSET = {"xr_months": MONTHS_PER_YEAR, "regressor_months": 0}


def restricted_forecasts(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """Q2(d) forecast frame with E_OS replaced by (G_t - 1) + G_t (D/P)_t."""
    if G_WINDOW not in G_OFFSET:
        raise ValueError(f"G_WINDOW must be one of {sorted(G_OFFSET)}; got {G_WINDOW!r}")
    off = G_OFFSET[G_WINDOW]
    H = MONTHS_PER_YEAR
    dates = df.index
    g = np.exp(df["dg"]).to_numpy()
    dp = np.exp(df["dp"]).to_numpy()

    base, a_is, b_is = os_forecasts(df)
    fc = base.rename(columns={"a_t": "a_t_q2d", "b_t": "b_t_q2d", "E_OS": "E_OS_q2d"})

    rows = []
    for target in fc.index:
        j = dates.get_loc(target)
        s0 = j - H                                      # row of t (forecast origin)
        assert fc.at[target, "origin"] == dates[s0]
        # the Q2(d) window is pairs s = 0 .. s0-1; Delta d is taken at rows s + off
        g_win = g[off : s0 + off]
        G_t = float(g_win.mean())
        rows.append(
            {
                "target": target,
                "G_t": G_t,
                "g_n": len(g_win),
                "g_first_month": dates[off],
                "g_last_month": dates[s0 + off - 1],
                "E_OS": (G_t - 1.0) + G_t * dp[s0],
            }
        )
    fc = fc.join(pd.DataFrame(rows).set_index("target"))
    assert (fc["g_n"] == fc["n_train"]).all(), "G_t window length differs from Q2(d) window"
    fc["a_t"] = fc["G_t"] - 1.0
    fc["b_t"] = fc["G_t"]
    return fc, a_is, b_is


def plot_forecasts(fc: pd.DataFrame, path: Path) -> None:
    t = fc.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(t, fc["E_OS"], color="C0", lw=1.2,
            label=r"$\hat{E}^{OS}_t[xR_e]$  ($a_t = \bar{G}_t - 1$, $b_t = \bar{G}_t$)")
    ax.plot(t, fc["E_IS"], color="C1", lw=1.2,
            label=r"$\hat{E}^{IS}_t[xR_e]$  (full-sample OLS, Eq. 2.2)")
    ax.plot(t, fc["xR_bar"], color="C2", lw=1.8,
            label=r"$\overline{xR}_{e,t}$  (expanding-window mean)")
    ax.set_xlabel(r"Month of $xR_{e,t+1}$")
    ax.set_ylabel("Forecast of one-year excess return")
    ax.set_title("Q2(e): in-sample, restricted out-of-sample and historical-mean forecasts")
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
    ax.set_title(r"Q2(e): 50-year (600-month) rolling $R^2_{OS}$, restricted forecast")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_CSV)
    fc, a_is, b_is = restricted_forecasts(df)

    y = fc["xR_actual"].to_numpy()
    r2, sse, sst = r2_os(y, fc["E_OS"].to_numpy())
    r2_q2d, _, _ = r2_os(y, fc["E_OS_q2d"].to_numpy())
    roll = rolling_r2_os(fc)

    first = fc.iloc[0]
    summary = pd.DataFrame(
        [
            ("g_window", G_WINDOW),
            ("n_forecasts", len(fc)),
            ("first_target", fc.index[0]),
            ("last_target", fc.index[-1]),
            ("g_first_n", int(first["g_n"])),
            ("g_first_start", first["g_first_month"]),
            ("g_first_end", first["g_last_month"]),
            ("G_first", float(first["G_t"])),
            ("G_last", float(fc["G_t"].iloc[-1])),
            ("a_is", a_is),
            ("b_is", b_is),
            ("sse", sse),
            ("sst", sst),
            ("r2_os", r2),
            ("r2_os_q2d_reference", r2_q2d),
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

    fc.to_csv(OUT_DIR / "q2e_forecasts.csv")
    roll.to_csv(OUT_DIR / "q2e_rolling_r2os.csv")
    summary.to_csv(OUT_DIR / "q2e_summary.csv", index=False)
    plot_forecasts(fc, OUT_DIR / "q2e_forecasts.png")
    plot_rolling(roll, OUT_DIR / "q2e_rolling_r2os.png")

    print(f"G_WINDOW             : {G_WINDOW}")
    print(f"In-sample Eq. 2.2    : a_hat = {a_is:.6f}, b_hat = {b_is:.6f}")
    print(
        f"Forecasts            : {len(fc)} ({fc.index[0]} .. {fc.index[-1]}); first G_t = "
        f"{first['G_t']:.6f} from {int(first['g_n'])} months "
        f"({first['g_first_month']} .. {first['g_last_month']}); last G_t = {fc['G_t'].iloc[-1]:.6f}"
    )
    print(f"SSE, SST             : {sse:.6f}, {sst:.6f}")
    print(f"R^2_OS (restricted)  : {r2:.6f}")
    print(f"R^2_OS (Q2(d) check) : {r2_q2d:.6f}")
    print(
        f"Rolling R^2_OS       : {len(roll)} windows of {ROLL_MONTHS} months, ends "
        f"{roll.index[0]} .. {roll.index[-1]} (first window starts "
        f"{roll['window_start'].iloc[0]}); min {roll['r2_os'].min():.4f} "
        f"({roll['r2_os'].idxmin()}), max {roll['r2_os'].max():.4f} ({roll['r2_os'].idxmax()})"
    )
    for name in ("q2e_forecasts.csv", "q2e_rolling_r2os.csv", "q2e_summary.csv",
                 "q2e_forecasts.png", "q2e_rolling_r2os.png"):
        print(f"wrote {OUT_DIR / name}")


if __name__ == "__main__":
    main()
