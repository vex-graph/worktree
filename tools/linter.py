#!/usr/bin/env python3
"""
tools/linter.py — Automated style & architectural compliance checker for vexgraph.
Enforces rules codified in preferences.md:
  - Rule 1: No arrow sugar (no '->', always '(*ptr).field')
  - Rule 2 & 16: Cast & pointer spacing ('(T*) var', 'T *name')
  - Rule 10: Two-layer access cap (flag 3+ layer member/deref chains)
  - Rule 17: Multi-repo architectural hierarchy (no upstream layer inversions)
  - Rule 18: Zero parent hops in includes (no '../')
  - Rule 23: ;;OVERVIEW presence & 4-tier section banners
"""

import os
import re
import sys
import argparse

# Terminal colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"

EXCLUDE_DIRS = {
    ".git", "build", "build-debug", "build-release",
    "cmake-build-debug", "cmake-build-release", "_build", "_out", "spv",
    "build-spoke", "build-vexspoke"
}
EXCLUDE_FILES = {"stb_truetype.h"}

def strip_comments_and_strings(line: str, in_multiline_comment: bool) -> tuple[str, bool]:
    """Strips comments and string literals from a C source line."""
    out = []
    i = 0
    n = len(line)

    while i < n:
        if in_multiline_comment:
            end = line.find("*/", i)
            if end != -1:
                in_multiline_comment = False
                i = end + 2
                continue
            else:
                break

        # Start of multi-line comment
        if i + 1 < n and line[i:i+2] == "/*":
            in_multiline_comment = True
            i += 2
            continue

        # Single-line comment
        if i + 1 < n and line[i:i+2] == "//":
            break

        # String literal
        if line[i] == '"':
            i += 1
            while i < n and line[i] != '"':
                if line[i] == '\\':
                    i += 2
                else:
                    i += 1
            i += 1
            out.append('""')
            continue

        # Character literal
        if line[i] == "'":
            i += 1
            while i < n and line[i] != "'":
                if line[i] == '\\':
                    i += 2
                else:
                    i += 1
            i += 1
            out.append("''")
            continue

        out.append(line[i])
        i += 1

    return "".join(out), in_multiline_comment

def find_lhs_backwards(s: str, arrow_pos: int) -> int:
    """Finds the start index of the LHS postfix-expression for -> at arrow_pos."""
    i = arrow_pos - 1
    while i >= 0 and s[i].isspace():
        i -= 1
    if i < 0:
        return arrow_pos

    while i >= 0:
        if s[i] == "]":
            depth = 1
            i -= 1
            while i >= 0 and depth > 0:
                if s[i] == "]": depth += 1
                elif s[i] == "[": depth -= 1
                i -= 1
            while i >= 0 and s[i].isspace(): i -= 1
            continue
        elif s[i] == ")":
            depth = 1
            i -= 1
            while i >= 0 and depth > 0:
                if s[i] == ")": depth += 1
                elif s[i] == "(": depth -= 1
                i -= 1
            while i >= 0 and s[i].isspace(): i -= 1
            if i >= 0 and (s[i].isalnum() or s[i] == "_"):
                while i >= 0 and (s[i].isalnum() or s[i] == "_"):
                    i -= 1
                while i >= 0 and s[i].isspace(): i -= 1
            continue
        elif s[i].isalnum() or s[i] == "_":
            while i >= 0 and (s[i].isalnum() or s[i] == "_"):
                i -= 1
            tmp = i
            while tmp >= 0 and s[tmp].isspace(): tmp -= 1
            if tmp >= 0 and s[tmp] == ".":
                i = tmp - 1
                while i >= 0 and s[i].isspace(): i -= 1
                continue
            else:
                break
        else:
            break

    return i + 1

