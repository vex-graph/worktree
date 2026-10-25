#!/usr/bin/env python3
"""
tools/arrange.py — structural layout for the Semantic Consistency Law (Control flow).

The linter checks spelling and reference form; this tool checks the shape of
control flow and the separation of statements:

  - a single-statement `if` / `for` / `while` / `else` body takes no braces;
  - the header keeps a space before the newline and the statement sits on the
    next line, indented;
  - no blank line sits between a header and its single body statement;
  - sequential statements in one block are separated by exactly one blank line;
  - a multi-statement body keeps its braces.

Usage:

  python3 tools/arrange.py                      # check, report violations
  python3 tools/arrange.py --diff               # show the proposed rewrite
  python3 tools/arrange.py --write              # apply the mechanical rewrite
  python3 tools/arrange.py --baseline .github/arrange-baseline.json
  python3 tools/arrange.py --write-baseline .github/arrange-baseline.json

The rewrite is mechanical and conservative: it never reindents a body, never
touches a braced `if`/`else` chain whose closing brace carries `else`, and never
removes braces that contain a comment or more than one statement.
"""

import argparse
import difflib
import importlib.util
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("linter", os.path.join(HERE, "linter.py"))
LINTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINTER)

SUFFIXES = (".c", ".h", ".m", ".mm")
DEFAULT_ROOTS = LINTER.DEFAULT_ROOTS
EXCLUDE_DIRS = LINTER.EXCLUDE_DIRS
EXCLUDE_FILES = LINTER.EXCLUDE_FILES

RULE = "Semantic Consistency Law (Control flow"
CONTROL = re.compile(r"^(\s*)((?:(?:else)\s+)?if|for|while)\s*\(")
ELSE = re.compile(r"^(\s*)else\s*$")
TYPE_OPEN = re.compile(r"\b(struct|union|enum)\b")
INIT_OPEN = re.compile(r"=\s*\{")
FUNC_OPEN = re.compile(r"\)\s*\{\s*$")
CONTROL_OPEN = re.compile(r"^\s*(?:(?:else\s+)?if|for|while|switch|do)\b.*\{\s*$")
ELSE_OPEN = re.compile(r"^\s*\}\s*else\b.*\{\s*$")


def strip_lines(lines):
    """Return comment/string-stripped code, same line count, same length."""
    code = []
    state = False
    for line in lines:
        stripped, state = LINTER.strip_comments_and_strings(line, state)
        code.append(stripped)
    return code


def brace_depths(code):
    before = []
    after = []
    depth = 0
    for line in code:
        before.append(depth)
        depth += line.count("{") - line.count("}")
        after.append(depth)
    return before, after


def brace_contexts(code):
    """Classify every brace as a statement block, a type body or other.

    Statement separation is only enforced inside function and control blocks;
    struct/union/enum members and initializers are declarations, not statements.
    """
    stack = []
    contexts = []
    for index, line in enumerate(code):
        contexts.append(list(stack))
        text = line.strip()
        if TYPE_OPEN.search(text) or INIT_OPEN.search(text):
            kind = "type"
        elif ELSE_OPEN.match(text) or CONTROL_OPEN.match(text) or FUNC_OPEN.search(text):
            kind = "block"
        elif text == "{":
            previous = next((code[j].strip() for j in range(index - 1, -1, -1)
                             if code[j].strip()), "")
            if TYPE_OPEN.search(previous) or previous.endswith("="):
                kind = "type"
            elif previous.endswith(")") or CONTROL_OPEN.match(previous):
                kind = "block"
            else:
                kind = "other"
        else:
            kind = "other"
        for char in line:
            if char == "{":
                stack.append(kind)
            elif char == "}" and stack:
                stack.pop()
    return contexts


def in_statement_block(contexts, index):
    stack = contexts[index]
    return bool(stack) and stack[-1] == "block"


def indent_of(line):
    return len(line) - len(line.lstrip(" \t"))


