# Independent TT16 local search

Date: 2026-10-04. Author: KT Verifier (Astra).

## Result

No improved tour was found. On each of n = 56, 58, 60, 62, the supplied TT16 tour is a **strict local minimum under a single cycle-preserving 2-opt move**. No sequence of two such moves gives fewer turns. This is finite local evidence, not a proof that 8n - 14 is globally optimal, and not a resolution of the constant gap.

The search uses new C++ code, not the corner CP-SAT model. All board cells are eligible. At most two search processes ran at once; each is single-threaded.

## Exhaustive one-move results

A move removes two disjoint cycle edges (a,b) and (c,d), listed in cycle order, and adds (a,c) and (b,d). Both new edges must be knight moves. Reversing the segment from b to c preserves one Hamiltonian cycle. For two disjoint edges this is the only new reconnection that preserves one cycle. The other new pairing closes two separate cycles and is excluded.

The complete census lists moves by their change in turn count:

| n | TT16 turns | +1 | +2 | +3 | +4 | nonpositive moves |
|---|---:|---:|---:|---:|---:|---:|
| 56 | 434 | 68 | 187 | 388 | 4344 | 0 |
| 58 | 450 | 68 | 170 | 269 | 2670 | 0 |
| 60 | 466 | 72 | 182 | 278 | 2892 | 0 |
| 62 | 482 | 76 | 210 | 433 | 5531 | 0 |

Thus any improvement by these switches must first increase the turn count.

## Exhaustive two-move results

For every legal first move, the program enumerates every legal second move on the resulting tour. The direct inverse is excluded. Counts refer to ordered move sequences, not distinct final tours.

| n | two-move sequences checked | minimum total change | equal-turn sequences | improving sequences |
|---|---:|---:|---:|---:|
| 56 | 20,363,423 | 0 | 1 | 0 |
| 58 | 10,946,600 | +2 | 0 | 0 |
| 60 | 12,830,579 | +1 | 0 | 0 |
| 62 | 31,351,550 | +1 | 0 | 0 |

Total: 75,492,152 sequences. An improving sequence from any of these seeds needs at least three 2-opt moves.

The equal-turn n=56 witness is saved as `turns_search_pair_level56_0.txt`. An independent Python checker verifies a closed Hamiltonian knight tour with 434 turns. Its undirected edge set differs from TT16 by three removed and three added edges. It is not just another traversal of the original cycle.

A further exhaustive run from this witness found one zero-cost single move and no improving single move. It also found no improving two-move sequence among 20,383,158 sequences. See `turns_search_neutral56.log`. This auxiliary run originally reused the witness output name; the original TT16 run was rerun to restore the witness, and its edge difference was checked after restoration. The current source derives output names from the input filename to prevent that overwrite.

## Random search

For each size, 12 runs made 3,000,000 proposals each (36 million per size; 144 million total). Every run starts from TT16. Run 0 allows only nonpositive changes; it cannot leave the seed. Runs 1–11 use simulated annealing, with initial temperatures drawn from 0.15, 0.30, 0.45, and 0.60, decreasing linearly to zero. The RNG seed is 20261004+n.

A proposal chooses a vertex, then one of its knight neighbors. Their cycle positions specify a possible reversal. Ninety percent of proposals select the first vertex in one of the four 24 by 24 corner squares; ten percent select it anywhere. Thus the search favors corners but does not freeze the rest of the board. Invalid reconnections are rejected before acceptance scoring.

| n | valid proposals | accepted moves | accepted zero-cost moves | best turns |
|---|---:|---:|---:|---:|
| 56 | 12,504,712 | 19,844 | 6,308 | 434 |
| 58 | 9,431,863 | 19,257 | 5,659 | 450 |
| 60 | 9,378,278 | 19,006 | 5,669 | 466 |
| 62 | 13,072,232 | 20,062 | 6,323 | 482 |

These counts describe proposals and accepted transitions, not unique tours. The run is bounded evidence; different moves or larger changes may improve the upper bound.

## Verification and files

- `turns_search_prepare.py` decodes the four audited TT16 certificates in `w-integrator/tours/certificates/`. It independently checks board membership, degree two, reciprocal edges, one cycle, and the turn count. Its output is a cycle of row-major vertex IDs.
- `turns_search.cpp` implements enumeration and search. The score uses only the four endpoints changed by a switch. During the exhaustive pair run, every first switch is applied and checked against a full turn recount; all board cells and edges are checked, too. Each reversal is undone and compared with the exact seed sequence. Saved candidates and random-run endpoints also receive full checks.
- `turns_search_validate.py` independently checks saved sequences with integer coordinate tests. `turns_search_validation.json` records their counts, edge differences, and SHA-256 hashes.
- `turns_search_pairs{n}.log` contains the full two-move score histograms.
- `turns_search_random{n}.log` contains the random-run summaries.

Run from the project root:

```sh
python3 gap/verifier/turns_search_prepare.py
g++ -O3 -std=c++17 gap/verifier/turns_search.cpp -o gap/verifier/turns_search_bin
for n in 56 58 60 62; do
  gap/verifier/turns_search_bin gap/verifier/turns_search_seed$n.txt pairs
  gap/verifier/turns_search_bin gap/verifier/turns_search_seed$n.txt 12 3000000
done
python3 gap/verifier/turns_search_validate.py
```

Current pair-mode witness output names append `.pair_level_<change>.txt` to the input filename. This differs from the saved witness name above; the cycle data are the same.

## Next useful step

A search based only on greedy 2-opt cannot leave these seeds. A direct three-edge exchange, or a search that permits intermediate disconnected cycle covers and then reconnects them, explores a different neighborhood. These are possible follow-ups; this report does not claim results for them. Claim audits remain the priority when new claims arrive.
