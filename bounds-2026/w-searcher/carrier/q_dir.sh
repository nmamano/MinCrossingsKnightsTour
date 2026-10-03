cd /home/nil/nil/knight-formation-research/w-searcher/carrier
while kill -0 3763429 2>/dev/null; do sleep 15; done
P=../../.venv/bin/python
$P -c "import cps_band as c; c.sweep('d21_2_-1',[4,6,8],[(3,3),(5,5)],300,rel=(1,))"
$P -c "import cps_band as c; c.sweep('d21_3_-1',[2,3,4],[(4,4),(6,6)],300,rel=(1,))"
$P -c "import cps_band as c; c.sweep('d21_1_-2',[2,4,6],[(3,3),(5,5)],300,rel=(1,))"
$P -c "import cps_band as c; c.sweep('d21_1_-3',[1,2,3],[(4,4),(6,6)],300,rel=(1,))"
echo QDONE
