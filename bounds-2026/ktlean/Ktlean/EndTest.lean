import Ktlean.Frames

/-!
# The weaker endpoint test (FINDINGS.md 10.4)

At a scan row `R`, let `F` be the sum of the coefficients of the selected edges in the list of
FINDINGS.md 10.2 (coordinates relative to row `R`, no `χ` factor). The row passes the test if
`F ≡ 2 (mod 3)` and the exceptional pair `(0,0)--(2,1)`, `(0,1)--(2,0)` is not both selected.

* `gL_eq_Fcoef`: for one edge, the flux through the two top end steps is `Fcoef` of the edge
  plus `1` if the edge meets the cell `(0, 0)`. So `Σ gL = F + deg(0, R)` (`sum_gL_eq`), and with
  degree two the test gives `Σ gL ≡ 1 (mod 3)`, which is what `corner_charge_mod` needs.
* `gB_rot`: the bottom end value of a frame is the top end value of the previous frame at row
  `n - 2 - R`.
* `corner_charge_mod_rot`: `corner_charge_mod` at every corner.

Remark (checked by hand, not used and not formalized): with degree two at `(0, R + 1)`, the
test reflected about row `R + 1/2` gives the same residue (both equal `Σ gL - 2`). In any case a
row that passes the joint test of TILE_INPUTS section 9 passes `GoodRow`.
-/

open Finset

namespace KT

/-- The coefficients of the eight listed edges, in canonical form (lower endpoint first),
relative to row `R`. -/
def Fcoef (e : Pt × Pt) : ℤ :=
  if e = ((0, -1), (1, 2)) then -1 else
  if e = ((1, -2), (-1, 2)) then -1 else
  if e = ((2, -1), (-2, 1)) then -1 else
  if e = ((1, -1), (-1, 2)) then 1 else
  if e = ((2, 0), (-2, 1)) then 1 else
  if e = ((1, 0), (-1, 2)) then -1 else
  if e = ((1, 0), (1, 2)) then -1 else
  if e = ((2, -1), (-1, 2)) then -1 else 0

lemma Fcoef_support {e : Pt × Pt} (h : Fcoef e ≠ 0) :
    0 ≤ e.1.1 ∧ e.1.1 ≤ 2 ∧ -2 ≤ e.1.2 ∧ e.1.2 ≤ 0 := by
  obtain ⟨⟨x, y⟩, ⟨u, v⟩⟩ := e
  unfold Fcoef at h
  dsimp only
  simp only [Prod.mk.injEq] at h
  split_ifs at h <;> omega

lemma gL_eq_Fcoef_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    0 ≤ x → 0 ≤ x + d.1 →
    gL (x, y) d = Fcoef (canon Prod.snd (x, y) d) +
      (if (x, y) = 0 ∨ (x, y) + d = 0 then 1 else 0) := by
  decide +kernel

