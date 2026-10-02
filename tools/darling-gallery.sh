cd ~/vexgraph
./tools/b build 2>&1 | tail -2
echo "=== suite ==="; ./tools/b test >/tmp/tc.log 2>&1; echo "exit=$?"; tail -1 /tmp/tc.log
echo
echo "=== launch the GPU-rendered gallery ==="
pgrep -x darling_gallery | xargs -r kill 2>/dev/null; sleep 1
./tools/b run darling_gallery 2>&1 | tail -1
sleep 4; echo "running: $(pgrep -x darling_gallery | head -1 || echo no)"