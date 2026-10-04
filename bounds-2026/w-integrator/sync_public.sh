#!/bin/sh
# Sync the research dir into the public repo folder bounds-2026/ (github.com/nmamano/MinCrossingsKnightsTour).
# Usage: sh w-integrator/sync_public.sh [--dry-run]
set -e
SRC=$HOME/nil/knight-formation-research/
DST=$HOME/nil/MinCrossingsKnightsTour/bounds-2026/
# Compiled binaries (ELF) anywhere in the research dir stay out; workers add new ones (e.g. gap/).
BINX=$(mktemp)
trap 'rm -f "$BINX"' EXIT
(cd "$SRC" && find . \( -path ./.venv -o -path ./ktlean/.lake -o -path ./ktlean/.git \) -prune -o -type f -size +0 -print \
  | while read -r f; do if head -c4 "$f" | grep -q ELF; then echo "/${f#./}"; fi; done) > "$BINX"
# Data files over 5 MB stay out (rebuildable; the claim reports hold their hashes). Report them to the CR.
BIG=$(cd "$SRC" && find . \( -path ./.venv -o -path ./ktlean/.lake -o -path ./ktlean/.git \) -prune -o -type f -size +5M \
  ! -name '*.npy' ! -name '*.bin' ! -name '*.drup' ! -name '*.cnf' -print | sed 's|^\./|/|')
[ -z "$BIG" ] || { echo "$BIG" >> "$BINX"; echo "EXCLUDED (over 5 MB):"; echo "$BIG"; }
# Repo-only files (.gitignore, README.md, requirements.txt) are excluded, so --delete keeps them.
rsync -a --delete "$@" --exclude-from="$BINX" \
  --exclude=/.gitignore --exclude=/README.md --exclude=/requirements.txt \
  --exclude=/.venv/ --exclude=/ktlean/.lake/ --exclude=/ktlean/.git/ --exclude=/CR_STATE.md \
  --exclude=/paper.pdf --exclude=/paper.txt --exclude=/board-patched.js \
  --exclude=__pycache__/ --exclude='*.npy' --exclude='*.bin' --exclude='*.drup' --exclude='*.cnf' \
  --exclude=/w-searcher/tm --exclude=/w-searcher/cert/certify --exclude=/w-searcher/cert/certify2 \
  --exclude=/w-searcher/cert/corner_charge --exclude=/w-searcher/cert/strip2 \
  --exclude=/w-searcher/carrier/band --exclude=/w-searcher/carrier/band2 \
  --exclude=/w-verifier/claim22_pdf_page.txt --exclude=/w-verifier/claim22_figure11_stream.txt \
  --exclude=/writeup/WRITER_STATE.md --exclude='/w-verifier/claim23*_clean/' --include='/gap/verifier/claim57_run/' --exclude='/gap/verifier/claim*_run/' --exclude=/writeup/turns/post.mdx --exclude=/writeup/crossings/post.mdx --exclude='/gap/verifier/claim*_clean/' --exclude='/w-integrator/pipeline/selftest_[!T]*/' \
  "$SRC" "$DST"
case " $* " in *" --dry-run "*) exit 0;; esac
# The office demo URL stays private.
sed -i 's|^URL https://knight-demo\.office\.nilmamano\.com \.|Served as the office demo app.|' "$DST/w-integrator/FINDINGS.md"
! grep -rIl 'office\.nilmamano\.com' "$DST" || { echo "FAIL: office URL in the files above"; exit 1; }
# No compiled binaries.
BIN=$(find "$DST" -type f -size +0 -exec sh -c 'head -c4 "$1" | grep -q "ELF" && echo "$1"' _ {} \;)
[ -z "$BIN" ] || { echo "FAIL: binaries: $BIN"; exit 1; }
# The demo is the GitHub Pages landing page: the repository root index.html loads bounds-2026/demo/ assets.
sed -e 's|href="demo.css"|href="bounds-2026/demo/demo.css"|' \
    -e 's|<script src="tourlib.js"></script>|<script>window.KT_BASE = '"'"'bounds-2026/demo/'"'"';</script>\n<script src="bounds-2026/demo/tourlib.js"></script>|' \
    -e 's|<script src="alg1.js"></script>|<script src="bounds-2026/demo/alg1.js"></script>|' \
    -e 's|<script src="app.js"></script>|<script src="bounds-2026/demo/app.js"></script>|' \
    "$DST/demo/index.html" > "$DST/../index.html"
grep -q 'bounds-2026/demo/app.js' "$DST/../index.html" || { echo "FAIL: root index.html"; exit 1; }
echo "sync OK"
