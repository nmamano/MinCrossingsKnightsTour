import Ktlean.Tour
import Ktlean.CrossCore

/-!
# Lower bound `4 * n - 2` on crossings

For closed tours and for 2-factors of the knight's graph on the `n × n` board.
-/

open Finset

namespace KT

variable {n : ℕ}

/-- A cell as a lattice point. -/
def pt (v : Cell n) : Pt := ((v.1 : ℤ), (v.2 : ℤ))

lemma pt_injective : Function.Injective (pt (n := n)) := by
  intro u v h
  simp only [pt, Prod.mk.injEq, Nat.cast_inj] at h
  exact Prod.ext (Fin.ext h.1) (Fin.ext h.2)

lemma pt_bounds (v : Cell n) : 0 ≤ (pt v).1 ∧ (pt v).1 < n ∧ 0 ≤ (pt v).2 ∧ (pt v).2 < n := by
  have := v.1.isLt; have := v.2.isLt
  simp only [pt]; omega

lemma disp_eq (u v : Cell n) : disp u v = pt v - pt u := rfl

lemma IsKnightMove.mem_knightVecs {u v : Cell n} (h : IsKnightMove u v) :
    pt v - pt u ∈ knightVecs := by
  rw [← disp_eq]; exact IsKnightVec.mem h

lemma detR_toPlane (a b c : Cell n) :
    detR (toPlane a) (toPlane b) (toPlane c) = (det (pt a) (pt b) (pt c) : ℝ) := by
  simp only [detR, det, toPlane, pt]; push_cast; ring

lemma ProperCross.openSegmentsMeet {a b c d : Cell n}
    (h : ProperCross (pt a) (pt b) (pt c) (pt d)) : OpenSegmentsMeet a b c d := by
  obtain ⟨h1, h2⟩ := h
  apply openSegment_inter_nonempty
  · rw [detR_toPlane, detR_toPlane]; exact_mod_cast h1
  · rw [detR_toPlane, detR_toPlane]; exact_mod_cast h2

/-- **Crossings of closed tours.** Every closed knight's tour of the `n × n` board has at least
`4 * n - 2` crossings. -/
theorem ClosedTour.four_mul_sub_two_le_numCrossings (T : ClosedTour n) :
    4 * n - 2 ≤ T.numCrossings := by
  classical
  set a : Fin (n * n) → Pt := fun i => pt (T.cell i)
  set d : Fin (n * n) → Pt := fun i => pt (T.cell (finRotate _ i)) - pt (T.cell i)
  have had : ∀ i, a i + d i = pt (T.cell (finRotate _ i)) := fun i => by simp [a, d]
  have key := eight_mul_le_properCross_pairs n a d
    (fun i => (T.isKnightMove i).mem_knightVecs) (fun i => pt_bounds _)
    (fun i => by rw [had]; exact pt_bounds _)
    (by
      intro i j hij h
      simp only [had, a] at h
      rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · exact hij (T.cell.injective (pt_injective h1))
      · have e1 := T.cell.injective (pt_injective h1)
        have e2 := T.cell.injective (pt_injective h2)
        by_cases hn : n ≤ 1
        · have : Subsingleton (Fin (n * n)) := by
            rw [Fin.subsingleton_iff_le_one]; nlinarith
          exact hij (Subsingleton.elim _ _)
        · apply finRotate_symm_ne (m := n * n) (by nlinarith) i
          rw [e2, e1, Equiv.symm_apply_apply])
    (by simp)
  simp only [had] at key
  -- each crossing pair is counted twice
  set X := univ.filter fun p : Fin (n * n) × Fin (n * n) => p.1 < p.2 ∧
    OpenSegmentsMeet (T.cell p.1) (T.cell (finRotate _ p.1))
      (T.cell p.2) (T.cell (finRotate _ p.2))
  have hX : T.numCrossings = X.card := by unfold ClosedTour.numCrossings; congr 1
  have hle := card_le_card (s := univ.filter fun p : Fin (n * n) × Fin (n * n) =>
      p.1 ≠ p.2 ∧ ProperCross (a p.1) (pt (T.cell (finRotate _ p.1)))
        (a p.2) (pt (T.cell (finRotate _ p.2)))) (t := X ∪ X.image Prod.swap) (by
    intro p hp
    simp only [mem_filter, mem_univ, true_and, a] at hp
    rcases lt_or_gt_of_ne hp.1 with hlt | hlt
    · exact mem_union_left _ (by
        simp only [X, mem_filter, mem_univ, true_and]
        exact ⟨hlt, hp.2.openSegmentsMeet⟩)
    · refine mem_union_right _ (mem_image.2 ⟨p.swap, ?_, Prod.swap_swap p⟩)
      simp only [X, mem_filter, mem_univ, true_and, Prod.fst_swap, Prod.snd_swap]
      exact ⟨hlt, ((properCross_comm _ _ _ _).1 hp.2).openSegmentsMeet⟩)
  have h1 := card_union_le X (X.image Prod.swap)
  have h2 := card_image_le (s := X) (f := Prod.swap)
  omega

/-- An ordered representative of an unordered pair. -/
noncomputable def rep {α : Type*} (e : Sym2 α) : α × α := Quot.out e

