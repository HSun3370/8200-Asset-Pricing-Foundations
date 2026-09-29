# AI Usage Summary — BUSFIN 8200, Problem Set 1

This file is a factual record of how AI was used while producing Problem Set 1. It is
descriptive only and makes no assessment of the work or of the use of AI.

**Evidence used.** `Pset 1/AI_INTERACTIONS.md` (26 entries, written at the time of each
interaction); the Git history from the first commit `db1e33d` through `833204b`; and the
differences between the Git commits recorded before and after each interaction.

**Attribution.** Every commit in this repository carries the same Git author, so authorship
alone cannot separate work done by the student from work done by AI. A change is attributed
to AI only where `AI_INTERACTIONS.md` records AI making it. Changes recorded in commits that
fall between two interactions are described by what the commit contains, without attributing
them to a person. `HW1.pdf` is the compiled output of `Pset 1/answers.md`; the interaction
log repeatedly records that it was rebuilt by the project's own build, outside AI's actions.

**Structure.** The summary table comes first. Sections then follow the problem set's order,
and within each item the interactions appear chronologically. Each interaction reports the
eight items required by `AI_POLICY.md` §2(e). Where the record does not support an item, it
says "not shown in the available record".

---

## Summary table

| Problem-set item | AI interactions | Main types of AI assistance |
|---|---|---|
| Q1(a) and Q1(e) | 1 (Entry 1) | Formatting/translation; math review |
| Q1(b) | 1 (Entry 2) | Empirical coding; code debugging |
| Q1(c) | 1 (Entry 3) | Empirical coding; math review |
| Q1(d) | 1 (Entry 4) | Empirical coding |
| Q2(a) | 1 (Entry 5) | Empirical coding; formatting/translation |
| Q2(b) | 1 (Entry 6) | Empirical coding; formatting/translation |
| Q2(c) | 1 (Entry 7) | Empirical coding; formatting/translation |
| Q2(d) | 1 (Entry 8) | Empirical coding; formatting/translation |
| Q2(e) | 1 (Entry 9) | Empirical coding; formatting/translation |
| Q3(a) | 3 (Entries 16, 17, 18) | Empirical coding; code debugging |
| Q3(b) | 3 (Entries 19, 20, 22) | Empirical coding; code debugging |
| Q3(c) | 1 (Entry 21) | Empirical coding; code debugging; formatting/translation |
| Q3(d) | 1 (Entry 23) | Empirical coding; code debugging |
| Q3(e) | 3 (Entries 24, 25, 26) | Empirical coding; formatting/translation; build diagnosis |
| Q4(a) | 2 (Entries 10, 11) | Empirical coding; formatting/translation |
| Q4(b) | 1 (Entry 12) | Empirical coding; code debugging; formatting/translation |
| Q4(c) | 1 (Entry 13) | Empirical coding; formatting/translation |
| Q4(d) | 1 (Entry 14) | Empirical coding; formatting/translation |
| Q4(e) | 1 (Entry 15) | Empirical coding; formatting/translation; record correction |
| **Total** | **26** | |

Across all 26 interactions the log records no instance of AI generating, completing or
rewriting a mathematical derivation or an economic argument, and no interpretation of
results written into `answers.md` by AI. Each interaction is paired with a Git commit before
and after it.

---

## Question 1

### Q1(a) and Q1(e) — Entry 1 (2026-08-30), commits `784db16` → `3b91a4b`

1. **Purpose.** Fix Markdown/MyST syntax and English grammar in the prose of the 1(a) and
   1(e) derivations, and check the mathematics.
2. **Work before AI.** The pre-work commit `784db16` adds 58 lines to `Pset 1/answers.md`.
   At that snapshot the file held the student's own written derivations for 1(a) and 1(e),
   with empty `###` headings where 1(b)–1(d) were unanswered and placeholder abstract text.
   No code existed for Question 1.
3. **AI assistance.** Converted 13 `$$\begin{align}…\end{align}$$` blocks to `aligned`, and
   made about 20 grammar and exposition edits, altering no mathematical expression. Checked
   the mathematics and flagged ten items without fixing them: an inconsistent middle
   expression in the `\kappa_0` definition; a repeated `r_{e,t+1}` index in three expanded
   recursions; a stray `\kappa_0` in the `H→∞` line; a missing `(1-\kappa)` in a commented
   line; the unstated Taylor-approximation and expectation justifications; the transversality
   argument; an index inconsistency and a false inequality in the 1(e) terminal condition;
   the absence of the final identity (1.9); an incorrectly written remainder term; and the
   unstated maintained assumptions.
