# Research Notes

This file collects research observations that are useful but too exploratory
for the root README.

## Uncolorable Graphs on 16 Vertices

All known 5-regular edge-uncolorable simple graphs on 16 vertices are listed in
[`../data/uncol/16v/uncol_16.g6`](../data/uncol/16v/uncol_16.g6).

All of them have edge connectivity less than 4. After splitting such a graph by
a minimum cut, one component is always uncolorable. For almost all of those
components, uncolorability follows from the component being overfull.

Open note: inspect the remaining cases whose uncolorable component is not
overfull.

Example recorded case:

```text
Graph: O~zPw[@?O@_E?J?J?BW?n
Uncolorable part: G~zPw[
Critical part: F~zPw
```

## Odd Component Cut Observation

Observation: a 5-regular graph is not 5-edge-colorable if it has a cut of size
less than 5 whose removal leaves an odd-order component.

Proof. Let `G` be a 5-regular graph and let `S` be a cut of size `C < 5`.
Remove the cut edges and choose one odd-order component `H`. Write `n = |V(H)|`.
The sum of degrees of vertices of `H` in the original graph is `5n`. Exactly
`C` of those degree contributions go to cut edges, so the number of edges inside
`H` is:

```math
|E(H)| = \frac{5n - C}{2}
```

Because `n` is odd, every matching in `H` has at most `floor(n / 2)` edges. A
proper edge coloring with 5 colors decomposes the edges into 5 matchings, so it
can cover at most:

```math
5 \left\lfloor \frac{n}{2} \right\rfloor = \frac{5(n - 1)}{2}
```

edges of `H`. But `C < 5` gives:

```math
|E(H)| = \frac{5n - C}{2} > \frac{5(n - 1)}{2}
```

Therefore `H` cannot be edge-colored with 5 colors. Any 5-edge-coloring of `G`
would restrict to a 5-edge-coloring of `H`, so `G` is also not 5-edge-colorable.

Equivalently, the odd component is overfull with respect to 5 colors. Since
`Delta(H) <= 5`, it is also overfull in the usual sense:

```math
|E(H)| > \Delta(H) \left\lfloor \frac{|V(H)|}{2} \right\rfloor
```

## Generating Larger Uncolorable Graphs

One construction direction is to generate overfull graphs with maximum degree at
most 5 on an odd number of vertices, then add vertices and edges until the graph
is 5-regular.

The command `generate-overfull` generates overfull candidates with maximum degree
at most 5 on odd vertex counts.

Open task: add or document a script that completes such candidates to
5-regular graphs.

## 4-Edge-Connected Examples

There is one known 4-edge-connected uncolorable 5-regular graph recorded at
<https://houseofgraphs.org/graphs/50543>.

Open task: investigate whether it can be used as a base construction for more
4-edge-connected examples.

## Multigraph to Simple 5-Regular Graphs

Open task: document the conversion from 5-regular multigraphs to simple
5-regular graphs, including the role of edge connectivity filters.
