#!/bin/bash
# tools/make_code_txt.sh — compile the codebase into a single code_2.txt.
#
# Usage: ./tools/make_code_txt.sh [output_file]
#   Default output: code_2.txt at the workspace root.
#
# Includes: preferences.md, CONTRIBUTING.md files, and all .md / .c / .h /
#           .m / .frag / .vert / .comp sources — including _main/vk_test.c
#           and _main/darling_gallery.c.
# Excludes: _docs, _thoughts, .git, build/output dirs, IDE caches.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CWD="$(pwd)"
if [ $# -ge 1 ]; then
    case "$1" in
        /*) OUT="$1" ;;
        *) OUT="$CWD/$1" ;;
    esac
else
    OUT="$ROOT/code.txt"
fi
cd "$ROOT" || exit 1

# Directories pruned from the walk (mechanical excludes + user excludes).
PRUNE=( "./_bugs" "./.opencode" "./.git" "./_docs" "./_thoughts" "./_build" "./_out" "./build" "./build-debug" "./build-release" "./build-stripped" "./build-vexspoke" "./cmake-build-debug" "./.idea" "./tools/__pycache__" )

PRUNE_ARGS=()
for d in "${PRUNE[@]}"; do
    PRUNE_ARGS+=( -path "$d" -prune -o )
done

TMP_LIST="$(mktemp)"
trap 'rm -f "$TMP_LIST"' EXIT

# shellcheck disable=SC2086
find -L . ${PRUNE_ARGS[@]} -type f \
    \( -name "preferences.md" -o -name "CONTRIBUTING.md" -o -name "*.md" \
     -o -name "*.c" -o -name "*.h" -o -name "*.m" \
     -o -name "*.frag" -o -name "*.vert" -o -name "*.comp" \) \
    -print0 | LC_ALL=C sort -z | tr '\0' '\n' | sed 's|^\./||' > "$TMP_LIST"

# Drop the output file itself if it lives in-tree and would otherwise match.
OUT_REL="${OUT#$ROOT/}"
grep -vxF "$OUT_REL" "$TMP_LIST" > "$TMP_LIST.filtered" || true
mv "$TMP_LIST.filtered" "$TMP_LIST"

FILE_COUNT="$(wc -l < "$TMP_LIST" | tr -d ' ')"
echo "Compiling $FILE_COUNT files into $OUT ..."

{
    echo "CODE.TXT — vexgraph workspace snapshot"
    echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "Files: $FILE_COUNT (preferences.md, CONTRIBUTING.md, .md/.c/.h/.m/.frag/.vert/.comp; excludes _docs, _thoughts, .git, build dirs)"
    echo ""
    while IFS= read -r f; do
        [ -n "$f" ] || continue
        lines="$(wc -l < "$ROOT/$f" | tr -d ' ')"
        echo "================================================================================"
        echo "FILE: $f ($lines lines)"
        echo "================================================================================"
        cat "$ROOT/$f"
        echo ""
    done < "$TMP_LIST"
} > "$OUT"

TOTAL="$(wc -l < "$OUT" | tr -d ' ')"
echo "Wrote $OUT ($TOTAL lines total, $FILE_COUNT source files)."
