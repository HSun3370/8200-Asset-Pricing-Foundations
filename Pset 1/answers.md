
# Homework 1

+++ {"part": "abstract"}
This is my abstract!
+++


## Question 1

### Proof
Start from taking logarithm on both sides of return expression:
$$ \log R_{e,t+1} = \log (1 + \exp(\log D_{t+1} - \log P_{t+1})) + \log P_{t+1} - \log P_t$$
for simplicity, I denote $r_{e,t+1} = \log R_{e,t+1}$, $p_{t+1} = \log P_{t+1}$, $d_{t+1} = \log D_{t+1}$, and $dp_{t+1} =\log D_{t+1} -\log P_{t+1}$, 
then by taylor expansion on $dp_{t+1}$ as it is stationary with mean $\bar{dp}$, we get 

$$
\begin{align}
r_{e,t+1} = \log (1 + \exp(\bar{dp})) + \frac{\exp (\bar{dp})}{1 + \exp (\bar{dp})} (dp_{t+1} - \bar{dp})  + p_{t+1} - p_t .
\end{align}
$$

Denote $\kappa  = 1/(1+ \exp{(\bar{dp}}))$, and $\kappa _0 = \log (1 + \exp(\bar{dp})) - \bar{dp}/(1+ \exp{(\bar{dp}})) = -\log \kappa - (1-\kappa) \log (1/\kappa -1)$. The log linearization turns to be

$$\begin{align}
r_{e,t+1} = \kappa_0 + (1-\kappa)  dp_{t+1}   + p_{t+1} - p_t .
\end{align}$$

Move $p_t$ to LHS and other terms to RHS, we get

$$\begin{align}
 p_t&= \kappa_0 + (1-\kappa)  d_{t+1}   - r_{e,t+1}  + \kappa ~ p_{t+1} \\
&= \kappa_0 + (1-\kappa)  d_{t+1}   - r_{e,t+1} + \kappa ~ [\kappa_0 + (1-\kappa)  d_{t+2}   - r_{e,t+2}  + \kappa ~ p_{t+2} ] \\ 
&= \kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
 &~~~~~~~~~~~~+(1-\kappa) (d_{t+1}  + \kappa~ d_{t+2} + ... + \kappa^{H-1} d_{t+H})  \\
& ~~~~~~~~~~~~ -  [r_{e,t+1} +\kappa~r_{e,t+1} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
&~~~~~~~~~~~~+ \kappa^H p_{t+H} 
% \\
% p_t& = \kappa_0 \frac{1- \kappa^H}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} d_{t+h} - \sum_{h=1}^H \kappa^{h-1} r_{e,t+h} + \kappa^H p_{t+H}
\end{align}$$

The log dividend price ratio $dp_t$ then can be written as
 
$$
\begin{align}
dp_t &= -\kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
& ~~~~~~~~~~~~ +  [r_{e,t+1} +\kappa~r_{e,t+1} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
 &~~~~~~~~~~~~d_t-(1-\kappa) (d_{t+1}  + \kappa~ d_{t+2} + ... + \kappa^{H-1} d_{t+H})  \\ 
&~~~~~~~~~~~~- \kappa^H p_{t+H}   \\
&= -\kappa_0 (1 + \kappa + ... + \kappa^{H-1})  \\
& ~~~~~~~~~~~~ +  [r_{e,t+1} +\kappa~r_{e,t+1} + ... + \kappa^{H-1}  r_{e,t+H} ] \\ 
 &~~~~~~~~~~~~d_t - d_{t+1} + \kappa ~ (d_{t+1} - d_{t+2}) +  ... + \kappa^{H-1} (d_{t+H-1} -  d_{t+H}  ) \\ 
&~~~~~~~~~~~~ +  \kappa^{H } d_{t+H} - \kappa^H p_{t+H}  \\
&= \kappa_0 \frac{ \kappa^H-1}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} r_{e,t+h} - \sum_{h=1}^H  \kappa^{h-1} \Delta d_{t+h} + \kappa^H dp_{t+H}
\end{align}
$$ 
where $\Delta d_{t+1} := d_{t+1} - d_t$. Notice that above identity holds ex post, and it should also hold when taking conditional expectation at time t. Then we get the equation

$$
\begin{align}
dp_t  = \kappa_0 \frac{ \kappa^H-1}{1- \kappa} + \sum_{h=1}^H \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum_{h=1}^H  \kappa^{h-1} \mathbb E_t \Delta  d_{t+h} + \kappa^H \mathbb E_t dp_{t+H}
\end{align}
$$ 

