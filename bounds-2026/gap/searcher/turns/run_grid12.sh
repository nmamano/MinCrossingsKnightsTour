#!/bin/bash
cd "$(dirname "$0")"
../wall/run_wd.sh grid_n58_ring4_scip.log 8 ../../../.venv/bin/python -u pring.py --n 58 --Z 8 --Db 4 --Dl 4 --noties --stop -17 --mip SCIP --iters 500 --time 1800 --budget 5400 --out grid_n58_ring4_scip.json
../wall/run_wd.sh grid_n62_ring4_scip.log 8 ../../../.venv/bin/python -u pring.py --n 62 --Z 8 --Db 4 --Dl 4 --noties --stop -16 --mip SCIP --iters 500 --time 1800 --budget 5400 --out grid_n62_ring4_scip.json
