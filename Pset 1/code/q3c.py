"""
Pset 1, Question 3(c) -- decile portfolios on the three Chen-Zimmermann signals.

Signals (CZ versions only, per footnote 7): BM_CZ = BMdec, MOM_CZ = Mom12m, GP_CZ = GP.
Returns come from CRSP; the risk-free benchmark is RF from the Ken French 3-factor file
(footnote 8).

Five schemes, each applied to all three signals:
    (i)   value-weighted,  rebalanced annually at June, NYSE breakpoints
    (ii)  equal-weighted,  rebalanced annually at June, NYSE breakpoints
    (iii) value-weighted,  rebalanced monthly,          NYSE breakpoints
    (iv)  value-weighted,  rebalanced annually at June, general breakpoints
    (v)   equal-weighted,  rebalanced monthly,          general breakpoints

Student's decisions on the points the problem leaves open:
  * Annual schemes form deciles on the signal at the end of June of year t and hold the
    portfolio over July of t through June of t+1 (the Fama-French convention).
  * Value weights use market equity at the formation date and are held fixed over the
    holding period -- June of t for annual schemes, month tau for monthly schemes.
  * A stock whose CRSP return that month is blank or letter-coded is dropped from its
    decile for that month; the remaining weights renormalise (the weighted mean divides
    by the weight of the stocks that actually have returns).
  * All three signals share a common sample starting June 1963, so the scatterplot
    series and the 15 HML averages cover the same window.

Breakpoints are the deciles of the signal among the firms used for breakpoints in that
formation month: NYSE-listed firms only (EXCHCD == 1) for the NYSE schemes, every firm
in the sample for the general schemes. All firms are then assigned to a decile using
those cut-offs.

HML is decile 10 minus decile 1. Its t-statistic uses the Newey-West (1987, 1994)
estimator with the data-driven bandwidth, implemented exactly as in q2b.py so the two
questions report comparable statistics.

Prerequisites: q3a_filter_crsp.py and crsp_add_prc_shrout.py (CRSP.csv must carry PRC
and SHROUT), plus the CZ cache from q3a.py or q3a_build_cz_cache.py.

Outputs: output/q3c_hml.csv, output/q3c_decile_means.csv and
         output/q3c_scheme_{i,ii,iii,iv,v}.png
"""

import io
import urllib.request
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
CZ_CACHE = PSET_DIR / "data_cache" / "cz_signals.parquet"
RF_CACHE = PSET_DIR / "data_cache" / "ff_rf.parquet"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

FF_URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
          "F-F_Research_Data_Factors_CSV.zip")
START_YYYYMM = 196306

SIGNALS = {"BM_CZ": "BMdec", "MOM_CZ": "Mom12m", "GP_CZ": "GP"}
COLORS = {"BM_CZ": "tab:blue", "MOM_CZ": "tab:red", "GP_CZ": "tab:green"}
SCHEMES = {
    "i": dict(label="VW, annual (June), NYSE breakpoints", w="vw", rebal="annual", bp="nyse"),
    "ii": dict(label="EW, annual (June), NYSE breakpoints", w="ew", rebal="annual", bp="nyse"),
    "iii": dict(label="VW, monthly, NYSE breakpoints", w="vw", rebal="monthly", bp="nyse"),
    "iv": dict(label="VW, annual (June), general breakpoints", w="vw", rebal="annual", bp="general"),
    "v": dict(label="EW, monthly, general breakpoints", w="ew", rebal="monthly", bp="general"),
}


# --------------------------------------------------------------------------- data


def load_crsp() -> pd.DataFrame:
    df = pd.read_csv(
        CRSP_CSV, dtype={"RET": str, "SICCD": str}, parse_dates=["date"]
    )
    df["yyyymm"] = df["date"].dt.year * 100 + df["date"].dt.month
    df["mi"] = df["date"].dt.year * 12 + df["date"].dt.month
    df["ret"] = pd.to_numeric(df["RET"], errors="coerce")
    me = df["PRC"].abs() * df["SHROUT"]
    df["me"] = me.where(me > 0)
    out = df.rename(columns={"PERMNO": "permno", "EXCHCD": "exchcd"})
    print(f"CRSP rows                  : {len(out):,}")
    return out[["permno", "yyyymm", "mi", "exchcd", "ret", "me"]]


