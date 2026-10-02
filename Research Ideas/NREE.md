# Noisy Rational Expectation Equilibrium

+++ {"part": "abstract"}
I worked on the standard model first, and then extend it to explain possible asset pricing puzzles. 
The goal is to explain Lu's puzzle and term structure of dividend stripes.
+++
 

```{raw:typst}
#set page(margin: auto)
```

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
Note that different agent $i,j$ may not have the same precise signal, so $\Sigma_{\epsilon,i}$ and $\Sigma_{\epsilon,j}$ have not to be equal.
Agent $i$ can also extract information from price signal $p$, by assuming the price is reflecting $f$ and $x$ in linear form, 
$$
p = A + B f + C x,
$$
<span style="color:grey">
$\sum_i W_{0,i}$ doen't show up in pricing equation because of CARA assumption.
</span>
The expectation formed based on public information is

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
E[f|\mathcal I_i] = Var[f|\mathcal I_i] (   \Sigma^{-1}  \mu +  \Sigma_{\epsilon,i}^{-1} s_i +\Sigma_{p}^{-1} B^{-1}(p-A)  ).
$$

The optimal investment for agent $i$ is thus

$$
q_i^* = \frac{1}{\rho} [   \Sigma^{-1}  \mu  +  \Sigma_{\epsilon,i}^{-1} s_i  +\Sigma_{p}^{-1} B^{-1}(p-A)  ] - \frac{1}{\rho} [\Sigma^{-1} +  \Sigma_{\epsilon,i}^{-1} +\Sigma_{p}^{-1}] ~ pr
$$

### Equilibrium Condition

For simplicity, let's work on the simplest case where population is uniformly distributed.

- A continuum of investors indexed by $i \in [0,1]$. Each takes prices as given, and has an initial wealth $W_{0,i}$.

The equilibrium equates asset supply and demand:
$$
\bar x + x = \int_0^1 \frac{1}{\rho} [   \Sigma^{-1}  \mu  +  \Sigma_{\epsilon,i}^{-1} s_i  +\Sigma_{p}^{-1} B^{-1}(p-A)  ] - \frac{1}{\rho} [\Sigma^{-1} +  \Sigma_{\epsilon,i}^{-1} +\Sigma_{p}^{-1}] ~ pr ~ di \\
=\frac{1}{\rho} [   \Sigma^{-1}  \mu  + \int_0^1 \Sigma_{\epsilon,i}^{-1} s_i di +\Sigma_{p}^{-1} B^{-1}(p-A)  ] - \frac{1}{\rho} [\Sigma^{-1} + \int_0^1 \Sigma_{\epsilon,i}^{-1} di +\Sigma_{p}^{-1}] ~ pr
$$

To simplify notations, let's define $\bar V = (\int_0^1 \Sigma_{\epsilon,i}^{-1} di)^{-1}$, and 
$$
\int_0^1 \Sigma_{\epsilon,i}^{-1} s_i di =\int_0^1 \Sigma_{\epsilon,i}^{-1} f di + \int_0^1 \Sigma_{\epsilon,i}^{-1} \epsilon_i di =  \bar V^{-1} f.
$$

Aggregate demand keeps the same form as individual demand but aggregating the precision of each individual's signal precision: 
$$
\bar x + x  
=\frac{1}{\rho} [   \Sigma^{-1}  \mu  + \bar V^{-1} f +\Sigma_{p}^{-1} B^{-1}(p-A)  ] - \frac{1}{\rho} [\Sigma^{-1} + \bar V^{-1} +\Sigma_{p}^{-1}] ~ pr.
$$
Clean everything up and solve $A$, $B$ and $C$:

$$
 [\Sigma^{-1} + \bar V^{-1} +\Sigma_{p}^{-1}] ~ pr     
=  [   \Sigma^{-1}  \mu  + \bar V^{-1} f +\Sigma_{p}^{-1} B^{-1}(p-A)  ] -   \rho (\bar x + x  ).
$$

