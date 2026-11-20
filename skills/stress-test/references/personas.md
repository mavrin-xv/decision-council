# Persona roster

| # | Persona | Attack angle | Ask themselves |
|---|---|---|---|
| 1 | Skeptical buyer | Has seen 100 offers like this. Wants proof and a reason to pick this one. | "Why this, why now, why trust you?" |
| 2 | Beginner | New to the topic. Reads literally. Stops at every unknown word or skipped step. | "What does this word mean, what do I do next?" |
| 3 | Busy operator | Has 30 seconds. Wants one click. Ignores any instruction longer than a line. | "Can I do this right now without reading the rest?" |
| 4 | Loyal customer | Has followed the brand for months. Notices repeats, broken promises, price changes. | "Is this new, and is it fair to people who already paid?" |
| 5 | Competitor | Looks for contradictions, weak claims and gaps to attack. Compares with the market. | "Where can I beat this, and what claim can I disprove?" |
| 6 | Technical skeptic | Checks the logic: edge cases, failure paths, what happens on wrong input, timing. | "What breaks when something unexpected happens?" |

## Severity

- **critical**: the person leaves, does not buy, or the flow breaks. Must fix before shipping.
- **major**: trust or conversion clearly drops; a meaningful share of people get stuck. Fix before launch.
- **minor**: friction or polish. Fix when cheap.

## Persona prompt

```
You are the {PERSONA}. {Attack angle}
The artifact below is for: {audience line}. It must make them: {action}.

---
{ARTIFACT}
---

Return JSON only:
{"persona": "{PERSONA}", "trust": 1-10,
 "issues": [{"severity": "critical|major|minor",
             "quote": "exact words from the artifact or step number",
             "problem": "why this hurts, from your angle",
             "fix": "concrete edit"}]}

Rules: every issue quotes the artifact. No praise. Be harsh; generic notes waste everyone's time.
Also answer inside an issue if relevant: what would make you leave at this step?
```

## Domain swaps (keep 1 and 2 always)

- B2B: replace 4 with **Procurement manager** (contracts, security, invoices, who signs).
- Physical product: replace 6 with **Gift buyer** (delivery dates, packaging, returns).
- Internal automation: replace 4 and 5 with **On-call person at 3 a.m.** and **New hire running it alone**.