4. **AI modifications.** `Pset 1/answers.md` (formatting and grammar only) and
   `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. The entry records that no mathematics was
   generated, completed or rewritten, and that the student determines and implements every
   correction. The single diagnostic suggestion was that the `H→∞` terminal condition be
   argued from stationarity and `κ ∈ (0,1)` rather than from the invalid inequality.
6. **State after AI.** Commit `3b91a4b` changes `answers.md` by 45 insertions and 45
   deletions, consistent with in-place formatting and grammar edits, and adds 31 lines to
   `AI_INTERACTIONS.md`.
7. **Subsequent work.** Commit `8f28f02` moves the interaction log to `Pset 1/` and updates
   the `@TP` skill. The next pre-work commit `f07aeb4` records 10 further lines in
   `answers.md` and a rebuilt `HW1.pdf`.
8. **Type of AI use.** Formatting or translation; math review.

### Q1(b) — Entry 2 (2026-08-30), commits `f07aeb4` → `e616388`

1. **Purpose.** Implement the student's Equation 1.4 construction as a runnable script
   producing the variance-decomposition figure.
2. **Work before AI.** At `f07aeb4` the repository held `answers.md` with the Question 1
   derivations and the two datasets. No `Pset 1/code/` directory existed. The student's
   prompt supplied the full construction: `κ` from the sample mean of `dp`, the three
   regressands, horizons 1–20, and the instruction to watch sample size and timing.
3. **AI assistance.** Flagged two design gaps and asked the student to decide: the timing
   convention for monthly observations of annual variables, and whether the third regressand
   carries the `κ^H` factor. Then wrote `code/q1b.py`, fixed one pandas-3.0 incompatibility,
   and ran it: `κ = 0.964228`, N = 1129, slopes summing to 1.00 at every horizon.
4. **AI modifications.** Created `code/q1b.py`, `output/q1b_slopes.csv` and
   `output/q1b_slopes.png`; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Both open choices were referred to the student,
   who chose overlapping monthly timing and the `κ^H dp_{t+H}` regressand. Mechanical choices
   by AI: Python, `np.polyfit` for the slope, row-shift alignment, file layout.
6. **State after AI.** Commit `e616388` adds `q1b.py` (136 lines), the CSV, the PNG and 21
   log lines. `answers.md` is unchanged in this commit.
7. **Subsequent work.** The next pre-work commit `ab591b9` records 8 added lines in
   `answers.md` and a rebuilt `HW1.pdf`, which is where the 1(b) figure enters the answer
   document.
8. **Type of AI use.** Empirical coding; code debugging.

### Q1(c) — Entry 3 (2026-08-30), commits `ab591b9` → `b1fa590`

1. **Purpose.** Implement the student's VAR-implied version of the Equation 1.4
   decomposition.
2. **Work before AI.** At `ab591b9`, `q1b.py` and its outputs existed, and `answers.md` had
   gained the 1(b) figure. The student's prompt gave the VAR specification, the formulas for
   `b_re` and `b_Δd`, the definition `b_z = Cov(dp_t, Z_t)/Var(dp_t)`, and the instruction to
   reuse the 1(b) `κ`.
3. **AI assistance.** Before this interaction AI had flagged three problems with an earlier
   draft of the student's formula: it returned a vector rather than a scalar, it used the
   innovation covariance where the unconditional covariance was needed, and it omitted a
   minus sign. Within the interaction AI flagged the still-missing minus and asked the
   student to decide. AI then wrote `code/q1c.py` and ran it, reporting stationary VAR
   eigenvalues, `b_z` with a `dp` element of exactly 1, slopes summing to 1 by construction,
   and agreement with the 1(b) estimates at `h = 1`.
4. **AI modifications.** Created `code/q1c.py`, `output/q1c_slopes.csv` and
   `output/q1c_slopes.png`; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. The sign correction and the specification
   revisions were made by the student. One minor point, whether `b_z` uses the full 1129-row
   sample or the 1117-row VAR-fit sample, was flagged with a stated default and not objected
   to. Mechanical choices: `np.linalg.lstsq`, the closed-form `M_H` with an assertion against
   the finite sum, a diagnostic column.
6. **State after AI.** Commit `b1fa590` adds `q1c.py` (161 lines), two outputs, 18 log lines,
   and 8 lines in `answers.md`.
7. **Subsequent work.** The next pre-work commit `af7ba35` records 7 added lines in
   `answers.md` and a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; math review.

### Q1(d) — Entry 4 (2026-08-30), commits `af7ba35` → `8abb9f2`

1. **Purpose.** Evaluate the Q1(c) decomposition at `H → ∞` and report the three values.
2. **Work before AI.** At `af7ba35` the 1(c) script and outputs existed and `answers.md`
   carried the 1(c) figure and text.
3. **AI assistance.** Recorded that no new design decision was required, since the limit is
   well defined for the stationary VAR already estimated. Wrote `code/q1d.py`, which imports
   the estimation functions from `q1c.py` so the VAR is identical, and ran it:
   `b_re^(∞) = 0.4892`, `b_Δd^(∞) = 0.5096`, `b_dp^(∞) = 0.0012`, with a consistency check
   against the theoretical value of 1.
4. **AI modifications.** Created `code/q1d.py`; `AI_INTERACTIONS.md`. No output files, since
   the student asked for the numbers in Markdown.
5. **Substantive decisions.** None. The entry records the `M_∞` limit as the closed form of
   the series the student had already written.
6. **State after AI.** Commit `8abb9f2` adds `q1d.py` (51 lines), 18 log lines, and a
   `__pycache__` file later removed by `38bd621`.
7. **Subsequent work.** Commit `38bd621` stops tracking `__pycache__`. Commit `4138169`,
   titled "finish question 1 of hw 1", adds 20 lines to `answers.md` along with two files
   under `Research Ideas/`.
8. **Type of AI use.** Empirical coding.

---

## Question 2

### Q2(a) — Entry 5 (2026-09-04), commits `001cee0` → `d746ff8`

1. **Purpose.** Implement the long-horizon regressions of average future excess returns on
   `D/P` for `H = 1…15` and insert the `R²_adj` figure into `answers.md`.
2. **Work before AI.** The pre-work commit `001cee0` is empty, so the working tree matched
   `4138169`: Question 1 complete in `answers.md`, three Q1 scripts and their outputs
   present, and Question 2 not started. The student's prompt specified the variables, the
   regression, the adjusted-`R²` formula and the figure.
3. **AI assistance.** Flagged one ambiguity and stopped: the prompt said the sample should be
   `n − H`, but the data are monthly observations of annual variables while `H` is in years.
   After the student chose the 12-month-per-year shift, AI wrote `code/q2a.py`, reused the
   loader conventions from `q1b.py`, ran it, and reported the full table of slopes and
   adjusted `R²` (0.0457 at `H = 1` rising to 0.4432 at `H = 14`).
4. **AI modifications.** Created `code/q2a.py`, `output/q2a_r2adj.csv` and
   `output/q2a_r2adj.png`; appended a figure block to `answers.md`; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. The timing convention was referred to the student,
   who chose `n − 12H`. AI recorded that this supersedes the `n − H` wording of the prompt.
   Mechanical choices: pandas/numpy structures, `np.polyfit`, dropping rows lacking a required
   future observation, output paths, figure styling matched to the Q1 figures. AI wrote no
   description of the results, noting that Q2(a) asks the student to describe them.
6. **State after AI.** Commit `d746ff8` adds `q2a.py` (125 lines), two outputs, 11 lines in
   `answers.md`, 42 log lines, and a rebuilt `HW1.pdf`.
7. **Subsequent work.** The next pre-work commit `2d7bb5a` records 11 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(b) — Entry 6 (2026-09-04), commits `2d7bb5a` → `2af8e0a`

1. **Purpose.** Estimate the one-year-ahead regression and report `b̂` with five standard-error
   estimators, prioritising established Python packages.
2. **Work before AI.** At `2d7bb5a` the Q2(a) script, outputs and figure existed. The student
   supplied the regression, the five `Ŝ` formulas, and the sandwich formula.
3. **AI assistance.** Installed `statsmodels` and `linearmodels`, read their source to match
   each routine against the student's written formulas, wrote `code/q2b.py`, and ran it:
   `b̂ = 2.8038` with standard errors 0.3798 (OLS), 0.6587 (White), 1.2990 (Newey–West, 11
   lags), 1.4537 (Hansen–Hodrick, 11 lags) and 1.2304 (Newey–West 1987/1994, `L = 24`).
   Verified that `b̂` reproduces the `H = 1` slope from Q2(a), reported the data-driven lag
   explicitly, and tested Hansen–Hodrick positive-definiteness.
4. **AI modifications.** Created `code/q2b.py`, `output/q2b_se.csv` and `output/q2b_se.tex`;
   appended a results block to `answers.md`; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Three items were flagged: package normalisation
   differs from the specification, so AI reported specification-exact numbers alongside the
   package values rather than adopting either silently; the aggregation of moment conditions
   inside the Newey–West (1994) bandwidth rule is not fixed by the problem statement, so AI
   used the package's own convention and flagged it for the student to confirm; and the
   repository had no dependency file, which AI raised without acting. AI wrote no
   interpretation of why the five standard errors differ.
6. **State after AI.** Commit `2af8e0a` adds `q2b.py` (213 lines), two outputs, 20 lines in
   `answers.md` and 37 log lines.
7. **Subsequent work.** The next pre-work commit `079ecb1` records 3 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`. Entry 7 identifies that edit as a shortened sentence
   in the Q2(b) block.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(c) — Entry 7 (2026-09-12), commits `079ecb1` → `b03881c`

