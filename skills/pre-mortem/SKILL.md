---
name: pre-mortem
description: Finds how a plan or claim fails before you commit. Two modes. Plan mode runs a Klein-style pre-mortem (it is 6 months later and this failed, write why), scores each failure reason by likelihood, impact and reversibility, and attaches tripwires and owners. Claim mode runs a doubt loop on one confident statement (claim, extract hidden assumptions, strongest doubt each, reconcile, stop) with a fresh-context reviewer that never sees the conclusion. Use when the user is about to commit money or time, says "pre-mortem", "what could go wrong", "doubt this", "poke holes", "prove it", "are we sure", "is this assumption right", or a board verdict scored 6/10 or less.
---

# Pre-mortem and doubt loop

Optimism hides failure reasons. Imagining that the failure already happened makes people name more of them (prospective hindsight, the basis of Gary Klein's pre-mortem). The doubt loop does the same for a single statement: it pulls out what must be true and tries to break each piece.

Pick the mode:
- **Plan mode**: there is a plan with steps, dates, money. "We launch the subscription box in March."
- **Claim mode**: there is one confident sentence a decision rests on. "Our customers will pay $18."

A plan usually contains 1 to 3 load-bearing claims. Run plan mode first, then claim mode on the claims behind the top risks.

## Plan mode

### Inputs
The plan in 3 to 10 lines: goal, what happens when, budget, team, success metric and date.

### Steps
1. **Set the scene.** Write: "It is {date + horizon}. The plan failed. Not a little: it clearly failed." Default horizon: 6 months, or the plan's own deadline.
2. **Generate failure reasons, independently.** Spawn 3 subagents in one message with different seats: the operator who runs it day to day, the customer, the person paying for it. Each writes 5 to 8 reasons it failed, specific and in past tense ("The supplier shipped late and we missed the gift season"). No solutions yet. Single-context host: write the three lists one after another and do not edit earlier lists.
3. **Merge.** Deduplicate into one list. Keep the most specific wording. Tag each reason with its category from [references/failure-categories.md](references/failure-categories.md) and check the categories that got zero reasons: add at least one reason for each empty category or state why it does not apply.
4. **Score.** For each reason: likelihood 1-5, impact 1-5, reversible yes/no. Use the anchors in [references/scoring.md](references/scoring.md).
5. **Tripwire and owner.** For every reason scoring 8 or more: the earliest observable signal with a threshold and date ("fewer than 40 sign-ups by day 14"), the mitigation you do now, and the person who watches it.
6. **Check.** Save as CSV (columns in the script docstring) and run `python3 scripts/risk_register.py risks.csv --md`. It sorts, bands (CRITICAL / WATCH / ACCEPT) and exits 1 if a critical risk has no mitigation or a watched risk has no tripwire or owner. Fix gaps until it passes.
7. **Reshape.** For each CRITICAL risk choose one: change the plan so it cannot happen, add a cheap test before the big spend, or accept it out loud with the user's name on it.

### Output
```
PRE-MORTEM: {plan}, horizon {date}
Top risks (table from risk_register.py --md)
Plan changes: what changes before start, one line each
Tests before spend: test, cost, pass threshold
Accepted risks: risk, who accepted
Verdict: GO / GO AFTER CHANGES / NO GO
```
NO GO when a CRITICAL risk has no possible mitigation and is irreversible.

## Claim mode (doubt loop)

### Steps
1. **CLAIM.** One sentence, no hedging, plus why it matters ("if wrong, we lose the launch budget"). If you cannot write it in one sentence it is a vibe: say so and stop. Compound claims ("X and Y and Z") become separate loops.
2. **EXTRACT.** List at least 3 hidden assumptions that must be true. Fewer than 3 means you are not looking. Also write the **contract**: what the claim must satisfy (numbers, dates, constraints).
3. **DOUBT.** Send ONLY the assumptions and contract to a fresh subagent, never the claim or your reasoning: handing over the conclusion gets you agreement. Use the prompt in [references/doubt-prompt.md](references/doubt-prompt.md). It returns the strongest counter-argument per assumption, not a list of weak ones.
4. **RECONCILE.** For each assumption pick exactly one outcome:
   - **survives**, with a source (labels: FACT, INTERNAL, CONVERGENCE; "common sense" is not a source),
   - **narrows**: the claim shrinks to a scope where it holds ("all customers" becomes "repeat customers in the first year"),
   - **dies**: the claim does not hold.
5. **STOP.** If any doubt is unreconciled or any assumption died, the claim is not ready. Report it. If only narrowing happened, restate the narrowed claim and optionally loop again. Hard cap: 3 loops on the same claim, then hand the open doubts to the user.

### Output
```
DOUBT LOOP: {claim}
Assumptions -> strongest doubt -> outcome (survives via SOURCE / narrows to SCOPE / dies)
Unreconciled: list or NONE
Verdict: PROCEED / PROCEED WITH NARROWED CLAIM: ... / STOP
Cheapest test to settle the open doubt: ...
```

## Hard rules

- Reasons are written in past tense as things that happened. "Might fail if" is not allowed; it lets people hedge.
- No solutions during generation (plan step 2). Mixing them kills the list.
- Every score of 8+ gets a tripwire with a number and a date. "Monitor closely" is not a tripwire.
- The doubt reviewer never sees the claim. This is the rule people break most.
- Do not run claim mode on taste or values ("our brand should feel warm"). Only on falsifiable claims.

## Failure modes

| Symptom | Fix |
|---|---|
| Every reason is "not enough marketing" | Seats were not distinct. Rerun step 2 with the category list as prompts. |
| All risks score 3x3 | Scorer is hedging. Force at least one 5 or justify why nothing can kill the plan. |
| Doubt reviewer agrees with everything | It saw the claim or your reasoning. Strip both, rerun. |
| Loop never ends | Cap at 3. Remaining doubt becomes a test, not more discussion. |
