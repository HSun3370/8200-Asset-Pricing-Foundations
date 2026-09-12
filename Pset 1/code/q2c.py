"""
Pset 1, Question 2(c) -- Amihud and Hurvich (2004) estimate of b in the
one-year-ahead predictive regression of the excess equity return on D/P.

Student specification (as given; decisions recorded 2026-09-12):
  Variables, as in Q2(a)/(b):  xR_t = exp(re_t) - exp(rf_t),  (D/P)_t = exp(dp_t).
  Timing: overlapping monthly regressions with "t+1" one year after t, i.e. the row
  12 months ahead (October 1991 on October 1990, November 1991 on November 1990, ...).

  1. OLS   (D/P)_{t+1} = theta_hat + phi_hat * (D/P)_t + eps_{t+1}
           theta_hat = intercept, phi_hat = slope (problem-set notation, chosen by the
           student after AI flagged that the prompt swapped the two symbols).
  2. Bias-corrected slope
           phi_c = phi_hat + (1/T)(1 + 3 phi_hat) + (3/T^2)(1 + 3 phi_hat),
           T = number of distinct calendar years in the dataset's YEAR column
           (1927-2021, so T = 95; student's decision).
  3. Bias-corrected residuals
           u_c_{t+1} = (D/P)_{t+1} - (theta_hat + phi_c * (D/P)_t).
  4. OLS   xR_{t+1} = a + b (D/P)_t + b_u u_c_{t+1} + eps_{t+1}.

Steps 1 and 4 use the same observations (every month t with both (D/P)_{t+1} and
xR_{t+1} available), which is also the Q2(b) sample. The Q2(b) slope from the
regression without u_c is printed alongside for reference. No standard errors are
computed (not required for Q2(c)).

Output: output/q2c_amihud_hurvich.csv (path relative to "Pset 1").
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

from q2b import DATA_CSV, MONTHS_PER_YEAR, OUT_DIR, load_data


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    """(D/P)_t, (D/P)_{t+1 year}, xR_{t+1 year}; rows kept only if all three exist."""
    xr = np.exp(df["re"]) - np.exp(df["rf"])
    dp_level = np.exp(df["dp"])
    return pd.DataFrame(
        {
            "dp_t": dp_level,
            "dp_t1": dp_level.shift(-MONTHS_PER_YEAR),
            "xr_t1": xr.shift(-MONTHS_PER_YEAR),
        }
    ).dropna()


def main() -> None:
    df = load_data(DATA_CSV)
    s = build_sample(df)
    n = len(s)
    T_years = int(df["YEAR"].nunique())

    dp_t = s["dp_t"].to_numpy()
    dp_t1 = s["dp_t1"].to_numpy()
    xr_t1 = s["xr_t1"].to_numpy()
    X = sm.add_constant(dp_t)                              # [1, (D/P)_t]

    # 1. AR(1) for D/P: intercept theta_hat, slope phi_hat
    theta_hat, phi_hat = sm.OLS(dp_t1, X).fit().params

    # 2. bias-corrected slope
    phi_c = (
        phi_hat
        + (1 + 3 * phi_hat) / T_years
        + 3 * (1 + 3 * phi_hat) / T_years**2
    )

    # 3. bias-corrected residuals
    u_c = dp_t1 - (theta_hat + phi_c * dp_t)

    # 4. predictive regression augmented with u_c
    X4 = np.column_stack([np.ones(n), dp_t, u_c])
    a_hat, b_hat, bu_hat = sm.OLS(xr_t1, X4).fit().params

    # reference: Q2(b) slope on the same sample, without u_c
    b_q2b = sm.OLS(xr_t1, X).fit().params[1]

    res = pd.DataFrame(
        [
            ("n_obs", n),
            ("T_years", T_years),
            ("theta_hat", theta_hat),
            ("phi_hat", phi_hat),
            ("phi_c", phi_c),
            ("a_hat", a_hat),
            ("b_hat", b_hat),
            ("b_u_hat", bu_hat),
            ("b_q2b_reference", b_q2b),
        ],
        columns=["parameter", "value"],
    )
    csv_path = OUT_DIR / "q2c_amihud_hurvich.csv"
    res.to_csv(csv_path, index=False)

    print(f"Sample             : n = {n} monthly obs, {s.index[0]} .. {s.index[-1]}")
    print(f"T (years)          : {T_years}")
    print()
    print("Step 1  (D/P)_{t+1} = theta + phi (D/P)_t")
    print(f"  theta_hat        : {theta_hat:.6f}")
    print(f"  phi_hat          : {phi_hat:.6f}")
    print("Step 2  bias-corrected slope")
    print(f"  phi_c            : {phi_c:.6f}")
    print("Step 3  u_c_{t+1} = (D/P)_{t+1} - (theta_hat + phi_c (D/P)_t)")
    print(f"  mean, sd of u_c  : {u_c.mean():.6f}, {u_c.std(ddof=0):.6f}")
    print("Step 4  xR_{t+1} = a + b (D/P)_t + b_u u_c_{t+1}")
    print(f"  a_hat            : {a_hat:.6f}")
    print(f"  b_hat            : {b_hat:.6f}")
    print(f"  b_u_hat          : {bu_hat:.6f}")
    print()
    print(f"Reference: Q2(b) b_hat (no u_c, same sample) = {b_q2b:.6f}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
