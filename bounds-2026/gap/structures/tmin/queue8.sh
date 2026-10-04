#!/bin/bash
# KT Structures 2026-10-04: tours by AddCircuit with the best known tour as hint (D=4), longer limits.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue[67].sh" > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) $*" >> logs/queue8.log; $PY tmin.py "$@" >> logs/queue8.log 2>&1; }
run 22 tour 4 1200 h22_tour_D4.json r22_tour_D4.json
run 24 tour 4 1200 h24_tour_D4.json mrg/r24_2f_D4.json
run 26 tour 4 1200 h26_tour_D4.json fam/p26_2f_D4_a6k10_t0.json
run 28 tour 4 1200 h28_tour_D4.json r28_tour_D4.json
run 32 tour 4 1200 h32_tour_D4.json r32_tour_D4.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue8.log
