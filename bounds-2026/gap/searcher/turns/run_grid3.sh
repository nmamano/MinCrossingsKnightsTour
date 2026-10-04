#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --stop -14 --out grid_$tag.json
done <<'LIST'
n50_Z8 --n 50 --Z 8 --P 8 --Q 4
n54_Z8 --n 54 --Z 8 --P 8 --Q 4
n56_def8 --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6
n56_def12 --n 56 --Z 8 --P 8 --Q 4 --defect 12 --defectW 8
LIST
