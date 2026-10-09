#!/usr/bin/env python3
"""Inventory and record executed evidence in tests/test-checklist.md."""

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import time


REPORT = Path("tests/test-checklist.md")
TITLE = "Timestamped Test Checklist Law"
HEADER = """# Ecosystem test checklist

Generated test report maintained by `python3 tools/test_checklist.py`.
Governed by the **Timestamped Test Checklist Law** in `preferences.md`.

- ✅ = an automated lab check passed for this exact file hash, in its stated scope.
- ❌ = untested, failed, skipped, or stale; see evidence. This is not a battle-tested claim.
- Last checked is actual Unix time: integer seconds since 1970-01-01T00:00:00Z.
  `—` means never checked. Estimates must never be recorded as executed evidence.
- The hash identifies the tested content. A file change invalidates a previous ✅;
  the old timestamp/evidence remains visible until the next executed check.
- The ledger tracks **executable tests only**: compilable/runnable test sources
  (`*_test.c/.m/.rs/.py`), registered runner scripts (`run.py`, `*_run.py`) and
  the shared test harness (`test_support.h`). Markdown, documentation, images,
  configuration and production source are deliberately excluded — a row exists
  to record a test that can actually run, not a file that never executes.
  This report alone is excluded to avoid a self-referential hash. A subsystem
  with no inventoried test is untested, not exempt.
- An integration pass only applies to explicitly named subjects and scope.
  Neither test-file presence nor a passing build proves every framework file.
- Platform gaps and omitted cases must be stated in the evidence/scope column.
- Visual appearance, interactive demos, and subjective approval are not tested
  by this ledger. The user performs visual checks and reports what is broken.
  Automated assertions (including numeric/pixel oracles) are lab evidence only,
  never visual approval. Do not launch galleries or manual demos to earn ✅.
- Descriptions explain the check; no author, agent name, or session ID is stored.

## Commands

```sh
python3 tools/test_checklist.py sync   # inventory executable tests; invalidate stale greens
python3 tools/test_checklist.py check  # reject missing rows or stale results
# Execute the test first, then record its executed test file:
python3 tools/test_checklist.py run --file tests/tools/test_checklist_test.py -- python3 -B tests/tools/test_checklist_test.py
```

`run` records only inventoried executable test files; naming a documented or
production file is rejected because those are not runnable tests.

`run` propagates failures; exit 77 is recorded as skipped, never green.
Add repeated `--file` arguments only for files actually exercised by the command.
Use `--scope` to describe proof limits, platform and gaps. A syntax check is only
syntax evidence, not runtime or full contract verification. Agents must read this
report before working and update affected rows in the same work cycle.
Use `--description` for a short explanation. Only `--kind lab` is recordable;
`--kind visual` is rejected before execution. Visual reports belong to the user.
Do not hand-edit generated tables; add files/tests and use `sync` or `run`.
"""


def inventory(root):
    """List executable test units (compilable/runnable tests, runners, harness).

    Documentation, configuration, images and production source are excluded by
    design: the ledger is a test-execution record, not a whole-tree inventory.
    """
    repos = {root, root / "tests", root / "b"}
    # Scan independently of the umbrella repo's ignores: nested repositories
    # own their inventory and their own ignore rules. .git may be a worktree file.
    for directory in ("ecosystem", "repos", "projects", "personal"):
        repos.update(p.parent for p in (root / directory).rglob(".git"))
    groups = {}
    for repo in sorted(repos):
        if not (repo / ".git").exists():
            continue
        group = repo.relative_to(root).as_posix()
        group = "workspace" if group == "." else group
        groups[group] = []
        names = subprocess.check_output(
            ["git", "-C", str(repo), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z"]
        ).decode().split("\0")
        for name in sorted(set(names) - {""}):
            if not is_executable_test(name):
                continue
            path = repo / name
            # Gitlinks are directories, not files owned by the parent repo.
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if rel != REPORT.as_posix():
                groups[group].append(rel)
    return groups


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


TEST_UNIT_SUFFIXES = (".c", ".m", ".mm", ".rs", ".py", ".cc", ".cpp", ".cxx")


def is_executable_test(name):
    """Whether a path is a compilable/runnable test unit, runner or harness.

    The ledger tracks tests that compile and run. Markdown, documentation,
    images, configuration and production source are intentionally excluded.
    """
    path = Path(name)
    base = path.name
    if base == "run.py" or base.endswith("_run.py"):
        return True
    if base == "test_support.h":
        return True
    if base.startswith("test_") and path.suffix == ".py":
        return True
    if path.suffix in TEST_UNIT_SUFFIXES and path.stem.endswith("_test"):
        return True
    return False


def cell(text):
    return (str(text).replace("|", "&#124;").replace("\r", " ").replace("\n", " ")
            .replace("<", "&lt;").replace(">", "&gt;"))


def load(report):
    records = {}
    if report.exists():
        text = report.read_text()
        legacy_authors = "| Written by |" in text
        for line in text.splitlines():
            if not line.startswith("| `"):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) != 7:
                raise ValueError("malformed checklist row")
            path = parts[0].strip("`")
            if path in records:
                raise ValueError(f"duplicate checklist row: {path}")
            records[path] = parts[1:]
            if legacy_authors:
                records[path][4] = ("Awaiting automated lab check" if parts[2] == "—"
                                    else "Automated lab evidence only; visual approval not recorded")
    return records