def replace_line_arrows(line: str) -> str:
    """Transforms all 'expr->field' into '(*expr).field' outside comments and strings."""
    comment_pos = -1
    in_str = False
    for idx in range(len(line)):
        if line[idx] == '"' and (idx == 0 or line[idx-1] != '\\'):
            in_str = not in_str
        elif not in_str and idx + 1 < len(line) and line[idx:idx+2] == "//":
            comment_pos = idx
            break

    code_part = line[:comment_pos] if comment_pos != -1 else line
    comment_part = line[comment_pos:] if comment_pos != -1 else ""

    s = code_part
    while True:
        pos = s.find("->")
        if pos == -1:
            break
        rhs_match = re.match(r"^->\s*([A-Za-z_]\w*)", s[pos:])
        if not rhs_match:
            break
        rhs = rhs_match.group(1)
        rhs_len = len(rhs_match.group(0))
        lhs_start = find_lhs_backwards(s, pos)
        lhs = s[lhs_start:pos].strip()
        repl = f"(*{lhs}).{rhs}"
        s = s[:lhs_start] + repl + s[pos + rhs_len:]

    return s + comment_part

C_TYPES = (
    r"(?:void|char|short|int|long|float|double|uint8_t|uint16_t|uint32_t|uint64_t|"
    r"int8_t|int16_t|int32_t|int64_t|size_t|uintptr_t|intptr_t|bool|unsigned|signed|"
    r"unsigned\s+char|unsigned\s+short|unsigned\s+int|unsigned\s+long|"
    r"struct\s+[A-Za-z_]\w*|const\s+[A-Za-z_]\w*|[A-Za-z_]\w*)"
)

RE_CAST_SPACE_INSIDE = re.compile(rf"\(\s*({C_TYPES})\s+(\*+)\s*\)")
RE_CAST_NO_SPACE_AFTER = re.compile(rf"\(\s*({C_TYPES}\*+)\)([\w\(])")

def fix_cast_spacing(line: str) -> str:
    """Auto-fixes cast spacing: (T *) -> (T*) and (T*)var -> (T*) var."""
    line = RE_CAST_SPACE_INSIDE.sub(r"(\1\2)", line)
    line = RE_CAST_NO_SPACE_AFTER.sub(r"(\1) \2", line)
    return line

