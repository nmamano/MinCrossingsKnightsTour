#!/bin/bash
cd /home/nil/nil/knight-formation-research/w-lowerbounds
for p in 6 8 12 16; do
 for r in mid diag edge interior; do
  for w in 3 4; do
   timeout 1500 ../.venv/bin/python corridor.py $r $p $w 0 1 2
  done
 done
done
