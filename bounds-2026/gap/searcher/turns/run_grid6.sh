#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --budget 900 --final 900 --out grid_$tag.json
done <<'LIST'
n56_defL --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides L --stop -14
n56_defB --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides B --stop -14
n56_defR --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides R --stop -14
n56_defT --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides T --stop -14
LIST
