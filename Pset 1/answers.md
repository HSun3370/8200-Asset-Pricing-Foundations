
# Homework 1

+++ {"part": "abstract"}
This is my abstract!
+++

```{raw:typst}
#set page(margin: auto)
```

## Question 1

### Proof
Start by taking logs on both sides of the return expression:
$$ \log R_{e,t+1} = \log (1 + \exp(\log D_{t+1} - \log P_{t+1})) + \log P_{t+1} - \log P_t$$
For simplicity, I denote $r_{e,t+1} = \log R_{e,t+1}$, $p_{t+1} = \log P_{t+1}$, $d_{t+1} = \log D_{t+1}$, and $dp_{t+1} =\log D_{t+1} -\log P_{t+1}$, 
then, by a Taylor expansion in $dp_{t+1}$ (which is stationary with mean $\bar{dp}$), we get 

$$
\begin{aligned}
r_{e,t+1} = \log (1 + \exp(\bar{dp})) + \frac{\exp (\bar{dp})}{1 + \exp (\bar{dp})} (dp_{t+1} - \bar{dp})  + p_{t+1} - p_t .
\end{aligned}
$$

Denote $\kappa  = 1/(1+ \exp{(\bar{dp}}))$, and $\kappa _0 = \log (1 + \exp(\bar{dp})) - \bar{dp}\exp (\bar{dp})/(1+ \exp{(\bar{dp}})) = -\log \kappa - (1-\kappa) \log (1/\kappa -1)$. The log-linearization becomes

$$\begin{aligned}
r_{e,t+1} = \kappa_0 + (1-\kappa)  dp_{t+1}   + p_{t+1} - p_t .
\end{aligned}$$

Moving $p_t$ to the left-hand side and the other terms to the right-hand side, we get

$$\begin{aligned}
 p_t&= \kappa_0 + (1-\kappa)  d_{t+1}   - r_{e,t+1}  + \kappa ~ p_{t+1} \\
&= \kappa_0 + (1-\kappa)  d_{t+1}   - r_{e,t+1} + \kappa ~ [\kappa_0 + (1-\kappa)  d_{t+2}   - r_{e,t+2}  + \kappa ~ p_{t+2} ] \\ 
&= \kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
 &~~~~~~~~~~~~+(1-\kappa) (d_{t+1}  + \kappa~ d_{t+2} + ... + \kappa^{H-1} d_{t+H})  \\
& ~~~~~~~~~~~~ -  [r_{e,t+1} +\kappa~r_{e,t+2} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
&~~~~~~~~~~~~+ \kappa^H p_{t+H} 
% \\
% p_t& = \kappa_0 \frac{1- \kappa^H}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} d_{t+h} - \sum_{h=1}^H \kappa^{h-1} r_{e,t+h} + \kappa^H p_{t+H}
\end{aligned}$$

The log dividend-price ratio $dp_t$ can then be written as
 
$$
\begin{aligned}
dp_t &= -\kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
& ~~~~~~~~~~~~ +  [r_{e,t+1} +\kappa~r_{e,t+1} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
 &~~~~~~~~~~~~d_t-(1-\kappa) (d_{t+1}  + \kappa~ d_{t+2} + ... + \kappa^{H-1} d_{t+H})  \\ 
&~~~~~~~~~~~~- \kappa^H p_{t+H}   \\
&= -\kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
& ~~~~~~~~~~~~ +  [r_{e,t+1} +\kappa~r_{e,t+1} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
 &~~~~~~~~~~~~d_t - d_{t+1} + \kappa ~ (d_{t+1} - d_{t+2}) +  ... + \kappa^{H-1} (d_{t+H-1} -  d_{t+H}  ) \\ 
&~~~~~~~~~~~~ +  \kappa^{H } d_{t+H} - \kappa^H p_{t+H}  \\
&= \kappa_0 \frac{ \kappa^H-1}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} r_{e,t+h} - \sum_{h=1}^H  \kappa^{h-1} \Delta d_{t+h} + \kappa^H dp_{t+H}
\end{aligned}
$$ 
where $\Delta d_{t+1} := d_{t+1} - d_t$. Notice that the identity above holds ex post (state by state), so it also holds in conditional expectation at time $t$, giving

$$
\begin{aligned}
dp_t  = \kappa_0 \frac{ \kappa^H-1}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum_{h=1}^H  \kappa^{h-1} \mathbb E_t \Delta  d_{t+h} + \kappa^H \mathbb E_t dp_{t+H}
\end{aligned}
$$ 

Letting $H \to \infty$ and imposing the no-bubble (transversality) condition
$$ \lim_{H\to \infty} \kappa^H \mathbb E_t dp_{t+H} = 0$$
we obtain equation (1.3):

$$
\begin{aligned}
dp_t  = \kappa_0 \frac{  -\kappa_0}{1- \kappa} + \sum_{h=1}^\infty \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum_{h=1}^\infty  \kappa^{h-1} \mathbb E_t \Delta  d_{t+h} 
\end{aligned}
$$ 


### 
 
:::{figure} output/q1b_slopes.png
:label: fig-q1b
:width: 90%

Equation 1.4 variance-decomposition slopes vs. horizon $H$ (EQ Dataset,
1928–2021; overlapping monthly starts; $\kappa = 1/(1+e^{\overline{dp}}) = 0.9642$).
:::


We can infer from the figure that, valuation ratio $dp_t$ can predict log run return, and the volatility of price mainly comes from the volatility of discount rate. 


### VAR
Using equation 
$$b_{re}^{(H)} = \mathbb{1}_{re} (\Gamma + \kappa^H  \Gamma^{H+1}) (I-\kappa \Gamma)^{-1} \frac{Cov (z_t,dp_t)}{Var(dp_t)}$$

$$b_{\Delta d}^{(H)} = -\mathbb{1}_{\Delta d} (\Gamma + \kappa^H  \Gamma^{H+1}) (I-\kappa \Gamma)^{-1} \frac{Cov (z_t,dp_t)}{Var(dp_t)}$$

and $b_{dp}^{(H)}=1-b_{re}^{(H)}-b_{\Delta d}^{(H)}$. 

:::{figure} output/q1c_slopes.png
:label: fig-q1c
:width: 90%

VAR-implied Equation 1.4 variance-decomposition terms vs. horizon $H$. Overlapping-annual
VAR(1) on $Z_t = [\Delta d_t,\ r_{e,t},\ dp_t]'$ estimated by OLS (EQ Dataset, 1928–2021;
$\kappa = 0.9642$, as in 1(b)). $b_{dp}^{(H)}$ is imposed as $1 - b_{re}^{(H)} - b_{\Delta d}^{(H)}$.
:::

 

