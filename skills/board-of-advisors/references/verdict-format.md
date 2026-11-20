# Verdict format

```
=== BOARD VERDICT ===
DECISION:     one line. Do / don't / do it this other way.
WHY:          2-3 sentences. What tipped it.
MAIN RISK:    one concrete risk, with the number or event that would show it.
FIRST STEP:   one action that can start today.
KILL IF:      the observable result that means stop (metric + threshold + date).
SPLIT:        where the board disagreed, one line. "None" only if the tally agrees.
NOT COVERED:  what no advisor addressed that matters.
CONFIDENCE:   N/10, one line on why.
=====================
```

## Confidence scale

| Score | Meaning | Required |
|---|---|---|
| 9-10 | Near certain | Every load-bearing claim is FACT or INTERNAL; board aligned; reversible |
| 7-8 | Strong | At most 1 HYPOTHESIS on the critical path; a kill criterion exists |
| 5-6 | Coin with an edge | 2+ HYPOTHESIS claims, or board split on the core argument |
| 3-4 | Lean against | Main risk is likely and expensive |
| 1-2 | Do not | A fatal flaw stood up in review |

Irreversible decisions (long contracts, public price cuts, firing, large prepaid spend) lose 1 point unless the main risk has a tested mitigation.

## Decision record handoff

When the user accepts, pass to `decision-log`:

```
title:      short name
decision:   DECISION line
why:        WHY line
risk:       MAIN RISK line
kill_if:    KILL IF line
review_on:  date when the kill criterion can be read
confidence: N
method:     board-of-advisors
```
