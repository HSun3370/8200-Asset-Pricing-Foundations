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
```



## Question 2

### 
nm 

```{include} output/q2a_gmm_table.md
```

```{figure} output/q2a_b_scatter.png
:label: fig-q2a-b
:width: 80%

$b$ coefficients of $M^*_t = a - b'xR_t$ by book-to-market decile (two-step GMM, 1927:07–2026:08).
```



## Question 3

###