To save notation, let $K := \Sigma^{-1} + \bar V^{-1} +\Sigma_{p}^{-1}$ denote the aggregate posterior precision.

**Step 1: Collect the $p$ terms.** Move $\Sigma_{p}^{-1} B^{-1} p$ to the left-hand side:
$$
\underbrace{\left( K r - \Sigma_{p}^{-1} B^{-1} \right)}_{=: M} p
= \left[ \Sigma^{-1}\mu - \Sigma_{p}^{-1} B^{-1} A - \rho \bar x \right] + \bar V^{-1} f - \rho\, x ,
$$
so the price implied by market clearing is
$$
p = M^{-1}\left[ \Sigma^{-1}\mu - \Sigma_{p}^{-1} B^{-1} A - \rho \bar x \right] + M^{-1} \bar V^{-1} f - \rho M^{-1} x .
$$

**Step 2: Match coefficients with the conjecture $p = A + Bf + Cx$.** The equation must hold for every realization of $f$ and $x$, so
$$
\begin{aligned}
A &= M^{-1}\left[ \Sigma^{-1}\mu - \Sigma_{p}^{-1} B^{-1} A - \rho \bar x \right], \\
B &= M^{-1} \bar V^{-1}, \\
C &= -\rho M^{-1}.
\end{aligned}
$$
This looks like a fixed point, because $M$ and $\Sigma_p$ both depend on $B$ and $C$.

**Step 3: Solve the information part first.** Divide $C$ by $B$:
$$
B^{-1} C = \left( \bar V M \right) \left( -\rho M^{-1} \right) = -\rho \bar V .
$$
$M$ cancels, so the price signal is known without solving for $B$ and $C$ separately:
$$
B^{-1}(p - A) = f + B^{-1} C x = f - \rho \bar V x .
$$
The price is a noisy signal of $f$, and the noise is larger when agents are more risk averse ($\rho$) or less informed ($\bar V$). With $x \sim N(0, \sigma_x^2 I)$ and $\bar V$ symmetric, the noise variance of the price signal is
$$
\Sigma_{p} = (B^{-1}C)\, \sigma_x^2 I\, (B^{-1}C)' = \rho^2 \sigma_x^2\, \bar V \bar V ,
\qquad
\Sigma_{p}^{-1} = \frac{1}{\rho^2 \sigma_x^2}\, \bar V^{-1} \bar V^{-1} .
$$
So $\Sigma_p$, and therefore $K = \Sigma^{-1} + \bar V^{-1} + \Sigma_{p}^{-1}$, depends only on primitives. The fixed point is gone.

**Step 4: Solve $B$.** Multiply $B = M^{-1} \bar V^{-1}$ by $M$:
$$
M B = \left( K r - \Sigma_{p}^{-1} B^{-1} \right) B = K r B - \Sigma_{p}^{-1} = \bar V^{-1}
\quad \Longrightarrow \quad
B = \frac{1}{r} K^{-1} \left( \bar V^{-1} + \Sigma_{p}^{-1} \right).
$$

**Step 5: Solve $C$.** Use $B^{-1}C = -\rho \bar V$ from Step 3:
$$
C = B\,(B^{-1}C) = -\frac{\rho}{r} K^{-1} \left( \bar V^{-1} + \Sigma_{p}^{-1} \right) \bar V .
$$

**Step 6: Solve $A$.** Multiply the $A$ equation by $M$; the $\Sigma_{p}^{-1} B^{-1} A$ terms cancel:
$$
\left( K r - \Sigma_{p}^{-1} B^{-1} \right) A = \Sigma^{-1}\mu - \Sigma_{p}^{-1} B^{-1} A - \rho \bar x
\quad \Longrightarrow \quad
A = \frac{1}{r} K^{-1} \left( \Sigma^{-1}\mu - \rho \bar x \right).
$$

