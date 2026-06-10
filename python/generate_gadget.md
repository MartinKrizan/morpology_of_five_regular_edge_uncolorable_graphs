Here is a task you can paste into Codex. I wrote it so Codex first inspects your existing project and then implements a computational gadget search without assuming too much about your current code structure.

---

## Codex task: Search for a 5-regular 5-port edge-coloring gadget

We are working on a graph theory project about finding **5-regular, 5-edge-connected, non-5-edge-colorable graphs** using gadget replacement.

I want to computationally search for a **5-port gadget** that can be used to replace a 3-vertex path in a cubic snark.

### Mathematical background

A 3-vertex path in a cubic graph has 5 boundary edges. In any 3-edge-coloring, the five boundary colors satisfy the cubic parity condition: one color appears 3 times and the other two appear once each, so the boundary pattern is of type:

[
(3,1,1).
]

But for a 5-regular 5-pole with 5 dangling ports, in any proper 5-edge-coloring, parity implies that all five ports must receive five distinct colors:

[
(1,1,1,1,1).
]

Therefore the gadget cannot directly simulate the three colors. We need to search for a gadget whose **port-color permutations encode exactly three useful macrostates**, corresponding to the three colors of a cubic edge-coloring.

The goal is not immediately to prove the full theorem, but to build infrastructure for finding and testing such gadgets.

---

# Main goal

Implement a computational search for candidate **5-regular 5-port gadgets** with the following properties:

1. Internal vertices all have degree 5 after accounting for ports.
2. The gadget has exactly 5 ports.
3. It is internally robust: no small edge cuts of size less than 5, except trivial cuts involving isolated port attachments if relevant.
4. The set of all possible proper 5-edge-colorings induces a restricted set of boundary signatures on the 5 ports.
5. Boundary signatures should be classified up to global permutation of the five colors.
6. We want to find gadgets whose boundary signatures can be partitioned into exactly 3 meaningful equivalence classes / macrostates, or are close to that.

---

# Step 1: Inspect the project

First inspect the repository structure. Find existing code for:

* graph representation,
* multigraph generation,
* regular graph generation,
* edge coloring,
* SAT/ILP/CP-SAT encodings,
* nauty/geng/multig integration,
* canonical labeling / isomorphism rejection,
* any existing snark or edge-colorability search code.

Reuse the existing infrastructure as much as possible. Do not rewrite large parts unnecessarily.

After inspecting, summarize briefly in comments or in a new `NOTES_gadget_search.md` file which existing components are reused.

---

# Step 2: Define gadget representation

Implement a representation for a 5-port gadget.

A gadget consists of:

* internal vertices (0,\dots,n-1),
* internal edges between internal vertices,
* five ports, each attached to an internal vertex.

The degree condition is:

[
\deg_{\text{internal}}(v) + #\text{ports attached to }v = 5
]

for every internal vertex (v).

Allow multiedges only if the existing project supports them cleanly. Otherwise start with simple internal graphs, but keep the interface abstract enough that multigraph support can be added.

Create a type/class similar to:

```cpp
struct Gadget5Pole {
    int n;
    vector<pair<int,int>> internal_edges;
    array<int,5> port_vertex;
};
```

or the equivalent in the project’s language.

Add validation functions:

```text
validate_degree_5(gadget)
validate_connected(gadget)
validate_no_loops(gadget)
validate_port_count_5(gadget)
```

Optional but useful:

```text
validate_simple_internal(gadget)
validate_multigraph_internal(gadget)
```

---

# Step 3: Generate candidate gadgets

Implement a candidate generator.

Input parameters:

```text
n_min
n_max
allow_multiedges
max_parallel_edges
require_connected
require_internal_cut_condition
```

For each number of internal vertices (n), generate internal graphs plus port placements satisfying:

[
\deg_{\text{internal}}(v) \le 5
]

and total missing degree equals 5:

[
\sum_v (5-\deg_{\text{internal}}(v)) = 5.
]

Then distribute exactly 5 ports so that each vertex receives exactly its missing degree:

[
#\text{ports at }v = 5-\deg_{\text{internal}}(v).
]

Important observation:

[
\sum_v \deg_{\text{internal}}(v) = 5n - 5.
]

So (5n-5) must be even. Therefore (n) must be odd.

Only search odd (n).

Start with small odd values:

