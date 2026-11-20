"""
Pset 3, Question 1(e) -- principal components of the 25 Size/BM portfolios and their
regressions on the Fama-French factors.

Student specification (as given, 2026-11-20):
  Data: monthly returns, July 1926 to the latest month, on the "25 Portfolios Formed on Size
  and Book-to-Market (5 x 5)" and the risk-free proxy RF from "Fama/French 3 Factors"
  (Ken French data library); downloaded into Pset 3/Data/ on 2026-11-20 from
    https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip
    https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip
  (both files built from the 202609 CRSP database; the extracted CSVs are kept in the repo).
  (i)   PCA on the excess monthly returns of the 25 portfolios; take the first three PCs;
        normalize each PC by sigma_Mkt / sigma_PC, sigma_Mkt = volatility of Mkt-RF.
  (ii)  Regress each PC on Mkt-RF; report alpha, beta, R^2_adj with Newey-West (1987, 1994)
        t-stats.
  (iii) Regress each PC on Mkt-RF, HML and SMB; report the same.

Decisions made by the student when AI flagged them (2026-11-20):
  * Returns: the "Average Value Weighted Returns -- Monthly" block of 25_Portfolios_5x5.csv.
  * Units: percent per month, as in the French files; xR = R - RF (percent).
  * PCA on the sample covariance matrix of the 25 excess returns.
  * PC series = portfolio of the raw (not demeaned) excess returns, PC_k,t = w_k' xR_t, with
    w_k the k-th eigenvector (unit length, eigenvalues sorted from largest), then multiplied
    by sigma_Mkt / sigma_PC_k.
  * Eigenvector signs are left as returned by numpy.linalg.eigh (arbitrary; another linear-
    algebra library could flip a PC's sign, which flips the signs of its alpha and betas).
  * Sample: every month in both files, 1926:07 to 2026:09 (the files are built from the
    202609 CRSP database).

Newey-West (carried over from the student's Pset 1 / Pset 2 regressions): Bartlett weights
1 - l/(L+1), Om_l = 1/(T-l) sum_t h_t h_{t-l}' with h_t = x_t e_t; aVar = (1/T) Q^-1 S Q^-1;
lag L from the Newey-West (1994) rule (linearmodels.kernel_optimal_bandwidth) applied, as in
linearmodels' OLS kernel covariance, to the sum of the non-constant regressors' scores (with
one regressor this is that regressor's score, the Pset 1/Pset 2 convention).
R^2_adj = 1 - (1 - R^2)(T - 1)/(T - k - 1), k = number of non-constant regressors.

Outputs (paths relative to "Pset 3"): output/q1e_regressions.csv, output/q1e_pca.csv
(loadings and variance shares), output/q1e_pc_series.csv, output/q1e_table_mkt.md,
output/q1e_table_ff3.md
"""

import io
from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 3
DATA = PSET_DIR / "Data"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

PORT_CSV = DATA / "25_Portfolios_5x5.csv"
FF_CSV = DATA / "F-F_Research_Data_Factors.csv"
VW_BLOCK = "Average Value Weighted Returns -- Monthly"
N_PC = 3


def read_french_block(path: Path, title: str) -> pd.DataFrame:
    """One monthly block of a Ken French CSV: the header row follows `title` (or is the
    first row starting with ','); the block ends at the first blank line."""
    lines = Path(path).read_text().splitlines()
    if title:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == title) + 1
    else:
        start = next(i for i, ln in enumerate(lines) if ln.startswith(","))
    end = next(i for i in range(start + 1, len(lines)) if not lines[i].strip())
    df = pd.read_csv(io.StringIO("\n".join(lines[start:end])), index_col=0)
    df.columns = [c.strip() for c in df.columns]
    df.index = pd.PeriodIndex(df.index.astype(str).str.strip(), freq="M")
    return df


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    port = read_french_block(PORT_CSV, VW_BLOCK)
    ff = read_french_block(FF_CSV, "")
    assert port.index.equals(ff.index), "portfolio and factor months differ"
    full = pd.period_range(port.index[0], port.index[-1], freq="M")
    assert port.index.equals(full), "monthly index has gaps"
    assert (port > -99.99).all().all() and (ff > -99.99).all().all(), "missing-value code"
    xr = port.sub(ff["RF"], axis=0)                     # percent per month
    return xr, ff


