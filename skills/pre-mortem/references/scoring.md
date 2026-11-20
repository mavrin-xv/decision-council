# Scoring anchors

## Likelihood
| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Never seen it happen in this kind of plan | Happened to others, rare | Happens often enough that you know someone it hit | More likely than not given what we know | Already showing signs |

## Impact
| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Annoying, absorbed in a day | Costs a week or a small share of budget | Misses the goal date or a third of the target | Misses the goal; recovery needs new money or a pivot | Ends the plan or harms the core business |

## Reversible
- **yes**: you can stop or undo within days for little cost (pause ads, revert a page, refund a few orders).
- **no**: long contracts, prepaid inventory, a public price cut, a hire, a broken promise to customers. Score is multiplied by 1.5.

## Bands (used by `scripts/risk_register.py`)
- **15+ CRITICAL**: change the plan, add a test before spend, or accept explicitly by name.
- **8-14 WATCH**: needs tripwire, mitigation and owner.
- **under 8 ACCEPT**: listed, no action.

## Good tripwires
A tripwire is observable, early, numeric and dated.
- Good: "Fewer than 25 paid pre-orders by day 10 of the waitlist."
- Good: "Cost per lead above $14 for 3 days in a row."
- Bad: "Watch sign-ups." (no threshold)
- Bad: "Revenue below plan at quarter end." (too late to act)
