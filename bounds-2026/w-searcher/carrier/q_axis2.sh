cd /home/nil/nil/knight-formation-research/w-searcher/carrier
while pgrep -u nil -f q_axis.sh > /dev/null; do sleep 30; done
for k in diag21 diag12 anti21 anti12; do ../../.venv/bin/python cps_band.py sweep $k '[2,4,6]' '[[1,1],[2,2],[3,3]]' 60; done > log_axis2.txt 2>&1