1. **Purpose.** Implement the student's four-step Amihud–Hurvich procedure and report the
   estimates as equations in `answers.md`.
2. **Work before AI.** At `079ecb1`, Q2(a) and Q2(b) were complete in `answers.md` with their
   scripts and outputs. The student's prompt gave all four steps and the overlapping annual
   timing.
3. **AI assistance.** Ran the fully specified first step read-only to quantify an open
   choice, then stopped and asked two questions. After the student decided, wrote
   `code/q2c.py` reusing the Q2(b) loader and reported `θ̂ = 0.011058`, `φ̂ = 0.719736`,
   `φ̂^c = 0.754041`, `â = −0.031411`, `b̂ = 2.341244`, `b̂_u = −13.483728`, with the
   reference regression reproducing the Q2(b) slope of 2.803803.
4. **AI modifications.** Created `code/q2c.py` and `output/q2c_amihud_hurvich.csv`; appended
   the results block to `answers.md` and then removed its own heading line; created and
   deleted a one-off insertion helper; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Two ambiguities were referred to the student: the
   prompt's notation was internally inconsistent about which coefficient is bias-corrected,
   and `T` was undefined. The student chose the problem set's notation with the correction
   applied to the slope, and `T = 95`. AI wrote no contrast with Q2(b) and no explanation of
   why the estimates differ, recording that Q2(c) asks the student for both.
6. **State after AI.** Commit `b03881c` adds `q2c.py` (117 lines), one output, 21 lines in
   `answers.md`, 73 log lines, and a rebuilt `HW1.pdf`.
7. **Subsequent work.** The next pre-work commit `8394e97` records 9 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`. Entry 8 identifies these as a rewritten opening
   sentence, a new paragraph interpreting the Q2(c) result, and an empty heading for Q2(d).
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(d) — Entry 8 (2026-09-12), commits `8394e97` → `acfe566`

1. **Purpose.** Produce expanding-window out-of-sample forecasts, the forecast plot, `R²_OS`,
   and the 50-year rolling `R²_OS` plot.
2. **Work before AI.** At `8394e97`, Questions 1 and 2(a)–2(c) were answered in `answers.md`,
   with scripts `q1b`–`q2c` and their outputs. The student's prompt specified the
   expanding-window scheme, the first forecast date, the three plotted series, and both
   `R²_OS` calculations.
3. **AI assistance.** Ran a read-only computation showing that the open choices flip the sign
   of `R²_OS`, then asked three questions. After the student decided, wrote `code/q2d.py` and
   ran it: 973 forecasts from December 1940 to December 2021, `R²_OS = 0.001825`, and 373
   rolling windows ranging from −0.0604 to 0.1583. Verified that the in-sample coefficients
   reproduce Q2(b). Viewed both figures.
4. **AI modifications.** Created `code/q2d.py` and four outputs; appended 32 lines to
   `answers.md`; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Three items were put to the student with numbers
   attached and no recommendation: the training window's end date relative to the forecast
   date, where AI pointed out that the specified window uses returns realised after the
   forecast date and overlapping the forecast target; the benchmark for SST; and the rolling
   window length. The student chose the window as originally written, SST around the
   evaluation-period mean, and 600 months.
6. **State after AI.** Commit `acfe566` adds `q2d.py` (219 lines), four outputs, 32 lines in
   `answers.md` and 69 log lines.
7. **Subsequent work.** The next pre-work commit `6406b0f` records 2 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`; Entry 9 identifies the edit as the removal of the
   `SSE/SST` step from the displayed `R²_OS` equation.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q2(e) — Entry 9 (2026-09-12), commits `6406b0f` → `ad7dd61`

1. **Purpose.** Repeat Q2(d) with the out-of-sample coefficients restricted to
   `a_t = Ḡ_t − 1` and `b_t = Ḡ_t`.
2. **Work before AI.** At `6406b0f`, Q2(d) was complete with `q2d.py` and its outputs, and
   `answers.md` carried the Q2(d) figures and `R²_OS`.
3. **AI assistance.** Computed both readings of the `Ḡ_t` window read-only and reported that
   they give `R²_OS` of −0.0039 and 0.0020. After the student chose, wrote `code/q2e.py`,
   which reuses the Q2(d) forecast frame so the sample, historical mean and in-sample
   forecast are identical by construction, and ran it: `R²_OS = 0.001978` over the same 973
   forecasts, with `Ḡ_t` rising from 1.000023 to 1.028394. Viewed both figures.
