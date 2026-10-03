import Ktlean.Corner

/-!
# The corner charge from one critical row at each end (FINDINGS.md sections 10.1-10.2)

In `corner_charge` the end value comes only from the knight edges that cross the two top end
steps (`x = 0, 1`, between rows `R` and `R + 1`) and the two right end steps (`y = 0, 1`, between
columns `R` and `R + 1`). Such an edge has an endpoint in column `0` or `1` and straddles row `R`
(lower endpoint row `≤ R`, upper endpoint row `> R`); for the bottom side, transpose.

A critical scan row `R` of the left strip fixes exactly these edges (FINDINGS.md 10.1): the edges
of the family with an endpoint in columns `0, 1` that straddle row `R` are the edges of the
pattern `P` (or `P'`) that straddle row `R`. We take this as the hypothesis. It is weaker than the
four-row pattern hypothesis of `corner_charge`.

Edges are written in a canonical orientation `(p, d)`: for the left side `d.2 > 0`, for the
bottom side `d.1 > 0`.
-/

open Finset

namespace KT

/-- The canonical orientation of the edge from `p` to `p + d` with respect to a coordinate `k`:
the endpoint with the smaller `k` first. -/
def canon (k : Pt → ℤ) (p d : Pt) : Pt × Pt := if 0 < k d then (p, d) else (p + d, -d)

/-- A canonical left strip edge (an endpoint in column `0` or `1`) that straddles row `0`. -/
def StradL (e : Pt × Pt) : Prop :=
  (e.1.1 ≤ 1 ∨ e.1.1 + e.2.1 ≤ 1) ∧ e.1.2 ≤ 0 ∧ 0 < e.1.2 + e.2.2

instance : DecidablePred StradL := fun e => by unfold StradL; infer_instance

/-- A canonical bottom strip edge (an endpoint in row `0` or `1`) that straddles column `0`. -/
def StradB (e : Pt × Pt) : Prop :=
  (e.1.2 ≤ 1 ∨ e.1.2 + e.2.2 ≤ 1) ∧ e.1.1 ≤ 0 ∧ 0 < e.1.1 + e.2.1

instance : DecidablePred StradB := fun e => by unfold StradB; infer_instance

/-- The edges of the pattern `P` (`s = 1`) or `P'` (`s = -1`) of the left strip that straddle
row `0`. Every such edge has its endpoints in rows `-2..2`, so the cells in rows `-2..2` give
all of them. -/
def PL (s : ℤ) : Finset (Pt × Pt) :=
  (((({0, 1} : Finset ℤ) ×ˢ Icc (-2) 2).biUnion fun v =>
    (patL s v).image fun w => canon Prod.snd v (w - v))).filter StradL

/-- The same for the bottom strip (transposed). -/
def PB (s : ℤ) : Finset (Pt × Pt) :=
  ((Icc (-2) 2 ×ˢ ({0, 1} : Finset ℤ)).biUnion fun v =>
    (patB s v).image fun w => canon Prod.fst v (w - v)).filter StradB

/-- The end values: the flux of the straddling pattern edges through the two end steps. -/
def endL (s : ℤ) : ℤ := ∑ e ∈ PL s, gL e.1 e.2
def endB (s : ℤ) : ℤ := ∑ e ∈ PB s, gB e.1 e.2

lemma endL_eq : ∀ s ∈ ({1, -1} : Finset ℤ), endL s = 1 := by decide +kernel
lemma endB_eq : ∀ s ∈ ({1, -1} : Finset ℤ), endB s = 1 := by decide +kernel

lemma gL_strad_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    0 ≤ x → 0 ≤ x + d.1 → gL (x, y) d ≠ 0 → StradL (canon Prod.snd (x, y) d) := by
  decide +kernel

lemma gB_strad_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    0 ≤ y → 0 ≤ y + d.2 → gB (x, y) d ≠ 0 → StradB (canon Prod.fst (x, y) d) := by
  decide +kernel

