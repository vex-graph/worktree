#!/usr/bin/env python3
"""
tools/python/alloc_gate.py — the Relational Memory Law, executed.

The engine owns every runtime byte. `Memory_alloc`, `MemoryArena_alloc` and
`Transient_alloc` are the only allocation entry points, and bare libc
allocation outside the engine's own implementation is a defect.

This tool turns that sentence into a gate:

    alloc_gate.py scan            per-repository counts, human readable
    alloc_gate.py check           fail when any repository grows past its baseline
    alloc_gate.py write-baseline  record the current counts (reviewable diff)

A baseline may only shrink. Raising one is a deliberate, reviewable commit that
says "this repository gained a libc allocation on purpose", which is exactly the
conversation the law wants to force.

What counts as a hit:
  * a call to malloc, calloc, realloc, free, strdup, strndup, posix_memalign,
    aligned_alloc or alloca;
  * that is not the tail of a longer identifier (`Memory_free`, `Panel_free`),
    a member access (`p->free`, `x.free`) or a comment line;
  * in a `.c`, `.m` or `.h` file under a repository, outside `test/`;
  * and outside the engine allocator itself, which is the one exempt path.

Rust `Box`/`Vec`/`String` are outside this tool's reach by design: they are not
C calls. The law binds them too; the check does not.
"""

import argparse
import json
import re
import sys
from pathlib import Path

BASELINE = Path("tools/alloc-baseline.json")
OWNER = "re/nio/mem.c"
MANIFEST = Path("tools/platforms.json")

# The banned entry points. The lookbehind rejects `Memory_free(`,
# `Panel_free(`, `p->free(` and `x.free(` — those are the ecosystem's own
# class operations, not the libc call this law bans.
BANNED = re.compile(
    r"(?<![\w.>])(malloc|calloc|realloc|free|strdup|strndup|"
    r"posix_memalign|aligned_alloc|alloca)\s*\("
)

SKIP_PREFIXES = ("//", "*", "/*", "#")


def tooling_repos() -> set[str]:
    """Repositories the manifest marks `allocExempt` (the named exception).

    The law binds the RUNTIME. A standalone tool that runs one-shot and exits
    satisfies all four exemption criteria — no daemon, no hosted image, no
    memory crossing a module boundary, no lifetime past one command — so libc
    is correct there and an arena would buy nothing. The flag is explicit and
    independent of `role`: a tool that loads a dynamic image is not exempt.
    """
    if not MANIFEST.is_file():
        return set()
    try:
        repos = json.loads(MANIFEST.read_text(encoding="utf-8")).get("repos", {})
    except (OSError, ValueError):
        return set()
    return {key.split("/")[-1] for key, value in repos.items()
            if value.get("allocExempt") is True}

SOURCE_SUFFIXES = (".c", ".m", ".h")


def repo_of(path: Path) -> str:
    """Repository key for a source path: `vex/<repo>` → `<repo>`, tools/ → root."""
    parts = path.parts
    if len(parts) >= 2 and parts[0] == "vex":
        return parts[1]
    return "(worktree)"


def is_skipped(path: Path) -> bool:
    text = path.as_posix()
    if "test/" in text or "/.git/" in text:
        return True
    return text.endswith(OWNER)


def scan_file(path: Path) -> list[tuple[int, str]]:
    """Bare libc allocation calls in one file, as (line number, line)."""
    hits = []
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except OSError:
        return hits
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith(SKIP_PREFIXES):
            continue
        if BANNED.search(line):
            hits.append((number, line.strip()))
    return hits


EXEMPT_TOOLING = tooling_repos()


def scan_tree() -> dict[str, list[tuple[int, str]]]:
    """Every hit, grouped by file path (the baseline's unit of record).

    Per-file, not per-repository: a count alone cannot say WHICH lines are new,
    and a gate that cannot point at the offending line is a gate people argue
    with instead of fixing.
    """
    found: dict[str, list[tuple[int, str]]] = {}
    roots = [Path("vex"), Path("tools")]
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix not in SOURCE_SUFFIXES or not path.is_file():
                continue
            if is_skipped(path) or repo_of(path) in EXEMPT_TOOLING:
                continue
            hits = scan_file(path)
            if hits:
                found[path.as_posix()] = hits
    return found


def load_baseline() -> dict[str, int]:
    """Baseline counts keyed by file path."""
    if not BASELINE.is_file():
        return {}
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    return {key: int(value) for key, value in data.get("files", {}).items()}


def cmd_scan() -> int:
    found = scan_tree()
    per_repo: dict[str, int] = {}
    for path_text, hits in found.items():
        per_repo[repo_of(Path(path_text))] = per_repo.get(repo_of(Path(path_text)), 0) + len(hits)
    width = max((len(name) for name in per_repo), default=10)
    for name in sorted(per_repo):
        print(f"  {name:<{width}}  {per_repo[name]}")
    print(f"  {'total':<{width}}  {sum(per_repo.values())}")
    return 0


def cmd_check() -> int:
    found = scan_tree()
    baseline = load_baseline()
    problems = []

    for path_text in sorted(found):
        hits = found[path_text]
        allowed = baseline.get(path_text, 0)
        if len(hits) > allowed:
            problems.append((path_text, hits, allowed))

    # A file that disappeared keeps its baseline entry: coverage must never
    # narrow silently when code moves or is deleted.
    for path_text in sorted(baseline):
        if path_text not in found and baseline[path_text] > 0:
            print(f"  note: '{path_text}' has a baseline but no longer matches any source")

    if not problems:
        total = sum(len(hits) for hits in found.values())
        allowed_total = sum(baseline.values())
        print(f"  {total} bare libc allocation calls in {len(found)} files, "
              f"baseline {allowed_total} — no growth")
        return 0

    for path_text, hits, allowed in problems:
        print(f"  FAIL {path_text}: {len(hits)} calls, baseline {allowed} "
              f"({len(hits) - allowed} new)")
        for number, line in hits:
            print(f"       {path_text}:{number}: {line}")
    print()
    print("  The Relational Memory Law bans libc allocation outside")
    print(f"  {OWNER}. Route the allocation through Memory_alloc /")
    print("  MemoryArena_alloc / Transient_alloc, or — if this is a deliberate")
    print("  exception — record it with:")
    print("      python3 -B tools/python/alloc_gate.py write-baseline")
    print("  and explain the raise in the commit message.")
    return 1


def cmd_write() -> int:
    found = scan_tree()
    counts = {path: len(hits) for path, hits in sorted(found.items())}
    document = {
        "version": 1,
        "note": (
            "Bare libc allocation calls per repository, outside "
            f"{OWNER} and outside test/ trees. The Relational Memory Law (No "
            "malloc, No free) requires these counts to only shrink. Raising a "
            "number is a reviewable exception, not a routine edit."
        ),
        "owner": OWNER,
        "files": counts,
    }
    BASELINE.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {BASELINE} — {sum(counts.values())} calls across {len(counts)} files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Relational Memory Law gate")
    parser.add_argument("command", choices=("scan", "check", "write-baseline"))
    arguments = parser.parse_args()

    if arguments.command == "scan":
        return cmd_scan()
    if arguments.command == "check":
        return cmd_check()
    return cmd_write()


if __name__ == "__main__":
    sys.exit(main())