### 

As $H\to\infty$, the 
$$b_{re}^{(\infty)} = \mathbb{1}_{re}  \Gamma    (I-\kappa \Gamma)^{-1} \frac{Cov (z_t,dp_t)}{Var(dp_t)}$$

$$b_{\Delta d}^{(\infty)} = -\mathbb{1}_{\Delta d} \Gamma    (I-\kappa \Gamma)^{-1} \frac{Cov (z_t,dp_t)}{Var(dp_t)}$$

The calculated numbers are 
$b_{re}^{(\infty)} = 0.4892$, 
$b_{\Delta d}^{(\infty)}=0.5096$, and 
$b_{dp}^{(\infty)} = 	0.0012 $. These numbers show that valuation ratio $dp$ can both predict divdend growth and returns, and half of price volatility is attribute to divdiden growth variance, half is attribute to  discount rate variance. This result is not aligned with Cochrane(2011). 

### Alternative log-linear present-value identity
Using the same trick,  
$$ 
R_{e,t+1} =  \frac{P_{t+1}+D_{t+1}}{ D_{t+1}  } \frac{D_{t+1} }{D_{t }   }  \frac {D_{t }   } {P_t + D_t} \frac  {P_t + D_t} {P_t} 
$$
, the log one-period return can be written as 
$$
\begin{aligned}
r_{e,t+1} =  -\log (1 - e^{-dy_{t+1}}) + \Delta d_{t+1} + \log (1 - e^{-dy_t}) + dy_t
\end{aligned}
$$
where $dy_t := \log (1+\frac{D_t}{P_t})$ and $\log (1 - e^{-dy_t})  =  \log \frac {D_{t }   } {P_t + D_t}$.

Applying a Taylor expansion of $\log (1 - e^{-dy_t})$ in $dy_t$ around its mean $\bar {dy}$, we have 
$$
\begin{aligned}
\log (1 - e^{-dy_t}) = \log (1 - e^{-\bar {dy}}) + \frac{e^{-\bar {dy}}}{1 - e^{-\bar {dy}}} ( dy_t -\bar {dy})
+O((dy_t-\bar{dy})^2)
\end{aligned}
$$
Letting $\kappa = e^{-\bar{dy}}$ to simplify the expression, 
$$
\begin{aligned}
\log (1 - e^{-dy_t}) = \log (1 - \kappa) + \frac{\kappa}{1 - \kappa } ( dy_t -\bar {dy})
+O((dy_t-\bar{dy})^2)
\end{aligned}
$$
Then the return is log-linearized as
$$
\begin{aligned}
r_{e,t+1} =  -\frac{\kappa}{1 - \kappa } ( dy_{t+1} -\bar {dy}) + \Delta d_{t+1} + \frac{\kappa}{1 - \kappa } ( dy_t -\bar {dy}) + dy_t
\end{aligned}
$$
and 
$$
\begin{aligned}
  \frac{dy_t}{1 - \kappa }   &=     r_{e,t+1} - \Delta d_{t+1}  +  \kappa  ~ \frac{ dy_{t+1}}{1 - \kappa } \\
   &=    r_{e,t+1} - \Delta d_{t+1}  \\
   &~~~~~~~~~~+  \kappa ~  [   r_{e,t+2} - \Delta d_{t+2}  +  \kappa ~ \frac{ dy_{t+2}}{1 - \kappa } ] \\
   &=    r_{e,t+1} - \Delta d_{t+1} + \kappa ~  [   r_{e,t+2} - \Delta d_{t+2} ] \\
   &~~~~~~~~~~ + ...+  \kappa^{H-1} ~  [   r_{e,t+H} - \Delta d_{t+H} ] + \kappa^H \frac{dy_{t+H}}{1 - \kappa } \\
   &=\sum^H_{h=1} \kappa^{h-1} r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1} \Delta d_{t+h} + \kappa^H \frac{dy_{t+H}}{1 - \kappa }
