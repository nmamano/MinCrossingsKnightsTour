#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --stop -14 --budget 1800 --out grid_$tag.json
done <<'LIST'
n56_P12Q6 --n 56 --Z 8 --P 12 --Q 6
n56_P8Q6 --n 56 --Z 8 --P 8 --Q 6
n56_P12Q4 --n 56 --Z 8 --P 12 --Q 4
n60_P12Q6 --n 60 --Z 8 --P 12 --Q 6
n62_Z10 --n 62 --Z 10 --P 8 --Q 4 --stop -16
LIST
