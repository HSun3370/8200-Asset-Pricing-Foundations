# Problem Set 1

**BUSFIN 8200: Asset Pricing Foundations**

## Problem Set Rules

- Your problem set solution must be delivered in the form of a typed report in PDF (not handwritten).
- You must also provide a Git repository with all your files and results. It includes the source files used to generate the PDF (e.g., the `.tex` script) as well as all coding scripts used to produce the results (e.g., the `.R` or `.py` scripts). The instructor needs to be able to reproduce your results and PDF from the source files in your Git repository.
- You are allowed to consult any material while working on the problem set (except solutions created by individuals not currently taking the course).
- You are allowed to talk with anyone while working on your problem set. In particular, the instructor highly recommends that you talk with your classmates about the problem set. Research requires collaboration. It is fine if you exchange information and even jointly produce parts of the problem set codes/derivations. However, you have to submit your own solutions.
- Do not abuse the rule above. While you can work together to produce the problem set solution (or even use the solution of a classmate as a starting point in developing your own solution), you cannot simply copy a question's solution from a classmate.
- You can also use AI when working on your problem set. However, you need to follow the rules in the "BUSFIN 8200 Problem Sets: AI Policy" document.

## Datasets

### EQ Dataset (for Questions 1 and 2)

The file `EQ Dataset.csv` has the following columns:

- **YEAR**: the year associated with the observation
- **MONTH**: the month associated with the observation
- **dp**: the log of the dividend-to-price ratio ($dp_t = \log(D_t/P_t)$), with $D_t$ reflecting the sum of the dividends paid by the total US equity market (i.e., firms available on CRSP) over the 12 months ending in month $t$. Dividends account for M&A paid in cash following the procedure described in Gonçalves (2021a).
- **dg**: the log of the annual dividend growth ($\Delta d_t = \log(D_t/D_{t-12})$), with $D_t$ reflecting the sum of the dividends paid by the total US equity market (i.e., firms available on CRSP) over the 12 months ending in month $t$. Dividends account for M&A paid in cash following the procedure described in Gonçalves (2021a).
- **rf**: the log of the annual (deflated) risk-free return ($r_{f,t} = \log(R_{f,t})$) ending in the given month.
- **re**: the log of the annual (deflated) equity market return ($r_{e,t} = \log(R_{e,t})$) ending in the given month.

**Note:** the dataset contains monthly observations of annual variables. So, the empirical analyses in Questions 1 and 2 have to be done accordingly.

### CZ Dataset (for Question 3)