def render(root, groups, records):
    lines = [HEADER.rstrip(), ""]
    for group, paths in sorted(groups.items()):
        lines += [f"## {group}", ""]
        if not paths:
            lines += ["No inventoried files yet; not verified.", ""]
        directories = {}
        for path in paths:
            directories.setdefault(str(Path(path).parent), []).append(path)
        for directory, files in sorted(directories.items()):
            lines += [f"### `{directory}`", "",
                      "| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |",
                      "| :--- | :---: | ---: | :--- | :--- | :--- | :--- |"]
            for path in sorted(files):
                record = list(records.get(path, ["❌", "—", "—", "No executed evidence", "Awaiting automated lab check", "untested"]))
                if record[0] == "✅" and record[2] != digest(root / path):
                    record[0], record[5] = "❌", "stale — content changed; rerun required"
                lines.append("| `" + path + "` | " + " | ".join(cell(c) for c in record) + " |")
            lines.append("")
    return "\n".join(lines)


def save(root, groups, records):
    report = root / REPORT
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render(root, groups, records))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["sync", "check", "run"])
    parser.add_argument("--file", action="append", default=[], help="workspace-relative tested subject; repeatable")
    parser.add_argument("--scope", default="Command-only evidence; no broader readiness claim")
    parser.add_argument("--description", default="Automated lab check; visual approval not recorded")
    parser.add_argument("--kind", choices=["lab", "visual"], default="lab")
    parser.add_argument("--timeout", type=float, default=120, help="maximum command duration in seconds")
    # Split explicitly so the executed command can contain arbitrary options.
    args = list(sys.argv[1:] if argv is None else argv)
    split = args.index("--") if "--" in args else len(args)
    command = args[split + 1:] if split < len(args) else []
    opts = parser.parse_args(args[:split])
    if opts.action == "run" and opts.kind != "lab":
        parser.error("visual checks are user-owned and cannot be run or recorded in this lab checklist")
    if opts.timeout <= 0:
        parser.error("--timeout must be positive")
    root = Path(__file__).resolve().parent.parent
    groups = inventory(root)
    records = load(root / REPORT)
    if opts.action == "check":
        report = root / REPORT
        if not report.exists() or report.read_text() != render(root, groups, records):
            print("Checklist missing or stale: run python3 tools/test_checklist.py sync", file=sys.stderr)
            return 1
        print("Checklist inventory and recorded hashes are current (not a claim that all files pass).")
        return 0
    if opts.action == "sync":
        save(root, groups, records)
        return 0
    paths = {p for entries in groups.values() for p in entries}
    if not command or not opts.file or any(p not in paths for p in opts.file):
        parser.error("run needs inventoried --file subjects and -- <command>")
    before = {p: digest(root / p) for p in opts.file}
    try:
        result = subprocess.run(command, cwd=root, timeout=opts.timeout).returncode
    except subprocess.TimeoutExpired:
        print(f"Lab command timed out after {opts.timeout:g}s", file=sys.stderr)
        result = 124
    except OSError as exc:
        print(exc, file=sys.stderr)
        result = 127
    checked = str(int(time.time()))
    changed = False
    for path, sha in before.items():
        same = (root / path).is_file() and digest(root / path) == sha
        changed |= not same
        status = "passed" if result == 0 else ("skipped (exit 77)" if result == 77 else f"failed (exit {result})")
        if not same:
            status = "stale — subject changed during test"
        records[path] = ["✅" if result == 0 and same else "❌", checked, sha,
                         f"{command!r}; {opts.scope}", opts.description, status]
    save(root, inventory(root), records)
    return (1 if changed else result if result >= 0 else 128 - result)


if __name__ == "__main__":
    raise SystemExit(main())