Imposing no-bubble condition and let $H \to \infty $, where
$$ \lim_{H\to \infty} \kappa^H \mathbb E_t dp_{t+H} = 0$$
, then we have equation (1.3)

$$
\begin{align}
dp_t  = \kappa_0 \frac{  -\kappa_0}{1- \kappa} + \sum_{h=1}^\infty \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum_{h=1}^\infty  \kappa^{h-1} \mathbb E_t \Delta  d_{t+h} 
\end{align}
$$ 


### 





###




### Alternative log linear present value identity:
Use same trick  
$$ 
R_{e,t+1} =  \frac{P_{t+1}+D_{t+1}}{ D_{t+1}  } \frac{D_{t+1} }{D_{t }   }  \frac {D_{t }   } {P_t + D_t} \frac  {P_t + D_t} {P_t} 
$$
, log one period return can be written as 
$$
\begin{align}
r_{e,t+1} =  -\log (1 - e^{-dy_{t+1}}) + \Delta d_{t+1} + \log (1 - e^{-dy_t}) + dy_t
\end{align}
$$
, where $dy_t := \log (1+\frac{D_t}{P_t})$, $\log (1 - e^{-dy_t})  =  \log \frac {D_{t }   } {P_t + D_t}$.

Apply Taylor expansion on $\log (1 - e^{-dy_t})$ over $dy_t$ with mean $\bar {dy}$, we have 
$$
\begin{align}
\log (1 - e^{-dy_t}) = \log (1 - e^{-\bar {dy}}) + \frac{e^{-\bar {dy}}}{1 - e^{-\bar {dy}}} ( dy_t -\bar {dy})
+O(dy_t^2)
\end{align}
$$
Let $\kappa = e^{-\bar{dy}}$ to simplify the expression, 
$$
\begin{align}
\log (1 - e^{-dy_t}) = \log (1 - \kappa) + \frac{\kappa}{1 - \kappa } ( dy_t -\bar {dy})
+O(dy_t^2)
\end{align}
$$
Then the return is log linearized as
$$
\begin{align}
r_{e,t+1} =  -\frac{\kappa}{1 - \kappa } ( dy_{t+1} -\bar {dy}) + \Delta d_{t+1} + \frac{\kappa}{1 - \kappa } ( dy_t -\bar {dy}) + dy_t
\end{align}
$$
and 
$$
\begin{align}
  \frac{dy_t}{1 - \kappa }   &=     r_{e,t+1} - \Delta d_{t+1}  +  \kappa  ~ \frac{ dy_{t+1}}{1 - \kappa } \\
   &=    r_{e,t+1} - \Delta d_{t+1}  \\
   &~~~~~~~~~~+  \kappa ~  [   r_{e,t+2} - \Delta d_{t+2}  +  \kappa ~ \frac{ dy_{t+2}}{1 - \kappa } ] \\
   &=    r_{e,t+1} - \Delta d_{t+1} + \kappa ~  [   r_{e,t+2} - \Delta d_{t+2} ] \\
   &~~~~~~~~~~ + ...+  \kappa^{H-1} ~  [   r_{e,t+H} - \Delta d_{t+H} ] + \kappa^H \frac{dy_{t+H}}{1 - \kappa } \\
   &=\sum^H_{h=1} \kappa^{h-1} r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1} \Delta d_{t+h} + \kappa^H \frac{dy_{t+H}}{1 - \kappa }
\end{align}
$$
Thus, the log linearization identity is 
$$
\begin{align}
  dy_t    =(1 - \kappa)(\sum^H_{h=1} \kappa^{h-1} r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1} \Delta d_{t+h}) + \kappa^H  dy_{t+H}  
\end{align}
$$
Take conditional expectaion at time $t$, identity also holds
$$
\begin{align}
  dy_t    =(1 - \kappa)(\sum^H_{h=1} \kappa^{h-1} \mathbb E_t r_{e,t+h} - \sum^H_{h=1} \kappa^{h-1}\mathbb E_t\Delta d_{t+h}) + \kappa^H \mathbb E_t dy_{t+H}  
\end{align}
$$
When imposing no-bubble assumption, the last term vanishes with $h\to \infty$,
$$ \lim_{h\to \infty} \kappa^H E_t \log (\frac{P_t + D_t}{P_t}) < \kappa^H E_t [1+ \log (\frac{  D_t}{P_t})] \to 0 $$

## Question 2