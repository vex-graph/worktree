#!/bin/bash
# tools/build_stripped.sh — release build with dead-code stripping + .app assembly.
#
# Proves the "unused getters/setters cost zero in the artifact" claim:
#   - compile: -O2 -ffunction-sections -fdata-sections (one section per symbol)
#   - link:    -Wl,-dead_strip (ld drops unreferenced sections)
# Without these flags the linker keeps every non-static function in each
# linked .o — including symmetric accessors nothing calls.
#
# Usage: ./tools/build_stripped.sh
# Output: _out/vktest-stripped.app (does NOT touch _out/vktest.app)
set -euo pipefail

CLION_CMAKE="/Applications/CLion.app/Contents/bin/cmake/mac/aarch64/bin/cmake"
if [ -x "$CLION_CMAKE" ]; then CMAKE="$CLION_CMAKE"; else CMAKE="$(command -v cmake)"; fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/build-stripped"
APP="$ROOT/_out/vktest-stripped.app"
BIN="vk_test"

echo "== configuring $BUILD_DIR (Release; dead-strip flags now live in CMakeLists) =="
"$CMAKE" -S "$ROOT" -B "$BUILD_DIR" -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Release

echo "== building $BIN =="
"$CMAKE" --build "$BUILD_DIR" --target "$BIN" -j "$(sysctl -n hw.ncpu)"

echo "== assembling $APP =="
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources/spv"

cp "$BUILD_DIR/$BIN" "$APP/Contents/MacOS/vktest"
cp "$BUILD_DIR/spv/"*.spv "$APP/Contents/Resources/spv/"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key><string>vktest-stripped</string>
    <key>CFBundleDisplayName</key><string>vktest (dead-stripped)</string>
    <key>CFBundleIdentifier</key><string>dev.vexgraph.vktest-stripped</string>
    <key>CFBundleExecutable</key><string>vktest</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
    <key>CFBundleShortVersionString</key><string>0.1.0</string>
    <key>CFBundleVersion</key><string>1</string>
    <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

echo "== size report =="
if [ -f "$ROOT/build-debug/$BIN" ]; then
    du -k "$ROOT/build-debug/$BIN" | awk '{printf "%8.1f KB  debug baseline (build-debug/vk_test)\n", $1}'
fi
du -k "$APP/Contents/MacOS/vktest" | awk '{printf "%8.1f KB  stripped executable\n", $1}'
ls "$APP/Contents/Resources/spv"/*.spv | wc -l | awk '{printf "%8d    shaders bundled (.spv count)\n", $1}'
du -sk "$APP" | awk '{printf "%8.1f KB  total bundle\n", $1}'
echo "== done: $APP =="