class Linter:
    def __init__(self, root_paths: list[str]):
        self.root_paths = root_paths
        self.violations = []
        self.files_scanned = 0

    def check_layer_inversion(self, filepath: str, line: str, lno: int) -> dict | None:
        """Enforces Rule 17: downward-only dependency hierarchy."""
        m = re.match(r'^\s*#include\s*["<]([^">]+)[">]', line)
        if not m:
            return None
        inc = m.group(1)

        # vexspoke is Layer 1: Leaf runtime
        if "projects/vexspoke" in filepath:
            prohibited = [
                "darling/", "hotcwap/", "window/", "hot/", "api/",
                "vulkan/vk_iosurface.h", "vulkan/vk_scene.h", "vulkan/vk_view.h", "vulkan/sdf_gpu.h"
            ]
            for p in prohibited:
                if inc.startswith(p):
                    return {
                        "rule": "Rule 17 (Layer Inversion)",
                        "file": filepath,
                        "line": lno,
                        "snippet": line.strip(),
                        "msg": f"vexspoke (L1 Leaf) includes downstream header '{inc}'"
                    }

        # hotcwap is Layer 2: OS Infrastructure
        if "projects/hotcwap" in filepath:
            prohibited = ["darling/", "api/"]
            for p in prohibited:
                if inc.startswith(p):
                    return {
                        "rule": "Rule 17 (Layer Inversion)",
                        "file": filepath,
                        "line": lno,
                        "snippet": line.strip(),
                        "msg": f"hotcwap (L2) includes downstream header '{inc}'"
                    }

        # darling-framework is R4 Interfaces: UI Toolkit
        if "projects/darling-framework" in filepath:
            prohibited = ["api/"]
            for p in prohibited:
                if inc.startswith(p):
                    return {
                        "rule": "Rule 17 (Layer Inversion)",
                        "file": filepath,
                        "line": lno,
                        "snippet": line.strip(),
                        "msg": f"darling-framework (R4) includes downstream header '{inc}'"
                    }

        return None

    def check_two_layer_cap(self, filepath: str, line: str, lno: int) -> dict | None:
        """Checks Rule 10: member/deref chain touches at most TWO layers deep."""
        if re.search(r'\(\*\(\*[A-Za-z_]\w*\)\.[A-Za-z_]\w*\)\.[A-Za-z_]\w*', line):
            return {
                "rule": "Rule 10 (Two-Layer Cap)",
                "file": filepath,
                "line": lno,
                "snippet": line.strip(),
                "msg": "Expression traverses 3+ layers deep (e.g. '(*(*a).b).c'). Hoist intermediate to local."
            }
        if re.search(r'\b[A-Za-z_]\w*\.[A-Za-z_]\w*\.[A-Za-z_]\w*\.[A-Za-z_]\w*', line):
            return {
                "rule": "Rule 10 (Two-Layer Cap)",
                "file": filepath,
                "line": lno,
                "snippet": line.strip(),
                "msg": "Expression traverses 3+ layers deep ('a.b.c.d'). Hoist intermediate to local."
            }
        return None

    def scan_file(self, filepath: str, fix: bool = False) -> list[dict]:
        file_violations = []
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        in_multiline = False
        has_overview = False
        new_lines = []
        modified = False

        for lno, raw_line in enumerate(lines, 1):
            stripped_code, in_multiline = strip_comments_and_strings(raw_line, in_multiline)

            # Check Rule 23: ;;OVERVIEW
            if lno <= 150 and ";;OVERVIEW" in raw_line:
                has_overview = True

            # Check Rule 17: Layer Inversion
            layer_viol = self.check_layer_inversion(filepath, raw_line, lno)
            if layer_viol:
                file_violations.append(layer_viol)

            # Check Rule 18: Canonical Includes (no '../')
            if re.match(r'^\s*#include\s*["<]\.\./', raw_line):
                file_violations.append({
                    "rule": "Rule 18 (Canonical Includes)",
                    "file": filepath,
                    "line": lno,
                    "snippet": raw_line.strip(),
                    "msg": "Prohibited '../' parent directory traversal in include path"
                })
                if fix:
                    fixed_inc = re.sub(r'#include\s*"\.\./src/([^"]+)"', r'#include "\1"', raw_line)
                    if fixed_inc != raw_line:
                        raw_line = fixed_inc
                        modified = True

            # Check Rule 1: No arrow sugar (->)
            if "->" in stripped_code:
                if re.search(r'->\s*[A-Za-z_]\w*', stripped_code):
                    file_violations.append({
                        "rule": "Rule 1 (No Arrow Sugar)",
                        "file": filepath,
                        "line": lno,
                        "snippet": raw_line.strip(),
                        "msg": "Found arrow operator '->'. Transform to '(*ptr).field'."
                    })
                    if fix:
                        fixed_line = replace_line_arrows(raw_line)
                        if fixed_line != raw_line:
                            raw_line = fixed_line
                            modified = True

            # Check Rule 2 & 16: Cast spacing
            m_space_inside = RE_CAST_SPACE_INSIDE.search(stripped_code)
            if m_space_inside:
                file_violations.append({
                    "rule": "Rule 16 (Cast Spacing)",
                    "file": filepath,
                    "line": lno,
                    "snippet": raw_line.strip(),
                    "msg": f"Space before '*' inside cast paren: '{m_space_inside.group(0)}', expected '(T*)'"
                })
                if fix:
                    fixed_cast = fix_cast_spacing(raw_line)
                    if fixed_cast != raw_line:
                        raw_line = fixed_cast
                        modified = True

            m_no_space = RE_CAST_NO_SPACE_AFTER.search(stripped_code)
            if m_no_space:
                file_violations.append({
                    "rule": "Rule 2 (Cast Spacing)",
                    "file": filepath,
                    "line": lno,
                    "snippet": raw_line.strip(),
                    "msg": f"Missing space after closing cast paren: '{m_no_space.group(0)}', expected '(T*) var'"
                })
                if fix:
                    fixed_cast = fix_cast_spacing(raw_line)
                    if fixed_cast != raw_line:
                        raw_line = fixed_cast
                        modified = True

            # Check Rule 10: Two-Layer Cap
            two_layer_viol = self.check_two_layer_cap(filepath, stripped_code, lno)
            if two_layer_viol:
                file_violations.append(two_layer_viol)

            new_lines.append(raw_line)

        # Check ;;OVERVIEW for standalone C implementation files
        if filepath.endswith((".c", ".m")) and not has_overview:
            if not any(x in filepath for x in ["test", "main/vk_test", "main/main", "CMakeLists"]):
                file_violations.append({
                    "rule": "Rule 23 (Living Overview)",
                    "file": filepath,
                    "line": 1,
                    "snippet": filepath,
                    "msg": "Missing ';;OVERVIEW' documentation header in first 150 lines"
                })

        if fix and modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        return file_violations

    def run(self, fix: bool = False, verbose: bool = False, filter_rule: str = None) -> int:
        print(f"{BOLD}{CYAN}=== VexGraph Architectural & Style Compliance Engine ==={RESET}")
        mode_str = f"{YELLOW}[AUTO-FIX MODE]{RESET}" if fix else f"{CYAN}[AUDIT MODE]{RESET}"
        print(f"Mode: {mode_str} | Target Paths: {', '.join(self.root_paths)}\n")

        all_violations = []
        for root_path in self.root_paths:
            for dirpath, _, filenames in os.walk(root_path):
                if any(ex in dirpath.split(os.sep) for ex in EXCLUDE_DIRS):
                    continue
                for fname in filenames:
                    if fname in EXCLUDE_FILES:
                        continue
                    if fname.endswith((".c", ".h", ".m")):
                        fpath = os.path.join(dirpath, fname)
                        self.files_scanned += 1
                        viols = self.scan_file(fpath, fix=fix)
                        if filter_rule:
                            viols = [v for v in viols if filter_rule.lower() in v["rule"].lower()]
                        all_violations.extend(viols)

        rule_counts = {}
        file_counts = {}
        for v in all_violations:
            rule = v["rule"]
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
            f = v["file"]
            file_counts[f] = file_counts.get(f, 0) + 1

        if verbose:
            for v in all_violations:
                print(f"{RED}✖ {v['rule']}{RESET} at {BOLD}{v['file']}:{v['line']}{RESET}")
                print(f"  {v['snippet']}")
                print(f"  {CYAN}↳ {v['msg']}{RESET}\n")

        print(f"Files scanned: {BOLD}{self.files_scanned}{RESET}")
        print(f"Total violations found: {BOLD}{RED if all_violations else GREEN}{len(all_violations)}{RESET}\n")

        if rule_counts:
            print(f"{BOLD}Breakdown by Rule:{RESET}")
            for rule, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
                print(f"  {RED}✖{RESET} {rule}: {BOLD}{count}{RESET}")
            print()

        if file_counts:
            print(f"{BOLD}Top Files with Violations:{RESET}")
            for fpath, count in sorted(file_counts.items(), key=lambda x: -x[1])[:10]:
                print(f"  {YELLOW}{count:3d}{RESET}  {fpath}")
            print()

        if not fix and all_violations:
            print(f"{YELLOW}Tip:{RESET} Run with {BOLD}--fix{RESET} to automatically refactor fixable violations (Rule 1 arrows, Rule 16 casts, Rule 18 includes).")

        return len(all_violations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VexGraph Style & Architectural Linter")
    parser.add_argument("--fix", action="store_true", help="Automatically fix fixable violations (arrow sugar, casts, includes)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print every violation line with snippet")
    parser.add_argument("--rule", type=str, default=None, help="Filter audit by specific rule name")
    parser.add_argument("paths", nargs="*", default=["projects/vexspoke", "projects/hotcwap", "projects/darling-framework", "projects/api-haven", "main"])
    args = parser.parse_args()

    linter = Linter(args.paths)
    count = linter.run(fix=args.fix, verbose=args.verbose, filter_rule=args.rule)
    sys.exit(0 if count == 0 or args.fix else 1)
