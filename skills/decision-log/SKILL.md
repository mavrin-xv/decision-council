---
name: decision-log
description: Keeps a plain-markdown log of business decisions with the reason, main risk, kill criterion and review date, flags when a new proposal repeats an idea that was already killed, and lists decisions due for review so they get checked against what actually happened. Use when the user makes or accepts a decision ("we decided", "log this", "write this down", "from now on", "we are not doing X again", "kill this idea"), after a board or council verdict is accepted, when a new proposal might contradict an earlier call, or at the start of a planning session ("what did we decide about X", "what is due for review").
---

# Decision log

Teams repeat dead ideas and forget why they chose what they chose. A decision log fixes both if it stays small, has a review date on every entry, and is checked before new proposals.

Two layers:
- **The log** (`decisions/`, one file per decision). Every decision, including killed ideas and reversed calls. Searched on demand, never loaded whole.
- **The brief** (output of `decision_log.py brief`). Up to 20 active decisions plus the "do not resurface" list. Small enough to load at the start of a session.

## When to use

- A verdict from `board-of-advisors`, `marketing-council` or `pre-mortem` is accepted.
- The user states a rule or kills an idea.
- A new proposal arrives: run `check` first.
- Start of a weekly or monthly planning session: run `due`.

## Procedure

### Record
1. Confirm with the user in one line: "Log this as a decision?" Never log silently what the user only floated.
2. Fill the record. Required: title, decision. Strongly expected for active decisions: why, risk, kill_if (metric + threshold + date), review_on. The template is [references/record-format.md](references/record-format.md).
3. Run:
   ```bash
   python3 scripts/decision_log.py add --title "..." --decision "..." --why "..." \
     --risk "..." --kill-if "..." --review-on 2026-06-30 --confidence 7 --method board-of-advisors
   ```
   The script warns if kill_if or review_on is missing. Ask for them once; log anyway if the user declines.
4. Killed idea: `--status killed` with `--why` stating what killed it. Killed entries are what `check` protects.

### Check a new proposal
`python3 scripts/decision_log.py check "proposal text"`. It lists related past decisions by shared keywords and exits 3 when a killed decision matches. On a match, show it to the user before doing anything:
```
Conflict with a decision from {date}: "{decision}" (status: killed, because {why}).
Reopen it? If yes, say what changed since then.
```
Reopen only with a stated change in facts. Then log the new decision with `--status active` and review the old one with `--status superseded`.

Keyword matching misses paraphrases. Also read the `brief` yourself and judge meaning, not only words.

### Review
`python3 scripts/decision_log.py due` lists active decisions past their review date. For each: read the kill criterion, get the actual number, then record:
`python3 scripts/decision_log.py review FILE --outcome "Churn 4.2% vs kill line 7%: keep" [--status reversed]`.
Write outcomes even when the decision held. A log with no outcomes teaches nothing.

### Load at session start
`python3 scripts/decision_log.py brief` and keep it in context. Apply active decisions without announcing them; flag conflicts before acting.

## Hard rules

- The user approves every entry. The agent proposes, never promotes silently.
- "Do not resurface" is respected until the user reopens it with a stated reason.
- Every active decision has a review date. Decisions with no review date are opinions.
- Brief stays at 20 active entries max. When over, supersede or archive the oldest.
- Never edit an old decision's text to match a new view. Add a new decision and supersede the old one, so the history stays true.

## Configure

`DECISION_LOG_DIR` sets the folder (default `./decisions`). Files are plain markdown and can live in a repo, a notes vault or a shared drive.