def load_rf() -> pd.DataFrame:
    """Monthly risk-free rate (decimal) from the Ken French 3-factor file."""
    if RF_CACHE.exists():
        rf = pd.read_parquet(RF_CACHE)
        print(f"RF months (cached)         : {len(rf):,}")
        return rf

    with urllib.request.urlopen(FF_URL, timeout=60) as resp:
        blob = resp.read()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        raw = z.read(z.namelist()[0]).decode("latin-1")

    rows = []
    for line in raw.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 5 and parts[0].isdigit() and len(parts[0]) == 6:
            rows.append((int(parts[0]), float(parts[4])))
    rf = pd.DataFrame(rows, columns=["yyyymm", "rf"])
    rf["rf"] = rf["rf"] / 100.0  # the file is in percent
    rf.to_parquet(RF_CACHE, index=False)
    print(f"RF months (downloaded)     : {len(rf):,}  "
          f"({rf.yyyymm.min()} .. {rf.yyyymm.max()})")
    return rf


def load_signals() -> pd.DataFrame:
    cz = pd.read_parquet(CZ_CACHE)
    print(f"CZ signal rows             : {len(cz):,}")
    return cz[["permno", "yyyymm"] + list(SIGNALS.values())]


# ---------------------------------------------------------------- portfolio build


def assign_deciles(f: pd.DataFrame, col: str, nyse_only: bool) -> np.ndarray:
    """Decile 1..10 from breakpoints computed within each formation month."""
    base = f.loc[f["exchcd"] == 1] if nyse_only else f
    qs = np.arange(1, 10) / 10.0
    bp = base.groupby("yyyymm")[col].quantile(qs).unstack()
    aligned = f[["yyyymm"]].merge(bp, left_on="yyyymm", right_index=True, how="left")
    B = aligned[bp.columns].to_numpy(dtype=float)
    v = f[col].to_numpy(dtype=float)[:, None]
    dec = 1.0 + (v > B).sum(axis=1)
    usable = ~np.isnan(B).any(axis=1)
    return np.where(usable, dec, np.nan)


