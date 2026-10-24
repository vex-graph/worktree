#!/usr/bin/env python3
"""
tools/ci_repos.py — manifest-driven checkout and per-repo CI callers.

The readiness manifest (`tools/platforms.json`) already names every repository,
its tier and its declared platforms. This tool uses that single source to:

  list                     print repo key, tier and remote
  clone [--auth TOKEN]     clone every missing repository into its key path
  callers [--write]        install the reusable-workflow caller in each repo
  baselines [--write]      record each repo's lint + layout baselines (dry run by default)
  check                    validate the manifest and report local checkouts

`clone`, `callers` and `baselines` default to a dry run; `--execute` / `--write`
is required to mutate the filesystem. Nothing here pushes or commits.

CI uses the same manifest, so a new repo is added once, not in every workflow.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path("tools/platforms.json")
BASELINE = ".github/lint-baseline.json"
LAYOUT = ".github/arrange-baseline.json"
LINTER = Path(__file__).resolve().parent / "linter.py"
ARRANGE = Path(__file__).resolve().parent / "arrange.py"
WORKFLOW = ".github/workflows/vexgraph-ci.yml"
CALLER = """\
# Vexgraph per-repo CI caller. Installed by vex-graph/worktree tools/ci_repos.py.
# The reusable workflow lives in vex-graph/worktree and is pinned to `main`.
name: Vexgraph CI

on:
  push:
  pull_request:
  workflow_dispatch:

jobs:
  vexgraph:
    uses: vex-graph/worktree/.github/workflows/repo-check.yml@main
    with:
      baseline: ".github/lint-baseline.json"
      layout: ".github/arrange-baseline.json"
    secrets: inherit
