# S1: a simpler replacement for PROOF_5N.md section 5

2026-10-03, KT Lower Bounds. Task S1 (CR order). Scope: section 5 of
`gap/turnstheory/PROOF_5N.md` ("finite strong strip certificate").
Labels: PROVEN, CERTIFIED, MEASURED, ARGUMENT, CONJECTURE.
None of this is audited yet.

## 0. Result in one paragraph

I did not find a hand proof of the section 5 statement at rate one.
I found a much smaller certificate and a hand identity that explains it.
The best option is option C below:

* A cut-state certificate replaces the 184,006-state graph.
  It has **3,136 states and 48,510 arcs**. It does **not use the forest
  (no-cycle) condition**. The checker is one file of about 130 lines,
  standard library plus NumPy, with no project imports. It runs in 4 s
  and 40 MB (MEASURED, 2026-10-03). The side constant improves from 37 to 28.
* A hand identity (section 2) gives the base rate "one crossing per row"
  with no computer. The computer is necessary only for the extra crossing per g-row.
* Routes (a) and (b) fail for a reason that I can show: any rate-one
  argument must move charge across an unbounded number of rows (section 3).
  A local (bounded-window) hand argument gives at most rate about 1/2. That
  gives about 4.5n, which is worse than the audited 24n/5. Thus I do not
  recommend route (b).

## 1. Option C: the cut-state certificate (best option)

### 1.1 The interface (unchanged)

Section 6 uses only inequality (8), through this statement from section 5:

    G_strong <= sum_sigma X_sigma - 4n + C_strip.          (S)

The current proof has C_strip = 37. Option C proves (S) with C_strip = 28.
Then (8) becomes G_strong <= T + 1130 <= T + 1160. Thus sections 6 and 7
and the theorem X >= 5n-612 do not change. (With 1130, the constant could
become 5n-597. I do not propose that change.)

### 1.2 Model

Side frame: inward column x = 0..3, row y. S_sigma is as in section 3:
all tour edges with an endpoint in column 0 or 1. Every vertex in
columns 0 and 1 has degree 2 in S_sigma. Every vertex in columns 2 and 3
has degree at most 2. **No other condition is used.** In particular,
S_sigma can contain cycles. Thus the model is a relaxation of the
section 5 model, and the certificate applies to the forest case too.

* A **cut state** is the set of S-edges that cross the cut between rows
  r and r+1 (lower end at row <= r, upper end at row >= r+1). Only 12
  edges can cross a cut. There are 3,136 reachable cut states.
* A **row arc** goes from the cut below row r to the cut above row r.
  It selects the S-edges whose lower endpoint is in row r, subject to
  the degree rules. Its weight w is the number of new proper crossings
  (new edge with pending edge, and new edge with new edge). Thus the
  later lower endpoint owns each crossing, as in section 5.
* The **row mask** is the set of S-edges that meet row r. It is the
  union of the two cut states and the new edges. The UP and DOWN
  indicators g are the section 4 indicators of this mask. The checker
  hard-codes the eight endpoint coefficients, the exception pair and
  the seven UP VIS pairs. DOWN uses their reflections y -> -y.
  The verifier's Claim 42 geometry check shows that the seven DOWN VIS
  pairs are exactly the reflections of the seven UP pairs.

The section 5 cell graph processes one cell at a time. It needs the
full-mask augmentation only to evaluate g at the row end. The row arc
contains the row mask directly. Thus neither the augmentation nor the
path labels are necessary.

### 1.3 Certificate (CERTIFIED, 2026-10-03)

Integer potentials h_up and h_down exist on the 3,136 cut states. For
every row arc u -> v in each orientation,

    4w - 4 - 4g + h(u) - h(v) >= 0.

The checker finds them by Bellman-Ford from the all-zero vector (every
state is a permitted start). It reaches a fixed point after 8 passes in
each orientation. Then it checks every arc.

| Quantity | Option C | Section 5 now |
| --- | ---: | ---: |
| States | 3,136 | 184,006 |
| Arcs | 48,510 | 343,631 |
| Uses forest / path labels | no | yes |
| h_up range | [-24, 0] | [-29, 0] |
| h_down range | [-28, 0] | [-33, 0] |
| Interface h_up - h_down | [0, 4] | [-4, 4] |
| Per-side error, scaled by 4 | 28 | 37 |
| Run time / memory | 4 s / 40 MB | about 22 s |

The join is the same as in section 5. Split each side at row n/2. Use
UP on the first half and DOWN on the second half. Use the common cut
state m at the split. With start state a and end state z:

    4(X_sigma - n - G_sigma) >= h_up(m) - h_up(a) + h_down(z) - h_down(m)
                             >= 0 - 0 + (-28) = -28.

