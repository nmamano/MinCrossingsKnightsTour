cd /home/nil/nil/knight-formation-research/w-searcher/carrier
while pgrep -u nil -x band > /dev/null || pgrep -u nil -x band2 > /dev/null; do sleep 10; done
for W in 3 4; do
  for k in vert12 midfold; do timeout 1200 ../../.venv/bin/python run_ext.py $k 4 3 1 $W; done
done
for W in 3 4 5; do
  echo "== diagfree W=$W"
  python3 extend.py ../../w-structures/diag_tpl_p6_w3.json 1 6 3 $W df_base_w${W}_c1.txt
  python3 band_gen.py diagfree $W df_w$W.txt
  CURHIST=1 NOCOREACH=1 BASE=df_base_w${W}_c1.txt /usr/bin/time -f "%M KB %e s" timeout 1800 ./band2 df_w$W.txt none 30000000 2>&1 | grep -v "q=" | cut -c1-200
done
for W in 2 3; do timeout 1200 ../../.venv/bin/python run_ext.py vert21 6 2 1 $W; done
echo QDONE
