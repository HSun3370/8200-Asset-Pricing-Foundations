# Homework 3

+++ {"part": "abstract"} 
+++
 

## Question 1
### 
The porfolio allocation problem is 
$$
\begin{align}
\max_{\bar \omega}~~ \mathbb{E}_t[R_{o,t+1} +\bar \omega' xR_{t+1}  ] - 0.5 \gamma_t (\bar \omega' \Sigma_{xR,t}\bar \omega +\Sigma_{R_o}+2\cdot\bar \omega' \mathbb{Cov}_t(R_{o,t+1},xR_{t+1})  ) ,
\end{align}
$$
where $\Sigma_{xR,t}:=\mathbb{Var}_t( xR_{t+1})$ and  $\Sigma_{R_o,t}:=\mathbb{Var}_t(R_{o,t+1} )$. FOC w.r.t $\bar \omega$:
$$ 
\mathbb{E}_t[  xR   ] - 0.5 \gamma_t (  2 \Sigma_{xR,t}\bar \omega  +2\cdot  \mathbb{Cov}_t(R_{o,t+1},xR_{t+1})  )  =0
$$
The optimal portfolio allocation is thus
$$
\bar \omega_{\gamma,t} = \frac{1}{\gamma_t}  \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR   ]  - \Sigma_{xR,t}^{-1}  \mathbb{Cov}_t(R_{o },xR ).
$$
When a risk-free asset exists, let $R_{o,t+1} = R_{f,t+1}$ and $\mathbb{Cov}_t(R_{o },xR) =0$. Thus, 

$$
\bar \omega_{\gamma,t} = \frac{1}{\gamma_t}  \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR   ] .
$$

###
Assume representative agent $\bar \omega_{\gamma,t} =\bar\omega_{m,t} $. Then we have 
$$
\begin{align}
\gamma_t \cdot \mathbb{Cov}_t(R_{w},xR ) &=\gamma_t \cdot \mathbb{Cov}_t(R_{o } +\bar \omega_{\gamma,t}' xR  ,xR ) \\
& = \gamma_t \cdot \mathbb{Cov}_t(R_{o }  ,xR )
+ \gamma_t \cdot \mathbb{Cov}_t( [\frac{1}{\gamma_t}  \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR   ]  - \Sigma_{xR,t}^{-1}  \mathbb{Cov}_t(R_{o },xR )]' xR  ,xR ) \\
& = \gamma_t \cdot \mathbb{Cov}_t(R_{o }  ,xR )  
+ \gamma_t \cdot \Sigma_{xR,t}   [\frac{1}{\gamma_t}  \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR   ]  - \Sigma_{xR,t}^{-1}  \mathbb{Cov}_t(R_{o },xR )]   \\
& = \mathbb{E}_t[  xR   ]   +  \gamma_t \cdot \mathbb{Cov}_t(R_{o }  ,xR )   - \gamma_t \cdot \mathbb{Cov}_t(R_{o }  ,xR )  \\
& =\mathbb{E}_t[  xR   ] 
\end{align} 
$$
Specifically, the SPF prices itself, which means that 
$$
\mathbb{E}_t[  xR_w ] = \gamma_t \cdot \mathbb{Cov}_t(R_{w}, xR_w  ) = \gamma_t \cdot\mathbb{Var}_t(R_{w}  ) -\gamma_t \cdot \mathbb{Cov}_t(R_{o},  R_w  )
$$

Thus, 
$$ 
\begin{align}
\mathbb{E}_t[  xR_j   ]  &= \gamma_t \cdot \mathbb{Cov}_t(R_{w},xR_j ) \\
&= \gamma_t \cdot   \frac{\mathbb{Cov}_t(R_{w},xR_j ) }{\mathbb{Var}_t(R_{w}  ) } \frac{  \mathbb{Var}_t(R_{w}  )}{ \mathbb{E}_t[  xR_w ]} \mathbb{E}_t[  xR_w ]\\
&= \beta_{j,t} \cdot  \mathbb{E}_t[  xR_w ]
\end{align}
$$


### Sharpe Ratio
$$
\mathbb{SR}_t = \frac{\mathbb{E}_t[ \bar \omega_t' xR_{t+1}  ]}{ \mathbb{Vol}_t [\bar \omega_t' xR_{t+1} ]} = \frac{\bar \omega_t' \mathbb{E}_t[  xR  ]}{ \sqrt {\bar \omega_t' \Sigma_{xR,t} \bar \omega_t }}
$$
FOC w.r.t $\bar \omega_t$:

$$
\frac{\partial \mathbb{SR}_t}{\partial \bar \omega_t}  = 
\frac{ \sqrt {\bar \omega_t' \Sigma_{xR,t} \bar \omega_t } \mathbb{E}_t[  xR  ]  }{  \bar \omega_t' \Sigma_{xR,t} \bar \omega_t } - \frac{\frac{  \Sigma_{xR,t} \bar \omega_t}{\sqrt {\bar \omega_t' \Sigma_{xR,t} \bar \omega_t }}\bar \omega_t'  \mathbb{E}_t[  xR  ]  }{  \bar \omega_t' \Sigma_{xR,t} \bar \omega_t } 
= 
\frac{  \bar \omega_t' \Sigma_{xR,t} \bar \omega_t   \mathbb{E}_t[  xR  ]   -    \bar \omega_t'  \mathbb{E}_t[  xR  ] \Sigma_{xR,t} \bar \omega_t }{  (\bar \omega_t' \Sigma_{xR,t} \bar \omega_t )^{3/2}}  =0
$$
We can get 
$$
 \bar \omega_t  = \frac{\bar \omega_t' \Sigma_{xR,t} \bar \omega_t }{\bar \omega_t'  \mathbb{E}_t[  xR  ] } ~~\Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR  ]
$$

Imposing $\mathbb{1}'\bar \omega_{max,t}  =1$, we can get 
$$\bar \omega_{max,t}  =\frac{\Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR  ]}. $$

This textbook method of deriving optimal sharpe ratio portfolio is too ad-hoc to me. I would prefer another method. First solve minimizing variance problem given porfolio weights constraint and target portfolio return $\mu$, then maximize the sharpe ratio by choosing target portfolio return $\mu$.

$$
\min_{\bar \omega_t} ~~ \frac{1}{2}\bar \omega_t' \Sigma_{xR} \bar \omega_t, ~~~s.t. ~ \omega_t' \mathbb{E}_t[  xR  ] \geq\mu, 1 = \mathbb{1}'\bar \omega_{ t}'
$$
Lagrangian for this maximization problem is 
$$
L =\frac{1}{2} \bar \omega_t' \Sigma_{xR} \bar \omega_t + \lambda [\omega_t' \mathbb{E}_t[  xR  ] - \mu]+ \gamma [ \mathbb{1}'\bar \omega_{ t} -1]
$$
FOC is 
$$
\frac{\partial L}{\partial \omega_t'} = \Sigma_{xR} \bar \omega_t + \lambda \mathbb{E}_t[  xR  ] + \gamma  \mathbb{1},
$$
where 
$$
\bar \omega_t^* = \lambda  \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] + \gamma \Sigma_{xR}^{-1} \mathbb{1},
$$
and 
$$
 \bar \omega_t' \Sigma_{xR} \bar \omega_t = - \lambda \bar \omega_t' \mathbb{E}_t[  xR  ]- \gamma \bar \omega_t' \mathbb{1} =  - \lambda \mu - \gamma .
$$
The complementary slackness condition is 
$$
\lambda, \gamma \geq 0,  ~~\mathbb{1}'\bar \omega_{ t} -1 =0,  ~~\lambda [\omega_t' \mathbb{E}_t[  xR  ] - \mu] =0, ~~\omega_t' \mathbb{E}_t[  xR  ] - \mu \geq 0.
$$

As two conditions will eventually bind, on the left hand side of $\bar \omega_t^*$, let's multiply $\mathbb{E}_t[  xR  ]'$ and $\mathbb{1}'$ we can get
$$
\mathbb{E}_t[  xR  ]' \bar \omega_t^* = \mu = -\lambda ~\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] -\gamma ~\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{1}
$$
and 
$$
\mathbb{1}' \bar \omega_t^* = 1 = -\lambda ~\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] - \gamma ~\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}
$$
Two equation two unknown, we can solve $\lambda^*$ and $\gamma^*$ by
$$-\lambda^* = \frac{ \mu\cdot \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]\cdot\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - (\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ])^2 },~~-\gamma^* =  \frac{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] -\mu\cdot \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]\cdot\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - (\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ])^2 } $$
Thus, under the optimal portfolio weights, the minimal variance is 
$$
(\bar \omega_t' \Sigma_{xR} \bar \omega_t)^* =  \frac{ \mu^2\cdot \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - 2\mu \cdot \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] + \mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]\cdot\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - (\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ])^2 }. 
$$
The sharpe ratio is 
$$
\mathbb{SR}_t = \frac{\mu}{\sqrt{(\bar \omega_t' \Sigma_{xR} \bar \omega_t)^*}} = \left( \frac{    \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - 2\frac{1}{\mu }\cdot \mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] + \frac{1}{\mu^2 }\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]\cdot\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{1}  - (\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ])^2 } \right)^{-\frac{1}{2}}
$$
The maximizing sharpe ratio portfolio return is $$(\frac{1}{\mu})^* = \frac{\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}$$, thus
$$
\mathbb{E}_t[  xR_{max}  ] = \mathbb{E}_t[  xR  ]' \bar \omega_t^* = \frac{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }
$$
thus
$$
  \bar \omega_t^* = \frac{ \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }.
$$
The variance of maximum sharpe ratio portfolio is
$$
\mathbb{Var}_t[  xR_{max}  ] = \frac{ \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }'   \Sigma_{xR} \frac{ \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] } =  \frac{\mathbb{E}_t[  xR  ] \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{(\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] )^2}
$$

For the investor, the portfolio weigth is 

$$
\bar \omega_{\gamma,t} = \frac {\mathbb{Var}_t[  xR_{max}  ]}{\mathbb{E}_t[  xR_{max}  ]}  \Sigma_{xR }^{-1}\mathbb{E}_t[  xR   ] =  \frac{\mathbb{E}_t[  xR  ] \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}{(\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] )^2}  \frac {\mathbb{1}' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ] }{\mathbb{E}_t[  xR  ]' \Sigma_{xR}^{-1} \mathbb{E}_t[  xR  ]}  \Sigma_{xR }^{-1}\mathbb{E}_t[  xR   ] =  \bar \omega_t^*.
$$


###
Let us stack the excess return into a vector, and define 
$$
xR_{t+1} = [xR_{m,t+1},xR_{1,t+1}^H,...,xR_{J,t+1}^H]'
$$
The covariance matrix of this excess return vector is 
$$
\Sigma_{xR} =  diag~\{ \sigma^2_{m,t},\sigma^2_{\epsilon,1,y},...,\sigma^2_{\epsilon,J,y}     \}
$$,
and the expected return is 
$$
\mathbb{E}_t[  xR  ] = [ \mu_{m,t}, \alpha_{1,t},..., \alpha_{J,t} ]'
$$

The maximum sharpe ratio portfolio weight is thus
$$
\bar \omega_{max,t}  =\frac{\Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR  ]}{\mathbb{1}' \Sigma_{xR,t}^{-1}\mathbb{E}_t[  xR  ]}
=\frac{[\frac{\mu_{m,t}}{\sigma^2_{m,t}}, \frac{\alpha_{1,t}}{\sigma^2_{\epsilon,1,y}},..., \frac{\alpha_{J,t} }{\sigma^2_{\epsilon,J,y}}]' }{\frac{\mu_{m,t}}{\sigma^2_{m,t}}+ \frac{\alpha_{1,t}}{\sigma^2_{\epsilon,1,y}}+...+ \frac{\alpha_{J,t} }{\sigma^2_{\epsilon,J,y}}}
$$
Thus, 
$$
\bar \omega_{m,t} = \frac{    \mu_{m,t} / \sigma^2_{m,t} }{\mu_{m,t} / \sigma^2_{m,t}  + \sum_j^J  \alpha_{j,t} / \sigma^2_{\epsilon,j,y}   }
$$
and 
$$
\bar \omega_{j,t} = \frac{   \alpha_{j,t}  \sigma^2_{\epsilon,j,y} }{\mu_{m,t} / \sigma^2_{m,t}  + \sum_j^J  \alpha_{j,t} / \sigma^2_{\epsilon,j,y}   }
$$

<!-- The expected return for maximum sharpe ratio portfolio is 
$$
\mathbb{E}_t[  xR_{max} ] =  \mathbb{E}_t[   \omega_{m,t} xR_{m,t+1} + \sum_j \omega_{j,t}^H xR^H_{j,t+1}   ] = \omega_{m,t} \mu_{m,t} + \alpha_{H,t}
$$
and the variance of that portfolio is 
$$
\mathbb{Var}_t[  xR_{max} ] = \omega_{m,t}^2 \sigma_{m,t}^2 + \sigma_{\epsilon,t}^2
$$ -->


The sharpe ratio square of market portfolio is $\mathbb{SR}[ xR_m]^2 = \frac{\mu_{m,t}^2}{\sigma_{m,t}^2}$, and the sharpe ratio square for the single hedge portfolio is 
$$
\begin{align}
\mathbb{SR}[ xR_{max}]^2 &=  \frac{[(1-\pi_{H,t} )\mu_{m,t} + \pi_{H,t} \alpha_{H,t}]^2}{(1-\pi_{H,t} )^2 \sigma_{m,t}^2 + \pi_{H,t}^2 \sigma^2_{\epsilon,t} } \\
 &= \frac{ (1-\pi_{H,t} )^2\mu_{m,t}^2 + \pi_{H,t}^2 \alpha_{H,t}^2 + 2  \pi_{H,t}(1-\pi_{H,t} )\mu_{m,t}  \alpha_{H,t}  }{(1-\pi_{H,t} )^2 \sigma_{m,t}^2 + \pi_{H,t}^2 \sigma^2_{\epsilon,t} }
\end{align}
$$

From equation 1.12, we have 
$$
\pi_{H,t} = \frac{\alpha_H/ \sigma_{\epsilon,t}^2}{\mu_{m,t}/\sigma^2_{m,t} + \alpha_H/ \sigma_{\epsilon,t}^2}, ~~1- \pi_{H,t} = \frac{\mu_{m,t}/\sigma^2_{m,t}}{\mu_{m,t}/\sigma^2_{m,t} + \alpha_H/ \sigma_{\epsilon,t}^2}, 
$$

The, the sharpe ratio square for the single hedge portfolio is 
$$
\begin{align}
\mathbb{SR}[ xR_{max}]^2 &=  \frac{[(1-\pi_{H,t} )\mu_{m,t} + \pi_{H,t} \alpha_{H,t}]^2}{(1-\pi_{H,t} )^2 \sigma_{m,t}^2 + \pi_{H,t}^2 \sigma^2_{\epsilon,t} } \\
 &=  \frac{[\mu_{m,t}^2/\sigma^2_{m,t} + \alpha_H^2/ \sigma_{\epsilon,t}^2]^2 }{\mu_{m,t}^2/\sigma^2_{m,t} + \alpha_H^2/ \sigma_{\epsilon,t}^2}
\end{align} = \mu_{m,t}^2/\sigma^2_{m,t} + \alpha_H^2/ \sigma_{\epsilon,t}^2
$$

The difference between two sharpe ratio is 
$$ 
\mathbb{SR}[ xR_{max}]^2-\mathbb{SR}[ xR_m]^2  =\alpha_H^2/ \sigma_{\epsilon,t}^2.
$$
and thus
$$ 
\alpha_H/ \sigma_{\epsilon,t}=\sqrt{\mathbb{SR}[ xR_{max}]^2-\mathbb{SR}[ xR_m]^2   }.
$$

Reduced-form multifactor models are looking for high $\alpha_H/ \sigma_{\epsilon,t}$, which is equivalent to maximize the sharpe ratio of factors. And we know that the maximium sharpe ratio portfolios is SDF which prices all assets, so multifactor models are constructing a SDF that with higher sharpe ratio to price all assets. 



### 

**(ii) Regressions of each PC on Mkt-RF**

```{include} output/q1e_table_mkt.md
```

**(iii) Regressions of each PC on Mkt-RF, HML and SMB**

```{include} output/q1e_table_ff3.md
```
 
3-factor tries to explain the covement of stock excess returns. They explains large parts of variations of first three components. The limitation is about economic meaning. Even through we can find factors that explains covement, we can't learn from the factor about the economic meaning and any risk-return relations. 


##

### 

Subtract $\log W_t$ on both side of the equation (2.1), we have 
$$
\log \frac{V_t}{W_t} = \max_{C_t, \bar \omega_t} ~ (1-\delta) \cdot \log \frac{C_t}{W_t} + \frac{\delta}{1-\gamma} \log \mathbb{E}_t [(\frac{V_{t+1}}{W_{t+1} } \frac{W_{t+1}}{W_t})^{1-\gamma}]
$$

For notation simplicity, let me define 
$$
vw_t := \log \frac{V_t}{W_t}, ~~cw_t = \log \frac{C_t}{W_t}
$$

Plug in the log wealth growth $\log W_{t+1}/W_t = \log  R_{w,t+1} + \log (1-\exp (cw_t))$
$$
 vw_t = \max_{cw_t, \bar \omega_t} ~ (1-\delta) \cdot cw_t + \frac{\delta}{1-\gamma} \log \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \} ]
$$


FOC w.r.t $cw_t$ we can get

$$
 \partial_{cw} vw_t =   (1-\delta)   +  \delta  \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \} ]^{-1} \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \}(\partial_{cw} vw_{t+1} +  \frac{-\exp cw_t}{1-\exp cw_t}   )]  
$$

Guess and verify: I guess $cw_t = \log (1-\delta)$ solves FOC, then verify
$$
\begin{align}
 &-\partial_{cw} vw_t +  (1-\delta)   + \delta \frac{-\exp cw_t}{1-\exp cw_t}+  \delta  \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \} ]^{-1} \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \} \partial_{cw} vw_{t+1}  ]  \\
&=   \delta  \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \} ]^{-1} \mathbb{E}_t [\exp \{  ( 1 -\gamma ) vw_{t+1} +( 1 -\gamma ) r_{w,t+1}  + ( 1 -\gamma ) \log (1-\exp  cw_t )   \}  \partial_{cw} vw_{t+1}  ] -\partial_{cw} vw_t\\
&= 0
\end{align} 
$$

The last equation is true by the definition of $vw


###





