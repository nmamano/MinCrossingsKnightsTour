#!/bin/bash
cd "$(dirname "$0")"
../wall/run_wd.sh grid_n56_def8.log 8 ../../../.venv/bin/python -u pring.py --n 56 --Z 8 --P 8 --Q 4 --defect 8 --defectW 6 --iters 300 --time 120 --workers 1 --stop -14 --budget 900 --final 1500 --out grid_n56_def8.json
./run_grid4.sh
