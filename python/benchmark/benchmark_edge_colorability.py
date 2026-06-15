#!/usr/bin/env python3
import argparse
import statistics
import sys
import time
from pathlib import Path


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


def timed_colorability_check(graph, k):
    start = time.perf_counter()
    colorable, _ = is_edge_k_colorable(graph, k, return_assignment=False)
    return colorable, time.perf_counter() - start


def benchmark_graph(graph, k):
    measurements = []
    expected_colorable = None

    for _ in range(RUNS_PER_GRAPH):
        colorable, elapsed_s = timed_colorability_check(graph, k)
        if expected_colorable is None:
            expected_colorable = colorable
        elif colorable != expected_colorable:
            raise RuntimeError(f"inconsistent colorability result for k={k}")
        measurements.append(elapsed_s)

    return expected_colorable, min(measurements)


def print_summary(k, best_times, colorable_count):
    if not best_times:
        print(f"k={k}: no graphs")
        return

    print(f"k={k}")
    print(f"  graphs: {len(best_times)}")
    print(f"  colorable: {colorable_count}")
    print(f"  uncolorable: {len(best_times) - colorable_count}")
    print(f"  min: {min(best_times):.6f}s")
    print(f"  max: {max(best_times):.6f}s")
    print(f"  avg: {statistics.fmean(best_times):.6f}s")
    print(f"  total: {sum(best_times):.6f}s")


def main():
    args = parse_args()
    source = Path(args.source)
    if not source.exists():
        print(f"Error: File {source} not found.", file=sys.stderr)
        return 1

    best_times_by_k = {k: [] for k in COLOR_COUNTS}
    colorable_counts_by_k = {k: 0 for k in COLOR_COUNTS}

    for graph in read_graphs_from_file(source):
        for k in COLOR_COUNTS:
            colorable, best_time = benchmark_graph(graph, k)
            best_times_by_k[k].append(best_time)
            if colorable:
                colorable_counts_by_k[k] += 1

    for k in COLOR_COUNTS:
        print_summary(k, best_times_by_k[k], colorable_counts_by_k[k])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
