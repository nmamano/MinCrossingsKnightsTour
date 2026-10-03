## Claim 32 — RED TEAM: ribbon absorption toward 5n — 2026-10-03

**Verdict: GAP for the proposed 5n theorem; FAIL for an unconditional wall-face yield lemma.** The simpler route remains worth pursuing, but the supplied steps do not yet give a private price of 1/4 per original side end. I found an exact zero-crossing field that defeats R3 if its only correction is for defects. This is a counterexample to that intermediate geometric statement, not a closed-tour counterexample to X >= 5n-O(1).

Sources: gap/structures/PLAN.md point 2, FINDINGS.md G9–G10, STRUCTURE.md, and the audited tile/boundary budget. I also read G11's pilot description to distinguish its fixed straight-interface model from the proposed universal claim. Source hashes and sizes: claim32_sources.json. All checks were light, single-process checks; no optimisation or large graph job was run.

### 32A. PROVEN counterexample: a wall can send its strands to other walls for free

On the whole integer plane choose every edge

    (x,y) -- (x+2,y+1)     when y is even,
    (x,y) -- (x-2,y+1)     when y is odd.

Every vertex has one edge to the row above and one to the row below. Edges in one open horizontal slab are parallel; different open slabs are disjoint. The field therefore has degree two and no crossings. It is the fold stack with f=y and alternating choices (2,1), (-2,1).

Every square in an even row has slash split; every square in an odd row has backslash split. The tiles cover all quarters exactly once. Thus **every integer horizontal line is a wall and there are no defects anywhere**. All ribbons incident to a wall have the required H bit. The complete strands are explicitly

    P_k(y) = (k + 2*(y mod 2), y),    y in Z.

They are strictly monotone in y and stay between x=k and x=k+2. In a rectangle, all strands whose two x coordinates are strictly inside it run from bottom to top. They do not return to a vertical side. A horizontal wall segment can have arbitrarily large length while almost all its incident strands are of this type. Only O(1) strands near either vertical boundary can meet that boundary. No defect correction explains this loss, because there are no defects.

This breaks R3 as a statement that each face of length l yields l/2-O(defects) distinct same-vertical-side strands. It also breaks any attempt to price all wall faces independently: this field has arbitrarily many wall faces at zero crossing cost. The same strand meets arbitrarily many faces. The existence of many such faces cannot create many independent connectivity obligations.

Independent exact check: claim32_pleats.py enumerates 625 edges in a padded window, checks all crossing pairs (zero), verifies degree two at 144 core vertices and exact coverage at 576 core quarters, and traces three interior strands from bottom to top. Output: claim32_pleats.json. The formulas above prove the family for every size; the window check only corroborates it.

**Required repair.** Give each original side end a persistent label. At a wall, either prove a return to the same side, or transfer that label through a precisely defined strand/face relation. A face has a price only for labels that ultimately create distinct connectivity obligations. A wall-to-wall transfer is free in this example. Any number of such transfers must be handled without a separate O(1) loss per wall. If R3 was intended only for isolated chevrons already connected to one vertical side, state that hypothesis: deriving it from the general ribbon decomposition remains a new lemma.

The example is a full-plane field and an open-window restriction, not a closed Hamiltonian tour. It does not satisfy a specification of four cheap, closed board sides. It therefore leaves open whether global side conditions can force enough *labelled* returns. It shows that the asserted local geometry does not supply that conclusion by itself.

### 32B. PROVEN local propagation; GAP in the global end count and assignment

Claim 30's repair is essential here. A bit propagates along one uninterrupted good half-ribbon run. It need not propagate across a bad interruption, even within one connected good domain. The validated n=96 tour in Claim 30B has H and V on two runs of ribbon 1 in the same connected slash domain. Consequently, an end cannot be transported past that interruption using the full-plane word model. The interruption must be entered in the absorber ledger at that point.

For a straight uninterrupted ribbon that actually reaches perpendicular cheap sides, incompatible H/V requirements do force an interruption or wall encounter. This supports the local obstruction in R2. It does not establish the full accounting inequality as written. The count 4n-O(1) requires a defined scan curve with one side-end slot per row, including rows whose collar has defects or a non-cheap pattern. G10 optimises a side attached to a *fixed* exterior word; it does not prove that every arbitrary tour has this collar decomposition or price a nonperiodic side carrying current.

