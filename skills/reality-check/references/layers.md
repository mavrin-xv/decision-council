# Four validation layers

## 1. It exists and runs
- Can it be opened right now? Show it.
- What happens on a phone screen?
- What happens on empty, wrong or very long input?
- What happens the second time (double submit, repeat order, re-run of the automation)?

## 2. It does what it claims
- For every "automatically": show it running without anyone touching it (a scheduled run log, a timestamp).
- For every "sends X": show the X that arrived (the email in an inbox, the message in the chat).
- For every "tracks X": show the event in the analytics tool with a time that matches a test action.

## 3. It matches the spec
- Line up the spec next to what was built. Every spec line is verified, missing or changed.
- List additions that were not in the spec. They were never checked against the goal.

## 4. It is useful
- Would the intended user complete the task tomorrow with no explanation?
- How many steps to first value? Count them.
- If it broke tomorrow, who would notice, and how fast? If nobody: add a check.

## Evidence that counts
| Counts | Does not count |
|---|---|
| Screenshot file at a named width | "Looks fine on mobile" |
| Log line with timestamp | "It ran" |
| Received email or message, with time | "Emails are set up" |
| Test output with pass count | "Tests pass" |
| An order or record id in the system | "Checkout works" |