4. **AI modifications.** Created `code/q2e.py` and five outputs; appended 34 lines to
   `answers.md`, including a `###` heading; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. The one open point, which months of `Δd` enter
   `Ḡ_t`, was put to the student with both options' values; the student chose the regressor
   months of each pair. AI also matched the equation formatting to the student's own edit of
   the Q2(d) equation.
6. **State after AI.** Commit `ad7dd61` adds `q2e.py` (184 lines), five outputs, 34 lines in
   `answers.md` and 73 log lines.
7. **Subsequent work.** The next pre-work commit `3eae001` records changes to
   `Bond Dataset.csv` (85 lines removed, 1 added), 13 added lines in `answers.md`, and a
   rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; formatting or translation.

---

## Question 3

### Q3(a) — Entry 16 (2026-09-27), commits `6d712a9` → `3b52481`

1. **Purpose.** Construct the momentum signal from CRSP and validate it against the
   Chen–Zimmermann `Mom12m` through monthly cross-firm regressions.
2. **Work before AI.** The pre-work commit `6d712a9` adds `Pset 1/Data.ipynb` (293 lines),
   the student's own notebook, which the entry records as containing a successful
   `openap.dl_signal(...)` call returning 4,245,647 rows. The student had downloaded CRSP to
   `CRSP.csv`, which is not tracked. No Q3 code existed.
3. **AI assistance.** Ran read-only diagnostics establishing that the extract already
   satisfied three of the required screens and measuring the utility, financial, unparseable
   `SICCD` and missing-return counts. Flagged four decisions and resolved none. Wrote
   `code/q3a_filter_crsp.py`, which destructively applied the SIC exclusions at the student's
   instruction (3,435,060 → 2,734,812 rows), and `code/q3a.py` building both momentum
   variants. The interaction ended incomplete: the Chen–Zimmermann download failed with a
   Google Drive quota error across three retries and all five releases.
4. **AI modifications.** Overwrote `Pset 1/CRSP.csv` in place (destructive, at the student's
   instruction); created `code/q3a_filter_crsp.py` and `code/q3a.py`; added two `.gitignore`
   rules; `AI_INTERACTIONS.md`. No figures, no outputs and no change to `answers.md`.
5. **Substantive decisions.** None by AI. Four choices were put to the student: destructive
   deletion of the raw download, the missing-return rule inside the compounding window, the
   treatment of unparseable `SICCD`, and the momentum window. AI noted that the student's
   revised window skipping month τ−1 departs from the problem statement's definition and
   would depress the validation slope by construction; the student chose to compute both.
6. **State after AI.** Commit `3b52481` adds `q3a.py` (200 lines), `q3a_filter_crsp.py` (64
   lines), seven `.gitignore` lines and 25 log lines. No outputs, consistent with the
   interaction stopping early.
7. **Subsequent work.** Commit `6c77976` adds `code/q3a_build_cz_cache.py` (68 lines). No
   interaction in `AI_INTERACTIONS.md` covers that commit, so its authorship is not shown in
   the available record; Entry 17 later refers to editing this file. The next pre-work commit
   `1133ea4` records six `.gitignore` lines and a large reduction of `Data.ipynb`.
8. **Type of AI use.** Empirical coding; code debugging.

### Q3(a) — Entry 17 (2026-09-27), commits `1133ea4` → `dc20330`

1. **Purpose.** Finish Q3(a) using Chen–Zimmermann files the student had downloaded by hand.
2. **Work before AI.** At `1133ea4` the two Q3(a) scripts existed but no outputs, and
   `answers.md` had no 3(a) section. The student had placed `Mom12m.csv`, `BMdec.csv` and
   `GP.csv` in `Pset 1/`.
3. **AI assistance.** Verified the three downloads were real CSVs, added them to `.gitignore`
   before staging because one exceeds GitHub's file-size limit, edited the cache builder to
   find them, and confirmed the assembled cache reproduces the row count from the student's
   own notebook exactly. Ran `q3a.py` end to end: 727 monthly regressions over 1964-06 to
   2024-12. The 12-return variant gave slope mean 0.8939 and `R²` mean 0.8917; the 11-return
   variant gave 0.8984 and 0.7885.
