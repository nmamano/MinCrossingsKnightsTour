import Ktlean.Assembly
import Ktlean.EndTest

/-!
# The combined count (FINDINGS.md 10.3-10.4, with the boundary count of `Boundary.lean`)

For a family of `n²` distinct knight edges in the board `[0, n-1]²` (`n = 2h`), with degree two
at every cell (for example the moves of a closed tour), let `Y` be the number of ordered pairs
of edges that cross properly (`Y = 2X`), and let `d` be the number of rows that fail the
endpoint test of FINDINGS 10.4 (`GoodRow`) in the scan ranges `[12, h-4]` and `[h+2, n-14]`
of the four sides. Then

  `10 n ≤ Y + d + 130`, that is `X ≥ 5n - 65 - d/2`.

With the per-row stability hypothesis `d ≤ X - 4n + 2 + C` (FINDINGS 10.4 and TILE_INPUTS
section 9 give `C = 1131`), this gives `3X ≥ 14n - C - 132`, so `X ≥ 14n/3 - 421`.
-/

open Finset

namespace KT

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- The exceptional pair `(0, y)--(2, y+1)`, `(0, y+1)--(2, y)` is present. -/
def ExcPair (b e : ι → Pt) (y : ℤ) : Prop :=
  ∃ i j, canon Prod.snd (b i - (0, y)) (e i) = ((0, 0), (2, 1)) ∧
    canon Prod.snd (b j - (0, y)) (e j) = ((2, 0), (-2, 1))

instance (b e : ι → Pt) (y : ℤ) : Decidable (ExcPair b e y) := by
  unfold ExcPair; infer_instance

/-- Row `y` of side `k` passes the endpoint test of FINDINGS.md 10.4: in frame `k`, the sum `F`
of the coefficients `Fcoef` of the edges (relative to row `y`) is `2` mod 3, and the exceptional
pair is not present. -/
def GoodRow (n : ℤ) (k : ℕ) (y : ℤ) : Prop :=
  (3 : ℤ) ∣ (∑ i, Fcoef (canon Prod.snd ((rotPt n)^[k] (a i) - (0, y)) (rotL^[k] (d i)))) - 2 ∧
    ¬ ExcPair (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) y

instance (n : ℤ) (k : ℕ) (y : ℤ) : Decidable (GoodRow a d n k y) := by
  unfold GoodRow; infer_instance

/-- The non-critical rows of the four sides in the two scan ranges (`n = 2h`). -/
def badRows (h : ℕ) : Finset (ℕ × ℤ) :=
  ((range 4) ×ˢ (Icc 12 ((h : ℤ) - 4) ∪ Icc ((h : ℤ) + 2) (2 * h - 14))).filter
    fun p => ¬ GoodRow a d (2 * h) p.1 p.2

/-- The crossing pairs at side `k`. -/
abbrev sideSet [DecidableEq ι] (n : ℤ) (k : ℕ) : Finset (ι × ι) :=
  sidePairs (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i))

/-- The corners `(k, R)`: corner `k` (the bottom-left corner of frame `k`), radius `R`. -/
def corners (h : ℕ) : Finset (ℕ × ℕ) := range 4 ×ˢ Icc 12 (h - 4)

/-- Corner `(k, R)` is retained if row `R` of side `k` and row `n - 2 - R` of side `k + 3`
(the bottom side of frame `k`) are critical. -/
def GoodCorner (n : ℤ) (c : ℕ × ℕ) : Prop :=
  GoodRow a d n c.1 c.2 ∧ GoodRow a d n ((c.1 + 3) % 4) (n - 2 - c.2)

instance (n : ℤ) : DecidablePred (GoodCorner a d n) := fun c => by
  unfold GoodCorner; infer_instance

/-- The retained corners. -/
def retained (h : ℕ) : Finset (ℕ × ℕ) := (corners h).filter (GoodCorner a d (2 * h))

/-- The unit squares of the corner path `γ_R` of frame `k`, in the original frame. -/
def cornerSq (n : ℤ) (c : ℕ × ℕ) : Finset Pt :=
  (boardSq n).filter fun s => (rotSq n)^[c.1] s ∈ gammaSq c.2

variable {a d}

