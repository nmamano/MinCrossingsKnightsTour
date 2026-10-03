# Claim 51: strong-end filtering and scalar quarter proof — 2026-10-03

**PASS.** Section 1 of `gap/turnstheory/PROOF_5N_SIMPLE.md` correctly proves

    X >= 5n-(32+C/2)

from the stated global strip black box T>=b-C, for even n>=32. In particular C=1160 gives 5n-612. The keep rule, distinct-row injection, usable-quarter exclusion, scalar inequality and final algebra are valid. The black box is exactly the one supplied by Claim 42, or by the smaller certificate audited in Claim 50.

This is a genuine shortening of the hand argument. No deficient-path case split, private resource allocation or good-middle lemma is needed. It still depends on the audited tile/flux/endpoint geometry and the strong strip certificate. No source proof or blog post was changed.

## 51A. KEEP and z<=b — PASS

A row is strong if at least one of the following holds: the oriented F value differs from two modulo three, the endpoint exception is present, or VIS is present. Thus a kept candidate has both ordinary endpoint tests passing, both exceptions absent and both visibility flags zero.

For each corner, the radii 12 through n/2-4 give n/2-15 candidates; over four corners N=2n-60. The squares on one candidate have maximum corner coordinate r. Different radii therefore use different squares. The four corner boxes are disjoint in the stated range.

On a fixed physical side, the two corners use vertex rows in the disjoint intervals

    [12,n/2-4] and [n/2+3,n-13].

Each row in these intervals belongs to one candidate only. Choose one strong endpoint of each discarded candidate. The chosen objects are (physical side, vertex row) pairs, precisely the objects counted by b. This is an injection, even when a discarded candidate has two strong endpoints or a crossing contributes to more than one physical strip. Hence z<=b. Extra strong rows outside the candidate-end intervals only make the inequality easier.

The first interval uses UP and the second DOWN. At a DOWN vertex row t the endpoint square has row t-1, as required by the audited test. No parity bit or unshifted reflection is being substituted.

## 51B. Each kept path supplies two distinct bad quarters — PASS

Write c=(-1)^r. The audited passing-endpoint calculation gives each endpoint residue two modulo three. Their sum is one modulo three, so the internal candidate is charged. This use of the endpoint lemma needs only its passing case, not a retention classification for the other values.

Equivalently, combining the two endpoint and outer-boundary terms gives the congruence

    outside flux = 1+c(F_left+F_bottom+5) modulo three
                 = 1 modulo three,

because both F values are two modulo three. This also explains the source's representative 1+3c. Only the congruence, and hence nonzero charge, is needed.

If every quarter in the squares traversed by the candidate were good, the local flux identity would give zero modulo three on every dual step. Thus some traversed square has a bad quarter. Every tile contributes equally to the two alternating pairs of quarters in a square; consequently m_B-m_R+m_T-m_L=0. Three multiplicities equal to one force the fourth to equal one. A bad square therefore has at least two bad quarters.

The two selected quarters can be taken from this one bad square. Candidate squares are disjoint, so selecting two per kept path produces 2M distinct quarters, without a matching or allocation argument.

## 51C. No forbidden overlap — PASS

Suppose a quarter on a kept path has multiplicity two and its unique pair belongs to S with a two-quarter overlap. Choose a physical side whose strip contains both edges. Every such strip edge touches vertex column zero or one and reaches vertex depth at most three. Its open quarters have square depth at most two.

A candidate square is (r,j) or (j,r) in its corner frame, with r>=12. If it is within square depth two of a side, that side is the corresponding endpoint side and its along-side square row is the endpoint row in the appropriate orientation. The other local side has depth r, and the opposite board sides have depth at least n-2-r>=n/2+2. Thus no unrelated side can supply the assumed overlap.

There are now exactly the two audited geometric cases:

* If both edges touch the outer column, a pair that reaches a candidate end square is the endpoint exception (or its reflected copy). The ordinary endpoint test would fail.
* Otherwise the two-quarter overlap is a VIS witness for that endpoint. The end would be strong.

Both contradict KEEP. DOWN uses the reflected square row, not the same square row as UP. Claim 42's one-exception/seven-VIS geometry and Claim 50's independent reflected VIS derivation cover exactly these cases.

Hence every bad quarter on a kept path is usable under the new definition. In particular the 2M quarters from 51B are usable. The proof does not require a separately named outer-column pair set B, a test only at large radii, or an interior-versus-end payment split.

## 51D. D+X1=2E and the scalar count — PASS

All sums here must be over the 4(n-1)^2 quarters of board squares. For an integer multiplicity m>=0, put

    d(m)=binom(m,2)-m+1=(m-1)(m-2)/2.

Then d(0)=1, d(1)=d(2)=0 and d(m)>=1 for m>=3. In particular the summand is nonnegative; the polynomial notation at m=0 is expressly valid in this definition.

There are n^2 selected knight edges and four quarter incidences per tile. The one/two-quarter overlap lemma gives sum binom(m,2)=2X-X1. Therefore

    D = 2X-X1-4n^2+4(n-1)^2 = 2E-X1,
    D+X1=2E.

This proves E>=0 as well. It includes every hole and every higher-multiplicity term, with no missing boundary correction.

