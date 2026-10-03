#!/bin/bash
# run_wd.sh LOG LIMIT_GB cmd... : run cmd with output to LOG; kill it by PID if its RSS exceeds LIMIT_GB.
LOG=$1; LIM=$2; shift 2
/usr/bin/time -v "$@" > "$LOG" 2>&1 &
TP=$!
sleep 1
CP=$(pgrep -P $TP | head -1)
while kill -0 $TP 2>/dev/null; do
  if [ -n "$CP" ] && [ -r /proc/$CP/status ]; then
    R=$(awk '/VmRSS/{print $2}' /proc/$CP/status)
    if [ -n "$R" ] && [ "$R" -gt $((LIM*1024*1024)) ]; then echo "WATCHDOG: killed PID $CP at RSS ${R} kB" >> "$LOG"; kill $CP; fi
  fi
  sleep 2
done
wait $TP; echo "exit=$?" >> "$LOG"