lemma gL_eq_Fcoef {p d : Pt} (hd : d ∈ knightVecs) (hx : 0 ≤ p.1) (hx' : 0 ≤ p.1 + d.1) :
    gL p d = Fcoef (canon Prod.snd p d) + (if p = 0 ∨ p + d = 0 then 1 else 0) := by
  by_cases hn : p.1 ∈ Icc (-4 : ℤ) 4 ∧ p.2 ∈ Icc (-4 : ℤ) 4
  · exact gL_eq_Fcoef_rel p.1 hn.1 p.2 hn.2 d hd hx hx'
  · simp only [mem_Icc] at hn
    have hb := mid_bounds hd
    have h1 : flux1 p d ((0, 0), true) = 0 := by
      by_contra h1; have := flux1_far hd h1; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h2 : flux1 p d ((1, 0), true) = 0 := by
      by_contra h2; have := flux1_far hd h2; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h3 : Fcoef (canon Prod.snd p d) = 0 := by
      by_contra h3
      have := Fcoef_support h3
      unfold canon at this
      split_ifs at this <;> simp only [Prod.fst_add, Prod.snd_add] at this <;> omega
    have h4 : ¬ (p = 0 ∨ p + d = 0) := by
      rintro (h | h) <;> simp only [Prod.ext_iff, Prod.fst_add, Prod.snd_add, Prod.fst_zero,
        Prod.snd_zero] at h <;> omega
    simp [gL, h1, h2, h3, h4]

/-- The bottom end value of the next frame is the top end value at row `n - 2 - R`. -/
lemma gB_rot {d : Pt} (hd : d ∈ knightVecs) (n R : ℤ) (p : Pt) :
    gB (rotPt n p - (R, 0)) (rotL d) = gL (p - (0, n - 2 - R)) d := by
  have key : ∀ j : ℤ, flux1 (rotPt n p - (R, 0)) (rotL d) ((0, j), false) =
      flux1 (p - (0, n - 2 - R)) d ((j, 0), true) := by
    intro j
    have e1 : flux1 (rotPt n p) (rotL d) ((R, j), false) =
        chi (R, 0) * flux1 (rotPt n p - (R, 0)) (rotL d) ((0, j), false) := by
      rw [← flux1_add _ _ (R, 0) (0, j) false (rotL_mem hd), sub_add_cancel]
      congr 2; ext <;> simp
    have e2 : (((R, j), false) : GridEdge) = rotE n ((j, n - 2 - R), true) := by
      simp only [rotE, rotPt, ite_true, Prod.mk.injEq, and_true]
      ext <;> simp; ring
    have e3 : flux1 p d ((j, n - 2 - R), true) =
        chi (0, n - 2 - R) * flux1 (p - (0, n - 2 - R)) d ((j, 0), true) := by
      rw [← flux1_add _ _ (0, n - 2 - R) (j, 0) true hd, sub_add_cancel]
      congr 2; ext <;> simp
    rw [e2, flux1_rot hd, e3] at e1
    have hc : chi (n - 1, 0) * rotSgn ((j, n - 2 - R), true) * chi (0, n - 2 - R) =
        chi (R, 0) := by
      simp only [chi, rotSgn, ite_true]; split_ifs <;> omega
    have hsq : chi (R, 0) * chi (R, 0) = 1 := by simp only [chi]; split_ifs <;> norm_num
    set F := flux1 (p - (0, n - 2 - R)) d ((j, 0), true)
    set G := flux1 (rotPt n p - (R, 0)) (rotL d) ((0, j), false)
    have : chi (R, 0) * (G - F) = 0 := by linear_combination -e1 + F * hc
    rcases mul_eq_zero.1 this with h | h
    · rw [h] at hsq; simp at hsq
    · linarith
  simp only [gB, gL, key]

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- `Σ gL = F + deg(0, R)` for a family in the half plane `x ≥ 0`. -/
lemma sum_gL_eq (hd : ∀ i, d i ∈ knightVecs) (hx : ∀ i, 0 ≤ (a i).1 ∧ 0 ≤ (a i + d i).1)
    (R : ℤ) :
    ∑ i, gL (a i - (0, R)) (d i) =
      ∑ i, Fcoef (canon Prod.snd (a i - (0, R)) (d i)) + deg a d (0, R) := by
  classical
  rw [← card_atCell hd, atCell, card_filter]
  push_cast
  rw [← sum_add_distrib]
  refine sum_congr rfl fun i _ => ?_
  rw [gL_eq_Fcoef (hd i) (by simpa using (hx i).1)
    (by have := (hx i).2; simp only [Prod.fst_add, Prod.fst_sub] at this ⊢; omega)]
  congr 1
  have e : (a i - (0, R) = 0 ∨ a i - (0, R) + d i = 0) ↔ (a i = (0, R) ∨ a i + d i = (0, R)) := by
    rw [sub_eq_zero, sub_add_eq_add_sub, sub_eq_zero]
  simp only [e]

/-- **Corner charge at every corner, from the end values mod 3.** -/
theorem corner_charge_mod_rot (hd : ∀ i, d i ∈ knightVecs) (n : ℤ)
    (hboard : ∀ i, InBoard n (a i) ∧ InBoard n (a i + d i))
    (hdeg : ∀ v, InBoard n v → deg a d v = 2)
    (k : ℕ) (R : ℕ) (hR : 12 ≤ R) (hRn : (R : ℤ) < n)
    (hL : (3 : ℤ) ∣ ∑ i, gL ((rotPt n)^[k] (a i) - (0, (R : ℤ))) (rotL^[k] (d i)) - 1)
    (hB : (3 : ℤ) ∣ ∑ i, gB ((rotPt n)^[k] (a i) - ((R : ℤ), 0)) (rotL^[k] (d i)) - 1) :
    ∃ q, (rotE n)^[k] q ∈ gammaSteps R ∧ ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  set ak : ι → Pt := fun i => (rotPt n)^[k] (a i)
  set dk : ι → Pt := fun i => rotL^[k] (d i)
  have hdk : ∀ i, dk i ∈ knightVecs := fun i => rotL_iter_mem (hd i) k
  have hpos : ∀ i, 0 ≤ (ak i).1 ∧ 0 ≤ (ak i).2 ∧ 0 ≤ (ak i + dk i).1 ∧ 0 ≤ (ak i + dk i).2 := by
    intro i
    have h1 := (hboard i).1.iter k
    have h2 := (hboard i).2.iter k
    rw [rotPt_iter_add] at h2
    exact ⟨h1.1, h1.2.2.1, h2.1, h2.2.2.1⟩
  have hdegk : ∀ v ∈ box R, deg ak dk v = 2 := by
    intro v hv
    have hvb : InBoard n v := by
      simp only [box, mem_product, mem_Icc] at hv
      unfold InBoard; omega
    obtain ⟨u, hu, rfl⟩ := exists_rot_iter hvb k
    rw [deg_iter a d n k u, hdeg u hu]
  obtain ⟨q', hq', hnd⟩ := corner_charge_mod ak dk hdk hpos R hR hdegk hL hB
  obtain ⟨q, rfl⟩ := ((rotE_surjective n).iterate k) q'
  exact ⟨q, hq', fun h => hnd ((three_dvd_omega_iter_iff a d hd n k q).2 h)⟩

end Family

end KT
