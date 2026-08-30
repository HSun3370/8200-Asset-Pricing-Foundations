"""
Pset 1, Question 1(d) -- H -> infinity limit of the Q1(c) VAR-implied decomposition.

Same VAR(1), b_z, and kappa as Q1(c) (imported from q1c.py so the estimate is identical).
Taking H -> infinity, kappa^H F^H -> 0 for the stationary estimated F, so

    M_inf         = F (I - kappa F)^{-1}      ( = lim_H (F - kappa^H F^{H+1})(I - kappa F)^{-1}
                                                 = sum_{j>=1} kappa^{j-1} F^j )
    b_re^(inf)      =  e_re' M_inf b_z
    b_Delta d^(inf) = -e_dg' M_inf b_z
    b_dp^(inf)      =  1 - b_re^(inf) - b_Delta d^(inf)   (imposed, as in Q1(c);
                                                           Eq. 1.6 gives the theoretical 0)

Prints the three numbers as a Markdown table plus the Eq. 1.6 consistency check.
"""

import numpy as np

from q1c import DATA_CSV, VARS, b_z_from_data, estimate_var, load_data


def main() -> None:
    df = load_data(DATA_CSV)
    dp_bar = df["dp"].mean()
    kappa = 1.0 / (1.0 + np.exp(dp_bar))

    _intercept, F, _Sigma, n_var = estimate_var(df)
    b_z = b_z_from_data(df)

    I3 = np.eye(3)
    e = {name: I3[k] for k, name in enumerate(VARS)}
    M_inf = F @ np.linalg.inv(I3 - kappa * F)

    b_re = float(e["re"] @ M_inf @ b_z)
    b_dg = float(-e["dg"] @ M_inf @ b_z)
    b_dp = 1.0 - b_re - b_dg
    eig_mod = np.abs(np.linalg.eigvals(F))

    print(f"kappa = {kappa:.6f}   VAR obs = {n_var}   eig|F| = {np.round(eig_mod, 4)}")
    print()
    print("| term | H -> infinity value |")
    print("|---|---|")
    print(f"| $b_{{re}}^{{(\\infty)}}$ | {b_re:.4f} |")
    print(f"| $b_{{\\Delta d}}^{{(\\infty)}}$ | {b_dg:.4f} |")
    print(f"| $b_{{dp}}^{{(\\infty)}} = 1 - b_{{re}}^{{(\\infty)}} - b_{{\\Delta d}}^{{(\\infty)}}$ | {b_dp:.4f} |")
    print()
    print(f"Eq. 1.6 check:  b_re^(inf) + b_Delta d^(inf) = {b_re + b_dg:.4f}   (theoretical: 1)")


if __name__ == "__main__":
    main()
