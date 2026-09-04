"""
Pset 1, Question 2(b) -- one-year-ahead predictive regression of the excess equity
return on the dividend-price ratio, with five standard-error estimators for b.

Student specification (as given):
  Regression (the H = 1 case of Equation 2.1 / Equation 2.2):
      y_t = theta' x_t + e_t,   y_t = xR_{t+1},  x_t = [1, (D/P)_t],  theta = [a, b]
  with xR_t = exp(re_t) - exp(rf_t) and (D/P)_t = exp(dp_t), and "t+1" one year
  ahead = 12 rows ahead in the monthly dataset (the timing convention the student
  fixed for Q2(a); see code/q2a.py).

  Asymptotic variance (problem set note under Q2(b)):
      Var[theta_hat] = (1/T) * Q^{-1} S_hat Q^{-1},     Q = (1/T) sum_t x_t x_t'

  Five S_hat estimators:
    (i)   OLS      : S = sigma_e^2 * Q,          sigma_e^2 = (1/T) sum_t e_t^2
    (ii)  White    : S = (1/T) sum_t e_t^2 x_t x_t'
    (iii) NW(11)   : S = Om_0 + sum_{l=1..L} (1 - l/(L+1)) (Om_l + Om_l'),  L = 11
    (iv)  HH(11)   : S = Om_0 + sum_{l=1..L} 1 * (Om_l + Om_l'),            L = 11
    (v)   NW 87/94 : Bartlett weights as in (iii) with L = a * T^(1/3), where a is
                     the Newey-West (1994, Eq. 2.2) data-driven constant.
  with Om_l = 1/(T-l) * sum_{t=l+1..T} e_t x_t x_{t-l}' e_{t-l}.

Packages are prioritised, per the student's request:
  * statsmodels  -- OLS fit; cov_hc0 (White); cov_hac_simple with weights_bartlett
                    (Newey-West) and weights_uniform (Hansen-Hodrick).
  * linearmodels -- kernel_optimal_bandwidth, the Newey-West (1994, Eq. 2.2)
                    data-driven bandwidth rule, used for method (v).

The reported numbers follow the formulas above exactly. statsmodels normalises each
lag term by 1/T rather than the specified 1/(T-l), so its HAC covariance equals the
specified one with each lag-l term scaled by (T-l)/T; both are computed and printed
side by side so the (tiny) difference is visible rather than hidden.

Outputs: output/q2b_se.csv and output/q2b_se.tex (paths relative to "Pset 1").
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv.covariance import kernel_optimal_bandwidth
from statsmodels.stats.sandwich_covariance import (
    cov_hac_simple,
    cov_hc0,
    weights_bartlett,
    weights_uniform,
)

PSET_DIR = Path(__file__).resolve().parents[1]      # .../Pset 1
DATA_CSV = PSET_DIR / "EQ Dataset.csv"
OUT_DIR = PSET_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

MONTHS_PER_YEAR = 12
OVERLAP_LAGS = MONTHS_PER_YEAR - 1                  # L = Overlap = H - 1 = 11


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(
        dict(year=df["YEAR"], month=df["MONTH"], day=1)
    ).dt.to_period("M")
    df = df.sort_values("date").set_index("date")
    full = pd.period_range(df.index[0], df.index[-1], freq="M")
    assert df.index.equals(full), "monthly date index has gaps; row-shift timing invalid"
    return df


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    """y_t = xR_{t+1 year}; x_t = [1, (D/P)_t]. Same construction as q2a.py at H = 1."""
    xr = np.exp(df["re"]) - np.exp(df["rf"])
    dp_level = np.exp(df["dp"])
    reg = pd.DataFrame(
        {"dp_level": dp_level, "y": xr.shift(-MONTHS_PER_YEAR)}
    ).dropna()
    return reg


def omega(h: np.ndarray, lag: int) -> np.ndarray:
    """Om_l = 1/(T-l) * sum_{t=l+1..T} h_t h_{t-l}', with h_t = e_t * x_t."""
    T = h.shape[0]
    if lag == 0:
        return h.T @ h / T
    return h[lag:].T @ h[:-lag] / (T - lag)


def s_hac(h: np.ndarray, L: int, weights: np.ndarray) -> np.ndarray:
    """S = Om_0 + sum_{l=1..L} w_l (Om_l + Om_l')."""
    S = omega(h, 0)
    for lag in range(1, L + 1):
        om = omega(h, lag)
        S = S + weights[lag] * (om + om.T)
    return S


def sandwich(Q: np.ndarray, S: np.ndarray, T: int) -> np.ndarray:
    """Var[theta_hat] = (1/T) Q^{-1} S Q^{-1}."""
    Qinv = np.linalg.inv(Q)
    return Qinv @ S @ Qinv / T