```text
n = 5, 7, 9, 11, 13
```

Use canonical rejection if available. If nauty is available in the project, use it to avoid generating isomorphic duplicates.

If canonical rejection is hard, implement a first version without it but keep the search small.

---

# Step 4: Edge-coloring solver for a gadget

Implement or reuse a proper 5-edge-coloring solver.

For a gadget, color both:

* internal edges,
* five ports.

Colors are:

```text
0, 1, 2, 3, 4
```

Constraint:

At every internal vertex, the incident internal edges and incident ports must all have distinct colors.

Since each internal vertex has total degree 5, this means each vertex sees all five colors exactly once.

The solver should be able to do two things:

### A. Decide colorability

```text
bool is_5_edge_colorable(gadget)
```

### B. Enumerate boundary signatures

```text
set<array<int,5>> enumerate_port_color_signatures(gadget)
```

The port signature is:

```text
[color(port0), color(port1), color(port2), color(port3), color(port4)]
```

Because of parity, every valid signature should be a permutation of:

```text
[0,1,2,3,4]
```

Assert this in debug mode. If a colorable gadget gives a repeated port color, something is wrong.

Implementation options:

* Use existing backtracking edge-coloring code if present.
* Otherwise implement a simple DFS with pruning.
* Or encode as SAT/ILP if the project already has a solver.

For small gadgets, DFS should be enough.

Suggested DFS:

1. Order edges by constraint tightness.
2. Assign colors one edge at a time.
3. Maintain used colors at each internal vertex.
4. For ports, treat them as edges incident to one internal vertex and one external dummy endpoint with no constraint.
5. Enumerate all possible port signatures, not necessarily all full colorings. Stop exploring a branch once the boundary signature is already found if possible.

---

# Step 5: Canonicalize boundary signatures

Two signatures that differ only by global color permutation should be considered equivalent.

For example:

```text
[2,4,0,1,3]
```

and

```text
[0,1,2,3,4]
```

are equivalent under color renaming if only absolute colors matter.

But we also care about the **relative permutation pattern of ports**.

Since every valid signature is a permutation of five distinct colors, canonicalize a signature by renaming colors in order of first appearance.

Example:

```text
[3,1,4,0,2] -> [0,1,2,3,4]
```

This alone collapses every permutation to the same form, so it is not enough if port positions matter.

Instead, implement two levels of canonicalization:

### Level 1: Color-renaming canonicalization only

Given a set of signatures (S), canonicalize the whole set under all (5!) global color permutations. Choose lexicographically minimal representation.

```text
canonical_signature_set_under_color_permutation(S)
```

This preserves port positions.

### Level 2: Color and port symmetries

Optionally canonicalize also under automorphisms of the five ports if the gadget has port symmetries.

For now, do not quotient by arbitrary port permutations unless explicitly testing symmetry. Port positions matter for composition.

---

# Step 6: Score candidate gadgets

For each gadget, compute:

```text
num_signatures = number of distinct port signatures
canonical_signature_set
automorphism info if available
internal edge connectivity score
```

The complete unrestricted behavior would allow all (5! = 120) port permutations.

We are interested in gadgets with a **small restricted subset** of allowed port permutations.

Prefer candidates with:

```text
num_signatures small
num_signatures divisible by 3, especially 3, 6, 12, 18, 24, 30
good internal edge-connectivity
few/no nontrivial cuts below 5
not obviously decomposable
```

Output a ranked list.

Suggested scoring:

```text
score = 1000 * num_signatures
        + 100 * number_of_small_cuts_below_5
        + n
```

Lower is better.

Also record whether the signature set can be partitioned into 3 equal-sized classes by a natural invariant.

Possible invariants to test:

* position of a chosen color,
* cyclic order class of the permutation,
* parity of permutation,
* membership in cosets of a subgroup of (S_5),
* stabilizer/orbit structure under the gadget’s port automorphism group.

---

# Step 7: Test whether signatures can encode three states

For each promising gadget, try to infer whether its boundary signatures support exactly three macrostates.

Implement a helper:

```text
analyze_three_state_encoding(signature_set)
```

This should try several partitions of the allowed signatures into 3 classes and test whether the classes are stable under global color permutation.

Useful group-theoretic view:

* The full color group is (S_5).
* Boundary signatures are permutations in (S_5).
* A gadget’s allowed signatures form a subset (A \subseteq S_5).
* Global color permutation acts by left multiplication.
* Port relabeling acts by right multiplication.

