#!/bin/bash

SESSION="demo_session"

# Kill existing session if it exists
tmux kill-session -t "$SESSION" 2>/dev/null

# Create new session with first window running a long-lived process
tmux new-session -d -s "$SESSION" -n "proc1" "sleep 9999"

# Create second window with another long-lived process
tmux new-window -t "$SESSION" -n "proc2" "sleep 9999"

echo "=== tmux session '$SESSION' started ==="
echo ""

# Show tmux session is running via ps
echo "=== ps -aux output (filtered for our session) ==="
ps -aux | head -1
ps -aux | grep "sleep 9999" | grep -v grep

echo ""
echo "=== PIDs for each tmux pane ==="

# Get PID of process running in pane 0 (proc1)
PID1=$(tmux list-panes -t "${SESSION}:proc1" -F "#{pane_pid}")
echo "Window 'proc1' (pane 0) PID: $PID1"

# Get PID of process running in pane 0 (proc2)
PID2=$(tmux list-panes -t "${SESSION}:proc2" -F "#{pane_pid}")
echo "Window 'proc2' (pane 0) PID: $PID2"

echo ""
echo "=== Verifying PIDs exist in process table ==="
echo "proc1 (PID $PID1):"
ps -p "$PID1" -o pid,ppid,cmd 2>/dev/null || echo "  PID $PID1 not found"

echo "proc2 (PID $PID2):"
ps -p "$PID2" -o pid,ppid,cmd 2>/dev/null || echo "  PID $PID2 not found"

echo ""
echo "=== Cleanup: killing session '$SESSION' ==="
tmux kill-session -t "$SESSION"
echo "Done."
