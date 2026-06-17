# Gadget Search

The project provides an installed Python command for searching 5-pole gadgets:

```sh
gadget-search --n-min 5 --n-max 9 --require-cut-5 --max-results 50
```

There is also a weaker classification command for grouping generated poles by
pairwise port-color constraints:

```sh
gadget-categorize --ports 5 --n-min 5 --n-max 13
```

In Docker, after rebuilding the image or reinstalling the editable package:

```sh
docker compose run --rm python gadget-search --n-min 5 --n-max 9 --require-cut-5
docker compose run --rm python gadget-categorize --ports 5 --n-min 5 --n-max 13
```

## Generator

The current implementation uses nauty `geng` directly. There is no pure Python
candidate-generation fallback.

For each odd internal order `n`, the command fixes the number of internal edges
to:

```text
(5n - 5) / 2
```

By default it calls `geng` with connected simple graphs and internal degree
bounds equivalent to:

```sh
geng -q -c -d4 -D5 n E:E
```

With these defaults, exactly five internal vertices have degree 4, and each
gets one port. Port labels `p0..p4` are kept meaningful because port order is
part of the boundary signature.

The generator rejects port placements that are equivalent by an internal
automorphism while preserving the five port labels. Use `--all-port-placements`
to disable that rejection.

For `gadget-categorize`, ports are inferred from degree deficits in sorted
vertex order. With the default `--geng-min-degree 4 --geng-max-degree 5`, each
port is attached to one degree-4 vertex. The graph6 output alone is therefore
enough to reconstruct the ports.

## Reused Components

The implementation follows the existing Python package layout under
`python/morphology_graphs`. It reuses the dependencies declared in
`python/pyproject.toml`: NetworkX for graph representation and isomorphism
checks, OR-Tools CP-SAT for edge-coloring constraints, and nauty command-line
tools from the Docker image for graph generation.

The CLI is exposed through the same `[project.scripts]` mechanism as `chcol`,
`filter-uncol`, and `generate-overfull`.

## Gadget Representation

`Gadget5Pole` lives in `morphology_graphs.core.gadget`.

A gadget stores:

```text
n
internal_edges
port_vertices
```

The degree condition is:

```text
internal_degree(v) + number_of_ports_attached_to(v) = 5
```

Validation helpers check port count, loops, simple internal edges, connectivity,
and the 5-regular degree condition after ports are included.

## Boundary Signatures

A boundary signature is the ordered list of colors on ports:

```text
[color(p0), color(p1), color(p2), color(p3), color(p4)]
```

Colors are integers `0..4`. The code asserts the parity consequence expected
for a colorable 5-pole: every valid port signature must be a permutation of all
five colors.

Signature enumeration uses OR-Tools CP-SAT. Instead of DFS over all full
edge-colorings, it repeatedly asks CP-SAT for one coloring, records the port
signature, and adds a blocking clause forbidding only that boundary signature.
This enumerates distinct boundary behavior without intentionally enumerating
all internal colorings that produce the same boundary.

## Canonical Signatures

`canonical_signature_set_under_color_permutation` canonicalizes the whole set of
allowed signatures under all global color permutations. Port positions are not
quotiented out.

This is the level-1 canonicalization from the original task. Arbitrary port
permutations are not used because port positions matter for composition.

## Cut Condition

For every nonempty proper subset `U` of internal vertices, the gadget cut size
is:

```text
internal edges crossing U to V-U + ports attached to vertices in U
```

`min_gadget_cut` brute-forces all subsets for small gadgets.
`--require-cut-5` rejects any candidate whose minimum such cut is below 5.

## Output

Candidates are ranked by:

```text
1000 * number_of_signatures + 100 * small_cut_count + n
```

Lower is better. If boundary-signature enumeration is incomplete because a
limit or timeout was reached, the score receives a large penalty so partial
results do not silently outrank completed candidates. The command writes JSON,
text, and DOT files under `output/gadgets` by default.

The JSON contains the raw gadget, signatures, canonical signature set, cut
data, score, and basic diagnostics such as divisibility by 3, parity counts,
and color-position counts.

## Category Output

`gadget-categorize` writes one `.g6` file per category under
`output/gadget_categories` by default. These files intentionally contain only
plain graph6 lines and no comments or metadata.

For every unordered port pair `(Pi, Pj)`, the command asks two CP-SAT decision
questions:

```text
is there a coloring with Pi = Pj?
is there a coloring with Pi != Pj?
```

The pair is counted as:

```text
forced_same       same possible, different impossible
forced_different  same impossible, different possible
flexible          both possible
blocked           neither possible
```

The category filename records the four counts, for example:

```text
n9p5_s0d10f0b0.g6
```

If CP-SAT returns `UNKNOWN` for a pair constraint, the command raises an error
instead of writing the graph into a possibly wrong category.