lemma GoodRow.mod {n : ℤ} {k : ℕ} {y : ℤ} (hg : GoodRow a d n (k % 4) y) :
    GoodRow a d n k y := by
  unfold GoodRow at *
  simpa only [rotPt_iter_mod, rotL_iter_mod] using hg

/-- One quarter turn moves column `0` of frame `k` to row `0` of frame `k + 1`. -/
lemma rot_succ_snd (n : ℤ) (k : ℕ) (p : Pt) :
    ((rotPt n)^[k + 1] p).2 = ((rotPt n)^[k] p).1 := by
  rw [Function.iterate_succ_apply']; rfl

/-- Two quarter turns move column `0` of frame `k` to column `n - 1` of frame `k + 2`. -/
lemma rot_add_two_fst (n : ℤ) (k : ℕ) (p : Pt) :
    ((rotPt n)^[k + 2] p).1 = n - 1 - ((rotPt n)^[k] p).1 := by
  rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
  simp [rotPt]

/-- An edge at column 0 of a frame: its endpoints. -/
def AtCol0 (b e : ι → Pt) (i : ι) : Prop := (b i).1 = 0 ∨ (b i + e i).1 = 0

instance (b e : ι → Pt) : DecidablePred (AtCol0 b e) := fun i => by
  unfold AtCol0; infer_instance

/-- If every edge of `S` has an endpoint in `C` (a set of board cells of degree two), then
`#S ≤ 2 #C`. -/
lemma card_le_of_endpoint_mem (hd : ∀ i, d i ∈ knightVecs) (C : Finset Pt)
    (hC : ∀ v ∈ C, deg a d v = 2) (S : Finset ι)
    (hS : ∀ i ∈ S, a i ∈ C ∨ a i + d i ∈ C) : S.card ≤ 2 * C.card := by
  classical
  have hsub : S ⊆ C.biUnion fun v => atCell a d v := by
    intro i hi
    rcases hS i hi with h | h
    · exact mem_biUnion.2 ⟨_, h, mem_atCell.2 (Or.inl rfl)⟩
    · exact mem_biUnion.2 ⟨_, h, mem_atCell.2 (Or.inr rfl)⟩
  calc S.card ≤ (C.biUnion fun v => atCell a d v).card := card_le_card hsub
    _ ≤ ∑ v ∈ C, (atCell a d v).card := card_biUnion_le
    _ = ∑ _v ∈ C, 2 := sum_congr rfl fun v hv => by rw [card_atCell hd, hC v hv]
    _ = 2 * C.card := by rw [sum_const, smul_eq_mul, mul_comm]

/-- At most six edges meet both column 0 and row 0. -/
lemma card_corner_edges (hd : ∀ i, d i ∈ knightVecs) (n : ℤ) (hn : 3 ≤ n)
    (hboard : ∀ i, InBoard n (a i) ∧ InBoard n (a i + d i))
    (hdeg : ∀ v, InBoard n v → deg a d v = 2) :
    (univ.filter fun i => AtCol0 a d i ∧ ((a i).2 = 0 ∨ (a i + d i).2 = 0)).card ≤ 6 := by
  have h := card_le_of_endpoint_mem hd {(0, 0), (0, 1), (0, 2)} (by
    intro v hv; apply hdeg
    simp only [mem_insert, mem_singleton] at hv
    rcases hv with rfl | rfl | rfl <;> (unfold InBoard; omega))
    (univ.filter fun i => AtCol0 a d i ∧ ((a i).2 = 0 ∨ (a i + d i).2 = 0)) (by
    intro i hi
    have hi' := (mem_filter.1 hi).2
    unfold AtCol0 at hi'
    have hb := mid_bounds (hd i)
    have := hboard i
    unfold InBoard at this
    simp only [mem_insert, mem_singleton, Prod.ext_iff, Prod.fst_add, Prod.snd_add] at hi' this ⊢
    omega)
  have h3 : ({(0, 0), (0, 1), (0, 2)} : Finset Pt).card = 3 := by decide
  omega

lemma rotPt_iter_add_three (n : ℤ) (k : ℕ) (p : Pt) :
    rotPt n ((rotPt n)^[k + 3] p) = (rotPt n)^[k] p := by
  rw [← Function.iterate_succ_apply' (f := rotPt n), show (k + 3).succ = k + 4 from rfl,
    Function.iterate_add_apply, rotPt_iter_four]

lemma rotL_iter_add_three (k : ℕ) (d : Pt) : rotL (rotL^[k + 3] d) = rotL^[k] d := by
  rw [← Function.iterate_succ_apply' (f := rotL), show (k + 3).succ = k + 4 from rfl,
    Function.iterate_add_apply, rotL_iter_four]

/-- Squares of distinct corner paths are distinct. -/
lemma cornerSq_disjoint {h : ℕ} (hh : 16 ≤ h) {c c' : ℕ × ℕ} (hc : c ∈ corners h)
    (hc' : c' ∈ corners h) (hne : c ≠ c') :
    Disjoint (cornerSq (2 * h) c) (cornerSq (2 * h) c') := by
  obtain ⟨k, R⟩ := c
  obtain ⟨k', R'⟩ := c'
  simp only [corners, mem_product, mem_range, mem_Icc] at hc hc'
  rw [disjoint_left]
  intro s h1 h2
  simp only [cornerSq, mem_filter, mem_gammaSq] at h1 h2
  have hne' : k ≠ k' ∨ R ≠ R' := by
    by_contra hcon; push Not at hcon; exact hne (by rw [hcon.1, hcon.2])
  rcases rotSq_iter_cases (2 * h : ℤ) hc.1 s with ⟨e, h3⟩ | ⟨e, h3⟩ | ⟨e, h3⟩ | ⟨e, h3⟩ <;>
  rcases rotSq_iter_cases (2 * h : ℤ) hc'.1 s with ⟨e', h4⟩ | ⟨e', h4⟩ | ⟨e', h4⟩ | ⟨e', h4⟩ <;>
  rw [h3] at h1 <;> rw [h4] at h2 <;> (try simp only at h1 h2) <;> omega

/-- The frame-`k` position of a corner square: column at least `1`, and column `1` only at the
end squares of the corner paths of frames `k` and `k + 1`. -/
lemma cornerSq_frame {h : ℕ} (hh : 16 ≤ h) {c : ℕ × ℕ} (hc : c ∈ corners h) {s : Pt}
    (hs : s ∈ cornerSq (2 * h) c) {k : ℕ} (hk : k < 4) :
    1 ≤ ((rotSq (2 * h))^[k] s).1 ∧ (((rotSq (2 * h))^[k] s).1 = 1 →
      (c.1 = k ∧ ((rotSq (2 * h))^[k] s).2 = c.2) ∨
      ((c.1 + 3) % 4 = k ∧ ((rotSq (2 * h))^[k] s).2 = 2 * h - 2 - c.2)) := by
  obtain ⟨k', R⟩ := c
  simp only [corners, mem_product, mem_range, mem_Icc] at hc
  simp only [cornerSq, mem_filter, mem_gammaSq] at hs
  rcases rotSq_iter_cases (2 * h : ℤ) hk s with ⟨e, h3⟩ | ⟨e, h3⟩ | ⟨e, h3⟩ | ⟨e, h3⟩ <;>
  rcases rotSq_iter_cases (2 * h : ℤ) hc.1 s with ⟨e', h4⟩ | ⟨e', h4⟩ | ⟨e', h4⟩ | ⟨e', h4⟩ <;>
  rw [h3] <;> rw [h4] at hs <;> (try simp only at hs ⊢) <;> omega

lemma card_corners {h : ℕ} (hh : 16 ≤ h) : (corners h).card + 60 = 4 * h := by
  simp only [corners, card_product, card_range, Nat.card_Icc]
  omega

/-- Each non-retained corner has a non-critical row of its own. -/
lemma corners_le (h : ℕ) :
    (corners h).card ≤ (retained a d h).card + (badRows a d h).card := by
  rw [← card_filter_add_card_filter_not (s := corners h) (GoodCorner a d (2 * h))]
  refine Nat.add_le_add_left ?_ _
  let f : ℕ × ℕ → ℕ × ℤ := fun c =>
    if GoodRow a d (2 * h) c.1 c.2 then ((c.1 + 3) % 4, 2 * h - 2 - c.2) else (c.1, c.2)
  refine card_le_card_of_injOn f (fun c hc => ?_) (fun c hc c' hc' hcc => ?_)
  · simp only [coe_filter, Set.mem_ofPred_eq, corners, mem_product, mem_range, mem_Icc] at hc
    obtain ⟨⟨hk, hR1, hR2⟩, hng⟩ := hc
    unfold GoodCorner at hng
    simp only [badRows, coe_filter, Set.mem_ofPred_eq, mem_product, mem_range, mem_union,
      mem_Icc, f]
    split_ifs with hg
    · exact ⟨⟨Nat.mod_lt _ (by norm_num), Or.inr ⟨by omega, by omega⟩⟩, fun h' => hng ⟨hg, h'⟩⟩
    · exact ⟨⟨hk, Or.inl ⟨by omega, by omega⟩⟩, hg⟩
  · simp only [coe_filter, Set.mem_ofPred_eq, corners, mem_product, mem_range, mem_Icc] at hc hc'
    obtain ⟨k, R⟩ := c
    obtain ⟨k', R'⟩ := c'
    simp only [f] at hcc
    split_ifs at hcc <;> simp only [Prod.mk.injEq] at hcc <;> ext <;> simp only <;> omega

section Standing

variable [DecidableEq ι] {n : ℤ} (hd : ∀ i, d i ∈ knightVecs)
  (hboard : ∀ i, InBoard n (a i) ∧ InBoard n (a i + d i))
  (hdeg : ∀ v, InBoard n v → deg a d v = 2) (hdist : DistinctEdges a d)
include hd hboard hdeg hdist

omit [DecidableEq ι] in
/-- Every frame satisfies the standing hypotheses. -/
lemma frame_ok (k : ℕ) :
    (∀ i, rotL^[k] (d i) ∈ knightVecs) ∧
    (∀ i, InBoard n ((rotPt n)^[k] (a i)) ∧
      InBoard n ((rotPt n)^[k] (a i) + rotL^[k] (d i))) ∧
    (∀ v, InBoard n v → deg (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) v = 2) ∧
    DistinctEdges (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) := by
  refine ⟨fun i => rotL_iter_mem (hd i) k, fun i => ?_, fun v hv => ?_, hdist.iter a d n k⟩
  · rw [← rotPt_iter_add]; exact ⟨(hboard i).1.iter k, (hboard i).2.iter k⟩
  · obtain ⟨u, hu, rfl⟩ := exists_rot_iter hv k
    rw [deg_iter a d n k u, hdeg u hu]

omit hd hboard hdeg hdist in
lemma sideSet_sub (k : ℕ) : sideSet a d n k ⊆ crossPairs a d := by
  intro p hp
  rw [← crossPairs_iter a d n k]
  exact (mem_filter.1 hp).1

lemma sideSet_card (hn : 1 ≤ n) (k : ℕ) : 2 * (n.toNat + 1) ≤ (sideSet a d n k).card := by
  obtain ⟨hdk, hbk, hdegk, hdistk⟩ := frame_ok hd hboard hdeg hdist k
  have := side_pairs hdk hdistk n.toNat (by omega)
    (fun i => by rw [Int.toNat_of_nonneg (by omega)]; exact hbk i)
    (fun y h0 h1 => hdegk _ (by unfold InBoard; simp only; omega))
  exact this

omit hboard hdeg hdist in
lemma sideSet_opp (hn : 4 ≤ n) (k : ℕ) : Disjoint (sideSet a d n k) (sideSet a d n (k + 2)) := by
  rw [disjoint_left]
  intro p h1 h2
  simp only [sidePairs, mem_filter] at h1 h2
  have e1 := h1.2.1
  have e2 := h2.2.1
  simp only [← rotPt_iter_add] at e1 e2
  rw [rot_add_two_fst, rot_add_two_fst] at e2
  have hb := mid_bounds (rotL_iter_mem (hd p.1) k)
  have hadd := rotPt_iter_add n k (a p.1) (d p.1)
  have : ((rotPt n)^[k] (a p.1 + d p.1)).1 = ((rotPt n)^[k] (a p.1)).1 + (rotL^[k] (d p.1)).1 := by
    rw [hadd]; rfl
  omega

lemma sideSet_adj (hn : 3 ≤ n) (k : ℕ) :
    (sideSet a d n k ∩ sideSet a d n (k + 1)).card ≤ 36 := by
  obtain ⟨hdk, hbk, hdegk, hdistk⟩ := frame_ok hd hboard hdeg hdist (k + 1)
  set E := univ.filter fun i => AtCol0 (fun i => (rotPt n)^[k + 1] (a i))
    (fun i => rotL^[k + 1] (d i)) i ∧ (((rotPt n)^[k + 1] (a i)).2 = 0 ∨
      ((rotPt n)^[k + 1] (a i) + rotL^[k + 1] (d i)).2 = 0)
  have hE := card_corner_edges hdk n hn hbk hdegk
  have hsub : sideSet a d n k ∩ sideSet a d n (k + 1) ⊆ E ×ˢ E := by
    intro p hp
    rw [mem_inter] at hp
    simp only [sidePairs, mem_filter] at hp
    simp only [mem_product, E, mem_filter, mem_univ, true_and, AtCol0, ← rotPt_iter_add,
      rot_succ_snd]
    simp only [← rotPt_iter_add] at hp
    exact ⟨⟨hp.2.2.1, hp.1.2.1⟩, ⟨hp.2.2.2, hp.1.2.2⟩⟩
  calc _ ≤ (E ×ˢ E).card := card_le_card hsub
    _ = E.card * E.card := card_product _ _
    _ ≤ 6 * 6 := Nat.mul_le_mul hE hE
    _ = 36 := rfl

omit hd hboard hdeg hdist in
lemma sideSet_four : sideSet a d n 4 = sideSet a d n 0 := by
  simp only [sideSet, rotPt_iter_four, rotL_iter_four, Function.iterate_zero, id]

/-- **The boundary pairs.** The crossing pairs at the four sides number at least `8n - 136`. -/
lemma boundary_card (hn : 4 ≤ n) :
    8 * n.toNat + 8 ≤ (sideSet a d n 0 ∪ sideSet a d n 1 ∪ sideSet a d n 2 ∪
      sideSet a d n 3).card + 144 := by
  set A0 := sideSet a d n 0
  set A1 := sideSet a d n 1
  set A2 := sideSet a d n 2
  set A3 := sideSet a d n 3
  have c0 : 2 * (n.toNat + 1) ≤ A0.card := sideSet_card hd hboard hdeg hdist (by omega) 0
  have c1 : 2 * (n.toNat + 1) ≤ A1.card := sideSet_card hd hboard hdeg hdist (by omega) 1
  have c2 : 2 * (n.toNat + 1) ≤ A2.card := sideSet_card hd hboard hdeg hdist (by omega) 2
  have c3 : 2 * (n.toNat + 1) ≤ A3.card := sideSet_card hd hboard hdeg hdist (by omega) 3
  have o02 : A0 ∩ A2 = ∅ := disjoint_iff_inter_eq_empty.1 (sideSet_opp hd hn 0)
  have o13 : A1 ∩ A3 = ∅ := disjoint_iff_inter_eq_empty.1 (sideSet_opp hd hn 1)
  have j01 : (A0 ∩ A1).card ≤ 36 := sideSet_adj hd hboard hdeg hdist (by omega) 0
  have j12 : (A1 ∩ A2).card ≤ 36 := sideSet_adj hd hboard hdeg hdist (by omega) 1
  have j23 : (A2 ∩ A3).card ≤ 36 := sideSet_adj hd hboard hdeg hdist (by omega) 2
  have j30 : (A0 ∩ A3).card ≤ 36 := by
    have := sideSet_adj hd hboard hdeg hdist (by omega) 3
    rwa [sideSet_four, inter_comm] at this
  have u1 := card_union_add_card_inter A0 A1
  have u2 := card_union_add_card_inter (A0 ∪ A1) A2
  have u3 := card_union_add_card_inter (A0 ∪ A1 ∪ A2) A3
  have i2 : ((A0 ∪ A1) ∩ A2).card ≤ 36 := by
    rw [union_inter_distrib_right, o02, empty_union]; exact j12
  have i3 : ((A0 ∪ A1 ∪ A2) ∩ A3).card ≤ 72 := by
    rw [union_inter_distrib_right, union_inter_distrib_right, o13, union_empty]
    calc _ ≤ (A0 ∩ A3).card + (A2 ∩ A3).card := card_union_le _ _
      _ ≤ 36 + 36 := Nat.add_le_add j30 j23
  omega

omit [DecidableEq ι] in
/-- A retained corner gives a charged step with both beside-squares among its squares. -/
lemma corner_charged {h : ℕ} (hN : n = 2 * h) (hh : 16 ≤ h) {c : ℕ × ℕ} (hc : c ∈ corners h)
    (hgood : GoodCorner a d n c) :
    ∃ q, besideSq q ⊆ cornerSq n c ∧ ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  obtain ⟨k, R⟩ := c
  simp only [corners, mem_product, mem_range, mem_Icc] at hc
  obtain ⟨⟨hL', -⟩, hB'⟩ := hgood
  have hB'' := (GoodRow.mod hB').1
  obtain ⟨hdk, hbk, hdegk, -⟩ := frame_ok hd hboard hdeg hdist k
  obtain ⟨hdk3, hbk3, hdegk3, -⟩ := frame_ok hd hboard hdeg hdist (k + 3)
  have hL : (3 : ℤ) ∣ ∑ i, gL ((rotPt n)^[k] (a i) - (0, (R : ℤ))) (rotL^[k] (d i)) - 1 := by
    rw [sum_gL_eq _ _ hdk (fun i => ⟨(hbk i).1.1, (hbk i).2.1⟩) R,
      hdegk (0, R) (by unfold InBoard; simp only; omega)]
    obtain ⟨u, hu⟩ := hL'
    exact ⟨u + 1, by push_cast; linarith⟩
  have hB : (3 : ℤ) ∣ ∑ i, gB ((rotPt n)^[k] (a i) - ((R : ℤ), 0)) (rotL^[k] (d i)) - 1 := by
    have e : ∀ i, gB ((rotPt n)^[k] (a i) - ((R : ℤ), 0)) (rotL^[k] (d i)) =
        gL ((rotPt n)^[k + 3] (a i) - (0, n - 2 - R)) (rotL^[k + 3] (d i)) := fun i => by
      rw [← rotPt_iter_add_three, ← rotL_iter_add_three, gB_rot (hdk3 i)]
    simp only [e]
    rw [sum_gL_eq _ _ hdk3 (fun i => ⟨(hbk3 i).1.1, (hbk3 i).2.1⟩) (n - 2 - R),
      hdegk3 (0, n - 2 - R) (by unfold InBoard; simp only; omega)]
    obtain ⟨u, hu⟩ := hB''
    exact ⟨u + 1, by push_cast; linarith⟩
  obtain ⟨q, hq, hnd⟩ := corner_charge_mod_rot a d hd n hboard hdeg k R hc.2.1 (by omega) hL hB
  refine ⟨q, fun t ht => ?_, hnd⟩
  have h1 : (rotSq n)^[k] t ∈ gammaSq R := by
    apply besideSq_subset_gammaSq hq
    rw [besideSq_rotE_iter]
    exact mem_image_of_mem _ ht
  simp only [cornerSq, mem_filter]
  refine ⟨?_, h1⟩
  rw [← rotSq_iter_mem_boardSq k]
  rw [mem_gammaSq] at h1
  simp only [boardSq, mem_product, mem_Icc]
  omega

/-- The tile overlaps of the boundary pairs avoid the squares of the retained corner paths. -/
lemma boundary_avoids {h : ℕ} (hN : n = 2 * h) (hh : 16 ≤ h) {k : ℕ} (hk : k < 4)
    {p : ι × ι} (hp : p ∈ sideSet a d n k) {c : ℕ × ℕ} (hc : c ∈ corners h)
    (hgood : GoodCorner a d n c) {t : QTri} (ht : sqOf t ∈ cornerSq n c) :
    ¬ (t ∈ tri (a p.1) (d p.1) ∧ t ∈ tri (a p.2) (d p.2)) := by
  rintro ⟨h1, h2⟩
  obtain ⟨hdk, hbk, -, hdistk⟩ := frame_ok hd hboard hdeg hdist k
  set ak : ι → Pt := fun i => (rotPt n)^[k] (a i)
  set dk : ι → Pt := fun i => rotL^[k] (d i)
  have m1 : (rotTri n)^[k] t ∈ tri (ak p.1) (dk p.1) := (mem_tri_rot_iter (hd _) n k _ t).2 h1
  have m2 : (rotTri n)^[k] t ∈ tri (ak p.2) (dk p.2) := (mem_tri_rot_iter (hd _) n k _ t).2 h2
  simp only [sideSet, sidePairs, crossPairs, mem_filter, mem_univ, true_and] at hp
  obtain ⟨⟨hne, -⟩, hc1, hc2⟩ := hp
  have hat : ∀ i, (ak i).1 = 0 ∨ (ak i + dk i).1 = 0 → ∃ y, i ∈ atCell ak dk (0, y) := by
    intro i hi
    rcases hi with hi | hi
    · exact ⟨(ak i).2, mem_atCell.2 (Or.inl (Prod.ext hi rfl))⟩
    · exact ⟨(ak i + dk i).2, mem_atCell.2 (Or.inr (Prod.ext hi rfl))⟩
  obtain ⟨y1, hy1⟩ := hat p.1 hc1
  obtain ⟨y2, hy2⟩ := hat p.2 hc2
  have hpos : ∀ i, 0 ≤ (ak i).1 ∧ 0 ≤ (ak i + dk i).1 := fun i =>
    ⟨(hbk i).1.1, (hbk i).2.1⟩
  have hsq := sqOf_rotTri_iter n k t
  subst hN
  have hfr := cornerSq_frame hh hc ht hk
  rw [← hsq] at hfr
  rcases col0_overlap hdk hdistk hpos hy1 hy2 hne m1 m2 with h0 | ⟨h1', j0, hj0, hex⟩
  · simp only [sqOf] at hfr; omega
  · -- the exceptional pair at row `j0` of side `k`, which is critical
    have hrowk : GoodRow a d (2 * h) k j0 := by
      have := hfr.2 (by simpa [sqOf] using h1')
      simp only [sqOf] at this
      rcases this with ⟨e1, e2⟩ | ⟨e1, e2⟩
      · rw [← e1, ← hj0, e2]; exact hgood.1
      · rw [← e1, ← hj0, e2]; exact hgood.2
    apply hrowk.2
    rcases hex with ⟨o1, e1, o2, e2⟩ | ⟨o1, e1, o2, e2⟩
    · rw [e1] at hy1 o1; rw [e2] at hy2 o2
      exact ⟨p.1, p.2, canon_exc hdk hy1 hy2 o1 o2⟩
    · rw [e1] at hy1 o1; rw [e2] at hy2 o2
      exact ⟨p.2, p.1, canon_exc hdk hy2 hy1 o2 o1⟩

/-- **The combined count.** For `n²` distinct knight edges in the board, `n = 2h`, `h ≥ 16`, with
degree two at every cell: `10 n ≤ Y + d + 130`, where `Y` is the number of ordered properly
crossing pairs (`Y = 2X`) and `d` is the number of non-critical rows in the scan ranges. -/
theorem combined_count {h : ℕ} (hN : n = 2 * h) (hh : 16 ≤ h)
    (hcard : Fintype.card ι = (2 * h) * (2 * h)) :
    10 * (2 * h) ≤ (crossPairs a d).card + (badRows a d h).card + 130 := by
  subst hN
  set N : ℤ := 2 * (h : ℤ)
  set Bo := sideSet a d N 0 ∪ sideSet a d N 1 ∪ sideSet a d N 2 ∪ sideSet a d N 3
  have hBo : Bo ⊆ crossPairs a d := by
    simp only [Bo, union_subset_iff]
    exact ⟨⟨⟨sideSet_sub 0, sideSet_sub 1⟩, sideSet_sub 2⟩, sideSet_sub 3⟩
  have hBoc : 8 * N.toNat + 8 ≤ Bo.card + 144 := boundary_card hd hboard hdeg hdist (by omega)
  have hNt : N.toNat = 2 * h := by omega
  rw [hNt] at hBoc
  set Rt := retained a d h
  have hRt : ∀ c ∈ Rt, c ∈ corners h ∧ GoodCorner a d N c := fun c hc => mem_filter.1 hc
  set e := Rt.equivFin
  set sq : Fin Rt.card → Finset Pt := fun l => cornerSq N (e.symm l).1
  set U : Finset QTri := (Rt.biUnion (cornerSq N)).biUnion
    fun s => (univ : Finset (Fin 4)).image fun j => (s.1, s.2, j)
  have hmemU : ∀ t ∈ U, ∃ c ∈ Rt, sqOf t ∈ cornerSq N c := by
    intro t ht
    obtain ⟨s, hs, ht⟩ := mem_biUnion.1 ht
    obtain ⟨c, hc, hs⟩ := mem_biUnion.1 hs
    obtain ⟨j, -, rfl⟩ := mem_image.1 ht
    exact ⟨c, hc, hs⟩
  have key := charged_squares_budget a d (2 * h) hd
    (fun i => by have := (hboard i).1; unfold InBoard at this; push_cast; omega)
    (fun i => by have := (hboard i).2; unfold InBoard at this; push_cast; omega)
    hdist hcard U
    (by
      intro t ht
      obtain ⟨c, -, hs⟩ := hmemU t ht
      simp only [cornerSq, boardSq, mem_filter, mem_product, mem_Icc] at hs
      obtain ⟨x, y, j⟩ := t
      simp only [sqOf] at hs
      simp only [boardTris, mem_product, mem_Icc, mem_univ, and_true]
      push_cast; omega)
    Bo hBo
    (by
      intro p hp t ht
      obtain ⟨c, hc, hs⟩ := hmemU t ht
      have hp' : ∃ k < 4, p ∈ sideSet a d N k := by
        simp only [Bo, mem_union] at hp
        rcases hp with ((hp | hp) | hp) | hp
        · exact ⟨0, by norm_num, hp⟩
        · exact ⟨1, by norm_num, hp⟩
        · exact ⟨2, by norm_num, hp⟩
        · exact ⟨3, by norm_num, hp⟩
      obtain ⟨k, hk, hp⟩ := hp'
      exact boundary_avoids hd hboard hdeg hdist rfl hh hk hp (hRt c hc).1 (hRt c hc).2 hs)
    Rt.card sq
    (by
      intro l l' hll'
      apply cornerSq_disjoint hh (hRt _ (e.symm l).2).1 (hRt _ (e.symm l').2).1
      intro heq
      exact hll' (e.symm.injective (Subtype.ext heq)))
    (by
      intro l s hs j
      exact mem_biUnion.2 ⟨s, mem_biUnion.2 ⟨_, (e.symm l).2, hs⟩,
        mem_image.2 ⟨j, mem_univ _, rfl⟩⟩)
    (by
      intro l
      have hc := hRt _ (e.symm l).2
      obtain ⟨q, hq, hnd⟩ := corner_charged hd hboard hdeg hdist rfl hh hc.1 hc.2
      exact ⟨q, hq (by simp [besideSq]), hq (by simp [besideSq]), hnd⟩)
  have hcnt : (corners h).card ≤ Rt.card + (badRows a d h).card := corners_le h
  have hc4 := card_corners hh
  omega

/-- **Conditional bound `X ≥ 14n/3 - O(1)`.** With the per-row stability hypothesis
`b ≤ E + C`, where `E = X - 4n + 2` and `Y = 2X` (stated as `2b ≤ Y - 8n + 4 + 2C`), the ordered
crossing pairs satisfy `28n ≤ 3Y + 2C + 264`. -/
theorem fourteen_mul_le_of_stability {h : ℕ} (hN : n = 2 * h) (hh : 16 ≤ h)
    (hcard : Fintype.card ι = (2 * h) * (2 * h)) (C : ℤ)
    (hstab : 2 * ((badRows a d h).card : ℤ) ≤ (crossPairs a d).card - 8 * (2 * h) + 4 + 2 * C) :
    28 * (2 * h : ℤ) ≤ 3 * (crossPairs a d).card + 2 * C + 264 := by
  have := combined_count hd hboard hdeg hdist hN hh hcard
  omega

end Standing

end Family

end KT
