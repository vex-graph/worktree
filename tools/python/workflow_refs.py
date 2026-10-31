#!/usr/bin/env python3
"""
tools/python/workflow_refs.py — resolve what the workflows name, before CI runs.

Every red run in this workspace's CI history has the same shape: a job that
dies before it tests anything, because a `run:` block names a path that moved
(`tools/linter.py` after the two-root layout) or a `runs-on:` label GitHub
retired (`macos-13`). Neither is a product defect and neither needs a runner to
find: both are references, and references resolve against this checkout.

  python3 tools/python/workflow_refs.py check

Read-only, cold path only: run it before a push, never in a product build.

The retired-label table is deliberately conservative. A label is added only
with a citation; an absent label costs one red run, an invented one teaches
nobody anything.
"""

import argparse
import re
import sys
from pathlib import Path


WORKFLOWS = Path(".github/workflows")

# Labels GitHub has disabled. Cite the removal when adding one.
RETIRED_RUNNERS = {
    "macos-10.15": "removed 2022",
    "macos-11": "removed 2024",
    "macos-12": "removed 2024",
    "macos-13": "disabled December 2025; use macos-15-intel for x86_64",
    "ubuntu-18.04": "removed 2023",
    "windows-2016": "removed 2022",
}

# Paths the workflows drive the workspace through. They carry no extension, so
# the general reference scan cannot see them, and every job depends on them.
ENTRY_POINTS = ("tools/b", "tools/prefs")

# Only source-shaped references are resolved; build outputs and globs are not
# files that exist before a build, and `$VAR` prefixes are resolved at runtime.
SUFFIXES = {
    ".py", ".c", ".h", ".m", ".mm", ".sh",
    ".json", ".toml", ".txt", ".md", ".lock", ".yml",
}

PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:tools|metadata|vexgraph-[A-Za-z0-9_-]+)/[A-Za-z0-9_./-]+)"
)
RUN_RE = re.compile(r"^(\s*)(?:-\s+)?run:\s*(.*)$")
RUNS_ON_RE = re.compile(r"^\s*(?:-\s+)?runs-on:\s*(.+?)\s*$")
# Matrix legs name the runner under `os:`; `runs-on:` then reads
# `${{ matrix.os }}`, so the retired-label check must read both.
OS_RE = re.compile(r"^\s*(?:-\s+)?os:\s*['\"]?([A-Za-z0-9._-]+)['\"]?\s*$")


def find_root(start):
    cur = start.resolve()
    while cur.parent != cur:
        if (cur / "tools" / "platforms.json").is_file():
            return cur
        cur = cur.parent
    return start.resolve().parent.parent


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def run_bodies(lines):
    """Yield (line number, text) for every `run:` body, block or single line."""
    index, total = 0, len(lines)
    while index < total:
        match = RUN_RE.match(lines[index])
        if not match:
            index += 1
            continue
        body_indent = len(match.group(1))
        inline = match.group(2).strip()
        if inline and not inline.startswith(("|", ">")):
            yield index + 1, inline
            index += 1
            continue
        index += 1
        # A block scalar runs to the first non-blank line at or above the
        # `run:` key; blank lines inside it belong to the body.
        while index < total:
            line = lines[index]
            if line.strip() and indent_of(line) <= body_indent:
                break
            yield index + 1, line
            index += 1


def references(lines):
    """Yield (line number, path) for each source-shaped reference in a run body."""
    for number, text in run_bodies(lines):
        for match in PATH_RE.finditer(text):
            path = match.group(1).rstrip(".,;:")
            if "*" in path or "{{" in path:
                continue
            if Path(path).suffix not in SUFFIXES:
                continue
            yield number, path


def runners(lines):
    """Yield (line number, label) for each literal runner label.

    Reads `runs-on:` for direct jobs and `os:` for matrix legs. Only labels in
    RETIRED_RUNNERS are reported, so an unrelated `os:` key cannot be a false
    alarm.
    """
    for index, line in enumerate(lines, 1):
        match = RUNS_ON_RE.match(line) or OS_RE.match(line)
        if not match:
            continue
        label = match.group(1).strip().strip("'\"")
        if not label or label.startswith(("$", "[", "{")):
            continue
        yield index, label


def check(root):
    problems = []
    scanned = 0
    for workflow in sorted((root / WORKFLOWS).glob("*.yml")):
        scanned += 1
        lines = workflow.read_text(encoding="utf-8").splitlines()
        name = workflow.relative_to(root).as_posix()
        for number, path in references(lines):
            if not (root / path).exists():
                problems.append(f"{name}:{number}: missing path  {path}")
        for number, label in runners(lines):
            reason = RETIRED_RUNNERS.get(label)
            if reason:
                problems.append(f"{name}:{number}: retired runner  {label} ({reason})")
    for entry in ENTRY_POINTS:
        candidate = root / entry
        if not (candidate.is_file() and candidate.stat().st_mode & 0o111):
            problems.append(f"{entry}: entry point missing or not executable")
    return scanned, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check"], nargs="?", default="check")
    parser.parse_args(argv)

    root = find_root(Path(__file__).parent)
    scanned, problems = check(root)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"{len(problems)} workflow reference(s) cannot resolve "
              f"across {scanned} file(s); CI would fail before testing anything.",
              file=sys.stderr)
        return 1
    print(f"Workflow references resolve across {scanned} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
