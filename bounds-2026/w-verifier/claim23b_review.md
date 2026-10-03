# Claim 23B — crossings post, full-proof appendix (2026-10-02)

**Verdict: both mathematical bounds PASS. The appendix needs completeness and scope edits before release.** The finite certificates agree with Claims 9, 12, 19, 20 and 21. The explicit bounds remain `X <= 19n/3 + 142` for every even `n >= 96`, and `X >= 14n/3 - 407` for every closed tour with even `n >= 32`.

The main defects are an omitted statement of the Lean scope, an incomplete description of the strip scan, and an unsupported assertion that all component-to-cut margins are fixed. The margins can also increase. An exact affine check establishes the condition needed for every growth step. There are also incorrect output-file paths and a claimed text output that the command does not create. Exact replacements follow below. No author source was edited.

## Sources and reproduction

I read the whole post, including its body and both appendices. I compared the appendix with the two proof documents and the sources of its check commands. The requested `w-turnstheory/APPENDIX_STATUS.md` is absent. This does not prevent the audit: the appendix and its actual dependencies are present.

The snapshot is in `w-verifier/claim23b_clean/`. It includes the post, proof sources, checker sources, twelve base files, and 36 saved tours. `sources.json` records their SHA-256 hashes. `changes_since_claim21.json` records the comparison with my Claim 21 snapshot. Every named checker and its strip dependency is unchanged from that snapshot. `PROOF_fold.md` is also unchanged. The lower proof has the Claim 21 wording repairs: it defines the endpoints in the flux identity, corrects the possible endpoint columns, states the degree requirements, and restores the corner overcount argument. No changed numerical certificate was found.

I ran the following seven distinct commands from a fresh copied project root, with a clean environment and the system Python. The jobs were sequential and restricted to one CPU core. No solver was used. Repeated appearances of the same command in the appendix do not require separate runs; the combined lower runner also reran its five checks.

| Command | Result |
| --- | --- |
| `python3 w-turnstheory/check_knight_tiles.py` | PASS: 1,292 edge pairs; maximum two common quarters; 648 single-edge flux checks. |
| `python3 w-turnstheory/check_corner_box.py` | PASS: eight nonzero end-flux coefficients, degree-two identity, and both parities of the outside charge. |
| `python3 w-turnstheory/check_col0_squares.py` | PASS: 20 normalized crossing pairs; the unique inward overlap type; five possible duplicate pairs per corner; 330-state boundary potential. |
| `python3 w-turnstheory/check_square_defects.py` | PASS: the alternating identity and at least two bad quarters in each defective square. |
| `python3 w-turnstheory/check_lower_stability.py` | PASS: 82,516 base states / 144,674 arcs; 167,782 augmented states / 315,389 arcs; potential range `[-29,0]`; overcount 1,104. |
| `python3 w-turnstheory/check_crossings_lower.py` | PASS: all five lower checks and the final arithmetic. |
| `python3 w-turnstheory/check_fold_proof.py` | PASS: all 36 saved tours, complete matchings, both states, local and total counts, and step-12 counterexamples. |

The full logs are `command_1.log` through `command_7.log`; `commands.json` gives exits and times. All exits are zero. The commands work without a solver, installed project package, or `PYTHONPATH` setting.

## Independent checks and mathematical scope

I reran my own geometry and endpoint code, my own strip graph and potentials, my own fold assembler and exterior-graph transport test, and the exact affine margin check. These programs import no worker construction or checker code. The extra run log is `extra_commands.json`. My stability program uses the existing project virtual environment because an older independent helper imports NetworkX; the appendix's seven commands need only the standard library. An initial attempt to run this extra program with the system Python stopped at that missing import. It did not find a mathematical failure.

