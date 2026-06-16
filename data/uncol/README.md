# 5-Regular Edge-Uncolorable Simple Graphs

This directory contains known simple 5-regular graphs that are not
edge-colorable with 5 colors.

The files are stored in graph6 format, one graph per line.

## Files

- [`14v/uncol_14.g6`](14v/uncol_14.g6) - 25 uncolorable graphs on 14 vertices.
- [`16v/uncol_16.g6`](16v/uncol_16.g6) - 2,882 uncolorable graphs on 16 vertices.

No uncolorable 5-regular simple graphs were found on fewer than 14 vertices in
the generated data.

## Provenance

The full lists of 5-regular graphs were generated with `genreg` using
[`../../scripts/generator/generate_5_reg.sh`](../../scripts/generator/generate_5_reg.sh).

The generated graphs were then filtered for edge colorability using the legacy
C++ checker in
[`../../scripts/test_coloring/test_col.cpp`](../../scripts/test_coloring/test_col.cpp).

Newer workflows can also use the Python command:

```sh
docker compose run --rm python filter-uncol < path/to/graphs.g6
```
