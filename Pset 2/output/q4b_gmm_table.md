| | Estimate | Std. error | t-stat |
|---|---:|---:|---:|
| $b$ | 2.8559 | 0.5908 | 4.83 |
| $\mu = E[R_w]$ | 1.0360 | 0.0191 | 54.12 |
| Pricing error: $\hat E[M_t\, xR_{w,t}]$ | -0.00428 | 0.00396 | -1.08 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM Lo 10 | -0.01603 | 0.01070 | -1.50 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 2-Dec | 0.00005 | 0.00641 | 0.01 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 3-Dec | -0.00380 | 0.00542 | -0.70 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 4-Dec | -0.00004 | 0.00545 | -0.01 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 5-Dec | 0.01095 | 0.00609 | 1.80 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 6-Dec | 0.01653 | 0.00617 | 2.68 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 7-Dec | 0.00449 | 0.00916 | 0.49 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 8-Dec | 0.02295 | 0.00824 | 2.79 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 9-Dec | 0.03055 | 0.00892 | 3.43 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM Hi 10 | 0.02156 | 0.01311 | 1.64 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM Lo PRIOR | -0.10145 | 0.01049 | -9.67 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 2 | -0.04078 | 0.00803 | -5.08 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 3 | -0.02025 | 0.00764 | -2.65 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 4 | -0.00527 | 0.00622 | -0.85 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 5 | -0.00033 | 0.00649 | -0.05 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 6 | -0.00015 | 0.00486 | -0.03 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 7 | 0.00618 | 0.00650 | 0.95 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 8 | 0.01682 | 0.00462 | 3.64 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 9 | 0.02082 | 0.00669 | 3.11 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM Hi PRIOR | 0.04557 | 0.01067 | 4.27 |
| Mean moment: $\hat E[R_{w,t} - \mu]$ | 0.05098 | 0.00498 | 10.24 |

$\chi^2$ test that the moment conditions are jointly zero (all 22 moments): $\chi^2(20) = 323.659$, p-value < 0.0001.

GMM with identity weighting matrix on all 22 moments; $M_t = 1 - b(R_{w,t} - \mu)$ with $\mu$ estimated jointly from $\hat E[R_{w,t} - \mu] = 0$. Monthly observations of annual returns, 1940:12–2021:12 (T = 973); BM/MOM excess returns are 12-month compounded nominal returns minus the 12-month compounded RF. Newey-West (1987, 1994) S (centered) with automatic lag L = 24.
