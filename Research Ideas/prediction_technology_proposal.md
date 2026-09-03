# Prediction Technology, Backtest Bias, and the Technological Benchmark for Alpha

*Research proposal — draft v0.1*

---

## 1. One-paragraph pitch

Traders forecast returns using a **prediction technology**: a rule that maps publicly available data into a forecast. Technologies differ in how much of the predictable component of returns they can actually extract, and they improve over time. Two things follow. First, a new technology looks profitable in backtest but fails live, for two separable reasons: (i) in-sample fit overstates out-of-sample forecasting power (overfitting), and (ii) historical prices were formed by an *inferior* aggregate technology, so a backtest is run against a price system that no longer exists. Second, in equilibrium a trader's alpha depends on her technology **relative to the market's average**, so the average technology is the correct benchmark for performance evaluation — and because traders using the same technology take the same positions, the average-technology portfolio is also a genuine common factor in trader returns. The project builds this model, derives a decomposition of the backtest–live wedge, and estimates the aggregate technology frontier from institutional holdings and fund returns.

**Working titles.** "The Technological Benchmark for Alpha"; "Why Backtests Beat Live Trading"; "Prediction Technology and the Price of Skill."

---

## 2. Motivation: three facts the model should organize

1. **Anomalies decay after publication.** McLean & Pontiff (2016) find roughly a 30–60% post-publication decline; Chen & Zimmermann's open-source library lets this be measured strategy-by-strategy. Diffusion of a technology, not discovery of a mistake — though Hou, Xue & Zhang (2020) argue that a majority of the anomaly zoo is Type-I error, largely microcap-driven, a competing reading the model has to confront.
2. **In-sample beats out-of-sample, and the gap grows with model complexity.** Welch & Goyal (2008); Bailey, Borwein, López de Prado & Zhu (2014) on deflated Sharpe ratios; Kelly, Malamud & Zhou (2024); Da, Nagel & Xiu (2022) on how estimation error caps attainable Sharpe ratios.
3. **Alpha is shrinking while data and compute explode.** Bai, Philippon & Savov (2016) on price informativeness; Farboodi & Veldkamp (2020) on long-run growth in financial data technology; Begenau, Farboodi & Veldkamp (2018) on big data and firm size. More technology in aggregate should mean *less* alpha for the average user, which is precisely the model's prediction.

---

## 3. Position relative to the literature

- **Classical noisy REE** (Grossman & Stiglitz 1980; Hellwig 1980; Admati 1985) makes heterogeneity come from *signals*. Here everyone sees the same data; heterogeneity is in the **learning rule applied to public data**. This is closer to Martin & Nagel (2022) and to the machine-learning asset-pricing literature (Gu, Kelly & Xiu 2020; Nagel 2021) than to the private-information tradition.
- **Veldkamp and coauthors** supply the machinery: information as a chosen input with a production function and a cost (Veldkamp 2011); data as an accumulating asset with increasing returns (Farboodi & Veldkamp 2020; the data-economy framework); and — most useful for me — a *revealed-preference method for measuring information from holdings* (Kacperczyk, Van Nieuwerburgh & Veldkamp 2016). That paper is the empirical bridge for the hardest part of this project.
- **Kelly, Malamud & Zhou (2024)** micro-found "technology quality" as a function of model complexity $c = P/T$ and shrinkage $z$. Their closed forms give an explicit map from technology parameters to out-of-sample forecast quality, which I can plug directly into an equilibrium price function. To my knowledge nobody has embedded the virtue-of-complexity machinery inside a market-clearing model where prices themselves absorb the average technology.
- **Berk & Green (2004)** and **Gârleanu & Pedersen (2018)** explain why gross alpha need not survive as net alpha. I need one of their frictions (heterogeneous adoption costs, or decreasing returns to scale) or Grossman–Stiglitz free entry kills all rents.
- **Contribution.** The novel object is the *non-stationarity of the price function under technological progress*, and the resulting identification: the backtest–live wedge has two components with different empirical signatures, and the diffusion component is proportional to the growth rate of aggregate technology over the backtest sample.

