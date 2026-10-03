import Ktlean.Tour

/-!
# The corner certificate: `8 * n - 28` turns

The proof of `TwoFactor.eight_mul_le_numTurns_add` loses up to 16 turns in each 4 × 4 corner.
Here we write the four-column lemma as a sum of local bounds `Lside` (Section "Lower bound" of
`writeup/turns/main.tex`): `t v ≥ Lside d v` for every cell, and the sum of `Lside d` over the
board is exactly `2 * n` for each side. Thus `T - 8 n = Σ_v (t v - Σ_sides Lside)`, the summand is
`≥ 0` outside the four corners, and a corner lemma bounds the sum over each corner.

The corner lemma is a parameter: `CornerBound c` says that the sum over every corner is at least
`-c`. `TwoFactor.eight_mul_le_numTurns_add_of_cornerBound` gives `8 n ≤ T + 4 c`.
A `CornerCert` (numbers `alpha` on the 16 corner cells, numbers `beta` on edges inside the corner)
whose local inequalities hold (a decidable finite check) gives `CornerBound (-Σ alpha)`.
The certificate of Lemma 3 of `main.tex` has `Σ alpha = -7`, so every 2-factor and every closed
tour has at least `8 n - 28` turns.
-/

open Finset

namespace KT

section Local

variable {α : Type*}

/-- The local bound at a cell at distance `i` from a side whose two neighbours are at distances
`c1` and `c2` from the same side. -/
def Lloc (i c1 c2 : ℤ) : ℤ :=
  if i = 0 then 1
  else if i = 1 ∨ i = 2 then
    (if c1 = 0 ∨ c1 = 3 then 1 else 0) + (if c2 = 0 ∨ c2 = 3 then 1 else 0) - 1
  else if i = 3 then
    1 - (if c1 = 1 ∨ c1 = 2 then 1 else 0) - (if c2 = 1 ∨ c2 = 2 then 1 else 0)
  else 0

/-- The local bound `L_i(v)` of the four-column lemma, for the side at distance `d`. -/
def Lside (N : α → Finset α) (d : α → ℤ) (v : α) : ℤ :=
  if d v = 0 then 1
  else if d v = 1 ∨ d v = 2 then ((N v).filter fun u => d u = 0 ∨ d u = 3).card - 1
  else if d v = 3 then 1 - ((N v).filter fun u => d u = 1 ∨ d u = 2).card
  else 0

lemma card_filter_pair [DecidableEq α] {u w : α} (huw : u ≠ w) (p : α → Prop)
    [DecidablePred p] :
    ((({u, w} : Finset α).filter p).card : ℤ) =
      (if p u then 1 else 0) + (if p w then 1 else 0) := by
  rw [filter_insert, filter_singleton]
  by_cases hu : p u <;> by_cases hw : p w <;> simp [hu, hw, huw]

lemma Lside_pair [DecidableEq α] {N : α → Finset α} {d : α → ℤ} {v u w : α} (huw : u ≠ w)
    (h : N v = {u, w}) : Lside N d v = Lloc (d v) (d u) (d w) := by
  unfold Lside Lloc
  rw [h, card_filter_pair huw, card_filter_pair huw]
  split_ifs <;> omega

lemma Lside_eq_zero {N : α → Finset α} {d : α → ℤ} {v : α} (h : 4 ≤ d v) : Lside N d v = 0 := by
  unfold Lside
  split_ifs <;> omega

/-- The local fact of the four-column lemma: `t v ≥ L(v)`. -/
lemma Lside_le_turn (N : α → Finset α) (hcard : ∀ v, (N v).card = 2)
    (d : α → ℤ) (hd0 : ∀ v, 0 ≤ d v)
    (hstep : ∀ v, ∀ u ∈ N v, d v - 2 ≤ d u ∧ d u ≤ d v + 2 ∧ d u ≠ d v)
    (turn : α → Prop) [DecidablePred turn]
    (hturn : ∀ v, ¬ turn v → ∃ u ∈ N v, ∃ w ∈ N v, d u + d w = 2 * d v) (v : α) :
    Lside N d v ≤ if turn v then 1 else 0 := by
  classical
  obtain ⟨u, w, huw, h⟩ := card_eq_two.1 (hcard v)
  have hu := hstep v u (by rw [h]; simp)
  have hw := hstep v w (by rw [h]; simp)
  have := hd0 u; have := hd0 w; have := hd0 v
  rw [Lside_pair huw h]
  by_cases ht : turn v
  · simp only [ht, ite_true]; unfold Lloc; split_ifs <;> omega
  · simp only [ht, ite_false]
    obtain ⟨u', hu', w', hw', hs⟩ := hturn v ht
    rw [h] at hu' hw'
    simp only [mem_insert, mem_singleton] at hu' hw'
    have hsum : d u + d w = 2 * d v := by
      rcases hu' with rfl | rfl <;> rcases hw' with rfl | rfl <;> omega
    unfold Lloc; split_ifs <;> omega

