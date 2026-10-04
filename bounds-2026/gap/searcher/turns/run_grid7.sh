#!/bin/bash
cd "$(dirname "$0")"
while read -r tag stop args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --budget 1500 --stop $stop --out grid_$tag.json
done <<'LIST'
n62_P12Q6 -16 --n 62 --Z 8 --P 12 --Q 6
n62_P16Q8 -16 --n 62 --Z 8 --P 16 --Q 8
n62_P8Q8 -16 --n 62 --Z 8 --P 8 --Q 8
n58_P16Q8 -17 --n 58 --Z 8 --P 16 --Q 8
n58_Z10 -17 --n 58 --Z 10 --P 8 --Q 4
n58_P12Q6 -17 --n 58 --Z 8 --P 12 --Q 6
LIST
