#!/bin/bash
# KT Structures 2026-10-04: second queue; starts after queue1 ends. Exact 2f bounds with hints, n=14 tour D4.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f queue1.sh > /dev/null; do sleep 20; done
run(){ echo "== $(date -u +%H:%M:%S) $*" >> logs/queue2.log; $PY tmin.py "$@" >> logs/queue2.log 2>&1; }
run 14 tour 4 600 r14_tour_D4.json
run 18 2f 0 900 r18_2f_D0.json r18_tour_D4.json
run 20 2f 0 900 r20_2f_D0.json r20_tour_D4.json
run 22 tour 4 600 r22_tour_D4.json
run 22 2f 4 300 r22_2f_D4.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue2.log
