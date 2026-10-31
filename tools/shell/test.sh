#!/bin/sh
# tools/shell/test.sh — Vexgraph test runner.
# A test is a b unit under vexgraph-ecosystem/tests whose workspace kind is "app".
# b owns no test policy; this script chooses the tests, runs each one through b,
# and reports the results.
#   tools/shell/test.sh [substring]
#   tools/shell/test.sh preferences
#   tools/shell/test.sh opencode_preferences | checklist_runner | linter | readiness | ci_repos | arrange | prefs
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "$here" in
    */scripts|*/shell) root=$(CDPATH= cd -- "$here/../.." && pwd) ;;
    *)                 root=$(CDPATH= cd -- "$here/.." && pwd) ;;
esac

cd "$root"
export B_CALLER_DIR="${B_CALLER_DIR:-$PWD}"
export B_HOME="${B_HOME:-$HOME/Library/Application Support/vexgraph/b}"

run_tooling_test() {
    case "$1" in
        opencode_preferences)
            bun test "$root/vexgraph-ecosystem/tests/tools/opencode_preferences_test.ts"
            ;;
        checklist_runner)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/test_checklist_test.py"
            ;;
        linter)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/linter_test.py"
            ;;
        readiness)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/readiness_test.py"
            ;;
        ci_repos)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/ci_repos_test.py"
            ;;
        arrange)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/arrange_test.py"
            ;;
        prefs)
            python3 -B "$root/vexgraph-ecosystem/tests/tools/prefs_test.py"
            ;;
        *)
            return 2
            ;;
    esac
}

case "${1:-}" in
    opencode_preferences|checklist_runner|linter|readiness|ci_repos|arrange|prefs)
        run_tooling_test "$1"
        exit $?
        ;;
    preferences)
        run_tooling_test opencode_preferences \
            && run_tooling_test checklist_runner \
            && run_tooling_test linter \
            && run_tooling_test readiness \
            && run_tooling_test ci_repos \
            && run_tooling_test arrange \
            && run_tooling_test prefs
        exit $?
        ;;
esac

filter="${1:-}"
launcher="$root/vexgraph-hobby-projects/b/b"
if [ ! -x "$launcher" ]; then
    echo "test.sh: b launcher not found or not executable: $launcher" >&2
    exit 1
fi

log_dir="$B_HOME/logs"
mkdir -p "$log_dir"

VEX_ROOT="$root" VEX_FILTER="$filter" VEX_B="$launcher" VEX_LOGS="$log_dir" python3 - <<'PY'
import json
import os
import subprocess
import sys

root = os.environ["VEX_ROOT"]
filter_str = os.environ["VEX_FILTER"]
launcher = os.environ["VEX_B"]
log_dir = os.environ["VEX_LOGS"]
reg_file = os.path.join(root, ".b/workspace.json")
if not os.path.isfile(reg_file):
    print("test.sh: no .b/workspace.json; run b generate at the repo root first", file=sys.stderr)
    sys.exit(1)

with open(reg_file) as f:
    data = json.load(f)

tests_prefix = "vexgraph-ecosystem/tests"
ENTRY_MARKERS = ("int main(", "fn main(")

def under_tests(directory):
    return directory == tests_prefix or directory.startswith(tests_prefix + "/")

def entry_source(unit):
    for name in unit.get("sources", []):
        path = os.path.join(root, unit["dir"], name)
        try:
            with open(path, "r", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        if any(marker in text for marker in ENTRY_MARKERS):
            return path
    return None

tests = []
for unit in data.get("units", []):
    if unit.get("kind") != "app" or not under_tests(unit["dir"]):
        continue
    if filter_str and filter_str not in unit["dir"]:
        continue
    tests.append(unit)

if not tests:
    print(f"test.sh: no tests match '{filter_str}'")
    sys.exit(0)

print(f"test.sh: running {len(tests)} test(s)")

passed = 0
failed = 0
skipped = 0
timedout = 0

for unit in tests:
    label = unit["dir"].replace("/", "_")
    shown = unit["dir"]
    entry = entry_source(unit)
    if entry is None:
        print(f"  FAIL    {shown} (no entry source)")
        failed += 1
        continue

    log_path = os.path.join(log_dir, f"test_{label}.log")
    try:
        with open(log_path, "w") as log_file:
            res = subprocess.run([launcher, "run", entry], cwd=root,
                                 stdout=log_file, stderr=subprocess.STDOUT, timeout=60)
            st = res.returncode
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT {shown} (>60s)")
        timedout += 1
        continue

    if st == 0:
        print(f"  PASS    {shown}")
        passed += 1
    elif st == 77:
        print(f"  SKIP    {shown} (contract unproved on this host)")
        skipped += 1
    else:
        print(f"  FAIL    {shown} (exit {st})")
        failed += 1
        with open(log_path, "r", errors="replace") as lf:
            sys.stdout.write("".join(lf.readlines()[-12:]))

print(f"test.sh: {passed} passed, {failed} failed, {timedout} timed out, {skipped} skipped")

if filter_str == "" and failed == 0 and timedout == 0:
    print("test.sh: running tooling tests...")
    subprocess.run(["bun", "test", os.path.join(root, "vexgraph-ecosystem/tests/tools/opencode_preferences_test.ts")], check=True)
    subprocess.run(["python3", "-B", os.path.join(root, "vexgraph-ecosystem/tests/tools/test_checklist_test.py")], check=True)

sys.exit(1 if (failed or timedout) else 0)
PY
