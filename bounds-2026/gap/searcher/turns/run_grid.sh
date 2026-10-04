#!/bin/bash
# tour lower bound / construction per family (cut loop); one job at a time, watchdog 8 GB
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --stop -14 --out grid_$tag.json
done <<'LIST'
n56_Z10 --n 56 --Z 10 --P 8 --Q 4
n56_Z12 --n 56 --Z 12 --P 8 --Q 4
n56_P16Q8 --n 56 --Z 8 --P 16 --Q 8
n56_D6 --n 56 --Z 8 --P 8 --Q 4 --Db 6 --Dl 6
n58_Z8 --n 58 --Z 8 --P 8 --Q 4
n60_Z8 --n 60 --Z 8 --P 8 --Q 4
n62_Z8 --n 62 --Z 8 --P 8 --Q 4
LIST
