"""
Pset 1, Question 3(a) -- construct MOM from CRSP and validate it against the
Chen-Zimmermann (2022) Mom12m signal.

Student specification:
  MOM for stock j at the end of month tau compounds the 12 monthly returns over
  tau-12 ... tau-1, matching footnote 4 of the problem statement and the stated
  definition of the CZ column:

      MOM_{j,tau} = prod_{k=1}^{12} ( 1 + r_{j,tau-k} ) - 1

  Missing-return handling (student's decision): all 12 calendar months must be present
  as rows for that permno; a CRSP return that is blank or carries a letter code (e.g.
  'C') is treated as a 0% return for that month.

  MOM_CZ = Mom12m from openassetpricing. Merge on (permno, yyyymm), drop missing, then
  for each month run a cross-firm OLS regression

      MOM_CZ_{j,tau} = a_tau + b_tau * MOM_{j,tau} + e_{j,tau}

  and plot the time series of a_tau, b_tau and R^2_tau as three figures.

Run Pset 1/code/q3a_filter_crsp.py first (applies the SIC exclusions to CRSP.csv).
The CZ signals are downloaded on first use, or assembled by q3a_build_cz_cache.py when
the project's Google Drive share is rate-limited.

Outputs: output/q3a_monthly_regressions.csv and output/q3a_{intercept,slope,r2}.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
OUT_DIR = PSET_DIR / "output"
CACHE_DIR = PSET_DIR / "data_cache"
OUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
CZ_CACHE = CACHE_DIR / "cz_signals.parquet"

WINDOW = 12  # compound returns over tau-12 ... tau-1


def load_mom() -> pd.DataFrame:
    """Build MOM per (permno, yyyymm) from the filtered CRSP extract."""
    df = pd.read_csv(
        CRSP_CSV, dtype={"RET": str, "SICCD": str}, parse_dates=["date"]
    )
    df["mi"] = df["date"].dt.year * 12 + df["date"].dt.month  # month index
    df = df.sort_values(["PERMNO", "mi"], ignore_index=True)

    # blank / letter-coded returns -> 0% for that month (student's decision)
    ret = pd.to_numeric(df["RET"], errors="coerce").fillna(0.0)
    permno, mi = df["PERMNO"], df["mi"]

    gross = np.ones(len(df))
    ok = np.ones(len(df), dtype=bool)
    for k in range(1, WINDOW + 1):
        # rows are sorted by (PERMNO, mi), so a plain shift is the k-th previous row;
        # require it to be the same permno AND exactly k calendar months earlier
        ok &= ((permno.shift(k) == permno) & (mi.shift(k) == mi - k)).to_numpy()
        gross *= 1.0 + ret.shift(k).fillna(0.0).to_numpy()

    df["MOM"] = np.where(ok, gross - 1.0, np.nan)
    df["yyyymm"] = df["date"].dt.year * 100 + df["date"].dt.month

    print(f"CRSP rows                    : {len(df):,}")
    print(f"  with a valid MOM           : {int(ok.sum()):,}")
    return df.loc[ok, ["PERMNO", "yyyymm", "MOM"]].rename(columns={"PERMNO": "permno"})


def load_cz() -> pd.DataFrame:
    """Load the Chen-Zimmermann signals, downloading them if not already cached."""
    if CZ_CACHE.exists():
        cz = pd.read_parquet(CZ_CACHE)
        print(f"CZ signals (cached)          : {len(cz):,}")
    else:
        import openassetpricing as oap

        openap = oap.OpenAP()
        cz = openap.dl_signal("pandas", ["BMdec", "Mom12m", "GP"])
        cz.to_parquet(CZ_CACHE, index=False)
        print(f"CZ signals (downloaded)      : {len(cz):,}")
    return cz[["permno", "yyyymm", "Mom12m"]].rename(columns={"Mom12m": "MOM_CZ"})


def monthly_regressions(d: pd.DataFrame) -> pd.DataFrame:
    """Cross-firm OLS of MOM_CZ on MOM, month by month, fully vectorised.

    Per month: b = Cov(x,y)/Var(x), a = ybar - b*xbar, R^2 = Corr(x,y)^2.
    """
    d = d.dropna(subset=["MOM", "MOM_CZ"])
    d = d.assign(xy=d["MOM"] * d["MOM_CZ"], xx=d["MOM"] ** 2, yy=d["MOM_CZ"] ** 2)
    g = d.groupby("yyyymm").agg(
        n=("MOM", "size"),
        sx=("MOM", "sum"),
        sy=("MOM_CZ", "sum"),
        sxy=("xy", "sum"),
        sxx=("xx", "sum"),
        syy=("yy", "sum"),
    )

    n = g["n"]
    cov = g["sxy"] / n - (g["sx"] / n) * (g["sy"] / n)
    var_x = g["sxx"] / n - (g["sx"] / n) ** 2
    var_y = g["syy"] / n - (g["sy"] / n) ** 2

    res = pd.DataFrame({"n": n, "slope": cov / var_x, "r2": cov**2 / (var_x * var_y)})
    res["intercept"] = g["sy"] / n - res["slope"] * (g["sx"] / n)

    keep = (n >= 3) & (var_x > 0) & (var_y > 0)
    dropped = int((~keep).sum())
    if dropped:
        print(f"  months dropped (n<3 or no variation): {dropped}")

    res = res.loc[keep].reset_index()
    res["date"] = pd.to_datetime(res["yyyymm"].astype(str), format="%Y%m")
    return res[["yyyymm", "date", "n", "intercept", "slope", "r2"]]


def make_figures(res: pd.DataFrame) -> None:
    specs = [
        ("intercept", "Intercept $a_\\tau$", "q3a_intercept.png", 0.0),
        ("slope", "Slope $b_\\tau$", "q3a_slope.png", 1.0),
        ("r2", "$R^2_\\tau$", "q3a_r2.png", 1.0),
    ]
    for stat, ylabel, fname, ref in specs:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.axhline(ref, color="0.6", lw=1, ls="--", zorder=1)
        ax.plot(res["date"], res[stat], lw=0.9, color="tab:blue", zorder=2)
        ax.set_xlabel("Month")
        ax.set_ylabel(ylabel)
        ax.set_title(f"Q3(a): cross-firm regression of $MOM_{{CZ}}$ on my $MOM$ - {ylabel}")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(OUT_DIR / fname, dpi=150)
        plt.close(fig)
        print(f"wrote {OUT_DIR / fname}")


def main() -> None:
    mom = load_mom()
    cz = load_cz()

    merged = mom.merge(cz, on=["permno", "yyyymm"], how="inner")
    print(f"merged firm-months           : {len(merged):,}")

    res = monthly_regressions(merged)
    csv_path = OUT_DIR / "q3a_monthly_regressions.csv"
    res.to_csv(csv_path, index=False)
    make_figures(res)

    pd.set_option("display.float_format", lambda x: f"{x:10.4f}")
    print(f"\nmonths with a regression     : {len(res):,}"
          f"  ({res['date'].min():%Y-%m} .. {res['date'].max():%Y-%m})")
    print("\nsummary of the monthly estimates:")
    print(res[["n", "intercept", "slope", "r2"]]
          .describe().loc[["mean", "std", "min", "50%", "max"]])
    print(f"\nwrote {csv_path}")


if __name__ == "__main__":
    main()
