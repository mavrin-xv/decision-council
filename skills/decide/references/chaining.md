# Chaining methods

What each method hands to the next.

| From | Field | To | Becomes |
|---|---|---|---|
| decision-log `check` | matching killed decision | user | "This was killed on {date} because {why}. Reopen?" |
| board-of-advisors | MAIN RISK | pre-mortem plan mode | the first failure reason to score |
| board-of-advisors | claims tagged [HYPOTHESIS] on the critical path | doubt loop | one loop per claim |
| marketing-council | FIRST TEST | pre-mortem | the plan to pre-mortem, if the test costs real money |
| pre-mortem | CRITICAL risks | doubt loop | the claim the mitigation depends on |
| pre-mortem | tripwires | decision-log | kill_if and review_on |
| any verdict | the artifact built from it | stress-test | target |
| stress-test SHIP | the live artifact | reality-check | the claims list |
| any accepted verdict | DECISION, WHY, MAIN RISK, KILL IF | decision-log `add` | the record |

## Confidence after several methods

Use the last method's score, then adjust:
- pre-mortem found an unmitigated CRITICAL risk: cap at 5.
- a doubt loop ended in STOP: cap at 5 until the open doubt is tested.
- stress-test verdict REWORK: the decision stands but the artifact does not ship; say so.