def main() -> None:
    df = load_data(DATA_CSV)
    reg = build_sample(df)

    y = reg["y"].to_numpy()
    X = sm.add_constant(reg[["dp_level"]].to_numpy())      # x_t = [1, D/P_t]
    T, k = X.shape

    fit = sm.OLS(y, X).fit()
    a_hat, b_hat = fit.params
    e = fit.resid
    h = X * e[:, None]                                     # h_t = e_t * x_t
    Q = X.T @ X / T
    sigma2 = (e @ e) / T                                   # sigma_e^2 = (1/T) sum e^2

    # ---- (v) Newey-West (1994, Eq. 2.2) data-driven bandwidth -------------------
    # linearmodels' convention for a model with an intercept: run the NW(1994) rule
    # on the non-constant regressor's moment condition, e_t * (D/P)_t.
    scores = h[:, 1:]
    L_nw94 = int(kernel_optimal_bandwidth(scores, kernel="bartlett"))
    a_const = L_nw94 / T ** (1 / 3)                        # the "a" in L = a * T^(1/3)

    # ---- the five S_hat estimators ---------------------------------------------
    estimators = {
        "OLS": sigma2 * Q,
        "White (1980)": h.T @ h / T,
        f"Newey-West ({OVERLAP_LAGS} lags)": s_hac(
            h, OVERLAP_LAGS, weights_bartlett(OVERLAP_LAGS)
        ),
        f"Hansen-Hodrick ({OVERLAP_LAGS} lags)": s_hac(
            h, OVERLAP_LAGS, weights_uniform(OVERLAP_LAGS)
        ),
        f"Newey-West (1987, 1994) [L={L_nw94}]": s_hac(
            h, L_nw94, weights_bartlett(L_nw94)
        ),
    }

    rows = []
    for name, S in estimators.items():
        V = sandwich(Q, S, T)
        var_b = V[1, 1]
        se_b = np.sqrt(var_b) if var_b > 0 else np.nan
        rows.append(
            {
                "method": name,
                "b": b_hat,
                "se_b": se_b,
                "t_b": b_hat / se_b if var_b > 0 else np.nan,
                "var_b_positive": bool(var_b > 0),
                "pos_def": bool(np.all(np.linalg.eigvalsh(V) > 0)),
            }
        )
    res = pd.DataFrame(rows)

    # ---- package cross-checks ---------------------------------------------------
    # White: statsmodels cov_hc0 is algebraically identical to the specified form.
    # HAC: statsmodels normalises every lag term by 1/T instead of 1/(T-l), so it is
    # the specified estimator with each lag-l term scaled by (T-l)/T.
    chk = {
        "White (1980)": cov_hc0(fit),
        f"Newey-West ({OVERLAP_LAGS} lags)": cov_hac_simple(
            fit, nlags=OVERLAP_LAGS, weights_func=weights_bartlett, use_correction=False
        ),
        f"Hansen-Hodrick ({OVERLAP_LAGS} lags)": cov_hac_simple(
            fit, nlags=OVERLAP_LAGS, weights_func=weights_uniform, use_correction=False
        ),
        f"Newey-West (1987, 1994) [L={L_nw94}]": cov_hac_simple(
            fit, nlags=L_nw94, weights_func=weights_bartlett, use_correction=False
        ),
    }
    res["se_b_statsmodels"] = [
        np.sqrt(chk[n][1, 1]) if n in chk and chk[n][1, 1] > 0 else np.nan
        for n in res["method"]
    ]
    # baseline OLS: statsmodels divides by T-k, the spec divides by T
    res.loc[res["method"] == "OLS", "se_b_statsmodels"] = fit.bse[1]

    res.to_csv(OUT_DIR / "q2b_se.csv", index=False)

    tex = [
        r"\begin{tabular}{lrrr}",
        r"\hline",
        r"Standard error method & $\hat{b}$ & s.e.$(\hat{b})$ & $t$-stat \\",
        r"\hline",
    ]
    for r in rows:
        se = "---" if np.isnan(r["se_b"]) else f"{r['se_b']:.4f}"
        tt = "---" if np.isnan(r["t_b"]) else f"{r['t_b']:.4f}"
        tex.append(f"{r['method']} & {r['b']:.4f} & {se} & {tt} " + r"\\")
    tex += [r"\hline", r"\end{tabular}"]
    (OUT_DIR / "q2b_se.tex").write_text("\n".join(tex) + "\n")

    pd.set_option("display.float_format", lambda v: f"{v:10.4f}")
    print(f"Sample      : T = {T} monthly obs, {reg.index[0]} .. {reg.index[-1]}")
    print(f"a_hat       : {a_hat:.6f}")
    print(f"b_hat       : {b_hat:.6f}")
    print(f"sigma_e^2   : {sigma2:.8f}   (1/T normalisation, as specified)")
    print(
        f"NW94 lag L  : {L_nw94}   "
        f"(a = L / T^(1/3) = {a_const:.4f}, T^(1/3) = {T ** (1 / 3):.3f})"
    )
    print()
    print(res.to_string(index=False))
    print()
    print(f"wrote {OUT_DIR / 'q2b_se.csv'}")
    print(f"wrote {OUT_DIR / 'q2b_se.tex'}")


if __name__ == "__main__":
    main()
