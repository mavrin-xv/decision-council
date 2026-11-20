# Evidence labels

Any claim about demand, pricing, competitors, channels or customer behaviour carries one label. Unlabelled market claims are treated as hypotheses.

| Label | Use for | Example |
|---|---|---|
| `[FACT: source]` | Public, checkable source: URL, dataset, filing, named article with date | `[FACT: competitor pricing page, read 2026-03-02] They charge $15/mo.` |
| `[INTERNAL: source]` | Your own data: dashboard export, sales log, survey file, named call | `[INTERNAL: Q1 churn export] 6.1% monthly churn on the $12 plan.` |
| `[CONVERGENCE: n sources]` | Several independent sources say the same thing | `[CONVERGENCE: 4 operator posts] Annual plans cut churn for this niche.` |
| `[HYPOTHESIS]` | No source. Plausible, untested | `[HYPOTHESIS] Customers will accept $18 if shipping is free.` |

## Rules

- One source minimum for FACT. "Everyone knows", "studies show", "industry trends" are HYPOTHESIS.
- Trend claims older than 90 days get "(may be stale)".
- Practitioner sources beat generic reports for small-business decisions: a shop owner's posted numbers beat a consulting deck.
- Your own results count. A sales export is data.
- Never mix labels in one sentence. Split the sentence.

## Why it matters for the verdict

Count the HYPOTHESIS labels on the critical path (the claims the decision fails without). That count caps confidence: see [verdict-format.md](verdict-format.md). Each one is also a candidate for the cheapest test in FIRST STEP.
