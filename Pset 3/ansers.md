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
\bar \omega_{m,t} = \frac{    \mu_{m,t} / \sigma^2_{m,t} }{\mu_{m,t} / \sigma^2_{m,t}  + \sum_j^J  \alpha_{j,t}  \sigma^2_{\epsilon,j,y}   }
$$
and 
$$
\bar \omega_{j,t} = \frac{   \alpha_{j,t}  \sigma^2_{\epsilon,j,y} }{\mu_{m,t} / \sigma^2_{m,t}  + \sum_j^J  \alpha_{j,t}  \sigma^2_{\epsilon,j,y}   }
$$
 