Download the firm-level signal dataset from Chen and Zimmermann (2022) (available at [openassetpricing.com](https://www.openassetpricing.com/)), referred to as the "CZ Dataset" in this problem set. For Question 3, you only need the columns:

- `permno` — the CRSP stock identifier
- `yyyymm` — the month identifier
- `Mom12m` — the stock return from month $\tau - 12$ to month $\tau - 1$, from Jegadeesh and Titman (1993)
- `BMdec` — the log of the book-to-market ratio, from Fama and French (1992)
- `GP` — the gross profitability variable, from Novy-Marx (2013)

### Dur Dataset (for Question 3)

Download the firm-level equity duration dataset from Gonçalves (2021b) (available at [andreigoncalves.com/published-papers](https://andreigoncalves.com/published-papers/)), referred to as the "Dur Dataset" in this problem set. Merge the CZ Dataset with the Dur Dataset, which contains firm-year equity duration information:

- `PERMNO` — the stock identifier
- `FF.YEAR` — the year identifier
- `Dur` — the equity duration

The timing of the `Dur` variable matches the timing of the `BM` variable (so, it is calculated at the end of June of year $t$ using market equity from December of $t-1$ and accounting information from the end of fiscal year $t-1$).

### Bond Dataset (for Question 4)

Download CRSP Fama-Bliss bond yields from June 1952 to the most recent date for bond strips with maturities from 1 to 5 years.[^1] This file is referred to as the "Bond Dataset" in this problem set.

[^1]: In WRDS, go to CRSP/Annual Update/Treasuries/Fama Bliss Discount Bonds (Monthly Only). Then, download the entire file and obtain bond yields from column `TMYTM`. The `TTERMLBL` column provides the bond description and the `MCALDT` column provides the date. Focus on `TTERMLBL = Fama Bliss Discount Bonds - X-Year (Nominal)` for X from 1 to 5.

---

## Question 1

### 1(a)

Consider the Campbell and Shiller (1989) log-linear (approximate) present value identity for equities ($h$ is in years):

$$
dp_t = \frac{\kappa_0 \cdot (\kappa^H - 1)}{1 - \kappa} + \sum_{h=1}^{H} \kappa^{h-1} \cdot r_{e,t+h} - \sum_{h=1}^{H} \kappa^{h-1} \cdot \Delta d_{t+h} + \kappa^H \cdot dp_{t+H} \tag{1.1}
$$

$$
= \frac{\kappa_0 \cdot (\kappa^H - 1)}{1 - \kappa} + \sum_{h=1}^{H} \kappa^{h-1} \cdot E_t[r_{e,t+h}] - \sum_{h=1}^{H} \kappa^{h-1} \cdot E_t[\Delta d_{t+h}] + \kappa^H \cdot E_t[dp_{t+H}] \tag{1.2}
$$

$$
= \frac{-\kappa_0}{1 - \kappa} + \sum_{h=1}^{\infty} \kappa^{h-1} \cdot E_t[r_{e,t+h}] - \sum_{h=1}^{\infty} \kappa^{h-1} \cdot E_t[\Delta d_{t+h}] \tag{1.3}
$$

where $\kappa = 1/(1 + e^{\overline{dp}})$ and $\kappa_0 = -\log(\kappa) - (1-\kappa)\cdot\log(1/\kappa - 1)$.

Starting from $R_{e,t+1} = (P_{t+1} + D_{t+1})/P_t$, derive the (approximate) Equations 1.1, 1.2, and 1.3. Explain and justify any assumptions you make.

### 1(b)

From Equation 1.1, we have

$$
1 = \underbrace{\frac{\text{Cov}\left[dp_t, \sum_{h=1}^{H} \kappa^{h-1} \cdot r_{e,t+h}\right]}{\text{Var}[dp]}}_{b_{re}^{(H)}} + \underbrace{\frac{\text{Cov}\left[dp_t, -\sum_{h=1}^{H} \kappa^{h-1} \cdot \Delta d_{t+h}\right]}{\text{Var}[dp]}}_{b_{\Delta d}^{(H)}} + \underbrace{\frac{\text{Cov}\left[dp_t, \kappa^H \cdot dp_{t+H}\right]}{\text{Var}[dp]}}_{b_{dp}^{(H)}} \tag{1.4}
$$

Applying Equation 1.4 to the EQ Dataset, reproduce the figure provided on slide 1.8 of the Module 1 lecture notes. This figure has $H$ on the x-axis and $\left(b_{re}^{(H)}, b_{\Delta d}^{(H)}, b_{dp}^{(H)}\right)$ on the y-axis. Explain what the inference from this figure is.

### 1(c)

Now, use Equation 1.4 and the EQ Dataset to reproduce a figure analogous to the one in Question 1(b) but with the terms from Equation 1.4 implied by the VAR (estimated by OLS)

$$
z_{t+1} = \Gamma_0 + \Gamma z_t + \tilde{z}_{t+1} \quad \text{where} \quad \tilde{z}_{t+1} \sim IID(0, \Sigma) \tag{1.5}
$$

where $z_t = [\Delta d_t \;\; r_{e,t} \;\; dp_t]'$.

### 1(d)

Taking $H \to \infty$, Equation 1.4 becomes

$$
1 = \underbrace{\frac{\text{Cov}\left[dp_t, \sum_{h=1}^{\infty} \kappa^{h-1} \cdot r_{e,t+h}\right]}{\text{Var}[dp]}}_{b_{re}^{(\infty)}} + \underbrace{\frac{\text{Cov}\left[dp_t, -\sum_{h=1}^{\infty} \kappa^{h-1} \cdot \Delta d_{t+h}\right]}{\text{Var}[dp]}}_{b_{\Delta d}^{(\infty)}} \tag{1.6}
$$

Using the VAR in Equation 1.5, calculate the values for $b_{re}^{(\infty)}$ and $b_{\Delta d}^{(\infty)}$. Interpret the results.

### 1(e)

Gao and Martin (2021) argue that while the Campbell and Shiller (1989) approximation is accurate on average, it can be inaccurate when $dp_t$ is too far from its mean (which happened at some important historical periods such as the late 1990s). They propose the following alternative log-linear (approximate) present value identity:

$$
dy_t = (1-\kappa) \cdot \left(\sum_{h=1}^{H} \kappa^{h-1} \cdot r_{e,t+h} - \sum_{h=1}^{H} \kappa^{h-1} \cdot \Delta d_{t+h}\right) + \kappa^H \cdot dy_{t+H} \tag{1.7}
$$

$$
= (1-\kappa) \cdot \left(\sum_{h=1}^{H} \kappa^{h-1} \cdot E_t[r_{e,t+h}] - \sum_{h=1}^{H} \kappa^{h-1} \cdot E_t[\Delta d_{t+h}]\right) + \kappa^H \cdot E_t[dy_{t+H}] \tag{1.8}
$$

$$
= (1-\kappa) \cdot \left(\sum_{h=1}^{\infty} \kappa^{h-1} \cdot E_t[r_{e,t+h}] - \sum_{h=1}^{\infty} \kappa^{h-1} \cdot E_t[\Delta d_{t+h}]\right) \tag{1.9}
$$

where $dy_t = \log(1 + D_t/P_t)$ and $\kappa = e^{-\overline{dy}}$.

Starting from $R_{e,t+1} = (P_{t+1} + D_{t+1})/P_t$, derive the (approximate) Equations 1.7, 1.8, and 1.9. Explain and justify any assumptions you make.

> **Hint.** The steps to derive Equation 1.7 are analogous to the steps used to derive Equation 1.1 in Question 1(a):
>
> 1. Show that $r_{e,t+1} - \Delta d_{t+1} = dy_t + \log(1 - e^{-dy_t}) - \log(1 - e^{-dy_{t+1}})$
> 2. Show that a first-order Taylor approximation yields $\log(1 - e^{-dy_t}) \approx \log(1-\kappa) + \left(\kappa/(1-\kappa)\right)\cdot(dy_t - \overline{dy})$
> 3. Substitute the expression from step 2 into the expression from step 1 to obtain $dy_t = (1-\kappa)\cdot(r_{e,t+1} - \Delta d_{t+1}) + \kappa \cdot dy_{t+1}$
> 4. Recursively substitute $dy_{t+h}$

---

## Question 2

### 2(a)

Using the EQ Dataset, estimate the regression (by OLS)

$$
\frac{1}{H} \cdot \sum_{h=1}^{H} xR_{e,t+h} = a^{(H)} + b^{(H)} \cdot D_t/P_t + \varepsilon_t^{(H)} \tag{2.1}
$$

for $H = 1, 2, 3, ..., 14, 15$ years (with $xR_{e,t} = e^{r_{e,t}} - e^{r_{f,t}}$ and $D_t/P_t = e^{dp_t}$). Plot a graph with $H$ on the x-axis and the $R^2_{adj}$ of these regressions on the y-axis. Describe the results you observe.

### 2(b)

Estimate the regression (by OLS)

$$
xR_{e,t+1} = a + b \cdot D_t/P_t + \varepsilon_t \tag{2.2}
$$

but this time also obtain standard errors for $\hat{b}$ using five different methods:

(i) The baseline OLS standard errors
(ii) The White (1980) standard errors
(iii) The Newey and West (1987) standard errors with 11 lags
(iv) The Hansen and Hodrick (1980) standard errors with 11 lags
(v) The Newey and West (1987, 1994) standard errors

The first two methods do not account for autocorrelation. The next two account for autocorrelation up to 11 lags (since $t+1$ is one year ahead of $t$ and we have a monthly dataset, our overlapping regressions induce artificial autocorrelation up to 11 lags). The last one accounts for autocorrelation with a data-driven method to select the number of lags. Report $\hat{b}$ as well as its t-statistic based on each of the five standard error estimation methods above.

> **Note on standard errors.** We discussed standard errors for time-series regressions in class but did not cover the details. However, the implementation of these estimators is simple (and available in standard econometric packages). Let the time index in the dataset be $\tau = 1, 2, ..., T$, representing months (as opposed to $t = 1, 2, ..., T$, representing years). Then, letting $y = xR_e$, $x_\tau = [1, D/P]$, and $\theta = [a, b]$, Equation 2.2 can be written as $y_{\tau \to \tau+H} = \theta' x_\tau + \varepsilon_\tau$ (with $H=12$ in our case). We estimate $\theta$ by OLS and obtain standard errors from
>
> $$
> \widehat{\text{Var}}[\hat{\theta}] = \frac{1}{T} \cdot \left(\frac{1}{T}\sum_{\tau=1}^{T} x_\tau x_\tau'\right)^{-1} \hat{S} \left(\frac{1}{T}\sum_{\tau=1}^{T} x_\tau x_\tau'\right)^{-1}
> $$
>
> with the square root of the diagonal elements of the $2\times2$ matrix $\widehat{\text{Var}}[\hat{\theta}]$ providing the asymptotic standard errors for $\hat{a}$ and $\hat{b}$. $S$ is called the spectral density matrix and is generally given by $S = \sum_{\ell=-\infty}^{\ell=\infty} E[\varepsilon_\tau x_\tau x_{\tau-\ell}' \varepsilon_{\tau-\ell}]$ (we will learn more about $S$ and its estimators in Module 2 when covering the Generalized Method of Moments).
>
> - In the absence of autocorrelation and heteroskedasticity, use $\hat{S}_{OLS} = \hat{\sigma}_\varepsilon^2 \cdot \left(1/T \cdot \sum_{\tau=1}^T x_\tau x_\tau'\right)$ — the baseline OLS estimator.
> - Under heteroskedasticity but no autocorrelation, use $\hat{S}_{White} = 1/T \cdot \sum_{\tau=1}^T \hat{\varepsilon}_\tau x_\tau x_\tau' \hat{\varepsilon}_\tau$ — the White (1980) estimator.
> - If there is autocorrelation and heteroskedasticity, use a HAC estimator of the form $\hat{S}_{HAC} = \hat{\Omega}_0 + \sum_{\ell=1}^{L} w_\ell \cdot \left[\hat{\Omega}_\ell + \hat{\Omega}_\ell'\right]$, where $\hat{\Omega}_\ell = 1/(T-\ell) \cdot \sum_{\tau=\ell+1}^{T} \hat{\varepsilon}_\tau x_\tau x_{\tau-\ell}' \hat{\varepsilon}_{\tau-\ell}$ and $L$ is the number of autocorrelation lags accounted for (see Andrews (1991)).
>   - Newey and West (1987) use the weighting function $w_\ell = 1 - \ell/(L+1)$, the most commonly used HAC estimator, which works well for autocorrelation that arises naturally in the data. Newey and West (1994) recommend $L = \text{const} \cdot T^{1/3}$, with the optimal constant estimator given in their Equation 2.2.
>   - Hansen and Hodrick (1980) propose $w_\ell = 1$ with $L = \text{Overlap} = H - 1$, which better captures the nature of the autocorrelation induced by overlapping regressions (but sometimes leads to a $\widehat{\text{Var}}[\hat\theta]$ that is not positive definite).
>   - Hodrick (1992) points out that if $y_{\tau \to \tau+H}$ reflects the sum of $y_\tau$ from $\tau+1$ to $\tau+H$, then inference using $w_\ell = 1$ with $L = H-1$ is asymptotically equivalent to inference based on a regression of $y_{\tau+1}$ onto $\sum_{\ell=\tau-(H-1)}^{\ell=\tau} x_\ell$, which leads to better finite-sample properties. However, we cannot use the Hodrick (1992) approach here since our $y_{\tau \to \tau+H}$ is an annual return, not the sum of monthly returns (in contrast, if $y_{\tau\to\tau+H}$ were an annual log return, it would be the sum of monthly log returns).

### 2(c)

Reestimate the regression in Equation 2.2 but this time using the method in Amihud and Hurvich (2004).[^2] Report the $b$ estimate obtained in this question and contrast it to the $b$ estimate obtained in Question 2(b). Explain why it is natural for the two estimates to differ.

[^2]: We discussed Amihud and Hurvich (2004) in class but did not cover the details. You can read Section II of Amihud and Hurvich (2004) for the underlying econometrics if you want, but the implementation of their estimator is simple. First, regress $D_{t+1}/P_{t+1}$ on $D_t/P_t$ to obtain (by OLS) the estimated intercept, $\hat\theta$, and the estimated slope, $\hat\phi$. The slope estimate is biased in small samples. You can obtain a bias-corrected slope estimate as $\hat\phi_c = \hat\phi + (1/T)\cdot(1+3\hat\phi) + (1/T^2)\cdot 3\cdot(1+3\hat\phi)$, where $T$ is the total number of years in the dataset, not the total number of months since $t+1$ is one year ahead of $t$. Then, calculate the bias-corrected residual estimates as $\hat{u}_{t+1}^c = D_{t+1}/P_{t+1} - (\hat\theta + \hat\phi_c \cdot D_t/P_t)$. Finally, estimate (by OLS) the regression $xR_{e,t+1} = a + b\cdot D_t/P_t + b_u \cdot \hat{u}_{t+1}^c + \varepsilon_t$ (2.3). We have that $\hat{b}_u$ converges to zero in probability so that $\hat{b}$ converges to $b$ in probability. More importantly, $\hat{b}$ represents an unbiased estimator for $b$ (even in relatively small samples). Amihud and Hurvich (2004) also provide a way to compute standard errors for $\hat{b}$ and to generalize their estimator to multiple predictors. However, in this question you do not need to compute the standard errors and there is only one predictor.

### 2(d)

Estimate the regression in Equation 2.2 again, but this time using out-of-sample (OS) estimation with an expanding window (i.e., using time-varying $a_t$ and $b_t$ estimated with historical data). Initiate your OS estimation in December 1940 (i.e., $D_t/P_t$ in December 1939 and $xR_{e,t+1}$ in December 1940). Label the historical (expanding window) mean as $\overline{xR}_{e,t}$, the fitted values from Question 2(b) as $\hat{E}_t^{IS}[xR_e]$, and the OS forecasts from this question as $\hat{E}_t^{OS}[xR_e]$. Plot the time series of $\overline{xR}_{e,t}$, $\hat{E}_t^{IS}[xR_e]$, and $\hat{E}_t^{OS}[xR_e]$ from December 1940 to the end of the sample. Then, calculate and report the $R^2_{OS}$ value using the forecasting errors from December 1940 to the end of the sample (note that we calculate $R^2_{OS}$ instead of $R^2_{adj,OS}$ because a degree-of-freedom adjustment is not needed in an OS analysis).

Now, to understand how $R^2_{OS}$ varies over time, calculate $R^2_{OS}$ using a 50-year rolling window for the forecasting errors (without modifying the $a_t$ and $b_t$ calculations) and provide a time-series plot of these $R^2_{OS}$ values (note that the time series will start in December 1990 and end at the end of your sample). A 50-year rolling window is used instead of a shorter window because a lot of data is needed to calculate meaningful $R^2_{OS}$ values (otherwise they pick up a lot of noise).

### 2(e)

Repeat Question 2(d). However, this time estimate the OS coefficients using $\hat{a}_t = G_t - 1$ and $\hat{b}_t = G_t$ when obtaining $\hat{E}_t^{OS}[xR_e]$, where $G_t$ is the historical (expanding window) average of $e^{\Delta d_t}$ over the same sample used to calculate $\overline{xR}_{e,t}$. These restrictions on $a_t$ and $b_t$ are motivated by a steady-state valuation model (with 0% real interest rate), which implies $E[xR_e] = (G-1) + G \cdot D/P$.[^3]

[^3]: This steady-state valuation model is not as unrealistic as it seems. For instance, if dividend growth is unpredictable and expected returns are 100% persistent (i.e., $E_t[\Delta d_{t+h}] = g$ and $E_t[r_{e,t+h}] = E_t[r_e]$), then Equation 1.9 implies $\log(1+D_t/P_t) = E_t[r_e] - g$, which is equivalent to $e^{E_t[r_e]} = e^g \cdot (1+D_t/P_t)$. Then, subtracting $e^{r_f}=1$ on both sides leads to $e^{E_t[r_e]} - e^{r_f} = (e^g - 1) + e^g \cdot D_t/P_t$. This equation implies the same type of restrictions on $a_t$ and $b_t$ as the steady-state model does, but in the context of a model in which expected returns (and thus $D_t/P_t$) are allowed to vary over time.

---

## Question 3

In this question, we work with the time index $\tau = 1, 2, ..., T$, representing months (as opposed to $t = 1, 2, ..., T$, representing years).

### 3(a)

Construct the momentum signal (MOM) monthly for the firms with data available in CRSP.[^4] Focus on the period from June 1963 to the recent date to match the book-to-market construction of Question 3(b). As is standard in the literature, restrict the analysis to common stocks of firms incorporated in the United States (CRSP `shrcd` = 10 or 11) trading on NYSE, Amex, or Nasdaq (CRSP `exchcd` = 1, 2, or 3), and exclude utilities ($4900 \le \text{SIC} \le 4949$) and financials ($6000 \le \text{SIC} \le 6999$).

[^4]: MOM for a stock at the end of month $\tau$ refers to the cumulative stock return from month $\tau-12$ to month $\tau-1$.

To validate your MOM construction, merge your dataset with the CZ Dataset and define $\text{MOM}_{CZ} = \text{Mom12m}$ (use the column `permno` to identify the stock and the column `yyyymm` to identify the date). For each month in the sample, estimate a cross-firm regression of $\text{MOM}_{CZ}$ onto your MOM and record the intercept and slope coefficients as well as the $R^2$ from these regressions. Provide three time-series plots: one for the intercepts, one for the slopes, and one for the $R^2$ values.

### 3(b)

Construct the book-to-market signal (BM) monthly for the firms with data available in the CRSP and COMPUSTAT datasets.[^5] To ensure all information used in the construction of BM is available to investors (see Fama and French (1992)), construct BM as of the end of June of year $t$ using CRSP market equity data from December of calendar year $t-1$ (for ME) and COMPUSTAT accounting data from the fiscal year ending in calendar year $t-1$ (for BE).[^6] Then, keep BM fixed from June of year $t$ to May of year $t+1$, updating BM again in June of year $t+1$. Also exclude firm-month observations with $\text{BE} \le 0$.

[^5]: You will need to merge CRSP and COMPUSTAT. The easiest way to do this is to directly use the "CRSP/COMPUSTAT Merged" dataset available on WRDS under CRSP.
[^6]: $\text{ME} = |PRC| \cdot \text{SHROUT}$ (from CRSP). $\text{BE} = \text{SE} + \text{TXDITC} - \text{BVPS}$ (from COMPUSTAT). SE reflects stockholders' equity and is given by SEQ, CEQ + PSTK, or AT − LT, in this sequence of availability. TXDITC reflects deferred taxes and is given by TXDITC if available (0 otherwise). BVPS reflects the book value of preferred shareholders and is given by PSTKRV, PSTKL, or PSTK, in this sequence of availability.

To avoid backfilling bias (see Fama and French (1993)), require a minimum of two previous years in COMPUSTAT for a company to be included in the analysis, and construct BM from June 1963 to the most recent date so that the first fiscal year of COMPUSTAT data is 1962. As is standard in the literature, restrict the analysis to common stocks of firms incorporated in the United States (CRSP `shrcd` = 10 or 11) trading on NYSE, Amex, or Nasdaq (CRSP `exchcd` = 1, 2, or 3), and exclude utilities ($4900 \le \text{SIC} \le 4949$) and financials ($6000 \le \text{SIC} \le 6999$).

To validate your BE/ME construction, merge your dataset with the CZ Dataset and calculate $\text{BM}_{CZ} = \exp(\text{BMdec})$ (use the column `permno` to identify the stock and the column `yyyymm` to identify the date). For each month in the sample, estimate a cross-firm regression of $\text{BM}_{CZ}$ onto your BM and record the intercept and slope coefficients as well as the $R^2$ from these regressions. Provide three time-series plots: one for the intercepts, one for the slopes, and one for the $R^2$ values.

### 3(c)

Let $\text{GP}_{CZ} = \text{GP}$. Then, for each of the three signals ($\text{BM}_{CZ}$, $\text{MOM}_{CZ}$, and $\text{GP}_{CZ}$), construct decile portfolios as described in the lectures (returns come from CRSP).[^7] Create five types of decile portfolios (for each signal):

(i) Value-weighted, rebalanced annually (at June), with NYSE breakpoints
(ii) Equal-weighted, rebalanced annually (at June), with NYSE breakpoints
(iii) Value-weighted, rebalanced monthly, with NYSE breakpoints
(iv) Value-weighted, rebalanced annually (at June), with general breakpoints
(v) Equal-weighted, rebalanced monthly, with general breakpoints

[^7]: Note that you are using only the signals constructed by Chen and Zimmermann (2022) in this question. This helps debug your code, since any unusual pattern you observe must come from potential errors in the formation of the portfolios, not from potential errors in the construction of the signals.

For each of the five types of decile portfolios, provide a scatterplot with the decile value (1 to 10) on the x-axis and the average portfolio excess return on the y-axis.[^8] To keep the three signals in the same scatterplot (so you have a total of five scatterplots), use blue for $\text{BM}_{CZ}$ portfolios, red for $\text{MOM}_{CZ}$ portfolios, and green for $\text{GP}_{CZ}$ portfolios. Moreover, calculate the HML portfolio (decile 10 − decile 1) in each case (you should have a total of 15 HML portfolios) and report in a table the HML average returns as well as their respective t-statistics (using Newey and West (1987, 1994) standard errors — see the note under Question 2(b)).

[^8]: The excess return ($xR$) in Questions 3(c) to 3(e) refers to the return of a stock or portfolio in excess of the return of a risk-free benchmark. You can obtain returns for a risk-free benchmark in the Ken French data library (under "Fama/French 3 Factors") from the column `RF`.

### 3(d)

Estimate Fama-MacBeth regressions of $xR_{j,\tau+1}$ on signals available at month $\tau$ and report the results in a table (including the t-statistic of each coefficient). Estimate the following regression specifications (at each $\tau$, use both OLS and WLS with month-$\tau$ market-equity weights):

$$
\begin{aligned}
\text{(i)}\quad & xR_{j,\tau+1} = a + b_{BM} \cdot Q^{BM}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(ii)}\quad & xR_{j,\tau+1} = a + b_{GP} \cdot Q^{GP}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(iii)}\quad & xR_{j,\tau+1} = a + b_{Dur} \cdot Q^{Dur}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(iv)}\quad & xR_{j,\tau+1} = a + b_{BM} \cdot Q^{BM}_{j,\tau} + b_{GP} \cdot Q^{GP}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(v)}\quad & xR_{j,\tau+1} = a + b_{Dur} \cdot Q^{Dur}_{j,\tau} + b_{BM} \cdot Q^{BM}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(vi)}\quad & xR_{j,\tau+1} = a + b_{Dur} \cdot Q^{Dur}_{j,\tau} + b_{GP} \cdot Q^{GP}_{j,\tau} + \varepsilon_{j,\tau+1} \\
\text{(vii)}\quad & xR_{j,\tau+1} = a + b_{Dur} \cdot Q^{Dur}_{j,\tau} + b_{BM} \cdot Q^{BM}_{j,\tau} + b_{GP} \cdot Q^{GP}_{j,\tau} + \varepsilon_{j,\tau+1}
\end{aligned}
$$

where $Q^X_{j,\tau}$ reflects the quantile of signal $X_{j,\tau}$ in the cross-firm distribution of $X$ at month $\tau$ (for BM and GP, use the Chen and Zimmermann (2022) version of the signals). The use of quantiles deals with the fact that signals often have skewed distributions and outliers.[^9]

[^9]: An alternative approach is to use the cross-firm z-score of winsorized log $X$, but this log approach cannot be used for signals that can take negative values (not the case here, but often the case in other applications).

### 3(e)

Gonçalves (2021b) proposes the use of multivariate regressions for portfolios analogous to the use of firm-level multivariate regressions in Question 3(d). For instance, if we have 10 $\text{BM}_{CZ}$ decile portfolios and 10 $\text{GP}_{CZ}$ decile portfolios, then for each portfolio $p$ we can calculate the average $\text{BM}_{CZ}$ decile of its firms (call it $\text{Dec}^{BM}_{p,\tau}$) as well as the average $\text{GP}_{CZ}$ decile of its firms (call it $\text{Dec}^{GP}_{p,\tau}$) and estimate the panel regression $xR_{p,\tau+1} = a + b_{BM}\cdot\text{Dec}^{BM}_{p,\tau} + b_{GP}\cdot\text{Dec}^{GP}_{p,\tau} + \varepsilon_{p,\tau+1}$ by pooled OLS using the 20 portfolios with Driscoll and Kraay (1998) standard errors.[^10] Following this approach, estimate the following regression specifications and report the results in a table (including t-statistics):

$$
\begin{aligned}
\text{(i)}\quad & xR_{p,\tau+1} = a + b_{BM} \cdot \text{Dec}^{BM}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(ii)}\quad & xR_{p,\tau+1} = a + b_{GP} \cdot \text{Dec}^{GP}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(iii)}\quad & xR_{p,\tau+1} = a + b_{Dur} \cdot \text{Dec}^{Dur}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(iv)}\quad & xR_{p,\tau+1} = a + b_{BM} \cdot \text{Dec}^{BM}_{p,\tau} + b_{GP} \cdot \text{Dec}^{GP}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(v)}\quad & xR_{p,\tau+1} = a + b_{Dur} \cdot \text{Dec}^{Dur}_{p,\tau} + b_{BM} \cdot \text{Dec}^{BM}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(vi)}\quad & xR_{p,\tau+1} = a + b_{Dur} \cdot \text{Dec}^{Dur}_{p,\tau} + b_{GP} \cdot \text{Dec}^{GP}_{p,\tau} + \varepsilon_{p,\tau+1} \\
\text{(vii)}\quad & xR_{p,\tau+1} = a + b_{Dur} \cdot \text{Dec}^{Dur}_{p,\tau} + b_{BM} \cdot \text{Dec}^{BM}_{p,\tau} + b_{GP} \cdot \text{Dec}^{GP}_{p,\tau} + \varepsilon_{p,\tau+1}
\end{aligned}
$$

