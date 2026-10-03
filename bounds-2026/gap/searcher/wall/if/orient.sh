#!/bin/bash
# zigzag orientation runs (ORL/ORR: 1 = z0, 2 = z1), WM=4, NOLAB, lambda=1 (2026-10-03)
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1
run() { # name shear mode CELLL CELLR ORL ORR
  L=if/or_$1.log; CELLL=$4 CELLR=$5 FIELDL=$4 FIELDR=$5 ORL=$6 ORR=$7 ./run_wd.sh $L 7 ./wifo $2 4 1 $3 8 1 90000000
  echo "$1 (shear $2 $3 Z$4 o$6 | $5 o$7): $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per level (E units) = //')"; }
run wall_z0z0 1/2 nz 02 02 1 1
run wall_z0z1 1/2 nz 02 02 1 2
run rib_z0z0 1 any 02 02 1 1
run rib_z0z1 1 any 02 02 1 2
run turn_z0z0 0 any 02 13 1 1
run turn_z0z1 0 any 02 13 1 2
run rib_z0H 1 any 02 00 1 0