The revised count should map each of these fixed boundary slots either to one labelled good run or directly to a paid side exception. Count the first absorber of that label once. Do not count the two sides of an interior run as two new original side ends. Do not replace defect-separated runs by a single word. The statement “a defect cut absorbs at most two ends” can hold for a specified cut of a specified ribbon, but does not mean one bad square is one such cut: a slash square contains halves of two different ribbons.

### 32C. GAP: a price in crossings is not yet an extra price above 4n

There are two different baseline arguments. The area proof gives X >= 4n-2 from total tile area; it does not identify 4n particular crossing pairs that can simply be removed. The audited boundary certificate does identify a set B with |B| >= 4n-24. A clean sufficient version of the new route is therefore a total absorption allocation of at least n-O(1) supported on crossing pairs outside B, with total allocation at each such pair at most one.

Side repairs can also use surplus crossings inside B, but then they need one combined residual budget. For example, reserve a baseline of 4n-24 inside B and allow only its remaining capacity plus X-|B| to pay absorbers. The total available capacity is X-4n+24. A crossing counted in a side-strip objective cannot also pay a nearby defect or seam at full strength. Unit capacity is global across all absorber types, not merely within each type.

This distinction matters for holes. A bad square need not contain a crossing at all. T4 bounds bad squares in U by E+X-|B|, with E=X-4n+2. With only |B| >= 4n-O(1), that is at most 2E+O(1). It does not assign a distinct crossing unit to each defect. For illustration, even if one separately proved at most four end labels per bad square, this budget alone would give at most 8E+O(1) labels and hence only E >= n/2-O(1) from 4n labels. This is a diagnostic calculation, not a new certified bound. A stronger defect inequality or an explicit allocation is needed for E >= n-O(1).

The gentle-seam price of 1/4 per end has no spare capacity for duplicate labels or overlap with side charges. A finite band optimum with fixed exterior fields does not certify arbitrary bent, merged, or terminated defect sets. G11 itself records the width and period restrictions. Its zero-cost walls also require the global connectivity argument refuted in its unconditional form in 32A.

### 32D. Status of the proposed steps and smallest useful repair

| Step | Audit status |
| --- | --- |
| Good-run H/V propagation and local wall orientation | PROVEN, with Claim 30's run and degree hypotheses |
| Cheap arbitrary side implies the required labelled H/V collar | GAP; G10 supplies restricted model evidence |
| Every original boundary end reaches a first absorber | ARGUMENT until slots, collars, run interruptions, and transfers are defined |
| Every wall face yields l/2 same-side strands up to defect losses | FAIL without added global hypotheses; alternating horizontal walls are a counterexample |
| A fixed P-compatible chevron strand needs a changed edge end | PROVEN in Claim 28's fixed-matching scope |
| Changed-end price 1/2 | CERTIFIED for the fixed exterior, W<=4 model in Claim 28; universal version remains GAP |
| Every defect/seam/side absorber pays 1/4 privately | CONJECTURE; no general allocation is provided |
| Adding the absorber prices to 4n | GAP until one baseline-residual ledger is proved |

The next hand lemma should describe labelled side ends under wall-to-wall transfers, with no per-wall loss. It must explicitly pass the alternating-wall field above and Claim 30's interrupted-ribbon example. Only then is a finite defect-price search measuring the needed quantity. A sufficient final target is: at least 4n-O(1) original labels receive weight 1/4, and the total weight charged to all residual crossing capacity is at most that capacity. This target includes side, wall, and defect repairs in one inequality.

**Pareto profile.** No new lower-bound coefficient is proved or refuted here. The counterexample is a two-line edge formula with an elementary slab argument; its finite input is zero. The exact 625-edge check is optional corroboration. The proposed 5n route has short geometric components, but its unresolved global transfer and residual-budget lemmas cannot yet be counted as a short proof. It remains a useful primary target after these repairs.

Claim 32 is complete. No author files were edited. The outstanding mathematical work is to replace R3 by a labelled transfer/return lemma and then prove a joint extra-crossing budget.
