#!/bin/bash
cd "$(dirname "$0")"
../wall/run_wd.sh bandL_n56_W6_tour.log 8 ../../../.venv/bin/python band.py --n 56 --side L --W 6 --Z 8 --mode tour --time 1800 --out bandL_n56_W6_tour.json
