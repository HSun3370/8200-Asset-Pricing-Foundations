# AI Interactions Log — BUSFIN 8200 Problem Set 2

This file is the contemporaneous, auditable record of **substantive** AI interactions for
**Problem Set 2**, as required by `AI_POLICY.md` §2(c). (`AI_POLICY.md`, `CLAUDE.md`, and the
`@TP` skill stay at the repo root; the AI records live in each problem set's own folder.
This log is independent of `Pset 1/AI_INTERACTIONS.md`.)

**Rules (`AI_POLICY.md` §2(d)):**

- Entries are **append-only**. Never delete, rewrite, combine, reorder, or selectively omit
  an entry.
- If an entry contains an error, leave it in place and add a correction in a later entry.
- Each substantive AI interaction is added here by the `@TP` skill (`/tp`), which also
  creates the Git commits before and after the interaction.
- Administrative requests (file navigation, explaining a command, environment setup not
  affecting substance) are not logged here.

---

## Entry template (reference only — not an entry)

```
### Entry N — <YYYY-MM-DD> — Pset <k>, Q<item>

- **Problem-set item:** 
- **Student's substantive prompt:** 
- **Purpose:** 
- **Git commit before interaction:** 
- **Assistance provided:** 
- **Files inspected:** 
- **Files directly modified by AI:** 
- **Errors / omissions / ambiguities identified:** 
- **Substantive math / economic / econometric suggestions made:** 
- **Type(s) of assistance:** math review | economic-reasoning review | empirical coding | code debugging | formatting/translation | other
- **Grouped minor follow-ups:** 
- **Git commit after interaction:** 
```

---

## Interactions

### Entry 1 — 2026-10-02 — Pset 2, Q1(a)/Q1(b)

- **Problem-set item:** Pset 2, Question 1(a) and 1(b): the row-reduction (elimination) matrix in `Pset 2/answers.md` that the student uses to conclude markets are complete (1a) and to obtain the contingent-claim prices (1b).
- **Student's substantive prompt:** "/tp i started to work on homework 2, which should have a seperate AI recording independetn with HW1. Now i want you to make the matrix in math, work on markdown gramma that make the matrix generated in pdf looks like math matrix"
- **Purpose:** (1) Start a separate AI-interaction record for Pset 2, independent of Pset 1; (2) convert the student's plain-text matrix into LaTeX matrix syntax so the MyST/Typst PDF export shows a typeset bracketed matrix.
- **Git commit before interaction:** `1b4ab91ff74d1853912a46e40b822032074b2eca`. Made with `git add -A`, so it also recorded unrelated working-tree changes present at the time: the move of the Pset 2 source files out of `Pset 2/RE__BUSFIN_8200_-_Fall_2026/` into `Pset 2/`, the move of `HW1.pdf` into `Pset 1/`, the new `Pset 2/answers.md`, and the student's edits to `Research Ideas/NREE.md`, `myst.yml` and the new `MREE.pdf`.
- **Assistance provided:**
  - *Formatting/translation (applied directly to `Pset 2/answers.md`):* replaced the display block
    ```
    [X,P] ->
    [[1,0,0, 0.2],
    [0,1,0,0.4],
    [0,0,1,0.2]]
    ```
    with
    ```
    [X, P] \;\rightarrow\;
    \begin{bmatrix}
    1 & 0 & 0 & 0.2 \\
    0 & 1 & 0 & 0.4 \\
    0 & 0 & 1 & 0.2
    \end{bmatrix}
    ```
    The entries, their order, the left-hand side `[X, P]`, and the arrow meaning are unchanged. `->` was replaced by `\rightarrow` because `->` inside LaTeX math typesets as a minus sign followed by `>`. `bmatrix` was chosen because MyST converts it to a Typst `mat(delim: "[", ...)`. No augmented-matrix divider bar was added, since the student's original had none.
  - *Render check:* built a PDF from a copy of `Pset 2/answers.md` in a temporary scratch folder outside the repo, with its own minimal `myst.yml` (`jupyter-book build --pdf`, template `lapreprint-typst`). The matrix rendered as a 3×4 bracketed matrix (equation (1)). The repo's `myst.yml`, which currently exports `Research Ideas/NREE.md`, was not changed.
  - Created this file, `Pset 2/AI_INTERACTIONS.md`, using the same header and entry template as `Pset 1/AI_INTERACTIONS.md`.
- **Files inspected:** `Pset 2/answers.md`; `Pset 2/Problem Set 2.pdf` (text of Question 1 extracted to identify the sub-items); `Pset 1/AI_INTERACTIONS.md` (header/template format); `myst.yml`; `.gitignore`.
- **Files directly modified by AI:** `Pset 2/answers.md` (the one display-math block above; formatting only); `Pset 2/AI_INTERACTIONS.md` (created, with this entry).
- **Errors / omissions / ambiguities identified:**
  1. Noticed in passing (no math check was requested, and nothing was changed): in the 1(e) display equation, the sum is written `\sum_i \pi(i) p(i) X(i)`, where `p(i)` is the symbol the answer uses for contingent-claim prices in 1(b)/1(d). The numbers in the same line use `0.8`, which is the SDF value `M(i)` from 1(d), not `p(i)`. The student decides whether and how to change this.
  2. The headings for 1(a)–1(e) are empty `###` lines. They render as "1.a." … "1.e." with no titles, and the 1(a) heading has no text under it because the elimination answer sits under the 1(b) heading. Not changed.
- **Substantive math / economic / econometric suggestions made:** none. The edit was LaTeX syntax only. Item 1 above points to a symbol inconsistency without proposing a correction.
- **Type(s) of assistance:** formatting/translation; other (setting up the Pset 2 record).
- **Grouped minor follow-ups:** none.
- **Git commit after interaction:** recorded in the Git log as the commit that adds this entry (message prefix `TP: after Pset 2 Q1(a)/Q1(b) - format elimination matrix`).
