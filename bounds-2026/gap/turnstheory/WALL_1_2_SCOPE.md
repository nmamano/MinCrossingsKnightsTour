# Claim 35 audit update — 2026-10-03

**PASS: achieved half-price wall and perfect plane extension. L2-v3
remains OPEN.** I read the completed audit in w-verifier/FINDINGS.md.
The Verifier adds an explicit full-plane alternating fold-stack
extension with no finite cycles. This resolves the finite-width
exterior limitation discussed in the earlier source review below.
The achieved rate uses 19 edge orbits, four row checks, a three-path
quotient graph, and a two-letter exterior formula; the large wall
minimum-mean graph is not required for this achievable-rate result.

The plane's gamma_R shapes are charged, explicitly checked at radii
12..80 and explained by periodicity. The remaining gaps are board-side
completion, the actual retention test, and eligible resources added by
that completion. Every plane edge preserves x+y modulo three, so a
Hamiltonian completion must introduce additional structure. Its cost
inside the selected paths' collars is unknown. The earlier finite
cylinder evidence is superseded by this stronger construction, not by
a closed-tour counterexample.

Chief Researcher reports that the Integrator is building such closed
tours. On receipt of a saved tour path, run the strict R=10 pure non-B
Hall test at p=2/3 (and p=1/2 as a comparison). Validate the full cycle,
recompute actual retained paths and the union B, and report Delta and
its cut. A single positive Delta rules out constants below that value;
an unbounded completed-tour family is required to disprove L2-v3 with
an unspecified absolute constant. No new completed-tour file was
provided with this audit update, so that test remains queued.

---

## Earlier source review, before the Claim 35 plane extension

# Scope of the (1,2) half-price wall — 2026-10-03

**Verdict: an obstruction to a universal open-wall price above 1/2;
not yet a counterexample to L2-v3 on closed tours.** Claim 35 is pending
in the material supplied for this review. This note checks the logical
scope of Searcher FINDINGS Section 7.1, not the whole new certificate.

The periodic witness has period vector (2,4). I read `verify_witness.py`
and `extend_witness.py` and ran the first checker. It reports degree two
at modeled cells, maximum degree two in the unroll, no finite cycle in
that unroll, and two crossings assigned to four successive rows. Its
output is `wall_1_2_check.log`. Searcher reports half a unit per level
in each tested currency and a nonzero psi jump, with perfect exterior
regions in the extension experiment.

The extension code uses a skew cylinder and soft outer degree bounds.
It explicitly does NOT forbid cycles. It does not build a square-board
Hamiltonian tour, impose the audited corner endpoint tests, or compute
a Hall neighbourhood of complete retained paths. Thus its feasibility
is not a completed-tour counterexample, even if the finite wall price
and the perfect exterior are independently audited.

A corner ray of slope two meets each sufficiently large gamma_r once.
That geometric intersection alone does not prove every gamma_r is
retained after completion: the combined flux is that of the ENTIRE
path, and another defect can cancel the local jump. The two endpoint
exceptions must also be absent. The audit uses only radii 12 through
n/2-4, so arbitrary periodic transversals cannot be substituted for
those candidates.

More importantly, L2-v3 permits an atom near ANY vertex of a retained
path to pay it. A crossing at one wall intersection need not be its
only eligible resource. Both long arms, both end zones, other walls,
and the width-ten collars must be included. Pure non-B pairs can
include side-strip surplus; mixed currency can include holes near the
ends. Perfect regions next to the wall do not fix those distant parts
of the Hall neighbourhood. A bounded-width cylinder extension is not
an arbitrarily wide perfect completion of those entire neighbourhoods.

## Exact route from the wall to a counterexample

For R=10, exhibit completed tours H_j and subsets J_j of their actual
retained candidates, with |J_j| tending to infinity, and prove

```
capacity(N_10(J_j)) <= |J_j|/2 + O(1).
```

Use the relevant currency's FULL atom support and the union of all
eligible resources, not only resources assigned to the wall. Then the
Hall deficit at p=2/3 is at least |J_j|/6-O(1), which defeats every
absolute C_flux in that fixed-radius conjecture. This can allow large
completion cost elsewhere; what matters is cost inside N_10(J_j).
To defeat an unspecified-radius conjecture requires such an argument
for every proposed fixed radius, not just ten.

If only a fraction rho of successive levels supplies retained paths,
one must compare p*rho with the wall's half-unit level cost. At p=2/3,
that particular estimate needs rho>3/4 for a linear deficit. Retention
and resource sharing are essential parts of the proposed obstruction.
No such growing completed-tour construction or neighbourhood bound is
provided in the current wall files.

## What the saved tours establish

Strict R=10 tests on 193 distinct validated completed tours give zero
mixed deficit at p=lambda=1/2. Mixed p=2/3 has seven positive deficits,
with LF5 reaching 25/2 at n=260 and a checked 94-path Hall cut. These
values are compatible with a large fixed C_flux and do not yet prove
unbounded growth. Pure non-B p=2/3 has zero deficit on all saved tours.
None of these measurements converts the new open wall into a formal
closed-tour disproof. See HALL_V3_RESULTS.md and HALL_CURRENCY_RESULTS.md.

The right research decision is nevertheless to stop treating 2/3 as a
universal flux-only wall price. Use p=lambda=1/2 for the main flux
skeleton; seek connectivity credit for a higher coefficient. This is
a choice of proof route, not a proved ceiling on every closed-tour
lower-bound argument.

## Reproduction and finite inputs

```sh
python3 gap/searcher/wall/verify_witness.py
```

I did not rerun the large wall graph or the two-worker cylinder solver.
The source and its reported finite results were sufficient for this
scope decision. This note uses a short Hall-deficit implication and
states the missing completion/retention/capacity hypotheses explicitly.
It is not a new lower-bound theorem or a replacement for Claim 35.
