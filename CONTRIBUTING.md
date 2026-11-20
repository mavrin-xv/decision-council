# Contributing

Thanks for helping. Small, tested changes are the easiest to merge.

## Good first contributions

- A new advisor frame or marketing specialist in `references/`, with a one-paragraph case where it changed a verdict.
- Domain persona swaps for `stress-test` (healthcare intake form, B2B procurement page, internal tool).
- A second worked example in `examples/` (invented business, every script run on it, outputs committed).
- Better keyword matching in `decision_log.py check`, still stdlib only.

## How

1. Open an issue first for anything that changes how a council runs (rounds, reviewer count, chairman rules).
2. Keep skills tool-agnostic: no hard dependency on one agent product, keys only through environment variables.
3. Run the commands listed in `AGENTS.md`. Paste their output in the PR.
4. Plain English. No hype words, no invented numbers. If a number is in the docs, say where it came from.

## Credit

If your change is based on someone else's method or repo, add it to the Credits section of the README with the URL and license.
