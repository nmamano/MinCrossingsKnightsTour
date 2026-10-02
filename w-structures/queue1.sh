PY=../.venv/bin/python
for p in 1 2 4; do for w in 2 3 4 5; do timeout 300 $PY run_seam.py vert $p $w 0 120 0; done; done
for p in 1 2 4; do for w in 2 3 4; do timeout 300 $PY run_seam.py horizAA $p $w 0 120 0; done; done
for w in 2 3; do timeout 300 $PY run_seam.py sharp 4 $w 4 60; done
echo exit=$?
