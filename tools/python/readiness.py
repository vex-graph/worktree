#!/usr/bin/env python3
"""
tools/readiness.py — per-repo readiness scoreboard for the vexgraph worktree.

Answers "how many parts are good to go?" without inventing a percentage:

  - production source files per repo (git-tracked, tests excluded)
  - executable test units per repo, attributed to the subsystem they test
  - executed ledger evidence: green / stale / untested, per subsystem
  - current lint and layout debt per repo, from the same rules CI gates on
  - declared platform support vs declared proof, from tools/platforms.json

Statuses stay distinct: a test unit is `green` only when its recorded hash still
matches, `stale` when the file changed, and `untested` otherwise. A platform is
`proven` only when the owning repo's own documentation says so; observed CI
results are reported separately and never overwrite the claim.

The scoreboard composes existing owners instead of rebuilding them: it reads
`tools/test_checklist.py` for the inventory, `tools/linter.py` for violations,
and the ledger for executed evidence. It never compiles a shadow build.

    python3 tools/readiness.py                  # text table
    python3 tools/readiness.py --markdown       # GitHub step-summary table
    python3 tools/readiness.py --json           # machine-readable
    python3 tools/readiness.py --execute        # also run ./tools/b build|test
"""

import argparse
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def _find_root(start: Path) -> Path:
    cur = start
    while cur.parent != cur:
        if (cur / "tools" / "platforms.json").is_file():
            return cur
        cur = cur.parent
    return start.parent.parent


ROOT = _find_root(Path(__file__).resolve().parent)
REPORT = Path("metadata/gists/test-checklist.md")
PLATFORMS = Path("tools/platforms.json")
SOURCE_SUFFIXES = {".c", ".h", ".m", ".mm", ".cc", ".cpp", ".cxx", ".rs"}
SUBSYSTEM_DIRS = (
    "vexgraph-ecosystem",
    "vexgraph-hobby-projects",
    "suite/ecosystem",
    "suite/personal",
    "suite/projects",
)
WORKTREE = "(worktree)"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_tools_py = Path(__file__).resolve().parent
CHECKLIST = load_module("test_checklist", _tools_py / "test_checklist.py" if (_tools_py / "test_checklist.py").is_file() else ROOT / "tools/test_checklist.py")
LINTER = load_module("linter", _tools_py / "linter.py" if (_tools_py / "linter.py").is_file() else ROOT / "tools/linter.py")
ARRANGE = load_module("arrange", _tools_py / "arrange.py" if (_tools_py / "arrange.py").is_file() else ROOT / "tools/arrange.py")


def tests_checkout(root):
    for cand in (root / "vexgraph-ecosystem" / "tests", root / "tests"):
        if (cand / ".git").exists():
            return cand
    return root / "vexgraph-ecosystem" / "tests"


def repo_dirs(root):
    """Every checked-out repository the scoreboard covers, plus the worktree."""
    tc = tests_checkout(root)
    found = [root]
    if (tc / ".git").exists():
        found.append(tc)
    for base in SUBSYSTEM_DIRS:
        directory = root / base
        if not directory.is_dir():
            continue
        found.extend(sorted(p for p in directory.iterdir() if p.is_dir()))
    return [p for p in found if (p / ".git").exists()]


def repo_key(root, path):
    if path == root:
        return WORKTREE
    rel = path.relative_to(root).as_posix()
    if rel in ("vexgraph-ecosystem/tests", "tests"):
        return "tests"
    return rel


def git_files(repo):
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z"], stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return []
    return [name for name in out.decode().split("\0") if name]


def owner_of_path(path, claims_by_subsystem):
    """Attribute a workspace-relative path to the repo that owns the subject.

    Tests under `tests/<subsystem>/` belong to the subsystem's repo, not to the
    shared tests checkout, so a repo's readiness includes the proof written for
    it. Tooling tests and workspace files belong to the worktree.
    """
    parts = path.split("/")
    if len(parts) > 1 and parts[0] == "suite":
        return "/".join(parts[:3])
    if len(parts) > 2 and parts[0] in SUBSYSTEM_DIRS:
        return "/".join(parts[:2])
    if parts[0] == "tests" and len(parts) > 1:
        subsystem = parts[1]
        if subsystem == "tools":
            return WORKTREE
        return claims_by_subsystem.get(subsystem, "tests")
    if len(parts) > 2 and parts[0] == "vexgraph-ecosystem" and parts[1] == "tests":
        subsystem = parts[2]
        if subsystem == "tools":
            return WORKTREE
        return claims_by_subsystem.get(subsystem, "tests")
    return WORKTREE


