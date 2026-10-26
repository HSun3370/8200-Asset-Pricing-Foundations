# AI Usage Summary — BUSFIN 8200, Problem Set 2

This file is a factual record of how AI was used while producing Problem Set 2. It is
descriptive only and makes no assessment of the work or of the use of AI.

**Evidence used.** `Pset 2/AI_INTERACTIONS.md` (13 entries, written at the time of each
interaction); the Git history from `1b4ab91`, the first commit of the Problem Set 2 record,
through `ea955d4`, the snapshot taken before this file was written; and the differences
between the Git commits made before and after each interaction.

**Attribution.** Every commit in this repository has the same Git author, so authorship
alone cannot separate work done by the student from work done by AI. A change is attributed
to AI only where `AI_INTERACTIONS.md` records AI making it. Changes recorded in a commit that
falls between two interactions (usually the next pre-work commit) are described by what the
commit contains. `AI_INTERACTIONS.md` labels those changes as the student's own; this file
reports that label as the log's description and does not make an attribution of its own.
`HW2-answers.pdf` is the compiled output of `Pset 2/answers.md`, defined by `myst.yml`. It is
regenerated whenever the PDF is built, by AI during interactions and outside them otherwise.

**Structure.** The summary table comes first. Sections then follow the problem set's order,
and within each item the interactions appear chronologically. One interaction concerned the
build of the whole document rather than a single question; it has its own section first.
Three interactions covered several items in one prompt (Entries 7, 10 and 12). Each is
reported once, under the combined heading of the items it covered. Each interaction reports
the eight items required by `AI_POLICY.md` §2(e). Where the record does not support an item,
it says "not shown in the available record".

---

## Summary table

| Problem-set item | AI interactions | Main types of AI assistance |
|---|---|---|
| Whole document (PDF build) | 1 (Entry 2) | Code debugging (build configuration); formatting/translation |
| Q1(a), Q1(b) | 1 (Entry 1) | Formatting/translation; other (setting up the Pset 2 record) |
| Q1(c), Q1(d), Q1(e) | 0 (Entry 1 noted a symbol inconsistency in 1(e) in passing) | — |
| Q2(a) | 2 (Entries 3, 4) | Empirical coding; formatting/translation |
| Q2(b) | 1 (Entry 5) | Empirical coding; formatting/translation |
| Q2(c) | 1 (Entry 6) | Empirical coding; formatting/translation |
| Q2(d) | 1 (Entry 7, shared with Q2(e)) | Empirical coding; formatting/translation |
| Q2(e) | 1 (Entry 7, shared with Q2(d)) | Empirical coding; formatting/translation |
| Q3(a) | 1 (Entry 8) | Code debugging (build configuration); formatting/translation |
| Q3(b) | 1 (Entry 9) | Empirical coding; formatting/translation |
| Q3(c) | 1 (Entry 10, shared with Q3(d), Q3(e)) | Empirical coding; formatting/translation |
| Q3(d) | 1 (Entry 10) | Empirical coding; formatting/translation |
| Q3(e) | 1 (Entry 10) | Empirical coding; formatting/translation |
| Q4(a) | 0 | — |
| Q4(b) | 1 (Entry 11) | Empirical coding; formatting/translation |
| Q4(c) | 3 (Entry 11, request declined; Entries 12, 13) | Math review; empirical coding; other (declining a derivation request) |
| Q4(d) | 1 (Entry 12, shared with Q4(c), Q4(e)) | Empirical coding; formatting/translation |
| Q4(e) | 1 (Entry 12) | Empirical coding; formatting/translation |

Total: 13 logged interactions, each with a pre-work commit and a post-work commit.

---

## Whole document (PDF build)

### PDF build — Entry 2 (2026-10-02), commits `49e1d34` → `9ecbed9`

1. **Purpose.** The student pasted a failing `jupyter-book build --pdf` log (`unknown
   variable: infty`, plus a duplicate-`abstract` warning) and wrote "debug".
2. **Work before AI.** At `49e1d34`, `answers.md` held the Question 1 answers, including
   the matrix formatted in Entry 1, with the arrow now written `\;-->\;` (the one change in
   this commit). `myst.yml`, as of the previous commit `6bcbe2a`, named the output
   `HW2-answers.pdf` and had all three `articles:` lines commented out.
3. **AI assistance.** Diagnosed the failure: with no article listed, MyST exported every
   Markdown file in the repository into the PDF, including `Pset 1/AI_INTERACTIONS.md`,
   whose `∞` character the Typst exporter writes as the invalid name `infty`. Fixed it by
   uncommenting the Pset 2 article, rebuilt the PDF, and checked the rendering. Noted, without
   changing them, that `-->` works only in the Typst export (`\longrightarrow` works in every
   renderer) and that the `∞` conversion would recur if such a file were exported.
