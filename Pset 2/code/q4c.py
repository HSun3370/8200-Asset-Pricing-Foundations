"""
Pset 2, Question 4(c) -- efficient (two-step) GMM estimate of b in the linear SDF
M_t = 1 - b (R_w,t - E[R_w]) from E[M_t xR_t] = 0.

Student specification (as given, 2026-10-24): "compute for question 4c", i.e. repeat
Question 4(b) with efficient GMM.

Decisions made by the student when AI flagged them (2026-10-24):
  * E[R_w] is fixed at the sample mean of R_w (treated as known), matching the student's
    4(c) derivation; 21 moments g_t = (1 - b (R_w,t - Rbar_w)) xR_t; one parameter b.
  * Two-step efficient GMM. Step 1: identity weighting. Step 2: W = S1^{-1}, with S1 the
    centered Newey-West S at the step-1 estimate. For the standard error, pricing-error
    t-stats and the chi^2 test, S is re-estimated (centered, own automatic lag) at the
    step-2 estimate and the general formulas are used with W = S1^{-1} (the 3(d) choice).
  * Sample 1940:12 to 2021:12; same assets as 4(b) (xR_w + 20 BM/MOM 12-month
    compounded excess returns).
Carried over: centered Newey-West S with the automatic Newey-West (1994) lag; GMM
formulas and chi^2 test (K - 1 = 20 d.f.) as in code/q4b.py.

Implementation: b is found numerically (grid over [-50, 50], step 0.01, then a bounded
scalar minimisation), and D by finite differences (q4b helpers). The student's analytical
expression is not implemented here; it can be checked against this estimate once written.

Outputs (paths relative to "Pset 2"): output/q4c_gmm.csv, output/q4c_gmm_table.md
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

from q2a import OUT_DIR
from q4b import SAMPLE, centered_nw_s, g_bar, gmm_inference, load_inputs

B_GRID = np.linspace(-50.0, 50.0, 10001)


def moments_fixed_mu(theta: np.ndarray, rw: np.ndarray, X: np.ndarray) -> np.ndarray:
    """g_t(b) = (1 - b (R_w,t - Rbar_w)) xR_t, with Rbar_w the sample mean (held fixed)."""
    m = 1.0 - theta[0] * (rw - rw.mean())
    return m[:, None] * X


def estimate_b(rw, X, W) -> float:
    obj = lambda b: float(g_bar([b], rw, X, moments_fixed_mu) @ W @ g_bar([b], rw, X, moments_fixed_mu))
    vals = np.array([obj(b) for b in B_GRID])
    k = int(np.argmin(vals))
    assert 0 < k < len(B_GRID) - 1, "grid minimum on boundary"
    r = minimize_scalar(obj, bounds=(B_GRID[k - 1], B_GRID[k + 1]), method="bounded",
                        options={"xatol": 1e-12})
    return float(r.x)


def main() -> None:
    rw, Xdf = load_inputs()
    X = Xdf.to_numpy()
    K = X.shape[1]

    b1 = estimate_b(rw, X, np.eye(K))
    S1, L1 = centered_nw_s(np.array([b1]), rw, X, moments_fixed_mu)
    W2 = np.linalg.inv(S1)
    b2 = estimate_b(rw, X, W2)
    S2, L2 = centered_nw_s(np.array([b2]), rw, X, moments_fixed_mu)
    res = gmm_inference(np.array([b2]), rw, X, W2, S2, moments_fixed_mu)

    labels = [r"Pricing error: $\hat E[M_t\, xR_{w,t}]$"]
    labels += [rf"Pricing error: $\hat E[M_t\, xR_{{p,t}}]$, {c}" for c in Xdf.columns[1:]]
    b, se = res["theta"][0], res["se"][0]
    rows = [{"quantity": "b", "estimate": b, "std_error": se, "t_stat": b / se},
            {"quantity": "b_step1_identity", "estimate": b1}]
    rows += [{"quantity": lab, "estimate": v, "std_error": s, "t_stat": t}
             for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    rows.append({"quantity": f"chi2({res['df']})", "estimate": res["chi2"], "p_value": res["p"]})
    pd.DataFrame(rows).to_csv(OUT_DIR / "q4c_gmm.csv", index=False)

    md = ["| | Estimate | Std. error | t-stat |", "|---|---:|---:|---:|",
          f"| $b$ | {b:.4f} | {se:.4f} | {b / se:.2f} |"]
    md += [f"| {lab} | {v:.5f} | {s:.5f} | {t:.2f} |"
           for lab, v, s, t in zip(labels, res["gbar"], res["se_g"], res["t_g"])]
    p_txt = f"= {res['p']:.4f}" if res["p"] >= 1e-4 else "< 0.0001"
    md += ["", f"$\\chi^2$ test that the pricing errors are jointly zero: "
               f"$\\chi^2({res['df']}) = {res['chi2']:.3f}$, p-value {p_txt}.", "",
           f"Efficient (two-step) GMM: first step with identity weighting ($\\hat b_1 = {b1:.4f}$), "
           f"second step weighted by the inverse of the first-step S (lag {L1}); "
           f"$M_t = 1 - b(R_{{w,t}} - \\bar R_w)$ with $E[R_w]$ set to the sample mean "
           f"$\\bar R_w = {rw.mean():.4f}$ and treated as known. Monthly observations of annual returns, "
           f"{SAMPLE[0].strftime('%Y:%m')}–{SAMPLE[-1].strftime('%Y:%m')} (T = {res['T']}). "
           f"Newey-West (1987, 1994) S (centered) re-estimated at $\\hat b$ with automatic lag L = {L2}."]
    (OUT_DIR / "q4c_gmm_table.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Rbar_w = {rw.mean():.6f}; step 1 b = {b1:.6f} (L = {L1}); step 2 b = {b2:.6f} (s.e. {se:.6f}, L = {L2})")
    print(f"FOC D'W g_bar = {res['foc'][0]:.2e}; chi2({res['df']}) = {res['chi2']:.4f}, p = {res['p']:.2e}; "
          f"eigen ratios = {res['eig'][0]:.1e}, {res['eig'][1]:.1e}")


if __name__ == "__main__":
    main()
