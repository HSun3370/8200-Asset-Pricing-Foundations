# Creative Destruction, Firm Exit, and the Cross-Section of Returns
### A literature review and research-design note

**Research question.** Standard valuation treats the firm as a perpetuity. In a
Schumpeterian economy it is not: a firm faces a hazard of being displaced by a
competitor and exiting. Does exposure to *aggregate variation in that hazard*
carry a risk premium, and can it account for (a) the size premium and (b) the
low-frequency variation in dividends that drives most price variation?

**Citation confidence key.**
`[V]` = bibliographic details verified in a literature search.
`[U]` = from general knowledge; **verify year, venue, and page numbers before citing.**

---

## 1. Two literatures that need to be joined

The idea sits at the intersection of two bodies of work that mostly do not talk
to each other:

1. **Displacement / creative-destruction asset pricing.** Innovation by *others*
   erodes the rents of incumbents. Mature, largely settled, with a clear
   theoretical core (§3) and a growing measurement literature (§5).
2. **Firm exit, distress, and survival in the cross-section.** Empirical, mostly
   reduced-form, and — importantly — the evidence here runs *against* a simple
   risk story (§6).

The proposed contribution lives in the seam: the first literature models
displacement as a *rent-erosion* process affecting continuing firms; the second
studies *exit* as an absorbing event but treats it as idiosyncratic. Almost
nobody prices the time-varying **exit hazard itself** as a state variable.

---

## 2. Theoretical antecedents (growth theory and firm dynamics)

These are the non-finance foundations. Cite for the mechanism, not for pricing.

- **Aghion & Howitt (1992, *Econometrica*)** `[V]` — the canonical creative-
  destruction growth model. Innovation by entrants destroys incumbent rents;
  growth and destruction are two sides of one process.
- **Acemoglu & Cao (2015, *JET*)** `[V]` — extends Schumpeterian growth to allow
  *incremental* innovation by incumbents alongside *radical* innovation by
  entrants. Generates a non-degenerate firm-size distribution (Pareto/Zipf) from
  entry and expansion-exit. This is the natural microfoundation for a
  size-dependent exit hazard, which is exactly what the size-premium argument
  needs.
- **Jovanovic (1982, *Econometrica*)**, **Hopenhayn (1992, *Econometrica*)** `[U]`
  — selection and passive learning; the standard framework in which small and
  young firms exit at higher rates. Establishes the empirical regularity the
  project relies on, but with *no* aggregate risk.
- **Aghion, Antonin & Bunel (2021), *The Power of Creative Destruction*** `[V]` —
  book-length synthesis; useful for framing, not for the model.

> **Note.** In all of these, exit is a *selection* device driven by idiosyncratic
> productivity draws. There is no priced risk. Getting from here to a premium
> requires an additional friction — see §3 and §9.

---

## 3. Displacement risk in general equilibrium (the theoretical core)

- **Gârleanu, Kogan & Panageas (2012), "Displacement Risk and Asset Returns,"
  *JFE* 105(3), 491–510** `[V]` — **the paper to build on.** OLG economy where
  innovation raises competitive pressure on existing firms *and* erodes older
  workers' human capital. Because innovators have not yet entered the economy,
  current agents cannot buy claims on their future rents; missing
  intergenerational risk sharing turns displacement into a systematic factor.
  Explains the growth–value factor, the value premium, and the equity premium.
  Circulated earlier as "The Demographics of Innovation and Asset Returns"
  (NBER WP 15457, 2009).
  - **Critically for the second leg of the project:** the paper derives the
    cointegration properties of (i) dividends paid by firms *currently
    tradeable* and (ii) "aggregate" dividends paid by *all* firms at each date.
    That wedge is the survivorship problem. Read this section closely — it is
    the closest existing treatment of the long-run-dividend argument.
