#!/bin/bash
# KT Structures 2026-10-04: third queue; starts after queue2 ends. Tours by lazy subtour cuts (D=4).
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
while pgrep -f "queue[12].sh" > /dev/null; do sleep 20; done
run(){ echo "== $(date -u +%H:%M:%S) $*" >> logs/queue3.log; $PY tmin.py "$@" >> logs/queue3.log 2>&1; }
for n in 20 24 28 32; do run $n tourlazy 4 900 r${n}_tourlazy_D4.json; done
echo "== DONE $(date -u +%H:%M:%S)" >> logs/queue3.log
