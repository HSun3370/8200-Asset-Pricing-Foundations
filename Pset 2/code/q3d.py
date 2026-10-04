"""
Pset 2, Question 3(d) -- two-step GMM version of Question 3(c).

Student specification (as given, 2026-10-04): "everything keeps the same, but use two
step GMM."

  * Same moments, data, sample (1940:12 to 2021:12), z_t and Newey-West settings as
    Q3(c) (see code/q3c.py).
  * Step 1 is Q3(c) (identity weighting). Step 2 minimises g_bar' S1^{-1} g_bar, with S1 the
    centered Newey-West S at the step-1 estimate.
  * Decision made by the student when AI flagged it (2026-10-04): for the standard error,
    the pricing-error t-stats and the chi^2 test, S is re-estimated (centered, with its
    own automatic lag) at the step-2 estimate, and the general formulas of code/q3c.py are
    used with W = S1^{-1}.

Outputs (paths relative to "Pset 2"): output/q3d_gmm.csv, output/q3d_gmm_table.md
"""

import numpy as np

from q3c import (MANAGED_LABELS, centered_nw_s, gmm_gamma, gmm_inference, load_eq,
                 managed_moments, print_result, write_table)


def main() -> None:
    rw, X, _ = managed_moments(load_eq())
    rw_, X_ = rw.to_numpy(), X.to_numpy()

    gamma1 = gmm_gamma(rw_, X_, np.eye(X_.shape[1]))
    S1, L1 = centered_nw_s(gamma1, rw_, X_)
    W2 = np.linalg.inv(S1)

    gamma2 = gmm_gamma(rw_, X_, W2)
    S2, L2 = centered_nw_s(gamma2, rw_, X_)
    res = gmm_inference(gamma2, rw_, X_, W2, S2)
    write_table("q3d", res, MANAGED_LABELS, X.index, L2,
                f"Two-step GMM, second step weighted by the inverse of the Q3(c) S (lag {L1})")
    print(f"step 1 gamma = {gamma1:.6f} (L = {L1})")
    print_result("3(d)", res, L2)
    gb = res["gbar"]
    print(f"  J with S2: T g' S2^-1 g = {res['T'] * gb @ np.linalg.solve(S2, gb):.4f}")


if __name__ == "__main__":
    main()
