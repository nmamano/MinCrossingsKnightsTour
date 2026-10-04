#!/bin/bash
cd "$(dirname "$0")"
while read -r tag args; do
  [ -z "$tag" ] && continue
  ../wall/run_wd.sh grid_$tag.log 8 ../../../.venv/bin/python -u pring.py $args --iters 300 --time 120 --workers 1 --stop -14 --out grid_$tag.json
done <<'LIST'
n66_Z8 --n 66 --Z 8 --P 8 --Q 4
n64_Z8 --n 64 --Z 8 --P 8 --Q 4
n68_Z8 --n 68 --Z 8 --P 8 --Q 4
LIST