**Step 7: Equilibrium price.** Putting $A$, $B$ and $C$ together,
$$
p\, r = K^{-1} \left[ \Sigma^{-1}\mu + \left( \bar V^{-1} + \Sigma_{p}^{-1} \right) \left( f - \rho \bar V x \right) \right] - \rho K^{-1} \bar x .
$$
The first term is a precision-weighted average of the prior mean $\mu$ and the price signal $f - \rho \bar V x$; the weights $K^{-1}\Sigma^{-1}$ and $K^{-1}(\bar V^{-1} + \Sigma_{p}^{-1})$ sum to $I$. The last term is the risk premium for holding the average supply $\bar x$.

<div style="color:gray">

Check: $B$ must be invertible for the price to be informative. It is, since $K^{-1}$ and $\bar V^{-1} + \Sigma_{p}^{-1}$ are both positive definite.

</div>

 


### Stochastic discount factor

With heterogeneous information, there is no single SDF that every agent uses: each agent prices assets with her own marginal utility, under her own information set $\mathcal I_i$. So we first derive each agent's SDF, and then the SDF of an outside observer (an econometrician) who sees only the public information $p$.

Shorthand: $\mu_i := E[f|\mathcal I_i]$, $V_i := Var[f|\mathcal I_i]$, and $z := B^{-1}(p-A) = f - \rho \bar V x$ for the price signal.

