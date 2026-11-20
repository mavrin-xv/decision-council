---
name: marketing-council
description: Runs a council of 8 marketing specialists (performance, brand, direct-response copy, creative, distribution, guerrilla, community voice, skeptic) on one marketing decision, then blind peer review, then a chairman verdict with the main risk, a first test and kill criteria. Use when the user must pick a channel, a campaign concept, an offer message, a funnel design, a launch plan or a positioning change before spending budget or weeks of effort, or says "which channel", "is this campaign good", "marketing council", "pressure-test my launch plan", "should we run ads or content". Not for proofreading a single post.
---

# Marketing Council

Same protocol as `board-of-advisors` (independent takes, blind review, chairman), with 8 marketing lenses instead of 5 general ones. Use it when the question is how to reach, convince and convert buyers, not whether the business move itself is right.

## When to use

- Choosing or dropping a channel, or the order of channels.
- A campaign, launch or offer message before money or weeks go into it.
- Funnel design: what the buyer sees first, second, third, and where they convert.
- A positioning or messaging change.

Not for: whether to build the product (use `board-of-advisors`), line edits on one ad (a single reviewer is enough).

## Inputs

Ask for what is missing, max 3 questions:
1. **The decision**: the channel, campaign or message under review, as a choice.
2. **The buyer**: who, awareness level (unaware, problem aware, solution aware, product aware, most aware), where they spend time.
3. **Numbers**: price, margin, current conversion or traffic, budget, time available.
4. **Brand context**: 3 lines on positioning and voice, plus 1 to 3 recent examples of the brand's own content. Without this, specialists give generic advice.

## Procedure

### Round 1: eight independent takes

Spawn 8 subagents in one message. Each gets the brief and one frame from [references/specialists.md](references/specialists.md). Each answers in under 200 words:
- Position (do / don't / change it),
- the 2 or 3 findings from its lens with a quote or number from the brief,
- the one change it would make,
- its frame question answered.

If the host cannot spawn subagents, write takes one at a time and mark the run as degraded.

### Round 2: blind review

1. Save takes to `answers.json`, run `python3 scripts/council.py shuffle answers.json --out-dir mc-run`.
2. Spawn 8 reviewers with `mc-run/packet.md` only. Each returns strongest, blind spot, what all missed, full ranking A to H.
3. Run `python3 scripts/council.py tally reviews.json --mapping mc-run/mapping.json`.

To cut cost, 4 reviewers is acceptable for a mid-stakes call; never fewer than 4.

### Round 3: chairman

Same rules as the board: synthesize, arguments over headcount, name the split, label evidence per [references/evidence-labels.md](references/evidence-labels.md). Then add the marketing-specific checks:
- **Numbers check.** If the performance lens could not compute a cost per lead or payback from the brief, FIRST STEP must collect that number.
- **Awareness check.** If the copy lens found the message is pitched at the wrong awareness level, that outranks creative and distribution findings.
- **Distribution check.** A verdict with no named first channel and posting order is incomplete.

Output:

```
=== MARKETING COUNCIL VERDICT ===
DECISION:      one line
WHY:           2-3 sentences
FIRST CHANNEL: where it goes first, then second, and what moves a buyer from one to the next
MESSAGE:       the one sentence the buyer must remember
MAIN RISK:     concrete, with the metric that shows it
FIRST TEST:    smallest test, budget or hours, sample size, duration
KILL IF:       metric + threshold + date
SPLIT:         where the council disagreed
CONFIDENCE:    N/10
=================================
```

Confidence scale and handoff format: see `board-of-advisors`, [references/verdict-scale.md](references/verdict-scale.md).

## Hard rules

- 8 lenses, each plays only its lens. The Skeptic is never removed.
- Every specialist must cite a line or number from the brief. A take with no quote is discarded and rerun.
- No vanity metrics in KILL IF (likes, impressions alone). Use leads, replies, sign-ups, sales, cost per result.
- The chairman picks ONE first channel. "Be everywhere" is not a verdict.

## Failure modes

| Symptom | Fix |
|---|---|
| Advice fits any business | Brand context missing. Add 3 lines plus examples, rerun round 1. |
| Performance lens says "unknown" for every number | FIRST STEP becomes "measure", not "launch". |
| Creative and copy contradict each other | Put it in SPLIT; FIRST TEST is an A/B of the two. |
| Council loves a guerrilla stunt | Check it against brand risk in the community lens before accepting. |
