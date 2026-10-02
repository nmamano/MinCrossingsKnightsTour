#!/bin/bash
cd /home/nil/nil/knight-formation-research/w-lowerbounds
for P in P Q; do for r in 8 9; do for j in 2 3 4 5 6 7 8; do timeout 3000 ../.venv/bin/python ne_m3.py $P $r $j; done; done; done
echo exit=$?