\end{aligned}
$$
Thus, the log-linearization identity is 
$$
\begin{aligned}
  dy_t    =(1 - \kappa)(\sum^H_{h=1} \kappa^{h-1} r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1} \Delta d_{t+h}) + \kappa^H  dy_{t+H}  
\end{aligned}
$$
Taking the conditional expectation at time $t$, the identity also holds
$$
\begin{aligned}
  dy_t    =(1 - \kappa)(\sum^H_{h=1} \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1}\mathbb E_t\Delta d_{t+h}) + \kappa^H \mathbb E_t dy_{t+H}  
\end{aligned}
$$
Imposing the no-bubble assumption, the last term vanishes as $h\to \infty$,
$$ \lim_{H \to \infty} \kappa^H E_t \log (\frac{P_t + D_t}{P_t})  \to 0 $$

## Question 2

### 

:::{figure} output/q2a_r2adj.png
:label: fig-q2a
:width: 90%

Adjusted $R^2$ of the regressions of the average future excess equity
return $\frac{1}{H}\sum_{h=1}^{H} xR_{e,t+h}$ on $D_t/P_t$, plotted against the
horizon $H = 1,\dots,15$ years.
:::

Valuation ratio $\frac{D}{P}$ predicts returns in the long run better than in the short run. 



### 
Estimating $xR_{e,t+1} = a + b \cdot D_t/P_t + \varepsilon_t$  by OLS on $T = 1117$ monthly start dates (1927:12--2020:12) gives
$\hat{a} = -0.0314$ and $\hat{b} = 2.8038$. The five standard errors for $\hat{b}$,
all built from $\widehat{\mathrm{Var}}[\hat\theta] = \frac{1}{T} Q^{-1} \hat{S} Q^{-1}$
with $Q = \frac{1}{T}\sum_\tau x_\tau x_\tau'$, are:

| Standard error method | $\hat{b}$ | s.e.$(\hat{b})$ | $t$-statistic |
|---|---|---|---|
| (i) OLS | 2.8038 | 0.3798 | 7.38 |
| (ii) White (1980) | 2.8038 | 0.6587 | 4.26 |
| (iii) Newey-West (1987), 11 lags | 2.8038 | 1.2990 | 2.16 |
| (iv) Hansen-Hodrick (1980), 11 lags | 2.8038 | 1.4537 | 1.93 |
| (v) Newey-West (1987, 1994), $L = 24$ | 2.8038 | 1.2304 | 2.28 |

The lag length in (v) is data-driven: the Newey and West (1994, Eq. 2.2) rule gives
$L = a \cdot T^{1/3}$ with $a = 2.31$, hence $L = 24$. The Hansen-Hodrick estimate in
(iv) is positive definite in this sample, so no truncation was needed.

###
I report Amihud and Hurvich (2004) estimation.

$$
\frac{D_{t+1}}{P_{t+1}} = \underset{0.0111}{\hat\theta} + \underset{0.7197}{\hat\phi}\,\frac{D_t}{P_t} + \hat\varepsilon_{t+1}
$$

$$
\hat\phi^c = \hat\phi + \frac{1}{T}\left(1+3\hat\phi\right) + \frac{3}{T^2}\left(1+3\hat\phi\right) = 0.7540, \qquad T = 95
$$

$$
\hat u^c_{t+1} = \frac{D_{t+1}}{P_{t+1}} - \left(\hat\theta + \hat\phi^c\,\frac{D_t}{P_t}\right)
$$

$$
xR_{e,t+1} = \underset{-0.0314}{\hat a} + \underset{2.3412}{\hat b}\,\frac{D_t}{P_t} + \underset{-13.4837}{\hat b_u}\,\hat u^c_{t+1} + \hat\varepsilon_{t+1}
$$

