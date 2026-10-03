#!/bin/bash
# zigzag field (left) | straight knight-line field (right), MODE any, lambda=1, WM=4, NOLAB (2026-10-03)
# zigzag '/' = CELL 02 (one a, one b move per cell); '\' = CELL 13. straight: '/'H 00, '/'V 22, '\'H 11, '\'V 33.
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1
for sh in ${SHEARS:-0 1/2 1 1/3 2/3}; do
 for z in 02 13; do
  for st in 0 2 1 3; do
   t=${sh/\//_}; L=if/z${z}_s${st}_sh${t}_W${W:-4}.log
   CELLL=$z CELLR=$st$st FIELDL=$z FIELDR=$st ./run_wd.sh $L 7 ./wifc $sh ${W:-4} 1 ${MODE:-any} 8 1 ${CAP:-90000000}
   echo "shear $sh Z$z | S$st: $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per row = //')"
  done
 done
done
