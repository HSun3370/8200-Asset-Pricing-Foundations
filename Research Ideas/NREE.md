# Noisy Rational Expectation Equilibrium


## Standard Model
Let us start with the most basic model, and then see the implication of this model when generalized, e.g. heterogenous agents with different risk aversion level, market power(market microstructure style). 


### Assets

- Two period $t=0,1$
- One riskless asset with deterministic return r >1 with perfect elastic supply.
- $N$ risky asset with payoffs $f \sim N(\mu,\Sigma)$.
- Risky assets are scarse and supply $\bar x + x$, where $x \sim N(0,\sigma_x^2 I) $

<span style="color:gray">
Can we make the $\mu$ bayesian style? Say, $\mu$ is also a random variable. 
We have good results when payoff $f$ is in discrete probability space. In multivariate normal settings, the law of one price and pricing kernal is not very obvious? What happen if probability state is discrete?
</span>




### Agent

Agent $i$ maximizes expected Constant Absolute Risk Averse(CARA) utiltiy function over second period payoff,

$$ E_i [U(X) ] =E_i[ - \exp (- \rho X)].$$

In this model, all payoffs are linear combinations of the payoffs of one riskless asset and $N$ risky asset. So $X$ follows multivariate normal distribution. 
Maximizing expected utility becomes maximizing mean variance trade-off $E_i(X) - \frac{\rho}{2}VAR_i(X) $. Agent $i$ buys $q_i$ risky assets and spends $q_i' p$ on risky assets with payoff $q_i' f$. The remaining wealth $W_{0,i} -q_i' p $ goes to riskless asset with payoff $(W_{0,i} -q_i' p) r $. 
The portfolio choice problem by maximizing expected utility $E_i [U_i]$ is  
$$
\max_{q_i} ~~ (W_{0,i} -q_i' p) r + q_i' E_i [f]  - \frac{\rho}{2} q_i' VAR_i(f) q_i
$$
and the optimal portfolio choice is
$$
q_i^* = \frac{1}{\rho}~ [VAR_i(f)]^{-1} \left( E_i [f] - p  r \right).
$$
 
- $\rho = -\frac{U''}{U'}$: absolute risk aversion parameter. Higher risk averse level detains willingness to hold risky asset.
- $[VAR_i(f)]^{-1}$: the precision of the inference of $f$. Uncertainty detains willingness to hold risky asset.
- Agent takes price $p$ as given, which determines all three components $[VAR_i(f)]^{-1}$, $E_i [f]$ and $p  r$.


### Information Set
- Agent $i$ forms beliefs and expectations based on information $\mathcal I_i$ she observed.
- $\mathcal I_i = \{s_i, p\}$ both public and private information
- $s_i$: private signal observed by agent $i$
- $p$: price vector observed by every agent
- $E[f|\mathcal I_i]$, $Var[f|\mathcal I_i]$: Agent $i$ uses information $\mathcal I_i$ to form expectations. 
- $f$ is realized but unobservable. Agent needs to infer $f$. 

Agent $i$ has received noisy private signal 
$$
s_i = f + \epsilon_i, ~~  \epsilon_i \sim_{IID} ~N(0,\Sigma_{\epsilon,i}),
$$
the expectation formed based on private information is 
$$
E[f| s_i] = s_i, Var[f|s_i]^{-1} =  \Sigma_{\epsilon,i}^{-1}.
$$

Agent $i$ can also extract information from price signal $p$, by assuming the price is reflecting $f$ and $x$ in linear form, 
$$
p = A + B f + C x,
$$
the expectation formed based on public information is
$$
E[f| p] = B^{-1}(p-A), Var[f|p]^{-1} = ( B^{-1}C (B^{-1}C)^{-1} )^{-1} :=  \Sigma_{p}^{-1} .
$$

Prior belief says
$$
f \sim N(\mu,\Sigma)
$$
the pior expectations are
$$
E[f ] = \mu, Var[f ]^{-1} =  \Sigma^{-1} .
$$


Doing Bayesian updates, the total precision is
$$
Var[f|\mathcal I_i]^{-1} = Var[f ]^{-1} + Var[f|s_i]^{-1 } +  Var[f|p]^{-1} =  \Sigma^{-1} +  \Sigma_{\epsilon,i}^{-1} +\Sigma_{p}^{-1}
$$
and the expected payoff is 
$$
E[f|\mathcal I_i] = Var[f|\mathcal I_i] (   \Sigma^{-1}  \mu +  \Sigma_{\epsilon,i}^{-1} s_i +\Sigma_{p}^{-1} B^{-1}(p-A)  )
$$


### Equilibrium Condition

Assume agent distribution is uniform. 



### Stochastic discount factor





### Market Power

If the number of investor is finite, $Pr(i)>0$. 

If the number of investor is infinite, then $Pr(i)=0$

If we can use probability tools to unify markets with market power together, using Convergence Analysis. 

By creating A "probability" 