lemma gL_strad {p d : Pt} (hd : d ∈ knightVecs) (hx : 0 ≤ p.1) (hx' : 0 ≤ p.1 + d.1)
    (h : gL p d ≠ 0) : StradL (canon Prod.snd p d) := by
  have hn : |p.1| ≤ 4 ∧ |p.2| ≤ 4 := by
    by_contra hc
    apply h
    have h1 : flux1 p d ((0, 0), true) = 0 := by
      by_contra h1; have := flux1_far hd h1; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h2 : flux1 p d ((1, 0), true) = 0 := by
      by_contra h2; have := flux1_far hd h2; dsimp only at this; rw [abs_le, abs_le] at *; omega
    simp [gL, h1, h2]
  rw [abs_le, abs_le] at hn
  exact gL_strad_rel p.1 (mem_Icc.2 hn.1) p.2 (mem_Icc.2 hn.2) d hd hx hx' h

lemma gB_strad {p d : Pt} (hd : d ∈ knightVecs) (hy : 0 ≤ p.2) (hy' : 0 ≤ p.2 + d.2)
    (h : gB p d ≠ 0) : StradB (canon Prod.fst p d) := by
  have hn : |p.1| ≤ 4 ∧ |p.2| ≤ 4 := by
    by_contra hc
    apply h
    have h1 : flux1 p d ((0, 0), false) = 0 := by
      by_contra h1; have := flux1_far hd h1; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h2 : flux1 p d ((0, 1), false) = 0 := by
      by_contra h2; have := flux1_far hd h2; dsimp only at this; rw [abs_le, abs_le] at *; omega
    simp [gB, h1, h2]
  rw [abs_le, abs_le] at hn
  exact gB_strad_rel p.1 (mem_Icc.2 hn.1) p.2 (mem_Icc.2 hn.2) d hd hy hy' h

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

omit [Fintype ι] in
lemma DistinctEdges.sub (hdist : DistinctEdges a d) (t : Pt) :
    DistinctEdges (fun i => a i - t) d := by
  intro i j hij h
  apply hdist i j hij
  simp only [sub_add_eq_add_sub, sub_left_inj] at h
  exact h

/-- If the edges of a family that meet a set `S` are exactly the edges of `P` (in canonical
orientation), then a symmetric edge function supported on `S` has the same sum on the family
and on `P`. -/
lemma sum_eq_of_image (hdist : DistinctEdges a d) (k : Pt → ℤ) (S : Pt × Pt → Prop)
    [DecidablePred S] (g : Pt → Pt → ℤ) (hsymm : ∀ i, g (a i + d i) (-d i) = g (a i) (d i))
    (hsupp : ∀ i, g (a i) (d i) ≠ 0 → S (canon k (a i) (d i))) (P : Finset (Pt × Pt))
    (hP : (univ.filter fun i => S (canon k (a i) (d i))).image (fun i => canon k (a i) (d i)) = P) :
    ∑ i, g (a i) (d i) = ∑ e ∈ P, g e.1 e.2 := by
  have hc : ∀ i, g (canon k (a i) (d i)).1 (canon k (a i) (d i)).2 = g (a i) (d i) := by
    intro i; unfold canon; split_ifs
    · rfl
    · exact hsymm i
  have hinj : Set.InjOn (fun i => canon k (a i) (d i))
      (univ.filter fun i => S (canon k (a i) (d i))) := by
    intro i _ j _ hij
    by_contra hne
    apply hdist i j hne
    simp only [canon] at hij
    split_ifs at hij <;> simp only [Prod.mk.injEq] at hij <;> obtain ⟨h1, h2⟩ := hij
    · exact Or.inl ⟨h1, by rw [h1, h2]⟩
    · exact Or.inr ⟨h1, by rw [h2, h1]; abel⟩
    · exact Or.inr ⟨by rw [← h1, ← neg_neg (d j), ← h2]; abel, h1⟩
    · have : d i = d j := neg_inj.1 h2
      exact Or.inl ⟨by rw [this] at h1; exact add_right_cancel h1, h1⟩
  rw [← hP, sum_image hinj, sum_filter_of_ne]
  · exact sum_congr rfl fun i _ => (hc i).symm
  · intro i _ h; exact hsupp i (by rwa [hc] at h)

/-- **Corner charge from the end values mod 3.** For a family of knight edges inside the
quadrant `x, y ≥ 0`, with degree two on the box `[0, R]²`: if the flux through the two top end
steps (`gL`, in coordinates relative to `(0, R)`) and through the two right end steps (`gB`,
relative to `(R, 0)`) are both `1` mod 3, then some step of the interior path `γ_R` has
`ω = flux + χ` not divisible by 3. -/
theorem corner_charge_mod (hd : ∀ i, d i ∈ knightVecs)
    (hpos : ∀ i, 0 ≤ (a i).1 ∧ 0 ≤ (a i).2 ∧ 0 ≤ (a i + d i).1 ∧ 0 ≤ (a i + d i).2)
    (R : ℕ) (hR : 12 ≤ R) (hdeg : ∀ v ∈ box R, deg a d v = 2)
    (hL : (3 : ℤ) ∣ ∑ i, gL (a i - (0, (R : ℤ))) (d i) - 1)
    (hB : (3 : ℤ) ∣ ∑ i, gB (a i - ((R : ℤ), 0)) (d i) - 1) :
    ∃ q ∈ gammaSteps R, ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  by_contra hall
  push Not at hall
  have hR2 : (2 : ℤ) ≤ R := by omega
  have h0 := three_dvd_sum_bdry a d hd (box R) hdeg
  obtain ⟨dj1, dj2⟩ := disjoint_parts hR2
  rw [bdry_box hR2, sum_union dj1, sum_union dj2] at h0
  -- the interior path
  have hΓ : (3 : ℤ) ∣ ∑ q ∈ gammaSteps R, eps (box R) q * (flux a d q + chi q.1) :=
    dvd_sum fun q hq => dvd_mul_of_dvd_right (hall q hq) _
  -- the outer steps
  have hO : 2 * ∑ q ∈ outerSteps R, eps (box R) q * (flux a d q + chi q.1) =
      2 * (1 + chi (0, R)) := by
    have hflux : ∀ q ∈ outerSteps R, flux a d q = 0 := fun q hq =>
      sum_eq_zero fun i _ => flux1_outer (hd i) ⟨(hpos i).1, (hpos i).2.1⟩
        ⟨(hpos i).2.2.1, (hpos i).2.2.2⟩ hq
    rw [sum_congr rfl fun q hq => by rw [hflux q hq, zero_add]]
    unfold outerSteps
    rw [sum_union]
    · rw [sum_image (by intro x _ y _ h; simpa using h),
        sum_image (by intro x _ y _ h; simpa using h)]
      have e1 : ∀ y ∈ Icc (0 : ℤ) R, eps (box R) ((-1, y), false) * chi ((-1, y), false).1 =
          chi (0, y) := by
        intro y _; simp [eps, box, chi]; split_ifs <;> omega
      have e2 : ∀ x ∈ Icc (0 : ℤ) R, eps (box R) ((x, -1), true) * chi ((x, -1), true).1 =
          chi (x, 0) := by
        intro x _; simp [eps, box, chi]; split_ifs <;> omega
      rw [sum_congr rfl e1, sum_congr rfl e2, mul_add, two_mul_sum_chi_col, two_mul_sum_chi_row]
      ring
    · rw [disjoint_left]; intro q h1 h2
      simp only [mem_image] at h1 h2
      obtain ⟨y, -, rfl⟩ := h1; obtain ⟨x, -, h⟩ := h2; simp [Prod.ext_iff] at h
  -- the four end steps
  have hT : ∃ w : ℤ, ∑ q ∈ T4 R, eps (box R) q * (flux a d q + chi q.1) =
      chi (0, R) * (2 + 3 * w) := by
    have he : ∀ q ∈ T4 R, eps (box R) q = 1 := by
      intro q hq; simp only [T4, mem_insert, mem_singleton] at hq
      rcases hq with rfl | rfl | rfl | rfl <;> simp [eps, box] <;> omega
    rw [sum_congr rfl fun q hq => by rw [he q hq, one_mul], sum_add_distrib]
    have hchi : ∑ q ∈ T4 R, chi q.1 = 0 := by
      unfold T4
      rw [sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega), sum_singleton]
      simp only [chi]; split_ifs <;> omega
    have hfl : ∑ q ∈ T4 R, flux a d q = ∑ i, (chi (0, (R : ℤ)) * gL (a i - (0, (R : ℤ))) (d i) +
        chi ((R : ℤ), 0) * gB (a i - ((R : ℤ), 0)) (d i)) := by
      simp only [flux]
      rw [sum_comm]
      refine sum_congr rfl fun i _ => ?_
      unfold T4
      rw [sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega), sum_singleton]
      have t : ∀ (t : Pt) (c : Pt) (v : Bool), flux1 (a i) (d i) (c + t, v) =
          chi t * flux1 (a i - t) (d i) (c, v) := by
        intro t c v
        rw [← flux1_add _ _ t c v (hd i), sub_add_cancel]
      rw [show (((0 : ℤ), (R : ℤ)), true) = ((0, 0) + (0, (R : ℤ)), true) by simp,
        show (((1 : ℤ), (R : ℤ)), true) = ((1, 0) + (0, (R : ℤ)), true) by simp,
        show (((R : ℤ), (0 : ℤ)), false) = ((0, 0) + ((R : ℤ), 0), false) by simp,
        show (((R : ℤ), (1 : ℤ)), false) = ((0, 1) + ((R : ℤ), 0), false) by simp, t, t, t, t]
      simp only [gL, gB]; ring
    have hc : chi ((R : ℤ), 0) = chi (0, (R : ℤ)) := by simp [chi]
    obtain ⟨u, hu⟩ := hL
    obtain ⟨v, hv⟩ := hB
    refine ⟨u + v, ?_⟩
    rw [hchi, add_zero, hfl, sum_add_distrib, ← mul_sum, ← mul_sum, hc]
    linear_combination chi (0, (R : ℤ)) * hu + chi (0, (R : ℤ)) * hv
  -- conclusion
  set O := ∑ q ∈ outerSteps R, eps (box R) q * (flux a d q + chi q.1)
  set T := ∑ q ∈ T4 R, eps (box R) q * (flux a d q + chi q.1)
  set Γ := ∑ q ∈ gammaSteps R, eps (box R) q * (flux a d q + chi q.1)
  obtain ⟨k, hk⟩ := h0
  obtain ⟨m, hm⟩ := hΓ
  obtain ⟨w, hw⟩ := hT
  have hchi1 : chi (0, (R : ℤ)) = 1 ∨ chi (0, (R : ℤ)) = -1 := by
    unfold chi; split_ifs <;> simp
  rcases hchi1 with h | h <;> rw [h] at hO hw <;> omega

