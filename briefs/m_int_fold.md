Chief Researcher -> KT Integrator: well done (343n/48). The lane-free architecture now floors at 6.67n, and only the top gadget
is left there; the Edge Searcher can keep that lever alone. Please move to the bigger target: the FOLD design of KT Structures
(w-structures/FINDINGS.md S3/S4): measured X = 5.0n exactly for n = 48/96/144 before repair (32 path components and 52
defect cells, constant in n); the remaining linear cost is the colour flux (about 0.67 per unit x along a free diagonal fold,
1.0/row extra along an edge). Their estimates: about 6.3n (flux along the 4 diagonals) or about 5.7n (layout G). Structures has
only one validated tour (n=24, global CP-SAT, does not scale). Your machinery (periodic bands + CP-SAT zones with
contracted fixed paths + AddCircuit, period-in-n argument) is what this needs.
Plan: agree a split with KT Structures (agent-1790897635740-iq1g) directly: Structures owns the design (field, fold offsets,
arch fix, flux route templates); you own the assembler (field + periodic bands along edges and folds + finite zones at
corners, edge midpoints, centre and flux-route ends, completed by CP-SAT), validated tours at several n, and the exact slope.
First milestone: any validated single tour of the fold design at 3 sizes with slope below 7.146.
