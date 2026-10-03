#!/bin/bash
# BEYOND5 item A'': psi walls (MODE nz, any fields) priced with their zone: weight per row = crossings
# + tau * (mixed margin squares), tau = e|1-s|/4 (switched ribbon ends >= alternations/2, mu = 2 corners).
# CUR = 2 tau = e|1-s|/2 (engine value = X + CUR/2 * mixed). Printed per-level value / TD = bound per row.
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1 MIXP=1
E=${E:-1/2}; EN=${E%/*}; ED=${E#*/}
for sh in ${SHEARS:-1/2 2/5 3/7 1/3 1/4 2/3 3/5 0}; do
  a=${sh%/*}; b=${sh#*/}; [ "$sh" = "0" ] && { a=0; b=1; }
  N=$((EN*(b-a))); D=$((2*ED*b)); g=$(python3 -c "import math;print(math.gcd($N,$D))"); N=$((N/g)); D=$((D/g))
  t=${sh/\//_}; L=if/M_sh${t}_e${EN}_${ED}_W4.log
  CUR=$N/$D ./run_wd.sh $L 7 ./wifm2 $sh 4 1 nz $((8*D)) 1 90000000
  r=$(grep -E 'RESULT' $L | tail -1 | sed 's/.*per row = \([-0-9]*\)\/\([0-9]*\).*/\1 \2/')
  echo "shear $sh e=$E CUR=$N/$D: $(grep -E 'RESULT|CAP|too' $L | tail -1 | sed 's/.*per row = //') => wall+zone bound per row = $(python3 -c "from fractions import Fraction as F;p,q='$r'.split();print(F(int(p),2*int(q)*$D))") ; $(grep 'colour current' $L | tail -1 | sed 's/colour current through u = 0/mixed margin squares/')"
done
