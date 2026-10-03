#!/bin/bash
# board side at x = 0 (left), field on the right margin; MODE any, lambda=1, NOLAB (2026-10-03)
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1 SIDE=1
for f in "00 0" "22 2" "02 02" "11 1" "33 3" "13 13"; do
  set -- $f; L=if/side_c$1_W${W:-4}.log
  CELLR=$1 FIELDR=$2 ./run_wd.sh $L 7 ./wifs 0 ${W:-4} 1 any 8 1 ${CAP:-90000000}
  echo "side | C$1: $(grep -E 'RESULT|CAP|too|interval' $L | tail -1 | sed 's/.*per row = //')"
done
