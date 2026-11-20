---
name: reality-check
description: Checks whether something claimed as done, working or ready actually is, by demanding evidence for every claim instead of descriptions. Default verdict is NEEDS WORK; it moves to CONDITIONALLY APPROVED or APPROVED only when each claim has a named artifact (screenshot, log line, test output, real message received). Use when someone says a launch, page, automation, campaign setup or hire plan is "ready", "done", "works", "production ready", or the user asks "is this actually ready", "reality check", "verify before we launch", "did this really work", "go / no-go".
---

# Reality check

Claims are cheap. "Works automatically", "sends the confirmation", "tracking is set up" are sentences, not proof. This skill lists every claim, asks for the artifact that proves it, and refuses approval until the artifacts exist.

Use it at the end of a decision cycle: the board said do it, the stress test fixed the artifact, now confirm it is actually live before money or customers hit it.

## Inputs

1. What is claimed ready, and the original scope or spec (even 5 lines).
2. Access to evidence: the page URL, the workflow, screenshots, logs, a test account. If none is available, the verdict is NEEDS WORK and the output is the evidence list to collect.

## Procedure

1. **List claims.** Extract every claim from the spec and from what the builder said ("emails go out", "mobile works", "the discount applies once"). One claim per line. Mark the ones a launch cannot survive without as `(must)`.
2. **Four layers.** For each claim, check the layers in [references/layers.md](references/layers.md): it exists and runs, it does what it claims, it matches the spec, a real user can use it without help.
3. **Collect evidence.** For each claim, run it or open it now, and record the artifact: file name, URL, log line, number, the received message. If a browser tool is available (e.g. Playwright), take screenshots at mobile and desktop width. Anything you cannot run right now stays `[ ]`.
4. **Write the checklist** in the format from the script docstring and run `python3 scripts/evidence_check.py checklist.md`. Words like "tested", "works", "looks fine" do not count as evidence; the script marks them WEAK.
5. **Scope diff.** List what was in the spec and missing, and what was built but not in the spec (unplanned additions are risk: they were never tested against the goal).
6. **Verdict.** Use the script status. You may lower it with a reason; you may not raise it.

## Output

```
STATUS: NEEDS WORK | CONDITIONALLY APPROVED | APPROVED
EVIDENCE: OK / OPEN / WEAK / FAIL per claim (script output)
MISSING FROM SPEC: ...
ADDED WITHOUT SPEC: ...
MUST FIX: numbered, each with the evidence that will close it
CONDITIONS (if conditional): what must be true, and when it is rechecked
VERDICT: one sentence
```

## Automatic NEEDS WORK

- "Zero issues found" on a first version.
- "Production ready", "works perfectly", "fully tested" with no artifact attached.
- A must claim that was only described, not shown.
- Something built in minutes that claims to cover a whole spec.
- You cannot test it right now.

## Hard rules

- Never approve from a description. Show or test.
- A failed claim (`[!]`) blocks approval even if everything else passes.
- Conditional approval always lists the conditions and a recheck date.
- Do not run it on ideas; that is `pre-mortem`. Reality check is for things that claim to exist.
