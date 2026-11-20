# Example: Northwind Roasters price change

Invented two-person coffee subscription business. Every file here was produced by running the pack's scripts on invented inputs.

| Step | Input | Command | Output |
|---|---|---|---|
| Route | numbers from brief.md | `triage.py --cost-if-wrong 15 --reversible yes --type decision --variables 4` | triage.txt |
| Board round 1 | brief.md | five advisors answer (model calls) | answers.json |
| Blind review | answers.json | `council.py shuffle answers.json --seed 7 --out-dir council-run` | council-run/packet.md, mapping.json |
| Tally | reviews.json | `council.py tally reviews.json --mapping council-run/mapping.json` | tally.txt |
| Chairman | all of the above | model call | verdict.md |
| Pre-mortem | risks.csv | `risk_register.py risks.csv --md` | risk-register.txt |
| Stress test | findings.json | `merge_findings.py findings.json --md` | stress-report.txt |
| Reality check | checklist.md | `evidence_check.py checklist.md` | reality-check.txt |
| Log | verdict | `decision_log.py add / check / due / brief` | decisions/, decision-log.txt |

Model outputs (answers.json, reviews.json, findings.json, verdict.md) were written by hand for this example to show the shape. Script outputs are real runs.
