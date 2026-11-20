#!/usr/bin/env bash
# decision-council installer: copies the skills (and slash commands) into Claude Code.
#
#   ./install.sh             into ~/.claude/skills and ~/.claude/commands (all projects)
#   ./install.sh --project   into ./.claude/skills and ./.claude/commands (this project only)
#   ./install.sh --no-commands   skills only
#
# Existing skills with the same name are backed up to <name>.bak.<timestamp> first.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"; CMDS=1
for a in "$@"; do
  case "$a" in
    --project) DEST="$(pwd)/.claude" ;;
    --no-commands) CMDS=0 ;;
    -h|--help) sed -n 2,8p "$0"; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 1 ;;
  esac
done

mkdir -p "$DEST/skills"
for s in "$HERE"/skills/*/; do
  name="$(basename "$s")"
  if [ -d "$DEST/skills/$name" ]; then
    mv "$DEST/skills/$name" "$DEST/skills/$name.bak.$(date +%s)"
    echo "backed up existing $name"
  fi
  cp -R "$s" "$DEST/skills/$name"
  echo "installed skill $name"
done
for k in decide board-of-advisors marketing-council; do cp -R "$HERE/templates" "$DEST/skills/$k/"; done

if [ "$CMDS" = 1 ]; then
  mkdir -p "$DEST/commands"
  for c in "$HERE"/commands/*.md; do cp "$c" "$DEST/commands/"; echo "installed /$(basename "$c" .md)"; done
fi

command -v python3 >/dev/null || command -v python >/dev/null || \
  echo "note: the helper scripts need Python 3.8+; the skills work without them, by hand."
echo "done. Try: /decide should we raise our price from \$12 to \$18?"
