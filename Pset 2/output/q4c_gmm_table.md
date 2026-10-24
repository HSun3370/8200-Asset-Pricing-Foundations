| | Estimate | Std. error | t-stat |
|---|---:|---:|---:|
| $b$ | 6.9259 | 0.7717 | 8.97 |
| Pricing error: $\hat E[M_t\, xR_{w,t}]$ | -0.10412 | 0.02866 | -3.63 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM Lo 10 | -0.12863 | 0.03583 | -3.59 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 2-Dec | -0.10186 | 0.02876 | -3.54 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 3-Dec | -0.10226 | 0.02803 | -3.65 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 4-Dec | -0.09644 | 0.02779 | -3.47 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 5-Dec | -0.08322 | 0.02593 | -3.21 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 6-Dec | -0.07701 | 0.02614 | -2.95 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 7-Dec | -0.09364 | 0.03360 | -2.79 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 8-Dec | -0.07943 | 0.02695 | -2.95 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM 9-Dec | -0.07497 | 0.02635 | -2.85 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, BM Hi 10 | -0.10436 | 0.03312 | -3.15 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM Lo PRIOR | -0.26846 | 0.05692 | -4.72 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 2 | -0.16333 | 0.04275 | -3.82 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 3 | -0.13040 | 0.03468 | -3.76 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 4 | -0.10574 | 0.02958 | -3.57 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 5 | -0.09261 | 0.02453 | -3.78 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 6 | -0.09967 | 0.02721 | -3.66 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 7 | -0.08839 | 0.02432 | -3.63 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 8 | -0.08172 | 0.02582 | -3.16 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM PRIOR 9 | -0.08233 | 0.02976 | -2.77 |
| Pricing error: $\hat E[M_t\, xR_{p,t}]$, MOM Hi PRIOR | -0.07182 | 0.03257 | -2.21 |

$\chi^2$ test that the pricing errors are jointly zero: $\chi^2(20) = 70.871$, p-value < 0.0001.

Efficient (two-step) GMM: first step with identity weighting ($\hat b_1 = 3.2860$), second step weighted by the inverse of the first-step S (lag 24); $M_t = 1 - b(R_{w,t} - \bar R_w)$ with $E[R_w]$ set to the sample mean $\bar R_w = 1.0870$ and treated as known. Monthly observations of annual returns, 1940:12–2021:12 (T = 973). Newey-West (1987, 1994) S (centered) re-estimated at $\hat b$ with automatic lag L = 22.