Search for subsets/classes that behave like three abstract colors.

For now, implement heuristic checks and print diagnostics. Do not over-engineer the proof.

Diagnostics to output:

```text
allowed permutations A
size of A
stabilizer size
orbits under candidate port symmetries
possible partitions into 3 equal classes
```

---

# Step 8: Edge-connectivity checker for gadget

Implement a cut checker for the gadget as a 5-pole.

For every nonempty proper subset (U) of internal vertices, compute:

```text
cut_size = number of internal edges crossing U to V\U
          + number of ports attached to vertices in U
```

This is the size of the cut separating (U) from the outside world.

Reject gadgets where there exists a nontrivial (U) with:

```text
cut_size < 5
```

However, be careful with singleton vertices. Since every vertex has total degree 5, singleton cuts have size exactly 5 and are fine.

Function:

```text
int min_gadget_cut(gadget)
```

and:

```text
bool is_internally_5_edge_connected(gadget)
```

For small (n), brute force over all subsets is fine.

---

# Step 9: Save output artifacts

For every promising gadget, save:

1. Graph data in a machine-readable format, for example JSON:

```json
{
  "n": 9,
  "internal_edges": [[0,1],[0,2],...],
  "ports": [0,3,4,7,8],
  "num_signatures": 12,
  "signatures": [[0,1,2,3,4], ...],
  "min_cut": 5
}
```

2. A human-readable text summary.

3. Optional DOT file for visualization:

```text
gadget_n9_candidate3.dot
```

Ports should be shown as dangling leaves or labeled half-edges:

```text
p0, p1, p2, p3, p4
```

---

# Step 10: Add a command-line interface

Add a CLI command such as:

```bash
./gadget_search --n-min 5 --n-max 13 --simple --require-cut-5 --max-results 50
```

or, if the project uses Python:

```bash
python gadget_search.py --n-min 5 --n-max 13 --simple --require-cut-5 --max-results 50
```

Expected output:

```text
Searching n=5...
Searching n=7...
Searching n=9...
Candidate #1:
  n = 9
  internal edges = 20
  port vertices = [0,2,4,6,8]
  min cut = 5
  allowed signatures = 12
  score = 12009
  saved to output/gadgets/candidate_001.json
```

---

# Step 11: Add tests

Add unit tests for:

### Degree validation

Construct small artificial gadgets and check that invalid degrees are rejected.

### Parity lemma

For every colorable generated 5-pole, every valid port signature must contain all five colors exactly once.

### Boundary enumeration

Create a trivial known gadget if possible and test that signatures are enumerated correctly.

### Cut checker

Test that a gadget with a known small cut is rejected.

### Serialization

Test save/load of candidate gadgets.

---

# Step 12: Optional second phase — composition test

After finding candidate gadgets, implement a small experimental replacement test.

Given a cubic graph (S) and a choice of disjoint 3-vertex paths, replace each path by a gadget candidate and test whether the resulting graph is 5-edge-colorable.

CLI example:

```bash
./test_replacement --snark petersen --gadget output/gadgets/candidate_001.json
```

For now this can be experimental. The first priority is finding gadgets with restricted boundary behavior.

---

# Important implementation notes

Do not assume that a small number of boundary signatures is automatically enough. A useful gadget must allow a projection from 5-edge-colorings to 3-edge-coloring states.

Therefore, output enough information to let us manually inspect the signatures.

When printing signatures, use port order exactly as given. Port positions matter.

Use deterministic ordering and deterministic random seeds where applicable.

Avoid huge searches initially. Start small and make the search restartable.

---

# Deliverables

Please implement:

1. `Gadget5Pole` representation.
2. Gadget validation.
3. Candidate generation for small odd (n).
4. Proper 5-edge-coloring boundary signature enumeration.
5. Boundary signature canonicalization under global color permutation.
6. Internal 5-edge-connectivity checker.
7. Candidate scoring and ranking.
8. JSON/DOT export for promising candidates.
9. CLI command for running the search.
10. Basic tests.

Also add a short documentation file:

```text
NOTES_gadget_search.md
```

explaining:

* how to run the search,
* how boundary signatures are represented,
* what the parity check means,
* how to interpret the output candidates.

Focus on correctness and inspectability first, performance second.