4. **AI modifications.** Three `.gitignore` rules; edited `code/q3a_build_cz_cache.py`;
   generated the CZ cache, `output/q3a_monthly_regressions.csv` and three PNGs; added a
   `### 3(a)` subsection to `answers.md` with the regression equation, one descriptive
   sentence, the three figures and a `% TODO` marker for the student's discussion;
   `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. AI reported as a diagnostic that even the 12-return
   variant gives a slope and `R²` near 0.89 rather than 1, and identified the student's
   missing-return rule as the probable cause, leaving the decision to the student. AI wrote
   no interpretation of the results.
6. **State after AI.** Commit `dc20330` adds 32 lines to `answers.md`, three figures, the
   728-row regression CSV, edits to the cache builder and 24 log lines.
7. **Subsequent work.** The next pre-work commit `6e2092d` records only a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; code debugging.

### Q3(a) — Entry 18 (2026-09-27), commits `6e2092d` → `31401ba`

1. **Purpose.** Keep only the 12-return momentum definition and drop the 11-return variant.
2. **Work before AI.** At `6e2092d`, Q3(a) was complete with both variants in the code, the
   outputs and the answer section.
3. **AI assistance.** Rewrote `q3a.py` for a single definition, removing the two-variant
   scaffolding, re-ran it, and verified the refactor was numerically inert: the same
   2,460,933 valid firm-months, 727 regressions and identical summary statistics as the
   no-skip column of Entry 17. Updated one sentence in the 3(a) subsection.
4. **AI modifications.** `code/q3a.py` (rewritten); one sentence in `answers.md`; regenerated
   the regression CSV and three PNGs; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Choosing the 12-month window was the student's
   instruction; AI removed the other code path. The Entry 17 diagnostic about the
   missing-return rule was restated as still open.
6. **State after AI.** Commit `31401ba` records `q3a.py` with 121 changed lines, 7 changed
   lines in `answers.md`, regenerated outputs and 19 log lines.
7. **Subsequent work.** The next pre-work commit `9f28ea1` records four `.gitignore` lines
   and a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding.

### Q3(b) — Entry 19 (2026-09-27), commits `9f28ea1` → `0e55fe8`

1. **Purpose.** Add CRSP `PRC` and `SHROUT` to `CRSP.csv` so market equity can be built.
2. **Work before AI.** At `9f28ea1`, Q3(a) was complete. The student had placed a second
   WRDS extract in `Pset 1/`.
3. **AI assistance.** Inspected the source file, ran a read-only pre-merge check confirming
   unique keys on both sides and a left join that adds no rows and drops none, gitignored the
   source before staging, then wrote and ran `code/crsp_add_prc_shrout.py`. Verified the
   merge was non-destructive by re-running `q3a.py` and reproducing its results exactly.
4. **AI modifications.** `Pset 1/CRSP.csv` (destructive: two columns appended in place);
   created `code/crsp_add_prc_shrout.py`; one `.gitignore` rule; regenerated the Q3(a)
   outputs during verification; `AI_INTERACTIONS.md`. `answers.md` untouched.
5. **Substantive decisions.** None by AI. No filtering, transformation or imputation was
   applied to the incoming columns. AI noted that `PRC` retains CRSP's sign convention and
   that missing and zero values are preserved, leaving the `ME` construction decisions to the
   student.
6. **State after AI.** Commit `0e55fe8` adds `crsp_add_prc_shrout.py` (78 lines) and 20 log
   lines. `CRSP.csv` is untracked, so its modification does not appear in the diff.
7. **Subsequent work.** The next pre-work commit `07e2d8b` records three `.gitignore` lines.
   Entry 20 explains that this commit was recreated during that interaction to remove a
   licensed Compustat file.
8. **Type of AI use.** Empirical coding.

### Q3(b) — Entry 20 (2026-09-27), commits `07e2d8b` → `bcf39a1`

1. **Purpose.** Build the book-to-market signal and validate it against `BMdec`.
2. **Work before AI.** At `07e2d8b`, Q3(a) was complete and `CRSP.csv` carried `PRC` and
   `SHROUT`. The student's prompt was "do 3b" with no specification, so the construction came
   from the problem statement's footnotes 5 and 6.
3. **AI assistance.** Checked the Compustat extract against footnote 6 and put four decisions
   to the student. Wrote `code/q3b.py` implementing the book-equity, market-equity and
   book-to-market construction with the June-to-May assignment and the exclusions, then ran
   it: 727 monthly regressions over 1964-06 to 2024-12, slope mean 0.9445 and `R²` mean
   0.9128. Diagnosed an overflow warning as evidence that `BMdec` in this vintage is already
   a ratio rather than a log, fitted both readings, and reported the contrast.
4. **AI modifications.** Created `code/q3b.py`; one `.gitignore` rule; added a `### 3(b)`
   subsection to `answers.md` with the construction, the regression equation, a note on the
   `BMdec` scale, three figures and a `% TODO` marker; generated the regression CSV and three
   PNGs; `AI_INTERACTIONS.md`. Git history was rewritten once, at the student's instruction,
   to remove a licensed Compustat file from the pre-work commit.
5. **Substantive decisions.** None by AI. Four choices went to the student: proceeding
   without `SEQ`, how to operationalise the two-prior-years screen, removing the licensed file
   from history, and the `BMdec` definition. On the last, AI supplied evidence and fitted both
   candidates but did not choose. Several working assumptions the problem statement does not
   pin down were stated to the student and recorded in the module docstring. A units
   alignment between `SHROUT` and Compustat was applied as arithmetic, not as a design choice.
6. **State after AI.** Commit `bcf39a1` adds `q3b.py` (233 lines), four outputs, 43 lines in
   `answers.md` and 23 log lines.
7. **Subsequent work.** The next pre-work commit `5043456` records 4 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; code debugging.

### Q3(c) — Entry 21 (2026-09-27), commits `5043456` → `ab7f3b7`

1. **Purpose.** Build fifteen sets of decile portfolios under five schemes, with five
   scatterplots and a table of HML averages and t-statistics.
2. **Work before AI.** At `5043456`, Q3(a) and Q3(b) were complete with their code, outputs
   and answer sections. The prompt was "do question 3c" with no specification of its own.
3. **AI assistance.** Reused the Newey–West convention already present in `q2b.py` so the
   t-statistics are comparable across items, put four decisions to the student, downloaded
   and cached the risk-free series named in footnote 8, and wrote `code/q3c.py`. Fixed a
   December month-index error found before running. Ran it: 2,523,847 firm-months, all
   fifteen HML series spanning 738 months, with the full set of averages and t-statistics
   recorded in the entry.
4. **AI modifications.** Created `code/q3c.py`; added a `### 3(c)` subsection to `answers.md`
   with the construction, five figures, the fifteen-row HML table and a `% TODO` marker;
   generated two CSVs, five PNGs and a cached risk-free file; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Four choices went to the student: the annual
   rebalancing window, the market equity used for value weights, the treatment of unusable
   returns during a holding month, and the sample start. Two implementation defects were
   fixed by AI as computational matters: the month-index conversion, and a LaTeX command AI
   had itself reintroduced that had previously broken the student's build.
6. **State after AI.** Commit `ab7f3b7` adds `q3c.py` (270 lines), two CSVs, five PNGs, 74
   lines in `answers.md` and 27 log lines.
7. **Subsequent work.** The next pre-work commit `1e9bea7` is empty.
8. **Type of AI use.** Empirical coding; code debugging; formatting or translation.

### Q3(b) — Entry 22 (2026-09-27), commits `1e9bea7` → `a5760cb`

1. **Purpose.** Rebuild book equity now that the Compustat extract carries `SEQ`, and check
   whether Q3(c) is affected.
2. **Work before AI.** At `1e9bea7`, Q3(a)–Q3(c) were complete. The student had replaced
   `COMPUSTATS.csv` with an extract including `seq`.
3. **AI assistance.** Established that Q3(c) has no Compustat dependency and reported this
   rather than presenting a re-run as a change, then re-ran `q3c.py` anyway and confirmed via
   `git status` that no output file changed. Updated the `SE` definition in `q3b.py` to
   footnote 6's sequence and re-ran: book equity now comes from `SEQ` for 262,826 firm-years
   and from the fallback for 701 more, and the regression statistics are identical to four
   decimal places.