Amihud and Hurvich estimation gives a smaller value than OLS estimation. This is because OLS estimation is upper biased in small sample as innovations of dividend-price ratio and excess return are positive correlated, and the AR(1) estimation is lower biased. 


### 


:::{figure} output/q2d_forecasts.png
:label: fig-q2d-forecasts
:width: 90%

Forecasts of the one-year-ahead excess return for $t+1$ from December 1940 to December 2021: the out-of-sample
forecast $\hat{E}^{OS}_t[xR_e] = a_t + b_t\,D_t/P_t$ with $a_t, b_t$ estimated on an expanding window,
the in-sample forecast $\hat{E}^{IS}_t[xR_e] = \hat a + \hat b\,D_t/P_t$ from Equation 2.2, and the
expanding-window historical mean $\overline{xR}_{e,t}$.
:::

Each expanding window runs from the pair $(t, t+1) =$ (December 1927, December 1928) through the pair
one month before the forecast pair (for the first forecast, through (November 1939, November 1940), 144 pairs), and
$\overline{xR}_{e,t}$ averages $xR_{e,t+1}$ over the same window. Over the 973 forecasts with $t+1$
from December 1940 to December 2021,

$$
R^2_{OS} =  1 - \frac{\sum_t \left(xR_{e,t+1} - \hat{E}^{OS}_t[xR_e]\right)^2}{\sum_t \left(xR_{e,t+1} - \mu_{xR}\right)^2} = 1 - \frac{26.7838}{26.8327} = 0.0018
$$

where $\mu_{xR}$ is the sample mean of $xR_{e,t+1}$ over the same 973 months; no degrees-of-freedom
adjustment is applied.

:::{figure} output/q2d_rolling_r2os.png
:label: fig-q2d-rolling
:width: 90%

$R^2_{OS}$ over 600-month (50-year) rolling windows of the out-of-sample forecast errors, plotted at each
window's last month from December 1990 to December 2021 (first window: January 1941 to December 1990). $a_t$ and $b_t$ are the
expanding-window estimates above; SST uses the sample mean of $xR_{e,t+1}$ within each window.
:::


### 

:::{figure} output/q2e_forecasts.png
:label: fig-q2e-forecasts
:width: 90%

Forecasts of the one-year-ahead excess return for $t+1$ from December 1940 to December 2021: the restricted out-of-sample
forecast $\hat{E}^{OS}_t[xR_e] = (\bar{G}_t - 1) + \bar{G}_t\,D_t/P_t$, the in-sample forecast
$\hat{E}^{IS}_t[xR_e] = \hat a + \hat b\,D_t/P_t$ from Equation 2.2, and the expanding-window historical mean
$\overline{xR}_{e,t}$.
:::

The sample, forecast dates, expanding windows, $\hat{E}^{IS}_t[xR_e]$ and $\overline{xR}_{e,t}$ are those of
Question 2(d). $\bar{G}_t$ averages $e^{\Delta d}$ over the same expanding window; for the first forecast it uses
$\Delta d$ from December 1927 to November 1939 (144 months), so $\bar{G}_t = 1.0000$. Over the 973 forecasts with $t+1$ from
December 1940 to December 2021,

$$
R^2_{OS} = 1 - \frac{\sum_t \left(xR_{e,t+1} - \hat{E}^{OS}_t[xR_e]\right)^2}{\sum_t \left(xR_{e,t+1} - \mu_{xR}\right)^2} = 1 - \frac{26.7797}{26.8327} = 0.0020
$$

where, as in Question 2(d), $\mu_{xR}$ is the sample mean of $xR_{e,t+1}$ over the same 973 months and no
degrees-of-freedom adjustment is applied.

:::{figure} output/q2e_rolling_r2os.png
:label: fig-q2e-rolling
:width: 90%

$R^2_{OS}$ of the restricted forecast over 600-month (50-year) rolling windows of the out-of-sample forecast
errors, plotted at each window's last month from December 1990 to December 2021 (first window: January 1941 to December 1990). SST uses the
sample mean of $xR_{e,t+1}$ within each window.
:::







## Question 3

### 3(a)

For each month $\tau$ I estimate the cross-firm regression
$$
\text{MOM}^{CZ}_{j,\tau} = a_\tau + b_\tau \cdot \text{MOM}_{j,\tau} + \varepsilon_{j,\tau}
$$
and plot the resulting $\hat a_\tau$, $\hat b_\tau$ and $R^2_\tau$ below. My own signal
compounds the 12 monthly returns over $\tau-12,\dots,\tau-1$, the same window used in the
problem statement and by Chen and Zimmermann (2022).

:::{figure} output/q3a_intercept.png
:label: fig-q3a-intercept
:width: 95%

Monthly intercepts $\hat a_\tau$ from the cross-firm regression of $\text{MOM}_{CZ}$ on my
$\text{MOM}$, June 1964 – December 2024 (727 months, on average 3,351 firms per month).
:::

