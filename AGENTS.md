# AGENTS.md

Notes for coding agents (Claude Code, Codex, Cursor, others) working on this repository.

## What this is

A skill pack. The product is the text in `skills/*/SKILL.md` and `references/`, plus small stdlib Python helpers in `skills/*/scripts/`. There is no server and no dependency to install.

## Layout

- `skills/decide/`: the router. Change it when you add or remove a method.
- `skills/board-of-advisors/`, `skills/marketing-council/`: council skills. Both ship the same `scripts/council.py`; keep the two copies identical.
- `skills/pre-mortem/`, `skills/stress-test/`, `skills/reality-check/`, `skills/decision-log/`: single-method skills, each with one script.
- `templates/`: blank inputs. `examples/northwind-price-change/`: a full invented run.
- `commands/`: thin slash commands that call a skill.

## Rules

- SKILL.md frontmatter has only `name` (same as the folder) and `description` (under 1024 characters, says what and "Use when"). Keep bodies under 500 lines; move detail to `references/`.
- Scripts: Python 3.8+, standard library only, `--help` works, exit codes documented in the docstring.
- Examples use invented businesses and people. No real company, person, account or city names.
- Run before you finish:

```bash
cd examples/northwind-price-change
python3 ../../skills/board-of-advisors/scripts/council.py tally reviews.json --mapping council-run/mapping.json
python3 ../../skills/pre-mortem/scripts/risk_register.py risks.csv --md
python3 ../../skills/stress-test/scripts/merge_findings.py findings.json --md
python3 ../../skills/reality-check/scripts/evidence_check.py checklist.md
python3 ../../skills/decision-log/scripts/decision_log.py --dir decisions check "wholesale to cafes"
python3 ../../skills/decide/scripts/triage.py --cost-if-wrong 15 --reversible yes --type decision
cmp ../../skills/board-of-advisors/scripts/council.py ../../skills/marketing-council/scripts/council.py
```

Expected exit codes: tally 0, risk register 0, merge 1 (REVISE), evidence check 1 (NEEDS WORK), check 3 (killed match), triage 0.
