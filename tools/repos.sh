#!/usr/bin/env bash
# tools/repos.sh — one-pane cross-repo status for the active vexgraph repos.
# Local-only workspace helper (tools/ is git-ignored, never published).
# Prints branch, dirty count, ahead/behind vs upstream, and last commit.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPOS=(
  "$ROOT"
  "$ROOT"/ecosystem/repos/*
  "$ROOT"/ecosystem/projects/*
  "$ROOT/ecosystem/ecosystem"
  "$ROOT/ecosystem/.github"
  "$ROOT/tests"
  "$ROOT/personal/b"
  "$ROOT/personal/vex-graph"
)
printf "%-40s %-10s %-6s %-6s %-6s %s\n" REPO BRANCH DIRTY AHEAD BEHIND LAST
for d in "${REPOS[@]}"; do
  if [ ! -d "$d/.git" ] && [ ! -f "$d/.git" ]; then continue; fi
  name="${d#"$ROOT"/}"; [ "$name" = "$ROOT" ] && name="(root)"
  br=$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')
  dirty=$(git -C "$d" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  counts=$(git -C "$d" rev-list --left-right --count '@{upstream}...HEAD' 2>/dev/null || echo '? ?')
  behind=$(echo "$counts" | awk '{print $1}')
  ahead=$(echo "$counts" | awk '{print $2}')
  last=$(git -C "$d" log -1 --pretty='%h %s' 2>/dev/null | cut -c1-46)
  printf "%-40s %-10s %-6s %-6s %-6s %s\n" "$name" "$br" "$dirty" "$ahead" "$behind" "$last"
done
