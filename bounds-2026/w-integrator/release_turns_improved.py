#!/usr/bin/env python3
"""Stage ONLY the 'improved turn bounds' release (Claims 55b, 56) in the public repo, leaving the held crossings
5n rows unstaged (KT Integrator, 2026-10-04). Run after sync_public.sh, on the CR's go:
    python3 w-integrator/release_turns_improved.py && git -C ~/nil/MinCrossingsKnightsTour diff --cached
It applies fixed replacements to the HEAD versions of README.md, bounds-2026/README.md, bounds-2026/RESULTS.md,
writes them to the index (git hash-object + update-index), and stages bounds-2026/TURNS_IMPROVED.md."""
import subprocess, os
R = os.path.expanduser('~/nil/MinCrossingsKnightsTour')
def git(*a, inp=None):
    return subprocess.run(['git', '-C', R, *a], input=inp, capture_output=True, text=True, check=True).stdout
ROWS = {
 'bounds-2026/RESULTS.md': [
  ("| T = 8n-14 | Constructed, even n>=48 | All-size insertion proof; exact turn count |\n",
   "| T = 8n-17 (n = 2 mod 8), T = 8n-16 (n = 6 mod 8) | Constructed, even n>=48 in these classes | All-size insertion proof, period 16; exact turn count |\n"
   "| T = 8n-14 | Constructed, even n>=48 | All-size insertion proof; exact turn count |\n"),
  ("## Turn upper bound: 8n-14\n",
   "## Turn upper bound: 8n-17 and 8n-16 for n = 2, 6 mod 8\n\n"
   "For every even n>=48 with n = 2 mod 8 there is a closed tour with exactly\n"
   "T=8n-17, and for every even n>=48 with n = 6 mod 8 one with exactly T=8n-16.\n"
   "For n = 0, 4 mod 8 the best known value is still 8n-14 (next section).\n\n"
   "Proof: [TURNS_IMPROVED.md](TURNS_IMPROVED.md) (construction; the block insertion of\n"
   "[TURNS_PROOFS.md, part F](TURNS_PROOFS.md#f-one-closed-tour-for-every-n-block-insertion)\n"
   "with period 16, done by a general checker).\n"
   "Audit: Claim 55b ([report](gap/verifier/claim55b_report.md), the checker) and\n"
   "Claim 56 ([report](gap/verifier/claim56_report.md), both bounds).\n"
   "Lean: no formal construction theorem is claimed.\n\n"
   "```sh\npython3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res2 --partial\n"
   "python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res6 --partial\n```\n\n"
   "## Turn upper bound: 8n-14\n"),
  ("- The exact minimum turn count, or which constant between 14 and 28 is sharp.\n",
   "- The exact minimum turn count: the sharp constant c in T_min(n) = 8n - c lies between\n"
   "  17 and 28 for n = 2 mod 8, 16 and 28 for n = 6 mod 8, and 14 and 28 for n = 0, 4 mod 8.\n")],
 'bounds-2026/README.md': [
  ("| T = 8n &minus; 14 | Constructed, even n &ge; 48 |",
   "| T = 8n &minus; 17 (n &equiv; 2 mod 8), 8n &minus; 16 (n &equiv; 6 mod 8) | Constructed, even n &ge; 48 in these classes | [TURNS_IMPROVED.md](TURNS_IMPROVED.md) | Claims 55b, 56 | none | `python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res2 --partial` (and `ES_res6`) |\n| T = 8n &minus; 14 | Constructed, even n &ge; 48 |"),
  ("- [TURNS_PROOFS.md](TURNS_PROOFS.md) - full proofs of the turn bounds 8n &minus; 28 and 8n &minus; 14, with every check (the appendix of the turns blog post).\n",
   "- [TURNS_PROOFS.md](TURNS_PROOFS.md) - full proofs of the turn bounds 8n &minus; 28 and 8n &minus; 14, with every check (the appendix of the turns blog post).\n"
   "- [TURNS_IMPROVED.md](TURNS_IMPROVED.md) - tours with 8n &minus; 17 turns (n &equiv; 2 mod 8) and 8n &minus; 16 turns (n &equiv; 6 mod 8), with the all-size checks.\n")],
 'README.md': [
  ("- Turns: a tour with T = 8n &minus; 14 for even n &ge; 48, and T &ge; 8n &minus; 28 for n &ge; 8.",
   "- Turns: a tour with T = 8n &minus; 14 for even n &ge; 48 (8n &minus; 17 for n &equiv; 2 mod 8, 8n &minus; 16 for n &equiv; 6 mod 8), and T &ge; 8n &minus; 28 for n &ge; 8.")]}
for path, pairs in ROWS.items():
    s = git('show', 'HEAD:' + path)
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:60]); s = s.replace(a, b)
    h = git('hash-object', '-w', '--stdin', inp=s).strip()
    git('update-index', '--cacheinfo', f'100644,{h},{path}')
git('add', 'bounds-2026/TURNS_IMPROVED.md')
git('add', '-A', 'bounds-2026/demo')   # demo step TI (app.js, build_data.py, README.md, data/TI_*.json, data/summary.json)
print(git('diff', '--cached', '--stat'))
