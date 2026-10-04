#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --stop -14 --mip SCIP --iters 500 --time 1200 --budget 3600 --out grid_$tag.json
done <<'LIST'
n56_defAll_scip --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6
n60_defAll_scip --n 60 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6
n56_def12All_scip --n 56 --Z 8 --P 8 --Q 4 --defect 12 --defectW 8
LIST
