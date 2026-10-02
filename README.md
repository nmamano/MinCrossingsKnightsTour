# knights-tour-bounds

Bounds on the minimum number of **crossings** and **turns** of a closed knight's tour on an n &times; n board,
with constructions, proofs, independent audits, Lean 4 proofs of key lower bounds, and an interactive demo.

This repository is the complete working record of one research session (2026-10-01/02, Pacific time).
It extends the results of the paper *Taming the Knight's Tour: Minimizing Turns and Crossings*
(Besa, Johnson, Mamano, Osegueda, Williams; [arXiv:1904.02824](https://arxiv.org/abs/1904.02824)).

Definitions. X counts unordered pairs of tour moves whose open segments intersect properly (a shared endpoint
does not count). T counts the squares where the tour changes direction. A 2-factor is a spanning subgraph of
the knight graph where every square has degree two; it can have several cycles.

## Results

Previous bounds: crossings 4n &minus; O(1) &le; X<sub>min</sub> &le; 12n + O(1) (paper), improved to 11.5n + O(1) by
Shisheng Li (2026); turns (6 &minus; &epsilon;)n &le; T<sub>min</sub> &le; 9.25n + O(1) (paper).

| Result | Status | Proof | Audit | Lean | Check command |
| --- | --- | --- | --- | --- | --- |
| X &le; 19n/3 + 142 | Proved, even n &ge; 96 | [PROOF_fold.md](w-turnstheory/PROOF_fold.md) | Claims 12, 21(B) | none | `python3 w-turnstheory/check_fold_proof.py` |
| X &le; 343n/48 + 671/24 | Proved, even n &ge; 96 | [PROOFS.md &sect;5](w-turnstheory/PROOFS.md) | Claim 8 | none | `python3 w-turnstheory/check_lf_proof.py` |
| X &le; 9n + 7 | Proved, even n &ge; 48 | [PROOFS.md &sect;1-4](w-turnstheory/PROOFS.md) | Claims 1, 4, 7 | none | `python3 w-turnstheory/check_upper_proofs.py` |
| X &ge; 14n/3 &minus; 407 | Proved, closed tours, even n &ge; 32 | [PROOF_crossings_lower.md](w-turnstheory/PROOF_crossings_lower.md) | Claims 19, 20, 21(B) | conditional on strip stability: [`KT.ClosedTour.fourteen_mul_le_of_stability`](ktlean/Ktlean/TourMain.lean) | `python3 w-turnstheory/check_crossings_lower.py` |
| X &ge; 4n &minus; 2 | Proved, every tour and 2-factor | [PROOF_crossings_lower.md &sect;1](w-turnstheory/PROOF_crossings_lower.md) | Claims 9, 20 | unconditional: [`KT.ClosedTour.four_mul_sub_two_le_numCrossings`, `KT.TwoFactor.four_mul_sub_two_le_numCrossings`](ktlean/Ktlean/Crossings.lean) | `python3 w-turnstheory/check_knight_tiles.py` |
| T = 8n &minus; 14 | Constructed, even n &ge; 48 | [turns paper](writeup/turns/main.pdf), [PROOFS.md &sect;1-4](w-turnstheory/PROOFS.md) | Claims 6, 7, 16 | none | `python3 w-turnstheory/check_upper_proofs.py` |
| T &ge; 8n &minus; 28 | Proved, tours and 2-factors, n &ge; 8 | [turns paper](writeup/turns/main.pdf) | Claim 16 | not formalized | `python3 writeup/turns/check_corner.py` |
| T &ge; 8n &minus; 64 | Proved, tours and 2-factors, n &ge; 8 | [turns paper](writeup/turns/main.pdf), [FINDINGS &sect;1](w-turnstheory/FINDINGS.md) | Claim 2 | unconditional: [`KT.ClosedTour.eight_mul_sub_64_le_numTurns`](ktlean/Ktlean/Tour.lean) | `python3 w-turnstheory/check_proof.py` |

Claims refer to the audit log [w-verifier/FINDINGS.md](w-verifier/FINDINGS.md). For every even n &ge; 48 the turn
results give 8n &minus; 28 &le; T<sub>min</sub>(n) &le; 8n &minus; 14, so T<sub>min</sub>(n)/n &rarr; 8. The TT16 construction
also shows that the paper's conjecture T &ge; 8n is false as stated (by a constant).
Full statements, scope and the list of what is not proved: [RESULTS.md](RESULTS.md).
The check commands run from the repository root, use Python 3, and need no solver.
All seven distinct commands passed on 2026-10-02 ([record](w-turnstheory/results_checks.json)).

## Progression of the upper bounds

| Measure | Step | Bound | Credit | Date |
| --- | --- | --- | --- | --- |
| crossings | original formation heel | 13n | Besa, Johnson, Mamano, Osegueda | 2019 |
| crossings | improved heel | 12n | Parker Williams | January 2022 |
| crossings | 4&times;40 block | 11.5n | Shisheng Li | May 2026 |
| crossings | H16a heel | 9n | Agent Team | October 1, 2026 |
| crossings | lane-free LF4 | 343n/48 &asymp; 7.15n | Agent Team | October 1, 2026 |
| crossings | fold design | 19n/3 &asymp; 6.33n | Agent Team | October 1, 2026 |
| turns | original formation heel | 9.5n | Besa, Johnson, Mamano, Osegueda | 2019 |
| turns | 21-turn heel | 9.25n | Parker Williams | January 2022 |
| turns | T18 heel (lane rule) | 8.5n | Agent Team | October 1, 2026 |
| turns | TT16 | 8n &minus; 14 | Agent Team | October 1, 2026 |

Bounds are leading terms (plus O(1)); dates of the Agent Team steps are Pacific time. The [demo](demo/) shows
every step as a real tour for even n up to 200.

## Methodology

**Setting.** One closed research session, 2026-10-01/02 (Pacific time), in the Isomux multi-agent office, room
"Research Lab". The human, Nil Mamano (co-author of the 2019 paper), set the goal (improve the asymptotic bounds
on crossings and turns) and required convincing proofs for every claim. A coordinating agent split the work,
wrote the briefs and tracked the state; the other agents worked in their own directories and reported to it.

**Agents and models.**

| Agent | Model | Role |
| --- | --- | --- |
| Chief Researcher | Claude Opus 5.5 | coordination, briefs, status |
| KT Integrator | Claude Opus 5.5 | full-tour assembly, CP-SAT corner completion, period-in-n arguments, interactive demo |
| KT Structures | Claude Opus 5.5 | global layouts: folds, seams, jog bands |
| KT Lower Bounds | Claude Opus 5.5 | lower-bound framework, strip transfer graphs, stability certificates; later the blog drafts |
| KT Edge Searcher | Claude Opus 5.5 | edge gadget search (CP-SAT, C++ transfer matrices); independent C++ certification |
| KT Verifier | GPT-6 Astra | adversarial audits with its own code (Claims 1-22) |
| KT Turns Theory | GPT-6 Astra | proofs |
| KT Lean | Claude Opus 5.5 | Lean 4 + Mathlib formalization |
| KT Turns Builder | Codex | early turn-heel searches (retired) |

The messages that directed the agents are kept in [briefs/](briefs/); [BRIEF.md](BRIEF.md) is the shared
starting brief.

**Verification rules.**
- Every claim is audited by a different agent with independent code ([w-verifier/](w-verifier/)).
  A result counts only after this audit.
- Finite certificates (corner completions, strip potentials, path matchings) are checked by two or three
  independent implementations.
- Full tours are checked by a single-cycle validator and an independent walk; crossing counts are compared
  with an all-pairs brute-force count.
- Key lower bounds are proved in Lean 4 ([ktlean/](ktlean/)): X &ge; 4n &minus; 2 and T &ge; 8n &minus; 64 unconditionally,
  X &ge; 14n/3 &minus; 421 with strip stability as an explicit hypothesis.
- Negative results are kept: jog bands (no self-carrying band exists), layout G (trapped), and the carrier
  search. See the FINDINGS.md files of the workers and the "What is not proved" section of RESULTS.md.

## Reproduce

Python 3.12 (the session used 3.12.3):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python w-turnstheory/check_fold_proof.py      # or any check command in the table
```

`requirements.txt` pins the versions used (python-sat: the session used a 1.9 development build; any release >= 1.8 is expected to work, unchecked). ortools, python-sat, numpy, scipy and networkx are used by the
searches and checks; matplotlib, pillow and pypdf only by the figures and some audit scripts.

Lean (toolchain in [ktlean/lean-toolchain](ktlean/lean-toolchain), `leanprover/lean4:v4.35.0-rc3`, with Mathlib):

```sh
cd ktlean
lake exe cache get          # once: downloads the Mathlib build
lake build
lake env lean Axioms.lean   # prints the main statements and their axioms
```

C++ tools of the Edge Searcher (compiled binaries are not in the repository; build them from the sources
with g++, for example `g++ -O2 -o w-searcher/tm w-searcher/tm.cpp`): `w-searcher/tm.cpp`,
`w-searcher/cert/{certify,certify2,corner_charge,strip2}.cpp`, `w-searcher/carrier/band.cpp`.

Interactive demo (static page, no build step):

```sh
PORT=8000 python3 demo/serve.py   # then open http://localhost:8000/
node demo/check.js                # independent check of all 645 demo tours
```

The `*.npy` strip-potential arrays of the lower-bound work are not in the repository; `w-lowerbounds/endpoint_stab.py`
regenerates them.

## Directory map

- [RESULTS.md](RESULTS.md) - entry point: every proved result, its proof, audit, Lean status and check command.
- [BRIEF.md](BRIEF.md), [RESTART.md](RESTART.md) - shared brief and early notes.
- [briefs/](briefs/) - the messages that directed the agents.
- [kt/](kt/) - shared core: tour validation and counts, a port of the paper's Algorithm 1, periodic strip model, CP-SAT gadget search.
- [w-integrator/](w-integrator/) - full-tour assembly, corner completion, period arguments, tour files.
- [w-structures/](w-structures/) - global layouts: folds, seams, jog bands.
- [w-lowerbounds/](w-lowerbounds/) - lower-bound framework, strip transfer graphs, stability certificates.
- [w-searcher/](w-searcher/) - edge gadget search and C++ certification.
- [w-turnsbuilder/](w-turnsbuilder/) - early turn-heel searches.
- [w-turnstheory/](w-turnstheory/) - proofs and their check scripts.
- [w-verifier/](w-verifier/) - independent audits (Claims 1-22) and the audit code.
- [ktlean/](ktlean/) - Lean 4 + Mathlib formalization.
- [writeup/](writeup/) - turns paper draft (main.tex, main.pdf) and blog drafts for turns and crossings.
- [w-viz/](w-viz/), [explain/](explain/) - figures.
- [demo/](demo/) - interactive demo of the constructions and of the progression of the bounds.
- [runs/](runs/) - early run logs. Root `*.py` files - early experiments.
- [board-original.js](board-original.js) - the original demo code of the 2019 paper.

## Credits

- The 2019 paper and its constructions: Juan Jose Besa, Timothy Johnson, Nil Mamano, Martha C. Osegueda,
  Parker Williams, [arXiv:1904.02824](https://arxiv.org/abs/1904.02824). Parker Williams improved the heels
  (12n crossings, 9.25n turns).
- Shisheng Li: the 4&times;40 block (11.5n crossings).
  Code: [github.com/daizisheng/MinCrossingsKnightsTour](https://github.com/daizisheng/MinCrossingsKnightsTour),
  page: [daizisheng.github.io/MinCrossingsKnightsTour](https://daizisheng.github.io/MinCrossingsKnightsTour/).
- Tools: Google OR-Tools (CP-SAT), PySAT, Lean 4 and Mathlib.

## Not included

The paper itself (see the arXiv link), and two audit files of Claim 22 that hold text and vector data
extracted from one page of the paper PDF (`w-verifier/claim22_pdf_page.txt`, `w-verifier/claim22_figure11_stream.txt`);
Shisheng Li's patched demo code (see his repository); the Python virtual environment, the Lean build directory,
compiled binaries and the `*.npy` arrays.

## License

TODO: license (Nil)
