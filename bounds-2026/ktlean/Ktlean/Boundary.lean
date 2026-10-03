import Ktlean.Rotate
import Ktlean.Square

/-!
# Crossings among the edges at one side of the board

Let every cell `(0, y)` of column 0 have degree two, with all edges inside the board
`[0, n-1]²`. The edges at `(0, y)` go to two of the four cells `(0, y) + w`, `w ∈ C0`. For two
consecutive rows, a finite check over the 36 choices gives

  `#crossings between the edges at (0, y) and at (0, y + 1) ≥ 1 + down(y + 1) - down(y)`,

where `down(y)` is the number of edges at `(0, y)` that go down. At row `0` no edge goes down; at
row `n - 1` both edges go down. Telescoping gives at least `n + 1` crossing pairs of edges at
column 0 (`2(n + 1)` ordered pairs). No acyclicity condition is necessary: this holds for every
family with degree two on column 0, for example every 2-factor of the knight's graph.
-/

open Finset

namespace KT

/-- The four knight vectors that point into the board from column 0. -/
def C0 : Finset Pt := {(1, 2), (2, 1), (2, -1), (1, -2)}

/-- The crossings between the edges from `(0, 0)` to `A` and from `(0, 1)` to `(0, 1) + B`. -/
def c2 (A B : Finset Pt) : ℕ :=
  ∑ w ∈ A, ∑ w' ∈ B, if ProperCross 0 w (0, 1) ((0, 1) + w') then 1 else 0

/-- The number of edges that go down. -/
def downCount (A : Finset Pt) : ℕ := (A.filter fun w => w.2 < 0).card

lemma c2_cert : ∀ A ∈ C0.powerset, ∀ B ∈ C0.powerset, A.card = 2 → B.card = 2 →
    1 + downCount B ≤ c2 A B + downCount A := by
  decide +kernel

lemma knight_neg : ∀ w ∈ knightVecs, -w ∈ knightVecs := by decide

lemma knight_mem_C0 : ∀ w ∈ knightVecs, 0 ≤ w.1 → w ∈ C0 := by decide

lemma C0_snd_ne : ∀ w ∈ C0, w.2 ≠ 0 := by decide

lemma knight_fst_ne : ∀ w ∈ knightVecs, w.1 ≠ 0 := by decide

section Family

variable {ι : Type*} [Fintype ι] [DecidableEq ι] (a d : ι → Pt)

/-- The edges at the point `v`. -/
def atCell (v : Pt) : Finset ι := univ.filter fun i => a i = v ∨ a i + d i = v

/-- The other endpoint of an edge at `v`. -/
def oth (v : Pt) (i : ι) : Pt := if a i = v then a i + d i else a i

/-- The neighbours of `v`, relative to `v`. -/
def nbr (v : Pt) : Finset Pt := (atCell a d v).image fun i => oth a d v i - v

/-- The crossing pairs between the edges at `(0, y)` and the edges at `(0, y + 1)`. -/
def rowPairs (y : ℤ) : Finset (ι × ι) :=
  ((atCell a d (0, y)) ×ˢ (atCell a d (0, y + 1))).filter fun p =>
    ProperCross (a p.1) (a p.1 + d p.1) (a p.2) (a p.2 + d p.2)

/-- The edges at column 0 that cross properly (ordered pairs). -/
def sidePairs : Finset (ι × ι) :=
  (crossPairs a d).filter fun p => ((a p.1).1 = 0 ∨ (a p.1 + d p.1).1 = 0) ∧
    ((a p.2).1 = 0 ∨ (a p.2 + d p.2).1 = 0)

variable {a d}

omit [DecidableEq ι] in
lemma mem_atCell {v : Pt} {i : ι} : i ∈ atCell a d v ↔ a i = v ∨ a i + d i = v := by
  simp [atCell]

omit [Fintype ι] [DecidableEq ι] in
lemma d_ne_zero (hd : ∀ i, d i ∈ knightVecs) (i : ι) : d i ≠ 0 := fun h => by
  have := hd i; rw [h] at this; simp [knightVecs, Prod.ext_iff] at this

omit [DecidableEq ι] in
lemma card_atCell (hd : ∀ i, d i ∈ knightVecs) (v : Pt) : (atCell a d v).card = deg a d v := by
  classical
  unfold atCell deg
  rw [filter_or, card_union_of_disjoint]
  rw [disjoint_filter]
  intro i _ h1 h2
  apply d_ne_zero hd i
  have : a i + d i = a i + 0 := by rw [add_zero, h2, h1]
  exact add_left_cancel this

omit [DecidableEq ι] in
lemma oth_sub_mem (hd : ∀ i, d i ∈ knightVecs) {v : Pt} {i : ι} (hi : i ∈ atCell a d v) :
    oth a d v i - v ∈ knightVecs := by
  rw [mem_atCell] at hi
  unfold oth
  split_ifs with h
  · rw [h, add_sub_cancel_left]; exact hd i
  · rw [← hi.resolve_left h, sub_add_cancel_left]; exact knight_neg _ (hd i)

