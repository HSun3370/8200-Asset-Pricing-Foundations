"""
Pset 3, Question 2(e) -- GMM estimate of b in the SDF
    M_t = a - b_m r_m,t - b_E r_E,t - b_V r_V,t
from E[M r_m] = E[M r_E] = E[M r_V] = 0.

Student specification (as given, 2026-11-22):
  Data: monthly ICAPM factors (market r_m, reinvestment risk r_E, volatility r_V) of
  Chabi-Yo, Goncalves, and Loudis (2025), from https://andreigoncalves.com/published-papers/.
  SDF and three moment conditions as above (the SDF prices r_m, r_E and r_V), GMM; report
  each b element times its factor volatility, and the Newey-West (1987, 1994) t-stat of
  each b.

Decisions made by the student when AI flagged them (2026-11-22):
  * Data file: "Original Intertemporal Risk Factors (1928-2019)",
      https://andreigoncalves.com/wp-content/uploads/ICAPMfactors_originalPaper.csv
    downloaded 2026-11-22 into Pset 3/Data/ (every month, 1928:01 to 2019:12; not the
    1928-2024 update).
  * Normalization: E[M] = 1 with E[r] set to the sample mean and treated as known, i.e.
    M_t = 1 - b'(r_t - E[r]) (course slides, Module 2, p. 38): 3 moments, 3 parameters.
  * Newey-West lag: the Newey-West (1994) rule is applied to each of the three moment series
    separately and the largest lag is used for S. (The Pset 2 convention, one lag from the sum
    of the standardized moment series, gave L = 1 here and depends on the factors' signs: with
    r_V sign-flipped it gives L = 14.)

Implementation (carried over / course formulas):
  * Units as in the file: monthly decimals. r_m is the excess market return (correlation
    0.99999 with Ken French's Mkt-RF); all three factors are treated as excess returns.
  * g_t(b) = (1 - b'(r_t - rbar)) r_t. Just identified, so b solves g_bar(b) = 0, which is
    linear in b: G b = rbar with G = (1/T) sum_t r_t (r_t - rbar)'.
  * aVar[b] = (1/T) G^-1 S G^-1' (the weighting matrix drops out).
  * S: Newey-West, Bartlett weights 1 - l/(L+1), Om_l = 1/(T-l) sum g_t g_{t-l}' (the
    student's convention since Pset 1); lag rule: linearmodels.kernel_optimal_bandwidth.
    g_bar(b_hat) = 0, so centered and uncentered S coincide.
  * Factor volatility: monthly sample standard deviation (divisor T - 1), as in Pset 3 1(e).

Outputs (paths relative to "Pset 3"): output/q2e_gmm.csv, output/q2e_table.md
"""

import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth

from q1e import DATA, OUT_DIR, newey_west_s

FACTOR_CSV = DATA / "ICAPMfactors_originalPaper.csv"
FACTORS = ["rM", "rE", "rV"]
LABELS = {"rM": "m", "rE": "E", "rV": "V"}


def load_factors() -> pd.DataFrame:
    df = pd.read_csv(FACTOR_CSV)
    df.index = pd.PeriodIndex(
        pd.to_datetime(dict(year=df["YEAR"], month=df["MONTH"], day=1)), freq="M"
    )
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly index has gaps"
    assert df[FACTORS].notna().all().all(), "missing factor values"
    return df[FACTORS]


def moments(b: np.ndarray, r: np.ndarray) -> np.ndarray:
    """g_t(b) = (1 - b'(r_t - rbar)) r_t.  Shape (T, 3)."""
    m = 1.0 - (r - r.mean(axis=0)) @ b
    return m[:, None] * r


def nw1994_lags(g: np.ndarray) -> list:
    """Newey-West (1994) automatic lag of each moment series."""
    return [int(kernel_optimal_bandwidth(x - x.mean(), kernel="bartlett")) for x in g.T]


def estimate(r: np.ndarray) -> dict:
    T = len(r)
    rbar = r.mean(axis=0)
    G = r.T @ (r - rbar) / T
    b = np.linalg.solve(G, rbar)
    g = moments(b, r)
    lags = nw1994_lags(g)
    L = max(lags)
    Ginv = np.linalg.inv(G)
    V = Ginv @ newey_west_s(g, L) @ Ginv.T / T
    return dict(b=b, se=np.sqrt(np.diag(V)), L=L, lags=lags, T=T, gbar=g.mean(axis=0),
                m=1.0 - (r - rbar) @ b, a=1.0 + b @ rbar)


def main() -> None:
    df = load_factors()
    r = df.to_numpy()
    fit = estimate(r)
    sigma = r.std(axis=0, ddof=1)
    res = pd.DataFrame(
        {"factor": FACTORS, "b": fit["b"], "std_error": fit["se"], "t_stat": fit["b"] / fit["se"],
         "sigma_monthly": sigma, "b_times_sigma": fit["b"] * sigma}
    )
    res.assign(NW_lag=fit["L"], T=fit["T"], a=fit["a"], start=str(df.index[0]),
               end=str(df.index[-1])).to_csv(OUT_DIR / "q2e_gmm.csv", index=False)

    md = ["| Factor | $b$ | $\\sigma$ (monthly) | $b \\cdot \\sigma$ | t($b$) |", "|---|---:|---:|---:|---:|"]
    md += [f"| $r_{{{LABELS[x.factor]}}}$ | {x.b:.4f} | {x.sigma_monthly:.4f} | {x.b_times_sigma:.4f} | {x.t_stat:.2f} |"
           for x in res.itertuples()]
    md += ["", f"GMM estimate of $b$ in $M_t = 1 - b'(r_t - \\hat E[r])$, $r_t = (r_{{m,t}}, r_{{E,t}}, r_{{V,t}})'$, from "
               f"$E[M \\cdot r_m] = E[M \\cdot r_E] = E[M \\cdot r_V] = 0$ with the normalization $E[M] = 1$ (just identified; "
               f"$\\hat E[r]$ treated as known). Original ICAPM factors of Chabi-Yo, Gonçalves, and Loudis (2025), monthly "
               f"decimals, {df.index[0].strftime('%Y:%m')}–{df.index[-1].strftime('%Y:%m')} (T = {fit['T']}). "
               f"t-statistics use Newey-West (1987, 1994) S with lag L = {fit['L']}, the largest of the three moments' "
               f"automatic lags ({', '.join(map(str, fit['lags']))})."]
    (OUT_DIR / "q2e_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Sample {df.index[0]} to {df.index[-1]}, T = {fit['T']}, NW(1994) lags {fit['lags']}, L = {fit['L']}")
    print(f"a = 1 + b'rbar = {fit['a']:.6f}; mean M = {fit['m'].mean():.6f}; sd M = {fit['m'].std(ddof=1):.6f}")
    print("max |g_bar(b_hat)| = %.2e" % np.abs(fit["gbar"]).max())
    print(res.to_string(index=False, float_format=lambda v: f"{v:.5f}"))


if __name__ == "__main__":
    main()
