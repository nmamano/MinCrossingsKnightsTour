#!/bin/bash
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
echo "== $(date -u +%H:%M:%S) COPIES=2 FIELD=15 PER=6,8 28 tour D=6" >> logs/queue11.log
COPIES=2 FIELD=15 PER=6,8 $PY tmin.py 28 tour 6 1500 g28_P6_8_c2_D6.json >> logs/queue11.log 2>&1
echo "== DONE" >> logs/queue11.log
