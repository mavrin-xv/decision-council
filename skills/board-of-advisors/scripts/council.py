#!/usr/bin/env python3
"""Blind peer review helper for an advisor council.

The model writes the advisor answers and the reviews. This script does the two
parts a model is bad at doing honestly: hiding who wrote what, and counting votes.

Usage:
  python council.py shuffle answers.json [--seed N] [--out-dir DIR]
      answers.json = {"question": "...", "answers": {"Contrarian": "text", ...}}
      Writes DIR/packet.md (answers relabelled A, B, C... in random order, roles
      removed) and DIR/mapping.json (label -> role). Give reviewers packet.md only.

  python council.py tally reviews.json --mapping DIR/mapping.json
      reviews.json = [{"reviewer": "R1", "ranking": ["C","A","E","B","D"],
                       "strongest": "C", "blind_spot": "B", "all_missed": "text"}, ...]
      Prints a Borda score per answer (first place = n-1 points), strongest and
      blind-spot votes, the roles revealed, and every "all_missed" line. Exits 2
      if a review ranks a label that does not exist or skips one.

  python council.py --help

Stdlib only. Same seed + same input = same labels, so a run can be reproduced.
"""
import argparse
import json
import random
import string
import sys
from pathlib import Path


def shuffle(args):
    data = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    answers = data.get("answers") or {}
    if len(answers) < 2:
        sys.exit("need at least 2 answers to review blind")
    roles = list(answers)
    rng = random.Random(args.seed)
    rng.shuffle(roles)
    labels = string.ascii_uppercase[: len(roles)]
    mapping = dict(zip(labels, roles))
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# Blind review packet", ""]
    if data.get("question"):
        lines += ["**Question:** " + data["question"].strip(), ""]
    lines += [
        "You are reviewing anonymous answers. One of them may be yours; judge it like the others.",
        "Answer three things: which answer has the strongest insight and why, which has the most",
        "serious blind spot, and what all of them missed. Then rank every label best to worst.",
        "",
    ]
    for label in labels:
        lines += [f"## Answer {label}", "", answers[mapping[label]].strip(), ""]
    (out / "packet.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "mapping.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"wrote {out / 'packet.md'} ({len(labels)} answers) and {out / 'mapping.json'}")
    print("give reviewers packet.md only; keep mapping.json away from them")


def tally(args):
    reviews = json.loads(Path(args.reviews).read_text(encoding="utf-8"))
    mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8"))
    labels = sorted(mapping)
    n = len(labels)
    score = {l: 0 for l in labels}
    strongest = {l: 0 for l in labels}
    blind = {l: 0 for l in labels}
    missed, bad = [], []
    for r in reviews:
        who = r.get("reviewer", "?")
        rank = [x.strip().upper() for x in r.get("ranking", [])]
        if sorted(rank) != labels:
            bad.append(f"{who}: ranking {rank} must list each of {labels} once")
            continue
        for pos, label in enumerate(rank):
            score[label] += n - 1 - pos
        s, b = (r.get("strongest") or "").upper(), (r.get("blind_spot") or "").upper()
        if s in strongest:
            strongest[s] += 1
        if b in blind:
            blind[b] += 1
        if r.get("all_missed"):
            missed.append(f"{who}: {r['all_missed'].strip()}")
    if bad:
        print("\n".join("INVALID " + x for x in bad))
        sys.exit(2)
    order = sorted(labels, key=lambda l: (-score[l], -strongest[l], blind[l]))
    print(f"{'label':<6}{'role':<26}{'borda':>6}{'strongest':>11}{'blind spot':>12}")
    for l in order:
        print(f"{l:<6}{mapping[l]:<26}{score[l]:>6}{strongest[l]:>11}{blind[l]:>12}")
    top = order[0]
    print(f"\ntop answer: {top} ({mapping[top]}), {score[top]} of {(n - 1) * len(reviews)} possible points")
    contested = [l for l in labels if strongest[l] and blind[l]]
    if contested:
        print("contested (voted both strongest and blind spot): " +
              ", ".join(f"{l} ({mapping[l]})" for l in contested))
    if missed:
        print("\nwhat all of them missed, per reviewer:")
        print("\n".join("  - " + m for m in missed))
    print("\nThe chairman weighs arguments, not this score. Use it to spot where the room split.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("shuffle", help="anonymise answers into a review packet")
    a.add_argument("answers")
    a.add_argument("--seed", type=int, default=None)
    a.add_argument("--out-dir", default="council-run")
    a.set_defaults(fn=shuffle)
    t = sub.add_parser("tally", help="count blind peer review votes")
    t.add_argument("reviews")
    t.add_argument("--mapping", required=True)
    t.set_defaults(fn=tally)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