---

## 4. The model

### 4.1 Environment

Overlapping one-period economies, $t = 0, 1, 2, \dots$. One risky asset in noisy supply $z_t \sim N(\bar z, \sigma_z^2)$, one riskless asset with gross return $R_f$. Payoff:

$$d_{t+1} = x_t' \beta + \varepsilon_{t+1}, \qquad \varepsilon_{t+1} \sim N(0, \sigma_\varepsilon^2),$$

where $x_t \in \mathbb{R}^P$ is a high-dimensional vector of **publicly observable** predictors (characteristics, macro state, alternative data) and $\beta$ is unknown. Write the predictable component $\theta_t \equiv x_t'\beta$ with $\mathrm{Var}(\theta_t) = \sigma_\theta^2$.

Nobody has private information. All heterogeneity is technological.

### 4.2 Defining prediction technology

A **technology** is an estimator $\mathcal{T}: \{x_s, d_{s+1}\}_{s<t} \mapsto \hat\beta$. Trader $i$'s signal is her own forecast $s_{it} = x_t' \hat\beta_i$.

Define **technology quality**

$$q_i \;\equiv\; \mathrm{Corr}^2\!\big(x_t'\hat\beta_i,\; x_t'\beta\big) \in [0,1],$$

the *out-of-sample* $R^2$ of the forecast against the true predictable component. $q_i = 1$ is perfect foresight of $\theta$; $q_i = 0$ is noise.

Two ways to justify a scalar index, and both should appear in the paper:

- **Theoretical.** Ranking technologies is properly a Blackwell partial order over experiments. Under joint normality the order collapses to a scalar precision, which is why the model is Gaussian. State this explicitly rather than assume it away — a referee will ask.
- **Micro-founded.** Kelly–Malamud–Zhou deliver $q(c, z, T)$ in closed form as a function of complexity $c = P/T$, ridge penalty $z$, and data quantity $T$. So $q_i$ is *not* a free parameter: it is the reduced form of a two-dimensional technology choice $(c_i, z_i)$ given data $T_i$. Farboodi–Veldkamp then endogenizes $T_i$ as accumulated data.

Because the projection is orthogonal, $\theta_t = a_i s_{it} + \eta_{it}$ with $\mathrm{Var}(\eta_{it}) = \sigma_\theta^2 (1 - q_i)$. Conditional on her own signal, trader $i$'s payoff precision is

$$\tau_i \;=\; \frac{1}{\sigma_\theta^2 (1 - q_i) + \sigma_\varepsilon^2},$$

which is increasing in $q_i$. **This is the "better technology → better forecast" map**, and it is the object the whole paper hangs on.

### 4.3 Equilibrium and the aggregate technology

Continuum of traders with CARA utility, risk aversion $\gamma$, distribution $G$ over $q$. Demand:

$$w_{it} = \frac{E_i[d_{t+1}] - R_f p_t}{\gamma \,\mathrm{Var}_i[d_{t+1}]}.$$

