#!/bin/sh
# KT Structures, 2026-10-03: reruns the SHEET section 8 measurements; logs in census.log
cd "$(dirname "$0")"; P=../../.venv/bin/python; V=../verifier; T=../../w-integrator/tours
for f in $T/FOLD24_n96.json $V/claim36_FOLD_n144.json $V/claim36_FOLD_n192.json $V/claim36_FOLD_n240.json $V/claim36_FOLD_n288.json \
         ../lowerbounds/conn/FIELD_n166_92_155.json $T/FOLDB1_n144.json $T/FOLDP_n96.json $T/FOLDX_n100.json $T/FJOG_n130.json \
         $T/FJOG_n132.json $T/LF4_n96.json $T/TT16_n72.json; do
  $P chord_census.py $f; $P nre_scan.py $f
done
echo exit=$?
