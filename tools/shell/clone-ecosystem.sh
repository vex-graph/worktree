#!/usr/bin/env bash
# tools/shell/clone-ecosystem.sh — reproduce the whole three-level workspace.
#
#   clone-ecosystem.sh <destination>              dry run: print every step
#   clone-ecosystem.sh <destination> --execute    do it
#
# From public sources only (GitHub and Gists), it builds:
#
#   <destination>/                      level 1 — the personal hub
#     metadata/gists/preferences/       the published constitution (Gist)
#     metadata/gists/test-checklist.md  the evidence ledger (Gist)
#     metadata/gists/readiness/         the readiness matrix (Gist)
#     metadata/gists/cookbook/          the function cookbook (Gist)
#     metadata/gists/BLOCKERS.md        blockers and deferred decisions (Gist)
#     metadata/vex-graph/               the profile/meta checkout
#     worktree/                         level 2 — the workspace repository
#       tools/                          the tools that run the whole thing
#       vex/<repo>/ ...                 level 3 — every manifest-declared
#                                       repository, cloned flat from
#                                       tools/platforms.json
#
# The manifest is the single source of what to clone; its keys are remote
# identities (org/repo), so each key lands at vex/<basename>. Deliberately
# not reproduced (per-person by design): harness configuration (.claude,
# .opencode, .idea), the agent bus, _notes. Uncommitted local material in an
# existing checkout is never imported — this builds the public shape only.
set -eu

here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
root="$(CDPATH= cd -- "$here/../.." && pwd)"
manifest="$root/tools/platforms.json"

WORKTREE_REMOTE="https://github.com/vex-graph/worktree.git"
PROFILE_REMOTE="https://github.com/vexgraph-dev/vexgraph-dev.git"
GIST_PREFS="4132a6c45cb6d3797c3e8eff2e94035a"
GIST_CHECKLIST="26f556f1a3a57b09d5c991d5ef9ef5ab"
GIST_READINESS="6943f92acb931b25dad1073c46da6ce7"
GIST_BLOCKERS="e921fa188eebbd0c68c4e59646109887"
GIST_COOKBOOK="0ade3bf94f5073607f5f7e7d459346bf"

dest="${1:-}"
mode="${2:-}"
if [ -z "$dest" ] || { [ -n "$mode" ] && [ "$mode" != "--execute" ]; }; then
    echo "usage: clone-ecosystem.sh <destination> [--execute]" >&2
    echo "  default is a dry run; --execute clones" >&2
    exit 2
fi
if [ -e "$dest" ] && [ -n "$(ls -A "$dest" 2>/dev/null)" ]; then
    echo "clone-ecosystem: destination exists and is not empty: $dest" >&2
    exit 1
fi
if [ ! -f "$manifest" ]; then
    echo "clone-ecosystem: manifest not found: $manifest" >&2
    exit 1
fi

clone() {  # clone <remote> <destination>
    if [ "$mode" = "--execute" ]; then
        git clone --depth 1 "$1" "$2"
    else
        printf 'would clone %s -> %s\n' "$1" "$2"
    fi
}

gist() {  # gist <id> <description>
    echo "would fetch gist $1 ($2)" >&2
    return 0
}

gist_execute() {  # gist_execute <id> <placement>
    id="$1"; placement="$2"
    tmp="$(mktemp -d)"
    git clone --depth 1 "https://gist.github.com/${id}.git" "$tmp/gist"
    case "$placement" in
        dir:*)
            target="$dest/metadata/gists/${placement#dir:}"
            mkdir -p "$target"
            mv "$tmp"/gist/* "$target"/
            ;;
        file:*)
            name="${placement#file:}"
            mkdir -p "$dest/metadata/gists"
            mv "$tmp"/gist/$name "$dest/metadata/gists/$name"
            ;;
        rename:BLOCKERS.md)
            mkdir -p "$dest/metadata/gists"
            mv "$tmp"/gist/blockers.md "$dest/metadata/gists/BLOCKERS.md"
            mv "$tmp"/gist/personal-agent-blockers.md "$dest/metadata/gists/"
            ;;
    esac
    rm -rf "$tmp"
}

# Level 2 — the workspace repository itself.
clone "$WORKTREE_REMOTE" "$dest/worktree"

# Level 3 — every manifest-declared repository, flat under vex/.
jq -r '.repos | to_entries[] | select(.key != "(worktree)") | [.key, .value.remote] | @tsv' "$manifest" |
while IFS=$'\t' read -r key remote; do
    name="${key##*/}"
    clone "$remote" "$dest/worktree/vex/$name"
done

# Level 1 — the hub's published material.
if [ "$mode" = "--execute" ]; then
    gist_execute "$GIST_PREFS" "dir:preferences"
    gist_execute "$GIST_CHECKLIST" "file:test-checklist.md"
    gist_execute "$GIST_READINESS" "dir:readiness"
    gist_execute "$GIST_BLOCKERS" "rename:BLOCKERS.md"
    gist_execute "$GIST_COOKBOOK" "dir:cookbook"
    clone "$PROFILE_REMOTE" "$dest/metadata/vex-graph"
else
    gist "$GIST_PREFS" "constitution -> metadata/gists/preferences/"
    gist "$GIST_CHECKLIST" "evidence ledger -> metadata/gists/test-checklist.md"
    gist "$GIST_READINESS" "readiness matrix -> metadata/gists/readiness/"
    gist "$GIST_BLOCKERS" "blockers -> metadata/gists/BLOCKERS.md"
    gist "$GIST_COOKBOOK" "cookbook -> metadata/gists/cookbook/"
    clone "$PROFILE_REMOTE" "$dest/metadata/vex-graph"
fi

echo
echo "clone-ecosystem: shape at $dest:"
echo "  metadata/gists/   published constitution, ledger, readiness, cookbook, blockers"
echo "  metadata/vex-graph/  profile/meta checkout"
echo "  worktree/         the workspace repository (level 2)"
echo "  worktree/vex/     every manifest-declared repository (level 3)"
echo "next: cd $dest/worktree && ./tools/orchestrator help && ./tools/prefs check"
echo "then: ./tools/prefs repo <name> before working in a repository"
