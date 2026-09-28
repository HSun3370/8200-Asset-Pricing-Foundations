"""
Pset 1, Question 3(d) -- Fama-MacBeth regressions of next-month excess returns on
cross-sectional signal quantiles.

Signals at month tau:
    BM  = BMdec  and  GP = GP, both the Chen-Zimmermann (2022) versions (as in 3(c));
    Dur = the firm-level equity duration of Goncalves (2021b), from FirmLevel Dur.csv.
          FF.YEAR = t means Dur is public as of June of year t, so it is carried across
          the twelve months July of t through June of t+1 -- the convention documented
          by the author, and the same holding window used in 3(c).

Q^X is the cross-firm PERCENTILE RANK of signal X within month tau, on [0, 1] (the
student's decision), so a slope is the excess return earned by moving a stock from the
bottom to the top of that month's distribution.

Specifications, each estimated by OLS and by WLS with month-tau market-equity weights:
    (i)   xR ~ Q_BM
    (ii)  xR ~ Q_GP
    (iii) xR ~ Q_Dur
    (iv)  xR ~ Q_BM + Q_GP
    (v)   xR ~ Q_Dur + Q_BM
    (vi)  xR ~ Q_Dur + Q_GP
    (vii) xR ~ Q_Dur + Q_BM + Q_GP

Student's decisions:
  * All seven specifications run on a COMMON SAMPLE -- firm-months where BM, GP and Dur
    are all present and market equity is positive -- so the specs are directly
    comparable and adding a regressor is a clean incremental change. Quantiles are
    computed within that common sample each month.
  * xR is the CRSP return less the Ken French RF. A firm-month whose CRSP return is
    blank or letter-coded is dropped (as in 3(c)).
  * Dur vintage: the release updated to 2025, FF.YEAR 1973-2025.

Stage one runs the cross-sectional regression month by month; stage two takes the
time-series mean of each slope with its Newey-West (1987, 1994) t-statistic using the
data-driven bandwidth, implemented exactly as in q2b.py and q3c.py.

Prerequisites: q3a_filter_crsp.py and crsp_add_prc_shrout.py (CRSP.csv must carry PRC
and SHROUT), the CZ cache, the Ken French RF cache written by q3c.py, and
data_cache/FirmLevel_Dur.csv.

Outputs: output/q3d_fama_macbeth.csv and output/q3d_monthly_slopes.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
CZ_CACHE = PSET_DIR / "data_cache" / "cz_signals.parquet"
RF_CACHE = PSET_DIR / "data_cache" / "ff_rf.parquet"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

# the Goncalves duration file, as downloaded from andreigoncalves.com
DUR_CANDIDATES = [
    PSET_DIR / "FirmLevel Dur.csv",
    PSET_DIR / "data_cache" / "FirmLevel_Dur.csv",
]


def dur_path() -> Path:
    for p in DUR_CANDIDATES:
        if p.exists():
            return p
    raise SystemExit(
        "FirmLevel Dur.csv not found. Download 'Dur Portfolios + Dur Estimates "
        "(updated)' from https://andreigoncalves.com/published-papers/ and put "
        f"FirmLevel Dur.csv in {PSET_DIR}."
    )

SPECS = {
    "(i)": ["BM"],
    "(ii)": ["GP"],
    "(iii)": ["Dur"],
    "(iv)": ["BM", "GP"],
    "(v)": ["Dur", "BM"],
    "(vi)": ["Dur", "GP"],
    "(vii)": ["Dur", "BM", "GP"],
}
SIGNALS = ["BM", "GP", "Dur"]
MIN_FIRMS = 10


def mi_to_yyyymm(mi: np.ndarray) -> np.ndarray:
    m0 = mi - 1  # mi = year*12 + month, with month in 1..12
    return (m0 // 12) * 100 + (m0 % 12) + 1


def load_panel() -> pd.DataFrame:
    """Signals and weights at month tau, joined to the excess return at tau+1."""
    crsp = pd.read_csv(CRSP_CSV, dtype={"RET": str, "SICCD": str}, parse_dates=["date"])
    crsp["mi"] = crsp["date"].dt.year * 12 + crsp["date"].dt.month
    crsp["yyyymm"] = crsp["date"].dt.year * 100 + crsp["date"].dt.month
    crsp["ret"] = pd.to_numeric(crsp["RET"], errors="coerce")
    me = crsp["PRC"].abs() * crsp["SHROUT"]
    crsp["me"] = me.where(me > 0)
    crsp = crsp.rename(columns={"PERMNO": "permno"})
    print(f"CRSP rows                    : {len(crsp):,}")

    cz = pd.read_parquet(CZ_CACHE)[["permno", "yyyymm", "BMdec", "GP"]]
    cz = cz.rename(columns={"BMdec": "BM"})

    dur_file = dur_path()
    dur = pd.read_csv(dur_file)
    dur = dur.rename(columns={"PERMNO": "permno", "FF.YEAR": "ff_year"})
    print(f"Dur source                   : {dur_file.name}")
    print(f"Dur firm-years               : {len(dur):,}  "
          f"(FF.YEAR {int(dur['ff_year'].min())}-{int(dur['ff_year'].max())})")

    # FF.YEAR = t is public at June of t, so carry it over July of t .. June of t+1
    rep = dur.loc[dur.index.repeat(12)].copy()
    rep["mi"] = rep["ff_year"].to_numpy() * 12 + 7 + np.tile(np.arange(12), len(dur))
    rep["yyyymm"] = mi_to_yyyymm(rep["mi"].to_numpy())
    dur_m = rep[["permno", "yyyymm", "Dur"]]

    sig = (
        crsp[["permno", "yyyymm", "mi", "me"]]
        .merge(cz, on=["permno", "yyyymm"], how="inner")
        .merge(dur_m, on=["permno", "yyyymm"], how="inner")
    )
    sig = sig.dropna(subset=SIGNALS + ["me"])  # common sample
    print(f"common-sample firm-months    : {len(sig):,}")

    rf = pd.read_parquet(RF_CACHE)
    nxt = crsp.loc[crsp["ret"].notna(), ["permno", "mi", "yyyymm", "ret"]].merge(
        rf, on="yyyymm", how="inner"
    )
    nxt["xret"] = nxt["ret"] - nxt["rf"]
    nxt["mi"] = nxt["mi"] - 1  # line the tau+1 return up with its tau signal row
    nxt = nxt[["permno", "mi", "xret"]]

    panel = sig.merge(nxt, on=["permno", "mi"], how="inner")
    print(f"with a return at tau+1       : {len(panel):,}")

    for s in SIGNALS:
        panel[f"Q_{s}"] = panel.groupby("yyyymm")[s].rank(pct=True)
    return panel.sort_values("yyyymm", ignore_index=True)


def omega(h: np.ndarray, lag: int) -> np.ndarray:
    T = h.shape[0]
    if lag == 0:
        return h.T @ h / T
    return h[lag:].T @ h[:-lag] / (T - lag)


def nw_mean_tstat(x: np.ndarray) -> tuple[float, float, int]:
    """Mean with a Newey-West (1987, 1994) t-statistic, as in q2b.py and q3c.py."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    T = len(x)
    mu = x.mean()
    h = (x - mu)[:, None]
    L = int(kernel_optimal_bandwidth(h, kernel="bartlett"))
    S = omega(h, 0)
    for lag in range(1, L + 1):
        om = omega(h, lag)
        S = S + (1.0 - lag / (L + 1)) * (om + om.T)
    return mu, mu / float(np.sqrt(S[0, 0] / T)), L