omit [DecidableEq ι] in
lemma oth_injOn (hdist : DistinctEdges a d) (v : Pt) :
    Set.InjOn (oth a d v) (atCell a d v) := by
  intro i hi j hj h
  have hi' := mem_atCell.1 (mem_coe.1 hi)
  have hj' := mem_atCell.1 (mem_coe.1 hj)
  by_contra hne
  apply hdist i j hne
  unfold oth at h
  split_ifs at h with h1 h2 h2
  · exact Or.inl ⟨h1.trans h2.symm, h⟩
  · exact Or.inr ⟨h1.trans (hj'.resolve_left h2).symm, h⟩
  · exact Or.inr ⟨h, (hi'.resolve_left h1).trans h2.symm⟩
  · exact Or.inl ⟨h, (hi'.resolve_left h1).trans (hj'.resolve_left h2).symm⟩

omit [DecidableEq ι] in
lemma card_nbr (hd : ∀ i, d i ∈ knightVecs) (hdist : DistinctEdges a d) (v : Pt) :
    (nbr a d v).card = deg a d v := by
  classical
  rw [nbr, card_image_of_injOn, card_atCell hd]
  intro i hi j hj h
  exact oth_injOn hdist v hi hj (sub_left_injective h)

omit [DecidableEq ι] in
/-- The column-0 endpoint of an edge is unique. -/
lemma atCell_col0_unique (hd : ∀ i, d i ∈ knightVecs) {i : ι} {y y' : ℤ}
    (h : i ∈ atCell a d (0, y)) (h' : i ∈ atCell a d (0, y')) : y = y' := by
  have hk := knight_fst_ne _ (hd i)
  rw [mem_atCell] at h h'
  rcases h with h | h <;> rcases h' with h' | h' <;>
    simp only [Prod.ext_iff, Prod.fst_add, Prod.snd_add] at h h' <;> omega

omit [DecidableEq ι] in
lemma seg_iff {v : Pt} {i : ι} (hi : i ∈ atCell a d v) (X Y : Pt) :
    ProperCross (a i) (a i + d i) X Y ↔ ProperCross v (oth a d v i) X Y := by
  rw [mem_atCell] at hi
  unfold oth
  split_ifs with h
  · rw [h]
  · rw [← hi.resolve_left h, properCross_swap]

omit [DecidableEq ι] in
lemma card_rowPairs (hdist : DistinctEdges a d) (y : ℤ) :
    (rowPairs a d y).card = c2 (nbr a d (0, y)) (nbr a d (0, y + 1)) := by
  have inj : ∀ v : Pt, Set.InjOn (fun i => oth a d v i - v) (atCell a d v) :=
    fun v i hi j hj h => oth_injOn hdist v hi hj (sub_left_injective h)
  rw [rowPairs, card_filter, sum_product, c2, nbr, sum_image (inj _)]
  refine sum_congr rfl fun i hi => ?_
  rw [nbr, sum_image (inj _)]
  refine sum_congr rfl fun j hj => ?_
  have e : ProperCross (a i) (a i + d i) (a j) (a j + d j) ↔
      ProperCross 0 (oth a d (0, y) i - (0, y)) (0, 1)
        ((0, 1) + (oth a d (0, y + 1) j - (0, y + 1))) := by
    rw [seg_iff hi, properCross_comm, seg_iff hj, properCross_comm,
      ← properCross_sub _ _ _ _ (0, y)]
    have e1 : ((0 : ℤ), y) - (0, y) = 0 := sub_self _
    have e2 : ((0 : ℤ), y + 1) - (0, y) = (0, 1) := by ext <;> simp
    have e3 : oth a d (0, y + 1) j - (0, y) =
        (0, 1) + (oth a d (0, y + 1) j - (0, y + 1)) := by
      ext <;> simp only [Prod.fst_sub, Prod.snd_sub, Prod.fst_add, Prod.snd_add] <;> ring
    rw [e1, e2, e3]
  simp only [e]

/-- **At least `n + 1` crossings at one side.** If every cell of column 0 of the board
`[0, n-1]²` has degree two and all edges lie in the board, then the edges at column 0 have at
least `n + 1` properly crossing pairs (`2(n + 1)` ordered pairs). -/
theorem side_pairs (hd : ∀ i, d i ∈ knightVecs) (hdist : DistinctEdges a d)
    (n : ℕ) (hn : 1 ≤ n) (hboard : ∀ i, InBoard n (a i) ∧ InBoard n (a i + d i))
    (hdeg : ∀ y : ℤ, 0 ≤ y → y < n → deg a d (0, y) = 2) :
    2 * (n + 1) ≤ (sidePairs a d).card := by
  -- the neighbour sets
  have hnbr : ∀ y : ℤ, 0 ≤ y → y < n → nbr a d (0, y) ∈ C0.powerset ∧
      (nbr a d (0, y)).card = 2 := by
    intro y h0 h1
    refine ⟨mem_powerset.2 ?_, by rw [card_nbr hd hdist, hdeg y h0 h1]⟩
    intro w hw
    obtain ⟨i, hi, rfl⟩ := mem_image.1 hw
    apply knight_mem_C0 _ (oth_sub_mem hd hi)
    have := hboard i
    unfold oth InBoard at *
    split_ifs <;> simp only [Prod.fst_sub] <;> omega
  have hdown0 : downCount (nbr a d (0, 0)) = 0 := by
    rw [downCount, card_eq_zero, filter_eq_empty_iff]
    intro w hw
    obtain ⟨i, hi, rfl⟩ := mem_image.1 hw
    have := hboard i
    unfold oth InBoard at *
    split_ifs <;> simp only [Prod.snd_sub] <;> omega
  have hdownN : downCount (nbr a d (0, (n : ℤ) - 1)) = 2 := by
    rw [downCount, filter_true_of_mem, (hnbr _ (by omega) (by omega)).2]
    intro w hw
    have hne := C0_snd_ne w (mem_powerset.1 (hnbr _ (by omega) (by omega)).1 hw)
    obtain ⟨i, hi, rfl⟩ := mem_image.1 hw
    have := hboard i
    unfold oth InBoard at *
    split_ifs at hne ⊢ <;> simp only [Prod.snd_sub] at hne ⊢ <;> omega
  -- telescoping
  have tele : ∀ m : ℕ, m + 1 ≤ n → m + downCount (nbr a d (0, (m : ℤ))) ≤
      ∑ y ∈ range m, (rowPairs a d y).card := by
    intro m
    induction m with
    | zero => intro _; simp [hdown0]
    | succ m ih =>
      intro hm
      have h1 := ih (by omega)
      have hA := hnbr m (by omega) (by omega)
      have hB := hnbr (m + 1) (by omega) (by omega)
      have hc := c2_cert _ hA.1 _ hB.1 hA.2 hB.2
      rw [sum_range_succ, card_rowPairs hdist]
      push_cast at hc ⊢
      omega
  have hS := tele (n - 1) (by omega)
  rw [show ((n - 1 : ℕ) : ℤ) = (n : ℤ) - 1 by omega, hdownN] at hS
  -- the forward pairs and their reverses are disjoint subsets of `sidePairs`
  set S := (range (n - 1)).biUnion fun y => rowPairs a d (y : ℤ)
  have hmem : ∀ p ∈ S, ∃ y : ℤ, p.1 ∈ atCell a d (0, y) ∧ p.2 ∈ atCell a d (0, y + 1) ∧
      ProperCross (a p.1) (a p.1 + d p.1) (a p.2) (a p.2 + d p.2) := by
    intro p hp
    obtain ⟨y, -, hy⟩ := mem_biUnion.1 hp
    simp only [rowPairs, mem_filter, mem_product] at hy
    exact ⟨y, hy.1.1, hy.1.2, hy.2⟩
  have hcardS : S.card = ∑ y ∈ range (n - 1), (rowPairs a d y).card := by
    rw [card_biUnion]
    intro y _ y' _ hyy'
    rw [Function.onFun, disjoint_left]
    intro p h1 h2
    simp only [rowPairs, mem_filter, mem_product] at h1 h2
    have := atCell_col0_unique hd h1.1.1 h2.1.1
    exact hyy' (by exact_mod_cast this)
  have col0 : ∀ {i : ι} {y : ℤ}, i ∈ atCell a d (0, y) → (a i).1 = 0 ∨ (a i + d i).1 = 0 := by
    intro i y h
    rw [mem_atCell] at h
    rcases h with h | h <;> rw [h] <;> simp
  have hsub1 : S ⊆ sidePairs a d := by
    intro p hp
    obtain ⟨y, h1, h2, hc⟩ := hmem p hp
    have hne : p.1 ≠ p.2 := fun h => by
      rw [h] at h1; have := atCell_col0_unique hd h1 h2; omega
    simp only [sidePairs, crossPairs, mem_filter, mem_univ, true_and]
    exact ⟨⟨hne, hc⟩, col0 h1, col0 h2⟩
  have hsub2 : S.image Prod.swap ⊆ sidePairs a d := by
    intro p hp
    obtain ⟨q, hq, rfl⟩ := mem_image.1 hp
    have := hsub1 hq
    simp only [sidePairs, crossPairs, mem_filter, mem_univ, true_and, Prod.fst_swap,
      Prod.snd_swap] at this ⊢
    exact ⟨⟨this.1.1.symm, (properCross_comm _ _ _ _).1 this.1.2⟩, this.2.2, this.2.1⟩
  have hdisj : Disjoint S (S.image Prod.swap) := by
    rw [disjoint_left]
    intro p h1 h2
    obtain ⟨q, hq, rfl⟩ := mem_image.1 h2
    obtain ⟨y, a1, a2, -⟩ := hmem _ h1
    obtain ⟨y', b1, b2, -⟩ := hmem _ hq
    have e1 := atCell_col0_unique hd a1 b2
    have e2 := atCell_col0_unique hd a2 b1
    omega
  have := card_le_card (union_subset hsub1 hsub2)
  rw [card_union_of_disjoint hdisj, card_image_of_injective _ Prod.swap_injective] at this
  omega

end Family

end KT
