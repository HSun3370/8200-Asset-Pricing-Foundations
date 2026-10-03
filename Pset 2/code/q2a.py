"""
Pset 2, Question 2(a) -- the SDF M*_t = a - b' xR_t that prices the excess returns of
the 10 book-to-market decile portfolios, estimated by two-step GMM.

Student specification (as given, 2026-10-03):
  Data
    * Data/Portfolios_Formed_on_BE-ME.csv, block "Value Weight Returns -- Monthly",
      columns Lo 10, 2-Dec, 3-Dec, 4-Dec, 5-Dec, 6-Dec, 7-Dec, 8-Dec, 9-Dec, Hi 10.
    * Data/F-F_Research_Data_Factors.csv, monthly block, column RF.
  Variables
    * xR_t = excess returns of the 10 portfolios over RF.
    * M*_t = a - b' xR_t; theta = (a, b) has 11 parameters.
  Moment conditions
    * E[M*_t xR_t] = 0   (10 conditions)
    * E[M*_t]      = 1   (1 condition)
  Estimation: two-step GMM; report the parameters with standard errors.
  Output: scatterplot with the portfolio decile (1..10) on the x-axis and the
          respective b coefficient on the y-axis.

Decisions made by the student when AI flagged them (2026-10-03):
  * Portfolios: the 10 deciles only ("Hi 20", the top quintile, is NOT used).
  * Sample: 1927:07 to 2026:08 (the last month in the file).
  * Units: decimals, xR_t = (R_t - RF_t) / 100.
  * S (for the second-step weighting matrix and the standard errors):
    Newey-West with the automatic Newey-West (1994) lag choice.

Implementation (programming choices, not part of the design):
  * The moments are linear in theta:  g_bar(theta) = D theta - c, with
        D = [[ mu,  -E[xR xR'] ],      c = [0_10; 1],   mu = E[xR]
             [ 1 ,  -mu'       ]]
    so each GMM step has the closed form theta = (D'WD)^{-1} D'W c.
    Step 1 uses W = I; step 2 uses W = S^{-1}, with S estimated at the step-1 estimate.
  * 11 moments and 11 parameters: the system is exactly identified, so both steps
    set g_bar = 0 exactly and give the same theta (the script checks this).
  * Var[theta_hat] = (1/T) (D'WD)^{-1} D'W S W D (D'WD)^{-1}; with W = S^{-1} this is
    (1/T) (D' S^{-1} D)^{-1}.
  * Newey-West S, with the same lag normalisation as Pset 1/code/q2b.py:
        S = Om_0 + sum_{l=1..L} (1 - l/(L+1)) (Om_l + Om_l'),
        Om_l = 1/(T-l) sum_{t=l+1..T} g_t g_{t-l}'.
    The textbook 1/T normalisation is also computed and its effect on the standard
    errors is printed.
  * Automatic lag L: linearmodels' kernel_optimal_bandwidth (Newey-West 1994 rule,
    Bartlett kernel), applied as in linearmodels' own GMM code to a vector of
    moments: each moment series is divided by its standard deviation and the 11
    series are summed into one series before the rule is applied.

Outputs (paths relative to "Pset 2"):
  output/q2a_gmm.csv, output/q2a_gmm_table.md, output/q2a_b_scatter.png

load_excess_returns, estimate_sdf and save_results are reused by code/q2b.py and code/q2c.py.
"""

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.iv.covariance import kernel_optimal_bandwidth

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 2
PORT_CSV = PSET_DIR / "Data" / "Portfolios_Formed_on_BE-ME.csv"
FF_CSV = PSET_DIR / "Data" / "F-F_Research_Data_Factors.csv"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

DECILES = ["Lo 10", "2-Dec", "3-Dec", "4-Dec", "5-Dec",
           "6-Dec", "7-Dec", "8-Dec", "9-Dec", "Hi 10"]
SAMPLE_START = pd.Period("1927-07", freq="M")
SAMPLE_END = pd.Period("2026-08", freq="M")


