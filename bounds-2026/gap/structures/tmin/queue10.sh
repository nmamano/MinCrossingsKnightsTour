#!/bin/bash
cd "$(dirname "$0")"; PY=../../../.venv/bin/python
echo "== $(date -u +%H:%M:%S) PER=8,10 24 tour" >> logs/queue10.log
PER=8,10 $PY tmin.py 24 tour 4 1800 t24_P8_10_s0.json >> logs/queue10.log 2>&1
echo "== DONE" >> logs/queue10.log
