---
name: stress-test
description: Attacks a plan, offer, landing page, onboarding flow, automation or brief with 6 personas in parallel (skeptical buyer, beginner, busy operator, loyal customer, competitor, technical skeptic). Each returns issues with the exact quote that triggered them, a severity and a fix; a script merges duplicates and gives SHIP / REVISE / REWORK. Use when something is about to ship or be shown to customers and the user says "stress-test this", "find the weak spots", "what will confuse people", "test my offer", "poke holes in this flow", "is this ready to launch", or after building any new funnel, offer or automation.
---

# Stress test

A decision answers "should we". A stress test answers "will this survive contact with real people". Six personas read the same artifact, each hunting for a different kind of failure, and every issue must point at an exact quote.

## When to use

- An offer, sales page, email sequence, pricing table, onboarding flow, automation spec or internal brief is drafted and about to go live.
- A board or marketing council verdict was accepted and turned into an artifact: test the artifact.

Not for: deciding whether to do the thing at all (`board-of-advisors`), predicting failure of a whole plan over months (`pre-mortem`).

## Inputs

1. **The artifact**, as text. Pages: paste the copy in reading order, with notes for images and buttons. Flows: numbered steps.
2. **Who it is for** in one line and **what it must make them do** (buy, book, reply, finish setup).

## Procedure

1. **Dispatch 6 personas in one message** using the roster and prompt in [references/personas.md](references/personas.md). Each gets the artifact and the audience line. Swap at most 2 personas for domain ones (for example "Procurement manager" for a B2B offer); keep the skeptical buyer and the beginner always.
2. **Each persona returns JSON**: trust score 1-10 and a list of issues, each with severity (critical / major / minor), the exact quote, the problem and a specific fix. Severity definitions are in the reference. An issue with no quote is dropped.
3. **Merge.** Save all six to `findings.json` and run `python3 scripts/merge_findings.py findings.json --md`. It merges issues that quote the same text, ranks issues found by several personas higher, and applies the verdict rule.
4. **Judge the merge.** Read the critical and major list yourself. Remove issues that misread the artifact (say which). Do not remove an issue only because it is uncomfortable.
5. **Second round if REVISE or REWORK.** Apply the fixes, then rerun only the 2 personas that gave the lowest trust scores on the revised artifact. Stop after 2 rounds and report what is still open.

## Output

```
STRESS TEST: {artifact}, {date}
CRITICAL: issue, quote, fix, found by
MAJOR: ...
MINOR: ... (max 5, the rest in a count)
TRUST: per persona and average
VERDICT: SHIP / REVISE / REWORK
Round 2: what changed, new trust scores (if run)
```

## Hard rules

- Quote or it did not happen. Every issue cites the artifact's own words or a numbered step.
- Fixes are concrete edits ("replace 'onboarding' with 'setup, 10 minutes'"), not advice ("make it clearer").
- Personas stay harsh. Praise is not returned; it wastes the reader's time.
- Verdict comes from the script rule, then the model may downgrade an issue only with a written reason.

## Failure modes

| Symptom | Fix |
|---|---|
| Six personas find the same 3 things | Prompts lacked the attack angle. Paste each persona block in full. |
| Beginner understands everything | The beginner was given background. Give only the artifact. |
| Lots of minor wording notes, no critical | Ask each persona: "what would make you leave at this step?" and rerun. |
| Loop keeps finding new issues | Two rounds max. Ship with known minors listed. |
