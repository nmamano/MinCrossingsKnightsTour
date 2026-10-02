PY=../.venv/bin/python
for p in 1 2 3; do for w in 6 7 8; do timeout 200 $PY run_seam.py gentle $p $w 0 150 0; done; done
for p in 1 2; do for w in 6 7 8; do timeout 200 $PY run_seam.py vert $p $w 0 150 0; done; done
for p in 1 2 4; do for w in 2 3; do timeout 200 $PY run_seam.py horizAA $p $w 0 60 0; done; done
echo exit=$?
