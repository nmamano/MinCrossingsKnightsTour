# Claim 49: residual payment for untrapping — 2026-10-03

**PASS in the requested red-team sense: no counterexample found to the revised depth-6 L5 in BEYOND5 13.7. This is not a proof of L5.** I tested existing closed-tour patch families, the defect-rich FJOG tour, and 2,964 single-cycle deep two-edge switches inside fixed chambers. A saved new switched tour passes the complete tour checker. None makes residual bad quarters grow too slowly for the new inside returns.

There is an important scope distinction: the existing Structures chamber implementation still uses the depth-3 cut. Applying that older count to Claim 47 gives many shallow inside returns with no deep payment. Moving the cut to depth 6 removes that example. It is not a counterexample to the requested revised L5.

## 49A. Definitions and audit scope

The source is `gap/structures/BEYOND5.md` section 13.7 L5, with REGION and U_in from SHEET 13. An inside return has both ports on a chamber's side interval and its interior path stays in the region plus barrier. U_in counts such returns with no changed end. The claim requires two residual quarter units per such return, after route (i), up to a bounded error.

`chamber_scan.py`, `chamber_ledger.py` and `c5_chamber.py` still put the collar boundary at depth 3. I preserved those sources and made local diagnostic copies with the boundary at depth 6 (line x=5.5), translating the interior bounds, boundary-square starts and good-run barrier termination together. The translated port test uses the same sign/line-label P-partner rule. These copies are `claim49_chamber6.py` and `claim49_ledger6.py`. Their output is a concrete interpretation of the proposed depth-6 statement, not a completed proof that all of L3/L4 carries over unchanged.

For spatial quarter ownership I used the explicit rule in `c5_chamber.selections`: choose at most two deep bad quarters of each retained candidate, greatest board depth first, then lexicographic quarter order. I rebuilt quarter multiplicities and these selections independently of the author's chamber payment totals. The global retained-candidate builder is the previously audited `check_hall_v3.geometry`. At depth at least five the bad quarters are payable. All candidate selected sets are checked disjoint.

This tie rule matters: `beyond5_ledger.py` defines the global BQx count by subtracting min(2, deep count), but does not specify a spatial allocation. A statement about BQx(REGION) must fix an allocation or quantify over its choice. The diagnostic below uses the existing spatial implementation's allocation.

## 49B. The old shallow example does not defeat the new target

The original depth-3 chamber census on the Claim 47 n=288 tour gives

    U_in = 59, BQx(REGION) = 0, selected quarters in REGION = 0.

These inside returns use the shallow collar affected by the 6-by-24 patches. The patches change only vertices at depths zero through five. They preserve the stubs on x=5.5 and their exact pairing through that collar; all interior edges beyond it stay fixed. With the depth-6 diagnostic, the same tour gives

    U_in = 1, BQx(REGION) = 0.

Thus the count 59 cannot be used as a depth-6 counterexample. The remaining deficit of two quarter units is compatible with the allowed constant. This also shows why a proof cannot silently reuse the old depth-3 count and require its shallow defects to be paid by deep BQx alone.

The Claim 38 boundary replacement at n=144 similarly gives only two depth-3 inside returns and zero region BQx. Ordinary FOLD n=144 has three at depth 3 and one in the depth-6 diagnostic. These are bounded examples, not violations of a statement with O(1) error.

## 49C. New deep-switch search and witness — CERTIFIED finite checks

Starting from the audited FOLD n=144 closed tour, I enumerated two-edge switches wholly inside one fixed depth-6 chamber. For tour-oriented edges a->b and c->d, the replacement is a--c and b--d. Four distinct endpoints and two new legal knight edges are required. This operation reverses one tour segment and retains a single cycle. The search also requires:

* The two source chords are distinct inside returns of the same chamber.
* Every affected tile quarter is deep and in that region, so its good barrier stays unchanged.
* The original collar and all its port pairings stay unchanged.

There are 2,964 admitted switches. Every one creates one additional return without a changed end and adds 16 bad quarters to its region. I then recalculated the route-(i) selected quarters on every affected retained candidate for every switch. The result is identical in all 2,964 cases:

    delta U_in = 1,
    delta raw deep BQ(region) = 16,
    delta selected quarters in region = 0,
    delta BQx(region) = 16,
    delta [2 U_in - BQx(region)] = -14.