- `claim23b_geometry.py/json` checks all eight knight directions and four translation parities against 200 dual steps, the complete coefficient identity, and the outside-box flux at both parities. It passes.
- `claim23b_stability.py/json` rebuilds 82,516 base states and a separate 184,006-state / 343,631-arc augmentation. Potentials for up, down and joint tests all have range `[-29,0]`. Its exact period-one witness has two crossings and one failed row per period. It passes. The larger augmented state count comes from retaining all relevant row edges, not just the watched test edges.
- `claim23b_fold.py` independently rebuilds 48 tours: the 36 saved sizes and twelve larger sizes `288,290,...,310`. All are single closed tours. It checks every stored edge at the saved sizes, all full port lists and returns, both side states, 36 complete exterior-graph transports, crossing counts, and twelve step-12 graphs. It passes. Results are in `claim23b_fold_results.json`.
- `claim23b_margins.py/json` checks 36,288 component-to-block inequalities as exact affine functions of `k`, together with board and branch bounds. It proves these inequalities for every integer `k >= 0`, not only sampled sizes. It passes. The current script is self-contained apart from the twelve base JSON files.
- `claim23b_text_checks.py/json` parses the eight printed coefficients directly and compares them with the independently audited test. It checks the exact constants. It passes.

The largest fold offset is 142, at base 114. Each +24 adds 152 crossings. The three complete matching types in A.3 are correct, including both same-cut returns of the six-port corner. Both parity states close each of the twelve outside matchings into one cycle. The completion from base 100 has three cycles when reused at 112 with step 12; this does not refer to the separate valid saved base-112 tour.

The lower argument keeps every charged square inside `D`. Its joint test includes the exceptional-pair exclusion required for whole squares. The near and far scan intervals are disjoint. A failed side-row can remove at most one candidate path. The boundary sets have at most five duplicates per corner, and the width-two strip overcount is at most 1,104. There is no double charge of a square, a retained path, or the `4n-2` area term.

I also ran `lake env lean Axioms.lean` from `ktlean/`, on one CPU core with the existing toolchain and compiled library. It passed. The printed theorem agrees with the source statement quoted below. The reported axioms are only `propext`, `Classical.choice`, and `Quot.sound`. This run checks the existing Lean environment; it is not a fresh toolchain installation or a rebuild of every dependency.

The exact chain is

```
E = X - 4n + 2,
|B| >= 4n - 24,
2L <= 4E + 44,
L >= 2n - 60 - b,
b <= E + 1131,
4n <= 4E + 2b + 164 <= 6E + 2426,
X >= 14n/3 - 1219/3 >= 14n/3 - 407.
```

These statements agree with Claims 19--21. The tile proof of `4n-2` also applies to a spanning 2-factor. The stronger proof uses the forest strip model and therefore has the stated Hamiltonian-tour scope.

## Required replacements

### 1. State the computational input and the exact Lean scope

The appendix names no Lean theorem or Lean command. It also does not plainly distinguish the finite stability input from the part formalized in Lean. Add the following after the opening paragraph of part B:

> This proof uses the strip stability lemma in B.5 as a computer-certified input. The named Python checker constructs the finite graph and checks every integer potential inequality; it does not assume an unverified solver answer. Lean proves `KT.ClosedTour.four_mul_sub_two_le_numCrossings` without a stability hypothesis. The stronger Lean theorem `KT.ClosedTour.fourteen_mul_le_of_stability` takes the explicit hypothesis `card(badRows) <= X - 4n + 2 + C` and concludes `14n <= 3X + C + 132`. With `C=1131`, that statement gives `X >= 14n/3 - 421`. The sharper constant 407 in this appendix follows from the argument and Python certificates below; it is not the constant in that Lean theorem.

Add a root-relative Lean check command with this note:

> With the project's Lean toolchain and dependencies installed, the following command checks the theorem statements and prints their axioms:
>
> `cd ktlean && lake env lean Axioms.lean`

The current Lean statement uses its own rotated side frames and `badRows` set. Its far scan range is `[h+2,2h-14]`; the appendix uses fixed side frames, the joint test, and `[h+3,2h-13]`. These are different conventions. Do not describe the two finite row sets or final constants as literally identical. The Lean result has only the stated stability hypothesis; it does not assert that the Bellman-Ford certificate has been checked inside Lean.

### 2. Specify the quadrant frames in A.1

After “Write `h=n/2` and `R(x,y)=(n-1-y,x)`.” add:

> Use rotation index `r=0,1,2,3` on the bottom-left, bottom-right, top-right, and top-left quadrants, respectively. The left and bottom halves have coordinates less than `h`; the other halves have coordinates at least `h`. Rotating back means applying `R^(-r)`.

This fixes the quadrant boundaries and the rotation used by every later placement rule.

### 3. Make the all-size cut margins explicit in A.2

Replace “Component shapes and the relative cut margins are fixed; checking the margins at `n0` therefore checks them for every `k`.” with:

> Put `h0=n0/2`. The corner upper cut is `30+12k = h-(h0-30) <= h-18`. The side upper cut is `h+22+12k = n-(h0-22) <= n-26`. In a corner block, `max(2x-y,2y-x) >= max(x,y)`, so the block stays away from the quadrant axes. In a left-side block, the lower cut `h+16` implies `x <= h-16`, so this block stays away from the diagonal corridor. The rotated bounds are the same. For each copied component cell, the board coordinates and cut labels are affine functions of `k`. Each required separation from a forbidden block is nonnegative at `k=0` and has nonnegative coefficient of `k`. Thus each separation stays nonnegative for every `k >= 0`. The component shapes stay fixed, but some separations increase.

Add a finite check for the last assertion:

```sh
python3 w-verifier/claim23b_margins.py
```

This small standard-library checker is now available. Include it with the released certificate files, or move the same affine assertions into `check_fold_proof.py` and name that updated command. The current fold checker extracts cuts at `k=0,1,2`; it does not itself check the signs of all affine coefficients. The general inequalities above and the affine check supply that missing reproducible fact.

Also replace “It cannot cross a diagonal fold without meeting the retained corridor.” with:

> It cannot cross a diagonal fold without meeting the retained corridor: the corridor contains the three integer transverse positions `y-x=0,1,2`, while a knight step changes `y-x` by at most three. The finite components cover the corridor ends and the central junction.

### 4. Define the port order fully in A.3

Replace the paragraph starting “To number ports, orient a crossing edge” with:

> To number ports, rotate the block to its bottom-left or left reference frame. Write a cut edge as `(u,v)` with the label of `u` less than the label of `v`. Its name is `(tag, depth(u), depth(v), label(u)-cut, label(v)-cut)`. Sort names lexicographically and number them from zero, separately at each cut. For a corner, use tag `L` if both endpoint x coordinates are at most two, otherwise `B` if both endpoint y coordinates are at most two, and otherwise `D`. The corresponding depths are x, y, and `y-x`. For a side, use tag `lo` if the lower-label endpoint has `y<h`, and `hi` otherwise; its depth is x. The complete sorted lists are in `w-turnstheory/fold_proof_checks.json`.

The current short description gives the ingredients but omits the index origin, sort convention, and exact tag choice used by the matching table.

### 5. Correct the output paths and the absent text output

In the opening paragraph of A, replace the sentence ending “in `fold_proof_checks.json`.” with:

> Complete port lists and matchings, including the outside matching, are in `w-turnstheory/fold_proof_checks.json`, which the command generates.

In A.5, replace “It writes `fold_proof_checks.json`; the run output is `fold_proof_checks.txt`.” with:

> It writes `w-turnstheory/fold_proof_checks.json` and prints its checks to standard output.

The named command does not create a `.txt` file. In B.7, replace “It stops on any failure and writes `crossings_lower_checks.json`.” with:

> It stops on any failure and writes `w-turnstheory/crossings_lower_checks.json`.

### 6. Define the side coordinates and the finite scan precisely

In B.1, replace “with `x` the column and `y` the row” with:

> with `x` increasing to the right and `y` increasing upwards

In B.5, replace “At each cell choose edges to later cells so that its final degree is two in columns `0,1` and at most two in columns `2,3`.” with:

> At each cell choose only legal knight edges to later cells that have at least one endpoint in columns `0,1`. Require final degree two in columns `0,1` and at most two in columns `2,3`.

Replace the sentence defining the width-one scan with:

> The width-one scan in B.4 uses columns `0,1,2`, allows only edges incident to column `0`, requires degree two in that column, and allows degree at most two in the other two columns.

