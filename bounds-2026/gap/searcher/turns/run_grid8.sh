#!/bin/bash
cd "$(dirname "$0")"
for s in R LR; do
../wall/run_wd.sh grid_n56_def${s}_ub.log 8 ../../../.venv/bin/python -u pring.py --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --defsides $s --stop 0 --ub -15 --iters 400 --time 300 --workers 1 --budget 3000 --out grid_n56_def${s}_ub.json
done
./run_grid7.sh
