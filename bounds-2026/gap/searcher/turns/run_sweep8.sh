#!/bin/bash
cd "$(dirname "$0")"
for n in 56 58 60 62; do ../wall/run_wd.sh sweep_Z8_n$n.log 8 ../../../.venv/bin/python sweep.py --n $n --Z 8 --time 20 --out sweep_Z8_n$n.jsonl; done
