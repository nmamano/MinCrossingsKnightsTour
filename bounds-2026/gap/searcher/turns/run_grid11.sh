#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --stop -14 --mip SCIP --iters 500 --time 1800 --budget 5400 --out grid_$tag.json
done <<'LIST'
n56_defAll_scip2 --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6
n56_ring4_scip --n 56 --Z 8 --Db 4 --Dl 4 --noties
n56_ring6_scip --n 56 --Z 8 --Db 6 --Dl 6 --noties
LIST