lemma mk_rep {α : Type*} (e : Sym2 α) : s((rep e).1, (rep e).2) = e := Quot.out_eq e

lemma TwoFactor.card_edgeFinset (F : TwoFactor n) [Fintype F.graph.edgeSet] :
    F.graph.edgeFinset.card = n * n := by
  classical
  have h := F.graph.sum_degrees_eq_twice_card_edges
  have hdeg : ∀ v, F.graph.degree v = 2 := by
    intro v
    rw [← SimpleGraph.card_neighborFinset_eq_degree, ← F.card_nbrs v]
    congr 1
    ext u
    rw [SimpleGraph.mem_neighborFinset]
    rfl
  simp only [hdeg, sum_const, card_univ, Fintype.card_prod, Fintype.card_fin, smul_eq_mul] at h
  have h' : (@SimpleGraph.edgeFinset _ F.graph (SimpleGraph.fintypeEdgeSet _)).card = n * n := by
    omega
  convert h' using 2
  ext e
  simp only [SimpleGraph.mem_edgeFinset]

/-- **Crossings of 2-factors.** Every 2-factor of the knight's graph on the `n × n` board has
at least `4 * n - 2` crossings. -/
theorem TwoFactor.four_mul_sub_two_le_numCrossings (F : TwoFactor n) :
    4 * n - 2 ≤ F.numCrossings := by
  classical
  unfold TwoFactor.numCrossings
  set E := F.graph.edgeFinset
  have hadj : ∀ e : E, (rep e.1).2 ∈ F.nbrs (rep e.1).1 := by
    intro e
    have he := e.2
    rw [← mk_rep e.1] at he
    exact (SimpleGraph.mem_edgeFinset.1 he : F.graph.Adj _ _)
  set a : E → Pt := fun e => pt (rep e.1).1
  set d : E → Pt := fun e => pt (rep e.1).2 - pt (rep e.1).1
  have had : ∀ e, a e + d e = pt (rep e.1).2 := fun e => by simp [a, d]
  have key := eight_mul_le_properCross_pairs n a d
    (fun e => (F.isKnightMove _ _ (hadj e)).mem_knightVecs) (fun e => pt_bounds _)
    (fun e => by rw [had]; exact pt_bounds _)
    (by
      intro e f hef h
      simp only [had, a] at h
      apply hef
      apply Subtype.ext
      rw [← mk_rep e.1, ← mk_rep f.1]
      rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · rw [pt_injective h1, pt_injective h2]
      · rw [pt_injective h1, pt_injective h2, Sym2.eq_swap])
    (by rw [Fintype.card_coe]; exact F.card_edgeFinset)
  simp only [had] at key
  have hle := card_le_mul_card_image_of_maps_to (f := fun q : E × E => ({q.1.1, q.2.1} : Finset _))
    (s := univ.filter fun q : E × E => q.1 ≠ q.2 ∧
      ProperCross (a q.1) (pt (rep q.1.1).2) (a q.2) (pt (rep q.2.1).2))
    (t := (E.powersetCard 2).filter fun P => ∃ e ∈ P, ∃ f ∈ P, e ≠ f ∧ EdgesCross e f)
    (by
      intro q hq
      simp only [mem_filter, mem_univ, true_and, a] at hq
      have hne : q.1.1 ≠ q.2.1 := fun h => hq.1 (Subtype.ext h)
      simp only [mem_filter, mem_powersetCard]
      refine ⟨⟨?_, card_pair hne⟩, q.1.1, by simp, q.2.1, by simp, hne, ?_⟩
      · intro x hx
        simp only [mem_insert, mem_singleton] at hx
        rcases hx with rfl | rfl
        · exact q.1.2
        · exact q.2.2
      · exact ⟨_, _, _, _, (mk_rep _).symm, (mk_rep _).symm, hq.2.openSegmentsMeet⟩)
    2 (by
      intro P hP
      simp only [mem_filter, mem_powersetCard] at hP
      obtain ⟨x, y, hxy, rfl⟩ := card_eq_two.1 hP.1.2
      refine (card_le_card_of_injOn (fun q : E × E => (q.1.1, q.2.1))
        (t := {(x, y), (y, x)}) ?_ ?_).trans (card_le_two)
      · intro q hq
        simp only [coe_filter, Set.mem_ofPred_eq, mem_filter, mem_univ, true_and] at hq
        obtain ⟨⟨hq1, -⟩, hq2⟩ := hq
        have hne : q.1.1 ≠ q.2.1 := fun h => hq1 (Subtype.ext h)
        have h1 : q.1.1 ∈ ({x, y} : Finset _) := hq2 ▸ by simp
        have h2 : q.2.1 ∈ ({x, y} : Finset _) := hq2 ▸ by simp
        simp only [mem_insert, mem_singleton] at h1 h2
        simp only [coe_insert, coe_singleton, Set.mem_insert_iff, Set.mem_singleton_iff,
          Prod.mk.injEq]
        rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2 <;>
          simp_all
      · intro q _ r _ h
        simp only [Prod.mk.injEq] at h
        exact Prod.ext (Subtype.ext h.1) (Subtype.ext h.2))
  omega

end KT
