#!/bin/bash
# KT Structures 2026-10-04: PER=8,10 with r = 0 on band cells (exact T - 8n under copying), then hinted tour runs.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue7.sh" > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) PER=$PER $*" >> logs/queue9.log; $PY tmin.py "$@" >> logs/queue9.log 2>&1; }
export PER=8,10
for n in 28 30 32 34 36; do run $n 2f 4 300 z${n}_2f_P810.json; done
for n in 28 30 32 34 36; do run $n tourlazy 4 900 z${n}_tour_P810.json; done
unset PER
run 22 tour 4 1200 h22_tour_D4.json r22_tour_D4.json
run 24 tour 4 1200 h24_tour_D4.json mrg/r24_2f_D4.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue9.log
