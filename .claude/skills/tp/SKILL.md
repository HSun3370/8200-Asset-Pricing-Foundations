---
name: tp
description: >-
  Traceable Prompt (@TP). Run at the START of EVERY substantive AI request for BUSFIN 8200
  problem-set work (math checking, economic-reasoning critique, empirical coding/debugging,
  formatting). Identifies the problem-set item, makes a Git commit before the work, enforces
  the course AI policy during the work, appends an entry to AI_INTERACTIONS.md, and makes a
  Git commit after. Invoke as /tp. Do not use for purely administrative requests.
---

# @TP — Traceable Prompt

Created to comply with the **BUSFIN 8200 Problem Sets: AI Policy** (`AI_POLICY.md`, §2).
Invoke at the beginning of **every substantive** AI interaction related to a problem set.
Do not bypass it for substantive work. This skill creates a contemporaneous, auditable
record. **It does not weaken or replace any requirement in `AI_POLICY.md`** — if anything
here appears to conflict with `AI_POLICY.md`, `AI_POLICY.md` governs.

## Is the request substantive?

- **Substantive → use @TP.** Any request to check, critique, generate, revise, explain,
  debug, format, translate, summarize, or otherwise assist with content related to a
  problem-set answer, derivation, economic argument, empirical design, code, interpretation,
  or submission. (Note: *generating / revising* substantive mathematics or economic
  reasoning is prohibited outright — see "Course AI policy limits" below.)
- **Administrative → no @TP needed.** Navigating or explaining files, explaining a shell
  command, clarifying something already said without new work, environment setup that does
  not affect substance.
- **Grouping minor follow-ups.** A short run of minor follow-up debugging or formatting
  requests may be folded into **one** interaction only if they (a) concern the same
  problem-set item, (b) happen in the same work session, and (c) are documented together in
  the same `AI_INTERACTIONS.md` entry. Group only when the student explicitly asks to.

## Course AI policy limits (enforce these during step 3)

- **Mathematical derivations** (`AI_POLICY.md` §1(a)): only **check** a derivation the
  student has already written, **explain** why a flagged step is wrong, or **diagnose** a
  specific step where the student is stuck. Never derive, continue, complete, rewrite, or
  replace the student's derivation. The student determines and implements every correction.
- **Economic reasoning** (`AI_POLICY.md` §1(b)): only **evaluate / critique** reasoning the
  student has already written — identify errors, omissions, inconsistencies, and explain
  them. Never generate, rewrite, or directly edit the economic argument.
- **Data analysis** (`AI_POLICY.md` §1(c)): a **specification written by the student** must
  already exist (plain-English `.md`/`.txt`, or initial code). Then you may implement,
  optimize, integrate, run, and debug that design.
  - You **may** make non-substantive programming choices (data structures, functions,
    packages, loops vs. vectorization, code organization).
  - You **may not** silently make substantive empirical choices that are missing from the
    spec — e.g. sample restrictions, timing conventions, treatment of missing observations,
    variable definitions, winsorization rules, regression specifications, standard-error
    choices. If such a decision is required, **flag the ambiguity and stop**; the student
    decides and updates the spec before you implement it.
  - Debugging: if the problem is purely computational, fix it. If debugging reveals that an
    empirical-design decision is needed, stop and have the student decide first.
- **Exposition help** is allowed *after* the substantive content exists (grammar, LaTeX,
  formatting, translating handwritten work into LaTeX). Log it as formatting/translation
  assistance; it must not generate, complete, or materially change the reasoning.

## Procedure

1. **Identify the problem-set item** (e.g. "Pset 1, Q1(a)"). If it is not clear from the
   request, ask the student to specify **before** doing any substantive work.
2. **Pre-work Git commit.** Record the current state of the repository:
   `git add -A` then `git commit -m "TP: before <item> — <short purpose>"`. If there is
   nothing to commit, use `git commit --allow-empty`. Record the resulting commit hash.
3. **Do the substantive work**, subject to the course AI policy limits above. If the request
   would require you to make a substantive mathematical, economic, or empirical-design
   decision the student has not specified, **stop, name the ambiguity, and ask the student
   to decide** before implementing.
4. **Append a new entry to `AI_INTERACTIONS.md`** using the template at the top of that
   file. **Do not modify, delete, combine, reorder, or rewrite any previous entry.** If a
   previous entry was wrong, leave it and record the correction in the new entry. The entry
   must include:
   - Problem-set item
   - The student's substantive prompt (verbatim or closely paraphrased)
   - Purpose of the request
   - Git commit hash **before** the interaction (from step 2)
   - A concise but complete description of the assistance provided
   - Files inspected
   - Files directly modified by AI, if any, and the nature of those changes
   - Any errors, omissions, or ambiguities identified
   - Any substantive mathematical, economic, or empirical suggestions made, distinguished
     from purely mechanical programming / formatting choices
   - Type(s) of assistance: math review | economic-reasoning review | empirical coding |
     code debugging | formatting/translation | other
   - Whether any minor subsequent debugging or formatting requests were grouped into this
     entry
5. **Post-work Git commit.** Commit the state after the interaction, including the
   `AI_INTERACTIONS.md` update: `git add -A` then
   `git commit -m "TP: after <item> — <short purpose>"`. If nothing changed, use
   `git commit --allow-empty`. Record the resulting commit hash.
6. **Report back** to the student: the problem-set item, both commit hashes, and the new
   `AI_INTERACTIONS.md` entry.

## If the record breaks

If step 2, 4, or 5 fails (no commit created, entry not appended), **stop and fix the record
before continuing** any substantive work (`AI_POLICY.md` §2(c)).
