# Edge-Coloring Solver Benchmarks

This directory contains benchmark tooling and historical timing results for
edge-coloring solvers on 5-regular graph instances.

Benchmark graph instances are stored in
[`../../data/benchmark`](../../data/benchmark).

## Method

Each graph was tested three times for `k = 5` and `k = 6`. For each graph and
color count, the best result, meaning the lowest runtime, was used in the final
comparison.

The historical results are in [`results.txt`](results.txt). Each line records a
graph file and solver, followed by four timing values:

```text
max_time min_time avg_time total_time
```

## Solvers

For `kissat`, `tassat`, `clasp`, and `cadical`, the benchmark scripts from
`ba-graph/benchmark/colouring` were used.

For the Python CP-SAT implementation, use:

```sh
./bench_all_edge.sh
```

The recorded CP-SAT results use `cp_model.number_of_workers = 1`. Increasing
the worker count can significantly improve performance on larger graphs.