[^10]: Gonçalves (2021b) shows that this panel regression of portfolio returns on portfolio deciles is a natural generalization of the HML average returns often emphasized in the literature. For instance, the coefficient estimate from a univariate regression of portfolio returns on portfolio deciles is equivalent to a weighted average of HML average returns, where HML portfolios are obtained from Decile10 − Decile1, Decile9 − Decile2, Decile8 − Decile3, Decile7 − Decile4, and Decile6 − Decile5.

Estimate each specification above using value-weighted portfolios as well as equal-weighted portfolios (in both cases the portfolios are rebalanced annually and rely on NYSE breakpoints). For the BM and GP portfolios, use the Chen and Zimmermann (2022) version of the signals.

---

## Question 4

### 4(a)

The "Bond Dataset" contains yields in percentage terms, $Y^{(H)}_{b,t}\cdot 100\%$. Construct time series of:

(i) Log yields: $y^{(H)}_{b,t} = \log(1 + Y^{(H)}_{b,t})$
(ii) Log forward rates: $f^{(H)}_{b,t} = H \cdot y^{(H)}_{b,t} - (H-1)\cdot y^{(H-1)}_{b,t}$
(iii) Log annual returns: $r^{(H)}_{b,t} = H\cdot y^{(H)}_{b,t-1} - (H-1)\cdot y^{(H-1)}_{b,t}$

