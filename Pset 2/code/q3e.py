"""
Pset 2, Question 3(e) -- Question 3(c) with the 20 BM and MOM decile portfolios added to
the moment conditions.

Student specification (as given, 2026-10-04): "for the excess return, add the excess
returns from 10 BM portfolio and 10 mom portfolios, so you need to use the time period
both have values."

Decisions made by the student when AI flagged them (2026-10-04):
  * Horizon: the BM/MOM excess returns are 12-month compounded nominal excess returns
    ending in month t, matching the annual xR_w,t:
        xR_p,t = prod_{k=0..11} (1 + R_p,t-k) - prod_{k=0..11} (1 + RF_t-k),
    with value-weighted monthly returns and RF from the Ken French files (as in Q2).
  * Moments (22): the two Q3(c) moments (xR_w and z_{t-1} xR_w) plus the 20 portfolios:
        E[R_w,t^(-gamma) xR_t] = 0,  xR_t = [xR_w, z_{t-1} xR_w, 10 BM, 10 MOM].
  * Sample: months where all moments are available, 1940:12 to 2021:12 (z starts 1940:12;
    the EQ data end 2021:12).
Carried over from Q3(c) ("repeat"): identity weighting matrix; z_t and sigma^2_e as in
code/q3c.py; centered Newey-West S with the automatic lag; chi^2 test with K - 1 = 21
degrees of freedom.

Outputs (paths relative to "Pset 2"): output/q3e_gmm.csv, output/q3e_gmm_table.md
"""

import numpy as np
import pandas as pd

from q2a import DECILES, FF_CSV, PORT_CSV, read_french_block
from q2b import MOM_CSV, MOM_DECILES
from q3c import (H, MANAGED_LABELS, centered_nw_s, gmm_gamma, gmm_inference, load_eq,
                 managed_moments, print_result, write_table)

VW_BLOCK = "Value Weight Returns -- Monthly"


def annual_excess_returns(index: pd.PeriodIndex) -> pd.DataFrame:
    """12-month compounded excess returns ending in each month of `index` (decimals)."""
    port = pd.concat([read_french_block(PORT_CSV, VW_BLOCK)[DECILES].add_prefix("BM "),
                      read_french_block(MOM_CSV, VW_BLOCK)[MOM_DECILES].add_prefix("MOM ")],
                     axis=1, join="inner")
    rf = read_french_block(FF_CSV, "")["RF"]
    first = index[0] - (H - 1)
    full = pd.period_range(first, index[-1], freq="M")
    port, rf = port.reindex(full), rf.reindex(full)
    assert port.notna().all().all() and rf.notna().all(), "French data missing in window"
    assert (port > -99.99).all().all(), "missing-value code in window"
    gross_p = (1 + port / 100).rolling(H).apply(np.prod, raw=True)
    gross_f = (1 + rf / 100).rolling(H).apply(np.prod, raw=True)
    return gross_p.sub(gross_f, axis=0).loc[index]


def main() -> None:
    rw, X2, _ = managed_moments(load_eq())
    xp = annual_excess_returns(X2.index)
    X = pd.concat([X2, xp], axis=1)
    assert X.notna().all().all() and len(X) == len(X2)
    K = X.shape[1]

    rw_, X_ = rw.to_numpy(), X.to_numpy()
    W = np.eye(K)
    gamma = gmm_gamma(rw_, X_, W)
    S, L = centered_nw_s(gamma, rw_, X_)
    res = gmm_inference(gamma, rw_, X_, W, S)
    labels = MANAGED_LABELS + [rf"$\hat E[R_{{w,t}}^{{-\gamma}} xR_{{p,t}}]$, {c}" for c in xp.columns]
    write_table("q3e", res, labels, X.index, L,
                "GMM with identity weighting matrix; BM/MOM excess returns are 12-month "
                "compounded nominal returns minus the 12-month compounded RF (Ken French)")
    print_result("3(e)", res, L)


if __name__ == "__main__":
    main()