def portfolio_returns(
    form: pd.DataFrame, rets: pd.DataFrame, rf: pd.DataFrame, scheme: dict
) -> pd.DataFrame:
    """Monthly excess return of each decile, given a formation table."""
    hold = np.arange(1, 13) if scheme["rebal"] == "annual" else np.arange(1, 2)

    rep = form.loc[form.index.repeat(len(hold)), ["permno", "mi", "decile", "me"]].copy()
    rep["mi"] = rep["mi"].to_numpy() + np.tile(hold, len(form))

    held = rep.merge(rets, on=["permno", "mi"], how="inner")
    held["w"] = held["me"] if scheme["w"] == "vw" else 1.0
    held["wr"] = held["w"] * held["ret"]

    g = held.groupby(["mi", "decile"]).agg(num=("wr", "sum"), den=("w", "sum"))
    port = (g["num"] / g["den"]).rename("ret").reset_index()
    # mi = year*12 + month with month in 1..12, so shift to a 0-based index first
    m0 = port["mi"] - 1
    port["yyyymm"] = (m0 // 12) * 100 + (m0 % 12) + 1

    port = port.merge(rf, on="yyyymm", how="inner")
    port["xret"] = port["ret"] - port["rf"]
    return port.loc[port["yyyymm"] >= START_YYYYMM, ["yyyymm", "decile", "xret"]]


# ------------------------------------------------------------------ Newey-West


def omega(h: np.ndarray, lag: int) -> np.ndarray:
    T = h.shape[0]
    if lag == 0:
        return h.T @ h / T
    return h[lag:].T @ h[:-lag] / (T - lag)


def nw_mean_tstat(x: np.ndarray) -> tuple[float, float, int]:
    """Mean of x with a Newey-West (1987, 1994) t-statistic, as in q2b.py."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    T = len(x)
    mu = x.mean()
    h = (x - mu)[:, None]                      # x_t = 1, so h_t = e_t
    L = int(kernel_optimal_bandwidth(h, kernel="bartlett"))
    S = omega(h, 0)
    for lag in range(1, L + 1):
        om = omega(h, lag)
        S = S + (1.0 - lag / (L + 1)) * (om + om.T)
    se = float(np.sqrt(S[0, 0] / T))           # Q = 1 for a constant-only regression
    return mu, mu / se, L


# ----------------------------------------------------------------------- outputs


def scatterplots(means: pd.DataFrame) -> None:
    for key, sch in SCHEMES.items():
        fig, ax = plt.subplots(figsize=(7.5, 5))
        for sig in SIGNALS:
            d = means[(means["scheme"] == key) & (means["signal"] == sig)]
            ax.scatter(d["decile"], d["mean_xret_pct"], color=COLORS[sig],
                       s=45, label=sig, zorder=3)
        ax.axhline(0, color="0.6", lw=0.8, zorder=1)
        ax.set_xticks(range(1, 11))
        ax.set_xlabel("Decile")
        ax.set_ylabel("Average excess return (% per month)")
        ax.set_title(f"Q3(c) scheme ({key}): {sch['label']}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        path = OUT_DIR / f"q3c_scheme_{key}.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"wrote {path}")


def main() -> None:
    crsp = load_crsp()
    rf = load_rf()
    cz = load_signals()

    rets = crsp.loc[crsp["ret"].notna(), ["permno", "mi", "ret"]]
    base = crsp.merge(cz, on=["permno", "yyyymm"], how="inner")
    print(f"CRSP x CZ firm-months      : {len(base):,}\n")

    mean_rows, hml_rows = [], []
    for key, sch in SCHEMES.items():
        for sig, col in SIGNALS.items():
            form = base.loc[base[col].notna() & base["me"].notna()].copy()
            if sch["rebal"] == "annual":
                form = form.loc[form["yyyymm"] % 100 == 6]
            form["decile"] = assign_deciles(form, col, sch["bp"] == "nyse")
            form = form.dropna(subset=["decile"])
            form["decile"] = form["decile"].astype(int)

            port = portfolio_returns(form, rets, rf, sch)
            wide = port.pivot(index="yyyymm", columns="decile", values="xret")

            for d in range(1, 11):
                if d in wide.columns:
                    mean_rows.append(dict(
                        scheme=key, signal=sig, decile=d,
                        mean_xret_pct=wide[d].mean() * 100, n_months=int(wide[d].notna().sum()),
                    ))

            hml = (wide[10] - wide[1]).dropna()
            mu, t, L = nw_mean_tstat(hml.to_numpy())
            hml_rows.append(dict(
                scheme=key, scheme_label=sch["label"], signal=sig,
                hml_pct=mu * 100, tstat=t, nw_lag=L, n_months=len(hml),
                first=int(hml.index.min()), last=int(hml.index.max()),
            ))
            print(f"  {key:<4} {sig:<7} HML {mu*100:7.3f}%/mo  t={t:6.2f}  "
                  f"L={L:<3} n={len(hml):,}")

    means = pd.DataFrame(mean_rows)
    hmls = pd.DataFrame(hml_rows)
    means.to_csv(OUT_DIR / "q3c_decile_means.csv", index=False)
    hmls.to_csv(OUT_DIR / "q3c_hml.csv", index=False)
    print()
    scatterplots(means)

    print("\n=== HML (decile 10 - decile 1), % per month, NW(1987,1994) t-stats ===")
    pd.set_option("display.width", 200)
    print(hmls[["scheme", "signal", "hml_pct", "tstat", "nw_lag", "n_months"]]
          .to_string(index=False, float_format=lambda v: f"{v:8.3f}"))
    print(f"\nwrote {OUT_DIR / 'q3c_hml.csv'}")
    print(f"wrote {OUT_DIR / 'q3c_decile_means.csv'}")


if __name__ == "__main__":
    main()