/-- **Corner charge from one critical row at each end.** For a family of distinct knight edges
inside the board, with degree two on the box `[0, R]²`: if the left strip edges that straddle
row `R` are exactly the `P/P'` edges (sign `sL`) that straddle row `R`, and the bottom strip edges
that straddle column `R` are exactly the transposed `P/P'` edges (sign `sB`), then some step of
the interior path `γ_R` has `ω = flux + χ` not divisible by 3. -/
theorem corner_charge_row (hd : ∀ i, d i ∈ knightVecs)
    (hpos : ∀ i, 0 ≤ (a i).1 ∧ 0 ≤ (a i).2 ∧ 0 ≤ (a i + d i).1 ∧ 0 ≤ (a i + d i).2)
    (hdist : DistinctEdges a d)
    (R : ℕ) (hR : 12 ≤ R) (hdeg : ∀ v ∈ box R, deg a d v = 2)
    (sL sB : ℤ) (hsL : sL ∈ ({1, -1} : Finset ℤ)) (hsB : sB ∈ ({1, -1} : Finset ℤ))
    (hrowL : (univ.filter fun i => StradL (canon Prod.snd (a i - (0, (R : ℤ))) (d i))).image
      (fun i => canon Prod.snd (a i - (0, (R : ℤ))) (d i)) = PL sL)
    (hrowB : (univ.filter fun i => StradB (canon Prod.fst (a i - ((R : ℤ), 0)) (d i))).image
      (fun i => canon Prod.fst (a i - ((R : ℤ), 0)) (d i)) = PB sB) :
    ∃ q ∈ gammaSteps R, ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  refine corner_charge_mod a d hd hpos R hR hdeg ⟨0, ?_⟩ ⟨0, ?_⟩
  · rw [sum_eq_of_image (fun i => a i - (0, (R : ℤ))) d (hdist.sub a d _) Prod.snd StradL
      gL (fun i => by simp only [sub_add_eq_add_sub]; rw [show a i + d i - (0, (R : ℤ)) =
        a i - (0, (R : ℤ)) + d i by abel]; exact gL_symm (hd i))
      (fun i h => gL_strad (hd i) (by simpa using (hpos i).1)
          (by have := (hpos i).2.2.1; simp only [Prod.fst_add, Prod.fst_sub] at this ⊢; omega) h)
      (PL sL) hrowL, ← endL, endL_eq sL hsL]
    ring
  · rw [sum_eq_of_image (fun i => a i - ((R : ℤ), 0)) d (hdist.sub a d _) Prod.fst StradB
      gB (fun i => by simp only [sub_add_eq_add_sub]; rw [show a i + d i - ((R : ℤ), 0) =
        a i - ((R : ℤ), 0) + d i by abel]; exact gB_symm (hd i))
      (fun i h => gB_strad (hd i) (by simpa using (hpos i).2.1)
          (by have := (hpos i).2.2.2; simp only [Prod.snd_add, Prod.snd_sub] at this ⊢; omega) h)
      (PB sB) hrowB, ← endB, endB_eq sB hsB]
    ring

end Family

end KT
