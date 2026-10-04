"""
Pset 2, Question 3(b) -- GMM estimate of the relative risk aversion gamma from the
unconditional SDF equation E[R_w,t^(-gamma) xR_w,t] = 0.

Student specification (as given, 2026-10-04):
  * Data: Data/EQ Dataset.csv (monthly observations of annual variables).
  * xR_t = exp(re_t) - exp(rf_t);  R_w,t = R_e,t = exp(re_t).
  * Moment condition: E[R_w,t^(-gamma) xR_t] = 0 (R_w and xR from the same row, as in
    the student's E[R_{w*,t+1}^(-gamma) xR_{t+1}] = 0).
  * GMM; S estimated with Newey-West (1987, 1994); report gamma and its standard error.

Applied as (stated so nothing is silent):
  * Sample: every month in the file, 1927:12 to 2021:12 (no restriction was specified).
  * One moment, one parameter: gamma_hat solves g_bar(gamma) = 0. The script scans
    gamma on [-50, 50] and requires exactly one sign change of g_bar, then solves with
    Brent's method inside that bracket. (If no root existed, footnote 5's minimisation
    would be needed; here a root exists, so g_bar(gamma_hat) = 0.)
  * aVar[gamma_hat] = S / (T G^2), with G = E_T[d/dgamma (R_w^(-gamma) xR)]
                                         = E_T[-ln(R_w) R_w^(-gamma) xR] at gamma_hat.
  * Newey-West S as in Q2 (code/q2a.py) and Pset 1/code/q2b.py: Bartlett weights
    1 - l/(L+1), Om_l = 1/(T-l) sum g_t g_{t-l}; lag L from the Newey-West (1994) rule
    (linearmodels.kernel_optimal_bandwidth) applied to the moment series g_t(gamma_hat).

Outputs (paths relative to "Pset 2"): output/q3b_gmm.csv, output/q3b_gmm_table.md
"""

import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth
from scipy.optimize import brentq, minimize_scalar

from q2a import OUT_DIR, PSET_DIR, newey_west_s

EQ_CSV = PSET_DIR / "Data" / "EQ Dataset.csv"
GAMMA_GRID = np.linspace(-50.0, 50.0, 10001)


def load_eq() -> pd.DataFrame:
    df = pd.read_csv(EQ_CSV)
    df.index = pd.PeriodIndex(
        pd.to_datetime(dict(year=df["YEAR"], month=df["MONTH"], day=1)), freq="M"
    )
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly index has gaps"
    assert df[["re", "rf"]].notna().all().all(), "missing re/rf"
    return pd.DataFrame(
        {"Rw": np.exp(df["re"]), "xR": np.exp(df["re"]) - np.exp(df["rf"])}, index=df.index
    )


def g_series(gamma: float, rw: np.ndarray, xr: np.ndarray) -> np.ndarray:
    return rw ** (-gamma) * xr


def main() -> None:
    d = load_eq()
    rw, xr = d["Rw"].to_numpy(), d["xR"].to_numpy()
    T = len(d)
    gbar = lambda g: g_series(g, rw, xr).mean()

    vals = np.array([gbar(g) for g in GAMMA_GRID])
    flips = np.flatnonzero(np.sign(vals[:-1]) != np.sign(vals[1:]))
    assert len(flips) == 1, f"expected one root of g_bar on [-50, 50], found {len(flips)}"
    lo, hi = GAMMA_GRID[flips[0]], GAMMA_GRID[flips[0] + 1]
    gamma = brentq(gbar, lo, hi, xtol=1e-14)

    g = g_series(gamma, rw, xr)
    G = np.mean(-np.log(rw) * g)
    L = int(kernel_optimal_bandwidth(g - g.mean(), kernel="bartlett"))
    S = newey_west_s(g[:, None], L)[0, 0]
    se = np.sqrt(S / (T * G ** 2))

    # Cross-check: the minimiser of g_bar^2 (footnote 5's GMM problem) is the same point.
    gamma_min = minimize_scalar(lambda c: gbar(c) ** 2, bracket=(lo, hi), tol=1e-12).x

    res = pd.DataFrame(
        {"parameter": ["gamma"], "estimate": [gamma], "std_error": [se],
         "t_stat": [gamma / se], "nw_lag": [L], "T": [T],
         "start": [str(d.index[0])], "end": [str(d.index[-1])]}
    )
    res.to_csv(OUT_DIR / "q3b_gmm.csv", index=False)

    table = (
        "| Parameter | Estimate | Std. error | t-stat |\n"
        "|---|---:|---:|---:|\n"
        f"| $\\gamma$ | {gamma:.4f} | {se:.4f} | {gamma / se:.2f} |\n"
        f"\nGMM with the single moment $\\hat E[R_{{w,t}}^{{-\\gamma}} xR_{{w,t}}] = 0$, "
        f"$R_{{w,t}} = e^{{r_{{e,t}}}}$, $xR_{{w,t}} = e^{{r_{{e,t}}}} - e^{{r_{{f,t}}}}$; monthly observations "
        f"of annual returns, {d.index[0].strftime('%Y:%m')}–{d.index[-1].strftime('%Y:%m')} (T = {T}). "
        f"Newey-West (1987, 1994) S with automatic lag L = {L}.\n"
    )
    (OUT_DIR / "q3b_gmm_table.md").write_text(table, encoding="utf-8")

    print(f"Sample {d.index[0]} to {d.index[-1]}, T = {T}")
    print(f"sign changes of g_bar on [-50, 50]: {len(flips)} (bracket [{lo:.2f}, {hi:.2f}])")
    print(f"gamma_hat = {gamma:.6f}   g_bar(gamma_hat) = {gbar(gamma):.2e}")
    print(f"argmin g_bar^2 = {gamma_min:.6f}")
    print(f"G = {G:.6f}   S = {S:.6e}   NW(1994) lag L = {L}")
    print(f"s.e. = {se:.6f}   t = {gamma / se:.3f}")


if __name__ == "__main__":
    main()