4. **AI modifications.** `myst.yml`: one line uncommented, written as
   `- file: Pset 2/answers.md` with a forward slash. `HW2-answers.pdf` was produced by the
   build AI ran. `AI_INTERACTIONS.md` (Entry 2).
5. **Substantive decisions.** None. The entry records a build-configuration fix only.
   Writing the path with a forward slash, so it also resolves on macOS/Linux, was a
   mechanical choice made by AI.
6. **State after AI.** `9ecbed9` changes one line of `myst.yml`, adds `HW2-answers.pdf` and
   adds 21 lines to the log. `answers.md` is unchanged.
7. **Subsequent work.** The next pre-work commit, `367a432`, adds the BM and Fama-French data
   files under `Pset 2/Data/` and `Slides/BUSFIN 8200 - Summary of Readings.pdf`, rebuilds
   `HW2-answers.pdf`, and changes `answers.md` (listed under Entry 3).
8. **Type of AI use.** Code debugging (build configuration); formatting or translation.

---

## Question 1

### Q1(a) and Q1(b) — Entry 1 (2026-10-02), commits `1b4ab91` → `6bcbe2a`

1. **Purpose.** Start a separate AI record for Problem Set 2, and convert the plain-text
   elimination matrix in the 1(a)/1(b) answer into LaTeX so the PDF shows a typeset matrix.
2. **Work before AI.** Commit `1b4ab91` adds `Pset 2/answers.md` (43 lines) with written
   answers to all of Question 1: the elimination result `[X,P] -> [[1,0,0,0.2],…]` in plain
   text, contingent-claim prices (0.2, 0.4, 0.2), the price of asset D (16), the SDF
   M = 0.8 in each state with statements on no-arbitrage and risk neutrality, and the 1(e)
   pricing sum. The headings are empty `###` lines. The same commit also contains changes
   outside Problem Set 2 (`Research Ideas/NREE.md`, `MREE.pdf`, `myst.yml`) and moves of the
   course files into `Pset 2/` and of `HW1.pdf` into `Pset 1/`. No Pset 2 code existed.
3. **AI assistance.** Replaced the plain-text block with a `bmatrix` block and `->` with
   `\rightarrow`, keeping every entry, its order and the left-hand side. Checked the
   rendering in a scratch build outside the repository. Noted without changing anything:
   (i) in 1(e) the sum is written with `p(i)` while its numbers use 0.8, the SDF value
   `M(i)`; (ii) the 1(a)–1(e) headings are empty, and 1(a) has no text under it.
4. **AI modifications.** `Pset 2/answers.md` (the one display block; formatting only). Created
   `Pset 2/AI_INTERACTIONS.md` with the Pset 1 header and template, plus Entry 1.
5. **Substantive decisions.** None. Choosing `bmatrix` and `\rightarrow` was a formatting
   choice. Item (i) is recorded as pointing out an inconsistency without proposing a
   correction.
6. **State after AI.** `6bcbe2a` changes `answers.md` by +7/−5 lines (the matrix block) and
   creates the log (77 lines). The same commit also changes `myst.yml` by +3/−2 lines: the
   output is renamed from `MREE.pdf` to `HW2-answers.pdf`, the `Research Ideas\NREE.md`
   article is commented out, and a commented `Pset 2\answers.md` line is added. Entry 1 does
   not list `myst.yml` among AI's modifications. Entry 2 records the resulting state of
   `myst.yml` as the cause of the next build failure.
7. **Subsequent work.** `49e1d34` changes the arrow in the new matrix block from
   `\;\rightarrow\;` to `\;-->\;`. Later, `367a432` changes the 1(e) sum from `p(i)` to
   `M(i)`, adds "Yes, see reasoning in 1b." under 1(a) and a sentence defining `X`, `P` and
   `p`, and changes the no-arbitrage sentence to "strictly positive and unique". No later AI
   interaction concerns Question 1.
8. **Type of AI use.** Formatting or translation; other (setting up the record).

---

## Question 2

### Q2(a) — Entry 3 (2026-10-03), commits `367a432` → `94db1cb`

1. **Purpose.** Implement the student's Q2(a) specification: excess returns of the BM
   deciles, the SDF M* = a − b′xR with E[M*·xR] = 0 and E[M*] = 1, two-step GMM, estimates
   with standard errors, and a scatterplot of b by decile.
2. **Work before AI.** At `367a432` the repository held `Pset 2/Data/Portfolios_Formed_on_BE-ME.csv`
   and `Pset 2/Data/F-F_Research_Data_Factors.csv`, and `answers.md` had a Question 2 heading
   with the placeholder line "nm". No Pset 2 code existed. The specification is the student's
   prompt, quoted in Entry 3: the data files, a column list, xR_t, the SDF form, the two
   moment conditions, two-step GMM, and the outputs.
