#!/bin/bash
# BEYOND5 item A: psi walls (MODE nz) between STRAIGHT-word fields, lambda=1, WM=4, NOLAB (2026-10-03).
# Unordered field pairs (180-degree rotation swaps sides). Straight types: '/'H 0, '/'V 2, '\'H 1, '\'V 3.
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1
for sh in ${SHEARS:-1/3 2/3 3/4}; do
 for pr in "0 0" "0 2" "0 1" "0 3" "2 2" "2 1" "2 3" "1 1" "1 3" "3 3"; do set -- $pr
   t=${sh/\//_}; L=if/A_s$1_s$2_sh${t}_W4.log
   CELLL=$1$1 CELLR=$2$2 FIELDL=$1 FIELDR=$2 ./run_wd.sh $L 7 ./wifc $sh 4 1 nz 8 1 90000000
   echo "shear $sh S$1 | S$2: $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per level (E units) = //')"
 done
done
