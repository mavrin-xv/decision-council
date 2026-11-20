---
name: board-of-advisors
description: Runs a board of 5 advisors with different thinking frames (Contrarian, First Principles, Expansionist, Outsider, Executor) on one business decision, has them review each other blind, then a chairman writes ONE verdict with a confidence score, the main risk and a first step. Use when the user faces a major call with real cost of being wrong, such as a new product, a price change, a pivot, a hire, a channel bet, or says "should I do X", "council this", "run the board", "war room this", "help me decide", "pressure-test this decision". Not for facts, content edits or code review.
---

# Board of Advisors

One question in, one verdict out. Five advisors attack the decision from five frames that do not overlap, review each other without knowing who wrote what, and a chairman turns that into a single call you can act on.

Why blind review: when advisors see each other's names and roles, they drift into polite agreement. Hiding authorship makes them judge the argument. This is the core of Karpathy's LLM Council, applied to business decisions.

## When to use

Use it when all three are true:
- the decision costs more than a day of work or real money if wrong,
- there are at least 3 moving parts (price, audience, timing, channel, team),
- you would otherwise decide on gut feel.

Skip it for factual lookups, writing tasks, or anything a single quick answer covers. For a single confident claim use `pre-mortem` (doubt loop). For a plan that is about to ship use `stress-test`. For a marketing choice (channel, message, campaign) use `marketing-council`.

## Inputs

Collect before round 1. If the user gave a one-liner, ask at most 2 questions:
1. **The decision**, as a choice: "Raise the plan from $12 to $18 for new customers" beats "pricing".
2. **Context**: what exists today, what was tried, numbers you have.
3. **Horizon and constraint**: by when, and what cannot change (budget, team, runway).

Write these into a brief using `templates/council-brief.md` (repo root; the installer also copies it into this skill folder), or the 3 headings above. Every advisor gets the same brief.

## Procedure

### Round 1: five independent takes (parallel)

Spawn 5 subagents in ONE message so none sees another's answer. If the host cannot spawn subagents, write each take in a separate turn and do not reread earlier takes while writing the next (flag the run as "single-context, degraded").

Give each the brief plus its frame from [references/advisors.md](references/advisors.md). The Outsider gets the brief WITHOUT company history or insider vocabulary: just what a customer would see.

Each advisor returns, in under 250 words:
- **Position**: do / don't / do differently, in one line.
- **Core argument**: the 2 or 3 reasons.
- **The one thing that would change my mind.**
- **Frame-specific ending** (listed per advisor in the reference).

### Round 2: blind peer review (parallel)

1. Save the five takes to `answers.json` as `{"question": ..., "answers": {"Contrarian": "...", ...}}`.
2. Run `python3 scripts/council.py shuffle answers.json --out-dir council-run`. It writes `packet.md` (answers labelled A to E in random order, roles stripped) and `mapping.json`.
3. Spawn 5 fresh reviewers. Each gets `packet.md` only. Each returns: strongest answer and why, the most serious blind spot and why, what all five missed, and a full ranking A to E.
4. Save reviews to `reviews.json` (format in the script docstring) and run `python3 scripts/council.py tally reviews.json --mapping council-run/mapping.json`.

No scripts available? Relabel by hand in a random order, and never tell reviewers which frame wrote which answer.

### Round 3: chairman synthesis

The chairman reads all 5 takes, all 5 reviews and the tally. Rules:
- **Synthesize, do not average.** One decision, not "on one hand".
- **Arguments beat headcount.** If 4 agree and 1 dissents with stronger reasoning, side with the dissenter and say why.
- **Name the split.** If the tally shows an answer voted both strongest and blind spot, that is the real argument in the room: state it.
- **Label evidence.** Every market claim in the verdict is tagged `[FACT: source]`, `[INTERNAL: source]` or `[HYPOTHESIS]` per [references/evidence-labels.md](references/evidence-labels.md).
- **Confidence is earned.** Use the scale in [references/verdict-format.md](references/verdict-format.md). A verdict resting on 2+ hypotheses cannot score above 6.

Output the verdict block exactly as in [references/verdict-format.md](references/verdict-format.md).

### After the verdict

Ask the user one question: accept, or go deeper on one angle? If accepted and the decision matters beyond today, hand off to `decision-log` with the verdict, the kill criteria and a review date. If confidence is 6 or lower, offer `pre-mortem` on the main risk before committing.

## Hard rules

- 5 advisors, 5 frames, no frame repeated, no advisor allowed to "see both sides". Their job is one lens.
- Round 2 is not optional. Without it the run is an opinion poll.
- The chairman never introduces a new argument that no advisor or reviewer made. If something important is missing, say so under "What the board did not cover".
- One verdict. If the honest answer is "it depends", the verdict names what it depends on and the cheapest test that settles it.
- Do not use real people as advisors ("what would a famous investor say"). Frames, not impersonations: they produce caricatures.

## Failure modes

| Symptom | Fix |
|---|---|
| All 5 takes agree | The brief leaked a preferred answer. Rewrite it as a neutral choice and rerun round 1. |
| Takes are generic ("it depends on your market") | Brief has no numbers. Ask for one number per moving part. |
| Reviewers praise everything | They were not told to rank. Ranking forces a worst answer. |
| Verdict is a list of options | Rerun round 3 with "pick one, name the test that would reverse it". |
| Costly run for a small call | Use `pre-mortem` doubt loop instead; the board is 11 model calls. |

## Cost

A full run is 5 advisor calls, 5 reviewer calls and 1 chairman call. Use it for decisions, not daily questions.
