# Track: crossings lower bound

Goal: prove X >= cn - O(1) with c > 5 for every closed tour on an n x n board.

## Where the current bound comes from

The tentative 5n - 597 proof ([../../bounds-2026/CROSSINGS_PROOFS.md](../../bounds-2026/CROSSINGS_PROOFS.md)
part B) adds to the 4n tile-area bound about 2n charged corner paths, each paying 1/2 crossing.
[../../bounds-2026/gap/PIVOT_BRIEF.md](../../bounds-2026/gap/PIVOT_BRIEF.md) explains why this kind of argument
stops at 5n: to go further, a charged path must pay more than 1/2 on its own, or the one-cycle (connectivity)
condition must be priced. That brief is marked speculative, and its program was not completed.

## Known dead ends (2026 session; see the status labels in each file)

- Strip-certificate increments: all bounds of the form [4 + 2b/(2b+1)]n stay below 5n (gap/PIVOT_BRIEF.md).
- A joint side inequality with changed collar ports: negative
  ([../../bounds-2026/gap/lowerbounds/FINDINGS.md](../../bounds-2026/gap/lowerbounds/FINDINGS.md) B5).
- Connectivity counts with weights on g rows and changed ports: dead
  ([../../bounds-2026/gap/structures/BEYOND5.md](../../bounds-2026/gap/structures/BEYOND5.md) section 13).
- Verifier claims 43 to 47 in [../../bounds-2026/gap/verifier/](../../bounds-2026/gap/verifier/) red-team
  several beyond-5n lemmas; some were found false.

## What to submit

A proof with its finite certificates and a checker, or a proved limit of a method. A small, simple step past 5n
is welcome. A method that cannot pass 5n is not, unless the note proves that limit.
