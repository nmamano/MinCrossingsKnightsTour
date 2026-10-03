cd /home/nil/nil/knight-formation-research/w-searcher/carrier
while pgrep -u nil -f "cps_band.py sweep" > /dev/null; do sleep 15; done
for W in 3 4 5 6; do for p in 2 4 6 8; do for r in 1 -1; do
  timeout 900 ../../.venv/bin/python freeband.py c1 $p $W $r 240
done; done; done
echo QDONE