Thus this complete finite search over the stated switch class does not realize the double-use risk. It does not exhaust larger patches, multiple coordinated switches, or different base fields.

One actual switch was saved and rechecked as a full tour:

    removed: (97,134)--(98,136), (99,133)--(100,135),
    added:   (98,136)--(100,135), (97,134)--(99,133).

The saved tour `claim49_deep_switch_n144.json` passes degree, reciprocal-edge, knight-move and single-cycle checks. A fresh chamber census gives U_in=2 and region BQx=16, versus 1 and 0 before the switch. The new crossings are 1032 versus 1024. This constructs a deep untrapping modification, but it pays eight times the proposed two-quarter rate rather than violating it.

Search and ownership evidence: `claim49_switch_search.py/json`, `claim49_switch_marks.py/json`. The search uses no solver. Its raw-price result and its post-selection result are separate checks.

## 49D. Region counts and the joint strip term

The following table uses the depth-6 diagnostic. REGION values sum over the reported chambers. J uses the original joint-strip convention: side rows 8 through n-9, S3 crossing ownership by the later lower endpoint, and the full-halo Q3 atoms in square columns zero through four. I independently counted J from exact tile intersections/multiplicities, rather than using the old port-weight proxy.

| Tour | U_in | Region BQx | Selected in regions | 2J | Global BQx | K | C5-J | C5-J minus 4n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FOLD n=144 | 1 | 0 | 0 | 796 | 356 | 7 | 1138 | 562 |
| New deep switch, n=144 | 2 | 16 | 0 | 796 | 372 | 7 | 1154 | 578 |
| FJOG n=132 | 113 | 955 | 0 | 559 | 1336 | 17 | 1861 | 1333 |
| Claim 47 patched n=288 | 1 | 0 | 0 | 2780 | 590 | 28 | 3314 | 2162 |

Here C5-J=2J+BQx-2K. All four examples already have positive joint-count margin. In particular the Claim 47 tour still has the large strip surplus identified by Claim 48. The deep switch leaves J and K unchanged and adds 16 to global BQx. It therefore also raises C5-J.

FJOG is the useful many-return test: it has 113 untrapped inside returns in this interpretation and 955 residual region quarters, well above the required 226. Some of its retained candidate paths do meet region bad quarters, but the implemented deepest-first selections occur elsewhere. This observation is not a general separation theorem.

The original depth-3 FJOG census, reproduced separately, gives U_in=173, region BQx=1034 and zero selections in those regions. Those numbers match the earlier Structures calculation but are not the width-6 counts above.

## 49E. What remains open; exact requirements for a proof

No closed-tour family or certified periodic patch with a linear residual-payment deficit was found. The gentle-seam risk from Claim 44E remains: a bound on raw carrier quarters does not by itself imply the same bound after subtracting candidate payments. The present switch search finds expensive defects, not a joint carrier theorem.

Before L5 can be proved or universally tested, specify:

1. The width-6 chamber and P-class definitions, including which boundary squares belong to REGION. The available author scripts implement depth 3; the local copies used here are explicitly a translated diagnostic.
2. A spatial rule for the two selected deep quarters, or an existential/universal quantifier over choices. The global count alone does not define BQx(REGION).
3. Whether the error is one constant in total or one per chamber. A bounded observed deficit cannot refute O(1), and linear chamber counts require the separate L9 error control.

In particular, do not promote the square Gap Lemma's raw-quarter price to L5 without a joint ownership argument. The tests here give no evidence against the revised L5, but they do not supply that argument.

## Reproduction and proof size

From the research root:

    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim49_switch_search.py
    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim49_switch_marks.py
    OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim49_census6.py gap/verifier/claim49_deep_switch_n144.json

`claim49_census.py` runs the old depth-3 version; `claim49_census6.py` runs the diagnostic depth-6 version. Saved census JSON files have the matching `claim49_` or `claim49_w6_` prefix. Sources and witness hashes are recorded in `claim49_sources.json`.

Finite input: a finite enumeration of 2,964 switches in one n=144 tour, one saved switched tour, and exact censuses of the listed tours. No transfer graph or new solver certificate was used. The result is a bounded red-team search with a stated scope, not an asymptotic lower-bound proof.