For any set Q of usable bad quarters, split it by multiplicity. The multiplicity-zero and multiplicity-at-least-three quarters number at most D, because each contributes at least one to D. Every remaining quarter has m=2 and a unique covering pair. If that pair is outside S, it can account for at most two such quarters; there are X-s outside pairs. If the pair belongs to S, usability forces a one-quarter overlap, and it accounts for at most one quarter counted by X1. Thus

    |Q| <= D+2(X-s)+X1
         = 2E+2(X-s)
         = 4E-2T.

S must be the UNION of within-side crossing-pair sets, as defined in the source. Replacing s by the sum of the four side counts would invalidate this interpretation of X-s. Counting some outside-S one-quarter pairs again in the X1 upper bound causes no problem: the argument is an upper bound on |Q| by larger counts, not a claim of a disjoint capacity allocation.

## 51E. Finish and black-box match — PASS

Apply the scalar inequality to the 2M selected usable quarters, and then use the black box and row injection:

    4E >= 2M+2T
        >= 2(N-z)+2b-2C
        >= 2N-2C.

Since N=2n-60 and X=E+4n-2, this is exactly

    E >= n-30-C/2,
    X >= 5n-(32+C/2).

There is no need for T to be nonnegative and no need to retain all charged paths. Discarding a formerly payable path is harmless because its selected strong row is already covered by the SAME global numerical black box.

The notation matches the certified inputs as follows:

| Simple proof | Audited strip input |
| --- | --- |
| S, a union of crossing-pair sets | S* in PROOF_5N.md / Claim 42 |
| s=|S| | Same union cardinality |
| b | G_strong, one OR flag per oriented side row |
| F, exception, VIS | Same eight coefficients, pair and visibility geometry |
| UP/DOWN split | Same first-half/second-half scan, DOWN square row r-1 |
| T=s-4n+2 | Same T |

Claim 42 proves b<=T+1139, hence b<=T+1160. Claim 50 proves b<=T+1130, again implying exactly (S) with C=1160. The four-side union correction 1104 is already included in these constants. It is not added or spent again in section 1.

The source's fallback C=1164 is also correct for the old separately bounded half-side potentials: the per-side error is (29+33)/4=31/2; four sides and the corner correction give b<=s-4n+1166=T+1164. This yields 5n-614. No fallback is necessary when using either audited common-state interface.

The direct proof applies for even n>=32. For the two numerical choices C=1160 and C=1164, the stated smaller positive even sizes satisfy the inequality trivially because the right-hand side is negative.

## 51F. Small clarifications for the presentation

No mathematical repair is needed. Two one-line clarifications would make the shorter text fully explicit:

1. Before defining D, add: “All quarter sums are over the 4(n-1)^2 quarters of the board squares.” Otherwise a reader extending m=0 outside the board could misunderstand the summation domain.
2. Express the passing-case flux statement as a congruence: “The passing endpoint calculation gives outside flux congruent to 1+3*(-1)^r, hence to 1 modulo three.” The proof uses a modular representative, not a fixed exact integer flux value for every passing edge configuration.

The source's “option C awaits independent audit” notes are now superseded by Claim 50. This audit did not edit them.

## 51G. Degree-two scope

The hand proof uses simplicity, legal knight edges, spanning degree two, the finite board and the strip black box. It does not use one-cycle connectivity. In particular n^2 edges and the mod-three zero circulation follow from degree two; all crossing-pair counts include pairs from different components if present.

Claim 50's cut-state input also uses only the strip degree constraints and includes cycles. Thus this simplified proof together with Claim 50 supports the stated section-7 extension to spanning SIMPLE knight 2-factors, with X counting all proper unordered crossing pairs. The old forest certificate alone would not justify that extension. No connected-tour hypothesis is silently used in the new filtering or scalar count.

## 51H. Checks and proof size

The hand arguments above are the audit. As an extra implementation check, `claim51_check.py` uses the independent Claim 50 tile geometry and flags to count the new kept set, all usable quarters, endpoint ownership and both scalar identities on three saved tours:

| Tour | N | M kept | z discarded | b | D | X1 | Usable quarters | 4E-2T |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD n=144 | 228 | 219 | 9 | 45 | 574 | 326 | 1253 | 1386 |
| Claim 47 patched n=288 | 516 | 471 | 45 | 81 | 1562 | 898 | 3081 | 3882 |
| FJOG n=132 | 204 | 169 | 35 | 66 | 1158 | 240 | 2158 | 2566 |

All checks passed. In each case every bad quarter of every kept path is usable, the selected 2M quarters are distinct, the chosen strong rows for discarded paths are distinct, and D+X1=2E exactly. The examples are not a substitute for the all-board proofs above.

Run `python3 gap/verifier/claim51_check.py` from the research root. Results are in `claim51_check.json` and `claim51_check.log`; source hashes are in `claim51_sources.json`.

Proof size: the shared tile/flux/passing-endpoint geometry, a keep/discard injection, one bad-square argument, one exclusion argument and one scalar count. The numerical finite input remains the strong strip certificate; with Claim 50 it has 3,136 states and 48,510 arcs. No new finite theorem, component classification, Hall argument or untrapping lemma is needed for this reorganization.
