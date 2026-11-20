---
name: decide
description: Entry point for getting one trusted verdict on a business decision. Sizes the stakes (cost if wrong, reversibility, moving parts), picks the cheapest method that fits (doubt loop, pre-mortem, board of advisors, marketing council, stress test, reality check), runs them in order and ends with a logged decision. Use when the user brings any decision or plan and asks "help me decide", "should we", "what do you think about doing X", "is this a good idea", "which option", "I have an idea", or does not know which council or check to run.
---

# Decide

The pack has six methods. Running the biggest one on every question wastes time and money; running none on a big bet is how expensive mistakes happen. This skill routes.

## Procedure

1. **Restate the decision as a choice.** "Should Northwind open a second location in the spring, yes or no" not "growth". If there are several options, list them (max 4).
2. **Size it.** Ask or estimate three things:
   - cost if wrong, in working days or money,
   - reversible within a week for little cost: yes or no,
   - moving parts (price, audience, timing, channel, team, supplier...).
   And classify the type: `decision` (whether to do it), `marketing` (how to reach buyers), `plan` (dated plan about to start), `claim` (one sentence a choice rests on), `built` (something said to be ready).
3. **Route.** Run `python3 scripts/triage.py --cost-if-wrong 15 --reversible no --type decision --variables 4` or apply the table below by hand.
4. **Run the methods in order**, passing each one's output into the next: the board's MAIN RISK becomes the pre-mortem's starting point, the pre-mortem's top claim goes to the doubt loop, the accepted verdict goes to `decision-log`. Field-by-field handoffs: [references/chaining.md](references/chaining.md).
5. **Close.** One final block, whatever methods ran:
   ```
   DECISION:  ...
   CONFIDENCE: N/10 (from the last method that scored it)
   FIRST STEP: ...
   KILL IF:   metric + threshold + date
   LOGGED:    file name, or "not logged (user declined / low stakes)"
   ```

## Routing table

| Situation | Run |
|---|---|
| Low stakes (under 2 days if wrong, reversible) | Doubt loop on the one claim it rests on, then decide. No council. |
| Whether to do something, mid or high stakes | `board-of-advisors` |
| Channel, message, campaign, funnel, positioning | `marketing-council` |
| High stakes or irreversible | add `pre-mortem` plan mode after the council |
| A dated plan about to start | `pre-mortem` plan mode, then doubt loop on the riskiest claim |
| An offer, page or flow ready to ship | add `stress-test` |
| Someone says it is done or ready | `reality-check` |
| Any accepted mid or high stakes verdict | `decision-log` |

Before any council, run `decision-log check` on the proposal. If it matches a killed idea, surface that first: there may be nothing to decide.

## Hard rules

- Match cost to stakes. A full board is 11 model calls; a marketing council is 17. Say the cost before running it on a small question.
- One verdict at the end, even when several methods ran. If two methods disagree, the later one with more evidence wins, and the disagreement is stated.
- Never skip the user's approval before logging.
- If the user only wants a quick opinion, give it, and offer the method in one line instead of running it.
