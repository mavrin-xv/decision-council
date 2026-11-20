#!/usr/bin/env python3
"""Pick the cheapest method that fits a decision's stakes.

Usage:
  python triage.py --cost-if-wrong N --reversible yes|no --type T [--variables N] [--ready]
  python triage.py --help

  --cost-if-wrong  rough cost of a wrong call in working days (money: divide by a day's cost)
  --reversible     can it be undone within a week for little cost?
  --type           decision | marketing | plan | claim | built
                     decision  = whether to do something (product, price, pivot, hire)
                     marketing = how to reach and convince buyers (channel, message, campaign)
                     plan      = a plan with dates and budget that is about to start
                     claim     = one confident sentence a choice rests on
                     built     = something claimed done / ready / working
  --variables      moving parts (price, audience, timing, channel, team...). default 3
  --ready          the artifact (page, offer, flow) exists and is about to ship

Prints the method sequence and the expected model calls. Stdlib only.
"""
import argparse

CALLS = {"doubt loop (pre-mortem claim mode)": 2, "pre-mortem plan mode": 4,
         "board-of-advisors": 11, "marketing-council": 17, "stress-test": 6,
         "reality-check": 1, "decision-log": 0}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cost-if-wrong", type=float, required=True)
    p.add_argument("--reversible", choices=["yes", "no"], required=True)
    p.add_argument("--type", choices=["decision", "marketing", "plan", "claim", "built"], required=True)
    p.add_argument("--variables", type=int, default=3)
    p.add_argument("--ready", action="store_true")
    a = p.parse_args()

    stakes = a.cost_if_wrong * (2 if a.reversible == "no" else 1)
    tier = "low" if stakes < 2 else "high" if stakes >= 10 or a.variables >= 4 else "mid"
    seq = []
    if a.type == "built":
        seq = ["reality-check"]
    elif a.type == "claim":
        seq = ["doubt loop (pre-mortem claim mode)"]
    elif a.type == "plan":
        seq = ["pre-mortem plan mode"] + (["doubt loop (pre-mortem claim mode)"] if tier != "low" else [])
    elif tier == "low":
        seq = ["doubt loop (pre-mortem claim mode)"]
    else:
        seq = ["marketing-council" if a.type == "marketing" else "board-of-advisors"]
        if tier == "high":
            seq.append("pre-mortem plan mode")
    if a.ready and "stress-test" not in seq:
        seq.append("stress-test")
    if tier != "low" or a.reversible == "no":
        seq.append("decision-log")

    print(f"stakes: {stakes:g} (tier {tier}, {'irreversible' if a.reversible == 'no' else 'reversible'}, "
          f"{a.variables} moving parts)")
    print("run, in order:")
    for i, s in enumerate(seq, 1):
        print(f"  {i}. {s}")
    print(f"approx. model calls: {sum(CALLS[s] for s in seq)}")
    if tier == "low":
        print("low stakes: a full council costs more than a wrong call. Decide, set a check date, move on.")


if __name__ == "__main__":
    main()
