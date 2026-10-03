#!/bin/sh
# Sync the research dir into the public repo folder bounds-2026/ (github.com/nmamano/MinCrossingsKnightsTour).
# Usage: sh w-integrator/sync_public.sh [--dry-run]
set -e
SRC=$HOME/nil/knight-formation-research/
DST=$HOME/nil/MinCrossingsKnightsTour/bounds-2026/
# Repo-only files (.gitignore, README.md, requirements.txt) are excluded, so --delete keeps them.
rsync -a --delete "$@" \
  --exclude=/.gitignore --exclude=/README.md --exclude=/requirements.txt \
  --exclude=/.venv/ --exclude=/ktlean/.lake/ --exclude=/ktlean/.git/ --exclude=/CR_STATE.md \
  --exclude=/paper.pdf --exclude=/paper.txt --exclude=/board-patched.js \
  --exclude=__pycache__/ --exclude='*.npy' \
  --exclude=/w-searcher/tm --exclude=/w-searcher/cert/certify --exclude=/w-searcher/cert/certify2 \
  --exclude=/w-searcher/cert/corner_charge --exclude=/w-searcher/cert/strip2 \
  --exclude=/w-searcher/carrier/band --exclude=/w-searcher/carrier/band2 \
  --exclude=/w-verifier/claim22_pdf_page.txt --exclude=/w-verifier/claim22_figure11_stream.txt \
  --exclude=/writeup/WRITER_STATE.md --exclude='/w-verifier/claim23*_clean/' \
  "$SRC" "$DST"
case " $* " in *" --dry-run "*) exit 0;; esac
# The office demo URL stays private.
sed -i 's|^URL https://knight-demo\.office\.nilmamano\.com \.|Served as the office demo app.|' "$DST/w-integrator/FINDINGS.md"
! grep -rIl 'office\.nilmamano\.com' "$DST" || { echo "FAIL: office URL in the files above"; exit 1; }
# No compiled binaries.
BIN=$(find "$DST" -type f -size +0 -exec sh -c 'head -c4 "$1" | grep -q "ELF" && echo "$1"' _ {} \;)
[ -z "$BIN" ] || { echo "FAIL: binaries: $BIN"; exit 1; }
echo "sync OK"
