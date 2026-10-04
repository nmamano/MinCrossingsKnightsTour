#!/bin/bash
# KT Structures 2026-10-04: periodic-band runs (PER=a,k) for extension by extend.py.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while ps -p 1911714 > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) PER=$PER $*" >> logs/queue4.log; $PY tmin.py "$@" >> logs/queue4.log 2>&1; }
export PER=4,10
run 22 2f 4 300 p22_2f_D4.json
run 22 tour 4 900 p22_tour_D4.json r22_tour_D4.json
run 24 2f 4 300 p24_2f_D4.json
run 24 tour 4 900 p24_tour_D4.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue4.log
