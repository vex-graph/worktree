#!/bin/sh
# tools/shell/ci.sh — run the CI gate locally, before a push spends a runner.
#
# Mirrors the `audit` job of .github/workflows/ci.yml step for step, plus a
# workflow-reference check that resolves moved paths and retired runner labels
# without a runner. The six-target build matrix (job 3) is deliberately absent:
# it needs six platforms, and it is gated behind this job anyway.
#
#   tools/shell/ci.sh
#
# Every step runs, so one pass shows every broken gate; the exit status is
# nonzero if any failed. Read-only: nothing here writes to the tree.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/../.." && pwd)
cd "$root"

python=python3
command -v python3 >/dev/null 2>&1 || python=python

log=$(mktemp "${TMPDIR:-/tmp}/vexgraph-ci.XXXXXX")
trap 'rm -f "$log"' EXIT INT TERM

failed=0
step() {
    name=$1
    shift
    printf '  %-42s' "$name"
    if "$@" >"$log" 2>&1; then
        printf 'PASS\n'
    else
        printf 'FAIL\n'
        sed 's/^/      /' "$log"
        failed=1
    fi
}

tooling_tests() {
    "$python" -B vexgraph-ecosystem/tests/tools/linter_test.py &&
    "$python" -B vexgraph-ecosystem/tests/tools/arrange_test.py &&
    "$python" -B vexgraph-ecosystem/tests/tools/readiness_test.py &&
    "$python" -B vexgraph-ecosystem/tests/tools/test_checklist_test.py &&
    "$python" -B vexgraph-ecosystem/tests/tools/ci_repos_test.py &&
    "$python" -B vexgraph-ecosystem/tests/tools/prefs_test.py
}

secret_scan() {
    ! git grep -E -i "BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY" \
        -- ':(exclude)_notes/' ':(exclude)_trash/'
}

echo "Local CI gate"
step "workflow references"  "$python" -B tools/python/workflow_refs.py check
step "declared checkouts"   "$python" -B tools/python/ci_repos.py check --require-all
step "tooling tests"        tooling_tests
step "preferences integrity" ./tools/prefs check
step "checklist ledger"     "$python" -B tools/python/test_checklist.py check
step "secret scan"          secret_scan

# CI tests `origin`, never this working tree. A green local gate on commits that
# were never pushed is the exact red run this script exists to prevent, so the
# gap is reported here rather than discovered on GitHub.
gap=$("$python" -c 'import json
repos = json.load(open("tools/platforms.json"))["repos"]
print(" ".join("." if key == "(worktree)" else key for key in repos))')

ahead_report=""
for repo in $gap; do
    [ -d "$repo/.git" ] || continue
    count=$(git -C "$repo" rev-list --count '@{u}..HEAD' 2>/dev/null || echo 0)
    [ "$count" = "0" ] && continue
    ahead_report="$ahead_report
    $repo: $count commit(s) ahead of origin"
done

if [ -n "$ahead_report" ]; then
    echo
    echo "  Publish gap — CI has not seen these commits:$ahead_report"
    echo "  Push nested repositories before the root; the root CI clones them."
fi

echo
if [ "$failed" -ne 0 ]; then
    echo "Gate failed. Fix the failing steps above; CI would reject this tree."
    exit 1
fi
echo "Gate passed. Remaining risk is platform-specific: the Windows and macOS legs."