def production_files(repo, key):
    if key == "tests":
        return 0
    count = 0
    for name in git_files(repo):
        path = repo / name
        if not path.is_file() or "tests" in Path(name).parts:
            continue
        if path.suffix in SOURCE_SUFFIXES:
            count += 1
    return count


def load_claims(root):
    path = root / PLATFORMS
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_counts(root, key, claims_by_subsystem):
    """Executed evidence for one owner: green, stale, untested, total."""
    try:
        records = CHECKLIST.load(root / REPORT)
    except (OSError, ValueError):
        return {"green": 0, "stale": 0, "untested": 0, "total": 0, "last": None}
    counts = Counter()
    last = None
    for path, record in records.items():
        if owner_of_path(path, claims_by_subsystem) != key:
            continue
        status, checked, sha = record[0], record[1], record[2]
        counts["total"] += 1
        if str(checked).isdigit():
            last = max(int(checked), last or 0)
        if status == "✅" and (root / path).is_file() and \
                CHECKLIST.digest(root / path) == sha:
            counts["green"] += 1
        elif status == "✅":
            counts["stale"] += 1
        else:
            counts["untested"] += 1
    return {
        "green": counts["green"],
        "stale": counts["stale"],
        "untested": counts["untested"],
        "total": counts["total"],
        "last": last,
    }


def test_units(root, claims_by_subsystem):
    """Executable test units per owner, from the shared tests checkout."""
    counts = Counter()
    for name in git_files(tests_checkout(root)):
        if not CHECKLIST.is_executable_test(name):
            continue
        parts = Path(name).parts
        subsystem = parts[0] if len(parts) > 1 else ""
        if subsystem == "tools":
            counts[WORKTREE] += 1
        else:
            counts[claims_by_subsystem.get(subsystem, "tests")] += 1
    return counts


def lint_by_repo(root, claims_by_subsystem):
    """Run the linter once and attribute violations to their owning repo."""
    roots = [str(p) for p in repo_dirs(root) if p != root]
    roots += [str(root / "tools"), str(root / ".github"),
              str(root / "metadata/gists")]
    linter = LINTER.Linter(roots, cwd=str(root))
    violations = linter.collect()
    counts = Counter(owner_of_path(v["file"], claims_by_subsystem)
                     for v in violations)
    rules = Counter(v["rule"] for v in violations)
    return counts, rules, linter.files_scanned


def layout_by_repo(root, claims_by_subsystem):
    """Run the arranger once and attribute findings to their owning repo."""
    roots = [str(p) for p in repo_dirs(root) if p != root]
    roots += [str(root / "tools"), str(root / ".github"),
              str(root / "metadata/gists")]
    violations = ARRANGE.collect(roots, cwd=str(root))
    counts = Counter(owner_of_path(v["file"], claims_by_subsystem)
                     for v in violations)
    return counts, sum(counts.values())