def first_stage(panel: pd.DataFrame):
    """Month-by-month cross-sectional slopes for every spec, OLS and WLS."""
    months = panel["yyyymm"].to_numpy()
    uniq, starts = np.unique(months, return_index=True)
    ends = np.append(starts[1:], len(months))

    y = panel["xret"].to_numpy(float)
    w = panel["me"].to_numpy(float)
    Q = {s: panel[f"Q_{s}"].to_numpy(float) for s in SIGNALS}

    out = {(k, m): [] for k in SPECS for m in ("OLS", "WLS")}
    kept = []
    for mth, s, e in zip(uniq, starts, ends):
        n = e - s
        if n < MIN_FIRMS:
            continue
        kept.append((int(mth), int(n)))
        yy, ww = y[s:e], w[s:e]
        for key, vars_ in SPECS.items():
            X = np.column_stack([np.ones(n)] + [Q[v][s:e] for v in vars_])
            for mode in ("OLS", "WLS"):
                rt = np.ones(n) if mode == "OLS" else np.sqrt(ww)
                coef, *_ = np.linalg.lstsq(X * rt[:, None], yy * rt, rcond=None)
                out[(key, mode)].append(coef)

    skipped = len(uniq) - len(kept)
    if skipped:
        print(f"  months skipped (n<{MIN_FIRMS})       : {skipped}")
    return {k: np.asarray(v) for k, v in out.items()}, kept


def main() -> None:
    panel = load_panel()
    slopes, kept = first_stage(panel)
    months = [m for m, _ in kept]
    nfirms = [n for _, n in kept]
    print(f"months in the regression     : {len(kept):,}  ({months[0]} .. {months[-1]})")
    print(f"firms per month              : mean {np.mean(nfirms):,.0f}, "
          f"min {min(nfirms):,}, max {max(nfirms):,}\n")

    rows, monthly = [], []
    for key, vars_ in SPECS.items():
        names = ["a"] + [f"b_{v}" for v in vars_]
        for mode in ("OLS", "WLS"):
            arr = slopes[(key, mode)]
            rec = dict(spec=key, method=mode, n_months=len(arr),
                       avg_n_firms=float(np.mean(nfirms)))
            for j, nm in enumerate(names):
                mu, t, L = nw_mean_tstat(arr[:, j])
                rec[nm], rec[f"{nm}_t"], rec[f"{nm}_L"] = mu, t, L
                monthly.append(pd.DataFrame(dict(
                    yyyymm=months, spec=key, method=mode, coef=nm, value=arr[:, j]
                )))
            rows.append(rec)

    res = pd.DataFrame(rows)
    res.to_csv(OUT_DIR / "q3d_fama_macbeth.csv", index=False)
    pd.concat(monthly, ignore_index=True).to_csv(
        OUT_DIR / "q3d_monthly_slopes.csv", index=False
    )

    pd.set_option("display.width", 250)
    cols = ["spec", "method", "a", "a_t", "b_BM", "b_BM_t", "b_GP", "b_GP_t",
            "b_Dur", "b_Dur_t", "n_months"]
    cols = [c for c in cols if c in res.columns]
    print("=== Fama-MacBeth: mean slopes (decimal return per month) and NW t-stats ===")
    print(res[cols].to_string(index=False, na_rep="",
                              float_format=lambda v: f"{v:9.4f}"))
    print(f"\nwrote {OUT_DIR / 'q3d_fama_macbeth.csv'}")
    print(f"wrote {OUT_DIR / 'q3d_monthly_slopes.csv'}")


if __name__ == "__main__":
    main()