:::{figure} output/q3a_slope.png
:label: fig-q3a-slope
:width: 95%

Monthly slopes $\hat b_\tau$.
:::

:::{figure} output/q3a_r2.png
:label: fig-q3a-r2
:width: 95%

Monthly $R^2_\tau$.
:::

% TODO: discuss what these three series say about the MOM construction.

### 3(b)

Book equity is $BE = SE + TXDITC - BVPS$ from the fiscal year ending in calendar year
$t-1$, market equity is $ME = |PRC| \cdot SHROUT$ from December of year $t-1$, and
$BM = BE/ME$ is assigned at the end of June of year $t$ and held fixed through May of
year $t+1$. Firm-months with $BE \le 0$ are dropped, and a firm must already have at
least two prior annual COMPUSTAT records before the fiscal year used. Following the
sequence in footnote 6, $SE$ is taken from `SEQ` where available (262,826 firm-years)
and from `CEQ + PSTK` otherwise (a further 701). The extract carries no `AT` or `LT`, so
the third route is unavailable and 20,686 firm-years are left without a book-equity
value.

For each month $\tau$ I then estimate the cross-firm regression
$$
\text{BM}^{CZ}_{j,\tau} = a_\tau + b_\tau \cdot \text{BM}_{j,\tau} + \varepsilon_{j,\tau}
$$
using $\text{BM}_{CZ} = \text{BMdec}$. Note that `BMdec` in the Chen and Zimmermann
(2022) data is already a book-to-market *ratio* rather than its log: 2.72% of its values
are negative, its quartiles ($0.36$, $0.68$, $1.17$) are ratio-scale, and exponentiating
it overflows. It is therefore used directly.

:::{figure} output/q3b_intercept.png
:label: fig-q3b-intercept
:width: 95%

Monthly intercepts $\hat a_\tau$ from the cross-firm regression of $\text{BM}_{CZ}$ on my
$\text{BM}$, June 1964 – December 2024 (727 months, on average 2,478 firms per month).
:::

:::{figure} output/q3b_slope.png
:label: fig-q3b-slope
:width: 95%

Monthly slopes $\hat b_\tau$.
:::

:::{figure} output/q3b_r2.png
:label: fig-q3b-r2
:width: 95%

Monthly $R^2_\tau$.
:::

% TODO: discuss what these three series say about the BM construction.

### 3(c)

Using only the Chen and Zimmermann (2022) versions of the signals
($\text{BM}_{CZ}=\text{BMdec}$, $\text{MOM}_{CZ}=\text{Mom12m}$,
$\text{GP}_{CZ}=\text{GP}$), I form decile portfolios under the five schemes below.
Breakpoints are the signal deciles among NYSE-listed firms (`EXCHCD` $=1$) for the NYSE
schemes and among all sample firms for the general schemes; every firm is then assigned
using those cut-offs. Annual schemes form deciles on the June signal of year $t$ and hold
July of $t$ through June of $t+1$; value weights use market equity at the formation date
and are held fixed over the holding period. A stock with no usable CRSP return in a month
is dropped from its decile that month and the remaining weights renormalise. Excess
returns are net of `RF` from the Ken French three-factor file, and all three signals share
a common sample beginning June 1963 (738 months).

:::{figure} output/q3c_scheme_i.png
:label: fig-q3c-i
:width: 85%

Scheme (i): value-weighted, rebalanced annually at June, NYSE breakpoints.
:::

:::{figure} output/q3c_scheme_ii.png
:label: fig-q3c-ii
:width: 85%

Scheme (ii): equal-weighted, rebalanced annually at June, NYSE breakpoints.
:::

:::{figure} output/q3c_scheme_iii.png
:label: fig-q3c-iii
:width: 85%

Scheme (iii): value-weighted, rebalanced monthly, NYSE breakpoints.
:::

:::{figure} output/q3c_scheme_iv.png
:label: fig-q3c-iv
:width: 85%

Scheme (iv): value-weighted, rebalanced annually at June, general breakpoints.
:::

:::{figure} output/q3c_scheme_v.png
:label: fig-q3c-v
:width: 85%

Scheme (v): equal-weighted, rebalanced monthly, general breakpoints.
:::

The fifteen HML portfolios (decile 10 $-$ decile 1) have the following average excess
returns, in percent per month, with $t$-statistics from Newey and West (1987, 1994)
standard errors using the data-driven bandwidth $L$:

| Scheme | Signal | HML (%/month) | $t$-stat | $L$ |
|---|---|---:|---:|---:|
| (i) VW, annual, NYSE | $\text{BM}_{CZ}$ | 0.370 | 1.66 | 7 |
| (i) VW, annual, NYSE | $\text{MOM}_{CZ}$ | 0.354 | 1.46 | 3 |
| (i) VW, annual, NYSE | $\text{GP}_{CZ}$ | 0.359 | 2.09 | 11 |
| (ii) EW, annual, NYSE | $\text{BM}_{CZ}$ | 0.999 | 5.13 | 14 |
| (ii) EW, annual, NYSE | $\text{MOM}_{CZ}$ | −0.215 | −0.97 | 11 |
| (ii) EW, annual, NYSE | $\text{GP}_{CZ}$ | 0.533 | 3.16 | 13 |
| (iii) VW, monthly, NYSE | $\text{BM}_{CZ}$ | 0.319 | 1.54 | 6 |
| (iii) VW, monthly, NYSE | $\text{MOM}_{CZ}$ | 1.237 | 4.56 | 5 |
| (iii) VW, monthly, NYSE | $\text{GP}_{CZ}$ | 0.343 | 2.01 | 11 |
| (iv) VW, annual, general | $\text{BM}_{CZ}$ | 0.446 | 1.75 | 12 |
| (iv) VW, annual, general | $\text{MOM}_{CZ}$ | 0.437 | 1.41 | 4 |
| (iv) VW, annual, general | $\text{GP}_{CZ}$ | 0.424 | 1.90 | 10 |
| (v) EW, monthly, general | $\text{BM}_{CZ}$ | 0.939 | 4.78 | 14 |
| (v) EW, monthly, general | $\text{MOM}_{CZ}$ | 0.594 | 1.88 | 10 |
| (v) EW, monthly, general | $\text{GP}_{CZ}$ | 0.593 | 2.85 | 13 |

% TODO: discuss the scatterplots and the HML table -- in particular how the weighting
% scheme and the rebalancing frequency change each signal's premium.

### 3(d)

$Q^X_{j,\tau}$ is the cross-firm percentile rank of signal $X$ within month $\tau$, on
$[0,1]$, so a slope is the excess return earned by moving a stock from the bottom to the
top of that month's distribution. $BM$ and $GP$ are the Chen and Zimmermann (2022)
signals; $Dur$ is the firm-level equity duration of Gonçalves (2021b), whose
`FF.YEAR` $=t$ observation is public at the end of June of year $t$ and is therefore
carried across July of $t$ through June of $t+1$. All seven specifications are estimated
on the common sample of firm-months for which $BM$, $GP$ and $Dur$ are all available and
market equity is positive, so the specifications are directly comparable: 617 months from
July 1973 to November 2024, averaging 2,279 firms per cross-section. Each month's
cross-sectional regression is run by OLS and by WLS with month-$\tau$ market-equity
weights; the reported coefficients are time-series means of the monthly slopes, in
percent per month, with Newey and West (1987, 1994) $t$-statistics in parentheses.

| Spec | Method | $a$ | $b_{BM}$ | $b_{GP}$ | $b_{Dur}$ |
|---|---|---:|---:|---:|---:|
| (i) | OLS | 0.56 (2.27) | 0.93 (3.71) | | |
| (i) | WLS | 0.64 (2.96) | 0.21 (0.68) | | |
| (ii) | OLS | 0.73 (2.48) | | 0.57 (3.50) | |
| (ii) | WLS | 0.49 (2.16) | | 0.34 (1.50) | |
| (iii) | OLS | 1.60 (6.98) | | | −1.15 (−5.95) |
| (iii) | WLS | 1.30 (6.77) | | | −0.87 (−2.84) |
| (iv) | OLS | 0.09 (0.32) | 1.08 (4.31) | 0.78 (5.01) | |
| (iv) | WLS | 0.23 (0.79) | 0.57 (1.76) | 0.56 (2.78) | |
| (v) | OLS | 1.35 (5.71) | 0.32 (1.13) | | −0.99 (−3.72) |
| (v) | WLS | 1.32 (3.97) | −0.21 (−0.56) | | −0.84 (−2.09) |
| (vi) | OLS | 1.40 (4.98) | | 0.27 (1.59) | −1.04 (−4.77) |
| (vi) | WLS | 0.84 (2.39) | | 0.49 (1.70) | −0.54 (−1.30) |
| (vii) | OLS | 0.72 (2.78) | 0.63 (1.95) | 0.56 (2.77) | −0.58 (−1.93) |
| (vii) | WLS | 0.47 (1.23) | 0.33 (1.27) | 0.60 (2.32) | −0.22 (−0.55) |

% TODO: discuss the Fama-MacBeth table -- the sign on Dur, what happens to BM and GP
% once Dur is included, and how the OLS and WLS results differ.

### 3(e)

