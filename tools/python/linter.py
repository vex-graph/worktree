#!/usr/bin/env python3
"""
tools/linter.py — automated style & architectural compliance checker for vexgraph.

Enforces laws codified in `PREFERENCES.md` (cite laws by Title, never number):
  - the Semantic Consistency Law: no arrow sugar, cast/pointer spelling,
    access depth, `nullptr` instead of `NULL`
  - the Vertical Integration Law: no upstream layer inversions
  - the Canonical Include Paths Law: no '../' parent traversal
  - the Living Documentation Law: `;;OVERVIEW` and `;;DEFINITION` on .c/.m
  - the No Section Sign Law: no U+00A7 in tracked text
  - the Two-Semicolon Annotation Style Law: markers start with `;;`

The linter is read-only. `--fix` is the sole mutating mode and it only rewrites
the mechanical subset (arrows, casts, `NULL`, control-flow spacing); it never
reflows layout. Structural arrangement lives in `tools/arrange.py`.

CI gates on a ratchet baseline so existing debt cannot grow:
  python3 tools/linter.py --baseline .github/lint-baseline.json
  python3 tools/linter.py --write-baseline .github/lint-baseline.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

# Terminal colors; disabled when stdout is not a tty or --no-color is passed.
_USE_COLOR = sys.stdout.isatty()

RED = "\033[31m" if _USE_COLOR else ""
GREEN = "\033[32m" if _USE_COLOR else ""
YELLOW = "\033[33m" if _USE_COLOR else ""
CYAN = "\033[36m" if _USE_COLOR else ""
BOLD = "\033[1m" if _USE_COLOR else ""
RESET = "\033[0m" if _USE_COLOR else ""

DEFAULT_ROOTS = (
    "vex",
    "tools",
)

# Roots whose text is scanned for the No Section Sign Law, beyond the source roots.
TEXT_ROOTS = ("../metadata/gists", ".github", "tools")

EXCLUDE_DIRS = {
    ".git", ".idea", "build", "build-debug", "build-release",
    "cmake-build-debug", "cmake-build-release", "_build", "_out", "spv",
    "build-spoke", "build-vexspoke", "_trash", "_notes", "node_modules",
}
EXCLUDE_FILES = {"stb_truetype.h"}

SOURCE_SUFFIXES = (".c", ".h", ".m", ".mm")
TEXT_SUFFIXES = (
    ".c", ".h", ".m", ".mm", ".cc", ".cpp", ".hpp", ".rs", ".py", ".ts",
    ".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".sh", ".cmake",
    ".js", ".html", ".css", ".sql", ".java", ".go", ".zig", ".swift",
)

SECTION_SIGN = "\u00a7"


def strip_comments_and_strings(line, in_multiline_comment):
    """Return (code, state): comments removed, literals blanked, same length."""
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
            break

        if i + 1 < n and line[i:i + 2] == "/*":
            in_multiline_comment = True
            i += 2
            continue

        if i + 1 < n and line[i:i + 2] == "//":
            break

        if line[i] == '"':
            i += 1
            while i < n and line[i] != '"':
                i += 2 if line[i] == "\\" else 1
            i += 1
            out.append('""')
            continue

        if line[i] == "'":
            i += 1
            while i < n and line[i] != "'":
                i += 2 if line[i] == "\\" else 1
            i += 1
            out.append("''")
            continue

        out.append(line[i])
        i += 1

    return "".join(out), in_multiline_comment


def rewrite_code(line, in_multiline_comment, transform):
    """Apply `transform` to code spans only, leaving comments and literals exact."""
    pieces = []
    code = []
    i = 0
    n = len(line)

    def flush():
        if code:
            pieces.append(transform("".join(code)))
            code.clear()

    while i < n:
        if in_multiline_comment:
            end = line.find("*/", i)
            if end == -1:
                pieces.append(line[i:])
                i = n
            else:
                pieces.append(line[i:end + 2])
                i = end + 2
                in_multiline_comment = False
            continue

        if i + 1 < n and line[i:i + 2] == "/*":
            flush()
            end = line.find("*/", i + 2)
            if end == -1:
                pieces.append(line[i:])
                in_multiline_comment = True
                i = n
            else:
                pieces.append(line[i:end + 2])
                i = end + 2
            continue

        if i + 1 < n and line[i:i + 2] == "//":
            flush()
            pieces.append(line[i:])
            i = n
            continue

        if line[i] == '"' or line[i] == "'":
            quote = line[i]
            flush()
            j = i + 1
            while j < n:
                if line[j] == "\\":
                    j += 2
                elif line[j] == quote:
                    j += 1
                    break
                else:
                    j += 1
            pieces.append(line[i:j])
            i = j
            continue

        code.append(line[i])
        i += 1

    flush()
    return "".join(pieces), in_multiline_comment


def find_lhs_backwards(s, arrow_pos):
    """Find the start index of the LHS postfix-expression for -> at arrow_pos."""
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
                if s[i] == "]":
                    depth += 1
                elif s[i] == "[":
                    depth -= 1
                i -= 1
            while i >= 0 and s[i].isspace():
                i -= 1
            continue
        elif s[i] == ")":
            depth = 1
            i -= 1
            while i >= 0 and depth > 0:
                if s[i] == ")":
                    depth += 1
                elif s[i] == "(":
                    depth -= 1
                i -= 1
            while i >= 0 and s[i].isspace():
                i -= 1
            if i >= 0 and (s[i].isalnum() or s[i] == "_"):
                while i >= 0 and (s[i].isalnum() or s[i] == "_"):
                    i -= 1
                while i >= 0 and s[i].isspace():
                    i -= 1
            continue
        elif s[i].isalnum() or s[i] == "_":
            while i >= 0 and (s[i].isalnum() or s[i] == "_"):
                i -= 1
            tmp = i
            while tmp >= 0 and s[tmp].isspace():
                tmp -= 1
            if tmp >= 0 and s[tmp] == ".":
                i = tmp - 1
                while i >= 0 and s[i].isspace():
                    i -= 1
                continue
            break
        else:
            break

    start = i + 1
    while start < arrow_pos and s[start].isspace():
        start += 1
    return start


def depth_violation(text):
    """Whether the access-depth checker would flag this text.

    Kept next to the fixer so a rewrite never trades an arrow finding for a
    depth finding. The regexes are defined below with the checker; Python
    resolves them at call time.
    """
    return bool(RE_POINTER_CHAIN.search(text) or RE_DOT_CHAIN.search(text)
                or RE_DEREF_CHAIN.search(text))


def replace_line_arrows(line):
    """Transform every mechanically safe 'expr->field' into '(*expr).field'.

    A rewrite is skipped when it would make the access-depth checker flag a
    line it did not flag before (for example `(*e).property->w` becoming
    `(*(*e).property).w`). Those need a hoisted local, not another dereference,
    so the arrow stays for manual work instead of trading one violation for
    another.
    """
    comment_pos = -1
    in_str = False
    for idx in range(len(line)):
        if line[idx] == '"' and (idx == 0 or line[idx - 1] != "\\"):
            in_str = not in_str
        elif not in_str and idx + 1 < len(line) and line[idx:idx + 2] == "//":
            comment_pos = idx
            break

    code_part = line[:comment_pos] if comment_pos != -1 else line
    comment_part = line[comment_pos:] if comment_pos != -1 else ""

    s = code_part
    search_from = 0
    while True:
        pos = s.find("->", search_from)
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
        candidate = s[:lhs_start] + repl + s[pos + rhs_len:]
        if depth_violation(candidate) and not depth_violation(s):
            search_from = pos + 2
            continue
        s = candidate
        search_from = lhs_start + len(repl)

    return s + comment_part


C_TYPES = (
    r"(?:void|char|short|int|long|f32|d64|u8|u16|u32|u64|"
    r"||i32|int64_t|bytes|pointer|intptr_t|bool|unsigned|signed|"
    r"unsigned\s+char|unsigned\s+short|unsigned\s+int|unsigned\s+long|"
    r"struct\s+[A-Za-z_]\w*|const\s+[A-Za-z_]\w*|[A-Za-z_]\w*)"
)

RE_CAST_SPACE_INSIDE = re.compile(rf"\(\s*({C_TYPES})\s+(\*+)\s*\)")
RE_CAST_NO_SPACE_AFTER = re.compile(rf"\(\s*({C_TYPES}\*+)\)([\w\(])")
RE_NULL = re.compile(r"\bNULL\b")
RE_DOT_CHAIN = re.compile(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){3,}\b")
RE_DEREF_CHAIN = re.compile(
    r"\(\*[^()\n]+\)\.[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+")
RE_POINTER_CHAIN = re.compile(r"\(\*\(\*[A-Za-z_]\w*\)\.[A-Za-z_]\w*\)\.[A-Za-z_]\w*")

# --- Relational Memory Law: the allocation site rule ----------------------
# Memory_alloc is the engine's general allocator. It is confined to the roles
# that own objects (core, plus the allocator itself in re) and, inside them, to
# constructors: a function that builds one instance and hands it back. Any
# other use is an allocation with no owner, which is what this rule forbids.
MEMORY_ALLOC_TIERS = (
    "vex/re/",                 # lifetime: the allocator itself
    "vex/vexspoke/",           # core
    "vex/determinant/",        # core
    "vex/graphvex/",           # core
    "vex/language/",           # core
    "vex/samplerate/",         # core
    "vex/darling/",            # core
    "vex/harness/",            # core
    "vex/sesh/",               # core
    "vex/job/",                # tool (not alloc-exempt)
)
RE_MEMORY_ALLOC = re.compile(r"\bMemory_alloc\s*\(")
RE_FUNCTION_DEF = re.compile(
    r"^\s*(?:static\s+|inline\s+|const\s+|extern\s+|_Noreturn\s+)*"
    r"[A-Za-z_][A-Za-z0-9_]*[\s\*]+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
CONTROL_WORDS = {"if", "for", "while", "switch", "return", "sizeof", "do", "else"}


# The only constructor is the one the Object() macro dispatches to: Class_N.
# A bare init() (or Class_init) is the one other entry point, for a final,
# non-constructable class. There is no third spelling.
CONSTRUCTOR_NAME = re.compile(r"[A-Z]\w*_[0-9]+")
FINAL_MARKER = ";;FINAL"
# Releasing memory is a documented act. It may happen in main, in a class's
# own teardown, or in a function the author marked ;;DECONSTRUCT. A behavior
# method may not free: whichever object owns the block releases it once, where
# the release is visible.
DECONSTRUCT_MARKER = ";;DECONSTRUCT"
RE_MEMORY_FREE = re.compile(r"\bMemory_free\s*\(")
RELEASE_SUFFIXES = ("_free", "_destroy", "_release", "_freeAll", "_destroyAll",
                    "_deconstruct")


# --- String Law: libc comparison and search -------------------------------
# strcmp/strncmp/strstr/strchr scan to a terminator that length-delimited text
# does not have, so they read past JSON views, mapped slices and bounded
# buffers. CharSequence owns the bounded implementations; no other file calls the
# libc forms.
RE_LIBC_STRING = re.compile(r"\b(strcmp|strncmp|strstr|strchr)\s*\(")
LIB_STRING_OWNERS = (
    "vex/vexspoke/primitive/char_sequence.c",
    "vex/vexspoke/primitive/vex-string.c",
)


def is_release_site(name):
    """main, a class teardown, or a constructor cleaning up its own failure."""
    return (name == "main" or name.startswith("free")
            or name.endswith(RELEASE_SUFFIXES) or is_constructor(name))
# The allocator implementation is the one place that may allocate freely: it
# is what Memory_alloc is, not a caller of it.
MEMORY_ALLOC_OWNER = "vex/re/nio/mem.c"


def is_constructor(name):
    """Class_N (what Object() dispatches to) or init(): the only allocators."""
    return (bool(CONSTRUCTOR_NAME.fullmatch(name)) or name == "init"
            or re.search(r"_init(?:[A-Z0-9_]|$)", name) is not None)



def fix_cast_spacing(line):
    """Auto-fix cast spacing: (T *) -> (T*) and (T*)var -> (T*) var."""
    line = RE_CAST_SPACE_INSIDE.sub(r"(\1\2)", line)
    line = RE_CAST_NO_SPACE_AFTER.sub(r"(\1) \2", line)
    return line


def is_test_path(rel):
    return ("/tests/" in f"/{rel}/" or rel.startswith("tests/")
            or rel.rsplit("/", 1)[-1].endswith("_test.c")
            or rel.rsplit("/", 1)[-1].endswith("_test.m"))


class Linter:
    def __init__(self, root_paths, cwd=None):
        self.root_paths = list(root_paths)
        self.cwd = os.path.abspath(cwd or os.getcwd())
        self.files_scanned = 0
        self.files_would_fix = 0
        self.text_scanned = 0

    def rel(self, path):
        try:
            return os.path.relpath(path, self.cwd).replace(os.sep, "/").replace("\\", "/")
        except ValueError:
            return str(path).replace(os.sep, "/").replace("\\", "/")

    def violation(self, rule, path, line, snippet, msg, fixable=False):
        return {
            "rule": rule,
            "file": path,
            "line": line,
            "snippet": snippet.strip(),
            "msg": msg,
            "fixable": fixable,
        }

    def check_layer_inversion(self, rel, line, lno):
        """Enforce the Vertical Integration Law: downward-only dependencies."""
        m = re.match(r'^\s*#include\s*["<]([^">]+)[">]', line)
        if not m:
            return None
        inc = m.group(1)

        tiers = (
            ("vex/lifetime/",
             ["darling/", "api/", "hot/"],
             "lifetime (substrate)"),
            ("vex/re/",
             ["darling/", "hotcwap/", "window/", "hot/", "api/"],
             "lifetime (allocator/storage)"),
            ("vex/vexspoke/",
             ["darling/", "hotcwap/", "window/", "hot/", "api/",
              "vulkan/vk_iosurface.h", "vulkan/vk_scene.h",
              "vulkan/vk_view.h", "vulkan/sdf_gpu.h"],
             "core (compute)"),
            ("vex/darling/",
             ["api/"],
             "core (UI)"),
        )
        for prefix, prohibited, label in tiers:
            if not rel.startswith(prefix):
                continue
            for p in prohibited:
                if inc.startswith(p):
                    return self.violation(
                        "Vertical Integration Law (Layer Inversion)",
                        rel, lno, line,
                        f"{label} includes downstream header '{inc}'")
        return None

    def scan_file(self, path, fix=False, dry_run=False):
        rel = self.rel(path)
        violations = []
        has_overview = False
        has_definition = False
        new_lines = []
        modified = False

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError as exc:
            return [self.violation("Read error", rel, 0, "", str(exc))]

        is_final = any(FINAL_MARKER in line for line in lines[:150])
        is_deconstruct = any(DECONSTRUCT_MARKER in line for line in lines[:150])
        in_multiline = False
        function = ""
        function_floor = 0
        pending = ""
        depth = 0
        for lno, raw_line in enumerate(lines, 1):
            state_before = in_multiline
            code, in_multiline = strip_comments_and_strings(raw_line, in_multiline)

            definition = RE_FUNCTION_DEF.match(code)
            if definition and not function and definition.group(1) not in CONTROL_WORDS:
                pending = definition.group(1)
            active = function or pending

            # A prototype names Memory_alloc but calls nothing: skip it.
            declaration = (
                definition is not None and definition.group(1) == "Memory_alloc"
            )
            if (RE_MEMORY_ALLOC.search(code) and not declaration
                    and not is_test_path(rel)
                    and rel != MEMORY_ALLOC_OWNER):
                if not rel.startswith(MEMORY_ALLOC_TIERS):
                    violations.append(self.violation(
                        "Relational Memory Law (Allocation site)", rel, lno,
                        raw_line,
                        f"Memory_alloc is confined to core roles "
                        f"(found in '{active or 'file scope'}')"))
                elif not is_final and not is_constructor(active):
                    violations.append(self.violation(
                        "Relational Memory Law (Allocation site)", rel, lno,
                        raw_line,
                        f"Memory_alloc outside the Object() constructor or "
                        f"init() (found in '{active or 'file scope'}')"))

            if (RE_MEMORY_FREE.search(code) and not is_test_path(rel)
                    and rel != MEMORY_ALLOC_OWNER and not is_deconstruct
                    and not is_release_site(active)):
                violations.append(self.violation(
                    "Relational Memory Law (Release site)", rel, lno, raw_line,
                    f"Memory_free outside main, a teardown, or ;;DECONSTRUCT "
                    f"(found in '{active or 'file scope'}')"))

            libc_string = RE_LIBC_STRING.search(code)
            if (libc_string and not is_test_path(rel)
                    and rel not in LIB_STRING_OWNERS):
                violations.append(self.violation(
                    "String Law (libc string call)", rel, lno, raw_line,
                    f"'{libc_string.group(1)}' is unbounded; use CharSequence_compare, "
                    f"CharSequence_find or CharSequence_findChar"))

            if lno <= 150:
                if ";;OVERVIEW" in raw_line:
                    has_overview = True
                if ";;DEFINITION" in raw_line:
                    has_definition = True

            layer = self.check_layer_inversion(rel, raw_line, lno)
            if layer:
                violations.append(layer)

            if re.match(r'^\s*#include\s*["<]\.\./', raw_line):
                violations.append(self.violation(
                    "Canonical Include Paths Law", rel, lno, raw_line,
                    "Prohibited '../' parent directory traversal in include path",
                    fixable=True))
                if fix:
                    fixed = re.sub(r'#include\s*"\.\./src/([^"]+)"',
                                   r'#include "\1"', raw_line)
                    if fixed != raw_line:
                        raw_line, modified = fixed, True

            if "->" in code and re.search(r"->\s*[A-Za-z_]\w*", code):
                fixed_line = replace_line_arrows(raw_line)
                violations.append(self.violation(
                    "Semantic Consistency Law (Reference form)", rel, lno,
                    raw_line, "Found arrow operator '->'. Use '(*ptr).field'.",
                    fixable=fixed_line != raw_line))
                if fix and fixed_line != raw_line:
                    raw_line, modified = fixed_line, True

            m_space_inside = RE_CAST_SPACE_INSIDE.search(code)
            if m_space_inside:
                violations.append(self.violation(
                    "Semantic Consistency Law (Cast and pointer spelling)",
                    rel, lno, raw_line,
                    f"Space before '*' inside cast paren: '{m_space_inside.group(0)}'",
                    fixable=True))
                if fix:
                    fixed = fix_cast_spacing(raw_line)
                    if fixed != raw_line:
                        raw_line, modified = fixed, True

            m_no_space = RE_CAST_NO_SPACE_AFTER.search(code)
            if m_no_space:
                violations.append(self.violation(
                    "Semantic Consistency Law (Cast and pointer spelling)",
                    rel, lno, raw_line,
                    f"Missing space after cast paren: '{m_no_space.group(0)}'",
                    fixable=True))
                if fix:
                    fixed = fix_cast_spacing(raw_line)
                    if fixed != raw_line:
                        raw_line, modified = fixed, True

            if RE_NULL.search(code):
                violations.append(self.violation(
                    "Semantic Consistency Law (Cast and pointer spelling)",
                    rel, lno, raw_line,
                    "'NULL' is not C23; use 'nullptr'", fixable=True))
                if fix:
                    fixed, _ = rewrite_code(
                        raw_line, state_before,
                        lambda s: RE_NULL.sub("nullptr", s))
                    if fixed != raw_line:
                        raw_line, modified = fixed, True

            chain = self.check_two_layer_cap(rel, code, lno, raw_line)
            if chain:
                violations.append(chain)

            opens = code.count("{")
            closes = code.count("}")
            if not function and pending and opens > 0:
                function = pending
                function_floor = depth
                pending = ""
            depth += opens - closes
            if function and depth <= function_floor:
                function = ""

            new_lines.append(raw_line)

        if path.endswith((".c", ".m")) and not is_test_path(rel):
            if not has_overview:
                violations.append(self.violation(
                    "Living Documentation Law", rel, 1, rel,
                    "Missing ';;OVERVIEW' in the first 150 lines"))
            if not has_definition:
                violations.append(self.violation(
                    "Living Documentation Law", rel, 1, rel,
                    "Missing ';;DEFINITION' in the first 150 lines"))

        if fix and modified and dry_run:
            self.files_would_fix += 1

        if fix and modified and not dry_run:
            try:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.writelines(new_lines)
            except OSError as exc:
                violations.append(self.violation(
                    "Write error", rel, 0, "", str(exc)))

        return violations

    def check_two_layer_cap(self, rel, code, lno, raw_line):
        """Enforce the Semantic Consistency Law (Access depth)."""
        if RE_POINTER_CHAIN.search(code):
            return self.violation(
                "Semantic Consistency Law (Access depth)", rel, lno, raw_line,
                "Expression traverses 3+ pointer layers; hoist a local.")
        if RE_DOT_CHAIN.search(code) or RE_DEREF_CHAIN.search(code):
            return self.violation(
                "Semantic Consistency Law (Access depth)", rel, lno, raw_line,
                "Member chain traverses 3+ layers; hoist a local.")
        return None

    def scan_text(self):
        """No Section Sign Law: U+00A7 is forbidden in tracked text."""
        violations = []
        seen = set()
        for root in dict.fromkeys(self.root_paths + list(TEXT_ROOTS)):
            if not os.path.isabs(root):
                root = os.path.join(self.cwd, root)
            if not os.path.isdir(root):
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
                for fname in sorted(filenames):
                    if not fname.endswith(TEXT_SUFFIXES):
                        continue
                    path = os.path.join(dirpath, fname)
                    real = os.path.realpath(path)
                    if real in seen or fname in EXCLUDE_FILES:
                        continue
                    seen.add(real)
                    try:
                        if os.path.getsize(path) > 8 * 1024 * 1024:
                            continue
                        with open(path, "r", encoding="utf-8",
                                  errors="ignore") as f:
                            for lno, line in enumerate(f, 1):
                                if SECTION_SIGN in line:
                                    self.text_scanned += 1
                                    violations.append(self.violation(
                                        "No Section Sign Law", self.rel(path),
                                        lno, line,
                                        "U+00A7 is forbidden; write 'section'"))
                                    break
                    except OSError:
                        continue
        return violations

    def collect(self, fix=False, dry_run=False, filter_rule=None):
        violations = []
        for root_path in self.root_paths:
            if not os.path.isabs(root_path):
                root_path = os.path.join(self.cwd, root_path)
            if not os.path.isdir(root_path):
                continue
            for dirpath, dirnames, filenames in os.walk(root_path):
                dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
                for fname in sorted(filenames):
                    if fname in EXCLUDE_FILES:
                        continue
                    if not fname.endswith(SOURCE_SUFFIXES):
                        continue
                    fpath = os.path.join(dirpath, fname)
                    self.files_scanned += 1
                    violations.extend(self.scan_file(fpath, fix=fix, dry_run=dry_run))

        violations.extend(self.scan_text())
        if filter_rule:
            needle = filter_rule.lower()
            violations = [v for v in violations if needle in v["rule"].lower()]
        return violations


def load_baseline(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError(f"{path}: unsupported baseline format")
    return {str(k): int(v) for k, v in data.get("counts", {}).items()}


def save_baseline(path, violations):
    counts = Counter(f"{v['file']}::{v['rule']}" for v in violations)
    data = {
        "version": 1,
        "note": "Ratchet baseline: CI fails only when a file/rule count grows.",
        "total": len(violations),
        "counts": {k: counts[k] for k in sorted(counts)},
    }
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")


def summarize(violations):
    rule_counts = Counter(v["rule"] for v in violations)
    repo_counts = Counter()
    for v in violations:
        parts = v["file"].split("/")
        repo_counts["/".join(parts[:3]) if parts[0] == "suite" else parts[0]] += 1
    return rule_counts, repo_counts


def ratchet_diff(violations, baseline):
    counts = Counter(f"{v['file']}::{v['rule']}" for v in violations)
    new = {k: counts[k] - baseline.get(k, 0)
           for k in counts if counts[k] > baseline.get(k, 0)}
    retired = {k: baseline[k] for k in baseline if counts.get(k, 0) < baseline[k]}
    return new, retired, sum(new.values()), sum(retired.values())


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="VexGraph style & architectural linter")
    parser.add_argument("--fix", action="store_true",
                        help="rewrite the mechanical subset (arrows, casts, NULL, spacing)")
    parser.add_argument("--dry-run", action="store_true",
                        help="with --fix: report what would be rewritten, write nothing")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="print every violation with its snippet")
    parser.add_argument("--rule", default=None, help="filter by rule title")
    parser.add_argument("--json", action="store_true",
                        help="machine-readable report on stdout")
    parser.add_argument("--baseline", default=None,
                        help="ratchet against a recorded baseline; fail only on new debt")
    parser.add_argument("--write-baseline", default=None,
                        help="record the current violations as the ratchet baseline")
    parser.add_argument("--no-color", action="store_true",
                        help="disable ANSI colors")
    parser.add_argument("paths", nargs="*", default=None,
                        help="roots to scan (defaults to the live workspace roots)")
    args = parser.parse_args(argv)

    if args.no_color:
        global RED, GREEN, YELLOW, CYAN, BOLD, RESET
        RED = GREEN = YELLOW = CYAN = BOLD = RESET = ""

    roots = args.paths or [p for p in DEFAULT_ROOTS if os.path.isdir(p)]
    if not roots:
        print("linter: no scannable roots; pass an explicit path", file=sys.stderr)
        return 2
    if args.baseline and args.write_baseline:
        print("linter: choose --baseline or --write-baseline, not both",
              file=sys.stderr)
        return 2

    linter = Linter(roots)
    if args.dry_run and not args.fix:
        print("linter: --dry-run only makes sense with --fix", file=sys.stderr)
        return 2
    violations = linter.collect(fix=args.fix, dry_run=args.dry_run, filter_rule=args.rule)
    rule_counts, repo_counts = summarize(violations)

    if args.write_baseline:
        save_baseline(args.write_baseline, violations)
        if not args.json:
            print(f"{BOLD}{CYAN}Recorded {len(violations)} violation(s) "
                  f"to {args.write_baseline}{RESET}")
        return 0

    baseline = load_baseline(args.baseline) if args.baseline else None
    new_counts, retired_counts, new_total, retired_total = (
        ratchet_diff(violations, baseline) if baseline is not None
        else ({}, {}, 0, 0))

    if args.json:
        report = {
            "files_scanned": linter.files_scanned,
            "files_would_fix": linter.files_would_fix,
            "total": len(violations),
            "by_rule": dict(rule_counts.most_common()),
            "by_repo": dict(repo_counts.most_common()),
            "violations": violations,
        }
        if baseline is not None:
            report["baseline"] = {
                "new": new_total,
                "retired": retired_total,
                "new_by_key": dict(sorted(new_counts.items())),
            }
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(f"{BOLD}{CYAN}=== VexGraph Architectural & Style Compliance ==={RESET}")
        mode = f"{YELLOW}[FIX]{RESET}" if args.fix else f"{CYAN}[AUDIT]{RESET}"
        print(f"Mode: {mode} | Roots: {', '.join(roots)}\n")

        if args.verbose:
            for v in violations:
                print(f"{RED}x {v['rule']}{RESET} at "
                      f"{BOLD}{v['file']}:{v['line']}{RESET}")
                print(f"  {v['snippet']}")
                print(f"  {CYAN}-> {v['msg']}{RESET}\n")

        print(f"Source files scanned: {BOLD}{linter.files_scanned}{RESET}")
        print(f"Files carrying U+00A7: {BOLD}{linter.text_scanned}{RESET}")
        color = GREEN if not violations else RED
        print(f"Total violations: {BOLD}{color}{len(violations)}{RESET}\n")

        if rule_counts:
            print(f"{BOLD}By rule:{RESET}")
            for rule, count in rule_counts.most_common():
                print(f"  {RED}x{RESET} {rule}: {BOLD}{count}{RESET}")
            print()
        if repo_counts:
            print(f"{BOLD}By repo:{RESET}")
            for repo, count in repo_counts.most_common(12):
                print(f"  {YELLOW}{count:6d}{RESET}  {repo}")
            print()

        if baseline is not None:
            color = GREEN if new_total == 0 else RED
            print(f"Ratchet: {BOLD}{color}{new_total} new{RESET}, "
                  f"{retired_total} retired, "
                  f"{sum(baseline.values())} recorded debt")
            for key, count in sorted(new_counts.items())[:20]:
                print(f"  {RED}+{count}{RESET} {key}")
            print()

        if not args.fix and not violations and baseline is None:
            print(f"{GREEN}No violations found.{RESET}")
        elif not args.fix:
            print(f"{YELLOW}Tip:{RESET} `--fix` rewrites the mechanical subset; "
                  f"`tools/arrange.py` handles layout.")

    if args.fix:
        return 0
    if baseline is not None:
        return 1 if new_total else 0
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