For $H = 2,3,4,5$, calculate and report in a table the average values of[^11]

(i) $xy^{(H)}_{b,t} = y^{(H)}_{b,t} - y^{(1)}_{b,t}$
(ii) $xf^{(H)}_{b,t} = f^{(H)}_{b,t} - f^{(1)}_{b,t}$
(iii) $xr^{(H)}_{b,t} = r^{(H)}_{b,t} - r^{(1)}_{b,t}$

[^11]: Note that the excess returns are not deflated, but would be identical if deflated. In particular, the deflated log return of a bond is $\log(R^{(H)}_{b,t}\cdot\Pi_t/\Pi_{t-1}) = r^{(H)}_{b,t} - \Delta\pi_t$. As such, the deflated excess log return of a bond is $xr^{(H)}_{b,t} = (r^{(H)}_{b,t}-\Delta\pi_t) - (r^{(1)}_{b,t}-\Delta\pi_t) = r^{(H)}_{b,t} - r^{(1)}_{b,t}$.

### 4(b)

For $H = 2,3,4,5$, estimate the regression

$$
(1/H)\cdot xr^{(H)}_{b,t\to t+H} = a^{(H)} + b^{(H)}\cdot xy^{(H)}_{b,t} + \varepsilon^{(H)}_t \tag{4.1}
$$