Decile portfolios are formed on $\text{BM}_{CZ}$, $\text{GP}_{CZ}$ and $Dur$, rebalanced
annually at June with NYSE breakpoints, both value-weighted and equal-weighted. Formation
at June of year $t$ uses the Chen and Zimmermann signals of that month together with the
duration observation carrying `FF.YEAR` $=t$, which Gonçalves documents as public at the
end of June of $t$; membership and weights are then held over July of $t$ through June of
$t+1$. $\text{Dec}^X_{p,\tau}$ is the average decile of signal $X$ among the firms in
portfolio $p$, weighted by the weight each firm carries in that portfolio, and is fixed at
the June formation month. A specification containing $k$ signals is estimated on the union
of those signals' decile portfolios, so 10 portfolios for a univariate specification, 20
for a bivariate one and 30 for (vii). Estimation is pooled OLS with Driscoll and Kraay
(1998) standard errors, over 618 months from July 1973 to December 2024, on the same
common sample of firms used in 3(d).

Coefficients are in percent per month **per decile**, with Driscoll–Kraay $t$-statistics
in parentheses.

| Spec | Weighting | $a$ | $b_{BM}$ | $b_{GP}$ | $b_{Dur}$ |
|---|---|---:|---:|---:|---:|
| (i) | VW | 0.61 (3.02) | 0.035 (1.43) |  |  |
| (ii) | VW | 0.55 (2.25) |  | 0.025 (1.18) |  |
| (iii) | VW | 1.20 (6.01) |  |  | −0.065 (−3.18) |
| (iv) | VW | −0.23 (−0.58) | 0.102 (2.86) | 0.095 (2.83) |  |
| (v) | VW | 1.26 (5.26) | 0.003 (0.11) |  | −0.081 (−3.35) |
| (vi) | VW | 1.45 (4.43) |  | −0.013 (−0.53) | −0.100 (−3.65) |
| (vii) | VW | 1.77 (2.33) | −0.025 (−0.46) | −0.027 (−0.57) | −0.122 (−2.64) |
| (i) | EW | 0.53 (2.07) | 0.091 (4.18) |  |  |
| (ii) | EW | 0.74 (2.49) |  | 0.052 (3.63) |  |
| (iii) | EW | 1.55 (6.37) |  |  | −0.097 (−6.12) |
| (iv) | EW | −0.21 (−0.66) | 0.125 (5.31) | 0.094 (5.99) |  |
| (v) | EW | 1.15 (4.07) | 0.055 (1.62) |  | −0.078 (−2.69) |
| (vi) | EW | 1.69 (5.07) |  | −0.008 (−0.40) | −0.114 (−5.08) |
| (vii) | EW | 0.66 (0.95) | 0.079 (1.56) | 0.045 (1.23) | −0.061 (−1.23) |

Consistent with footnote 10, the univariate slopes reproduce the corresponding HML
averages of 3(c) once scaled by the nine decile steps: the value-weighted $b_{BM}$ of
$0.035$ implies $0.32\%$ per month against the $0.370\%$ HML reported in scheme (i).

% TODO: discuss the panel table -- the sign and robustness of Dec^Dur, what happens to
% Dec^BM and Dec^GP once duration is included, the VW/EW contrast, and how these results
% compare with the firm-level Fama-MacBeth estimates of 3(d).

##  Question 4


### 

Average excess log yields, log forward rates and log annual returns (Fama-Bliss discount bonds; $xy$ averaged over 871 months from June 1952 to December 2024, $xf$ over 871 months from June 1952 to December 2024, and $xr$ over 859 months from June 1953 to December 2024), in percent:

| $H$ | average $xy^{(H)}_{b,t}$ | average $xf^{(H)}_{b,t}$ | average $xr^{(H)}_{b,t}$ |
|---|---|---|---|
| 2 | 0.1686 | 0.3372 | 0.3154 |
| 3 | 0.3278 | 0.6461 | 0.6069 |
| 4 | 0.4660 | 0.8805 | 0.8198 |
| 5 | 0.5639 | 0.9557 | 0.8719 |

where $xy^{(H)}_{b,t} = y^{(H)}_{b,t} - y^{(1)}_{b,t}$, $xf^{(H)}_{b,t} = f^{(H)}_{b,t} - y^{(1)}_{b,t}$ and
$xr^{(H)}_{b,t} = r^{(H)}_{b,t} - r^{(1)}_{b,t}$, with $y^{(H)}_{b,t} = \log(1 + Y^{(H)}_{b,t})$,
$f^{(H)}_{b,t} = H\,y^{(H)}_{b,t} - (H-1)\,y^{(H-1)}_{b,t}$ and $r^{(H)}_{b,t} = H\,y^{(H)}_{b,t-1} - (H-1)\,y^{(H-1)}_{b,t}$,
where $t-1$ is the same month one year earlier.

:::{figure} output/q4a_log_yields.png
:label: fig-q4a-yields
:width: 60%

