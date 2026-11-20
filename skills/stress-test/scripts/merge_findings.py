#!/usr/bin/env python3
"""Merge persona findings from a stress test into one ranked report with a verdict.

Usage:
  python merge_findings.py findings.json [--md]
  python merge_findings.py --help

findings.json = [
  {"persona": "Skeptical buyer", "trust": 4,
   "issues": [{"severity": "critical", "quote": "exact words from the target",
               "problem": "why it hurts", "fix": "specific change"}]},
  ...
]
severity: critical | major | minor

Issues from different personas that quote the same text (case and spacing
ignored, or one quote contains the other) are merged and list every persona
that found them; an issue found by 2+ personas moves up within its severity.

Verdict rule:
  any critical                         -> REWORK if 3+ criticals, else REVISE
  no critical, 3+ major or avg trust<6 -> REVISE
  otherwise                            -> SHIP
Exit code 0 for SHIP, 1 for REVISE / REWORK. Stdlib only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RANK = {"critical": 0, "major": 1, "minor": 2}


def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip(" .\"'")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("findings")
    p.add_argument("--md", action="store_true")
    a = p.parse_args()
    data = json.loads(Path(a.findings).read_text(encoding="utf-8"))

    merged, trust = [], {}
    for block in data:
        persona = block.get("persona", "?")
        if block.get("trust") is not None:
            trust[persona] = float(block["trust"])
        for it in block.get("issues", []):
            sev = (it.get("severity") or "minor").lower()
            if sev not in RANK:
                sys.exit(f"{persona}: unknown severity {sev!r}")
            q = norm(it.get("quote"))
            hit = None
            for m in merged:
                mq = m["key"]
                if q and mq and (q == mq or q in mq or mq in q):
                    hit = m
                    break
            if hit:
                hit["personas"].append(persona)
                if RANK[sev] < RANK[hit["severity"]]:
                    hit["severity"] = sev
                hit["fixes"].append(it.get("fix", ""))
            else:
                merged.append({"key": q, "quote": it.get("quote", ""), "severity": sev,
                               "problem": it.get("problem", ""), "personas": [persona],
                               "fixes": [it.get("fix", "")]})
    merged.sort(key=lambda m: (RANK[m["severity"]], -len(m["personas"])))
    c = sum(m["severity"] == "critical" for m in merged)
    mj = sum(m["severity"] == "major" for m in merged)
    avg = sum(trust.values()) / len(trust) if trust else 10
    verdict = "REWORK" if c >= 3 else "REVISE" if c or mj >= 3 or avg < 6 else "SHIP"

    for sev in ("critical", "major", "minor"):
        items = [m for m in merged if m["severity"] == sev]
        if not items:
            continue
        print(f"\n{'## ' if a.md else ''}{sev.upper()} ({len(items)})")
        for m in items:
            who = ", ".join(dict.fromkeys(m["personas"]))
            fix = next((f for f in m["fixes"] if f), "-")
            print(f"- \"{m['quote']}\": {m['problem']} [found by {who}]")
            print(f"  fix: {fix}")
    print(f"\n{'## ' if a.md else ''}TRUST")
    for k, v in trust.items():
        print(f"- {k}: {v:g}/10")
    print(f"- average: {avg:.1f}/10")
    print(f"\nVERDICT: {verdict} ({c} critical, {mj} major, {len(merged) - c - mj} minor)")
    sys.exit(0 if verdict == "SHIP" else 1)


if __name__ == "__main__":
    main()