def pca(xr: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Eigenvalues (descending) and eigenvectors (columns) of the sample covariance."""
    evals, evecs = np.linalg.eigh(np.cov(xr.to_numpy(), rowvar=False))
    order = np.argsort(evals)[::-1]
    return evals[order], evecs[:, order]


def newey_west_s(h: np.ndarray, L: int) -> np.ndarray:
    T = h.shape[0]
    S = h.T @ h / T
    for lag in range(1, L + 1):
        om = h[lag:].T @ h[:-lag] / (T - lag)
        S = S + (1.0 - lag / (L + 1.0)) * (om + om.T)
    return S


def ols_nw(y: np.ndarray, X: np.ndarray) -> dict:
    """OLS of y on [1, X] with Newey-West standard errors and automatic lag."""
    T = len(y)
    x = np.column_stack([np.ones(T), X])
    coef, *_ = np.linalg.lstsq(x, y, rcond=None)
    e = y - x @ coef
    h = x * e[:, None]
    L = int(kernel_optimal_bandwidth(h[:, 1:].sum(axis=1), kernel="bartlett"))
    Qinv = np.linalg.inv(x.T @ x / T)
    se = np.sqrt(np.diag(Qinv @ newey_west_s(h, L) @ Qinv / T))
    k = x.shape[1] - 1
    r2 = 1.0 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return dict(coef=coef, se=se, t=coef / se, r2=r2,
                r2_adj=1.0 - (1.0 - r2) * (T - 1) / (T - k - 1), L=L, T=T)


def table_md(rows: list, regressors: list, note: str) -> str:
    head = "| PC | $\\alpha$ | t | " + " | ".join(
        f"$\\beta_{{{r}}}$ | t" for r in regressors) + " | $R^2_{adj}$ |"
    sep = "|---|" + "---:|" * (2 + 2 * len(regressors) + 1)
    body = []
    for r in rows:
        cells = [f"{r['coef'][0]:.4f}", f"{r['t'][0]:.2f}"]
        for j in range(1, len(regressors) + 1):
            cells += [f"{r['coef'][j]:.4f}", f"{r['t'][j]:.2f}"]
        body.append(f"| {r['name']} | " + " | ".join(cells) + f" | {r['r2_adj']:.4f} |")
    return "\n".join([head, sep, *body]) + "\n\n" + note + "\n"


def main() -> None:
    xr, ff = load_data()
    T = len(xr)
    evals, evecs = pca(xr)
    W = evecs[:, :N_PC]                                       # 25 x 3, unit-length columns
    raw = xr.to_numpy() @ W                                   # portfolios of raw excess returns
    sigma_mkt = ff["Mkt-RF"].std(ddof=1)
    scale = sigma_mkt / raw.std(axis=0, ddof=1)
    pcs = pd.DataFrame(raw * scale, index=xr.index, columns=[f"PC{k + 1}" for k in range(N_PC)])

    share = evals / evals.sum()
    pd.DataFrame(W, index=xr.columns, columns=pcs.columns).to_csv(OUT_DIR / "q1e_pca.csv")
    with open(OUT_DIR / "q1e_pca.csv", "a", encoding="utf-8") as f:
        f.write("eigenvalue," + ",".join(f"{v:.6f}" for v in evals[:N_PC]) + "\n")
        f.write("variance_share," + ",".join(f"{v:.6f}" for v in share[:N_PC]) + "\n")
        f.write("scale_sigmaMkt_over_sigmaPC," + ",".join(f"{v:.6f}" for v in scale) + "\n")
    out_series = pcs.copy()
    out_series.index = out_series.index.astype(str)
    out_series.rename_axis("month").to_csv(OUT_DIR / "q1e_pc_series.csv")

    specs = {"mkt": ["Mkt-RF"], "ff3": ["Mkt-RF", "HML", "SMB"]}
    results, csv_rows = {}, []
    for key, regs in specs.items():
        X = ff[regs].to_numpy()
        results[key] = []
        for pc in pcs.columns:
            r = ols_nw(pcs[pc].to_numpy(), X)
            r["name"] = pc
            results[key].append(r)
            row = {"spec": key, "pc": pc, "alpha": r["coef"][0], "t_alpha": r["t"][0],
                   "R2_adj": r["r2_adj"], "NW_lag": r["L"], "T": r["T"]}
            for j, reg in enumerate(regs, start=1):
                row[f"beta_{reg}"] = r["coef"][j]
                row[f"t_beta_{reg}"] = r["t"][j]
            csv_rows.append(row)
    pd.DataFrame(csv_rows).to_csv(OUT_DIR / "q1e_regressions.csv", index=False)

    sample = f"{xr.index[0].strftime('%Y:%m')}–{xr.index[-1].strftime('%Y:%m')} (T = {T})"
    common = (f"PCs: first three principal components of the covariance matrix of the 25 "
              f"value-weighted Size/BM portfolio excess returns, each formed as $w_k' xR_t$ and "
              f"scaled to the volatility of Mkt-RF. Monthly, {sample}; returns in percent per "
              f"month. t-stats use Newey-West (1987, 1994) standard errors with the automatic lag")
    lags = lambda key: ", ".join(f"{r['name']}: {r['L']}" for r in results[key])
    (OUT_DIR / "q1e_table_mkt.md").write_text(
        table_md(results["mkt"], ["Mkt"], f"Regression of each PC on Mkt-RF. {common} ({lags('mkt')})."),
        encoding="utf-8")
    (OUT_DIR / "q1e_table_ff3.md").write_text(
        table_md(results["ff3"], ["Mkt", "HML", "SMB"],
                 f"Regression of each PC on Mkt-RF, HML and SMB. {common} ({lags('ff3')})."),
        encoding="utf-8")

    pd.set_option("display.width", 160)
    print(f"Sample {xr.index[0]} to {xr.index[-1]}, T = {T}; sigma_Mkt = {sigma_mkt:.4f}")
    print("variance share of PC1-3:", np.round(share[:N_PC], 4), " cumulative:", round(share[:N_PC].sum(), 4))
    print("scale factors:", np.round(scale, 4), "; weight sums:", np.round(W.sum(axis=0), 4))
    print(pd.DataFrame(csv_rows).to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
