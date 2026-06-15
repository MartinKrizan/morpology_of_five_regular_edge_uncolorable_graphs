# Benchmark of edge-coloring solvers for 5r graphs

Performance was measured on graphs from [benchmark directory](../../data/benchmark).

Each graph was tested 3 times for k=5 and k=6. For each graph and k, best result(lowest time) was used for final results.

In [results file](results.txt) are those results. For each graph file and solver, there is line with 4 numbers: max time, min time, avg time and sum of times.

For kissat, tassat, clasp and cadical solvers benchmarking scripts from ba-graph/benchmark/colouring were used.

For python-cpsat [bench_all_edge.sh](bench_all_edge.sh) was used. All results are with cp_model.number_of_workes set to 1. For graphs with large number of vertices, increasing this number improves preformance significantly.