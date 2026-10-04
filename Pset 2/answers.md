# Homework 2

+++ {"part": "abstract"} 
+++
 

## Question 1


### 
Yes, see reasoning in 1b.
###
Define the payoff as $X$, price vector as $P$, and price of contingent claim as $p$.
Solve the linear equation $X p = P$ by elimination, we got  

$$
[X, P] \;-->\;
\begin{bmatrix}
1 & 0 & 0 & 0.2 \\
0 & 1 & 0 & 0.4 \\
0 & 0 & 1 & 0.2
\end{bmatrix}
$$
Thus, we have complete markets in this economy and the price of continguent claim for state of nature 1, 2,3 are $[0.2,0.4,0.2]'$


###
The price should be 
$$[30,20,10] \times [0.2,0.4,0.2]' = 16$$


###
SDP in this economy is calucalteed by $M(i) = \frac{p(i)}{\pi(i)}$
$$ M = [0.8, 0.8,0.8]'. $$
This economy satisfies no-arbitrage as all the prices of contingent claims are strictly positive and unique. 
SDF remains the same accross all states, which means that agents in this economy are risk neutral. 

###

$$
P_D = \sum_i \pi(i) M(i) X(i) = \frac{1}{4} \cdot 0.8\cdot 30 + \frac{1}{2} \cdot 0.8\cdot 20 + \frac{1}{4} \cdot 0.8\cdot 10 = 16
$$


```{raw:typst}
#set page(margin: auto)
#let diff = sym.partial
```



## Question 2

###  

```{include} output/q2a_gmm_table.md
```

```{figure} output/q2a_b_scatter.png
:label: fig-q2a-b
:width: 80%

$b$ coefficients of $M^*_t = a - b'xR_t$ by book-to-market decile (two-step GMM, 1927:07–2026:08).
```

### 

```{include} output/q2b_gmm_table.md
```

```{figure} output/q2b_b_scatter.png
:label: fig-q2b-b
:width: 80%

$b$ coefficients of $M^*_t = a - b'xR_t$ by momentum decile (two-step GMM, 1927:07–2026:08).
```

The sample correlation between $M^*_t$ from Question 2(a) (BM deciles) and $M^*_t$ from Question 2(b) (MOM deciles) is $\text{Corr}(M^*_{BM,t}, M^*_{MOM,t}) = 0.3555$ (monthly, 1927:07–2026:08, $T = 1190$).

This correlation means that two SDF has $35.55\%$ explanation power pricing same portion of return variation. 

### 

```{include} output/q2c_gmm_table.md
```

```{figure} output/q2c_b_scatter.png
:label: fig-q2c-b
:width: 80%

$b$ coefficients of $M^*_t = a - b'xR_t$ estimated on the 20 BM and MOM decile portfolios jointly, by decile (blue: BM portfolios; red: MOM portfolios; two-step GMM, 1927:07–2026:08).
```

```{include} output/q2c_sharpe_table.md
```

SDF constructed using 20 portfolios has higher sharpe ratio than other two. Higher sharpe ratio means pricing power is high. As in the linear pricing SDF setting, the highest sharpe ratio portfolio can price every return.



###

```{include} output/q2d_pricing_errors_table.md
```

Every SDF perfectly prices excess returns of portfolios where SDF comes from, as in each case it is just identified. 
However, SDF from some portfolios cannot perfectly price returns of other portfios. We can increase the portfolio number to increase pricing ability. 


### 

Estimates of $M^*_t = a - b'xR_t$ on the 20 BM and MOM decile portfolios using data until December 1989:

```{include} output/q2e_gmm_table.md
```

```{include} output/q2e_pricing_errors_table.md
```


Out of sample pricing errors are non-zero for all portfolios, which means the true values for $a,b$ are time varying. 



## Question 3

###

The portfolio choice problem is 

$$
\max_{\bar \omega_t} V= \frac{1}{1-\gamma} E [ (W_t R_{f,t+1} + \bar \omega_t' W_t xR_{t+1})^{1-\gamma} ] 
$$
FOC w.r.t $\bar \omega_t$,  
$$
\frac{\partial}{\partial \bar \omega_t}V =   E [ ( R_{f,t+1} + \bar \omega_t' xR_{t+1})^{ -\gamma}  W_t^{1-\gamma} xR_{t+1} ] =0 
$$
We can put $W_t^{1-\gamma}$ outside of expectation as it is known at time $t$ and divide it from both sides. Then the FOC becomes
$$
E [ R_{ \omega_t^*,t+1}  ^{ -\gamma}  xR_{t+1} ] =E [ ( R_{f,t+1} + \bar \omega_t^*' xR_{t+1})^{ -\gamma}  xR_{t+1} ] =0.
$$
Thus, $M_t = R_{ \omega_t^*,t+1}  ^{ -\gamma}$ prices all excess returns.


###

```{include} output/q3b_gmm_table.md
```

### 

```{include} output/q3c_gmm_table.md
```

### 

```{include} output/q3d_gmm_table.md
```

### 

```{include} output/q3e_gmm_table.md
```





