# BUSFIN 8200 Problem Sets: AI Policy

*Source: BUSFIN 8200 Problem Sets — AI Policy (Prof. Lu Zhang), Fisher College of Business, Ohio State University.*

**This file governs how AI (including Claude, in this repository) may assist with problem set work. Any AI agent operating in this repo must follow this policy for all substantive requests related to a problem set.**

---

## What you need to deliver for each problem set

1. **The problem set solution in PDF format** (not handwritten).
2. **A Git repository containing all files and results.** This must include the source files used to generate the PDF (e.g., the `.tex` file) as well as all coding scripts used to produce the results (e.g., `.R` or `.py` files). The instructor must be able to reproduce both the results and the PDF from the source files in the Git repository.

---

## AI Policy — Rationale

AI is revolutionizing research production. At the same time, the researchers who benefit most from AI are those who understand the economics, mathematics, and empirical methods underlying what they ask AI to do. The goal is not to prevent use of AI, but to constrain *how* it is used on problem sets so that AI accelerates learning rather than replacing it. Students should leave the course with at least the same underlying understanding as earlier cohorts who worked through these problems without AI, while also learning to use AI productively.

If AI tools are used while solving a problem set, the process below must be followed.

---

## 1. How to use AI

For each task (i.e., each item within a question), first determine conceptually what the task requires, then follow the appropriate procedure below.

### (a) Mathematical questions

- First work through the derivation yourself, either by hand or directly in the `.tex` file (or equivalent).
- If working by hand, you may upload a picture of your derivation to AI and ask it to translate what you wrote into LaTeX.
- Once you have produced your own derivation, you may ask AI to **check** it. If AI identifies a possible error, you may ask it to **explain** why a particular step is incorrect, but **you** must determine and implement the correction yourself. **Do not** ask AI to rewrite, complete, or replace your derivation.
- If you become stuck before completing the derivation, you may show AI the work already done and ask it to **diagnose** a specific problem with your reasoning or a particular step. You may **not** ask it to continue the derivation or provide the remaining solution.
- AI serves as a **checker and diagnostic tool**, not as the source of the mathematical derivation.
- After the substantive derivation is written, you may ask AI to improve exposition, grammar, or LaTeX formatting. Document this as formatting/translation assistance — it must not be used to generate, complete, or replace the mathematical reasoning.

### (b) Economic reasoning questions

- First work through the question entirely using your own reasoning and write your answer in the `.tex` file.
- Once written, you may ask AI to **evaluate** the reasoning and identify possible errors, omissions, or inconsistencies. You may ask AI to explain its criticism, but you must decide whether you agree and make any changes yourself.
- **Do not** ask AI to generate, rewrite, or directly edit the economic reasoning in your answer. AI is a **critic** of an argument you have already developed, not the source of the argument.
- After the substantive answer is written, you may ask AI to improve exposition, grammar, or LaTeX formatting. Document this as formatting/translation assistance — it must not be used to generate, replace, or materially change the economic reasoning.

### (c) Data analysis questions

For data analysis, AI may be used extensively to implement, optimize, integrate, and debug code. **However, the empirical design must come from you, not from AI.**

Before asking AI to write code, you must create a specification file. You may either:

1. describe the architecture of the analysis in plain English in a `.txt`, `.md`, or equivalent file; or
2. write the initial code yourself in whatever programming language you choose.

The specification must be detailed enough that AI is **implementing your design**, not making economically or econometrically substantive decisions for you. Whenever relevant, specify: data sources, sample restrictions, variable definitions, timing conventions, transformations, econometric specifications, standard error procedures, and desired outputs.

**Illustrative (simplified) example specification:**

> i. Read the CRSP and COMPUSTAT data using my WRDS account.
> ii. For each firm *i* and year *t* in COMPUSTAT, subset to firms satisfying: [criteria].
> iii. For each *i*, *t*, create a `BM` variable = book equity / market equity, combining accounting info from the fiscal year ending in calendar year *t*−1 with market cap from CRSP as of December *t*−1. Define BE as: [...]. Define ME as: [...].
> iv. Align `BM` with CRSP monthly returns for stock *i* from July *t* through June *t*+1.
> v. Estimate Fama-MacBeth regressions of returns on `BM`. Apply Newey-West (1987, 1994) standard errors.
> vi. Output results as a table in a `.tex` file called `Question 1(a)`.

Once the specification exists, you may ask AI to translate it into optimized, functional code; integrate it with the rest of the project; run it; and debug implementation errors.

