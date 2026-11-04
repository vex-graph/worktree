#!/bin/sh
# tools/shell/test.sh — run owner-test units through b.
#
# A test is a directory carrying a b.assembly.json under vex/<repo>/test/.
# b owns exactly one unit: `b run` inside that directory builds it and executes
# it. This script owns the policy b deliberately refuses to hold — which units
# exist, which ones a filter selects, and how a run is reported.
#
# A unit's exit status means:
#   0                     passed
#   77 (B_TEST_SKIP)      declined to run (no loopback port, no keychain, ...)
#   anything else         failed
#
#   tools/shell/test.sh                every unit
#   tools/shell/test.sh vexspoke       units whose path contains "vexspoke"
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "$here" in
    */scripts|*/shell) root=$(CDPATH= cd -- "$here/../.." && pwd) ;;
    *)                 root=$(CDPATH= cd -- "$here/.." && pwd) ;;
esac

cd "$root"

launcher="$root/tools/b"
if [ ! -x "$launcher" ]; then
    echo "test.sh: b launcher not found or not executable: $launcher" >&2
    echo "test.sh: build it with 'cd vex/b && ./b.sh'" >&2
    exit 1
fi

filter="${1:-}"
passed=0
skipped=0
failed=0
failures=""

for manifest in $(find vex -name b.assembly.json -not -path '*/.b/*' -not -path '*/.git/*' | sort); do
    unit=$(dirname "$manifest")
    case "$unit" in
        */test|*/test/*) ;;
        *) continue ;;
    esac
    if [ -n "$filter" ]; then
        case "$unit" in
            *"$filter"*) ;;
            *) continue ;;
        esac
    fi

    printf '  %-58s' "${unit#vex/}"
    log=$(mktemp "${TMPDIR:-/tmp}/vex-test.XXXXXX")
    if ( cd "$unit" && "$launcher" run ) >"$log" 2>&1; then
        status=0
    else
        status=$?
    fi
    case "$status" in
        0)
            printf 'PASS\n'
            passed=$((passed + 1))
            ;;
        77)
            printf 'SKIP\n'
            skipped=$((skipped + 1))
            ;;
        *)
            printf 'FAIL (exit %s)\n' "$status"
            sed 's/^/      /' "$log"
            failed=$((failed + 1))
            failures="$failures
    $unit"
            ;;
    esac
    rm -f "$log"
done

echo
if [ "$failed" -ne 0 ]; then
    echo "  $passed passed, $skipped skipped, $failed failed$failures"
    exit 1
fi
echo "  $passed passed, $skipped skipped, 0 failed"
