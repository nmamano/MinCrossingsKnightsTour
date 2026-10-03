# Fold proof questions (2026-10-02)

I am deriving the reduced blocks directly, so no extra computation is requested yet.
Please put the promised FOLD_DATA.md in place when ready. In particular, does the
Integrator already have a complete port matching for a corner wedge (label
max(2x-y,2y-x)) and for a side chevron (left frame label
2*min(y,n-y)-x)? These are the blocks I will test, with width 6 and two
extra copies for n -> n+24. A known step-12 failure residue would also help.

Update: I derived the matchings. Corner blocks of width 6 are idempotent;
side chevron blocks of width 6 induce the four-cycle [1,2,3,0]. Thus +24
changes the side matching by its square, and +48 restores it. The all-n
proof will check both parity states per residue, not assert a false
identity matching for +24. Actual FOLD24 base n100 transplanted to112 has
3 cycles; base102 transplanted to114 has2. No answer is needed for these.

Resolved: no question remains. PROOF_fold.md and check_fold_proof.py are
complete. The independent check passed all 36 tours and both matching
states. FOLD_DATA.md was not yet present; the proof uses the source code,
saved base components, and saved tours directly.

# New finite task after the one-row corner lemma (2026-10-02)

Section 10 now proves X >= 9n/2 - 585 using the existing per-row 1/2
certificate. To pass 4.5, please assign the following finite computation.
No new geometry or solver search for tours is required.

Use the width-two strip graph. At scan row R, form F modulo 3 from the
selected edges below, with coordinates relative to R:

- coefficient -1: (0,-1)--(1,1), (0,0)--(1,-2), (0,0)--(2,-1),
  (0,2)--(1,0), (1,0)--(2,2), (1,1)--(2,-1);
- coefficient +1: (0,1)--(1,-1), (0,1)--(2,0).

An endpoint row is admissible iff F == 2 mod 3 and the two edges
(0,0)--(2,1), (0,1)--(2,0) are not both selected. Mark failure by b=1.
The new proved corner identity and whole-square exclusion require only
this test, not a critical P/P' row. The coefficient list is checked in
check_corner_one_row.py; see FINDINGS 10.1--10.2 for why all relevant edges
straddle the row.

At phase zero, initialise the accumulator from the pending edges; during
the row, add contributions of newly introduced edges exactly once. Also
track the two exceptional-edge bits. Charge b when the row ends. This
can be an augmented graph or a transfer graph of complete rows.
Find beta>1/2 and a converged exact potential for weights
q*(4w-1)-4p*b, beta=p/q. A critical cycle obstruction at 1/2 would also be
useful. Do not infer a certificate from a capped nonconverged search.

The opposite corner on the same side uses the reflected list y -> -y,
and the reflected exceptional pair. Separate certificates for the two
orientations suffice; splitting the walk at the middle adds only O(1).
Alternatively, charge failure of either test at every row, if that still
permits beta>1/2. Report the potential range and an independent checker.

Why this would finish a stronger theorem: L >= 2n-O(1)-b and the square
budget give 4n <= 4E+2b+O(1). Stability b <= E/beta+O(1) gives
X >= [4+2beta/(2beta+1)]n-O(1), strictly above 4.5 for beta>1/2.

# Assigned finite task resolved; next task: fractional endpoint loss (2026-10-02)

The binary task above is DONE: beta=1, yielding 14n/3-407 (FINDINGS 10.5).
Please assign this next finite check to KT Lower Bounds. The geometry is
proved in FINDINGS 11.1-11.3; its local checker is
`python3 w-turnstheory/check_endpoint_loss.py`.

Use the existing width-two strip graph and endpoint accumulator, but test
one orientation at a time (`up`, then `down`). Carry row parity as an
extra state bit. Compute F and the inward-exception flag e exactly as in
`endpoint_independent.py`. At the end of the row set

    c = +1 on even local rows, -1 on odd local rows;
    h = ((1+c)//2 + c*(F+2)) mod 3;
    t = 2 if e else {0:1, 1:2, 2:0}[h].

Here t=2a is twice the new endpoint penalty. Charge t once at row end,
then reset the accumulator and toggle parity. Include both initial
parities. For beta=p/q, certify the integer arc weights

    q*(4w-1) - 2*p*t.

Find ANY beta>1, with a converged potential and its exact range. Test
4/3 as the best value permitted by the known critical cycle; if needed
seek a smaller value or extract an obstruction at beta=1. Reuse the
independent set-of-test-edges implementation to verify the answer. No
full-board solver run and no wider strip graph are requested.

IMPORTANT: use separate oriented certificates. The local parity at the
opposite corner is reversed on an even board. Taking the maximum of the
two physical-end penalties at each row would put back the known beta=1
obstruction. The proof splits each side at its middle and uses one
oriented certificate on each half, with arbitrary initial parity. This
costs eight endpoint-potential errors in total, which is O(1).

Why the task improves the theorem: if the endpoint residues are h,k and
neither inward exception occurs, the path is lost only for (h,k) equal
to (0,0), (1,2), or (2,1). Penalties a(0)=1/2, a(1)=1, a(2)=0 pay one
for each such pair. An exception receives penalty one. Hence L>=2n-O(1)-A
and 4n<=4E+2A+O(1). A certificate beta*A<=E+O(1) gives coefficient
4+2beta/(2beta+1). Beta>1 improves 14/3; beta=4/3 gives 52/11.

The known critical period-one field has F=1 in both orientations, no
exception, two crossings per row, and alternating penalties 1 and 1/2.
Thus its ratio is 4/3, not 1. A different critical cycle could still
block this improvement; that possibility remains open.

STOPPED (2026-10-02): the fractional endpoint task above is withdrawn.
No further computation is requested. Work now concerns the two final proofs.
