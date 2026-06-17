# Uncolorable Graphs on up to 16 Vertices

Non-isomorphic simple 5-regular edge-uncolorable graph:

| Number of Vertices | Count | List |
| ------------------ | ----- | ---- |
| < 14               | 0     | -    |
| 14                 | 25    | [`../data/uncol/14v/uncol_14.g6`](../data/uncol/14v/uncol_14.g6)    |
| 16                 | 2882    | [`../data/uncol/16v/uncol_16.g6`](../data/uncol/16v/uncol_16.g6)    |



All of them contains cut with size less than 4 that splits graph into two components of odd size. After splitting a graph by
such cut, one component is always uncolorable. For all of those
components, uncolorability follows from the component being overfull.

# Odd Component Cut Observation

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

# Generating Large Uncolorable Graphs

One construction direction is to generate overfull graphs with maximum degree at
most 5 on an odd number of vertices.  This graph will be class 2. It can be easily extended to 5-regular but adding filler vertices and edges. This only generates 3 edge-connected graphs. Those are not interestring for colorability research but useful for testing and measuring edge-colorability algorithms.

The command `generate-overfull` generates overfull candidates with maximum degree 5 on odd vertex counts.

# Multigraph to Simple 5-Regular Graphs

This construction transforms 5-regular loopless multigraph to simple graph preserving its edge-connectivity and edge-colorability. 
It is implemented in [replace_multiedge_vertices_with_k5](../python/morphology_graphs/core/k5_substitution.py) function.

## Steps:

Choose a vertex `v` incident with a parallel edge. Since the graph is
5-regular, the five edges incident with `v` can be written as:

```math
e_i = vx_i, \qquad i = 1,\ldots,5
```

where some of the vertices `x_i` may be equal. Delete `v`, add five new
vertices $b_1,\ldots,b_5$ inducing a copy of `K5`, and add the five external
edges:

```math
b_i x_i, \qquad i = 1,\ldots,5.
```

Repeat this step while parallel edges remain.

## Regularity and Simplicity

**Regularity:** Each new vertex $b_i$ has 4 neighbors inside the $K_5$ block and 1 external neighbor $x_i$, preserving its degree at 5. Every old vertex $x_i$ maintains its original degree because the deleted edge $vx_i$ is replaced by exactly one edge $b_i x_i$.

**Simplicity:** The internal edges of $K_5$ are simple by definition. If $v$ shared parallel edges with a neighbor (e.g., $x_1 = x_2$), the replacement yields edges $b_1 x_1$ and $b_2 x_1$. Because $b_1 \neq b_2$, these edges are not parallel. Thus, the operation introduces no new parallel edges and strictly reduces the number of multi-edges.

## Edge-Connectivity

Let `G'` be obtained from `G` by one substitution, and let `B` be the inserted
`K5` block. Cuts are counted with edge multiplicity. Every cut of `G` gives a
cut of `G'` of the same size by putting all of `B` on the side formerly
containing `v`. Hence:

```math
\lambda(G') \leq \lambda(G)
```

For the reverse inequality, take any nontrivial cut of `G'`. If the cut does
not split `B`, then contracting `B` back to `v` gives a cut of `G` of the same
size.

Now suppose the cut splits `B`. Let the smaller part of the split contain `s`
vertices of `B`, where $`1 <= s <= 2`$.  

If this smaller part contains no vertices
outside `B`, then the cut has size at least:

```math
s(5-s) + s \geq 5
```

This is at least $`\lambda(G)`$, because every 5-regular graph has
edge-connectivity at most `5`.

Otherwise, move those `s` block vertices to the other side of the cut. This
removes `s(5-s)` internal crossing edges of the `K5` block and can change at
most `s` external edges, since each block vertex has exactly one external edge.
Because:

```math
s(5-s) \geq s
```

the cut size does not increase. After the move, `B` lies entirely on one side,
so contracting `B` back to `v` gives a cut of `G` no larger than the original
cut of `G'`. Therefore:

```math
\lambda(G') \geq \lambda(G)
```

and so:

```math
\lambda(G') = \lambda(G)
```

## Edge-Colorability

```math
G \text{ is 5-edge-colorable } \Longleftrightarrow
G' \text{ is 5-edge-colorable}.
```

$(\Rightarrow)$ Suppose $G$ has a proper 5-edge-coloring. The 5 edges incident with $v$ must receive 5 distinct colors. Assign these identical colors to the 5 external edges of $B$. Because $K_5$ can be 5-edge-colored such that each vertex is missing exactly one unique color, we can permute the internal colors of $B$ so that vertex $b_i$ misses the exact color assigned to its external edge $b_i x_i$. This successfully extends the coloring to $G'$.

$(\Leftarrow)$ Suppose $G'$ has a proper 5-edge-coloring. Since $K_5$ contains 10 edges, any 5-edge-coloring forces each color class to be a matching of size exactly 2. This means every color is missing at exactly one vertex of $B$. Consequently, the external edge at each vertex must use that missing color. The 5 external edges therefore receive 5 distinct colors. Contracting $B$ back to $v$ yields a valid 5-edge-coloring of $G$.

By induction, the repeated `K5` substitution preserves both edge-connectivity
and 5-edge-colorability. In particular, it preserves uncolorability.
