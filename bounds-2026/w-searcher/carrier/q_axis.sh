cd /home/nil/nil/knight-formation-research/w-searcher/carrier
for k in vert21 vert12 midfold; do ../../.venv/bin/python cps_band.py sweep $k '[2,4,6,8]' '[[1,1],[2,2],[3,3]]' 60; done > log_axis1.txt 2>&1
for k in edgeA edgeB; do ../../.venv/bin/python cps_band.py sweep $k '[2,4,6,8]' '[[1,0],[2,0],[3,0],[4,0]]' 60; done >> log_axis1.txt 2>&1
