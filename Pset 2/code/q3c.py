"""
Pset 2, Question 3(c) -- GMM estimate of gamma from two unconditional moments, with an
identity weighting matrix:
    E[R_w,t^(-gamma) xR_w,t]           = 0
    E[R_w,t^(-gamma) z_{t-1} xR_w,t]   = 0
z_t = E^OS_t[xR_e] / sigma^2_e is the trading instrument of a managed portfolio.

Student specification (as given, 2026-10-04):
  * R_w,t = R_e,t = exp(re_t), xR_w,t = exp(re_t) - exp(rf_t) (as in Q3(b)).
  * z_t = E^OS_t[xR_e] / sigma^2_e; sigma^2_e = unconditional variance of R_e,t over the
    sample; E^OS_t[xR_e] = a + b D_t/P_t with D_t/P_t = exp(dp), a = average G - 1,
    b = average G, G = exp(dg).
  * Identity weighting matrix. Table: gamma with standard error; value and t-stat of the
    pricing error of each moment; p-value of the chi^2 test that the pricing errors are
    jointly zero. S by Newey-West (1987, 1994).

Decisions made by the student when AI flagged them (2026-10-04):
  * E^OS_t[xR_e] is the out-of-sample forecast of Pset 1 Q2(e): "average G" is the
    expanding-window mean of exp(dg) over months 1927:12 .. origin-1, and
    E^OS = (G_t - 1) + G_t * (D/P)_t at the forecast origin t. z_{t-1} paired with
    xR_w,t is the forecast made 12 months earlier (Pset 1's one-year timing). The first
    forecast targets 1940:12, so the sample is 1940:12 to 2021:12. The forecast is
    rebuilt here and checked against Pset 1/output/q2e_forecasts.csv when that file exists.
  * sigma^2_e: variance of R_e,t over the GMM estimation sample, divisor T.
  * S: centered, i.e. built from g_t(gamma_hat) - g_bar(gamma_hat).
  * (3(d)) S for inference is re-estimated at the second-step estimate.
  * (3(e)) 12-month compounded nominal BM/MOM excess returns; 22 moments.

Implementation (applies to 3(c)-(e); standard GMM formulas, Hansen 1982 / Cochrane ch. 11):
  * g_t(gamma) = R_w,t^(-gamma) X_t with X_t the K payoffs; d = dg_bar/dgamma
    = E_T[-ln(R_w) R_w^(-gamma) X_t].
  * gamma_hat = argmin g_bar' W g_bar: grid scan over [-50, 50] (step 0.01), then a
    bounded scalar minimisation around the best grid point (must be interior).
  * With a = d'W:  Var(gamma_hat) = (1/T) (a d)^-1 a S a' (a d)^-1,
                   Var(g_bar)     = (1/T) (I - d (a d)^-1 a) S (I - d (a d)^-1 a)'.
    Pricing-error t-stats use the diagonal of Var(g_bar). The chi^2 statistic is
    g_bar' Var(g_bar)^+ g_bar with K - 1 degrees of freedom; Var(g_bar) has rank K - 1,
    so the pseudo-inverse keeps its K - 1 largest eigenvalues.
  * Newey-West S as in Q2 (code/q2a.py): Bartlett weights 1 - l/(L+1),
    Om_l = 1/(T-l) sum g_t g_{t-l}', on the centered g_t; lag L from the Newey-West
    (1994) rule applied, as in Q2, to the sum of the standardized moment series.

Outputs (paths relative to "Pset 2"): output/q3c_gmm.csv, output/q3c_gmm_table.md
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import chi2

from q2a import OUT_DIR, PSET_DIR, newey_west_s, nw1994_lag

EQ_CSV = PSET_DIR / "Data" / "EQ Dataset.csv"
PSET1_FORECASTS = PSET_DIR.parent / "Pset 1" / "output" / "q2e_forecasts.csv"
H = 12                                           # one year = 12 monthly rows
FIRST_TARGET = pd.Period("1940-12", freq="M")    # first Pset 1 Q2(e) forecast target
GAMMA_GRID = np.linspace(-50.0, 50.0, 10001)


def load_eq() -> pd.DataFrame:
    df = pd.read_csv(EQ_CSV)
    df.index = pd.PeriodIndex(
        pd.to_datetime(dict(year=df["YEAR"], month=df["MONTH"], day=1)), freq="M"
    )
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly index has gaps"
    assert df.notna().all().all(), "missing values in EQ dataset"
    df["Rw"] = np.exp(df["re"])
    df["xRw"] = np.exp(df["re"]) - np.exp(df["rf"])
    return df


def os_forecast(df: pd.DataFrame) -> pd.Series:
    """Pset 1 Q2(e) E^OS, indexed by target month t+1 (= forecast origin + 12 months)."""
    g = np.exp(df["dg"]).to_numpy()
    dp = np.exp(df["dp"]).to_numpy()
    out = {}
    for j in range(df.index.get_loc(FIRST_TARGET), len(df)):
        s0 = j - H                                # row of the forecast origin
        G = g[:s0].mean()                         # months 1927:12 .. origin - 1
        out[df.index[j]] = (G - 1.0) + G * dp[s0]
    e_os = pd.Series(out, name="E_OS")
    if PSET1_FORECASTS.exists():
        p1 = pd.read_csv(PSET1_FORECASTS, index_col="target")["E_OS"]
        p1.index = pd.PeriodIndex(p1.index, freq="M")
        assert p1.index.equals(e_os.index) and np.allclose(p1.to_numpy(), e_os.to_numpy(),
                                                           rtol=0, atol=1e-12)
    return e_os


def managed_moments(df: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame, float]:
    """R_w and the payoffs [xR_w, z_{t-1} xR_w] on the 1940:12.. sample, plus sigma^2_e."""
    e_os = os_forecast(df)
    d = df.loc[e_os.index]
    var_e = d["Rw"].var(ddof=0)
    z_lag = e_os / var_e                          # z_{t-1}, aligned with xR_w,t
    X = pd.DataFrame({"xR_w": d["xRw"], "z_xR_w": z_lag * d["xRw"]})
    return d["Rw"], X, var_e


def g_bar(gamma: float, rw: np.ndarray, X: np.ndarray) -> np.ndarray:
    return (rw[:, None] ** (-gamma) * X).mean(axis=0)


def gmm_gamma(rw: np.ndarray, X: np.ndarray, W: np.ndarray) -> float:
    obj = lambda c: float(g_bar(c, rw, X) @ W @ g_bar(c, rw, X))
    vals = np.array([obj(c) for c in GAMMA_GRID])
    k = int(np.nanargmin(vals))
    assert 0 < k < len(GAMMA_GRID) - 1, "GMM objective minimised at the grid boundary"
    res = minimize_scalar(obj, bounds=(GAMMA_GRID[k - 1], GAMMA_GRID[k + 1]),
                          method="bounded", options={"xatol": 1e-12})
    return float(res.x)


def centered_nw_s(gamma: float, rw: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, int]:
    g = rw[:, None] ** (-gamma) * X
    gc = g - g.mean(axis=0)
    L = nw1994_lag(gc)
    return newey_west_s(gc, L), L


def gmm_inference(gamma: float, rw: np.ndarray, X: np.ndarray, W: np.ndarray,
                  S: np.ndarray) -> dict:
    T, K = X.shape
    gb = g_bar(gamma, rw, X)
    d = (-np.log(rw)[:, None] * rw[:, None] ** (-gamma) * X).mean(axis=0)[:, None]   # K x 1
    a = d.T @ W                                                                      # 1 x K
    ad_inv = np.linalg.inv(a @ d)
    var_gamma = (ad_inv @ a @ S @ a.T @ ad_inv / T).item()
    P = np.eye(K) - d @ ad_inv @ a
    var_g = P @ S @ P.T / T
    evals, evecs = np.linalg.eigh(var_g)
    keep = np.argsort(evals)[1:]                                                     # rank K-1
    var_g_pinv = (evecs[:, keep] / evals[keep]) @ evecs[:, keep].T
    stat = float(gb @ var_g_pinv @ gb)
    se_g = np.sqrt(np.diag(var_g))
    return dict(gamma=gamma, se=np.sqrt(var_gamma), gbar=gb, se_g=se_g, t_g=gb / se_g,
                chi2=stat, df=K - 1, p=float(chi2.sf(stat, K - 1)), T=T, K=K,
                eig_ratio=float(np.sort(evals)[0] / np.sort(evals)[-1]))


def write_table(prefix: str, res: dict, labels: list, sample: pd.PeriodIndex,
                L: int, weighting: str) -> None:
    rows = [{"quantity": "gamma", "estimate": res["gamma"], "std_error": res["se"],
             "t_stat": res["gamma"] / res["se"]}]
    rows += [{"quantity": f"pricing error: {lab}", "estimate": v, "std_error": s, "t_stat": t}
             for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    rows.append({"quantity": f"chi2({res['df']})", "estimate": res["chi2"],
                 "std_error": np.nan, "t_stat": np.nan, "p_value": res["p"]})
    pd.DataFrame(rows).to_csv(OUT_DIR / f"{prefix}_gmm.csv", index=False)

    md = ["| | Estimate | Std. error | t-stat |", "|---|---:|---:|---:|",
          f"| $\\gamma$ | {res['gamma']:.4f} | {res['se']:.4f} | {res['gamma'] / res['se']:.2f} |"]
    md += [f"| Pricing error: {lab} | {v:.5f} | {s:.5f} | {t:.2f} |"
           for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    md.append("")
    p_txt = f"= {res['p']:.4f}" if res["p"] >= 1e-4 else "< 0.0001"
    md.append(f"$\\chi^2$ test that the pricing errors are jointly zero: "
              f"$\\chi^2({res['df']}) = {res['chi2']:.3f}$, p-value {p_txt}.")
    md.append("")
    md.append(f"{weighting}; monthly observations of annual returns, "
              f"{sample[0].strftime('%Y:%m')}–{sample[-1].strftime('%Y:%m')} (T = {res['T']}). "
              f"Newey-West (1987, 1994) S (centered) with automatic lag L = {L}.")
    (OUT_DIR / f"{prefix}_gmm_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")


MANAGED_LABELS = [r"$\hat E[R_{w,t}^{-\gamma} xR_{w,t}]$",
                  r"$\hat E[R_{w,t}^{-\gamma} z_{t-1} xR_{w,t}]$"]


def print_result(name: str, res: dict, L: int) -> None:
    print(f"{name}: gamma = {res['gamma']:.6f} (s.e. {res['se']:.6f}), T = {res['T']}, K = {res['K']}, L = {L}")
    print("  g_bar :", np.array2string(res["gbar"], precision=6))
    print("  t     :", np.array2string(res["t_g"], precision=3))
    print(f"  chi2({res['df']}) = {res['chi2']:.4f}, p = {res['p']:.4f}; "
          f"smallest/largest eigenvalue of Var(g_bar) = {res['eig_ratio']:.1e}")


def main() -> None:
    df = load_eq()
    rw, X, var_e = managed_moments(df)
    K = X.shape[1]
    W = np.eye(K)
    gamma = gmm_gamma(rw.to_numpy(), X.to_numpy(), W)
    S, L = centered_nw_s(gamma, rw.to_numpy(), X.to_numpy())
    res = gmm_inference(gamma, rw.to_numpy(), X.to_numpy(), W, S)
    write_table("q3c", res, MANAGED_LABELS, X.index, L, "GMM with identity weighting matrix")
    print(f"sample {X.index[0]} to {X.index[-1]}; sigma^2_e = {var_e:.6f}")
    print_result("3(c)", res, L)


if __name__ == "__main__":
    main()
