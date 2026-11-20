# Doubt reviewer prompt

Send this to a fresh subagent (or a different model). Paste the assumptions and the contract. Do NOT paste the claim, the plan's rationale, or your own view.

```
Adversarial review. Below are assumptions a business decision depends on, and the
contract the decision must meet. Assume the author is overconfident.

For EACH assumption, give the single strongest counter-argument: the most likely real-world
way it is false, with a concrete mechanism, a historical pattern, or a number that would show it.
No weak "maybe some people won't" doubts. No summaries. No praise.
If after real effort you cannot break an assumption, say "could not break" and why.

Then list any assumption the author did not write but which must also be true.

ASSUMPTIONS:
A1: ...
A2: ...
A3: ...

CONTRACT:
...
```

## Strong vs weak doubt

- Weak: "Maybe customers won't like the higher price."
- Strong: "Comparable coffee subscriptions sit at $14-16; a $18 price puts you top of the shelf with no visible extra value, and subscription buyers compare monthly totals, not per-bag prices."

## Cross-model option

A reviewer from a different model family shares fewer blind spots with the author. If the user has another model CLI installed, offer it. Write the prompt to a file and pass it on stdin so quotes and backticks in the text are never run by the shell:

```bash
some-model-cli < doubt-prompt.txt
```

Ask the user before calling any external tool. Never paste secrets or customer data into it.
