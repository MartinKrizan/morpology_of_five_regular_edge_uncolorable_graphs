#!/usr/bin/env python3
import argparse
import statistics
import sys
import time
from pathlib import Path
from ortools.sat.python import cp_model


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from morphology_graphs.core.g_from_file import read_graphs_from_file
from morphology_graphs.core.is_colorable import is_edge_k_colorable


RUNS_PER_GRAPH = 3
COLOR_COUNTS = (5, 6)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark edge k-colorability checks for graph6 inputs."
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to a file containing one graph6 graph per line.",
    )
    return parser.parse_args()


def timed_colorability_check(graph, k, solver):
    start = time.perf_counter()
    colorable, _ = is_edge_k_colorable(graph, k, return_assignment=False, verify_assignment=False, solver=solver)
    return colorable, time.perf_counter() - start


def benchmark_graph(graph, k, solver):
    measurements = []
    expected_colorable = None

    for _ in range(RUNS_PER_GRAPH):
        colorable, elapsed_s = timed_colorability_check(graph, k, solver)
        if expected_colorable is None:
            expected_colorable = colorable
        elif colorable != expected_colorable:
            raise RuntimeError(f"inconsistent colorability result for k={k}")
        measurements.append(elapsed_s)

    return expected_colorable, min(measurements)


def print_summary(k, best_times, colorable_count, total):
    if not best_times:
        print(f"k={k}: no graphs")
        return

    print(f"python CPsat - colorable:{colorable_count}/{total}")
    print(f" {max(best_times):.9f},{min(best_times):.9f},{statistics.fmean(best_times):.9f}, {sum(best_times):.9f}")


def main():
    args = parse_args()
    source = Path(args.source)
    if not source.exists():
        print(f"Error: File {source} not found.", file=sys.stderr)
        return 1

    best_times_by_k = {k: [] for k in COLOR_COUNTS}
    colorable_counts_by_k = {k: 0 for k in COLOR_COUNTS}

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.num_search_workers = 1

    for graph in read_graphs_from_file(source):
        for k in COLOR_COUNTS:
            colorable, best_time = benchmark_graph(graph, k, solver)
            best_times_by_k[k].append(best_time)
            if colorable:
                colorable_counts_by_k[k] += 1

    best_times = []
    col =0

    for k in COLOR_COUNTS:
        best_times = best_times + best_times_by_k[k]
        col = col + colorable_counts_by_k[k]


    print_summary(k, best_times, col, len(best_times))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