/-- The sum of the local bounds over a four-column strip is exactly `2 * m`. -/
theorem sum_Lside [Fintype α] (N : α → Finset α) (hcard : ∀ v, (N v).card = 2)
    (hsymm : ∀ v u, u ∈ N v → v ∈ N u)
    (c : α → ℤ) (hc0 : ∀ v, 0 ≤ c v)
    (hstep : ∀ v, ∀ u ∈ N v, c v - 2 ≤ c u ∧ c u ≤ c v + 2 ∧ c u ≠ c v)
    (m : ℕ) (hcol : ∀ k : ℤ, 0 ≤ k → k < 4 → (univ.filter fun v => c v = k).card = m) :
    ∑ v, Lside N c v = 2 * m := by
  classical
  set A0 := univ.filter fun v => c v = 0
  set A3 := univ.filter fun v => c v = 3
  set A12 := univ.filter fun v => c v = 1 ∨ c v = 2
  have hA0 : A0.card = m := hcol 0 (by norm_num) (by norm_num)
  have hA3 : A3.card = m := hcol 3 (by norm_num) (by norm_num)
  have hA12 : A12.card = 2 * m := by
    have h1 := hcol 1 (by norm_num) (by norm_num)
    have h2 := hcol 2 (by norm_num) (by norm_num)
    rw [show A12 = (univ.filter fun v => c v = 1) ∪ (univ.filter fun v => c v = 2) from
      filter_or _ _ _, card_union_of_disjoint (disjoint_filter.2 fun v _ h h' => by omega)]
    omega
  have hf03 : ∀ v, ((N v).filter fun u => c u = 0 ∨ c u = 3) = N v ∩ A0 ∪ N v ∩ A3 := by
    intro v; ext u; simp [A0, A3, and_or_left]
  have hf12 : ∀ v, ((N v).filter fun u => c u = 1 ∨ c u = 2) = N v ∩ A12 := by
    intro v; ext u; simp [A12]
  have hdisj : ∀ v, Disjoint (N v ∩ A0) (N v ∩ A3) := fun v =>
    disjoint_of_subset_left inter_subset_right
      (disjoint_of_subset_right inter_subset_right (disjoint_filter.2 fun v _ h h' => by omega))
  -- pointwise decomposition of `Lside`
  have hpt : ∀ v, Lside N c v = (if c v = 0 then 1 else 0) +
      (if c v = 1 ∨ c v = 2 then ((N v ∩ A0).card + (N v ∩ A3).card : ℤ) - 1 else 0) +
      (if c v = 3 then 1 - ((N v ∩ A12).card : ℤ) else 0) := by
    intro v
    unfold Lside
    rw [hf03, hf12, card_union_of_disjoint (hdisj v)]
    split_ifs <;> omega
  simp only [hpt, sum_add_distrib]
  rw [← sum_filter, ← sum_filter, ← sum_filter]
  -- double counting
  have E0 : ∑ v ∈ A12, (N v ∩ A0).card = 2 * m := by
    rw [sum_card_inter_comm N hsymm]
    rw [sum_congr rfl fun v hv => (show (N v ∩ A12).card = 2 by
      rw [← hcard v]; congr 1
      refine inter_eq_left.2 fun u hu => ?_
      simp only [A0, mem_filter, mem_univ, true_and] at hv
      have := hstep v u hu; have := hc0 u
      simp only [A12, mem_filter, mem_univ, true_and]
      omega)]
    simp [hA0, mul_comm]
  have E3 : ∑ v ∈ A12, (N v ∩ A3).card = ∑ v ∈ A3, (N v ∩ A12).card :=
    sum_card_inter_comm N hsymm A12 A3
  have hE0 : ∑ v ∈ A12, ((N v ∩ A0).card : ℤ) = 2 * m := by exact_mod_cast E0
  have hE3 : ∑ v ∈ A12, ((N v ∩ A3).card : ℤ) = ∑ v ∈ A3, ((N v ∩ A12).card : ℤ) := by
    exact_mod_cast E3
  rw [sum_sub_distrib, sum_sub_distrib, sum_add_distrib, hE0, hE3]
  simp only [sum_const, A0, A3, A12] at hA0 hA3 hA12 ⊢
  rw [hA0, hA3, hA12]
  ring

end Local

/-! ## Corner bounds and certificates -/

/-- `CornerBound c`: in every corner, the sum of `t v - L_x(v) - L_y(v)` over the 16 corner
cells is at least `-c`. Here a corner is given abstractly: a 2-regular symmetric graph on a
finite type, with corner coordinates `X, Y ≥ 0` (injective, every cell of `[0,3]²` is hit), every
edge a knight vector in these coordinates, and a turn predicate that holds unless the two moves
are opposite. -/
def CornerBound (c : ℤ) : Prop :=
  ∀ (α : Type) [Fintype α] [DecidableEq α] (N : α → Finset α) (X Y : α → ℤ)
    (turn : α → Prop) [DecidablePred turn],
    (∀ v, (N v).card = 2) → (∀ v u, u ∈ N v → v ∈ N u) →
    (∀ v, ∀ u ∈ N v, IsKnightVec (X u - X v, Y u - Y v)) →
    (∀ v, 0 ≤ X v) → (∀ v, 0 ≤ Y v) →
    (∀ u w, X u = X w → Y u = Y w → u = w) →
    (∀ x y : ℤ, 0 ≤ x → x < 4 → 0 ≤ y → y < 4 → ∃ v, X v = x ∧ Y v = y) →
    (∀ v, ¬ turn v → ∃ u ∈ N v, ∃ w ∈ N v,
      X u - X v = -(X w - X v) ∧ Y u - Y v = -(Y w - Y v)) →
    -c ≤ ∑ v ∈ univ.filter (fun v => X v < 4 ∧ Y v < 4),
      ((if turn v then 1 else 0) - Lside N X v - Lside N Y v)

/-- The eight knight vectors. -/
def kvList : List (ℤ × ℤ) :=
  [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

lemma IsKnightVec.mem_kvList {d : ℤ × ℤ} (h : IsKnightVec d) : d ∈ kvList := by
  have := h.mem
  simp only [mem_insert, mem_singleton] at this
  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- A corner certificate: `alpha` lists the numbers `α(x, y)` at index `4 * y + x`; `beta` lists
edges `(u, w, β)`, oriented from `u` to `w`. -/
structure CornerCert where
  /-- `alpha[4 * y + x] = α(x, y)`. -/
  alpha : List ℤ
  /-- Entries `(u, w, β)`: the edge `u -- w` has the number `β`, counted `+β` at `u`. -/
  beta : List ((ℤ × ℤ) × (ℤ × ℤ) × ℤ)

namespace CornerCert

variable (C : CornerCert)

/-- `α(x, y)`. -/
def alphaAt (x y : ℤ) : ℤ := C.alpha.getD (4 * y + x).toNat 0

/-- The sum of the numbers `α(x, y)` over the corner. -/
def total : ℤ := ∑ p ∈ (Icc (0 : ℤ) 3 ×ˢ Icc (0 : ℤ) 3), C.alphaAt p.1 p.2

/-- The number `β` listed for the oriented pair `(p, q)` (0 if it is not listed). -/
def betaAt (p q : ℤ × ℤ) : ℤ := (C.beta.map fun e => if e.1 = p ∧ e.2.1 = q then e.2.2 else 0).sum

/-- The signed contribution of the edge `p -- q` at its endpoint `p`. -/
def G (p q : ℤ × ℤ) : ℤ := C.betaAt p q - C.betaAt q p

/-- A point of the corner square `[0, 3]²`. -/
def InBox (p : ℤ × ℤ) : Prop := 0 ≤ p.1 ∧ p.1 < 4 ∧ 0 ≤ p.2 ∧ p.2 < 4

instance (p : ℤ × ℤ) : Decidable (InBox p) := by unfold InBox; infer_instance

/-- The local value `t - L_x - L_y` at the cell `(x, y)` with moves `a` and `b`. -/
def rloc (x y : ℤ) (a b : ℤ × ℤ) : ℤ :=
  (if a = -b then 0 else 1) - Lloc x (x + a.1) (x + b.1) - Lloc y (y + a.2) (y + b.2)

/-- The certificate is valid: every listed edge lies in the corner square, and the local
inequality `r(v) ≥ α(v) + D(v)` holds for every cell and every pair of distinct legal moves. -/
def Valid : Prop :=
  (∀ e ∈ C.beta, InBox e.1 ∧ InBox e.2.1) ∧
  ∀ x ∈ ([0, 1, 2, 3] : List ℤ), ∀ y ∈ ([0, 1, 2, 3] : List ℤ), ∀ a ∈ kvList, ∀ b ∈ kvList,
    a ≠ b → 0 ≤ x + a.1 → 0 ≤ y + a.2 → 0 ≤ x + b.1 → 0 ≤ y + b.2 →
    C.alphaAt x y + C.G (x, y) (x + a.1, y + a.2) + C.G (x, y) (x + b.1, y + b.2) ≤
      rloc x y a b

instance : Decidable C.Valid := by unfold Valid; infer_instance

lemma G_antisymm (p q : ℤ × ℤ) : C.G q p = - C.G p q := by unfold G; ring

lemma betaAt_eq_zero (hC : ∀ e ∈ C.beta, InBox e.1 ∧ InBox e.2.1) {p q : ℤ × ℤ}
    (h : ¬ (InBox p ∧ InBox q)) : C.betaAt p q = 0 := by
  unfold betaAt
  refine List.sum_eq_zero fun z hz => ?_
  obtain ⟨e, he, rfl⟩ := List.mem_map.1 hz
  rw [ite_eq_right_iff]
  rintro ⟨rfl, rfl⟩
  exact absurd (hC e he) h

lemma G_eq_zero (hC : ∀ e ∈ C.beta, InBox e.1 ∧ InBox e.2.1) {p q : ℤ × ℤ}
    (h : ¬ (InBox p ∧ InBox q)) : C.G p q = 0 := by
  unfold G
  rw [C.betaAt_eq_zero hC h, C.betaAt_eq_zero hC (by tauto)]
  ring

lemma mem_four {x : ℤ} (h0 : 0 ≤ x) (h4 : x < 4) : x ∈ ([0, 1, 2, 3] : List ℤ) := by
  interval_cases x <;> decide

/-- **Corner lemma from a certificate.** A valid certificate gives `CornerBound (-Σ α)`. -/
theorem cornerBound (hC : C.Valid) : CornerBound (-C.total) := by
  intro α _ _ N X Y turn _ hcard hsymm hknight hX0 hY0 hinj hsurj hturn
  rw [neg_neg]
  set S := univ.filter (fun v => X v < 4 ∧ Y v < 4)
  let pos : α → ℤ × ℤ := fun v => (X v, Y v)
  -- the local inequality at every corner cell
  have hloc : ∀ v ∈ S, C.alphaAt (X v) (Y v) + ∑ u ∈ N v, C.G (pos v) (pos u) ≤
      (if turn v then 1 else 0) - Lside N X v - Lside N Y v := by
    intro v hv
    simp only [S, mem_filter, mem_univ, true_and] at hv
    obtain ⟨u, w, huw, h⟩ := card_eq_two.1 (hcard v)
    have hku := hknight v u (by rw [h]; simp)
    have hkw := hknight v w (by rw [h]; simp)
    have hk1 := hku.bounds
    have hk2 := hkw.bounds
    simp only at hk1 hk2
    set a : ℤ × ℤ := (X u - X v, Y u - Y v) with ha
    set b : ℤ × ℤ := (X w - X v, Y w - Y v) with hb
    have hab : a ≠ b := by
      intro e
      simp only [ha, hb, Prod.ext_iff] at e
      exact huw (hinj u w (by omega) (by omega))
    have key := hC.2 (X v) (mem_four (hX0 v) hv.1) (Y v) (mem_four (hY0 v) hv.2) a
      hku.mem_kvList b hkw.mem_kvList hab
      (by have := hX0 u; simp only [ha]; omega) (by have := hY0 u; simp only [ha]; omega)
      (by have := hX0 w; simp only [hb]; omega) (by have := hY0 w; simp only [hb]; omega)
    have e1 : (X v + a.1, Y v + a.2) = pos u := by simp only [ha, pos]; ext <;> simp
    have e2 : (X v + b.1, Y v + b.2) = pos w := by simp only [hb, pos]; ext <;> simp
    have e3 : X v + a.1 = X u := by simp only [ha]; ring
    have e4 : X v + b.1 = X w := by simp only [hb]; ring
    have e5 : Y v + a.2 = Y u := by simp only [ha]; ring
    have e6 : Y v + b.2 = Y w := by simp only [hb]; ring
    rw [e1, e2] at key
    unfold rloc at key
    rw [e3, e4, e5, e6] at key
    rw [h, sum_pair huw, Lside_pair huw h, Lside_pair huw h]
    have ht : (if a = -b then (0 : ℤ) else 1) ≤ if turn v then 1 else 0 := by
      by_cases hv' : turn v
      · simp only [hv', ite_true]; split_ifs <;> norm_num
      · simp only [hv', ite_false]
        obtain ⟨u', hu', w', hw', h1, h2⟩ := hturn v hv'
        rw [h] at hu' hw'
        simp only [mem_insert, mem_singleton] at hu' hw'
        have hopp : a = -b := by
          simp only [Prod.ext_iff, Prod.fst_neg, Prod.snd_neg, ha, hb]
          rcases hu' with rfl | rfl <;> rcases hw' with rfl | rfl <;> constructor <;> omega
        simp only [hopp, ite_true, le_refl]
    simp only [pos] at key ⊢
    linarith
  -- the edge terms cancel
  have hD : ∑ v ∈ S, ∑ u ∈ N v, C.G (pos v) (pos u) = 0 := by
    have hrw : ∀ v ∈ S, ∑ u ∈ N v, C.G (pos v) (pos u) =
        ∑ u ∈ S, if u ∈ N v then C.G (pos v) (pos u) else 0 := by
      intro v hv
      rw [← sum_filter]
      refine (sum_subset (fun u hu => (mem_filter.1 hu).2) fun u hu hu' => ?_).symm
      have huS : u ∉ S := fun h' => hu' (mem_filter.2 ⟨h', hu⟩)
      refine C.G_eq_zero hC.1 fun ⟨_, hq⟩ => huS ?_
      simp only [S, mem_filter, mem_univ, true_and]
      exact ⟨hq.2.1, hq.2.2.2⟩
    rw [sum_congr rfl hrw]
    have hswap := sum_comm (s := S) (t := S)
      (f := fun v u => if u ∈ N v then C.G (pos v) (pos u) else 0)
    have hneg : ∑ u ∈ S, ∑ v ∈ S, (if u ∈ N v then C.G (pos v) (pos u) else 0) =
        - ∑ u ∈ S, ∑ v ∈ S, (if v ∈ N u then C.G (pos u) (pos v) else 0) := by
      rw [← sum_neg_distrib]
      refine sum_congr rfl fun u _ => ?_
      rw [← sum_neg_distrib]
      refine sum_congr rfl fun v _ => ?_
      have : u ∈ N v ↔ v ∈ N u := ⟨hsymm v u, hsymm u v⟩
      by_cases h' : v ∈ N u
      · simp only [this.2 h', h', ite_true]; exact C.G_antisymm _ _
      · simp only [h', ite_false, neg_zero, show u ∉ N v from fun h'' => h' (this.1 h'')]
    linarith
  -- the sum of `α` over the corner
  have hA : ∑ v ∈ S, C.alphaAt (X v) (Y v) = C.total := by
    unfold total
    refine sum_nbij pos (fun v hv => ?_) (fun v _ w _ e => ?_) (fun p hp => ?_) fun v _ => rfl
    · simp only [S, mem_filter, mem_univ, true_and] at hv
      simp only [mem_product, mem_Icc, pos]
      have := hX0 v; have := hY0 v
      omega
    · simp only [pos, Prod.ext_iff] at e
      exact hinj v w e.1 e.2
    · simp only [coe_product, coe_Icc, Set.mem_prod, Set.mem_Icc] at hp
      obtain ⟨v, h1, h2⟩ := hsurj p.1 p.2 (by omega) (by omega) (by omega) (by omega)
      refine ⟨v, ?_, ?_⟩
      · simp only [S, coe_filter, mem_univ, true_and, Set.mem_ofPred_eq]
        omega
      · simp only [pos, h1, h2]
  have hsum := sum_le_sum hloc
  rw [sum_add_distrib, hD, add_zero, hA] at hsum
  exact hsum

end CornerCert

/-- The corner certificate of Lemma 3 (corner lemma) of `writeup/turns/main.tex`, Tables 1 and 2,
in corner coordinates `(x, y)`. -/
def cert28 : CornerCert where
  alpha := [-1, 0, 0, -1,
            0, 1, 0, -1,
            0, 0, 0, -1,
            -1, -1, -1, -1]
  beta := [((0, 1), (1, 3), -1), ((0, 2), (2, 3), -1), ((0, 3), (1, 1), 1),
           ((1, 0), (3, 1), -1), ((1, 1), (3, 0), -1), ((1, 2), (3, 3), -1),
           ((2, 0), (3, 2), -1), ((2, 1), (3, 3), -1), ((2, 2), (3, 0), -1)]

lemma cert28_valid : cert28.Valid := by decide +kernel

lemma cert28_total : cert28.total = -7 := by decide +kernel

/-- **Corner lemma** (Lemma 3 of `main.tex`): in every corner the sum of `r(v)` is at least `-7`. -/
theorem cornerBound_seven : CornerBound 7 := by
  have := cert28.cornerBound cert28_valid
  rwa [cert28_total, neg_neg] at this

end KT
