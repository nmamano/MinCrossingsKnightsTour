#!/bin/bash
# KT Structures 2026-10-04: larger-n 2f (D=4) and a long exact 2f bound at n=20.
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue[45].sh" > /dev/null; do sleep 10; done
run(){ echo "== $(date -u +%H:%M:%S) $*" >> logs/queue6.log; $PY tmin.py "$@" >> logs/queue6.log 2>&1; }
for n in 36 40 48; do run $n 2f 4 400 r${n}_2f_D4.json; done
run 20 2f 0 2400 r20_2f_D0b.json r20_2f_D4.json
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue6.log