where the hold-to-maturity excess return is $xr^{(H)}_{b,t\to t+H} = \sum_{h=1}^{H} xr^{(H-h+1)}_{t+h} = \sum_{h=1}^{H}\left(r^{(H-h+1)}_{t+h} - r^{(1)}_{t+h}\right)$.[^12]

[^12]: Note that $xr^{(H)}_{b,t\to t+H} \ne \sum_{h=1}^{H}\left(r^{(H)}_{t+h} - r^{(1)}_{t+h}\right)$. The intuition is that we want to capture the hold-to-maturity return on the $H$-year bond. In one year, this bond will have maturity of $H-1$. Then, in the subsequent year it will have maturity of $H-2$, and so on.

Using the results from the regressions in Equation 4.1, reproduce a table analogous to the first panel of the first table on slide 5.5 of the Module 1 lecture notes. For the t-statistics, use the method in Hansen and Hodrick (1980) (see the note under Question 2(b)).

### 4(c)

For $H = 2,3,4,5$, estimate the regression[^13]

$$
xr^{(H)}_{b,t+1} = a^{(H)} + b^{(H)}\cdot xf^{(H)}_{b,t} + \varepsilon^{(H)}_t \tag{4.2}
$$

[^13]: Note that for $H=2$ we have $xr^{(2)}_{b,t\to t+2} = xr^{(2)}_{b,t+1}$ (to verify, substitute $H=2$ in the expression for $xr^{(2)}_{b,t\to t+2}$ in Question 4(b)). Moreover, with $H=2$ we have $xf^{(2)}_{b,t} = 2\cdot xy^{(2)}_{b,t}$ (to verify, substitute $H=2$ in the expression for $xf^{(H)}_{b,t}$ in Question 4(a)). So, $b^{(2)}$ in Equation 4.2 is the same as $b^{(2)}$ in Equation 4.1 (to verify, substitute $xr^{(2)}_{b,t+1} = xr^{(2)}_{b,t\to t+2}$ and $xf^{(2)}_{b,t} = 2\cdot xy^{(2)}_{b,t}$ in Equation 4.2 and divide both sides by $H=2$).

