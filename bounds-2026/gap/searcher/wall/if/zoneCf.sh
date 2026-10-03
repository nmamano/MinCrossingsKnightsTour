#!/bin/bash
# BEYOND5 item C (general words): zone end price. Left margin: any word of split L ('/' = 02, '\' = 13), right
# margin: one straight type. MODE any, lambda=1, W=4. Weight = crossings - e|1-s|/2 * (mixed left margin squares)
# per row (switched ribbon ends per row >= alternations/2 = mixed*|1-s|/2). Certified min >= 0 <=> every zone end
# at this boundary costs >= e per switched ribbon end (in the model). Negative slopes: split '\' on the left.
cd "$(dirname "$0")/.."
export NOLAB=1 LAMS=1/1 MIXP=1 CURS=-1
E=${E:-1/2}; EN=${E%/*}; ED=${E#*/}
for sh in ${SHEARS:-1/2 0 2/3}; do
 a=${sh%/*}; b=${sh#*/}; [ "$sh" = "0" ] && { a=0; b=1; }
 for sp in 02 13; do for st in 0 2 1 3; do
  N=$((EN*(b-a))); D=$((ED*b)); g=$(python3 -c "import math;print(math.gcd($N,$D))"); N=$((N/g)); D=$((D/g))
  t=${sh/\//_}; L=if/Cf_sh${t}_L${sp}_S${st}_e${EN}_${ED}.log
  CUR=$N/$D FIELDL=$sp FIELDR=$st ./run_wd.sh $L 7 ./wifm2 $sh 4 1 any $((8*D)) 1 90000000
  r=$(grep -E 'RESULT' $L | tail -1 | sed 's/.*per row = \([-0-9]*\)\/\([0-9]*\).*/\1 \2/')
  echo "shear $sh left $sp any word | S$st, e=$E: min = $(python3 -c "from fractions import Fraction as F;p,q='$r'.split();print(F(int(p),2*int(q)*$D))" 2>/dev/null || grep -E 'CAP|too' $L) per row; $(grep 'colour current' $L | tail -1 | sed 's/.*through u = 0:/mixed:/')"
 done; done
done
