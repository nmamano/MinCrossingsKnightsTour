#!/bin/bash
cd "$(dirname "$0")"
for s in R LR; do
../wall/run_wd.sh grid_n56_def${s}_scip.log 8 ../../../.venv/bin/python -u pring.py --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides $s --stop -14 --mip SCIP --iters 500 --time 1200 --budget 3600 --out grid_n56_def${s}_scip.json
done
