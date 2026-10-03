#!/bin/bash
# minimal excess per period for a mismatch (charged row 0 with a passing up test), by bisection with side_sat.py
PY=../../../.venv/bin/python
for W in "$@"; do for P in 8 10 12 14 16; do
  lo=-1; hi=$((2*P+4))   # lo: UNSAT known (excess <= lo impossible), hi: assumed SAT
  while [ $((hi-lo)) -gt 1 ]; do
    mid=$(((lo+hi)/2))
    out=$(timeout 3000 $PY side_sat.py $P $W 0 $mid pass); echo "$out"
    if echo "$out" | grep -q ': SAT'; then hi=$mid; else lo=$mid; fi
  done
  echo "RESULT P=$P W=$W mismatch min excess = $hi"
done; done