def read_french_block(path: Path, title: str) -> pd.DataFrame:
    """Read one monthly block of a Ken French CSV: the header row follows `title`
    (or is the first row starting with ','), and the block ends at the first blank line."""
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


def load_excess_returns(port_csv: Path = PORT_CSV, columns: list = DECILES,
                        block: str = "Value Weight Returns -- Monthly") -> pd.DataFrame:
    port = read_french_block(port_csv, block)[columns]
    rf = read_french_block(FF_CSV, "")["RF"]
    port = port.loc[SAMPLE_START:SAMPLE_END]
    assert port.index[0] == SAMPLE_START and port.index[-1] == SAMPLE_END
    full = pd.period_range(SAMPLE_START, SAMPLE_END, freq="M")
    assert port.index.equals(full), "monthly index has gaps"
    assert rf.index.to_series().reindex(full).notna().all(), "RF missing for some months"
    assert (port > -99.99).all().all(), "missing-value code (-99.99 / -999) in sample"
    xr = port.sub(rf.reindex(full), axis=0) / 100.0      # decimals
    return xr


def moments(theta: np.ndarray, x: np.ndarray) -> np.ndarray:
    """g_t(theta) = [M_t xR_t, M_t - 1], with M_t = a - b' xR_t.  Shape (T, N+1)."""
    a, b = theta[0], theta[1:]
    m = a - x @ b
    return np.column_stack([m[:, None] * x, m - 1.0])


def omega(g: np.ndarray, lag: int, per_lag_norm: bool) -> np.ndarray:
    T = g.shape[0]
    if lag == 0:
        return g.T @ g / T
    denom = (T - lag) if per_lag_norm else T
    return g[lag:].T @ g[:-lag] / denom


def newey_west_s(g: np.ndarray, L: int, per_lag_norm: bool = True) -> np.ndarray:
    S = omega(g, 0, per_lag_norm)
    for lag in range(1, L + 1):
        om = omega(g, lag, per_lag_norm)
        S = S + (1.0 - lag / (L + 1.0)) * (om + om.T)
    return S


def nw1994_lag(g: np.ndarray) -> int:
    z = g - g.mean(axis=0)
    z = (z / z.std(axis=0)).sum(axis=1)
    return int(kernel_optimal_bandwidth(z, kernel="bartlett"))


def gmm_step(D: np.ndarray, c: np.ndarray, W: np.ndarray) -> np.ndarray:
    """argmin (D theta - c)' W (D theta - c)."""
    return np.linalg.solve(D.T @ W @ D, D.T @ W @ c)


def gmm_cov(D: np.ndarray, W: np.ndarray, S: np.ndarray, T: int) -> np.ndarray:
    bread = np.linalg.inv(D.T @ W @ D)
    return bread @ D.T @ W @ S @ W @ D @ bread / T


def estimate_sdf(xr: pd.DataFrame) -> dict:
    """Two-step GMM for M*_t = a - b' xR_t with E[M* xR] = 0 and E[M*] = 1."""
    x = xr.to_numpy()
    T, N = x.shape

    mu = x.mean(axis=0)
    Exx = x.T @ x / T
    D = np.block([[mu[:, None], -Exx], [np.ones((1, 1)), -mu[None, :]]])
    c = np.r_[np.zeros(N), 1.0]

    # Step 1: W = I.
    theta1 = gmm_step(D, c, np.eye(N + 1))
    g1 = moments(theta1, x)
    L1 = nw1994_lag(g1)
    S1 = newey_west_s(g1, L1)

    # Step 2: W = S^{-1} from step 1.
    W2 = np.linalg.inv(S1)
    theta2 = gmm_step(D, c, W2)
    g2 = moments(theta2, x)
    L2 = nw1994_lag(g2)
    S2 = newey_west_s(g2, L2)
    V = gmm_cov(D, np.linalg.inv(S2), S2, T)
    se = np.sqrt(np.diag(V))

    gbar = g2.mean(axis=0)
    J = T * gbar @ np.linalg.inv(S2) @ gbar

    # Same standard errors with the textbook 1/T lag normalisation (for comparison).
    S2_T = newey_west_s(g2, L2, per_lag_norm=False)
    se_T = np.sqrt(np.diag(gmm_cov(D, np.linalg.inv(S2_T), S2_T, T)))

    m_star = pd.Series(theta2[0] - x @ theta2[1:], index=xr.index, name="M_star")
    return dict(theta1=theta1, theta=theta2, se=se, se_T=se_T, L1=L1, L=L2,
                gbar=gbar, J=J, m_star=m_star, T=T, N=N)


