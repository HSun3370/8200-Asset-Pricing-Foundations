"""
Pset 1, Question 4(a) -- Fama-Bliss discount bond log yields, log forward rates and log
annual returns, and the average excess measures xy, xf, xr for H = 2..5.

Student specification (as given; decisions recorded 2026-09-12):
  Data: Bond Dataset.csv. MCALDT is the date, TMYTM the yield in percent (Y^(H)_t * 100).
        Maturity H in years comes from TTERMTYPE (5001..5005 -> H = 1..5), checked against
        TTERMLBL ("1-Year" .. "5-Year"). Bonds are paired by the year and month of MCALDT
        (MCALDT is the last trading day of the month, which varies).
  1. Log yields          y^(H)_t = log(1 + Y^(H)_t),                  H = 1..5
  3. Log forward rates   f^(H)_t = H y^(H)_t - (H-1) y^(H-1)_t,       H = 2..5, same month
  4. Log annual returns  r^(H)_t = H y^(H)_{t-1} - (H-1) y^(H-1)_t,   H = 2..5, where t-1 is
                                                                      the same month one
                                                                      year earlier
  5. Averages for H = 2..5 of
        xy^(H)_t = y^(H)_t - y^(1)_t
        xf^(H)_t = f^(H)_t - y^(1)_t
        xr^(H)_t = r^(H)_t - benchmark        benchmark set by XR_BENCHMARK
     taken over the months set by AVG_SAMPLE.

  XR_BENCHMARK (student's decision, see AI_INTERACTIONS.md):
    "y1_t" -- subtract y^(1)_t, as in the student's original prompt
    "r1_t" -- subtract r^(1)_t = 1*y^(1)_{t-1} - 0*y^(0)_t = y^(1)_{t-1}, the problem set's
              definition xr^(H) = r^(H) - r^(1)
  AVG_SAMPLE (student's decision, see AI_INTERACTIONS.md):
    "own"    -- each measure averaged over all months in which it exists
    "common" -- all measures averaged over the months in which xr exists

Plots: one figure per variable (log yields, forward rates, log returns), one line per
maturity, values shown x100. CSVs keep decimal log units.

Outputs (paths relative to "Pset 1"):
  output/q4a_log_yields.csv, output/q4a_log_yields.png,
  output/q4a_forward_rates.csv, output/q4a_forward_rates.png,
  output/q4a_log_returns.csv, output/q4a_log_returns.png,
  output/q4a_excess_series.csv, output/q4a_average_excess.csv, output/q4a_summary.csv
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 1
DATA_CSV = PSET_DIR / "Bond Dataset.csv"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

MATURITIES = [1, 2, 3, 4, 5]
EXCESS_H = [2, 3, 4, 5]
MONTHS_PER_YEAR = 12

XR_BENCHMARK = "r1_t"  # student decision, 2026-09-12 (AI_INTERACTIONS.md Entry 10)
AVG_SAMPLE = "own"  # student decision, 2026-09-12 (AI_INTERACTIONS.md Entry 10)


def load_percent_yields(path: Path) -> pd.DataFrame:
    """Month x maturity table of TMYTM (percent), indexed by year-month of MCALDT."""
    df = pd.read_csv(path)
    df["H"] = df["TTERMTYPE"] - 5000
    for H, label in df.groupby("H")["TTERMLBL"].first().items():
        assert f"{H}-Year" in label, f"TTERMTYPE {5000 + H} has label {label!r}"
    df["ym"] = pd.to_datetime(df["MCALDT"]).dt.to_period("M")
    assert not df.duplicated(["H", "ym"]).any(), "more than one yield for a maturity-month"

    wide = df.pivot(index="ym", columns="H", values="TMYTM").sort_index()
    assert list(wide.columns) == MATURITIES, list(wide.columns)
    full = pd.period_range(wide.index[0], wide.index[-1], freq="M")
    assert wide.index.equals(full), "months missing from the date range"
    assert wide.notna().all().all(), "missing yields -- treatment not specified"
    return wide


def build_series(wide: pd.DataFrame) -> dict[str, pd.DataFrame]:
    y = np.log(1.0 + wide / 100.0)                              # columns H = 1..5

    # same month one year earlier, matched on year-month
    y_prev = y.reindex(y.index - MONTHS_PER_YEAR)
    y_prev.index = y.index

    f = pd.DataFrame({H: H * y[H] - (H - 1) * y[H - 1] for H in EXCESS_H})
    r = pd.DataFrame({H: H * y_prev[H] - (H - 1) * y[H - 1] for H in EXCESS_H})

    benchmark = {"y1_t": y[1], "r1_t": y_prev[1]}[XR_BENCHMARK]
    xy = pd.DataFrame({H: y[H] - y[1] for H in EXCESS_H})
    xf = pd.DataFrame({H: f[H] - y[1] for H in EXCESS_H})
    xr = pd.DataFrame({H: r[H] - benchmark for H in EXCESS_H})
    return {"y": y, "f": f, "r": r, "xy": xy, "xf": xf, "xr": xr}


def averages(s: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    if AVG_SAMPLE == "common":
        keep = s["xr"].notna().all(axis=1)
        frames = {k: s[k][keep] for k in ("xy", "xf", "xr")}
    else:
        frames = {k: s[k] for k in ("xy", "xf", "xr")}

    avg = pd.DataFrame({f"avg_{k}": v.mean() for k, v in frames.items()})
    avg.index.name = "H"

    info = []
    for k, v in frames.items():
        rows = v.dropna(how="any")
        info.append((k, len(rows), rows.index[0], rows.index[-1]))
    info = pd.DataFrame(info, columns=["measure", "n_months", "first_month", "last_month"])
    return avg, info


def plot_lines(frame: pd.DataFrame, labels: dict, title: str, ylabel: str, path: Path) -> None:
    t = frame.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    for i, (col, label) in enumerate(labels.items()):
        ax.plot(t, 100 * frame[col], color=f"C{i}", lw=1.0, label=label)
    ax.set_xlabel("Month (MCALDT)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    if XR_BENCHMARK not in ("y1_t", "r1_t"):
        raise ValueError(f"XR_BENCHMARK must be 'y1_t' or 'r1_t'; got {XR_BENCHMARK!r}")
    if AVG_SAMPLE not in ("own", "common"):
        raise ValueError(f"AVG_SAMPLE must be 'own' or 'common'; got {AVG_SAMPLE!r}")

    wide = load_percent_yields(DATA_CSV)
    s = build_series(wide)
    avg, info = averages(s)

    def named(frame: pd.DataFrame, prefix: str) -> pd.DataFrame:
        out = frame.rename(columns=lambda H: f"{prefix}{H}")
        out.index.name = "month"
        return out

    named(s["y"], "y").to_csv(OUT_DIR / "q4a_log_yields.csv")
    named(s["f"], "f").to_csv(OUT_DIR / "q4a_forward_rates.csv")
    named(s["r"], "r").to_csv(OUT_DIR / "q4a_log_returns.csv")
    pd.concat([named(s["xy"], "xy"), named(s["xf"], "xf"), named(s["xr"], "xr")], axis=1).to_csv(
        OUT_DIR / "q4a_excess_series.csv"
    )
    avg.to_csv(OUT_DIR / "q4a_average_excess.csv")

    r_valid = s["r"].dropna(how="any")
    summary = pd.DataFrame(
        [
            ("xr_benchmark", XR_BENCHMARK),
            ("avg_sample", AVG_SAMPLE),
            ("first_month", s["y"].index[0]),
            ("last_month", s["y"].index[-1]),
            ("n_months", len(s["y"])),
            ("r_first_month", r_valid.index[0]),
            ("r_n_months", len(r_valid)),
        ]
        + [(f"{m}_{field}", row[field]) for _, row in info.iterrows()
           for m in [row["measure"]] for field in ("n_months", "first_month", "last_month")],
        columns=["parameter", "value"],
    )
    summary.to_csv(OUT_DIR / "q4a_summary.csv", index=False)

    plot_lines(s["y"], {H: rf"$y^{{({H})}}_t$" for H in MATURITIES},
               "Q4(a): log yields of Fama-Bliss discount bonds", r"Log yield $\times 100$",
               OUT_DIR / "q4a_log_yields.png")
    plot_lines(s["f"], {H: rf"$f^{{({H})}}_t$" for H in EXCESS_H},
               "Q4(a): log forward rates", r"Log forward rate $\times 100$",
               OUT_DIR / "q4a_forward_rates.png")
    plot_lines(s["r"], {H: rf"$r^{{({H})}}_t$" for H in EXCESS_H},
               "Q4(a): log annual holding-period returns", r"Log annual return $\times 100$",
               OUT_DIR / "q4a_log_returns.png")

    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"XR_BENCHMARK = {XR_BENCHMARK}, AVG_SAMPLE = {AVG_SAMPLE}")
    print(f"Months: {s['y'].index[0]} .. {s['y'].index[-1]} ({len(s['y'])}); returns from "
          f"{r_valid.index[0]} ({len(r_valid)})")
    print("\nAverage sample by measure:")
    print(info.to_string(index=False))
    print("\nAverages (percent, x100):")
    print((100 * avg).to_string())
    for name in ("q4a_log_yields", "q4a_forward_rates", "q4a_log_returns"):
        print(f"wrote {OUT_DIR / (name + '.csv')} and .png")
    for name in ("q4a_excess_series.csv", "q4a_average_excess.csv", "q4a_summary.csv"):
        print(f"wrote {OUT_DIR / name}")


if __name__ == "__main__":
    main()
