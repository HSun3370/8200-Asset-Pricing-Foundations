# Homework 2

+++ {"part": "abstract"} 
+++
 

## Question 1


### 
###
Solve the linear equation $X p = P$ by elimination, we got  

$$ 
[X,P] -> 
[[1,0,0, 0.2],
[0,1,0,0.4],
[0,0,1,0.2]]
$$
Thus, we have complete markets in this economy and the price of continguent claim for state of nature 1, 2,3 are $[0.2,0.4,0.2]'$


###
The price should be 
$$[30,20,10] \times [0.2,0.4,0.2]' = 16$$


###
SDP in this economy is calucalteed by $M(i) = \frac{p(i)}{\pi(i)}$
$$ M = [0.8, 0.8,0.8]'. $$
This economy satisfies no-arbitrage as all the price of contingent claims are strictly positive. 
SDF remains the same accross all states, which means that agents in this economy are risk neutral. 

###

$$
P_D = \sum_i \pi(i) p(i) X(i) = \frac{1}{4} \cdot 0.8\cdot 30 + \frac{1}{2} \cdot 0.8\cdot 20 + \frac{1}{4} \cdot 0.8\cdot 10 = 16
$$


```{raw:typst}
#set page(margin: auto)
```