Sum over the four sides: G_strong <= sum X_sigma - 4n + 28. This is (S).

### 1.4 Proposed text for section 5

Replace paragraphs 1-4 of section 5 ("Each S_sigma is ..." through
"...checked common-state interface is essential to this presentation.")
by sections 1.2 and 1.3 above. Keep the corner paragraph
("A pair counted in two adjacent strips ...") and (8) as they are.
Delete the last sentence of section 5 ("The forest condition is where
Hamiltonian connectivity enters the proof."). It is not true for option
C: the strip certificate does not use connectivity. Also delete "is a proper
subgraph of the connected tour, so it is a forest" from the first sentence. See section 5 of this
file for the effect of that.

The Turns Theory agent and the Verifier must decide about this edit. I did not
edit PROOF_5N.md.

## 2. The hand part: an exact local identity for the base rate

### 2.1 Statement (PROVEN by the hand computation below; MEASURED on tours)

For one side, let m(q) be the number of S-tiles that contain the
quarter q. Use only squares of the board. Then

    2 X_sigma = 2n + 6 + H0 + c + (1/2) sum_{q in col 1} |m(q)-1|
                + sum_{q in cols 0,1, m>=1} binom(m(q)-1, 2)
                + sum_{q in cols >= 2} binom(m(q), 2) + X1_sigma.      (K)

Here H0 counts holes (m = 0) in square column 0, c counts S-edges
(1,y)--(2,y+-2), and X1_sigma counts crossing pairs of S whose tiles
share exactly one quarter. Every term after 2n+6 is nonnegative. Thus

    X_sigma >= n + 3      for every side of every closed tour.

This is the base rate (one crossing per row) with no computer and no
connectivity.

### 2.2 Proof

Call an S-edge type a, b, c or d when it joins columns {0,1}, {0,2},
{1,2} or {1,3}. Its tile has 4 quarters in column 0 (type a), 2 in
column 0 and 2 in column 1 (type b), 4 in column 1 (type c), or 2 in
column 1 and 2 in column 2 (type d). Degree two in columns 0 and 1 gives

    a + b = 2n,       a + c + d = 2n.

Square columns 0 and 1 each have 4(n-1) quarters, and only S-tiles meet
them. Let H0, H1 count holes and exc0, exc1 = sum (m-1)_+ in these columns. Mass minus covered quarters gives

    exc0 = 4a + 2b - 4(n-1) + H0 = 2a + 4 + H0,
    exc1 = 2b + 4c + 2d - 4(n-1) + H1 = 4n - 4a + 2c + 4 + H1.

From the second line, 2a = 2n + c + 2 - (exc1 - H1)/2. Thus

    exc0 + exc1 = 2n + 6 + H0 + c + (H1 + exc1)/2.

H1 + exc1 is the sum of |m-1| over column 1. The audited tile lemma
gives 2X_sigma - X1_sigma = sum_q binom(m(q),2). For m >= 1,
binom(m,2) = (m-1) + binom(m-1,2). Insert exc0 + exc1, and (K) follows.

The averaging step is necessary. Each of the two lines alone contains the term
+-2(n-a), which can be negative. Their average has only nonnegative
local terms.

### 2.3 Checks (MEASURED, 2026-10-03)

* (K) holds exactly on all four sides of all 28 saved closed tours in
  `w-verifier/claim16_runner/` (even n = 48..102), 112 sides
  (`simple_strip/check_tours.py`, log `simple_strip/check_tours.log`).
  On the same sides, G_sigma <= X_sigma - n + 7 holds with slack 23 or more.
* Row-local form. Let kappa(r) be the part of the terms in (K) that lies in square
  row r (c-edges count 1/2 in each of their two square rows; an X1 pair
  goes to the row of its shared quarter). Then kappa(r) is a function of
  the cut state above row r. On all 48,510 row arcs,
  2kappa(v) - (4w - 4) = phi(u) - phi(v) holds exactly for a potential phi with
  range [-3, 20] (`simple_strip/kid.py`). Thus (K) is a telescoping
  per-row identity, not only a global one.

### 2.4 What remains for the computer

With (K), statement (S) is equivalent, up to a constant, to

    sum_r kappa(r) >= 2 G_sigma - C.                                 (S')

kappa(r) >= 0 always. Only 46 of the 3,136 cut states have kappa < 2.
The local inequality kappa(r) >= 2 g(r) holds on 47,648 of the 48,510
row arcs (98.2%) and fails on 862 (MEASURED). With the kappa cost
2kappa(v) - 4g, the optimal potential is zero on all but 197 states (UP) and
240 states (DOWN). Its range is 8 and 12 quarter-crossings. An LP potential with
minimum L1 norm (split kappa 1/2-1/2 between the two cuts of a row) is
nonzero on only 75 states. These are the facts that a hand proof must use.

## 3. Why routes (a) and (b) fail

### 3.1 The extremal structure (MEASURED, cut-state graph)

* With g ignored, exactly two periodic patterns have one crossing per
  row. Both have period one. P: from each row y, edges (0,y)-(1,y+2), (0,y)-(2,y+1),
  (1,y)-(3,y+1). Q is the mirror image of P. Both have kappa = 0 and g = 0 in both orientations.
* At rate one, the critical cycles include P': edges (0,y)-(1,y+2),
  (0,y)-(2,y+1), (1,y)-(2,y+2) on every row. P' has 2 crossings per row and g = 1 on every row
  (F = 1 and VIS). Thus rate one is sharp, as Claim 42 found.

### 3.2 Route (a): the potentials have no simple form

* No potential that is a linear or quadratic function of the 12
  pending-edge indicators exists (LP infeasible), for the crossing cost and
  for the kappa cost. For the crossing cost, an LP with all 297 monomials of
  degree <= 3 is feasible. I did not search for a short cubic potential.
* No two-valued potential {0, A} exists for any A (2-SAT conflict).

### 3.3 The debt mechanism: no bounded-window argument gives rate one

From P, every continuation has a nonnegative running sum of 2kappa - 4g
(single-source potential >= 0). From Q, a 7-row transition into P has
seven g-rows and kappa-cost -8. That is, two g-rows are left unpaid.
The configuration can then stay in P (kappa = 0, g = 0) for any number of rows.
Thus, for any window length L, there is a configuration in which a g-row
gets less than its share from all kappa within distance L.
The payment comes from the opposite switch P -> Q, which costs at least
+24 (six crossings above its own g-rows), and that switch can be arbitrarily far away.

The window LP agrees: with best weights on 2, 4, 6 and 8 cuts around the
row, the worst window has t = -2.8, -2.24, -2.09, -2.06 (needed: 0)
(`simple_strip/window.py`). A local hand lemma thus gets at most rate
about 1/2. With rate lambda, the final bound is 4n + lambda n. Rate 1/2
gives 4.5n, which is worse than the audited X >= 24n/5 (Claim 31).
**Route (b) has no useful weaker form: a useful rate needs lambda > 0.8,
and that needs the same nonlocal accounting as rate one.**

### 3.4 A possible hand route (CONJECTURE, not done)

A phase argument could work. Mark each row as P-phase or Q-phase by its
most recent clean pattern. Then prove three items: (i) kappa(r) >= 2g(r)
for rows that are not near a switch; (ii) a Q -> P switch leaves at most
two g-rows unpaid; (iii) a P -> Q switch has a surplus of at least two
crossings. Items (i)-(iii) need a classification of all exits from P and Q.
Section 2.4 shows that this classification touches about 200 states. I estimate
many pages of cases. I do not recommend it unless a full hand proof is
a firm requirement.

## 4. Option ranking

1. **Option C** (section 1): smaller, simpler, connectivity-free,
   better constant. Interface (S) is unchanged. Recommended.
2. Option C plus the identity (K) as an explanatory lemma: (K) proves the
   base rate by hand. The text can say that the computer is used only for
   "one more crossing per g-row".
3. Option C with the kappa cost: a potential that is nonzero on 75 states.
   It is smaller as a table, but it needs the telescoping check of (K)
   as a second finite input. Not recommended over option C.
4. Route (b): no useful version (section 3.3).

## 5. Side effect: the strip lemma does not use connectivity

The option C certificate allows cycles in S_sigma. In PROOF_5N.md, the words
connected / forest / Hamiltonian occur only in the header (line 12), the
definition of H (line 16), section 5 and the section 7 file note.
If sections 1-4 also do not use it, then the 5n-612 bound holds for every
2-factor of knight moves. The flux identity of section 2 holds for any
2-regular graph (the vertex sum uses only deg = 2). I have not checked
sections 3-4 for this. ARGUMENT, to be checked by Turns Theory and the Verifier.

## 6. Reproduction

Run from the research root.

```
.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py
.venv/bin/python gap/lowerbounds/simple_strip/check_tours.py
```

The first is the option C certificate. It prints the sizes, ranges, interface and
side constant, and saves `simple_strip/cut_potential_up.npy` and
`_down.npy`. The second checks (K) and the per-side bound on the saved tours.
The other analysis scripts in `simple_strip/` (build.py, rows.py,
nocyc.py, kappa.py, kid.py, kpot.py, ss.py, window.py, linpot.py,
quadpot.py, kfeat.py, twoval.py, sparse.py, debt_path.py) produced the
numbers in sections 2.3-3. They import verifier geometry
(`claim26_certificate`, `claim37_check`) and need `nocyc.py` and
`kappa.py` to run first.
