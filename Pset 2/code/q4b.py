"""
Pset 2, Question 4(b) -- GMM estimate of b in the linear SDF M_t = 1 - b (R_w,t - E[R_w])
from E[M_t xR_t] = 0, with an identity weighting matrix.

Student specification (as given, 2026-10-24):
  "assume sdf is M_t = 1 - b (R_w - E R_w), and moment condition is E[M xR] = 0. using
   excess return on w and 20 portfolios BM and MOM. using identity weights matrix,
   produce a table, report b with standard error, also produce values and t statistics
   for pricing error of each moment condition as well as p value for X2 test with null
   hypothesis that pricing errors are jointly zero. using Newey west 1987 1994."

Decisions made by the student when AI flagged them (2026-10-24):
  * E[R_w] is estimated jointly as a parameter mu, with the extra moment
    E[R_w,t - mu] = 0. theta = (b, mu); 22 moments:
        g_t = [ (1 - b (R_w,t - mu)) xR_t  (21 pricing moments) ;  R_w,t - mu ].
  * Weighting: identity on all 22 moments (A = G'), so mu_hat need not equal the sample
    mean of R_w.
  * Sample 1940:12 to 2021:12 (the Q3(c)-(e) sample).
  * Results inserted into answers.md.
Carried over from Q3 (see code/q3c.py, q3e.py): R_w,t = exp(re_t), xR_w,t = exp(re_t) -
exp(rf_t); the 20 BM/MOM excess returns are 12-month compounded nominal excess returns
(Ken French, value weighted); centered Newey-West S with the automatic Newey-West (1994)
lag; standard GMM formulas with a = D'W:
    Var(theta) = (1/T) (aD)^-1 a S a' (aD)^-1',  Var(g_bar) = (1/T) P S P',
    P = I - D (aD)^-1 a;  chi^2 = g_bar' Var(g_bar)^+ g_bar with K - 2 = 20 d.f.
    (the pseudo-inverse keeps the K - 2 non-zero eigenvalues), over all 22 moments.

Implementation choices: the estimate is found numerically (coarse grid over (b, mu), then a
local Nelder-Mead / BFGS polish), and the Jacobian D is computed by central finite
differences. The script checks the first-order condition D' W g_bar = 0 at the estimate.

Outputs (paths relative to "Pset 2"): output/q4b_gmm.csv, output/q4b_gmm_table.md

The GMM helpers take an optional moment function `mom` (default: the 4(b) moments);
code/q4c.py reuses them with its own moments.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chi2

from q2a import OUT_DIR, newey_west_s, nw1994_lag
from q3c import load_eq
from q3e import annual_excess_returns

SAMPLE = pd.period_range("1940-12", "2021-12", freq="M")
B_GRID = np.linspace(-20.0, 20.0, 401)
MU_GRID = np.linspace(0.8, 1.4, 301)


def load_inputs() -> tuple[np.ndarray, pd.DataFrame]:
    df = load_eq().loc[SAMPLE]
    xp = annual_excess_returns(SAMPLE)
    X = pd.concat([df["xRw"].rename("xR_w"), xp], axis=1)
    assert X.notna().all().all() and len(X) == len(SAMPLE)
    return df["Rw"].to_numpy(), X


def moments(theta: np.ndarray, rw: np.ndarray, X: np.ndarray) -> np.ndarray:
    b, mu = theta
    m = 1.0 - b * (rw - mu)
    return np.column_stack([m[:, None] * X, rw - mu])


def g_bar(theta, rw, X, mom=None):
    return (mom or moments)(np.asarray(theta, float), rw, X).mean(axis=0)


def jacobian(theta, rw, X, h=1e-6, mom=None) -> np.ndarray:
    cols = []
    for k in range(len(theta)):
        e = np.zeros(len(theta)); e[k] = h
        cols.append((g_bar(theta + e, rw, X, mom) - g_bar(theta - e, rw, X, mom)) / (2 * h))
    return np.column_stack(cols)


def gmm_estimate(rw, X, W) -> np.ndarray:
    obj = lambda th: float(g_bar(th, rw, X) @ W @ g_bar(th, rw, X))
    grid = np.array([[obj((b, mu)) for mu in MU_GRID] for b in B_GRID])
    i, j = np.unravel_index(np.argmin(grid), grid.shape)
    assert 0 < i < len(B_GRID) - 1 and 0 < j < len(MU_GRID) - 1, "grid minimum on boundary"
    x0 = np.array([B_GRID[i], MU_GRID[j]])
    r1 = minimize(obj, x0, method="Nelder-Mead",
                  options=dict(xatol=1e-12, fatol=1e-22, maxiter=40000))
    r2 = minimize(obj, r1.x, method="BFGS", options=dict(gtol=1e-14))
    return r2.x if r2.fun <= r1.fun else r1.x


def centered_nw_s(theta, rw, X, mom=None):
    g = (mom or moments)(np.asarray(theta, float), rw, X)
    gc = g - g.mean(axis=0)
    L = nw1994_lag(gc)
    return newey_west_s(gc, L), L


def gmm_inference(theta, rw, X, W, S, mom=None) -> dict:
    T = len(rw)
    gb = g_bar(theta, rw, X, mom)
    K, P = len(gb), len(theta)
    D = jacobian(theta, rw, X, mom=mom)
    a = D.T @ W
    ad_inv = np.linalg.inv(a @ D)
    V = ad_inv @ a @ S @ a.T @ ad_inv.T / T
    Pm = np.eye(K) - D @ ad_inv @ a
    var_g = Pm @ S @ Pm.T / T
    evals, evecs = np.linalg.eigh(var_g)
    keep = np.argsort(evals)[P:]
    stat = float(gb @ ((evecs[:, keep] / evals[keep]) @ evecs[:, keep].T) @ gb)
    se_g = np.sqrt(np.diag(var_g))
    ev = np.sort(evals)
    return dict(theta=theta, se=np.sqrt(np.diag(V)), gbar=gb, se_g=se_g, t_g=gb / se_g,
                chi2=stat, df=K - P, p=float(chi2.sf(stat, K - P)), T=T, K=K,
                foc=a @ gb, eig=(ev[P - 1] / ev[-1], ev[P] / ev[-1]))


def write_table(prefix: str, res: dict, labels: list, L: int, weighting: str) -> None:
    names = ["b", "mu"]
    rows = [{"quantity": n, "estimate": v, "std_error": s, "t_stat": v / s}
            for n, v, s in zip(names, res["theta"], res["se"])]
    rows += [{"quantity": lab, "estimate": v, "std_error": s, "t_stat": t}
             for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    rows.append({"quantity": f"chi2({res['df']})", "estimate": res["chi2"], "p_value": res["p"]})
    pd.DataFrame(rows).to_csv(OUT_DIR / f"{prefix}_gmm.csv", index=False)

    md = ["| | Estimate | Std. error | t-stat |", "|---|---:|---:|---:|"]
    md += [f"| {lab} | {v:.4f} | {s:.4f} | {v / s:.2f} |"
           for lab, v, s in zip(["$b$", r"$\mu = E[R_w]$"], res["theta"], res["se"])]
    md += [f"| {lab} | {v:.5f} | {s:.5f} | {t:.2f} |"
           for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    p_txt = f"= {res['p']:.4f}" if res["p"] >= 1e-4 else "< 0.0001"
    md += ["", f"$\\chi^2$ test that the moment conditions are jointly zero (all {res['K']} moments): "
               f"$\\chi^2({res['df']}) = {res['chi2']:.3f}$, p-value {p_txt}.", "",
           f"{weighting}; $M_t = 1 - b(R_{{w,t}} - \\mu)$ with $\\mu$ estimated jointly from "
           f"$\\hat E[R_{{w,t}} - \\mu] = 0$. Monthly observations of annual returns, "
           f"{SAMPLE[0].strftime('%Y:%m')}–{SAMPLE[-1].strftime('%Y:%m')} (T = {res['T']}); "
           f"BM/MOM excess returns are 12-month compounded nominal returns minus the 12-month "
           f"compounded RF. Newey-West (1987, 1994) S (centered) with automatic lag L = {L}."]
    (OUT_DIR / f"{prefix}_gmm_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def labels_for(X: pd.DataFrame) -> list:
    labs = [r"Pricing error: $\hat E[M_t\, xR_{w,t}]$"]
    labs += [rf"Pricing error: $\hat E[M_t\, xR_{{p,t}}]$, {c}" for c in X.columns[1:]]
    labs.append(r"Mean moment: $\hat E[R_{w,t} - \mu]$")
    return labs


def main() -> None:
    rw, Xdf = load_inputs()
    X = Xdf.to_numpy()
    W = np.eye(X.shape[1] + 1)
    theta = gmm_estimate(rw, X, W)
    S, L = centered_nw_s(theta, rw, X)
    res = gmm_inference(theta, rw, X, W, S)
    write_table("q4b", res, labels_for(Xdf), L, "GMM with identity weighting matrix on all 22 moments")

    print(f"T = {res['T']}, K = {res['K']}, NW lag L = {L}; sample mean of R_w = {rw.mean():.6f}")
    print(f"b = {theta[0]:.6f} (s.e. {res['se'][0]:.6f}); mu = {theta[1]:.6f} (s.e. {res['se'][1]:.6f})")
    print(f"FOC D'W g_bar = {np.array2string(res['foc'], precision=2)}")
    print(f"chi2({res['df']}) = {res['chi2']:.4f}, p = {res['p']:.2e}; "
          f"eigen ratios (P-th smallest, next) = {res['eig'][0]:.1e}, {res['eig'][1]:.1e}")
    print("g_bar:", np.array2string(res["gbar"], precision=5))
    print("t    :", np.array2string(res["t_g"], precision=2))


if __name__ == "__main__":
    main()
