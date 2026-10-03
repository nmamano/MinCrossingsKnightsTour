#!/bin/bash
# BEYOND5 item A': psi walls (MODE nz), any fields, weight = crossings + CURS * t * (colour current through the
# cut u = 0) per row, t = CUR (default 2/9); WM=4, NOLAB, lambda=1 (2026-10-03).
# Printed per-level value / TD = crossing-equivalent per row. Lower bound on crossings + t|J| = max over CURS = +-1.
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1 CUR=${CUR:-2/9}
TD=${CUR#*/}
for sh in ${SHEARS:-1/2 0 1 1/3 2/3 1/4 3/4 2/5 3/5}; do
 for sg in 1 -1; do
   t=${sh/\//_}; L=if/L_sh${t}_c${CUR/\//_}_s${sg}_W4.log
   CURS=$sg ./run_wd.sh $L 7 ./wifq $sh 4 1 nz $((8*TD)) 1 90000000
   echo "shear $sh CURS=$sg t=$CUR: $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per level (E units) = //') ; last cycle: $(grep 'colour current' $L | tail -1)"
 done
done
