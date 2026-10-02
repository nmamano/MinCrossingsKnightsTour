cd /home/nil/nil/knight-formation-research/w-searcher/carrier
P=../../.venv/bin/python
$P -c "import cps_band as c; c.sweep('midfold',[6,10,12],[(2,2)],600,rel=(1,))"
$P -c "import cps_band as c; c.sweep('diagfree',[6,12],[(5,5)],600,rel=(1,))"
$P -c "import cps_band as c; c.sweep('midfold',[8,12],[(3,3)],600,rel=(1,))"
echo QDONE
