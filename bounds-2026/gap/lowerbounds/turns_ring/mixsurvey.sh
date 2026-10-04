#!/bin/bash
# survey of two-family residue mixtures: which have a zero-cost periodic pattern on all four sides
cd /home/nil/nil/knight-formation-research/gap/lowerbounds/turns_ring
PY=../../../.venv/bin/python
for n in 48 50; do
for R in 0 1 2 3 01 02 03 12 13 23 012 013 023 123; do $PY mixstrip.py A D 4 $R $n; done
for R in 0 1 2 01 02 12; do $PY mixstrip.py A C 3 $R $n; done
for R in 0 1 2 3 4 01 02 03 04 12 13 14 23 24 34 012 013 014 023 024 034 123 124 134 234 0123 0124 0134 0234 1234; do $PY mixstrip.py A B 5 $R $n; done
done
