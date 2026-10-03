#!/bin/bash
# KT Structures 2026-10-04: sequential T_min queue, 2 CP-SAT workers total.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
run(){ echo "== $(date -u +%H:%M:%S) $*" >> logs/queue1.log; $PY tmin.py "$@" >> logs/queue1.log 2>&1; }
run 16 2f 0 600 r16_2f_D0.json r16_tour_D4.json
run 14 2f 0 600 r14_2f_D0.json
run 14 tour 0 600 r14_tour_D0.json
for n in 18 20 24 28 32; do run $n tour 4 600 r${n}_tour_D4.json; run $n 2f 4 300 r${n}_2f_D4.json; done
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue1.log
