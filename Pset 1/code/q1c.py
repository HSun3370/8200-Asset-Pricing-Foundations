"""
Pset 1, Question 1(c) -- VAR-implied version of the Equation 1.4 variance decomposition.

Student construction (as specified; the missing minus on b_{Delta d} was corrected by
the student):

  Z_t = [dg_t, re_t, dp_t]'          (dg = Delta d).
  VAR(1), overlapping annual:  Z_{t+1} = H + F Z_t + e,  with t+1 = t + 12 months.
    Estimate H (3x1) and F (3x3) by OLS -- regress Z_{tau+12} on [1, Z_tau] over every
    month tau for which tau+12 is in the sample.  Sigma = E(e e') (residual covariance;
    reported for completeness, not used in the decomposition).
  b_z = Cov(dp_t, Z_t) / Var(dp_t)   -- 3-vector, computed directly from the data
                                        (independent of the VAR estimate).
  For H = 1..20:
    M_H       = (F - kappa^H F^{H+1}) (I - kappa F)^{-1}   [ = sum_{j=1}^H kappa^{j-1} F^j ]
    b_re      =  e_re'  M_H b_z
    b_Delta d = -e_dg'  M_H b_z
    b_dp      =  1 - b_re - b_Delta d
  kappa = 1 / (1 + exp(dp_bar)),  dp_bar = full-sample mean of `dp`  (same as 1(b)).
  Also reported (not plotted): b_dp_direct = e_dp' (kappa^H F^H) b_z  as an identity check.

Outputs: output/q1c_slopes.csv and output/q1c_slopes.png (paths relative to "Pset 1").
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PSET_DIR = Path(__file__).resolve().parents[1]
DATA_CSV = PSET_DIR / "EQ Dataset.csv"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

H_MAX = 20
MONTHS_PER_YEAR = 12
VARS = ["dg", "re", "dp"]  # Z_t ordering; dg = Delta d


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(
        dict(year=df["YEAR"], month=df["MONTH"], day=1)
    ).dt.to_period("M")
    df = df.sort_values("date").set_index("date")
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly date index has gaps; row-shift timing invalid"
    return df


def estimate_var(df: pd.DataFrame):
    """Overlapping-annual VAR(1): Z_{tau+12} ~ [1, Z_tau], OLS (equation by equation)."""
    Z = df[VARS].to_numpy()
    Zlead = df[VARS].shift(-MONTHS_PER_YEAR).to_numpy()
    mask = ~np.isnan(Zlead).any(axis=1)
    X = np.column_stack([np.ones(mask.sum()), Z[mask]])
    Y = Zlead[mask]
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)  # (4 x 3): row 0 = intercept, rows 1-3 = F'
    intercept = beta[0]
    F = beta[1:].T  # F[i, j] = d Z_{i,t+1} / d Z_{j,t}
    resid = Y - X @ beta
    Sigma = resid.T @ resid / (len(Y) - X.shape[1])
    return intercept, F, Sigma, int(mask.sum())


def b_z_from_data(df: pd.DataFrame) -> np.ndarray:
    Z = df[VARS].to_numpy()
    dp = df["dp"].to_numpy()
    Zc = Z - Z.mean(axis=0)
    dpc = dp - dp.mean()
    cov_dp_Z = (Zc * dpc[:, None]).mean(axis=0)
    var_dp = (dpc ** 2).mean()
    return cov_dp_Z / var_dp


def horizon_slopes(F: np.ndarray, kappa: float, b_z: np.ndarray) -> pd.DataFrame:
    I3 = np.eye(3)
    e = {name: I3[k] for k, name in enumerate(VARS)}  # unit selector row vectors
    ImkF_inv = np.linalg.inv(I3 - kappa * F)

    rows = []
    for h in range(1, H_MAX + 1):
        Fh = np.linalg.matrix_power(F, h)
        M = (F - kappa ** h * (F @ Fh)) @ ImkF_inv
        M_sum = sum(
            kappa ** (j - 1) * np.linalg.matrix_power(F, j) for j in range(1, h + 1)
        )
        assert np.allclose(M, M_sum), f"M_H closed form != finite sum at h={h}"

        b_re = float(e["re"] @ M @ b_z)
        b_dg = float(-e["dg"] @ M @ b_z)
        b_dp = 1.0 - b_re - b_dg
        b_dp_direct = float(e["dp"] @ (kappa ** h * Fh) @ b_z)
        rows.append(
            {
                "h": h,
                "b_re": b_re,
                "b_dg": b_dg,
                "b_dp": b_dp,
                "sum": b_re + b_dg + b_dp,
                "b_dp_direct": b_dp_direct,
            }
        )
    return pd.DataFrame(rows)


def make_figure(res: pd.DataFrame, kappa: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(1.0, color="0.6", lw=1, ls="--", zorder=1)
    ax.axhline(0.0, color="0.6", lw=0.8, zorder=1)
    ax.plot(res["h"], res["b_re"], "o-", label=r"$b_{re}^{(H)}$  (returns)")
    ax.plot(res["h"], res["b_dg"], "s-", label=r"$b_{\Delta d}^{(H)}$  ($-$dividend growth)")
    ax.plot(res["h"], res["b_dp"], "^-", label=r"$b_{dp}^{(H)}$  ($1-b_{re}-b_{\Delta d}$)")
    ax.set_xlabel("Horizon $H$ (years)")
    ax.set_ylabel("Slope coefficient")
    ax.set_title(f"Q1(c): VAR-implied Eq. 1.4 decomposition  ($\\kappa = {kappa:.4f}$)")
    ax.set_xticks(range(2, H_MAX + 1, 2))
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = load_data(DATA_CSV)
    dp_bar = df["dp"].mean()
    kappa = 1.0 / (1.0 + np.exp(dp_bar))

    intercept, F, Sigma, n_var = estimate_var(df)
    b_z = b_z_from_data(df)
    res = horizon_slopes(F, kappa, b_z)

    csv_path = OUT_DIR / "q1c_slopes.csv"
    png_path = OUT_DIR / "q1c_slopes.png"
    res.to_csv(csv_path, index=False)
    make_figure(res, kappa, png_path)

    np.set_printoptions(precision=4, suppress=True)
    pd.set_option("display.float_format", lambda v: f"{v:9.4f}")
    print(f"N monthly obs              : {len(df)}  ({df.index[0]} .. {df.index[-1]})")
    print(f"dp_bar / kappa            : {dp_bar:.6f} / {kappa:.6f}")
    print(f"overlapping-annual VAR obs : {n_var}")
    print(f"\nVAR intercept H : {intercept}")
    print("VAR F  (rows = [dg, re, dp]_(t+1), cols = [dg, re, dp]_t):")
    print(F)
    print(f"eig(F) moduli   : {np.abs(np.linalg.eigvals(F))}")
    print("Sigma (residual cov, not used downstream):")
    print(Sigma)
    print(f"\nb_z = Cov(dp, Z)/Var(dp) : {b_z}   (dp element = 1 by construction)")
    print(f"\n{res.to_string(index=False)}")
    print(f"\nwrote {csv_path}")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