4. **AI modifications.** `code/q3b.py` (definition, reporting, docstring); one passage in the
   3(b) subsection of `answers.md`; regenerated the Q3(b) outputs; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Footnote 6 fixes the order in which the book-equity
   routes are tried, so implementing `SEQ` first follows the problem statement. All decisions
   recorded in Entry 20 carry over unchanged. A standing limitation, that two columns are
   still absent so some firm-years have no book equity, was restated.
6. **State after AI.** Commit `a5760cb` records 21 changed lines in `q3b.py`, 8 changed lines
   in `answers.md`, regenerated Q3(b) outputs and 21 log lines. The Q3(c) outputs carry no
   diff, confirming they are unchanged.
7. **Subsequent work.** Commit `94a0150`, titled "works on 9/27", adds Problem Set 2
   materials and a rebuilt `HW1.pdf`. The next pre-work commit `24661d8` is empty.
8. **Type of AI use.** Empirical coding.

### Q3(d) — Entry 23 (2026-09-28), commits `24661d8` → `15290e8`

1. **Purpose.** Estimate and tabulate the seven Fama–MacBeth specifications, by OLS and by
   market-equity WLS.
2. **Work before AI.** At `24661d8`, Q3(a)–Q3(c) were complete. The duration dataset was not
   in the repository. The student's prompt quoted the question and specified the two-stage
   procedure and the Newey–West t-statistics.
3. **AI assistance.** Located and downloaded the duration data from the author's site, read
   the accompanying notes to establish its availability timing, and put three decisions to
   the student. When the student then asked to take duration from the Chen–Zimmermann
   dataset, AI flagged that the nearest CZ signal is a different measure, listed the CZ signal
   names as evidence, and waited for confirmation rather than proceeding. Wrote
   `code/q3d.py`, compared the student's own copy of the duration file against the downloaded
   one and confirmed identical contents, and ran it: 617 monthly cross-sections over 1973-07
   to 2024-11 covering 1,406,156 firm-months, with all fourteen slope estimates and
   t-statistics recorded in the entry.
4. **AI modifications.** Created `code/q3d.py`; generated two output CSVs and a cached copy
   of the duration file; added a `### 3(d)` subsection to `answers.md` with the construction,
   the fourteen-row table and a `% TODO` marker; `AI_INTERACTIONS.md`. A package was added to
   the virtual environment to open the archive.
5. **Substantive decisions.** None by AI. Three choices went to the student: the quantile
   definition, the common-sample restriction, and the data vintage. Identifying the CZ
   duration signal as a different variable was a factual check against the problem statement,
   and the student made the call.
6. **State after AI.** Commit `15290e8` adds `q3d.py` (239 lines), the duration CSV, two
   output CSVs, 35 lines in `answers.md` and 23 log lines.
7. **Subsequent work.** The next pre-work commit `75e32f2` records one `.gitignore` line and
   a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; code debugging.

### Q3(e) — Entry 24 (2026-09-28), commits `75e32f2` → `1c530fb`

1. **Purpose.** Estimate the seven portfolio-panel specifications with Driscoll–Kraay
   standard errors, for value-weighted and equal-weighted portfolios.
2. **Work before AI.** At `75e32f2`, Q3(a)–Q3(d) were complete with their code, outputs and
   answer sections. The student's prompt quoted the question in full.
3. **AI assistance.** Confirmed the required covariance estimator is available in
   `linearmodels`, put three decisions to the student, and stated three further readings of
   the problem text explicitly so they could be overridden. Wrote `code/q3e.py` and ran it:
   618 months from July 1973 to December 2024, 18,540 portfolio-months per weighting, with
   all fourteen slope estimates and t-statistics recorded in the entry. Ran a consistency
   check implied by footnote 10 against the Q3(c) HML averages.
4. **AI modifications.** Created `code/q3e.py`; generated two output CSVs; added a `### 3(e)`
   subsection to `answers.md` with the construction, the fourteen-row table, the consistency
   check and a `% TODO` marker; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Three choices went to the student: how the average
   decile is weighted, when it is measured, and the common-sample restriction. The
   standard-error method is specified by the problem, and its bandwidth is the package
   default, which AI stated rather than tuned. AI also flagged, without acting, that the
   duration file had been added to `.gitignore` after it was already tracked.
6. **State after AI.** Commit `1c530fb` adds `q3e.py` (234 lines), two output CSVs, 43 lines
   in `answers.md` and 23 log lines.
7. **Subsequent work.** The next pre-work commit `bcb4da2` records only a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding.

### Q3(e) — Entry 25 (2026-09-28), commits `bcb4da2` → `5557d3e`

1. **Purpose.** Split the single results table into one table per weighting scheme.
2. **Work before AI.** At `bcb4da2`, the 3(e) subsection held one fourteen-row table.
3. **AI assistance.** Split the table into two seven-row tables and dropped the redundant
   column. An initial caption syntax was replaced with bold labels because that syntax is not
   part of MyST and the build had already broken once on an unsupported construct. No number,
   t-statistic or surrounding sentence changed.
4. **AI modifications.** `Pset 1/answers.md`, the 3(e) table only.
5. **Substantive decisions.** None. Presentation only; all estimates unchanged. AI noted that
   the 3(d) table could be split on the same principle but made no such change.
6. **State after AI.** Commit `5557d3e` records 39 insertions and 16 deletions in
   `answers.md` and 15 log lines.
7. **Subsequent work.** The next pre-work commit `c0f7ff4` records only a rebuilt `HW1.pdf`.
8. **Type of AI use.** Formatting or translation.

### Q3(e) — Entry 26 (2026-09-28), commits `c0f7ff4` → `fb5645e`

1. **Purpose.** Explain a block of Typst build warnings and determine whether the PDF is
   wrong.
2. **Work before AI.** At `c0f7ff4`, Question 3 was complete in `answers.md` and `HW1.pdf`
   had been rebuilt. The student pasted the warnings and wrote "debug".
3. **AI assistance.** Established the messages are warnings rather than errors, traced them
   to the table package used by the PDF template when a table straddles a page boundary, and
   extracted the rendered text to confirm that no rows are lost and the repeated header is
   correct. Identified the cause as the table split made in Entry 25 and recommended
   deferring the fix until the remaining prose is written, since added text reflows the pages.
