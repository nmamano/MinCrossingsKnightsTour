#!/bin/bash
# KT Structures 2026-10-04: which band period k costs least (2f, D=4, n=24 and 26).
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue4.sh" > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) PER=$PER $*" >> logs/queue5.log; $PY tmin.py "$@" >> logs/queue5.log 2>&1; }
for k in 2 4 6 8 12; do export PER=4,$k; run 26 2f 4 200 p26_2f_D4_k$k.json; done
export PER=6,10; run 26 2f 4 200 p26_2f_D4_a6k10.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue5.log
