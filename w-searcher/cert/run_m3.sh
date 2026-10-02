cd /home/nil/nil/knight-formation-research/w-searcher/cert
W=$1
for o in h v; do for OX in 0 1; do for OY in 0 1; do
  info=$(python3 gen.py m3 $W $o $OX $OY /tmp/m3_${W}${o}${OX}${OY}.txt)
  res=$( (ulimit -v 7000000; ./certify2 /tmp/m3_${W}${o}${OX}${OY}.txt) 2>/dev/null )
  echo "W=$W o=$o OX=$OX OY=$OY | $info | $res | $(date +%H:%M)" | tee -a m3_results.txt
done; done; done
