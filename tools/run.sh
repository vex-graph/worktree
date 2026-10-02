#!/bin/sh
# tools/run.sh — build ONE target through b, then launch it as a real .app so
# macOS lets it activate its window (a shell-launched binary is denied focus).
#
# Usage:
#   tools/run.sh <target>
#   tools/run.sh tests/darling/frame/liquid_glass_frame_test.c   (name derived)
#
# Or edit TARGET below and run with no argument.
TARGET="${1:-panel_test}"

set -e
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

case "$TARGET" in
    *.c) TARGET="$(basename "$TARGET")"; TARGET="${TARGET%.c}" ;;
esac

echo "run.sh -> b build $TARGET"
"$root/tools/b" build "$TARGET"

state="${B_HOME:-$HOME/Library/Application Support/vexgraph/b}"
bin="$state/out/debug/bin/$TARGET"
app="$state/out/debug/apps/$TARGET.app"

# b already bundles real app targets as .app — just open that.
if [ -x "$app/Contents/MacOS/$TARGET" ] && [ ! -f "$bin" ]; then
    echo "run.sh -> open $app"
    exec open -W "$app"
fi

[ -x "$bin" ] || { echo "run.sh: no binary for '$TARGET' in $state/out/debug/bin"; exit 1; }

# Wrap the plain test binary in a minimal .app so LaunchServices runs it as a
# foreground application (it can then activate). A tiny launcher tees its
# stdout/stderr to a log we print once it exits.
log="$state/out/debug/$TARGET.log"
rm -rf "$app"
mkdir -p "$app/Contents/MacOS"
cat > "$app/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
    <key>CFBundleName</key><string>$TARGET</string>
    <key>CFBundleExecutable</key><string>$TARGET</string>
    <key>CFBundleIdentifier</key><string>com.vexgraph.run.$TARGET</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>NSHighResolutionCapable</key><true/>
</dict></plist>
PLIST
cat > "$app/Contents/MacOS/$TARGET" <<LAUNCHER
#!/bin/sh
exec "$bin" >"$log" 2>&1
LAUNCHER
chmod +x "$app/Contents/MacOS/$TARGET"

echo "run.sh -> open $app"
open -W "$app" || true
echo "--- $TARGET output ---"
cat "$log" 2>/dev/null || true
