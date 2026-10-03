#!/bin/bash
# (1,2) wall, WM=4, NOLAB, lambda=1: margin squares restricted to ribbon fields (FIELDL|FIELDR), 2026-10-03
for pr in "02 02" "0 0" "2 2" "0 2" "2 0" "13 13" "1 1" "3 3" "1 3" "3 1" "0 1" "0 3" "2 1" "2 3" "1 0" "3 0" "1 2" "3 2"; do
  set -- $pr
  FIELDL=$1 FIELDR=$2 LAMS=1/1 NOLAB=1 ./run_wd.sh f12_$1_$2.log 7 ./wallc 1/2 4 1 nz 8 1 90000000
  echo "FIELDL=$1 FIELDR=$2: $(grep -E 'RESULT|CAP' f12_$1_$2.log | tail -1)"
done
