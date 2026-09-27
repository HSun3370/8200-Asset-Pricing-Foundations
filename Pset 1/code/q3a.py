"""
Pset 1, Question 3(a) -- construct MOM from CRSP and validate it against the
Chen-Zimmermann (2022) Mom12m signal.

Student specification:
  Two momentum variants are built for stock j at the end of month tau:

    MOM_skip    = prod_{k=2}^{12} ( 1 + r_{j,tau-k} ) - 1    (11 returns, tau-12..tau-2;
                                                              skips the most recent month)
    MOM_noskip  = prod_{k=1}^{12} ( 1 + r_{j,tau-k} ) - 1    (12 returns, tau-12..tau-1)

  MOM_noskip matches the definition in the problem statement (footnote 4) and the stated
  definition of the CZ column; MOM_skip is the Jegadeesh-Titman 12-1 convention. Both are
  computed so the two can be compared against MOM_CZ.

  Missing-return handling (student's decision): every calendar month in a variant's window
  must be present as a row for that permno; a CRSP return that is blank or carries a letter
  code (e.g. 'C') is treated as a 0% return for that month. Because the two windows differ,
  the two variants have different valid samples (noskip is the stricter one).

  MOM_CZ = Mom12m from openassetpricing. Merge on (permno, yyyymm), drop missing, then for
  each month run a cross-firm OLS regression, separately for each variant,

      MOM_CZ_{j,tau} = a_tau + b_tau * MOM_{j,tau} + e_{j,tau}

  and plot the time series of a_tau, b_tau and R^2_tau. Each of the three figures overlays
  both variants.

Run Pset 1/code/q3a_filter_crsp.py first (applies the SIC exclusions to CRSP.csv).
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

# variant -> (first lag, last lag) used in the compounding window
VARIANTS = {
    "skip": (2, 12),    # tau-12 .. tau-2, 11 returns
    "noskip": (1, 12),  # tau-12 .. tau-1, 12 returns
}
LABELS = {
    "skip": "skip $\\tau-1$ (11 returns)",
    "noskip": "no skip (12 returns)",
}
COLORS = {"skip": "tab:blue", "noskip": "tab:red"}


def load_mom() -> pd.DataFrame:
    """Build both MOM variants per (permno, yyyymm) from the filtered CRSP extract."""
    df = pd.read_csv(CRSP_CSV, dtype={"RET": str}, parse_dates=["date"])
    df["mi"] = df["date"].dt.year * 12 + df["date"].dt.month  # month index
    df = df.sort_values(["PERMNO", "mi"], ignore_index=True)

    # blank / letter-coded returns -> 0% for that month (student's decision)
    ret = pd.to_numeric(df["RET"], errors="coerce").fillna(0.0)
    permno, mi = df["PERMNO"], df["mi"]

    n = len(df)
    gross = {v: np.ones(n) for v in VARIANTS}
    ok = {v: np.ones(n, dtype=bool) for v in VARIANTS}

    max_lag = max(hi for _, hi in VARIANTS.values())
    for k in range(1, max_lag + 1):
        # rows are sorted by (PERMNO, mi), so a plain shift is the k-th previous row;
        # require it to be the same permno AND exactly k calendar months earlier
        same = ((permno.shift(k) == permno) & (mi.shift(k) == mi - k)).to_numpy()
        r_lag = ret.shift(k).fillna(0.0).to_numpy()
        for v, (lo, hi) in VARIANTS.items():
            if lo <= k <= hi:
                ok[v] &= same
                gross[v] *= 1.0 + r_lag

    print(f"CRSP rows                    : {n:,}")
    for v in VARIANTS:
        df[f"MOM_{v}"] = np.where(ok[v], gross[v] - 1.0, np.nan)
        print(f"  valid MOM_{v:<7}          : {int(ok[v].sum()):,}")

    df["yyyymm"] = df["date"].dt.year * 100 + df["date"].dt.month
    cols = ["PERMNO", "yyyymm"] + [f"MOM_{v}" for v in VARIANTS]
    keep = np.logical_or.reduce([ok[v] for v in VARIANTS])
    return df.loc[keep, cols].rename(columns={"PERMNO": "permno"})


def load_cz() -> pd.DataFrame:
    """Download (and cache) the Chen-Zimmermann signals."""
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


def monthly_regressions(d: pd.DataFrame, xcol: str) -> pd.DataFrame:
    """Cross-firm OLS of MOM_CZ on `xcol`, month by month, fully vectorised.

    Per month: b = Cov(x,y)/Var(x), a = ybar - b*xbar, R^2 = Corr(x,y)^2.
    """
    d = d.dropna(subset=[xcol, "MOM_CZ"])
    d = d.assign(
        xy=d[xcol] * d["MOM_CZ"], xx=d[xcol] ** 2, yy=d["MOM_CZ"] ** 2
    )
    g = d.groupby("yyyymm").agg(
        n=(xcol, "size"),
        sx=(xcol, "sum"),
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
        print(f"  {xcol}: months dropped (n<3 or no variation): {dropped}")
    return res.loc[keep, ["n", "intercept", "slope", "r2"]]


def make_figures(res: pd.DataFrame) -> None:
    specs = [
        ("intercept", "Intercept $a_\\tau$", "q3a_intercept.png", 0.0),
        ("slope", "Slope $b_\\tau$", "q3a_slope.png", 1.0),
        ("r2", "$R^2_\\tau$", "q3a_r2.png", 1.0),
    ]
    for stat, ylabel, fname, ref in specs:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.axhline(ref, color="0.6", lw=1, ls="--", zorder=1)
        for v in VARIANTS:
            ax.plot(
                res["date"], res[f"{stat}_{v}"], lw=0.9,
                color=COLORS[v], label=LABELS[v], zorder=2,
            )
        ax.set_xlabel("Month")
        ax.set_ylabel(ylabel)
        ax.set_title(f"Q3(a): cross-firm regression of $MOM_{{CZ}}$ on my $MOM$ - {ylabel}")
        ax.legend(loc="best", fontsize=9)
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

    parts = []
    for v in VARIANTS:
        r = monthly_regressions(merged, f"MOM_{v}")
        parts.append(r.add_suffix(f"_{v}"))
    res = pd.concat(parts, axis=1).reset_index()
    res["date"] = pd.to_datetime(res["yyyymm"].astype(str), format="%Y%m")

    csv_path = OUT_DIR / "q3a_monthly_regressions.csv"
    res.to_csv(csv_path, index=False)
    make_figures(res)

    pd.set_option("display.float_format", lambda x: f"{x:10.4f}")
    print(f"\nmonths with a regression     : {len(res):,}"
          f"  ({res['date'].min():%Y-%m} .. {res['date'].max():%Y-%m})")
    for v in VARIANTS:
        print(f"\n--- MOM_{v} ({LABELS[v]}) ---")
        print(res[[f"n_{v}", f"intercept_{v}", f"slope_{v}", f"r2_{v}"]]
              .describe().loc[["mean", "std", "min", "50%", "max"]])
    print(f"\nwrote {csv_path}")


if __name__ == "__main__":
    main()
