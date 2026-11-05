#!/bin/sh
# code.sh — every C, Objective-C, header and Rust source concatenated into one
# file, with a header per file and a count at the end.
#
# The point is a single document you can read, search, or measure without
# opening a thousand files. Line numbers inside each file are preserved; the
# header tells you which file you are in and how long it is.
#
# usage: tools/code.sh [--out FILE] [--repo NAME] [--no-tests] [--ext c,h,m,rs]
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
workspace=$(dirname -- "$here")
territory="$workspace/vex"

out="$workspace/code.txt"
repo=""
extensions="c,h,m,rs"
with_tests=1

usage() {
    echo "usage: tools/code.sh [--out FILE] [--repo NAME] [--no-tests] [--ext c,h,m,rs]"
}

while [ $# -gt 0 ]; do
    case "$1" in
        --out) out=$2; shift 2 ;;
        --repo) repo=$2; shift 2 ;;
        --no-tests) with_tests=0; shift ;;
        --ext) extensions=$2; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "code.sh: unknown argument $1" >&2; usage >&2; exit 2 ;;
    esac
done

if [ -n "$repo" ]; then
    search_root="$territory/$repo"
    [ -d "$search_root" ] || { echo "code.sh: no repository at $search_root" >&2; exit 1; }
else
    search_root="$territory"
fi

[ -d "$search_root" ] || { echo "code.sh: no territory at $territory" >&2; exit 1; }

pattern=$(printf '%s' "$extensions" | tr ',' '|')

files=$(mktemp)
stats=$(mktemp)
trap 'rm -f "$files" "$stats"' EXIT

find "$search_root" \
    \( -name .git -o -name .b -o -name node_modules -o -name target \
       -o -name dist -o -name __pycache__ \) -prune -o \
    -type f -print 2>/dev/null |
    grep -E "\.($pattern)\$" | sort > "$files"

: > "$out"

total_files=0
total_lines=0
total_blank=0

while IFS= read -r file; do
    if [ "$with_tests" = 0 ]; then
        case "$file" in
            */test/*|*/tests/*) continue ;;
        esac
    fi

    lines=$(wc -l < "$file" | tr -d ' ')
    blank=$(grep -c '^[[:space:]]*$' "$file" 2>/dev/null || true)
    blank=${blank:-0}

    relative=${file#"$workspace"/}
    printf '// ===== %s (%s lines) =====\n' "$relative" "$lines" >> "$out"
    cat "$file" >> "$out"
    printf '\n' >> "$out"

    total_files=$((total_files + 1))
    total_lines=$((total_lines + lines))
    total_blank=$((total_blank + blank))

    name=${relative#"vex/"}
    name=${name%%/*}
    printf '%s %s\n' "$name" "$lines" >> "$stats"
done < "$files"

written=$(wc -c < "$out" | tr -d ' ')

printf 'files    %s\n' "$total_files"
printf 'lines    %s\n' "$total_lines"
printf 'code     %s (non-blank)\n' "$((total_lines - total_blank))"
printf 'blank    %s\n' "$total_blank"
printf 'bytes    %s\n' "$written"
printf 'output   %s\n' "$out"

printf '\nby repository (lines)\n'
awk '{ sum[$1] += $2 } END { for (name in sum) printf "%-24s %8d\n", name, sum[name] }' "$stats" |
    sort -k2 -rn | head -30

if [ -n "$repo" ]; then
    exit 0
fi

printf '\nlargest files\n'
while IFS= read -r file; do
    printf '%8s %s\n' "$(wc -l < "$file" | tr -d ' ')" "${file#"$workspace"/}"
done < "$files" | sort -rn | head -15
