#!/bin/bash
# more slopes: zigzag '/' | straight '/' (positive shear: Z02|S0,S2; negative shear by mirror: Z13|S1,S3), WM=4 (2026-10-03)
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1
for sh in ${SHEARS:-1/4 1/5 3/4 2/5 3/5 1/6 5/6}; do
 for pr in "02 0" "02 2" "13 1" "13 3"; do set -- $pr
   t=${sh/\//_}; L=if/z$1_s$2_sh${t}_W4.log
   CELLL=$1 CELLR=$2$2 FIELDL=$1 FIELDR=$2 ./run_wd.sh $L 7 ./wifc $sh 4 1 any 8 1 90000000
   echo "shear $sh Z$1 | S$2: $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per level (E units) = //')"
 done
done