"""


def load_manifest(root):
    path = root / MANIFEST
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    repos = data.get("repos")
    if not isinstance(repos, dict) or not repos:
        errors.append("manifest has no repos")
        repos = {}
    for key, claim in repos.items():
        if key == "(worktree)":
            continue
        if key.startswith("/") or ".." in Path(key).parts:
            errors.append(f"{key}: key must be a relative path inside the workspace")
        remote = claim.get("remote", "")
        if not remote.startswith("https://") or not remote.endswith(".git"):
            errors.append(f"{key}: remote must be an https .git URL")
        if not isinstance(claim.get("tier"), str):
            errors.append(f"{key}: missing tier")
    return data, errors


def entries(data):
    repos = data.get("repos", {})
    return [(key, claim) for key, claim in repos.items() if key != "(worktree)"]


def redact(text, token):
    """Keep a token out of planned commands and CI logs."""
    return text.replace(token, "***") if token else text


def lawbooks(repo):
    return sorted(path.name for path in repo.glob("*-preferences.md"))


def readiness(repo):
    """The five things a per-repo caller needs before it can go green."""
    return {
        "checkout": (repo / ".git").exists(),
        "lawbook": bool(lawbooks(repo)),
        "lint": (repo / BASELINE).is_file(),
        "layout": (repo / LAYOUT).is_file(),
        "caller": (repo / WORKFLOW).is_file(),
    }


def clone(args):
    data, errors = load_manifest(args.root)
    if errors:
        for error in errors:
            print(f"manifest: {error}", file=sys.stderr)
        return 2
    failed = 0
    for key, claim in entries(data):
        dest = args.root / key
        if (dest / ".git").exists():
            print(f"present  {key}")
            continue
        remote = claim["remote"]
        if args.auth:
            remote = remote.replace("https://", f"https://{args.auth}@", 1)
        command = ["git", "clone", "--depth", str(args.depth), remote, str(dest)]
        if args.dry_run:
            print("would   ", redact(" ".join(command), args.auth))
            continue
        if dest.exists() and any(dest.iterdir()):
            print(f"refused  {key}: destination is not empty", file=sys.stderr)
            failed += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest.rmdir()
        print(f"cloning  {key}")
        result = subprocess.run(command, cwd=str(args.root))
        if result.returncode != 0:
            failed += 1
    return 1 if failed else 0


def callers(args):
    data, errors = load_manifest(args.root)
    if errors:
        for error in errors:
            print(f"manifest: {error}", file=sys.stderr)
        return 2
    blocked = 0
    for key, _claim in entries(data):
        repo = args.root / key
        gaps = [name for name in ("lawbook", "lint", "layout")
                if not readiness(repo)[name]]
        if gaps and not args.force:
            print(f"blocked  {key}: missing {', '.join(gaps)}")
            blocked += 1
            continue
        path = repo / WORKFLOW
        if path.exists() and path.read_text(encoding="utf-8") == CALLER:
            print(f"current  {key}")
            continue
        if not args.write:
            state = "would update" if path.exists() else "would install"
            print(f"{state} {path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(CALLER, encoding="utf-8", newline="\n")
        print(f"installed {path}")
    if blocked:
        print(f"{blocked} repo(s) blocked; record a lawbook and both baselines "
              f"first, or pass --force", file=sys.stderr)
    return 1 if args.write and blocked else 0


def baselines(args):
    data, errors = load_manifest(args.root)
    if errors:
        for error in errors:
            print(f"manifest: {error}", file=sys.stderr)
        return 2
    for tool in (LINTER, ARRANGE):
        if not tool.is_file():
            print(f"tool: {tool} is missing", file=sys.stderr)
            return 2
    failed = 0
    for key, _claim in entries(data):
        repo = args.root / key
        if not (repo / ".git").exists():
            print(f"missing  {key}", file=sys.stderr)
            failed += 1
            continue
        if not args.write:
            totals = {}
            for name, tool in (("lint", LINTER), ("layout", ARRANGE)):
                result = subprocess.run(
                    [sys.executable, "-B", str(tool), "--json", "."],
                    cwd=str(repo), capture_output=True, text=True)
                if result.returncode not in (0, 1):
                    print(f"error    {key}: {name} exited {result.returncode}",
                          file=sys.stderr)
                    failed += 1
                    break
                totals[name] = json.loads(result.stdout)["total"]
            else:
                print(f"would    {key}: lint {totals['lint']}, "
                      f"layout {totals['layout']} -> {BASELINE}, {LAYOUT}")
            continue
        print(f"recording {key}")
        for name, tool, target in (("lint", LINTER, BASELINE),
                                   ("layout", ARRANGE, LAYOUT)):
            result = subprocess.run(
                [sys.executable, "-B", str(tool), "--no-color",
                 "--write-baseline", str(repo / target), "."],
                cwd=str(repo), capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{name}: {result.stderr.strip()}", file=sys.stderr)
                failed += 1
                break
    return 1 if failed else 0


def check(args):
    data, errors = load_manifest(args.root)
    for error in errors:
        print(f"manifest: {error}", file=sys.stderr)
    for key, claim in entries(data):
        state = readiness(args.root / key)
        marks = (
            ("present", "absent", state["checkout"], 8),
            ("lawbook", "no-lawbook", state["lawbook"], 11),
            ("lint", "no-lint", state["lint"], 8),
            ("layout", "no-layout", state["layout"], 12),
            ("caller", "no-caller", state["caller"], 10),
        )
        columns = " ".join((yes if flag else no).ljust(width)
                           for yes, no, flag, width in marks)
        print(f"{columns} {key:44s} {claim.get('tier', '?')}")
    if args.require_all:
        missing = [key for key, _claim in entries(data)
                   if not readiness(args.root / key)["checkout"]]
        for key in missing:
            print(f"missing checkout: {key}", file=sys.stderr)
        errors.extend(f"missing checkout: {key}" for key in missing)
    if args.require_ready:
        gaps = []
        for key, _claim in entries(data):
            state = readiness(args.root / key)
            for name in ("checkout", "lawbook", "lint", "layout", "caller"):
                if not state[name]:
                    gaps.append(f"{key}: {name}")
        for gap in gaps:
            print(f"not ready: {gap}", file=sys.stderr)
        errors.extend(f"not ready: {gap}" for gap in gaps)
    return 1 if errors else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="action", required=True)

    list_parser = sub.add_parser("list", help="print the manifest")
    list_parser.set_defaults(func=None)

    clone_parser = sub.add_parser("clone", help="clone missing repositories")
    clone_parser.add_argument("--auth", default=os.environ.get("ECOSYSTEM_PAT", ""))
    clone_parser.add_argument("--depth", type=int, default=1)
    clone_parser.add_argument("--dry-run", action="store_true")
    clone_parser.set_defaults(func=clone)

    caller_parser = sub.add_parser("callers", help="install per-repo callers")
    caller_parser.add_argument("--write", action="store_true")
    caller_parser.add_argument("--force", action="store_true",
                               help="install even without a lawbook or baselines")
    caller_parser.set_defaults(func=callers)

    baseline_parser = sub.add_parser(
        "baselines", help="record each repo's lint + layout baselines")
    baseline_parser.add_argument("--write", action="store_true")
    baseline_parser.set_defaults(func=baselines)

    check_parser = sub.add_parser("check", help="validate the manifest")
    check_parser.add_argument("--require-all", action="store_true")
    check_parser.add_argument("--require-ready", action="store_true",
                              help="fail unless checkout, lawbook, both baselines and caller exist")
    check_parser.set_defaults(func=check)

    args = parser.parse_args(argv)
    data, errors = load_manifest(args.root)
    if args.action == "list":
        for key, claim in entries(data):
            print(f"{key}\t{claim.get('tier', '?')}\t{claim.get('remote', '')}")
        return 1 if errors else 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
