# Record format

One file per decision: `decisions/YYYY-MM-DD-short-slug.md`. The script writes and reads the `- **key:** value` lines; anything below them is free notes.

```markdown
# Raise the standard plan to $18 for new customers

- **date:** 2026-04-02
- **status:** active
- **decision:** New customers pay $18/month from May 1. Existing customers stay at $12 for 6 months.
- **why:** Margin on the $12 plan is 9% after shipping; competitors sit at $15-17.
- **risk:** New-customer conversion drops more than the price gain.
- **kill_if:** Trial-to-paid below 18% for 4 weeks after May 1 (baseline 24%).
- **review_on:** 2026-06-01
- **confidence:** 7
- **method:** board-of-advisors
- **tags:** pricing, subscription

Notes: board split on grandfathering length (3 vs 6 months). Chairman sided with 6.
```

## Status values

| Status | Meaning |
|---|---|
| active | In force. Shows in the brief and in `due` once past review_on. |
| killed | Idea rejected. `check` exits 3 when a proposal matches it. Keep `why`. |
| reversed | Was active; the review showed it was wrong. Outcome says what happened. |
| superseded | Replaced by a newer decision. Name the new file in the outcome. |

## Writing a kill criterion

Metric + threshold + date, readable without interpretation.
- Good: "Fewer than 30 paid pre-orders by June 15."
- Good: "Refund rate above 5% in the first 60 days."
- Bad: "If it doesn't work out."
- Bad: "If customers don't like it."

## Types worth logging

| Type | Log? |
|---|---|
| Hard rule ("we never discount the annual plan") | yes, active |
| Product, price, channel, hire decisions | yes, active |
| Killed idea | yes, killed |
| Experiment result that changes a future choice | yes, with outcome |
| Tactical note ("used tool X this week") | no |