Log yields $y^{(H)}_{b,t}$ of the Fama-Bliss discount bonds for $H = 1,\dots,5$, June 1952 to December 2024 (shown $\times 100$).
:::

:::{figure} output/q4a_forward_rates.png
:label: fig-q4a-forwards
:width: 60%

Log forward rates $f^{(H)}_{b,t}$ for $H = 2,\dots,5$, June 1952 to December 2024 (shown $\times 100$).
:::

:::{figure} output/q4a_log_returns.png
:label: fig-q4a-returns
:width: 60%

Log annual returns $r^{(H)}_{b,t}$ for $H = 2,\dots,5$, June 1953 to December 2024 (shown $\times 100$).
:::


### 

Regressions of the average annual hold-to-maturity excess return on the excess log yield,

$$
\frac{1}{H}\, xr^{(H)}_{b,t:t+H} = a^{(H)} + b^{(H)}\, xy^{(H)}_{b,t} + \varepsilon^{(H)}_t, \qquad xr^{(H)}_{b,t:t+H} = \sum_{h=1}^{H} xr^{(H-h+1)}_{b,t+h},
$$

estimated by OLS on overlapping monthly observations, where $t+h$ is the same month $h$ years later and $xr^{(1)}_{b,t} = 0$. The $t$-statistics use Hansen and Hodrick (1980) standard errors with $L = 12H - 1$ monthly lags, the number of months by which consecutive $H$-year dependent variables overlap; each regression uses every month $t$ for which its variables are available.

| $H$ | $b^{(H)}$ | $t$-statistic (Hansen-Hodrick) |
|---|---|---|
| 2 | 0.6774 | 3.57 | 
| 3 | 0.5316 | 3.21 | 
| 4 | 0.4141 | 2.52 | 
| 5 | 0.3453 | 2.30 |


### 

Regressions of the one-year excess log return on the excess log forward rate,

$$
xr^{(H)}_{b,t+1} = a^{(H)} + b^{(H)}\, xf^{(H)}_{b,t} + \varepsilon^{(H)}_{t+1},
$$

estimated by OLS on overlapping monthly observations, where $t+1$ is the same month one year later, using the 859 months with $t$ from June 1952 to December 2023 for every $H$. The $t$-statistics use Newey and West (1987, 1994) standard errors: Bartlett weights with the lag length chosen by the Newey and West (1994) rule, as in Question 2(b) ($L = 23, 23, 24, 23$ for $H = 2, 3, 4, 5$).

| $H$ | $b^{(H)}$ | $t$-statistic (Newey-West) |
|---|---|---|
| 2 | 0.6774 | 3.23 |
| 3 | 0.8887 | 3.35 |
| 4 | 1.1163 | 3.62 |
| 5 | 0.9641 | 2.91 |


### 

Cochrane and Piazzesi (2005) factor, estimated from

$$
\frac{1}{4}\sum_{H=2}^{5} xr^{(H)}_{b,t+1} = \theta_0 + cp_t + u_t, \qquad cp_t = \sum_{H=1}^{5} \theta_H\, f^{(H)}_{b,t},
$$

by OLS on overlapping monthly observations, where $t+1$ is the same month one year later and $f^{(1)}_{b,t} = y^{(1)}_{b,t}$, using the 859 months with $t$ from June 1952 to December 2023.

:::{figure} output/q4d_cp_nber.png
:label: fig-q4d-cp
:width: 80%

The figure plots the fitted value $\hat{\theta}_0 + cp_t$ of $\frac{1}{4}\sum_{H=2}^{5} xr^{(H)}_{b,t+1}$ (shown $\times 100$) for $t$ from June 1952 to December 2024; grey areas mark NBER recession months (FRED USREC = 1). Months after December 2023 use the coefficients estimated through December 2023.
:::


### 

Regressions of the one-year excess log return on the Cochrane-Piazzesi factor,

$$
xr^{(H)}_{b,t+1} = a^{(H)} + b^{(H)}\, (\hat{\theta}_0 + cp_t) + \varepsilon^{(H)}_{t+1},
$$

estimated by OLS on overlapping monthly observations, where $t+1$ is the same month one year later, using the 859 months with $t$ from June 1952 to December 2023 for every $H$. The regressor is the fitted value $\hat{\theta}_0 + cp_t$ plotted in Question 4(d). The $t$-statistics use Newey and West (1987, 1994) standard errors: Bartlett weights with the lag length chosen by the Newey and West (1994) rule, as in Question 2(b) ($L = 23, 23, 23, 23$ for $H = 2, 3, 4, 5$).

| $H$ | $b^{(H)}$ | $t$-statistic (Newey-West) |
|---|---|---|
| 2 | 0.4418 | 4.16 |
| 3 | 0.8274 | 4.18 |
| 4 | 1.2517 | 4.45 |
| 5 | 1.4791 | 4.25 |

