# Crossings appendix: Claim 23B corrections complete

2026-10-02. The review version is `writeup/crossings/post.mdx`.
Both bounds are unchanged: 19n/3+142 for the construction and
14n/3-407 for the lower bound, with their existing size ranges.

## Text changes

Applied every exact replacement from Claim 23B sections 1-8. All 19
quoted replacement blocks, including the body replacements, were checked
for literal presence in the final post.

- B now states the finite stability input, the unconditional Lean tile
  theorem, and the conditional Lean theorem with its different constant.
- A.1 defines every quadrant and its rotation.
- A.2 gives the corridor barrier and the all-size affine cut margins.
- A.3 gives the complete port naming, sorting, tags, and index origin.
- A.4 gives the unit-slab proof that a free fold has no proper crossing.
- A.5 and B.7 name the correct root-relative JSON outputs. A.5 says that
  checks are printed to standard output; it no longer claims the command
  creates a text log.
- B.1 fixes the coordinate directions. B.5 specifies legal strip edges,
  exact degrees, crossing weights, inclusive row tests, and telescoping.
- The body charge paragraph includes unit-grid flux. Overview items 1
  and 3 state the correct area surplus and endpoint condition.
- Details and the appendix each link to the requested public code and
  data URL: https://github.com/nmamano/knights-tour-bounds.

## New affine certificate

`w-turnstheory/check_fold_margins.py` contains the same affine assertions
as the independent Claim 23B margin check. It reads only the twelve base
JSON files and writes `w-turnstheory/fold_margin_checks.json`. It checks
board containment, fixed label branches, and all 36,288 component-to-block
margin inequalities for every k>=0. It also checks the component count.
There is no dependency on `w-verifier/`.

A.2 names the new command. The existing `check_fold_proof.py` now calls
it before the tour, port-matching, and crossing-count checks, so the full
upper certificate still has a single entry command.

## Commands checked

All commands below passed on 2026-10-02, sequentially. The site compiler
was used read-only. The proof blocks remain collapsed by default.

| Command from the project root | Result |
| --- | --- |
| `python3 w-turnstheory/check_fold_margins.py` | PASS, 36,288 affine margin inequalities over twelve bases |
| `python3 w-turnstheory/check_fold_proof.py` | PASS, including the new margins and all 36 saved tours |
| `node writeup/crossings/check_mdx.mjs` | PASS with the site's MDX compiler and settings |
| `cd ktlean && lake env lean Axioms.lean` | PASS, theorem statements and standard axioms |

The Lean run used the installed toolchain and compiled library, with its
existing bin directory added to PATH. It was not a fresh dependency build.
Logs are `w-turnstheory/claim23b_fold_run.log`,
`w-turnstheory/claim23b_lean_run.log`, and
`writeup/crossings/compile.log`. The margin report is
`w-turnstheory/fold_margin_checks.json`.

The other Python checker sources were unchanged; their passing Claim 23B
results still apply. Exact-text checks also confirmed the two source
links, the corrected output paths, and the absence of verifier paths in
the post. The appendix is ready for the review closeout.
