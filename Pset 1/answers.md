
# Homework 1

+++ {"part": "abstract"}
This is my abstract!
+++


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
Estimating $xR_{e,t+1} = a + b \cdot D_t/P_t + \varepsilon_t$ (the $H = 1$ case of
Equation 2.1) by OLS on $T = 1117$ monthly start dates (1927:12--2020:12) gives
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