**Step 1: Euler equation for agent $i$.** Terminal wealth is $W_{1,i} = (W_{0,i} - q_i'p)\, r + q_i' f$. The first-order condition of $\max_{q_i} E_i[-\exp(-\rho W_{1,i})]$ is
$$
E_i\left[ \exp(-\rho W_{1,i}) \, (f - p r) \right] = 0
\quad \Longrightarrow \quad
p = E_i\left[ m_i f \right],
\qquad
m_i := \frac{\exp(-\rho W_{1,i})}{r\, E_i\left[\exp(-\rho W_{1,i})\right]} .
$$
By construction $E_i[m_i] = 1/r$, so $m_i$ also prices the riskless asset.

**Step 2: Closed form.** The term $(W_{0,i} - q_i'p)\, r$ is known at $t=0$ and cancels between numerator and denominator. Since $f|\mathcal I_i \sim N(\mu_i, V_i)$, the normal moment generating function gives $E_i[\exp(-\rho q_i'f)] = \exp(-\rho q_i'\mu_i + \frac{\rho^2}{2} q_i' V_i q_i)$, so
$$
m_i = \frac{1}{r} \exp\left( -\rho\, q_i'(f - \mu_i) - \frac{\rho^2}{2}\, q_i' V_i q_i \right).
$$
Check: multiplying a normal density by $\exp(-\rho q_i' f)$ shifts its mean to $\mu_i - \rho V_i q_i$, so $E_i[m_i f] = (\mu_i - \rho V_i q_i)/r$. Setting this equal to $p$ gives $q_i = \frac{1}{\rho} V_i^{-1}(\mu_i - p r)$, which is the demand $q_i^*$ derived above.

**Step 3: The SDF is not unique.** Every agent observes $p$, so $\sigma(p) \subseteq \mathcal I_i$. By the law of iterated expectations,
$$
E\left[ m_i f \,|\, p \right] = E\left[ E[m_i f|\mathcal I_i] \,\big|\, p \right] = E[p\,|\,p] = p .
$$
So each $m_i$ also prices assets for the econometrician, and so does any average $\int_0^1 w_i m_i\, di$ with $\int_0^1 w_i\, di = 1$. To get an SDF written in public information only, start from the econometrician's posterior. Given $p$ (equivalently $z$), Bayesian updating of the prior with the price signal gives
$$
f \,|\, p \sim N(\mu_0, V_0),
\qquad
V_0^{-1} = \Sigma^{-1} + \Sigma_p^{-1} = K - \bar V^{-1},
\qquad
\mu_0 = V_0 \left( \Sigma^{-1}\mu + \Sigma_p^{-1} z \right).
$$

**Step 4: Risk premium given public information.** Take $E[\,\cdot\,|p]$ of the market-clearing condition $K p r = \Sigma^{-1}\mu + \bar V^{-1} f + \Sigma_p^{-1} z - \rho(\bar x + x)$. Since $p r$ and $z$ are known given $p$,
$$
K p r = \underbrace{\Sigma^{-1}\mu + \Sigma_p^{-1} z}_{= V_0^{-1}\mu_0} + \bar V^{-1} \mu_0 - \rho\left( \bar x + E[x|p] \right) = K \mu_0 - \rho\left( \bar x + E[x|p] \right),
$$
so the expected excess payoff given public information is
$$
\mu_0 - p r = \rho K^{-1} \left( \bar x + E[x|p] \right),
\qquad
E[x|p] = \frac{1}{\rho} \bar V^{-1} (\mu_0 - z),
$$
where $E[x|p]$ follows from $x = \frac{1}{\rho}\bar V^{-1}(f - z)$.

**Step 5: SDF for public information.** Guess the same exponential-affine form as in Step 2,
$$
m_0 = \frac{1}{r} \exp\left( -\lambda'(f - \mu_0) - \frac{1}{2} \lambda' V_0 \lambda \right).
$$
Then $E[m_0|p] = 1/r$ and $E[m_0 f|p] = (\mu_0 - V_0 \lambda)/r$. Pricing requires $E[m_0 f|p] = p$, so
$$
\lambda = V_0^{-1}(\mu_0 - p r) = \rho\, V_0^{-1} K^{-1} \left( \bar x + E[x|p] \right).
$$
Compare with Step 2: $m_0$ is the SDF of a hypothetical CARA investor with risk aversion $\rho$ who observes only $p$ and holds her optimal portfolio $q_0 = \frac{1}{\rho} V_0^{-1}(\mu_0 - pr)$, so that $\lambda = \rho q_0$. Since she is infinitesimal, adding her does not change the equilibrium.

The linear version $m_0^{lin} = \frac{1}{r}\left[1 - \lambda'(f - \mu_0)\right]$, with the same $\lambda$, also prices all assets given $p$. It is the unique SDF in the span of the payoffs $\{1, f\}$, i.e., the projection of every $m_i$ and of $m_0$ onto that span.

**Step 6: Implications.**

- *Risk premia vary with the price.* From Step 4, $\mu_0 - p r = \rho K^{-1}(\bar x + E[x|p])$. A low price signal $z$ could mean low $f$ or high supply $x$. The econometrician attributes part of it to high $x$, so she expects a high excess payoff. Formally, $\mu_0 - z = V_0 \Sigma^{-1}(\mu - z)$, so
$$
\mu_0 - p r = \rho K^{-1} \bar x + K^{-1} \bar V^{-1} V_0 \Sigma^{-1} (\mu - z),
$$
which falls as $z$ rises (in the one-asset case, all coefficients are positive scalars). So prices predict excess payoffs with a negative sign, even though every agent is rational.
- *Hansen–Jagannathan bound.* For the linear SDF, $Var(m_0^{lin}|p) / E[m_0^{lin}|p]^2 = \lambda' V_0 \lambda$. So the maximum squared conditional Sharpe ratio on excess payoffs $f - pr$ is
$$
\lambda' V_0 \lambda = \rho^2 \left( \bar x + E[x|p] \right)' K^{-1} V_0^{-1} K^{-1} \left( \bar x + E[x|p] \right).
$$





### Market Power

If the number of investor is finite, $Pr(i)>0$. 

If the number of investor is infinite, then $Pr(i)=0$

If we can use probability tools to unify markets with market power together, using Convergence Analysis. 

By creating A "probability" 