4. **AI modifications.** `AI_INTERACTIONS.md` only. `answers.md`, the code and the outputs
   were untouched. A package was added to the virtual environment to read the PDF.
5. **Substantive decisions.** None. No number, specification or text changed.
6. **State after AI.** Commit `fb5645e` adds 20 log lines and nothing else.
7. **Subsequent work.** The working tree after `fb5645e` carried a rebuilt `HW1.pdf` and 13
   changed lines in `answers.md`, captured in commit `833204b`; the diff shows the abstract
   placeholder removed, spacing around the Typst block, and a comma added in the 3(a) text.
8. **Type of AI use.** Other (build diagnosis); formatting or translation in advisory form.

---

## Question 4

### Q4(a) — Entry 10 (2026-09-12), commits `3eae001` → `81064d9`

1. **Purpose.** Build log yields, log forward rates and log annual returns from the bond
   data, and report the average excess measures for `H = 2…5`.
2. **Work before AI.** At `3eae001`, Questions 1 and 2 were complete. The same commit records
   85 lines removed from `Bond Dataset.csv`; AI's inspection during the interaction found
   these were empty placeholder rows for other CRSP series, with the five Fama–Bliss series
   unchanged. No Q4 code existed.
3. **AI assistance.** Read the Q4 text, ran read-only diagnostics on the bond file (five
   series, 871 months, no duplicates, gaps or missing yields), compared the student's
   formulas against the problem statement, and computed the averages under each open choice
   before asking. After the student decided, wrote `code/q4a.py` and ran it, reporting the
   table of average `xy`, `xf` and `xr` and producing three figures. Viewed all three.
4. **AI modifications.** Created `code/q4a.py`, three CSVs of series, an excess-series CSV,
   an averages CSV, a summary CSV and three PNGs; added 17 lines to `answers.md` including a
   `###` heading, the table and the definitions; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Two choices went to the student: which one-year
   term `xr` subtracts, where AI showed that the problem statement's `r^(1)_t` is the yield a
   year earlier while the prompt's `y^(1)_t` is a year later; and the averaging sample. AI
   also checked that the prompt's `xf` benchmark coincides with the problem statement's and
   told the student, without asking. The plots were saved but not placed in `answers.md`,
   since the problem asks only for a table.
6. **State after AI.** Commit `81064d9` adds `q4a.py` (194 lines), nine output files, 17
   lines in `answers.md` and 100 log lines.
7. **Subsequent work.** The next pre-work commit `4dc4cf4` records only a rebuilt `HW1.pdf`.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q4(a) — Entry 11 (2026-09-12), commits `4dc4cf4` → `b5603a9`

1. **Purpose.** Add the three Q4(a) figures to `answers.md`.
2. **Work before AI.** At `4dc4cf4`, the Q4(a) table and definitions were in `answers.md` and
   the three PNGs existed in `output/`.
3. **AI assistance.** Confirmed the file was unchanged since the previous commit, then
   appended three figure directives with labels, 90% width and factual captions giving the
   series, maturities, date ranges and scaling. The entry records that the student did not
   type the tracking command for this request and that AI applied the workflow itself,
   telling the student so.
4. **AI modifications.** `Pset 1/answers.md` (21 lines added); `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None. Figure placement, labels, width and caption wording were
   the only choices, all presentational. The PNGs were not regenerated.
6. **State after AI.** Commit `b5603a9` adds 21 lines to `answers.md` and 27 log lines.
7. **Subsequent work.** The next pre-work commit `cf2f2be` records 6 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`; Entry 12 identifies the edit as changing the three
   figure widths from 90% to 60%.
8. **Type of AI use.** Formatting or translation.

### Q4(b) — Entry 12 (2026-09-12), commits `cf2f2be` → `1d1155e`

1. **Purpose.** Regress the average annual hold-to-maturity excess return on the excess log
   yield for `H = 2…5`, with Hansen–Hodrick t-statistics.
2. **Work before AI.** At `cf2f2be`, Q4(a) was complete with its script, outputs and figures.
   The student's prompt gave the hold-to-maturity sum, the regression and the standard-error
   method.
3. **AI assistance.** Built the hold-to-maturity returns from the Q4(a) series, checked them
   against the same quantity computed directly from log yields, and estimated the regressions
   under both open choices before asking. After the student decided, wrote `code/q4b.py` and
   ran it. AI then found an error in its own code: the zero one-year term at the end of the
   sum had been treated as requiring data, which dropped the last year of each sample. AI
   identified this while preparing Q4(c), using the problem statement's footnote 13 as the
   test, fixed it, re-ran, and confirmed footnote 13 holds exactly. Final estimates: slopes
   0.6774, 0.5316, 0.4141 and 0.3453 with t-statistics 3.57, 3.21, 2.52 and 2.30.