3. **AI assistance.** Before coding, flagged four open points and asked the student to
   choose: (1) the column list included `Hi 20`, a quintile nearly collinear with the top
   deciles, while the prompt said 10 portfolios; (2) the sample period; (3) percent vs.
   decimal units; (4) the estimator of S. Told the student that 11 moments and 11 parameters
   make the system exactly identified, so the weighting matrix does not affect the
   estimates. Wrote and ran `code/q2a.py`: â = 1.0368 (s.e. 0.0119) and ten b̂ values with
   Newey-West standard errors (lag 19). Checked the step-1/step-2 agreement, ḡ = 0, the mean
   of M* = 1, and an independent closed-form solution (agreement to 3.5e-13).
4. **AI modifications.** Created `code/q2a.py` and the outputs `output/q2a_gmm.csv`,
   `q2a_gmm_table.md` and `q2a_b_scatter.png`. `AI_INTERACTIONS.md` (Entry 3). `answers.md`
   was not edited.
5. **Substantive decisions.** The student chose: the 10 deciles only (no `Hi 20`), the sample
   1927:07–2026:08, decimals, and Newey-West S with the automatic NW (1994) lag. AI's choices
   within that method, disclosed in the entry: Bartlett weights with Ω_l = 1/(T−l) (taken
   from the student's Pset 1 code; the 1/T alternative changes the s.e. by at most 0.08%),
   the bandwidth applied to the sum of the standardized moment series (as in `linearmodels`),
   and W = I in step 1 (no effect under exact identification). Programming choices: the
   closed-form linear GMM step, file layout and plot styling.
6. **State after AI.** `94db1cb` adds `q2a.py` (220 lines), the three outputs and 26 log
   lines. `answers.md` is unchanged.
7. **Subsequent work.** The next pre-work commit, `913fd82`, adds
   `Pset 2/Data/10_Portfolios_Prior_12_2.csv` (the MOM data).
8. **Type of AI use.** Empirical coding.

### Q2(a) — Entry 4 (2026-10-03), commits `913fd82` → `932fde8`

1. **Purpose.** "plz insert the figures you have in Pset 2 answers.md".
2. **Work before AI.** At `913fd82`, `answers.md` had the Q2(a) heading and the "nm"
   placeholder. The Entry 3 outputs existed in `Pset 2/output/`.
3. **AI assistance.** Inserted an include of the estimates table and a `{figure}` block for
   the scatterplot under the Q2(a) heading. The caption describes only what is plotted.
   Rebuilt and checked the PDF. Only one figure existed, so AI also inserted the table and
   told the student it could be removed.
4. **AI modifications.** `answers.md` (two inserted blocks; no existing text changed);
   `HW2-answers.pdf` (rebuilt); `AI_INTERACTIONS.md` (Entry 4).
5. **Substantive decisions.** None. Including the table was a reading of the request,
   disclosed in the entry.
6. **State after AI.** `932fde8` adds 10 lines to `answers.md`, rebuilds the PDF and adds 20
   log lines.
7. **Subsequent work.** `da46a05` removes the "nm" placeholder and adds a Q2(b) heading. As
   of `ea955d4`, the Q2(a) section of `answers.md` contains only the AI-inserted table and
   figure. No text describing or explaining the scatterplot pattern appears there.
8. **Type of AI use.** Formatting or translation.

### Q2(b) — Entry 5 (2026-10-03), commits `da46a05` → `d25900c`

1. **Purpose.** "Do the same as 2a" for the 10 momentum deciles, report the same table and
   figure, and compute and report the correlation between the two SDFs in `answers.md`.
2. **Work before AI.** At `da46a05`: the MOM data file, `code/q2a.py` and its outputs, and
   `answers.md` with the Q2(a) table and figure and an empty Q2(b) heading.
3. **AI assistance.** Applied every Q2(a) decision to the MOM deciles and stated each one in
   the script's docstring. Refactored `q2a.py` into reusable functions, and verified that the
   Q2(a) outputs were reproduced byte for byte. Wrote and ran `code/q2b.py`: â = 1.0666
   (s.e. 0.0154), ten b̂ values (lag 3), and Corr(M*_BM, M*_MOM) = 0.3555 (checked against a
   closed-form computation). Inserted the table, the figure and one sentence reporting the
   correlation value into `answers.md`. Rebuilt the PDF. The log also records a syntax error
   introduced and fixed during the refactor, before anything was committed.
4. **AI modifications.** `code/q2a.py` (refactor), new `code/q2b.py`, five outputs
   (`q2b_gmm.csv`, `q2b_gmm_table.md`, `q2b_b_scatter.png`, `q2b_sdf_series.csv`,
   `q2b_sdf_corr.csv`), `answers.md`, `HW2-answers.pdf`, `AI_INTERACTIONS.md` (Entry 5).
5. **Substantive decisions.** None new. All empirical choices were carried over from Entry 3.
   Using the Pearson correlation of the fitted series over their common months is recorded
   as AI's reading of "the correlation between two SDF". The sentence inserted in
   `answers.md` reports the number only; the entry records that no interpretation was
   written.
6. **State after AI.** `d25900c` changes `q2a.py` by +43/−16, adds `q2b.py` (68 lines), the
   outputs, 12 lines of `answers.md`, the rebuilt PDF and 22 log lines.
7. **Subsequent work.** `62fc188` (the next pre-work commit) is empty. Later, `7f16ddf` adds an
   interpretation sentence under 2(b): "This correlation means that two SDF has 35.55%
   explanation power …". The log records that AI did not review this text.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(c) — Entry 6 (2026-10-03), commits `62fc188` → `4bef166`

1. **Purpose.** Repeat Q2(a) on the 20 merged BM and MOM portfolios with a two-color
   scatterplot, and report the Sharpe ratios of xR* = b′xR from 2(a), 2(b) and 2(c).
2. **Work before AI.** `62fc188` is an empty commit, so the state equals `d25900c`: Q2(a) and
   Q2(b) code, outputs and answer-sheet content. No Q2(c) heading existed.
3. **AI assistance.** Checked that the 20-portfolio system is well-conditioned and told the
   student it is again exactly identified. Asked two questions: the Sharpe-ratio frequency,
   and whether to insert the results into `answers.md`. Added an optional `plot` argument to
   `save_results()`, and verified that the 2(a)/2(b) outputs were unchanged. Wrote and ran
   `code/q2c.py`: â = 1.0927 (s.e. 0.0195), 20 b̂ values (lag 7), and annualized Sharpe
   ratios of 0.6646, 0.8937 and 1.0545. Inserted the table, the figure (blue BM, red MOM) and
   the Sharpe table under a new empty 2(c) heading. Rebuilt the PDF.
4. **AI modifications.** `code/q2a.py` (+5/−3), new `code/q2c.py`, five outputs, `answers.md`,
   `HW2-answers.pdf`, `AI_INTERACTIONS.md` (Entry 6).
5. **Substantive decisions.** The student chose annualized Sharpe ratios only (√12 × monthly
   mean / s.d., with divisor T−1), and the insertion into `answers.md`. Everything else was
   carried over from Entry 3. Ordering the parameters BM first, then MOM, and the plot
   styling are recorded as presentation choices. The entry records that AI did not name or
   hint at the "key SDF property" the question asks about.
6. **State after AI.** `4bef166` adds `q2c.py` (97 lines), the outputs, 15 lines of
   `answers.md`, the rebuilt PDF and 25 log lines.
7. **Subsequent work.** `7f16ddf` adds a paragraph under 2(c) ("SDF constructed using 20
   portfolios has higher sharpe ratio than other two. …") and an empty heading for 2(d).
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(d) and Q2(e) — Entry 7 (2026-10-03), commits `7f16ddf` → `aef3c3c`

1. **Purpose.** Compute 2(d): the pricing errors α_p = Ê[xR_p] − Ĉov(−M*, xR_p) of the 20
   portfolios under the three SDFs. Compute 2(e): the 2(c) construction on data through
   1989:12, the out-of-sample SDF from 1990:01, and α_OS,p over 1990:01–end.
2. **Work before AI.** At `7f16ddf`: the Q2(a)–(c) code and outputs; `answers.md` with
   interpretation text under 2(b) and 2(c) and an empty heading for 2(d). The student's
   prompt gave the α formula, the use of realized averages, and the 2(e) procedure.
3. **AI assistance.** Asked three questions (the covariance divisor, the units of α, and what
   to insert). Wrote and ran `code/q2d.py` and `code/q2e.py`. 2(d): α ≈ 0 for each SDF on its
   own test assets; non-zero α for the other assets (MOM α under the BM SDF from −1.0157 to
   0.5418, BM α under the MOM SDF from −0.1511 to 0.3450; percent per month). 2(e):
   estimates on 1927:07–1989:12 (â = 1.1248, lag 21) and α_OS from 0.4322 to 2.7055. All α
   were recomputed independently (agreement to 3e-14). Inserted the 2(d) table under the
   existing heading, and a new 2(e) heading with a one-line lead-in sentence and two tables.
   Rebuilt the PDF.
4. **AI modifications.** New `code/q2d.py` and `code/q2e.py`; six outputs; `answers.md`;
   `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 7).
5. **Substantive decisions.** The student chose: divide by T, percent per month, and insert
   the α tables plus the 2(e) estimates. Carried over: the data, the SDF construction, the
   sample start 1927:07, and the GMM settings. Reading "xP_p" as xR_p is recorded as reading
   a typo. AI did not normalize M*_OS; the formula was applied as given.
6. **State after AI.** `aef3c3c` adds `q2d.py` (77 lines) and `q2e.py` (78 lines), the
   outputs, 13 lines of `answers.md`, the rebuilt PDF and 27 log lines.
7. **Subsequent work.** `2f1e723` adds the Q3(a) derivation (see Entry 8). Later, `6950f6b`
   adds interpretation text under 2(d) ("Every SDF perfectly prices excess returns of
   portfolios where SDF comes from …") and under 2(e) ("Out of sample pricing errors are
   non-zero for all portfolios …").
8. **Type of AI use.** Empirical coding; formatting or translation.

---

## Question 3

### Q3(a) — Entry 8 (2026-10-03), commits `2f1e723` → `86b7707`

1. **Purpose.** The student pasted a build error (`unknown variable: diff`) on the FOC
   equation of the Q3(a) derivation. The entry records this as a request to debug the build.
2. **Work before AI.** Commit `2f1e723` adds the Q3(a) derivation to `answers.md`: the
   portfolio-choice problem, the FOC with respect to ω̄_t, and the conclusion that the
   FOC prices all excess returns. It also adds an empty Q3(b) heading and a rebuilt PDF.
3. **AI assistance.** Diagnosed a toolchain incompatibility: MyST converts `\partial` to the
   Typst name `diff`, which Typst 0.15.1 no longer defines. Added `#let diff = sym.partial` to
   the existing `{raw:typst}` block, rebuilt the PDF and checked the rendering. The log
   records that the derivation was not checked, since no math check was requested.
4. **AI modifications.** `answers.md` (one line in the raw Typst block; the derivation text
   was unchanged); `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 8).
5. **Substantive decisions.** None.
6. **State after AI.** `86b7707` adds one line to `answers.md`, rebuilds the PDF and adds 19
   log lines.
7. **Subsequent work.** `6950f6b` edits the derivation: `\bar \omega_t'` becomes
   `\bar \omega_t^*'`, and the conclusion becomes "Thus, $M_t = R_{\omega_t^*,t+1}^{-\gamma}$
   prices all excess returns." The same commit moves `EQ Dataset.csv` into `Pset 2/Data/`.
   Entry 9 reports that the edited line triggers a "double superscript" LaTeX warning; the
   line is unchanged as of `ea955d4`.
8. **Type of AI use.** Code debugging (build configuration); formatting or translation.

### Q3(b) — Entry 9 (2026-10-04), commits `6950f6b` → `fa36e46`

1. **Purpose.** Estimate γ by GMM from E[R_w^(−γ)·xR_w] = 0, with R_w = exp(re) and
   xR = exp(re) − exp(rf) from the EQ dataset and Newey-West S, and report the result in
   `answers.md`.
2. **Work before AI.** At `6950f6b`: `Pset 2/Data/EQ Dataset.csv`, the edited Q3(a)
   derivation, and an empty Q3(b) heading. The specification is the student's prompt: the
   data, variable definitions, moment condition, GMM, Newey-West S, and the report.
3. **AI assistance.** Asked no questions, and recorded how the specification was applied: the
   full sample 1927:12–2021:12, same-row timing, the Q2 Newey-West convention, and a check
   that a root of ḡ(γ) exists (footnote 5). Wrote and ran `code/q3b.py`: γ̂ = 1.9061
   (s.e. 0.6026, t = 3.16, lag 26). Checked G by finite differences and S against
   statsmodels (s.e. 0.6015 with 1/T normalization). Inserted the table include under the
   Q3(b) heading and rebuilt the PDF. Reported a LaTeX "double superscript" warning in the
   Q3(a) text and a form that renders in every engine, without changing it.
4. **AI modifications.** New `code/q3b.py`; `output/q3b_gmm.csv`, `q3b_gmm_table.md`;
   `answers.md` (one include); `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 9).
5. **Substantive decisions.** None by AI. The entry describes the sample, timing and
   Newey-West convention as readings of the student's specification. Root-finding by grid
   scan plus Brent's method is a programming choice.
6. **State after AI.** `fa36e46` adds `q3b.py` (103 lines), two outputs, 3 lines of
   `answers.md`, the rebuilt PDF and 27 log lines.
7. **Subsequent work.** The next pre-work commit, `448e034`, contains only a rebuilt PDF. As
   of `ea955d4`, the Q3(b) section contains only the AI-inserted table.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q3(c), Q3(d) and Q3(e) — Entry 10 (2026-10-04), commits `448e034` → `d073713`

1. **Purpose.** 3(c): GMM for γ with the market moment and the managed-portfolio moment
   z_{t−1}·xR_w (z_t = E^OS_t[xR_e]/σ²_e), identity weighting, and a table of γ, pricing
   errors, t-stats and the χ² p-value. 3(d): the same with two-step GMM. 3(e): add the BM and
   MOM portfolios to the moments.
2. **Work before AI.** At `448e034` (only a rebuilt PDF changed): the Q3(b) code and
   `answers.md` ending with the Q3(b) table. The student's prompt defined the moments, z_t,
   σ²_e and E^OS (a = average G − 1, b = average G, G = exp(dg)), the identity weighting,
   the table contents and Newey-West S.
3. **AI assistance.** Read the student's Pset 1 Q2(e) forecast code. Asked seven questions in
   two rounds (listed below). Wrote `code/q3c.py` (shared GMM code plus 3(c)), `q3d.py` and
   `q3e.py`. Rebuilt the Pset 1 out-of-sample forecast inside Pset 2 and asserted that it
   matches the saved Pset 1 output. Results (1940:12–2021:12, T = 973, lag 24):
   3(c) γ̂ = 3.0147 (s.e. 0.7174), χ²(1) = 0.770, p = 0.380; 3(d) γ̂ = 2.9736 (s.e. 0.7109),
   χ²(1) = 0.789, p = 0.374; 3(e) γ̂ = 2.9999 (s.e. 0.7044), χ²(21) = 217.09, p < 0.0001.
   Checked the FOC, the eigenvalues of Var(ḡ), and a hand-computed compounded return.
   Inserted three empty headings and table includes, and rebuilt the PDF. Noted a page-break
   rendering quirk in the 3(e) table.
4. **AI modifications.** New `code/q3c.py`, `q3d.py`, `q3e.py`; six outputs; `answers.md`;
   `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 10).
5. **Substantive decisions.** The student chose: (1) E^OS from Pset 1 Q2(e) (the option AI
   labeled "Recommended"), which sets the sample start at 1940:12; (2) σ²_e over the
   estimation sample; (3) centered S; (4) S re-estimated at the 3(d) estimate for
   inference; (5) 12-month compounded nominal BM/MOM excess returns (the option AI labeled
   "Recommended"); (6) 22 moments in 3(e), keeping the z moment, where the problem text
   lists 21; (7) insertion into `answers.md`. The entry identifies the two "Recommended"
   labels as AI suggestions. Carried over or standard: identity weighting in 3(e),
   W = Ŝ(3c)⁻¹ in 3(d), the Newey-West convention, and the GMM sandwich and χ² formulas
   with a rank-(K−1) pseudo-inverse.
6. **State after AI.** `d073713` adds `q3c.py` (193 lines), `q3d.py` (45), `q3e.py` (72),
   six outputs, 15 lines of `answers.md`, the rebuilt PDF and 32 log lines.
7. **Subsequent work.** `f6c9b0d` adds the Q4(a) answer and three slide PDFs (see Entry 11).
   As of `ea955d4`, the Q3(c)–(e) sections contain only the AI-inserted tables.
8. **Type of AI use.** Empirical coding; formatting or translation.

---

## Question 4

### Q4(b) — Entry 11 (2026-10-24), commits `f6c9b0d` → `120421e`

1. **Purpose.** 4(b): estimate b in M_t = 1 − b(R_w − E[R_w]) from E[M·xR] = 0, with xR_w and
   the 20 BM/MOM portfolios, identity weighting, and a table with χ². The same prompt asked
   for 4(c): "derive the analytical expression and compute it".
2. **Work before AI.** Commit `f6c9b0d` adds the Q4(a) answer (Taylor-expansion and
   Stein's-lemma derivations of a_t and b_t, and a paragraph on the disadvantage of the
   approximation), an empty Q4(b) heading, and three slide PDFs.
3. **AI assistance.** Declined to derive the 4(c) expression, citing `AI_POLICY.md` §1(a), and
   offered numerical computation or a check of the student's own expression. The student
   chose to derive first, so 4(c) was not implemented. For 4(b), asked five questions (listed
   below) and ran a scratch comparison of two weighting options, not saved in the
   repository. Wrote and ran `code/q4b.py`, which estimates numerically with a
   finite-difference Jacobian so that no closed form appears in the code: b̂ = 2.8559
   (s.e. 0.5908), μ̂ = 1.0360 (s.e. 0.0191; sample mean 1.0870), χ²(20) = 323.66,
   p < 0.0001. Inserted the table include and rebuilt the PDF. Reported that one display
   equation in the student's 4(a) text runs past the margin.
4. **AI modifications.** New `code/q4b.py`; `output/q4b_gmm.csv`, `q4b_gmm_table.md`;
   `answers.md` (one include); `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 11).
5. **Substantive decisions.** The student chose: (1) estimate E[R_w] jointly as μ with an
   extra moment; (2) the sample 1940:12–2021:12; (3) derive 4(c) first; (4) insertion into
   `answers.md`; (5) identity weighting on all 22 moments rather than pinning μ̂ to the
   sample mean. AI quoted preliminary point estimates for both weighting options before the
   student decided. Carried over: the data construction from 3(e), centered Newey-West S,
   and the GMM formulas. The entry records that no closed-form expression for b̂ appears in
   the code, the entry or AI's reply.
6. **State after AI.** `120421e` adds `q4b.py` (165 lines), two outputs, 3 lines of
   `answers.md`, the rebuilt PDF and 28 log lines.
7. **Subsequent work.** `161646c` adds the student's 4(c) derivation under a new heading: the
   minimization with weight S⁻¹, the FOC, and a final expression for b.
8. **Type of AI use.** Empirical coding; formatting or translation; other (declining a
   derivation request).

### Q4(c), Q4(d) and Q4(e) — Entry 12 (2026-10-24), commits `161646c` → `3535964`

1. **Purpose.** "check if my derviation is right or not. then compute for question 4c and do
   4d and 4e."
2. **Work before AI.** At `161646c`: `answers.md` with the 4(b) table and the student's 4(c)
   derivation, ending in `b = (c′S⁻¹c)⁻¹ c′S⁻¹` (in the log's notation). The prompt gave no
   specification for 4(d)/4(e) beyond the problem text.
3. **AI assistance.** *Math review.* Flagged five points without writing a correction:
   (1) the final expression is a 1×K vector, not a scalar, because the term of ḡ(b) that does
   not involve b is dropped after the FOC; (2) the notation R_{t+1} versus same-dated excess
   returns; (3) E[R_w] is held fixed while 4(b) estimated it; (4) S is treated as fixed,
   which is correct for two-step GMM; (5) the loose term "covariance matrix of pricing
   errors". *Empirical work.* Asked seven questions in two rounds (listed below). Read the
   course slides for the GRS and Fama-MacBeth formulas. Wrote `q4c.py`, `q4d.py` and
   `q4e.py`. Results: 4(c) efficient b̂ = 6.9259 (s.e. 0.7717), χ²(20) = 70.87; 4(d)
   λ̂ = 1.0870 (s.e. 0.0164), α̂_j from −0.885 to −1.555, GRS = 1179.65 (p ≈ 0); 4(e)
   λ̂ = 0.09467 (s.e. 0.01621), α̂_j from −0.11638 to 0.05531. AI told the student that the
   4(d) α's follow mechanically from using a gross-return factor, and offered to re-run with
   xR_w; nothing was changed. Checked against an independent minimizer, statsmodels OLS/HAC,
   the original GRS form, and FM residual orthogonality. Inserted three table includes (4(c)
   after the derivation; new 4(d) and 4(e) headings) and rebuilt the PDF.
4. **AI modifications.** `code/q4b.py` (optional moment-function argument; outputs verified
   unchanged); new `code/q4c.py`, `q4d.py`, `q4e.py`; eight outputs; `answers.md` (three
   includes, plus a line break and a blank line after the derivation's closing `$$`);
   `HW2-answers.pdf`; `AI_INTERACTIONS.md` (Entry 12).
5. **Substantive decisions.** The student chose: (1) 4(c) with μ fixed at the sample mean
   (21 moments), matching the derivation; (2) the gross return R_w as the 4(d)/4(e) factor,
   after AI noted in the question (citing the course slides) that α_j are pricing errors and
   λ = E[f] when the factor is an excess return; (3) the 21 test assets of 4(b); (4) the
   sample 1940:12–2021:12; (5) full-sample betas; (6) no intercept in the cross-sectional
   regressions; (7) insertion into `answers.md`. The entry records the excess-return note as
   an econometric caution by AI that the student did not adopt. Other choices recorded as
   carried over or taken from course/standard formulas: the regression NW lag rule from the
   student's Pset 1 code, and the GRS form from the slides/Cochrane. Numerical estimation of
   4(c) is recorded as a programming choice.
6. **State after AI.** `3535964` changes `q4b.py` by +12/−9, adds `q4c.py` (96 lines),
   `q4d.py` (120) and `q4e.py` (74), eight outputs, +14/−1 lines of `answers.md`, the rebuilt
   PDF and 36 log lines.
7. **Subsequent work.** `bbe7250` changes the final line of the 4(c) derivation to end in
   `Ê[R_{t+1}]`. Entry 13 records that AI did not write this change.
8. **Type of AI use.** Math review; empirical coding; formatting or translation.

### Q4(c) — Entry 13 (2026-10-24), commits `bbe7250` → `8cf4e26`

1. **Purpose.** "i corrected my derviation. check if it is correct and see if it align with
   your numerical computation".
2. **Work before AI.** Commit `bbe7250` changes one line of `answers.md`: the final
   expression becomes `b = (c′S⁻¹c)⁻¹ c′S⁻¹ Ê[R_{t+1}]`. The other lines of the derivation are
   unchanged from `161646c`.
3. **AI assistance.** Confirmed that the error flagged in Entry 12 is resolved and found no
   remaining algebraic error. Repeated two points still open: the notation R_{t+1}, and
   wording that does not say S is the first-step estimate. Implemented the student's
   expression in `q4c.py`: 6.925904157 with S = S₁, versus 6.925904477 numerically
   (difference −3.2e-7); 3.285957697 with S = I, matching the identity first step.
4. **AI modifications.** `code/q4c.py` (evaluates the student's expression, asserts agreement
   with the numerical estimates, writes two CSV rows; estimation method and reported table
   unchanged); `output/q4c_gmm.csv` (two rows); `AI_INTERACTIONS.md` (Entry 13). `answers.md`
   and the PDF were not changed.
5. **Substantive decisions.** None. The expression implemented is the student's own. The
   entry reads the student's Ê[R_{t+1}] as Ê[xR_t] for the check.
6. **State after AI.** `8cf4e26` changes `q4c.py` by +18/−2, adds two lines to
   `q4c_gmm.csv` and adds 22 log lines.
7. **Subsequent work.** Commit `09dd0cf` ("hw2", 2026-10-24) changes only `HW2-answers.pdf`;
   it is not covered by any entry. `ea955d4` (2026-10-26) is the empty snapshot made before
   this file. As of `ea955d4`, the 4(b)–4(e) sections contain the AI-inserted tables and the
   student's 4(c) derivation, with no other text.
8. **Type of AI use.** Math review; empirical coding.

---

## Notes on the record itself

- **Pairing.** Each of the 13 interactions has a pre-work commit (`TP: before …`) cited in
  `AI_INTERACTIONS.md` and a matching post-work commit (`TP: after …`) that adds its entry.
  Pre-work commit `62fc188` is empty, and `448e034` contains only a rebuilt PDF.
- **Commits outside the interaction pairs.** `09dd0cf` ("hw2") changes only
  `HW2-answers.pdf` and is not covered by any entry. `ea955d4` is the snapshot made before
  this file. Commit `6bcbe2a` (the Entry 1 post-work commit) contains a `myst.yml` change that
  Entry 1 does not list among AI's modifications; its origin is not shown in the available
  record.
- **Changes outside Problem Set 2 inside Pset 2 commits.** Commit `1b4ab91` also records
  changes to `Research Ideas/NREE.md`, `MREE.pdf`, `myst.yml`, and the move of `HW1.pdf`.
  Commits `367a432` and `f6c9b0d` add slide PDFs under `Slides/`.
- **Requests not logged.** Under `AI_POLICY.md` §2(c), requests treated as administrative
  (no change to problem-set content or files) are not logged in `AI_INTERACTIONS.md`, so
  they are not covered here.
- **Derivation requests.** In Entry 11, AI declined to derive the 4(c) expression. In
  Entry 12, AI flagged and explained an error in the student's derivation without writing
  the correction. In Entry 13, AI verified the student's corrected expression. Entries 8 and 9
  record that the Q3(a) derivation was not checked, and Entry 11 records the same for the
  Q4(a) derivation; no math check was requested for either.
- **Interpretive text.** Every entry that inserted results into `answers.md` records that no
  interpretation was written. The interpretation sentences under 2(b), 2(c), 2(d) and 2(e)
  first appear in pre-work commits (`7f16ddf`, `6950f6b`). The two descriptive sentences AI
  inserted (the 2(b) correlation value and the 2(e) lead-in) report numbers and table
  contents only.
- **Corrections inside the record.** No entry was edited or removed; the file grows only by
  appending. Entry 13 records the resolution of the error flagged in Entry 12. Entries 5 and
  7 record AI's own tool errors (a syntax error, a failed edit anchor, a failed heredoc
  append), each fixed before the related commit.
- **Data files.** All Problem Set 2 inputs (`Pset 2/Data/*.csv`) are committed to the
  repository. Question 3(c)–(e) also reads `Pset 1/output/q2e_forecasts.csv`, only as a
  consistency check on the rebuilt forecast.
- **This file.** `AI_USAGE.md` was generated by AI from the sources named at the top, using
  the prompt in `AI_POLICY.md` §2(e). `AI_INTERACTIONS.md` was not modified while producing
  it, and no other existing project file was changed. Commit `ea955d4` records the repository
  state before this file was written, and the commit that adds this file records the state
  after.
