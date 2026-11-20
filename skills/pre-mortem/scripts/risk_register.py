#!/usr/bin/env python3
"""Score and sort a pre-mortem risk register, and flag risks with no tripwire.

Usage:
  python risk_register.py risks.csv [--top N] [--md]
  python risk_register.py --help

risks.csv columns (header row required, extra columns ignored):
  risk          short failure reason ("Supplier misses the March delivery")
  likelihood    1-5   (1 = very unlikely, 5 = expected)
  impact        1-5   (1 = annoying, 5 = kills the plan)
  reversible    yes / no   (no = cannot be undone cheaply; score x1.5)
  tripwire      the observable early signal + threshold ("fewer than 20 preorders by day 10")
  mitigation    what you do now to lower likelihood or impact
  owner         who watches the tripwire

Score = likelihood x impact, x1.5 if not reversible. Bands:
  >= 15 CRITICAL (fix or reshape the plan before starting)
  8-14  WATCH    (needs a tripwire and an owner)
  < 8   ACCEPT   (note it, move on)

Exit code 1 if any CRITICAL risk has no mitigation, or any CRITICAL/WATCH risk
has no tripwire or no owner, so the check can gate a plan.
Stdlib only.
"""
import argparse
import csv
import sys
from pathlib import Path


def band(score):
    return "CRITICAL" if score >= 15 else "WATCH" if score >= 8 else "ACCEPT"


def to_int(value, field, row_no):
    try:
        v = int(str(value).strip())
    except ValueError:
        sys.exit(f"row {row_no}: {field} must be 1-5, got {value!r}")
    if not 1 <= v <= 5:
        sys.exit(f"row {row_no}: {field} must be 1-5, got {v}")
    return v


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--top", type=int, default=0, help="show only the N highest")
    p.add_argument("--md", action="store_true", help="print a markdown table")
    a = p.parse_args()

    rows = []
    with open(Path(a.csv), newline="", encoding="utf-8-sig") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
            if not r.get("risk"):
                continue
            lk = to_int(r.get("likelihood"), "likelihood", i)
            im = to_int(r.get("impact"), "impact", i)
            irreversible = r.get("reversible", "yes").lower() in ("no", "n", "false", "0")
            score = lk * im * (1.5 if irreversible else 1)
            r.update(score=score, band=band(score), irreversible=irreversible)
            rows.append(r)
    if not rows:
        sys.exit("no risks found (need a 'risk' column)")
    rows.sort(key=lambda r: -r["score"])
    show = rows[: a.top] if a.top else rows

    problems = []
    for r in rows:
        if r["band"] == "CRITICAL" and not r.get("mitigation"):
            problems.append(f"CRITICAL with no mitigation: {r['risk']}")
        if r["band"] in ("CRITICAL", "WATCH"):
            if not r.get("tripwire"):
                problems.append(f"{r['band']} with no tripwire: {r['risk']}")
            if not r.get("owner"):
                problems.append(f"{r['band']} with no owner: {r['risk']}")

    if a.md:
        print("| # | Risk | L | I | Rev | Score | Band | Tripwire | Owner |")
        print("|---|---|---|---|---|---|---|---|---|")
        for n, r in enumerate(show, 1):
            print(f"| {n} | {r['risk']} | {r['likelihood']} | {r['impact']} | "
                  f"{'no' if r['irreversible'] else 'yes'} | {r['score']:g} | {r['band']} | "
                  f"{r.get('tripwire') or '-'} | {r.get('owner') or '-'} |")
    else:
        for n, r in enumerate(show, 1):
            print(f"{n:>2}. [{r['band']:<8}] {r['score']:>5g}  {r['risk']}")
            if r.get("tripwire"):
                print(f"              tripwire: {r['tripwire']}")
    counts = {b: sum(1 for r in rows if r["band"] == b) for b in ("CRITICAL", "WATCH", "ACCEPT")}
    print(f"\n{len(rows)} risks: {counts['CRITICAL']} critical, {counts['WATCH']} watch, {counts['ACCEPT']} accept")
    if problems:
        print("\nGAPS:")
        print("\n".join("  - " + x for x in problems))
        sys.exit(1)
    print("every critical risk has a mitigation; every critical/watch risk has a tripwire and owner")


if __name__ == "__main__":
    main()
