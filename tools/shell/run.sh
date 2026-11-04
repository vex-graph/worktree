#!/bin/sh
# tools/shell/run.sh — build ONE unit through b, then launch it as a real .app
# so macOS lets it activate its window (a shell-launched binary is denied focus).
#
# A unit is a directory carrying a b.assembly.json. b builds it into
# <unit>/.b/out/<application.name>; this script wraps that binary in a minimal
# bundle and hands it to LaunchServices.
#
#   tools/shell/run.sh darling-framework/test/compositor
#   tools/shell/run.sh darling-framework/test/compositor --wait
#
# --wait blocks until the application exits and then prints its output. Without
# it the app is launched and this script returns, which is what an interactive
# window wants.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "$here" in
    */scripts|*/shell) root=$(CDPATH= cd -- "$here/../.." && pwd) ;;
    *)                 root=$(CDPATH= cd -- "$here/.." && pwd) ;;
esac

target="${1:-}"
wait_for_exit=0
case "${2:-}" in
    --wait) wait_for_exit=1 ;;
esac

if [ -z "$target" ]; then
    echo "run.sh: name a unit directory, e.g. darling-framework/test/compositor" >&2
    exit 1
fi

# Paths are workspace-relative, like every other tool here.
cd "$root"

# Accept either a unit directory or a path inside one.
unit="$target"
while [ ! -f "$unit/b.assembly.json" ]; do
    parent=$(dirname "$unit")
    if [ "$parent" = "$unit" ] || [ "$parent" = "." ]; then
        echo "run.sh: no b.assembly.json above $target" >&2
        exit 1
    fi
    unit="$parent"
done
unit=$(CDPATH= cd -- "$unit" && pwd)

name=$(python3 - "$unit/b.assembly.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1]))["application"]["name"])
PY
)

echo "run.sh -> b build $name  ($unit)"
( cd "$unit" && "$root/tools/b" build "$name" )

# Output is territory-grounded: find the claimed root above the unit.
territory="$unit"
while [ ! -f "$territory/.b/workspace.json" ]; do
    parent=$(dirname "$territory")
    if [ "$parent" = "$territory" ]; then
        echo "run.sh: no .b/workspace.json above $unit" >&2
        exit 1
    fi
    territory="$parent"
done

binary="$territory/.b/out/$name"
[ -x "$binary" ] || { echo "run.sh: no binary at $binary" >&2; exit 1; }

app="$territory/.b/out/$name.app"
log="$territory/.b/out/$name.log"
rm -rf "$app"
mkdir -p "$app/Contents/MacOS"
cat > "$app/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
    <key>CFBundleName</key><string>$name</string>
    <key>CFBundleExecutable</key><string>$name</string>
    <key>CFBundleIdentifier</key><string>com.vexgraph.run.$name</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>NSHighResolutionCapable</key><true/>
</dict></plist>
PLIST
cat > "$app/Contents/MacOS/$name" <<LAUNCHER
#!/bin/sh
exec "$binary" >>"$log" 2>&1
LAUNCHER
chmod +x "$app/Contents/MacOS/$name"

# The bundle is the launch surface; the binary inside it is the same artifact
# b produced, so the .app and the unit never drift.
echo "run.sh -> $app"
if [ "$wait_for_exit" = 1 ]; then
    : >"$log"
    open -W "$app" || true
    echo "--- $name output ---"
    cat "$log" 2>/dev/null || true
else
    open "$app"
    echo "run.sh: launched; output goes to $log"
fi