The earlier instruction to keep boundary-incident edges suggests this restriction, but the transition definition must also state it. The checker excludes inner-to-inner edges. A reader who generates all knight edges on the stated three or four columns gets a different graph.

After the sentence defining transition weight `w`, add:

> Count a new edge's proper crossings with the other new edges and with the still-pending edges, once per unordered pair. An edge whose two endpoints were already processed cannot cross a new edge, since every knight edge has nonzero vertical displacement and the scan processes rows in order.

Replace “Every test edge straddles that row, so these data suffice.” with:

> Every test edge has minimum row at most the test row and maximum row at least the test row. Thus it is either pending at row start or is selected while processing that row; these data suffice.

Some test edges only touch the test row at an endpoint. The inclusive condition matters for the row-end test.

### 7. State the potential telescoping step

In B.5, replace “Summing over the strip walk proves” with:

> For each arc `u -> v`, `p(u)` and `p(v)` are the potentials of its endpoint states. Summing the inequalities over the `4n` transitions gives `4X_sigma-4n-4b_sigma >= p(end)-p(start) >= -29`. Hence

The displayed inequality that follows can stay. This makes the endpoint allowance explicit and removes the undefined arc variables in the formula.

### 8. Make the free-fold argument explicit

In A.4, replace the sentences starting “At a free fold” and ending “shared endpoints.” with:

> At an axis fold, use the integer coordinate normal to that axis. At a diagonal fold, use `y-x` in its local frame. Each relevant field edge changes that coordinate by one unit in the same direction on both sides of the fold. Within each open unit slab all field edges are parallel. Edges in different slabs have disjoint interiors in that coordinate and can meet on a slab boundary only at endpoints. Thus the free fold has no proper crossing.

This is the geometric argument used in Claim 12. The current phrase “each family remains on its own side” does not explain the edge that crosses the fold or why it cannot cross another edge.

## Post body agreement

The theorem callout and the minimum interval have the correct size ranges. The ratios are explicitly leading-coefficient ratios. The body now treats 19n/3 as an upper bound and rejects an unproved optimum for the whole fold family. The 9n heel arithmetic, the 343n/48 progression, and the 720-crossing tour at n=96 agree with the audited record. The two inequalities `E >= n-b/2-41` and `E >= b-1131` agree exactly with B.6. The fixed allowance in the bad-quarter budget is now stated. The captions distinguish a periodic average from a separate charge for each row.

Two body replacements are still needed:

**Charge definition.** Replace the paragraph starting “The tool is a charge.” with:

> The tool is a charge. Colour the cells black and white, like a chess board. Orient both the tour moves and all unit grid edges from black to white. Along a path through unit-square centres, add their signed crossings from the path's left side to its right side, modulo 3. The exact rule is in the [details](#details).

The current paragraph mentions only tour moves. Their flux alone is not the charge with the two properties listed next. The unit-grid contribution is essential, including along the outside corner boundary.

**Five-step overview.** Replace item 1 with:

> 1. Each knight move owns a small tile. Their total area exceeds the area between the board's cells by `2n-1`. This gives the tile bound `4n-2`.

Replace item 3 with:

> 3. At each corner, a nested path is charged when both of its end rows pass the endpoint test. There are about `n/2` candidate paths per corner.

The current item 1 says the tiles almost cover the board exactly once, which need not hold for an arbitrary tour with many crossings. The current item 3 states the charge without its endpoint condition. The later sections already give the correct conditions.

The internal links to Details and to appendix parts A and B resolve. There is no public source download link in the post. Before publication, add the actual repository or archive link with the named scripts, their dependencies, the twelve bases, and the 36 tours. No external proof from FINDINGS or TILE_INPUTS is needed after the replacements above; the files serve as certificate data and check implementations.

## Final scope

The numerical results and all seven named commands pass. The all-size insertion argument and the lower-bound charging argument agree with the audited record after the explicit definitions and margin statement above. The exact sentence replacements distinguish the computer-certified stability input from the conditional Lean statement. No bound needs to change. The remaining action is for the writer to apply these replacements and include the named certificate files in the public source bundle.