def split_control(code):
    """Return (keyword, head_end) for a single-line control header, else None."""
    match = CONTROL.match(code)
    if not match:
        return None
    keyword = " ".join(match.group(2).split())
    open_paren = code.find("(", match.start(2))
    depth = 0
    for index in range(open_paren, len(code)):
        char = code[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return keyword, index + 1
    return None


def violation(path, line, snippet, msg):
    return {
        "rule": f"{RULE}: {msg})",
        "file": path,
        "line": line,
        "snippet": snippet.strip(),
        "msg": msg,
        "fixable": True,
    }


def analyze(path, text):
    """Return (violations, replacements, deletions, insertions).

    replacements: {line_index: [replacement lines without newline]}
    deletions:    set(line_index)
    insertions:   {line_index: [lines without newline to insert before it]}
    """
    lines = text.splitlines()
    code = strip_lines(lines)
    before, after = brace_depths(code)
    contexts = brace_contexts(code)
    total = len(lines)

    violations = []
    replacements = {}
    deletions = set()
    insertions = {}

    def is_comment_only(index):
        return bool(lines[index].strip()) and not code[index].strip()

    def next_structural(start, stop=None):
        stop = total if stop is None else stop
        for index in range(start, stop):
            if code[index].strip():
                return index
        return None

    # ── braced single-statement bodies ─────────────────────────────────────
    for index, line in enumerate(code):
        match = CONTROL.match(line)
        if not match:
            continue
        split = split_control(line)
        if split is None:
            continue
        _keyword, head_end = split
        if line[head_end:].strip() != "{":
            continue
        if "else" in line[head_end:]:
            continue
        close = None
        for candidate in range(index + 1, total):
            if after[candidate] == before[index] and "}" in code[candidate]:
                close = candidate
                break
        if close is None:
            continue
        if lines[close].strip() != "}":
            continue  # `} else {` or a trailing comment: leave the chain alone

        body = []
        skip = False
        for inner in range(index + 1, close):
            if not lines[inner].strip():
                continue
            if is_comment_only(inner):
                skip = True
                break
            if "{" in code[inner] or "}" in code[inner]:
                skip = True
                break
            body.append(inner)
        if skip or len(body) != 1:
            continue

        statement = code[body[0]].strip()
        if not statement.endswith(";"):
            continue
        header = lines[index].rstrip()
        header = re.sub(r"\{\s*$", "", header).rstrip() + " "
        replacements[index] = [header]
        deletions.add(close)
        violations.append(violation(
            path, index + 1, lines[index],
            "single-statement braces"))

    # ── unbraced headers: trailing space, body line, no gap ────────────────
    for index, line in enumerate(code):
        else_match = ELSE.match(line)
        split = split_control(line)
        if split is None and not else_match:
            continue
        if split is not None:
            keyword, head_end = split
            tail = line[head_end:].strip()
            raw_tail = lines[index][head_end:]
            if "//" in raw_tail or "/*" in raw_tail:
                continue
            if tail == "":
                pass  # body on the next line
            elif tail.endswith(";") and "{" not in tail and "}" not in tail:
                body = lines[index][head_end:].strip()
                header = lines[index][:head_end].rstrip() + " "
                replacements[index] = [header, " " * (indent_of(lines[index]) + 3) + body]
                violations.append(violation(
                    path, index + 1, lines[index],
                    "body on the header line"))
                continue
            else:
                continue
        else:
            tail = ""

        body_index = next_structural(index + 1)
        if body_index is None:
            continue
        if code[body_index].strip().startswith("#"):
            continue
        if indent_of(lines[body_index]) <= indent_of(lines[index]):
            continue
        if code[body_index].strip() == "{":
            continue  # Allman brace: handled as a multi-statement body
        if not (code[body_index].strip().endswith(";")
                or split_control(code[body_index]) or ELSE.match(code[body_index])):
            continue

        header = lines[index].rstrip("\n")
        if not header.endswith((" ", "\t")):
            replacements[index] = [header + " "]
            violations.append(violation(
                path, index + 1, lines[index], "header space"))
        gaps = range(index + 1, body_index)
        if gaps and all(not lines[gap].strip() for gap in gaps):
            deletions.update(gaps)
            violations.append(violation(
                path, index + 1, lines[index], "header body gap"))

        # The control statement ends with its single body statement; the next
        # sibling needs one blank line after it.
        if (code[body_index].strip().endswith(";")
                and in_statement_block(contexts, index)):
            follower = body_index + 1
            if (follower < total and lines[follower].strip()
                    and code[follower].strip()
                    and before[follower] == before[index]
                    and indent_of(lines[follower]) == indent_of(lines[index])):
                follow = code[follower].strip()
                if not follow.startswith(("}", "else", ";", ")", ",")):
                    insertions.setdefault(follower, []).append("")
                    violations.append(violation(
                        path, follower + 1, lines[follower],
                        "statement separation"))

    # ── a closed block followed immediately by a sibling statement ─────────
    for index, line in enumerate(code):
        if line.strip() != "}":
            continue
        if not contexts[index] or contexts[index][-1] != "block":
            continue
        follower = index + 1
        if follower >= total or not lines[follower].strip():
            continue
        if not code[follower].strip():
            continue
        if (before[follower] != after[index]
                or indent_of(lines[follower]) != indent_of(line)):
            continue
        follow = code[follower].strip()
        if follow.startswith(("}", "else", ";", ")", ",")):
            continue
        insertions.setdefault(follower, []).append("")
        violations.append(violation(
            path, follower + 1, lines[follower], "statement separation"))

    # ── sequential statements: one blank line between them ─────────────────
    for index, line in enumerate(code):
        if not line.rstrip().endswith(";"):
            continue
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if (stripped.startswith(("for", "while"))
                and not line.rstrip().endswith(";")):
            continue
        if index > 0 and lines[index - 1].rstrip().endswith("\\"):
            continue  # macro continuation
        if lines[index].rstrip().endswith("\\"):
            continue
        if not in_statement_block(contexts, index):
            continue
        if index + 1 >= total:
            continue
        follower = index + 1
        if not lines[follower].strip():
            continue
        if not code[follower].strip():
            continue  # comment immediately after: leave it alone
        if before[follower] != before[index]:
            continue
        if indent_of(lines[follower]) != indent_of(lines[index]):
            continue
        follow = code[follower].strip()
        if follow.startswith(("}", "else", "case ", "default:", "{", "#",
                              ".", "->", "+", "-", "*", "/", "%", "&", "|",
                              "?", ":", ",", "]")):
            continue
        if follow.startswith("while") and line.lstrip().startswith("}"):
            continue
        insertions.setdefault(follower, []).append("")
        violations.append(violation(
            path, follower + 1, lines[follower], "statement separation"))

    return violations, replacements, deletions, insertions


def apply_edits(lines, replacements, deletions, insertions):
    output = []
    for index, line in enumerate(lines):
        output.extend(insertions.get(index, []))
        if index in deletions:
            continue
        if index in replacements:
            output.extend(replacements[index])
            continue
        output.append(line)
    return output


def fixpoint(path, text, limit=5):
    """Apply edits until the layout stops changing."""
    for _ in range(limit):
        lines = text.splitlines()
        _found, replacements, deletions, insertions = analyze(path, text)
        if not (replacements or deletions or insertions):
            break
        output = apply_edits(lines, replacements, deletions, insertions)
        updated = "\n".join(output) + ("\n" if output else "")
        if updated == text:
            break
        text = updated
    return text


def iter_files(root_paths, cwd=None):
    cwd = os.path.abspath(cwd or os.getcwd())
    for root_path in root_paths:
        if not os.path.isabs(root_path):
            root_path = os.path.join(cwd, root_path)
        if os.path.isfile(root_path):
            if (root_path.endswith(SUFFIXES)
                    and os.path.basename(root_path) not in EXCLUDE_FILES):
                yield root_path
            continue
        if not os.path.isdir(root_path):
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [name for name in dirnames if name not in EXCLUDE_DIRS]
            for name in sorted(filenames):
                if name in EXCLUDE_FILES or not name.endswith(SUFFIXES):
                    continue
                yield os.path.join(dirpath, name)


def rel(path, cwd):
    try:
        return os.path.relpath(path, cwd).replace(os.sep, "/").replace("\\", "/")
    except ValueError:
        return str(path).replace(os.sep, "/").replace("\\", "/")


def collect(root_paths, cwd=None):
    cwd = os.path.abspath(cwd or os.getcwd())
    violations = []
    for path in iter_files(root_paths, cwd):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError:
            continue
        display = rel(path, cwd)
        found, _replacements, _deletions, _insertions = analyze(display, text)
        violations.extend(found)
    return violations


def rewrite(paths, cwd=None):
    """Apply the mechanical rewrite in place; return changed file count."""
    cwd = os.path.abspath(cwd or os.getcwd())
    changed = 0
    for path in iter_files(paths, cwd):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        updated = fixpoint(rel(path, cwd), text)
        if updated == text:
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(updated)
        changed += 1
    return changed


def diff_report(paths, cwd=None):
    cwd = os.path.abspath(cwd or os.getcwd())
    chunks = []
    for path in iter_files(paths, cwd):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        updated = fixpoint(path, text)
        if updated == text:
            continue
        relative = rel(path, cwd)
        chunks.extend(difflib.unified_diff(
            text.splitlines(), updated.splitlines(),
            fromfile=f"a/{relative}", tofile=f"b/{relative}", lineterm=""))
        chunks.append("")
    return "\n".join(chunks)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="VexGraph structural layout (control flow)")
    parser.add_argument("--write", action="store_true",
                        help="apply the mechanical rewrite")
    parser.add_argument("--diff", action="store_true",
                        help="print a unified diff instead of a violation list")
    parser.add_argument("--json", action="store_true",
                        help="machine-readable violation report")
    parser.add_argument("--no-color", action="store_true",
                        help="accepted for symmetry with the linter; output is plain")
    parser.add_argument("--baseline", default=None,
                        help="ratchet against a recorded baseline")
    parser.add_argument("--write-baseline", default=None,
                        help="record the current violations as the baseline")
    parser.add_argument("paths", nargs="*", default=None,
                        help="roots to scan (defaults to the live workspace roots)")
    args = parser.parse_args(argv)

    roots = args.paths or [path for path in DEFAULT_ROOTS if os.path.isdir(path)]
    if not roots:
        print("arrange: no scannable roots; pass an explicit path", file=sys.stderr)
        return 2
    if args.baseline and args.write_baseline:
        print("arrange: choose --baseline or --write-baseline, not both",
              file=sys.stderr)
        return 2
    if sum(bool(flag) for flag in (args.write, args.diff)) > 1:
        print("arrange: choose one of --write or --diff", file=sys.stderr)
        return 2

    if args.write:
        changed = rewrite(roots)
        print(f"Rewrote {changed} file(s)")
        return 0
    if args.diff:
        text = diff_report(roots)
        if text:
            print(text, end="")
        return 1 if text else 0

    violations = collect(roots)
    if args.write_baseline:
        LINTER.save_baseline(args.write_baseline, violations)
        print(f"Recorded {len(violations)} violation(s) to {args.write_baseline}")
        return 0

    baseline = LINTER.load_baseline(args.baseline) if args.baseline else None
    new_counts, retired_counts, new_total, retired_total = (
        LINTER.ratchet_diff(violations, baseline) if baseline is not None
        else ({}, {}, 0, 0))

    if args.json:
        print(json.dumps({
            "total": len(violations),
            "by_rule": dict(Counter(v["rule"] for v in violations).most_common()),
            "violations": violations,
            "new_total": new_total,
            "retired_total": retired_total,
        }, indent=2))
    else:
        rule_counts = Counter(v["rule"] for v in violations)
        print(f"Arrangement violations: {len(violations)}")
        for rule, count in rule_counts.most_common():
            print(f"{count:6d}  {rule}")
        if baseline is not None:
            print(f"\nRatchet: {new_total} new, {retired_total} retired, "
                  f"{sum(baseline.values())} recorded debt")
            if new_total:
                print("\nNew debt:")
                for key, count in sorted(new_counts.items()):
                    print(f"{count:6d}  {key}")
        if args.baseline is None:
            print("\nUse --diff to inspect the rewrite or --write to apply it.")

    if args.baseline is not None:
        return 1 if new_total else 0
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
