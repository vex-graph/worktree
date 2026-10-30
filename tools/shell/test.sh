#!/bin/sh
# tools/shell/test.sh — Vexgraph test runner: builds declared targets and runs tests.
# Usage:
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

# Build all targets first
"$root/tools/b" build

log_dir="$B_HOME/logs"
mkdir -p "$log_dir"

python3 - <<PY
import json
import os
import subprocess
import sys
import time

root = "$root"
filter_str = "$filter"
reg_file = os.path.join(root, ".b/workspace.json")
if not os.path.isfile(reg_file):
    print("test.sh: no .b/workspace.json found; run tools/b workspace first", file=sys.stderr)
    sys.exit(1)

with open(reg_file, "r") as f:
    data = json.load(f)

tests = [t["output"] for t in data.get("tests", []) if "output" in t]
if filter_str:
    tests = [t for t in tests if filter_str in os.path.basename(t)]

if not tests:
    print(f"test.sh: no tests match '{filter_str}'")
    sys.exit(0)

print(f"test.sh: running {len(tests)} test(s)")

passed = 0
failed = 0
skipped = 0
timedout = 0

for t_path in tests:
    full_path = os.path.join(root, t_path) if not os.path.isabs(t_path) else t_path
    name = os.path.basename(t_path)
    if not os.path.isfile(full_path) or not os.access(full_path, os.X_OK):
        print(f"  FAIL    {name} (binary not found: {full_path})")
        failed += 1
        continue

    log_path = os.path.join("$log_dir", f"test_{name}.log")
    try:
        with open(log_path, "w") as log_file:
            res = subprocess.run([full_path], stdout=log_file, stderr=subprocess.STDOUT, timeout=30)
            st = res.returncode
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT {name} (>30s)")
        timedout += 1
        continue

    if st == 0:
        print(f"  PASS    {name}")
        passed += 1
    elif st == 77:
        print(f"  SKIP    {name} (contract unproved on this host)")
        skipped += 1
    else:
        print(f"  FAIL    {name} (exit {st})")
        failed += 1
        if os.path.isfile(log_path):
            with open(log_path, "r", errors="replace") as lf:
                lines = lf.readlines()[-12:]
                sys.stdout.write("".join(lines))

print(f"test.sh: {passed} passed, {failed} failed, {timedout} timed out, {skipped} skipped")

if filter_str == "" and failed == 0 and timedout == 0:
    print("test.sh: running tooling tests...")
    subprocess.run(["bun", "test", f"{root}/vexgraph-ecosystem/tests/tools/opencode_preferences_test.ts"], check=True)
    subprocess.run(["python3", "-B", f"{root}/vexgraph-ecosystem/tests/tools/test_checklist_test.py"], check=True)

sys.exit(1 if (failed or timedout) else 0)
PY
