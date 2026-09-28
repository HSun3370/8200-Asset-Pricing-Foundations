"""
Pset 1, Question 3(e) -- portfolio-level panel regressions of excess returns on average
portfolio deciles, following Goncalves (2021b).

Portfolios: decile portfolios on BM_CZ, GP_CZ and Dur, rebalanced annually at June with
NYSE breakpoints, formed both value-weighted and equal-weighted. Formation at June of
year t uses BM and GP from the Chen-Zimmermann data at that month and the Goncalves
duration with FF.YEAR = t, which the author documents as public at the end of June of
year t. Membership and weights are then held over July of t through June of t+1, the
same convention as 3(c).

For each portfolio p, Dec^X_p is the average decile of signal X among the firms in p,
weighted by the weight each firm carries in that portfolio -- market equity for the
value-weighted portfolios and equal for the equal-weighted ones (the student's decision),
so Dec describes the same portfolio whose return is on the left-hand side. Dec is fixed
at the June formation month and held across the twelve holding months (also the student's
decision), matching how membership and weights are held.

A specification containing k signals is estimated on the union of those signals' decile
portfolios, so 10 portfolios for a univariate spec, 20 for a bivariate one and 30 for
specification (vii) -- the generalisation of the "20 portfolios" example in footnote 10.

    (i)   xR ~ Dec_BM                     (10 portfolios)
    (ii)  xR ~ Dec_GP                     (10)
    (iii) xR ~ Dec_Dur                    (10)
    (iv)  xR ~ Dec_BM + Dec_GP            (20)
    (v)   xR ~ Dec_Dur + Dec_BM           (20)
    (vi)  xR ~ Dec_Dur + Dec_GP           (20)
    (vii) xR ~ Dec_Dur + Dec_BM + Dec_GP  (30)

Estimation is pooled OLS with Driscoll and Kraay (1998) standard errors, via
linearmodels' PooledOLS. All specifications run on the common sample of firms for which
BM, GP and Dur are all available (the student's decision), as in 3(d). Excess returns are
CRSP returns less the Ken French RF; a firm with no usable return in a month is dropped
from its portfolio for that month and the remaining weights renormalise, as in 3(c).

Prerequisites: q3a_filter_crsp.py and crsp_add_prc_shrout.py, the CZ cache, the Ken
French RF cache written by q3c.py, and FirmLevel Dur.csv.

Outputs: output/q3e_panel.csv and output/q3e_portfolio_panel.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PooledOLS

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
CZ_CACHE = PSET_DIR / "data_cache" / "cz_signals.parquet"
RF_CACHE = PSET_DIR / "data_cache" / "ff_rf.parquet"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

DUR_CANDIDATES = [
    PSET_DIR / "FirmLevel Dur.csv",
    PSET_DIR / "data_cache" / "FirmLevel_Dur.csv",
]

SIGNALS = ["BM", "GP", "Dur"]
SPECS = {
    "(i)": ["BM"],
    "(ii)": ["GP"],
    "(iii)": ["Dur"],
    "(iv)": ["BM", "GP"],
    "(v)": ["Dur", "BM"],
    "(vi)": ["Dur", "GP"],
    "(vii)": ["Dur", "BM", "GP"],
}


def dur_path() -> Path:
    for p in DUR_CANDIDATES:
        if p.exists():
            return p
    raise SystemExit("FirmLevel Dur.csv not found; see q3d.py for the download source.")


def mi_to_yyyymm(mi: np.ndarray) -> np.ndarray:
    m0 = mi - 1
    return (m0 // 12) * 100 + (m0 % 12) + 1


def load_inputs():
    crsp = pd.read_csv(CRSP_CSV, dtype={"RET": str, "SICCD": str}, parse_dates=["date"])
    crsp["mi"] = crsp["date"].dt.year * 12 + crsp["date"].dt.month
    crsp["yyyymm"] = crsp["date"].dt.year * 100 + crsp["date"].dt.month
    crsp["ret"] = pd.to_numeric(crsp["RET"], errors="coerce")
    me = crsp["PRC"].abs() * crsp["SHROUT"]
    crsp["me"] = me.where(me > 0)
    crsp = crsp.rename(columns={"PERMNO": "permno", "EXCHCD": "exchcd"})
    print(f"CRSP rows                    : {len(crsp):,}")

    cz = pd.read_parquet(CZ_CACHE)[["permno", "yyyymm", "BMdec", "GP"]]
    cz = cz.rename(columns={"BMdec": "BM"})

    dur = pd.read_csv(dur_path()).rename(
        columns={"PERMNO": "permno", "FF.YEAR": "ff_year"}
    )
    print(f"Dur firm-years               : {len(dur):,}")

    # formation rows: June of each year t
    june = crsp.loc[crsp["date"].dt.month == 6,
                    ["permno", "yyyymm", "mi", "exchcd", "me"]].copy()
    june["ff_year"] = june["yyyymm"] // 100
    form = (
        june.merge(cz, on=["permno", "yyyymm"], how="inner")
            .merge(dur, on=["permno", "ff_year"], how="inner")
            .dropna(subset=SIGNALS + ["me"])
    )
    print(f"June formation firm-years    : {len(form):,}  "
          f"({form.yyyymm.min()} .. {form.yyyymm.max()})")

    rf = pd.read_parquet(RF_CACHE)
    rets = crsp.loc[crsp["ret"].notna(), ["permno", "mi", "yyyymm", "ret"]].merge(
        rf, on="yyyymm", how="inner"
    )
    rets["xret"] = rets["ret"] - rets["rf"]
    return form, rets[["permno", "mi", "xret"]]


def assign_deciles(f: pd.DataFrame, col: str) -> np.ndarray:
    """NYSE-breakpoint deciles 1..10 within each formation month."""
    base = f.loc[f["exchcd"] == 1]
    qs = np.arange(1, 10) / 10.0
    bp = base.groupby("mi")[col].quantile(qs).unstack()
    aligned = f[["mi"]].merge(bp, left_on="mi", right_index=True, how="left")
    B = aligned[bp.columns].to_numpy(dtype=float)
    v = f[col].to_numpy(dtype=float)[:, None]
    dec = 1.0 + (v > B).sum(axis=1)
    return np.where(~np.isnan(B).any(axis=1), dec, np.nan)


def build_portfolios(form: pd.DataFrame, rets: pd.DataFrame, weighting: str) -> pd.DataFrame:
    """One row per (portfolio, holding month): its excess return and its Dec^X values."""
    f = form.copy()
    f["w"] = f["me"] if weighting == "vw" else 1.0
    for X in SIGNALS:
        f[f"wd_{X}"] = f["w"] * f[f"dec_{X}"]

    frames = []
    for S in SIGNALS:
        key = ["mi", f"dec_{S}"]
        agg = f.groupby(key).agg(
            W=("w", "sum"), **{f"s_{X}": (f"wd_{X}", "sum") for X in SIGNALS}
        )
        for X in SIGNALS:
            agg[f"Dec_{X}"] = agg[f"s_{X}"] / agg["W"]
        agg = agg[[f"Dec_{X}" for X in SIGNALS]].reset_index()
        agg = agg.rename(columns={"mi": "form_mi", f"dec_{S}": "decile"})

        # hold membership and weights over the twelve months after formation
        cols = ["permno", "mi", f"dec_{S}", "w"]
        rep = f.loc[f.index.repeat(12), cols].copy()
        rep = rep.rename(columns={"mi": "form_mi", f"dec_{S}": "decile"})
        rep["mi"] = rep["form_mi"].to_numpy() + np.tile(np.arange(1, 13), len(f))

        held = rep.merge(rets, on=["permno", "mi"], how="inner")
        held["wx"] = held["w"] * held["xret"]
        g = held.groupby(["form_mi", "decile", "mi"]).agg(
            num=("wx", "sum"), den=("w", "sum")
        )
        port = (g["num"] / g["den"]).rename("xret").reset_index()

        port = port.merge(agg, on=["form_mi", "decile"], how="inner")
        port["signal"] = S
        port["portfolio"] = S + port["decile"].astype(int).astype(str).str.zfill(2)
        frames.append(port)

    out = pd.concat(frames, ignore_index=True)
    out["yyyymm"] = mi_to_yyyymm(out["mi"].to_numpy())
    return out


def run_specs(panel: pd.DataFrame, weighting: str) -> list:
    rows = []
    for key, vars_ in SPECS.items():
        sub = panel.loc[panel["signal"].isin(vars_)].copy()
        d = sub.set_index(["portfolio", "yyyymm"])
        y = d["xret"]
        X = d[[f"Dec_{v}" for v in vars_]].copy()
        X.insert(0, "const", 1.0)

        res = PooledOLS(y, X).fit(cov_type="driscoll-kraay")
        rec = dict(spec=key, weighting=weighting.upper(),
                   n_portfolios=sub["portfolio"].nunique(),
                   n_months=sub["yyyymm"].nunique(), n_obs=int(res.nobs))
        rec["a"] = float(res.params["const"])
        rec["a_t"] = float(res.tstats["const"])
        for v in vars_:
            rec[f"b_{v}"] = float(res.params[f"Dec_{v}"])
            rec[f"b_{v}_t"] = float(res.tstats[f"Dec_{v}"])
        rows.append(rec)
        print(f"  {weighting.upper():<3} {key:<6} n_port={rec['n_portfolios']:<3} "
              f"obs={rec['n_obs']:,}")
    return rows


def main() -> None:
    form, rets = load_inputs()
    for X in SIGNALS:
        form[f"dec_{X}"] = assign_deciles(form, X)
    form = form.dropna(subset=[f"dec_{X}" for X in SIGNALS])
    print(f"formation rows with deciles  : {len(form):,}\n")

    rows, panels = [], []
    for weighting in ("vw", "ew"):
        panel = build_portfolios(form, rets, weighting)
        panel["weighting"] = weighting.upper()
        panels.append(panel)
        print(f"{weighting.upper()} portfolio-months          : {len(panel):,}")
        rows += run_specs(panel, weighting)

    res = pd.DataFrame(rows)
    res.to_csv(OUT_DIR / "q3e_panel.csv", index=False)
    pd.concat(panels, ignore_index=True).to_csv(
        OUT_DIR / "q3e_portfolio_panel.csv", index=False
    )

    pd.set_option("display.width", 250)
    cols = ["spec", "weighting", "a", "a_t", "b_BM", "b_BM_t", "b_GP", "b_GP_t",
            "b_Dur", "b_Dur_t", "n_portfolios", "n_months"]
    cols = [c for c in cols if c in res.columns]
    print("\n=== Q3(e): pooled OLS, Driscoll-Kraay t-stats "
          "(decimal return per month per decile) ===")
    print(res[cols].to_string(index=False, na_rep="",
                              float_format=lambda v: f"{v:9.4f}"))
    print(f"\nwrote {OUT_DIR / 'q3e_panel.csv'}")
    print(f"wrote {OUT_DIR / 'q3e_portfolio_panel.csv'}")


if __name__ == "__main__":
    main()
