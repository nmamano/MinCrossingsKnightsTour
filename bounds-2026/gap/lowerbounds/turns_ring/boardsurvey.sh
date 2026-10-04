#!/bin/bash
cd /home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring
PY=../../../.venv/bin/python
for n in 48 50; do
for M in AB:5:0 AB:5:01 AB:5:02 AB:5:03 AB:5:04 AB:5:13 AB:5:14 AB:5:012 AB:5:013 AB:5:014 AB:5:023 AB:5:024 AB:5:034 AB:5:0123; do
  timeout 1300 $PY board_sat.py $n 4 0 900 $M 2>&1 | head -1
done; done
