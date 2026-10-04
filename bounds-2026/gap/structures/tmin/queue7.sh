#!/bin/bash
# KT Structures 2026-10-04: band-periodic 2f (PER=8,10) for extension + merge, all residues of n mod 10.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue6.sh" > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) PER=$PER $*" >> logs/queue7.log; $PY tmin.py "$@" >> logs/queue7.log 2>&1; }
export PER=8,10
for n in 28 30 32 34 36; do run $n 2f 4 300 q${n}_2f_P810.json; done
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue7.log
