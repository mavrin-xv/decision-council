#!/usr/bin/env python3
"""Turn a claims-vs-evidence checklist into a readiness status.

Usage:
  python evidence_check.py checklist.md
  python evidence_check.py --help

checklist.md: one claim per list line, in this shape:
  - [x] Checkout works on mobile | evidence: screenshot-mobile-checkout.png
  - [ ] Confirmation email arrives | evidence:
  - [x] Handles empty cart | evidence: "tested by hand"
  - [!] Refund flow | evidence: returns 500 on second refund
Markers: [x] verified, [ ] not verified, [!] verified and FAILED.
Lines starting with "  - (must)" or containing "(must)" are must-pass claims.

Rules (default stance is NEEDS WORK):
  APPROVED                 every claim [x] with evidence, nothing failed
  CONDITIONALLY APPROVED   all (must) claims [x] with evidence, some others open
  NEEDS WORK               anything else
Evidence that is only words like "works", "tested", "looks fine", "ok", "done"
does not count: it must name an artifact (file, link, log line, number, message id).
Exit 0 for APPROVED, 1 otherwise. Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

WEAK = re.compile(r"^\W*(works?|tested( by hand)?|looks (fine|good)|ok(ay)?|done|yes|checked|fine|should work)\W*$", re.I)
LINE = re.compile(r"^\s*[-*]\s*\[( |x|X|!)\]\s*(.+?)(?:\|\s*evidence:\s*(.*))?$")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("checklist")
    a = p.parse_args()
    claims = []
    for raw in Path(a.checklist).read_text(encoding="utf-8").splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        mark, text, ev = m.group(1).lower(), m.group(2).strip(), (m.group(3) or "").strip()
        must = "(must)" in text.lower()
        weak = bool(ev) and bool(WEAK.match(ev.strip('"\'')))
        state = "failed" if mark == "!" else "verified" if mark == "x" and ev and not weak else \
            "weak-evidence" if mark == "x" and weak else "unverified"
        claims.append((state, must, text.replace("(must)", "").strip(), ev))
    if not claims:
        sys.exit("no checklist lines found (format: - [x] claim | evidence: ...)")

    ok = [c for c in claims if c[0] == "verified"]
    musts = [c for c in claims if c[1]]
    failed = [c for c in claims if c[0] == "failed"]
    if not failed and len(ok) == len(claims):
        status = "APPROVED"
    elif not failed and musts and all(c[0] == "verified" for c in musts):
        status = "CONDITIONALLY APPROVED"
    else:
        status = "NEEDS WORK"

    tag = {"verified": "OK  ", "failed": "FAIL", "weak-evidence": "WEAK", "unverified": "OPEN"}
    for state, must, text, ev in claims:
        print(f"{tag[state]} {'(must) ' if must else ''}{text}" + (f"  <- {ev}" if ev else ""))
    print(f"\n{len(ok)}/{len(claims)} verified, {len(failed)} failed, "
          f"{sum(c[0] == 'weak-evidence' for c in claims)} with words instead of evidence")
    print(f"STATUS: {status}")
    if status == "CONDITIONALLY APPROVED":
        print("conditions: " + "; ".join(c[2] for c in claims if c[0] != "verified"))
    sys.exit(0 if status == "APPROVED" else 1)


if __name__ == "__main__":
    main()