4. **AI modifications.** Created `code/q4b.py` and regenerated its two outputs after the fix;
   appended 18 lines to `answers.md`, then corrected the four table numbers inside the
   three-column layout the student had meanwhile adopted; `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Two choices went to the student: the Hansen–Hodrick
   lag length and the sample. The entry records that the numbers shown when the student
   decided were affected by the coding error, gives the corrected alternatives, and states
   that the error was purely computational because the student's own formula fixes the sample.
6. **State after AI.** Commit `1d1155e` adds `q4b.py` (138 lines), two outputs, 18 lines in
   `answers.md` and 85 log lines.
7. **Subsequent work.** The next pre-work commit `1ef4b37` is empty, so nothing changed
   between the two interactions.
8. **Type of AI use.** Empirical coding; code debugging of AI's own error; formatting or
   translation.

### Q4(c) — Entry 13 (2026-09-13), commits `1ef4b37` → `36dbf0d`

1. **Purpose.** Regress the one-year excess return on the excess forward rate for `H = 2…5`,
   with Newey–West t-statistics.
2. **Work before AI.** At `1ef4b37`, Q4(a) and the corrected Q4(b) were complete.
3. **AI assistance.** Estimated the regressions under both readings of "Newey–West" read-only
   and reported both, noting that the problem statement names the 1987/1994 method. Confirmed
   every horizon uses the same 859 months, so no sample question arose, and verified footnote
   13 holds. After the student chose, wrote `code/q4c.py` and ran it: slopes 0.6774, 0.8887,
   1.1163 and 0.9641 with t-statistics 3.23, 3.35, 3.62 and 2.91.
4. **AI modifications.** Created `code/q4c.py` and one output CSV; appended 18 lines to
   `answers.md` including a `###` heading, the equation, one sentence and a three-column
   table matching the layout the student had chosen for Q4(b); `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. The one choice, which Newey–West variant, went to
   the student. The bandwidth convention was carried over from Q2(b), where it had been
   flagged.
6. **State after AI.** Commit `36dbf0d` adds `q4c.py` (102 lines), one output, 18 lines in
   `answers.md`, 78 log lines and a rebuilt `HW1.pdf`.
7. **Subsequent work.** The next pre-work commit `8523435` adds `Pset 1/USREC.csv`, the NBER
   recession series the student downloaded for Q4(d).
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q4(d) — Entry 14 (2026-09-13), commits `8523435` → `d106555`

1. **Purpose.** Estimate the Cochrane–Piazzesi regression and plot the factor with NBER
   recessions shaded.
2. **Work before AI.** At `8523435`, Q4(a)–Q4(c) were complete and the student had added
   `USREC.csv`, which AI inspected before including it in the snapshot.
3. **AI assistance.** Ran the regression read-only and reported the coefficients, `R²` of
   0.1575 on 859 months, the two candidate plotted series and the recession coverage, then
   asked two questions. After the student decided, wrote `code/q4d.py` and ran it: the plot
   covers 871 months with 113 recession months in 11 shaded spans. Viewed the figure.
4. **AI modifications.** Created `code/q4d.py`, three output CSVs and the figure; appended 18
   lines to `answers.md` including a `###` heading, the regression and the figure;
   `AI_INTERACTIONS.md`.
5. **Substantive decisions.** None by AI. Two choices went to the student: whether to plot
   the factor as the problem statement defines it or the fitted value including the
   intercept, and the plot range. AI wrote the regression without the problem statement's
   underbrace notation because it could not verify that it survives the PDF export.
6. **State after AI.** Commit `d106555` adds `q4d.py` (183 lines), four outputs, 18 lines in
   `answers.md`, 74 log lines and a rebuilt `HW1.pdf`. Entry 15 records a correction: the
   rebuilt PDF in this commit was produced outside AI's actions, which Entry 14 did not say.
7. **Subsequent work.** The next pre-work commit `70286d4` records 5 changed lines in
   `answers.md` and a rebuilt `HW1.pdf`; Entry 15 identifies these as a Typst page-margin
   block and a figure width change.
8. **Type of AI use.** Empirical coding; formatting or translation.

### Q4(e) — Entry 15 (2026-09-13), commits `70286d4` → `758fc41`

1. **Purpose.** Regress one-year excess returns on the Cochrane–Piazzesi factor for
   `H = 2…5`, with Newey–West (1987, 1994) t-statistics.
2. **Work before AI.** At `70286d4`, Q4(a)–Q4(d) were complete, including the factor series
   saved by Q4(d).
3. **AI assistance.** Checked the saved factor against a recomputation from the saved
   coefficients, confirmed every horizon uses the same 859 months, and estimated both
   candidate regressors read-only. After the student chose, wrote `code/q4e.py`, which stops
   if the saved factor does not match the Q4(d) coefficients, and ran it: slopes 0.4418,
   0.8274, 1.2517 and 1.4791 with t-statistics 4.16, 4.18, 4.45 and 4.25.
4. **AI modifications.** Created `code/q4e.py` and one output CSV; appended 18 lines to
   `answers.md` including a `###` heading, the equation, one sentence and a three-column
   table; `AI_INTERACTIONS.md`, including the correction to Entry 14.
5. **Substantive decisions.** None by AI. The one choice, which version of the factor to use,
   went to the student; AI reported that the two differ by a constant, which leaves the
   slopes unchanged but shifts the intercepts and alters the automatically chosen lag at two
   horizons.
6. **State after AI.** Commit `758fc41` adds `q4e.py` (111 lines), one output, 18 lines in
   `answers.md` and 86 log lines.
7. **Subsequent work.** Commits `3ce7f06`, `a5adadc`, `35dc364` and `b09906c` follow, adding
   a rebuilt PDF, Problem Set 2 materials, a research note, a `requirements.txt` and editor
   settings. Work then moved to Question 3.
8. **Type of AI use.** Empirical coding; formatting or translation; a correction to the
   interaction record.

---

## Notes on the record itself

- **Pairing.** Each of the 26 interactions cites a pre-work commit in `AI_INTERACTIONS.md`,
  and each has a matching post-work commit whose message begins `TP: after`. Four pre-work
  commits (`001cee0`, `1ef4b37`, `1e9bea7`, `24661d8`) are empty, recording that the working
  tree was unchanged at that point.
- **One commit outside the record.** `6c77976`, which adds `code/q3a_build_cz_cache.py`, falls
  between the Entry 16 and Entry 17 commits and is not covered by any entry. Its authorship
  is not shown in the available record.
- **Corrections inside the record.** Entry 15 corrects an omission in Entry 14. Entry 12
  records an error in AI's own code together with its correction, and reports that the
  student's earlier decisions were taken while looking at the affected numbers. Entry 5
  records that the student's decision supersedes wording in their own prompt. No entry was
  edited or removed; the file grows only by appending.
- **Data files.** Several inputs are excluded from Git by `.gitignore`, including the CRSP
  and Compustat extracts and the Chen–Zimmermann downloads, which the entries describe as
  licensed or too large for the hosting limit. Entry 20 records one history rewrite, at the
  student's instruction, to remove a licensed Compustat file from a commit. Two interactions
  modified `CRSP.csv` in place, both recorded as destructive and both at the student's
  instruction.
- **This file.** `AI_USAGE.md` was generated by AI from the sources named at the top, using
  the prompt in `AI_POLICY.md` §2(e). `AI_INTERACTIONS.md` was not modified while producing
  it, and no other existing project file was changed. Commits before and after its creation
  record the repository state around this step.