Every signal is a linear function of the same $x_t$, so aggregation is tractable: define $\bar\beta \equiv \int \hat\beta_i \, dG$ and the **aggregate technology quality** $\bar q \equiv \mathrm{Corr}^2(x_t'\bar\beta, \theta_t)$. Market clearing gives a linear price

$$p_t = \frac{1}{R_f}\Big(A + B\, x_t'\bar\beta - C\, z_t\Big).$$

*Note a subtlety worth a proposition of its own:* averaging estimators reduces variance, so $\bar q \ge \int q_i \, dG$ — **the market's technology is better than the average trader's technology.** This is bagging inside an equilibrium, and it strengthens the pessimistic message for individual traders.

### 4.4 Alpha depends on relative technology

Trader $i$'s expected excess profit is, to a first order,

$$\alpha_i \;\propto\; \frac{1}{\gamma}\Big(q_i - q_P\Big) \cdot \frac{\sigma_\theta^2}{\sigma_\theta^2(1-q_i) + \sigma_\varepsilon^2},$$

where $q_P$ is the quality of the price-implied forecast, itself a function of $\bar q$ and supply noise $\sigma_z^2$. Three immediate corollaries, all matching the intuition in the original sketch:

- **$\alpha_i > 0$ iff $q_i > q_P$.** You are paid only for beating the market's technology, not for having a good technology.
- **Universal adoption kills alpha.** If a new technology diffuses to everyone, $q_i \to \bar q \to q_P$ and $\alpha_i \to 0$. This is the "cannot make money once everyone knows it" channel.
- **Noise trading is the source of rents.** As $\sigma_z^2 \to 0$, $q_P \to$ full revelation and alpha vanishes for everyone (Grossman–Stiglitz).

### 4.5 The technology factor

Decompose holdings: $w_{it} = \bar w_t + \Delta w_{it}$, where $\bar w_t$ is the portfolio implied by the aggregate technology $\bar\beta$. Then

$$R^i_{t+1} = \underbrace{\beta_i^m R^m_{t+1}}_{\text{market}} + \underbrace{\lambda_i F^{\text{tech}}_{t+1}}_{\text{average technology}} + \underbrace{\alpha_i + u_{it+1}}_{\text{relative advantage}}, \qquad F^{\text{tech}}_{t+1} \equiv \bar w_t' R_{t+1}.$$

Be careful with language here, because it matters for how the paper is received:

- **As a benchmark**, $F^{\text{tech}}$ is unambiguously correct: it is what you would have earned with average technology, so alpha measured against it is exactly the return to *relative* technological advantage. This is the strongest and safest version of the claim.
- **As a risk factor**, it needs an extra argument: traders sharing a technology take *correlated positions*, so $F^{\text{tech}}$ carries real return variance and generates crowding and unwind risk. This is Stein (2009) and the August 2007 quant unwind (Khandani & Lo 2011). It is a factor in the covariance sense; whether it carries a risk *premium* requires more work and should be flagged as an open question rather than asserted.

### 4.6 Making technology scarce (do not skip this)

With free entry and a common adoption cost, Grossman–Stiglitz indifference means *net* alpha is zero for everyone and there is nothing to explain. I need one of:

- **Heterogeneous adoption costs** $\kappa_i \sim H$. The marginal adopter is indifferent; inframarginal traders earn rents. The cross-sectional distribution of alpha then identifies $H$.
- **Capacity constraints / decreasing returns to scale** (Berk & Green 2004): AUM expands until gross alpha is competed to zero at the margin, and observed alpha is a scale phenomenon.
- **Diffusion lags.** An innovation arrives at Poisson rate $\lambda$, initially held by a fraction $n_0$, and adoption follows a logistic path $\dot n_t = \phi n_t (1 - n_t)$. Rents are transient but persistent enough to be measured; $\phi$ is directly estimable from anomaly decay.

I favor combining the first and third: heterogeneous costs give a stationary alpha *distribution*, diffusion gives the *decay* dynamics.

### 4.7 The central result: decomposing the backtest–live wedge

Let $\bar q_t$ be increasing over calendar time. A trader with technology $q$ backtests over $s \in [T_0, T]$ and then trades live at $T$.

**Proposition (backtest bias).**
$$\underbrace{\widehat{\alpha}^{\text{backtest}} - \alpha^{\text{live}}}_{\text{total wedge}} \;=\; \underbrace{\Big[\hat q^{\text{IS}} - q^{\text{OOS}}\Big]\cdot\frac{\partial \alpha}{\partial q}}_{\text{(A) overfitting}} \;+\; \underbrace{\int_{T_0}^{T}\!\Big[f\big(q - q_{P,s}\big) - f\big(q - q_{P,T}\big)\Big] d\mu(s)}_{\text{(B) diffusion}} \;>\;0 .$$

Channel (A) is the familiar statistical problem: in-sample fit is inflated by roughly $c/T$ terms.
Channel (B) is the economics, and I believe it is the paper's contribution: **the backtest is evaluated against prices formed by a weaker aggregate technology than the one the trader will actually face.** To a first order,

$$\text{(B)} \;\approx\; \frac{\partial \alpha}{\partial q_P}\Big(q_{P,T} - \overline{q_{P,s}}\Big) \;\propto\; \text{growth of aggregate prediction technology over the backtest window}.$$

**Why the two channels are separately identified.** (A) scales with the strategy's own complexity $c_i$ and with $1/T$, and is idiosyncratic across strategies. (B) is a *calendar-time* effect: it is common across all strategies backtested over the same window, it scales with the length of the lookback, and it is larger for technologies that diffuse faster. Different signatures, so a panel of backtested-then-live strategies identifies both.

---

## 5. Measurement: the hard part

Five strategies, ordered from most to least direct. I would use at least three and check consistency.

**(a) Holdings-based inversion — the workhorse.**
Under the model, portfolio weights load on the trader's forecast, so
$$\mathrm{Cov}_t\big(w_{it},\, R_{t+1}\big) \;\text{ is monotone in } q_i .$$
This is exactly the "picking" measure of Kacperczyk, Van Nieuwerburgh & Veldkamp (2016), which means the estimator is off the shelf and already validated. **Data:** 13F filings, N-PORT, CRSP/Thomson mutual fund holdings. The model supplies the structural map from the covariance to $q_i$ rather than treating it as a descriptive statistic.

**(b) Construct $F^{\text{tech}}$ directly from aggregate institutional holdings.**
$\bar w_t$ is the AUM-weighted aggregate active portfolio, i.e. aggregate institutional weights minus market-cap weights. This is a *constructible time series*, and it is testable in the most convincing way available: **does adding $F^{\text{tech}}$ to a standard factor model shrink the cross-sectional dispersion of fund alphas?** If the average technology is the right benchmark, it should absorb a large share of what looks like alpha under FF5 or $q^5$.

**(c) Price informativeness as an external series for $\bar q_t$.**
$\bar q_t$ maps one-to-one into price informativeness. Bai, Philippon & Savov (2016) and Dávila & Parlatore (identifying price informativeness) give independent estimates. Use these to *over-identify* — if the holdings-based $\bar q_t$ and the price-based $\bar q_t$ diverge, the model is wrong somewhere.

**(d) Anomaly decay identifies the diffusion rate $\phi$.**
Estimate post-publication half-lives strategy-by-strategy from Chen & Zimmermann's library. Sharp auxiliary prediction: **simple, low-technology anomalies should decay fast; complex ones should decay slowly**, because complexity is itself a barrier to adoption.

**(e) Input-based validation of $\bar q_t$.**
Alternative-data vendor adoption; quantitative vs. discretionary classification from fund prospectus text (Abis 2020); ML/data-science job postings at asset managers (Lightcast/Burning Glass); compute and data spend. These are noisy but exogenous-ish, and they discipline the structural estimate.

**Bonus dataset for the wedge itself.** Smart-beta and factor ETFs publish **backtested index returns before launch**, then trade live. That is a direct, dated, pre-registered measurement of $\widehat{\alpha}^{\text{backtest}} - \alpha^{\text{live}}$ across hundreds of strategies with known complexity and known launch dates. If this project has one killer empirical exhibit, it is that.

---

## 6. Testable predictions

1. The backtest–live wedge rises with the growth of aggregate technology over the backtest window, controlling for strategy complexity.
2. The wedge rises with strategy complexity $c$, controlling for calendar time.
3. Average alpha falls as $\bar q_t$ rises; alpha *dispersion* falls unless the dispersion of $q_i$ widens faster.
4. Fund returns comove through $F^{\text{tech}}$; comovement spikes during crowded unwinds.
5. Adding $F^{\text{tech}}$ to the benchmark shrinks measured alpha dispersion materially.
6. Anomaly decay is faster for technologically simple strategies.
7. Cross-section: funds with higher measured $q_i$ earn higher alpha *and* higher fees, with fees capturing most of the rent (Berk–Green).

---

## 7. Roadmap

| Phase | Goal | Output |
|---|---|---|
| 1 (1–2 months) | Static two-type noisy REE, closed-form $\alpha(q_i, \bar q)$. Verify the relative-technology result and the bagging result $\bar q \ge \int q_i$. | Section 2 of the paper |
| 2 (2–3 months) | Add diffusion and heterogeneous adoption costs; derive the backtest-bias proposition and the two-channel decomposition. | Core theory |
| 3 (2 months) | Build $F^{\text{tech}}_t$ from 13F/N-PORT; run the alpha-dispersion horse race. | First empirical exhibit |
| 4 (2–3 months) | ETF pre-launch backtest vs. live sample; test predictions 1–2. | Second exhibit |
| 5 | Structural estimation of $\{q_i\}, \bar q_t, \phi, H$ by SMM; validate against price informativeness. | Full paper |

Phase 1 plus Phase 3 alone is a credible second-year paper. Do not attempt the full structural estimation first.

---

## 8. Objections to prepare for

1. **"Grossman–Stiglitz says net alpha is zero."** Answer: adoption frictions and diffusion lags. Be explicit about which friction generates the rents; do not smuggle it in.
2. **"Is your factor a risk factor?"** Answer honestly: it is a *benchmark*, and separately a common source of covariance through crowding. A risk premium requires an SDF argument I do not yet have.
3. **"Technology is a partial order, not a scalar."** Answer: Blackwell + Gaussian. Show what breaks with non-Gaussian signals.
4. **"You cannot separate rising $\bar q_t$ from a time-varying risk premium."** This is the most dangerous objection. The defense is the cross-sectional complexity interaction (prediction 2), which a time-varying premium does not generate.
5. **"Backtests are selected on being good."** True and severe. The ETF pre-launch sample partly handles it because launch is a commitment date; still, model the selection.
6. **Endogeneity of adoption.** Technology adoption responds to expected profits, so $q_i$ and $\alpha_i$ are jointly determined. The structural model handles this by construction, but reduced-form regressions of alpha on $q_i$ do not.
7. **Survivorship in fund data.** Standard, but the alpha-dispersion test is sensitive to it.

---

## 9. References to pull

**Information in equilibrium.** Grossman & Stiglitz (1980, AER); Hellwig (1980, JET); Admati (1985, ECMA); Blackwell (1953); Veldkamp, *Information Choice in Macroeconomics and Finance* (2011).

**Data economy (core reference).** Farboodi & Veldkamp, "Long-Run Growth of Financial Technology" (2020, AER); Farboodi & Veldkamp, *A Model of the Data Economy* / the data-economy book manuscript; Begenau, Farboodi & Veldkamp (2018, JME); Abis, Farboodi, Veldkamp & Venkateswaran on valuing data; Dugast & Foucault (2018, JFE), "Data Abundance and Asset Price Informativeness."

**Measuring information from holdings.** Kacperczyk, Van Nieuwerburgh & Veldkamp (2016, ECMA); Berk & van Binsbergen (2015, JFE).

**Complexity and the limits of prediction.** Kelly, Malamud & Zhou (2024, JF); Martin & Nagel (2022, JFE); Da, Nagel & Xiu (2022 WP), "The Statistical Limit of Arbitrage"; Gu, Kelly & Xiu (2020, RFS); Nagel (2021), *Machine Learning in Asset Pricing*.

**Backtest bias and decay.** McLean & Pontiff (2016, JF); Chen & Zimmermann, Open Source Cross-Sectional Asset Pricing; Harvey, Liu & Zhu (2016, RFS); Bailey, Borwein, López de Prado & Zhu (2014); Welch & Goyal (2008, RFS).

**Skill, rents, crowding.** Berk & Green (2004, JPE); Gârleanu & Pedersen (2018, JF); Stein (2009, JF); Khandani & Lo (2011); Abis (2020 WP), "Man vs. Machine."

**Price informativeness.** Bai, Philippon & Savov (2016, JFE); Dávila & Parlatore, "Identifying Price Informativeness."

*Verify all years and outlets before circulating — several are working papers whose publication status may have changed.*