- **Kogan, Papanikolaou & Stoffman (2020), "Left Behind: Creative Destruction,
  Inequality, and the Stock Market," *JPE* 128(3), 855–906** `[V]` — same
  incompleteness, different friction. Shareholders do not capture all gains from
  innovation even when they own the innovating firms, because part accrues to
  innovators who cannot sell claims on their future ideas. Generates a high
  aggregate premium, return comovement, and cross-sectional premium differences
  that representative-agent models miss. (NBER WP 18671, 2013, "Winners and
  Losers.")
- **Papanikolaou (2011, *JPE*)**, **Kogan & Papanikolaou (2014, *JF*)** `[U]` —
  investment-specific technology shocks hurt assets in place and benefit growth
  options. The "growth options hedge displacement" channel.
- **Gârleanu, Panageas & Yu (2012, *JF*), "Technological Growth and Asset
  Pricing"** `[U]` — infrequent, large technological innovations with slow
  diffusion; jump-like arrival of destruction.
- **Ai & Kiku (2013)** `[U]` — growth options hedge assets-in-place risk because
  the cost of option exercise is procyclical. A competing channel that produces
  similar cross-sectional predictions; worth distinguishing from.
- **Chen, Li, Thakor & Ward (2026), "Appropriated Growth," *JFE* 176** `[V]` —
  recent extension of the "gains from growth do not accrue to shareholders"
  logic. Check for overlap.

---

## 4. Endogenous entry and exit in GE asset-pricing models

This is where firm *exit* is actually modeled rather than assumed away.

- **Bena, Garlappi & Grüning (2016), "Heterogeneous Innovation, Firm Creation and
  Destruction, and Asset Prices," *RAPS* 6(1), 46–87** `[V]` — **closest
  existing structural model.** GE with endogenous firm creation *and
  destruction*; incremental innovation by incumbents and radical innovation by
  entrants drive productivity. Innovation incentives generate time-varying
  growth and countercyclical uncertainty. Calibrated to US patents 1975–2013.
  Conclusion: the incumbent–entrant interplay is a first-order determinant of
  priced risk. **Read this before writing anything down** — it may already
  contain the mechanism, though it does not target the size premium or the
  dividend term structure.
- **Corhay, Kung & Schmid (2020), "Competition, Markups, and Predictable
  Returns," *RFS*** `[V]` — monopolistic competition with endogenous entry and
  exit; endogenous industry concentration produces countercyclical markups,
  which amplify macro risk. The nonlinear map from the *measure of firms* to
  markups endogenously generates countercyclical macro volatility. With
  recursive preferences: predictable risk premia forecastable by competition
  measures, and a **U-shaped term structure of equity returns**. Directly
  relevant to the dividend-strip leg.
- **Loualiche, "Asset Pricing with Entry and Imperfect Competition," *JF***
  `[V, year/issue to verify]` — entry threat in the cross-section of returns.
- **Bustamante & Donangelo (2017), "Product Market Competition and Industry
  Returns," *RFS*** `[V]` — decomposes competition's effect on systematic risk
  into operating leverage, entry threat, and risk feedback channels, which work
  in *opposing* directions. Important caution: the sign is not obvious.
- **Dou, Ji & Wu**, "Competition, Profitability, and Risk Premia" and "The
  Oligopoly Lucas Tree" `[V, venues to verify]` — strategic competition; a
  "competition risk premium" arising because competition intensifies in bad
  times, narrowing margins and amplifying adverse shocks.
- **Opp, Parlour & Walden (2014)** `[U]`; **Gomes, Kogan & Zhang (2003),
  "Equilibrium Cross Section of Returns," *JPE* 111(4), 693–732** `[V]` — the
  benchmark for generating size and value effects from firm dynamics *without*
  a displacement channel. Useful as the null.
- **"Asset Pricing with Costly and Delayed Firm Entry," *Macroeconomic
  Dynamics*** `[V, authors to verify]` — growing product variety through
  costly, delayed entry generates endogenous low-frequency productivity
  fluctuations and large persistent variation in consumption growth and asset
  prices. This is a *long-run-risk-from-entry* result, i.e. the mirror image of
  the proposed long-run-dividend channel.

---

## 5. Measuring creative destruction empirically

- **Grammig & Jank (2016), "Creative Destruction and Asset Prices," *JFQA*
  51(6), 1739–1768** `[V]` — **the direct precedent for the stated hypothesis.**
  Argues small-value firms must offer higher expected returns to compensate for
  the risk from serendipitous invention activity, while large-growth stocks
  hedge creative destruction and receive expected-return *discounts*. A
  two-factor model with a creative-destruction factor explains the cross-section
  of size- and BM-sorted portfolios; estimated compensations are economically
  large. Large-growth firms load *positively* on patent-activity growth.
  (Earlier WP version 2010.)
- **Kakhbod, Kogan, Li & Papanikolaou, "Measuring Creative Destruction," MIT
  Sloan WP 7234-24 / SSRN 5008685, R&R at *RFS*** `[V]` — text-based measure of
  *innovation displacement*: how relevant one firm's innovations are to
  another's operations. When other major innovators' recent innovations overlap
  a focal firm's technologies, its profit growth declines over the next seven
  years, worsening annually, especially for non-innovative firms. Firms with
  higher displacement exposure earn **higher risk-adjusted returns** the
  following year. This is the state-of-the-art measure — use it or beat it.
- **Ma, "Technological Obsolescence," NBER WP 29504** `[V]` — measures *realized*
  obsolescence. Finds an alpha spread that risk-based displacement models
  explain only 5–10% of, and interprets the residual as under-reaction favoring
  obsolete firms. **This is the main empirical challenge to a risk-based
  reading** and must be addressed head-on.
- **Kelly, Papanikolaou, Seru & Taddy (2021), *AER: Insights* 3(3), 303–320**,
  "Measuring Technological Innovation over the Long Run" `[V]` — text-based
  patent novelty/impact measures; the standard input.
- **Kogan, Papanikolaou, Seru & Stoffman (2017, *QJE*)** `[U]` — market-value-based
  patent innovation measure. Workhorse dataset.
- **Kogan, Papanikolaou, Schmidt & Seegmiller, "Technology and Labor
  Displacement," *REStud*** `[V, year to verify]`; **Green, Kogan, Papanikolaou &
  Schmidt (2025 WP), "Winners and Losers: Competition, Creative Destruction, and
  Labor Income Risk"** `[V]` — passthrough of product-market creative
  destruction to worker earnings; asymmetric and concentrated among top workers.
  Relevant because it supplies the *marginal-utility* link that makes
  displacement systematic.

---

## 6. Firm exit, distress, and the cross-section — the awkward evidence

Read this section as a set of obstacles, not support.

- **Campbell, Hilscher & Szilagyi (2008), "In Search of Distress Risk," *JF***
  `[V]` — reduced-form failure model (Chapter 7/11, financial-reason delisting,
  D rating). Finds distressed stocks earn *low* average returns — the **distress
  anomaly**. If exit hazard were a priced risk, the sign should be positive.
  Any exit-risk story must explain why the highest-hazard firms underperform.
- **Dichev (1998, *JF*)** `[U]` — bankruptcy risk is not a systematic risk; same
  negative-sign problem.
- **Vassalou & Xing (2004, *JF*)** `[U]` — default risk varies with economic
  conditions and is related to the size premium; the more favorable prior.
- **Shumway (1997, *JF*), "The Delisting Bias in CRSP Data"**; **Kothari,
  Shanken & Sloan (1995, *JF*)**; **Shumway & Warther (1999)** `[V for the
  claim, U for details]` — survivorship/delisting bias is conjectured to be *the
  main source* of the size premium. **This is a serious identification hazard:**
  a data artifact and the proposed theory predict the same thing.
- **Hou & Moskowitz (2005)** `[V]` — price delay / market frictions explain a
  substantial share of the size premium.
- **"Taking Over the Size Effect: Asset Pricing Implications of Merger Activity"**
  (working paper) `[V, authors to verify]` — size-portfolio returns are
  primarily driven by M&A news; an ex-ante takeover-likelihood factor correlates
  highly with SMB; **acquisition news explains virtually all of the size premium
  in US data**, and the premium falls to insignificance in recent decades.
  **Direct threat to the project:** acquisition *is* exit, but exit at a premium
  to shareholders — the opposite sign from destruction.
- **Asness, Frazzini, Israel, Moskowitz & Pedersen (2018, *JFE*), "Size Matters,
  If You Control Your Junk"** `[U]` — the size premium survives controlling for
  quality. The counterweight to the above.
- **Fama & French (2001, *JFE*), "Disappearing Dividends"** `[U]` — composition
  of the listed universe changes over time; relevant to the aggregate-dividend
  measurement problem.

---

## 7. Long-run dividends, duration, and the equity term structure

This is the second leg, and where the sharper contribution probably lies.

- **Bansal & Yaron (2004, *JF*)**; **Bansal, Dittmar & Lundblad (2005, *JF*)**
  `[U]` — long-run cash-flow risk; cash-flow betas account for a majority of
  cross-sectional premium variation.
- **Hansen, Heaton & Li (2008, *JPE*)** `[U]` — long-run risk–return tradeoff for
  valuing cash flows exposed to macro growth. The formal machinery for "long-run
  dividend variation."
- **Lettau & Wachter (2007, *JF*), "Why Is Long-Horizon Equity Less Risky? A
  Duration-Based Explanation of the Value Premium"** `[U]` — **the key tension.**
  In this framework *shorter* duration means *more* exposure to priced
  cash-flow shocks and *less* to discount-rate shocks. A high exit hazard
  shortens duration. The proposed mechanism therefore needs to establish which
  effect dominates; it cannot be assumed.
- **van Binsbergen, Brandt & Koijen (2012, *AER*)**, "On the Timing and Pricing
  of Dividends" `[U]`; **Gormsen (2021, *JF*)**, "Time Variation of the Equity
  Term Structure" `[U]` — dividend-strip evidence.
- **Belo, Collin-Dufresne & Goldstein (2015, *JF*)**, "Dividend Dynamics and the
  Term Structure of Dividend Strips" `[U]` — leverage/payout dynamics reconcile
  strip prices with long-run risk. **Their mechanism competes with an
  exit-hazard mechanism for the same moments.**
- **Gonçalves (2021)**, "The Short Duration Premium" (*JFE*) and "Reinvestment
  Risk and the Equity Term Structure" (*JF*) `[U, verify both]` — duration in
  the cross-section; central to the empirical design.
- **"Equity Duration and Predictability" (*JFE* 2025)** `[V, authors to verify]`
  — higher equity duration implies a larger role for expected returns in
  price variation; in the post-1945 US, expected returns explain ~90% of
  dividend–price variation, and the share *falls* with payout ratio in the
  cross-section. Sharpens the identification: if exit hazard shortens duration,
  it should *reduce* the discount-rate share of price variation.
- **Larrain & Yogo (2008, *JFE*)**; **Boudoukh, Michaely, Richardson & Roberts
  (2007, *JF*)** `[U]` — net payout vs. dividends; entry/exit and net issuance
  drive a wedge between aggregate and per-share cash flows. Essential for
  measuring the survivorship component of index dividends.
- **Kragt, de Jong & Driessen, "The Dividend Term Structure"** `[V]` — finds most
  stock-price variation captured by short-term and business-cycle movements in
  discounted risk-adjusted dividends, with limited updating of *long-horizon*
  expectations. **This cuts against the "long-run dividend variation explains a
  lot of price variation" premise** and should be confronted directly.

---

## 8. Technical toolkit: hazard rates as priced jumps

The natural formalism is a Poisson/jump-intensity model with a time-varying,
partly systematic intensity — mathematically identical to the disaster
literature, transplanted to the firm level.

- **Barro (2006, *QJE*)**; **Gabaix (2012, *QJE*), "Variable Rare Disasters"**
  `[U]` — Gabaix's *linearity-generating* processes give firm-level "resilience"
  with tractable closed forms. This is arguably the cleanest off-the-shelf
  machinery for a firm-level exit intensity.
- **Wachter (2013, *JF*)** `[V]` — time-varying disaster probability drives high
  market volatility and return predictability; equity premium is substantial
  even at *short* maturities because all maturities share disaster exposure.
  Note the parallel: a firm-exit jump also hits all maturities of that firm's
  strip, which is one way to break the duration objection in §7.
- **Gourio (2012, *AER*), "Disaster Risk and Business Cycles"** `[U]`.
- **Berkman, Jacobsen & Lee (2011, *JFE*)** `[V]` — time-varying crisis index;
  crisis risk correlates with E/P and dividend yield and is priced across
  industries. A template for the empirical design.
- **Bhamra, Dorion, Jeanneret & Weber** `[U]` — jump/credit risk and equity
  returns; check for overlap on hazard-rate pricing.

---

## 9. What is established, what is open

**Established (do not reclaim as novel):**
1. Creative destruction is a priced systematic factor — Gârleanu–Kogan–Panageas;
   Kogan–Papanikolaou–Stoffman.
2. Creative destruction can explain size *and* value premia — Grammig & Jank
   already published this exact claim.
3. Displacement exposure predicts profit declines and higher risk-adjusted
   returns at the firm level — Kakhbod–Kogan–Li–Papanikolaou.
4. GE models with endogenous firm creation and destruction match asset-pricing
   moments — Bena–Garlappi–Grüning; Corhay–Kung–Schmid.

**Genuinely open:**
1. **The exit hazard as a priced state variable.** Existing models price
   *rent erosion* for surviving firms. None, as far as I can find, prices the
   time-varying *probability of the claim terminating*, separately from the
   level of expected cash flows.
2. **The term-structure implication.** If exit hazard is a jump intensity, it
   truncates the dividend strip at *every* maturity but with cumulative weight
   rising in maturity. That is a specific, testable prediction for the slope of
   the term structure and for how cross-sectional duration sorts should behave
   in high- vs. low-hazard states. Corhay–Kung–Schmid's U-shape is the nearest
   existing result; nobody has connected it to firm-level survival.
3. **The aggregate-vs-per-share dividend wedge.** GKP flag the cointegration
   issue but do not quantify it. How much of index dividend growth is
   survivorship of the *traded* set rather than growth of the *economy*? This is
   measurable with CRSP/Compustat plus delisting returns, and it is a clean
   stand-alone paper even without a model.

---

## 10. Three obstacles the project must clear

**(a) Diversification.** Firm exit is largely idiosyncratic. A diversifiable
hazard lowers expected cash flow, not the risk premium — it changes P, not
E[R]. Every successful paper above buys a premium with a specific
incompleteness: untradeable future cohorts (GKP), untradeable innovator rents
(KPS), concentrated labor-income exposure (Green et al.). **The model needs an
explicit statement of what makes the hazard co-move with marginal utility.**
Options: (i) counter-cyclical aggregate exit intensity with recursive
preferences; (ii) an untradeable-entrant wedge as in GKP; (iii) labor-income
concentration as in the Green et al. channel.

**(b) The duration sign.** Higher hazard = shorter duration = (in most
calibrations, per Lettau–Wachter) *less* exposure to persistent discount-rate
shocks. The proposed mechanism needs the hazard's own price of risk to dominate
the duration effect. Wachter (2013) shows one way out (jump exposure is
maturity-invariant); this should be worked out analytically before calibration.

**(c) The empirical target.** The size premium is a fragile target: it may be
delisting bias, it may be M&A news, it has weakened over recent decades, and
the distress anomaly runs the wrong way. **Consider retargeting** to (i) the
dividend term structure, (ii) the cross-section of cash-flow duration, or (iii)
the aggregate/per-share dividend wedge — none of which is contaminated the same
way, and each of which yields a sharper, more falsifiable prediction.

---

## 11. Suggested reading order

1. Gârleanu, Kogan & Panageas (2012) — including the cointegration section.
2. Bena, Garlappi & Grüning (2016) — the closest structural competitor.
3. Grammig & Jank (2016) — the closest empirical precedent.
4. Kakhbod, Kogan, Li & Papanikolaou — current measurement frontier.
5. Ma, "Technological Obsolescence" — the main challenge.
6. Lettau & Wachter (2007) + Corhay, Kung & Schmid (2020) — the duration and
   term-structure tension.
7. The M&A/size-effect working paper + Shumway (1997) — the identification
   hazards.

---

## Appendix A — search strategy

**Keywords:** creative destruction asset prices; displacement risk; obsolescence
risk; firm exit hazard risk premium; endogenous entry exit asset pricing;
competition risk premium; technological displacement returns; survivorship
aggregate dividends; dividend strip firm exit; equity duration hazard.

**JEL:** G12 (asset pricing), O31/O33 (innovation, technological change), E44,
L11 (firm size/market structure), D52 (incomplete markets).

**Authors to follow (forward citations on Google Scholar):** Dimitris
Papanikolaou, Leonid Kogan, Stavros Panageas, Nicolae Gârleanu, Lorenzo
Garlappi, Howard Kung, Lukas Schmid, Alexandre Corhay, Winston Dou, Song Ma,
Erik Loualiche, Lawrence Schmidt.

**Highest-yield forward-citation seeds:** GKP (2012) and KPS (2020). Anyone
building on the exit margin will cite one of these.

**Working-paper sources to sweep:** NBER WP series, SSRN (FEN Asset Pricing),
authors' personal sites (Papanikolaou and Kogan post current versions), recent
WFA/AFA/SFS Cavalcade/Utah Winter Finance programs.

---

## Appendix B — full reference list (to be verified before submission)

> Entries marked `[U]` were reconstructed from general knowledge and **must** be
> checked against the published record. Do not paste into a bibliography
> unverified.

- Acemoglu, D., & Cao, D. (2015). Innovation by entrants and incumbents. *Journal of Economic Theory*, 157, 255–294. `[V]`
- Aghion, P., & Howitt, P. (1992). A model of growth through creative destruction. *Econometrica*, 60(2), 323–351. `[V]`
- Aghion, P., Antonin, C., & Bunel, S. (2021). *The Power of Creative Destruction*. Harvard University Press. `[V]`
- Ai, H., & Kiku, D. (2013). Growth to value: Option exercise and the cross section of equity returns. *JFE*. `[U]`
- Asness, C., Frazzini, A., Israel, R., Moskowitz, T., & Pedersen, L. (2018). Size matters, if you control your junk. *JFE*, 129(3). `[U]`
- Bansal, R., & Yaron, A. (2004). Risks for the long run. *JF*, 59(4), 1481–1509. `[V]`
- Bansal, R., Dittmar, R., & Lundblad, C. (2005). Consumption, dividends, and the cross section of equity returns. *JF*. `[U]`
- Belo, F., Collin-Dufresne, P., & Goldstein, R. (2015). Dividend dynamics and the term structure of dividend strips. *JF*, 70(3). `[U]`
- Bena, J., Garlappi, L., & Grüning, P. (2016). Heterogeneous innovation, firm creation and destruction, and asset prices. *RAPS*, 6(1), 46–87. `[V]`
- Berkman, H., Jacobsen, B., & Lee, J. (2011). Time-varying rare disaster risk and stock returns. *JFE*. `[V]`
- Boudoukh, J., Michaely, R., Richardson, M., & Roberts, M. (2007). On the importance of measuring payout yield. *JF*. `[U]`
- Bustamante, M. C., & Donangelo, A. (2017). Product market competition and industry returns. *RFS*, 30(12). `[V]`
- Campbell, J., Hilscher, J., & Szilagyi, J. (2008). In search of distress risk. *JF*, 63(6). `[V]`
- Chan, K. C., & Chen, N.-F. (1991). Structural and return characteristics of small and large firms. *JF*, 46, 1467–1484. `[V]`
- Chen, Y., Li, X., Thakor, R., & Ward, C. (2026). Appropriated growth. *JFE*, 176, 104207. `[V]`
- Corhay, A., Kung, H., & Schmid, L. (2020). Competition, markups, and predictable returns. *RFS*. `[V]`
- Dichev, I. (1998). Is the risk of bankruptcy a systematic risk? *JF*, 53(3). `[U]`
- Dou, W., Ji, Y., & Wu, W. Competition, profitability, and risk premia. `[V, venue to verify]`
- Dou, W., Ji, Y., & Wu, W. The oligopoly Lucas tree. `[V, venue to verify]`
- Fama, E., & French, K. (2001). Disappearing dividends. *JFE*, 60(1). `[U]`
- Gabaix, X. (2012). Variable rare disasters. *QJE*, 127(2). `[U]`
- Gârleanu, N., Kogan, L., & Panageas, S. (2012). Displacement risk and asset returns. *JFE*, 105(3), 491–510. `[V]`
- Gârleanu, N., Panageas, S., & Yu, J. (2012). Technological growth and asset pricing. *JF*. `[U]`
- Gomes, J., Kogan, L., & Zhang, L. (2003). Equilibrium cross section of returns. *JPE*, 111(4), 693–732. `[V]`
- Gonçalves, A. (2021). The short duration premium. *JFE*. `[U]`
- Gonçalves, A. (2021). Reinvestment risk and the equity term structure. *JF*. `[U]`
- Gormsen, N. (2021). Time variation of the equity term structure. *JF*. `[U]`
- Gourio, F. (2012). Disaster risk and business cycles. *AER*, 102(6). `[U]`
- Grammig, J., & Jank, S. (2016). Creative destruction and asset prices. *JFQA*, 51(6), 1739–1768. `[V]`
- Green, B., Kogan, L., Papanikolaou, D., & Schmidt, L. (2025). Winners and losers: Competition, creative destruction, and labor income risk. Working paper. `[V]`
- Hansen, L. P., Heaton, J., & Li, N. (2008). Consumption strikes back? *JPE*, 116(2). `[U]`
- Hopenhayn, H. (1992). Entry, exit, and firm dynamics in long run equilibrium. *Econometrica*, 60(5). `[U]`
- Hou, K., & Moskowitz, T. (2005). Market frictions, price delay, and the cross-section of expected returns. *RFS*. `[V]`
- Jovanovic, B. (1982). Selection and the evolution of industry. *Econometrica*, 50(3). `[U]`
- Kakhbod, A., Kogan, L., Li, P., & Papanikolaou, D. (2024/2025). Measuring creative destruction. MIT Sloan WP 7234-24; SSRN 5008685. R&R *RFS*. `[V]`
- Kelly, B., Papanikolaou, D., Seru, A., & Taddy, M. (2021). Measuring technological innovation over the long run. *AER: Insights*, 3(3), 303–320. `[V]`
- Kogan, L., & Papanikolaou, D. (2014). Growth opportunities, technology shocks, and asset prices. *JF*. `[U]`
- Kogan, L., Papanikolaou, D., Schmidt, L., & Seegmiller, B. Technology and labor displacement. *REStud*. `[V, year to verify]`
- Kogan, L., Papanikolaou, D., Seru, A., & Stoffman, N. (2017). Technological innovation, resource allocation, and growth. *QJE*, 132(2). `[U]`
- Kogan, L., Papanikolaou, D., & Stoffman, N. (2020). Left behind: Creative destruction, inequality, and the stock market. *JPE*, 128(3), 855–906. `[V]`
- Kothari, S. P., Shanken, J., & Sloan, R. (1995). Another look at the cross-section of expected stock returns. *JF*, 50(1). `[U]`
- Kragt, J., de Jong, F., & Driessen, J. The dividend term structure. `[V, venue to verify]`
- Larrain, B., & Yogo, M. (2008). Does firm value move too much to be justified by subsequent changes in cash flow? *JFE*, 87(1). `[U]`
- Lettau, M., & Wachter, J. (2007). Why is long-horizon equity less risky? A duration-based explanation of the value premium. *JF*, 62(1). `[U]`
- Loualiche, E. Asset pricing with entry and imperfect competition. *JF*. `[V, year to verify]`
- Ma, S. (2021). Technological obsolescence. NBER WP 29504. `[V]`
- Papanikolaou, D. (2011). Investment shocks and asset prices. *JPE*, 119(4). `[U]`
- Shumway, T. (1997). The delisting bias in CRSP data. *JF*, 52(1). `[U]`
- Shumway, T., & Warther, V. (1999). The delisting bias in CRSP's Nasdaq data. *JF*, 54(6). `[U]`
- van Binsbergen, J., Brandt, M., & Koijen, R. (2012). On the timing and pricing of dividends. *AER*, 102(4). `[U]`
- Vassalou, M., & Xing, Y. (2004). Default risk in equity returns. *JF*, 59(2). `[U]`
- Wachter, J. (2013). Can time-varying risk of rare disasters explain aggregate stock market volatility? *JF*, 68(3). `[V]`
- Taking over the size effect: Asset pricing implications of merger activity. Working paper. `[V, authors to verify]`
- Equity duration and predictability. (2025). *JFE*. `[V, authors to verify]`
- Asset pricing with costly and delayed firm entry. *Macroeconomic Dynamics*. `[V, authors to verify]`