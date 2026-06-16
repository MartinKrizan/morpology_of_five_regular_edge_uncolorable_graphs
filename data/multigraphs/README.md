# 5-Regular Multigraph Lists

This directory contains edge-uncolorable 5-regular multigraphs.

The multigraphs were generated with `nauty-geng` and `nauty-multig`, following
the same general approach as the BA graph generation tooling:
<https://github.com/ba-graph-research/ba-graph/blob/master/tools/generation/multigraphs/generateMultigraphs_d.sh>.

To keep the lists manageable and relevant to the current experiments, these
files only include multigraphs with maximum edge multiplicity 2. Higher
multiplicity implies the presence of an edge cut of size at most 4.

Unless stated otherwise, files use nauty simple text output format.

## Files

- [`uncol_8_m2_all_small.txt`](uncol_8_m2_all_small.txt) - 21 uncolorable
  multigraphs on 8 vertices.
- [`uncol_10_m2_all_small.txt`](uncol_10_m2_all_small.txt) - 1,745
  uncolorable multigraphs on 10 vertices.
- [`uncol_12_m2_all_small.txt`](uncol_12_m2_all_small.txt) - 275,302
  uncolorable multigraphs on 12 vertices.
- [`high_conn_12_uncol_m.txt`](high_conn_12_uncol_m.txt) - 3 graphs obtained
  from the 12-vertex list by keeping cases with edge connectivity greater than
  3 and converting them to simple graph6 format.

## Filtering

Colorability was checked with the Python filter:

```sh
docker compose run --rm python filter-uncol < data/multigraphs/uncol_8_m2_all_small.txt
```

The high-connectivity conversion uses:

```sh
docker compose run --rm python filter-low-con < data/multigraphs/uncol_12_m2_all_small.txt
```