- AI **may** make programming choices that do not alter the substance of the design (e.g., data structures, functions, packages, loops vs. vectorized operations, code organization).
- AI **may not** silently make substantive choices missing from the specification (e.g., sample restrictions, timing conventions, treatment of missing observations, variable definitions, winsorization rules, regression specifications, standard error choices). If such a decision is required, **AI must flag the ambiguity** rather than resolve it. You must decide and update the specification before AI implements it.
- For debugging: if the problem is purely computational, AI may fix it directly. If debugging reveals that an empirical design decision is required, you must make that decision yourself and update the specification before AI implements it.

**Guiding principle: you design the empirical analysis; AI can only implement it.**

---

## 2. How to document AI usage

If AI is used, the Git repository must contain a complete, auditable record of that use.

### (a) Use a single AI project/workspace

- All AI use related to a problem set must occur within **one** project/workspace associated with that problem set, in an environment such as VS Code, Codex, Cursor, or equivalent.
- Different models/agents may be used within the designated project as long as their use remains part of the same auditable project record.
- **Not allowed:** separate temporary chatbot conversations, other AI applications, or other projects/workspaces outside the designated project (e.g., a separate ChatGPT/Claude/Gemini chat not tied to this repo's record).
- AI inline autocomplete, grammar/style tools, and ordinary IDE code completion are allowed and do **not** require a separate `AI_INTERACTIONS.md` entry.
- However, if an AI tool contributes substantive code, mathematics, economic reasoning, empirical choices, or answer text, its use **must** be captured via Git history and summarized in `AI_USAGE.md`. Any deliberate request to produce, revise, critique, debug, or explain substantive work counts as a substantive AI interaction under Section 2(c).

### (b) Keep problem set files inside the AI project

The AI project/workspace should contain the Git repository and the files used to produce the problem set solution, so the AI agent can inspect the actual work and link its actions to specific file versions.

### (c) Use `@TP` for every substantive AI interaction

- Before any substantive request to AI, first create the `@TP` skill using the prompt in **Appendix A** below.
- Invoke `@TP` at the beginning of **every** substantive AI interaction related to the problem set. Do not bypass it for substantive work.
- If `@TP` fails to create the required Git commits or `AI_INTERACTIONS.md` entry, **stop and fix the record before continuing.**
- A request is **substantive** if it asks AI to check, critique, generate, revise, explain, debug, format, translate, summarize, or otherwise assist with content related to a problem set answer, derivation, empirical design, code, interpretation, or submission.
- **Administrative** requests (navigating files, explaining a terminal command, clarifying something already said without new work, environment setup not affecting substance) do **not** require separate before/after Git snapshots.
- Closely related **minor** subsequent requests (e.g., a short sequence of minor debugging iterations or formatting adjustments) may be grouped into **one** substantive interaction if they concern the same problem set item, occur in the same work session, and are documented together via `@TP`.
- The `@TP` skill is responsible for: creating Git snapshots before and after the interaction, and appending the required entry to `AI_INTERACTIONS.md`. This creates a **contemporaneous** record rather than relying on reconstruction after the fact.

### (d) Do not alter the AI interaction record

- Do **not** delete, rewrite, combine, or selectively omit entries in `AI_INTERACTIONS.md`.
- If an entry contains an error, **leave the original entry in place** and add a correction in a subsequent entry.
- Git history must preserve both the evolution of the substantive work and the evolution of the AI interaction record.

### (e) Create the final AI usage summary

After completing the problem set, give the AI agent the following prompt (verbatim):

```
Create a file called AI_USAGE.md that provides a complete, factual summary of how AI
was used throughout this problem set.

Use AI_INTERACTIONS.md, the Git commit history, and the differences between the
relevant Git commits as your primary evidence. Do not rely on memory of previous
conversations when the repository provides a record, and do not infer the student's
reasoning, intentions, or understanding when these are not directly supported by the
available evidence.

Organize AI_USAGE.md first by problem set item and, within each item, chronologically
by AI interaction.

For each AI interaction, report:
1. Purpose: What the student asked AI to do.
2. Work before AI: What relevant derivation, economic reasoning, empirical design,
   or code already existed in the repository immediately before the AI interaction.
   Base this description on the Git snapshot before the interaction.
3. AI assistance: What substantive assistance AI provided, including errors identified,
   explanations provided, code generated or debugged, and suggestions made.
4. AI modifications: Which files, if any, AI directly changed during the interaction
   and the nature of those changes.
5. Substantive decisions: Identify any mathematical, economic, or econometric choices
   suggested or made by AI. Distinguish these from purely mechanical programming
   or formatting choices.
6. State after AI: Describe the relevant differences between the Git snapshots before
   and after the interaction.
7. Subsequent student work: When observable from the Git history, describe changes
   the student made after the AI interaction and before the next AI interaction. Do not
   attribute a change to the student unless the Git history supports that attribution.
8. Type of AI use: Classify the interaction using all applicable categories: math
   review; economic reasoning review; empirical coding; code debugging; formatting
   or translation; or other.

If the available evidence does not support any of these items, write "not shown in the
available record" rather than guessing.

At the beginning of AI_USAGE.md, also provide a short summary table listing, for each
problem set item, the number of AI interactions and the main types of AI assistance
used.

The purpose of AI_USAGE.md is to allow another AI agent or the instructor to evaluate
how the student used AI. Accordingly, be descriptive and factual. Do not evaluate
whether the student's AI use complied with the course policy; simply document what
occurred.

Do not delete or modify AI_INTERACTIONS.md or any other existing project files when
producing AI_USAGE.md.
```

- Both `AI_INTERACTIONS.md` and `AI_USAGE.md` must be included in the submitted Git repository.
- **Grading may be directly affected by compliance with this AI policy**, including the completeness, accuracy, and auditability of the AI use record.

---

## Appendix A: Prompt for Creating the `@TP` Skill

Use the following prompt inside the designated AI project/workspace to create the reusable traceable-prompt skill. After creating it, invoke `@TP` at the beginning of each substantive AI request related to the problem set.

```
Create a reusable AI skill called @TP, short for traceable prompt, for this problem set
project. The purpose of this skill is to help me comply with the BUSFIN 8200
problem set AI policy. When I invoke @TP at the beginning of a substantive AI
request, do the following.

1. First, identify the problem set item to which my request relates. If the item is not
   clear, ask me to specify it before doing the substantive work.
2. Before doing the substantive work, create a Git commit that records the current
   state of the repository. If there are no file changes to commit, create an empty
   commit so that the state before the interaction is still recorded. Record the
   commit hash for the state before the interaction.
3. Complete my substantive request, subject to the course AI policy. If the request
   asks you to make a substantive mathematical, economic, or empirical design
   decision that I have not specified, identify the ambiguity and ask me to decide
   before implementing it.
4. After completing the substantive work, append a new entry to
   AI_INTERACTIONS.md. Do not modify, delete, combine, or rewrite previous entries.
5. The new entry in AI_INTERACTIONS.md must include the problem set item; my
   substantive prompt; the purpose of the request; the Git commit before the
   interaction; a concise but complete description of the assistance you provided; the
   files you inspected; the files you directly modified, if any; any errors, omissions, or
   ambiguities you identified; any substantive mathematical, economic, or empirical
   suggestions you made; whether the interaction involved checking mathematics,
   checking economic reasoning, empirical implementation, code debugging,
   formatting/translation, or another form of assistance; and whether any minor
   subsequent debugging or formatting requests were grouped into this same
   interaction.
6. After updating AI_INTERACTIONS.md, create another Git commit recording the
   state of the repository after the interaction. If there are no file changes to commit,
   create an empty commit so that the state after the interaction is still recorded.
7. If I explicitly group closely related minor subsequent debugging or formatting
   requests into the same interaction, document them in the same
   AI_INTERACTIONS.md entry. Only group subsequent requests when they concern
   the same problem set item, occur in the same work session, and are documented
   together.

The skill should help create an auditable record. It should not weaken or replace any
requirement in the course AI policy.
```

---

## Quick-reference checklist for any AI agent working in this repo

- [ ] Before substantive work: is `@TP` invoked? Item identified? Pre-work Git commit made?
- [ ] Math: only check/diagnose, never derive or complete for the student.
- [ ] Economic reasoning: only critique, never generate or rewrite the argument.
- [ ] Data analysis: is there a specification (`.txt`/`.md`/initial code) before code generation? Flag any unspecified substantive empirical decision instead of resolving it.
- [ ] After substantive work: `AI_INTERACTIONS.md` entry appended (never edited/deleted), post-work Git commit made.
- [ ] At the end: `AI_USAGE.md` generated per the Appendix prompt, without modifying `AI_INTERACTIONS.md`.