Using the results from the regressions in Equation 4.2, reproduce a table analogous to the second panel of the first table on slide 5.5 of the Module 1 lecture notes. For the t-statistics, use the method in Newey and West (1987, 1994) (see the note under Question 2(b)).

### 4(d)

Estimate the Cochrane and Piazzesi (2005) factor from

$$
\frac{1}{4}\cdot\sum_{H=2}^{5} xr^{(H)}_{b,t+1} = \theta_0 + \underbrace{\sum_{H=1}^{5} \theta_h \cdot f^{(H)}_{b,t}}_{cp_t} + u_t \tag{4.3}
$$

and provide a time-series plot of $cp_t$ with NBER recession gray areas in the background (the NBER recession dummies are available from the [FRED USREC series](https://fred.stlouisfed.org/series/USREC)).

### 4(e)

For $H = 2,3,4,5$, estimate the regression

$$
xr^{(H)}_{b,t+1} = a^{(H)} + b^{(H)}\cdot cp_t + \varepsilon^{(H)}_t \tag{4.4}
$$

Using the results from the regressions in Equation 4.4, reproduce a table analogous to the second table on slide 5.5 of the Module 1 lecture notes. For the t-statistics, use the method in Newey and West (1987, 1994) (see the note under Question 2(b)).

---

## References

- Amihud, Y. and C. M. Hurvich (2004). "Predictive Regressions: A Reduced-Bias Estimation Method". *Journal of Financial and Quantitative Analysis* 39.4, pp. 813–841.
- Andrews, D. W. K. (1991). "Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation". *Econometrica* 59.3, pp. 817–858.
- Campbell, J. Y. and R. J. Shiller (1989). "The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors". *Review of Financial Studies* 1.3, pp. 195–228.
- Chen, A. Y. and T. Zimmermann (2022). "Open Source Cross-Sectional Asset Pricing". *Critical Finance Review* 27.2, pp. 207–264.
- Cochrane, J. H. and M. Piazzesi (2005). "Bond Risk Premia". *American Economic Review* 95.1, pp. 138–160.
- Driscoll, J. C. and A. C. Kraay (1998). "Consistent Covariance Matrix Estimation with Spatially Dependent Panel Data". *Review of Economics and Statistics* 80.4, pp. 549–560.
- Fama, E. F. and K. R. French (1992). "The Cross-Section of Expected Stock Returns". *Journal of Finance* 47.2, pp. 427–465.
- Fama, E. F. and K. R. French (1993). "Common Risk Factors in the Returns on Stocks and Bonds". *Journal of Financial Economics* 33.1, pp. 3–56.
- Gao, C. and I. Martin (2021). "Volatility, Valuation Ratios, and Bubbles: An Empirical Measure of Market Sentiment". *Journal of Finance* 76.6, pp. 3211–3254.
- Gonçalves, A. S. (2021a). "Reinvestment Risk and the Equity Term Structure". *Journal of Finance* 76.5, pp. 2153–2197.
- Gonçalves, A. S. (2021b). "The Short Duration Premium". *Journal of Financial Economics* 141.3, pp. 919–945.
- Hansen, L. P. and R. J. Hodrick (1980). "Forward Exchange Rates as Optimal Predictors of Future Spot Rates: An Econometric Analysis". *Journal of Political Economy* 88.5, pp. 829–853.
- Hodrick, R. J. (1992). "Dividend Yields and Expected Stock Returns: Alternative Procedures for Inference and Measurement". *Review of Financial Studies* 5.3, pp. 357–386.
- Jegadeesh, N. and S. Titman (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency". *Journal of Finance* 48.1, pp. 65–91.
- Newey, W. K. and K. D. West (1987). "A Simple, Positive-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix". *Econometrica* 55.3, pp. 703–708.
- Newey, W. K. and K. D. West (1994). "Automatic Lag Selection in Covariance Matrix Estimation". *Review of Economic Studies* 61.4, pp. 631–653.
- Novy-Marx, R. (2013). "The other side of value: The gross profitability premium". *Journal of Financial Economics* 108.1, pp. 1–28.
- White, H. (1980). "A Heteroskedastic Consistent Covariance Matrix and a Direct Test for Heteroskedasticity". *Econometrica* 48.4, pp. 817–838.