def run_command(command, timeout):
    try:
        result = subprocess.run(command, cwd=str(ROOT), timeout=timeout,
                                capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return "timeout"
    except OSError as exc:
        return f"error: {exc}"
    return "pass" if result.returncode == 0 else f"fail({result.returncode})"


def build_report(root, execute=False, timeout=1800):
    claims = load_claims(root)
    declared = claims.get("repos", {})
    platforms = claims.get("platforms", ["macos", "linux", "windows"])
    claims_by_subsystem = {
        claim["subsystem"]: key for key, claim in declared.items()
        if claim.get("subsystem")
    }

    units = test_units(root, claims_by_subsystem)
    lint_counts, lint_rules, files_scanned = lint_by_repo(
        root, claims_by_subsystem)
    layout_counts, layout_total = layout_by_repo(root, claims_by_subsystem)

    rows = []
    for repo in repo_dirs(root):
        key = repo_key(root, repo)
        claim = declared.get(key, {})
        ledger = ledger_counts(root, key, claims_by_subsystem)
        if key == "tests":
            sources = 0
        else:
            sources = production_files(repo, key)
        rows.append({
            "repo": key,
            "tier": claim.get("tier", "?"),
            "sources": sources,
            "test_units": units.get(key, 0),
            "green": ledger["green"],
            "stale": ledger["stale"],
            "untested": ledger["untested"],
            "ledger_total": ledger["total"],
            "last_checked": ledger["last"],
            "lint": lint_counts.get(key, 0),
            "layout": layout_counts.get(key, 0),
            "support": claim.get("support", []),
            "proven": claim.get("proven", []),
        })

    rows.sort(key=lambda row: (row["tier"], row["repo"]))

    summary = {
        "repos": len(rows),
        "production_files": sum(row["sources"] for row in rows),
        "lint_files_scanned": files_scanned,
        "lint_total": sum(lint_counts.values()),
        "lint_by_rule": dict(lint_rules.most_common()),
        "layout_total": layout_total,
        "test_units": sum(row["test_units"] for row in rows),
        "green": sum(row["green"] for row in rows),
        "stale": sum(row["stale"] for row in rows),
        "untested": sum(row["untested"] for row in rows),
        "repos_with_green": sum(1 for row in rows if row["green"]),
        "proven": {platform: sum(1 for row in rows if platform in row["proven"])
                   for platform in platforms},
        "supported": {platform: sum(1 for row in rows if platform in row["support"])
                      for platform in platforms},
        "build": "not run",
        "test": "not run",
    }
    if execute:
        summary["build"] = run_command(["./tools/b", "build"], timeout)
        summary["test"] = run_command(["./tools/shell/test.sh"], timeout)

    return {"summary": summary, "rows": rows, "platforms": platforms}


def text_report(report):
    summary = report["summary"]
    lines = ["Vexgraph readiness", "",
             f"{'repo':44s} {'tier':8s} {'src':>5s} {'tests':>7s} "
             f"{'ledger':>9s} {'lint':>6s} {'layout':>7s}  proven"]
    for row in report["rows"]:
        ledger = f"{row['green']}/{row['ledger_total']}"
        if row["stale"]:
            ledger += f"!{row['stale']}"
        proven = ",".join(row["proven"]) or "-"
        lines.append(f"{row['repo']:44s} {row['tier']:8s} {row['sources']:5d} "
                     f"{row['test_units']:7d} {ledger:>9s} {row['lint']:6d} "
                     f"{row['layout']:7d}  {proven}")
    lines.append("")
    lines.append(
        f"{summary['repos']} repos | {summary['production_files']} production files | "
        f"{summary['test_units']} test units | "
        f"{summary['green']} green, {summary['stale']} stale, "
        f"{summary['untested']} untested | lint {summary['lint_total']} | "
        f"layout {summary['layout_total']}")
    proven = ", ".join(f"{k} {v}/{summary['repos']}"
                       for k, v in summary["proven"].items())
    lines.append(f"declared proof: {proven}")
    if summary["build"] != "not run" or summary["test"] != "not run":
        lines.append(f"workspace build: {summary['build']} | "
                     f"workspace test: {summary['test']}")
    else:
        lines.append("workspace build/test: not run (use --execute)")
    return "\n".join(lines)


def markdown_report(report):
    summary = report["summary"]
    lines = [
        "### Vexgraph readiness",
        "",
        f"**{summary['repos']} repos** | "
        f"**{summary['production_files']}** production files | "
        f"**{summary['green']}/{summary['test_units']}** test units green "
        f"({summary['stale']} stale, {summary['untested']} untested) | "
        f"**{summary['lint_total']}** lint violations | "
        f"**{summary['layout_total']}** layout findings",
        "",
        "| Repo | Tier | Sources | Test units | Green | Stale | Untested | Lint | Layout | Proven |",
        "| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
    ]
    for row in report["rows"]:
        proven = ", ".join(row["proven"]) or "none"
        lines.append(
            f"| `{row['repo']}` | {row['tier']} | {row['sources']} | "
            f"{row['test_units']} | {row['green']} | {row['stale']} | "
            f"{row['untested']} | {row['lint']} | {row['layout']} | {proven} |")
    proven = ", ".join(f"{k} {v}/{summary['repos']}"
                       for k, v in summary["proven"].items())
    lines += ["", f"Declared proof: {proven}",
              f"Workspace build: {summary['build']} | "
              f"Workspace test: {summary['test']}"]
    return "\n".join(lines)


def write_out(text, path):
    if not path or path == "-":
        print(text)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.rstrip() + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Vexgraph readiness scoreboard")
    parser.add_argument("--json", action="store_true", help="print the raw report")
    parser.add_argument("--markdown", action="store_true",
                        help="print a GitHub step-summary table")
    parser.add_argument("--out", default=None,
                        help="write to a file instead of stdout ('-' = stdout)")
    parser.add_argument("--execute", action="store_true",
                        help="also run ./tools/b build and ./tools/shell/test.sh")
    parser.add_argument("--timeout", type=float, default=1800,
                        help="seconds per executed command")
    args = parser.parse_args(argv)

    report = build_report(ROOT, execute=args.execute, timeout=args.timeout)
    if args.json:
        text = json.dumps(report, indent=2, sort_keys=False)
    elif args.markdown:
        text = markdown_report(report)
    else:
        text = text_report(report)
    write_out(text, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