def save_results(fit: dict, xr: pd.DataFrame, columns: list, prefix: str,
                 xlabel: str = "", title: str = "", plot: bool = True) -> pd.DataFrame:
    """Write <prefix>_gmm.csv, <prefix>_gmm_table.md and (if plot) <prefix>_b_scatter.png."""
    theta1, theta2, se, T, N = fit["theta1"], fit["theta"], fit["se"], fit["T"], fit["N"]
    names = ["a"] + [f"b_{k} ({p})" for k, p in enumerate(columns, start=1)]
    res = pd.DataFrame(
        {
            "parameter": names,
            "estimate_step1": theta1,
            "estimate": theta2,
            "std_error": se,
            "t_stat": theta2 / se,
        }
    )
    res.to_csv(OUT_DIR / f"{prefix}_gmm.csv", index=False)

    rows = ["| Parameter | Estimate | Std. error | t-stat |",
            "|---|---:|---:|---:|"]
    for _, r in res.iterrows():
        label = "$a$" if r["parameter"] == "a" else (
            f"$b_{{{r['parameter'].split()[0][2:]}}}$ ({r['parameter'].split('(')[1][:-1]})")
        rows.append(f"| {label} | {r['estimate']:.4f} | {r['std_error']:.4f} | {r['t_stat']:.2f} |")
    note = (f"\nTwo-step GMM, monthly, {xr.index[0].strftime('%Y:%m')}–"
            f"{xr.index[-1].strftime('%Y:%m')} (T = {T}). Excess returns in decimals. "
            f"Newey-West S with automatic lag L = {fit['L']}.\n")
    (OUT_DIR / f"{prefix}_gmm_table.md").write_text("\n".join(rows) + "\n" + note, encoding="utf-8")
    if not plot:
        return res

    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    deciles = np.arange(1, N + 1)
    ax.scatter(deciles, theta2[1:], color="tab:blue", zorder=3)
    ax.axhline(0.0, color="grey", linewidth=0.8)
    ax.set_xticks(deciles)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$b$ coefficient")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"{prefix}_b_scatter.png", dpi=200)
    plt.close(fig)
    return res


def print_summary(fit: dict, xr: pd.DataFrame, res: pd.DataFrame) -> None:
    theta1, theta2, se = fit["theta1"], fit["theta"], fit["se"]
    pd.set_option("display.width", 120)
    print(f"Sample {xr.index[0]} to {xr.index[-1]}, T = {fit['T']}, N = {fit['N']}")
    print(f"NW(1994) automatic lag: step 1 L = {fit['L1']}, step 2 L = {fit['L']}")
    print(f"max |theta_step2 - theta_step1| = {np.abs(theta2 - theta1).max():.2e}")
    print(f"max |g_bar| at step-2 estimate = {np.abs(fit['gbar']).max():.2e};  J = {fit['J']:.2e}")
    print(f"mean M* = {fit['m_star'].mean():.6f}")
    print(f"max relative change in s.e. under 1/T lag normalisation: "
          f"{np.abs(fit['se_T'] / se - 1).max():.2%}")
    print(res.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


def main() -> None:
    xr = load_excess_returns()
    fit = estimate_sdf(xr)
    res = save_results(
        fit, xr, DECILES, "q2a",
        xlabel="Book-to-market decile (1 = Lo 10, 10 = Hi 10)",
        title=r"Q2(a): $b$ in $M^*_t = a - b'xR_t$, BM deciles",
    )
    print_summary(fit, xr, res)


if __name__ == "__main__":
    main()
