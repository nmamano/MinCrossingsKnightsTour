#!/bin/bash
cd "$(dirname "$0")"
../wall/run_wd.sh ring_n56_W6_2f.log 8 ../../../.venv/bin/python band.py --n 56 --ring --W 6 --Z 8 --time 1800 --out ring_n56_W6_2f.json
