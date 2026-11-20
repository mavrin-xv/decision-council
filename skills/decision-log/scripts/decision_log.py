#!/usr/bin/env python3
"""A small decision log in plain markdown files: record, review, and catch repeats.

Each decision is one file DIR/YYYY-MM-DD-slug.md with a simple header block.
Statuses: active | killed (do not resurface) | reversed | superseded.

Usage:
  python decision_log.py add --title "Raise price to $18" --decision "..." \
      [--why ...] [--risk ...] [--kill-if ...] [--review-on YYYY-MM-DD] \
      [--confidence N] [--method board-of-advisors] [--status active|killed] [--tags a,b]
      [--date YYYY-MM-DD]   (default today)
  python decision_log.py list [--status active]
  python decision_log.py due [--today YYYY-MM-DD]      decisions whose review date has passed
  python decision_log.py check "text of a new proposal"  finds related past decisions,
                                                        warns loudly on killed ones (exit 3)
  python decision_log.py review FILE --outcome "what happened" [--status reversed]
  python decision_log.py brief [--max 20]               short list of active + killed for
                                                        loading into an agent's context
Global: --dir DIR (default ./decisions, or env DECISION_LOG_DIR)

Stdlib only. Files stay human-editable; the script only reads "key: value" header lines.
"""
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

FIELDS = ["title", "date", "status", "decision", "why", "risk", "kill_if", "review_on",
          "confidence", "method", "tags", "outcome"]
STOP = set("a an the to of and or for in on at with we our is are be by it this that from as "
           "do not no should will can new more less".split())


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50] or "decision"


def read(path):
    meta, body = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- \*\*(\w+):\*\* ?(.*)$", line)
        if line.startswith("# ") and "title" not in meta:
            meta["title"] = line[2:].strip()
        elif m and m.group(1) in FIELDS:
            meta[m.group(1)] = m.group(2).strip()
        else:
            body.append(line)
    meta["file"] = path.name
    return meta


def write(path, meta, extra=""):
    lines = [f"# {meta.get('title', 'Decision')}", ""]
    for k in FIELDS:
        if k != "title" and meta.get(k):
            lines.append(f"- **{k}:** {meta[k]}")
    if extra:
        lines += ["", extra]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load(d):
    return [read(p) for p in sorted(d.glob("*.md")) if p.name.lower() != "readme.md"]


def words(s):
    return {w for w in re.findall(r"[a-z0-9$]+", s.lower()) if w not in STOP and len(w) > 2}


def cmd_add(a, d):
    d.mkdir(parents=True, exist_ok=True)
    today = a.date or dt.date.today().isoformat()
    meta = {"title": a.title, "date": today, "status": a.status, "decision": a.decision,
            "why": a.why, "risk": a.risk, "kill_if": a.kill_if, "review_on": a.review_on,
            "confidence": a.confidence, "method": a.method, "tags": a.tags}
    if a.status == "active" and not a.kill_if:
        print("warning: no --kill-if. A decision without a stop condition cannot be reviewed.")
    if a.status == "active" and not a.review_on:
        print("warning: no --review-on date. It will never show up in 'due'.")
    path = d / f"{today}-{slug(a.title)}.md"
    write(path, {k: v for k, v in meta.items() if v})
    print(f"logged {path}")


def cmd_list(a, d):
    for m in load(d):
        if a.status and m.get("status") != a.status:
            continue
        print(f"{m.get('date', '?'):<11} {m.get('status', '?'):<11} {m.get('title', m['file'])}"
              + (f"  (review {m['review_on']})" if m.get("review_on") else ""))


def cmd_due(a, d):
    today = a.today or dt.date.today().isoformat()
    due = [m for m in load(d) if m.get("status") == "active" and m.get("review_on")
           and m["review_on"] <= today and not m.get("outcome")]
    for m in due:
        print(f"DUE {m['review_on']}  {m.get('title')}  kill if: {m.get('kill_if', '-')}  [{m['file']}]")
    print(f"{len(due)} decision(s) due for review" if due else "nothing due")


def cmd_check(a, d):
    q = words(a.text)
    hits = []
    for m in load(d):
        w = words(" ".join(m.get(k, "") for k in ("title", "decision", "tags", "why")))
        overlap = q & w
        if len(overlap) >= 2 or (overlap and len(q) <= 3):
            hits.append((len(overlap), m, overlap))
    hits.sort(key=lambda x: -x[0])
    killed = False
    for n, m, ov in hits[:8]:
        flag = "KILLED, do not resurface" if m.get("status") == "killed" else m.get("status", "?")
        killed |= m.get("status") == "killed"
        print(f"[{flag}] {m.get('date')} {m.get('title')}: {m.get('decision', '')}")
        print(f"    shared words: {', '.join(sorted(ov))}  [{m['file']}]")
    if not hits:
        print("no related decisions found")
    if killed:
        print("\nThis proposal matches a killed decision. Surface the conflict to the user before acting.")
        sys.exit(3)


def cmd_review(a, d):
    path = d / a.file if not Path(a.file).exists() else Path(a.file)
    meta = read(path)
    meta["outcome"] = f"{dt.date.today().isoformat()}: {a.outcome}"
    if a.status:
        meta["status"] = a.status
    write(path, meta)
    print(f"updated {path}")


def cmd_brief(a, d):
    ms = load(d)
    act = [m for m in ms if m.get("status") == "active"][-a.max:]
    kil = [m for m in ms if m.get("status") == "killed"]
    print("# Decisions in force")
    for m in act:
        print(f"- [{m.get('date')}] {m.get('title')}: {m.get('decision', '')}")
    print("\n# Do not resurface")
    for m in kil:
        print(f"- [{m.get('date')}] {m.get('title')}: {m.get('why', '')}")
    if len([m for m in ms if m.get('status') == 'active']) > a.max:
        print(f"\n(more than {a.max} active decisions: archive or supersede old ones)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dir", default=os.environ.get("DECISION_LOG_DIR", "decisions"))
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("--title", required=True)
    s.add_argument("--decision", required=True)
    for f in ("why", "risk", "kill-if", "review-on", "confidence", "method", "tags", "date"):
        s.add_argument("--" + f, default="")
    s.add_argument("--status", default="active", choices=["active", "killed", "reversed", "superseded"])
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("list"); s.add_argument("--status"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("due"); s.add_argument("--today"); s.set_defaults(fn=cmd_due)
    s = sub.add_parser("check"); s.add_argument("text"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("review"); s.add_argument("file"); s.add_argument("--outcome", required=True)
    s.add_argument("--status", choices=["active", "killed", "reversed", "superseded"]); s.set_defaults(fn=cmd_review)
    s = sub.add_parser("brief"); s.add_argument("--max", type=int, default=20); s.set_defaults(fn=cmd_brief)
    a = p.parse_args()
    a.fn(a, Path(a.dir))


if __name__ == "__main__":
    main()
