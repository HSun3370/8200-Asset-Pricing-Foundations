"""
Pset 1, Question 3(b) -- construct the book-to-market signal BM and validate it against
exp(BMdec) from the Chen-Zimmermann (2022) dataset.

Construction (problem statement, footnotes 5-6, plus the student's decisions):

  BE  = SE + TXDITC - BVPS, from the fiscal year ending in calendar year t-1
        SE    = SEQ, else CEQ + PSTK -- footnote 6's sequence. The extract carries SEQ
                                but not AT or LT, so the third route (AT - LT) is still
                                unavailable and a firm-year with neither SEQ nor both of
                                CEQ and PSTK gets no BE.
        TXDITC = txditc if available, else 0
        BVPS   = PSTKRV, else PSTKL, else PSTK
  ME  = |PRC| * SHROUT from CRSP, December of year t-1. SHROUT is in thousands of
        shares and Compustat is in millions of dollars, so ME is divided by 1000 to put
        both in millions before forming the ratio.
  BM  = BE / ME, assigned at the end of June of year t and held fixed from June of
        year t through May of year t+1.

  Screens: firm-months with BE <= 0 are excluded; the firm must already have at least
  two prior annual COMPUSTAT records before the fiscal year used (STUDENT'S DECISION:
  count records, so the fiscal year used is the firm's third or later observation); the
  panel starts in June 1963. The SHRCD/EXCHCD and utility/financial exclusions are
  already baked into CRSP.csv, and the BM panel is intersected with it.

  Working assumptions flagged to the student, easily changed:
    - "fiscal year ending in calendar year t-1" is keyed on the calendar year of
      `datadate` (the literal reading); this differs from Compustat's `fyear` field in
      13.5% of rows.
    - 685 (LPERMNO, datadate-year) pairs map to two GVKEYs; both copies are dropped
      rather than picking one arbitrarily.
    - No currency filter is applied; the CRSP share-code and exchange screens already
      restrict the sample to US-incorporated common stock.

Validation: BM_CZ = BMdec, used directly as a level rather than exponentiated -- see
load_cz_bm() for the evidence and the student's decision. Merge on (permno, yyyymm),
drop missing, then for each month run the cross-firm OLS regression

    BM_CZ_{j,tau} = a_tau + b_tau * BM_{j,tau} + e_{j,tau}

and plot the time series of a_tau, b_tau and R^2_tau.

Prerequisites: q3a_filter_crsp.py and crsp_add_prc_shrout.py (CRSP.csv must carry PRC
and SHROUT), and the CZ cache from q3a.py or q3a_build_cz_cache.py.

Outputs: output/q3b_monthly_regressions.csv and output/q3b_{intercept,slope,r2}.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]
CRSP_CSV = PSET_DIR / "CRSP.csv"
COMP_CSV = PSET_DIR / "COMPUSTATS.csv"
OUT_DIR = PSET_DIR / "output"
CZ_CACHE = PSET_DIR / "data_cache" / "cz_signals.parquet"
OUT_DIR.mkdir(exist_ok=True)

START_YYYYMM = 196306  # BM panel starts June 1963
MIN_PRIOR_RECORDS = 2  # firm needs >= 2 earlier annual COMPUSTAT records


def load_book_equity() -> pd.DataFrame:
    """BE by (permno, fiscal-year-end calendar year), per footnote 6."""
    comp = pd.read_csv(COMP_CSV, parse_dates=["datadate"])
    comp = comp.sort_values(["GVKEY", "datadate"], ignore_index=True)
    print(f"COMPUSTAT rows                 : {len(comp):,}")

    # backfill-bias screen: count earlier annual records for the same Compustat firm
    prior = comp.groupby("GVKEY").cumcount()
    comp = comp.loc[prior >= MIN_PRIOR_RECORDS].copy()
    print(f"  after >={MIN_PRIOR_RECORDS} prior records      : {len(comp):,}")

    # footnote 6: SE = SEQ, else CEQ + PSTK, else AT - LT. The extract carries SEQ but
    # not AT/LT, so the first two routes are used and the third is unavailable.
    se_ceq_pstk = comp["ceq"] + comp["pstk"]
    se = comp["seq"].where(comp["seq"].notna(), se_ceq_pstk)
    n_seq = int(comp["seq"].notna().sum())
    n_fallback = int((comp["seq"].isna() & se_ceq_pstk.notna()).sum())
    n_none = int(se.isna().sum())
    print(f"  SE from SEQ                  : {n_seq:,}")
    print(f"  SE from CEQ+PSTK fallback    : {n_fallback:,}")
    print(f"  SE unavailable (no AT/LT)    : {n_none:,}")

    txditc = comp["txditc"].fillna(0.0)
    bvps = comp["pstkrv"].fillna(comp["pstkl"]).fillna(comp["pstk"])
    comp["BE"] = se + txditc - bvps
    comp["fy_end_year"] = comp["datadate"].dt.year

    comp = comp.dropna(subset=["BE", "LPERMNO"])
    print(f"  with a computable BE         : {len(comp):,}")

    # a handful of permno-years map to two gvkeys; drop rather than choose arbitrarily
    dup = comp.duplicated(subset=["LPERMNO", "fy_end_year"], keep=False)
    if dup.any():
        print(f"  dropped ambiguous permno-years: {int(dup.sum()):,}")
        comp = comp.loc[~dup]

    comp = comp.rename(columns={"LPERMNO": "permno"})
    return comp[["permno", "fy_end_year", "BE"]]


def load_december_me() -> pd.DataFrame:
    """ME in $ millions by (permno, calendar year), from December CRSP rows."""
    crsp = pd.read_csv(
        CRSP_CSV, usecols=["PERMNO", "date", "PRC", "SHROUT"], parse_dates=["date"]
    )
    dec = crsp.loc[crsp["date"].dt.month == 12].copy()
    ok = dec["PRC"].notna() & dec["SHROUT"].notna() & (dec["SHROUT"] != 0)
    dec = dec.loc[ok]
    # |PRC| ($/share) * SHROUT (thousands of shares) = $ thousands -> millions
    dec["ME"] = dec["PRC"].abs() * dec["SHROUT"] / 1000.0
    dec["me_year"] = dec["date"].dt.year
    print(f"December ME observations       : {len(dec):,}")
    return dec.rename(columns={"PERMNO": "permno"})[["permno", "me_year", "ME"]]


def build_bm_panel(be: pd.DataFrame, me: pd.DataFrame) -> pd.DataFrame:
    """BM set in June of year t, held through May of t+1, as a monthly panel."""
    ann = be.merge(
        me, left_on=["permno", "fy_end_year"], right_on=["permno", "me_year"], how="inner"
    )
    print(f"firm-years with BE and ME      : {len(ann):,}")

    ann = ann.loc[ann["BE"] > 0].copy()
    print(f"  after excluding BE <= 0      : {len(ann):,}")

    ann["BM"] = ann["BE"] / ann["ME"]
    ann["june_year"] = ann["fy_end_year"] + 1  # BE/ME from t-1 are used from June of t

    # expand each firm-year to its 12 months: June of t .. May of t+1
    months = np.arange(12)
    rep = ann.loc[ann.index.repeat(12)].copy()
    off = np.tile(months, len(ann))
    mi = rep["june_year"].to_numpy() * 12 + 5 + off      # month index, 0-based month
    rep["yyyymm"] = (mi // 12) * 100 + (mi % 12) + 1
    panel = rep[["permno", "yyyymm", "BM"]]
    panel = panel.loc[panel["yyyymm"] >= START_YYYYMM]
    print(f"BM firm-months                 : {len(panel):,}")
    return panel


def load_cz_bm() -> pd.DataFrame:
    """BM_CZ from the CZ dataset.

    The problem statement describes BMdec as "the log of the book-to-market ratio" and
    asks for BM_CZ = exp(BMdec). That does not hold for this CZ vintage: 2.72% of BMdec
    values are negative (a log book-to-market cannot exist for negative book equity),
    its quartiles 0.36 / 0.68 / 1.17 are ratio-scale, and exp() overflows on the maximum
    of 13,961. Validating against BMdec directly gives mean R^2 0.91 and slope 0.97
    against 0.19 and 3,321 for the exponentiated version. STUDENT'S DECISION: use BMdec
    as the level it evidently is.
    """
    cz = pd.read_parquet(CZ_CACHE)[["permno", "yyyymm", "BMdec"]].dropna()
    cz["BM_CZ"] = cz["BMdec"]
    print(f"CZ BMdec observations          : {len(cz):,}")
    return cz[["permno", "yyyymm", "BM_CZ"]]


def monthly_regressions(d: pd.DataFrame) -> pd.DataFrame:
    """Cross-firm OLS of BM_CZ on BM, month by month (b = Cov/Var, R^2 = Corr^2)."""
    d = d.dropna(subset=["BM", "BM_CZ"])
    d = d.assign(xy=d["BM"] * d["BM_CZ"], xx=d["BM"] ** 2, yy=d["BM_CZ"] ** 2)
    g = d.groupby("yyyymm").agg(
        n=("BM", "size"), sx=("BM", "sum"), sy=("BM_CZ", "sum"),
        sxy=("xy", "sum"), sxx=("xx", "sum"), syy=("yy", "sum"),
    )

    n = g["n"]
    cov = g["sxy"] / n - (g["sx"] / n) * (g["sy"] / n)
    var_x = g["sxx"] / n - (g["sx"] / n) ** 2
    var_y = g["syy"] / n - (g["sy"] / n) ** 2

    res = pd.DataFrame({"n": n, "slope": cov / var_x, "r2": cov**2 / (var_x * var_y)})
    res["intercept"] = g["sy"] / n - res["slope"] * (g["sx"] / n)

    keep = (n >= 3) & (var_x > 0) & (var_y > 0)
    if int((~keep).sum()):
        print(f"  months dropped (n<3 or no variation): {int((~keep).sum())}")

    res = res.loc[keep].reset_index()
    res["date"] = pd.to_datetime(res["yyyymm"].astype(str), format="%Y%m")
    return res[["yyyymm", "date", "n", "intercept", "slope", "r2"]]


def make_figures(res: pd.DataFrame) -> None:
    specs = [
        ("intercept", "Intercept $a_\\tau$", "q3b_intercept.png", 0.0),
        ("slope", "Slope $b_\\tau$", "q3b_slope.png", 1.0),
        ("r2", "$R^2_\\tau$", "q3b_r2.png", 1.0),
    ]
    for stat, ylabel, fname, ref in specs:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.axhline(ref, color="0.6", lw=1, ls="--", zorder=1)
        ax.plot(res["date"], res[stat], lw=0.9, color="tab:green", zorder=2)
        ax.set_xlabel("Month")
        ax.set_ylabel(ylabel)
        ax.set_title(f"Q3(b): cross-firm regression of $BM_{{CZ}}$ on my $BM$ - {ylabel}")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(OUT_DIR / fname, dpi=150)
        plt.close(fig)
        print(f"wrote {OUT_DIR / fname}")


def main() -> None:
    be = load_book_equity()
    me = load_december_me()
    panel = build_bm_panel(be, me)

    # keep only firm-months that survive the CRSP screens already applied to CRSP.csv
    crsp = pd.read_csv(CRSP_CSV, usecols=["PERMNO", "date"], parse_dates=["date"])
    crsp["yyyymm"] = crsp["date"].dt.year * 100 + crsp["date"].dt.month
    keys = crsp.rename(columns={"PERMNO": "permno"})[["permno", "yyyymm"]]
    panel = panel.merge(keys, on=["permno", "yyyymm"], how="inner")
    print(f"  intersected with CRSP screens: {len(panel):,}")

    merged = panel.merge(load_cz_bm(), on=["permno", "yyyymm"], how="inner")
    print(f"merged firm-months             : {len(merged):,}")

    res = monthly_regressions(merged)
    csv_path = OUT_DIR / "q3b_monthly_regressions.csv"
    res.to_csv(csv_path, index=False)
    make_figures(res)

    pd.set_option("display.float_format", lambda x: f"{x:10.4f}")
    print(f"\nmonths with a regression       : {len(res):,}"
          f"  ({res['date'].min():%Y-%m} .. {res['date'].max():%Y-%m})")
    print("\nsummary of the monthly estimates:")
    print(res[["n", "intercept", "slope", "r2"]]
          .describe().loc[["mean", "std", "min", "50%", "max"]])
    print(f"\nwrote {csv_path}")


if __name__ == "__main__":
    main()
