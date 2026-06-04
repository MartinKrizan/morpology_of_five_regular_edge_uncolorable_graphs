#!/usr/bin/env python3
"""
Benchmark: compare is_edge_k_colorable vs is_multigraph_edge_k_colorable
on all 16-vertex 5-regular uncolorable graphs from data/uncol/16v/uncol_16.g6.

Verifies that every graph is reported as uncolorable by both functions.
"""

import os
import sys
import time
import networkx as nx

# Add parent directory to path so we can import functions_d
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from functions_d.g_from_file import read_graphs_from_file
from functions_d.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable


DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "uncol", "16v", "uncol_16.g6"
)
K = 5  # edge-coloring with 5 colors (these are 5-regular, so 5-edge-colorable = class 1)


def main():
    data_path = os.path.normpath(DATA_FILE)
    if not os.path.exists(data_path):
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    # Load all graphs upfront so IO doesn't affect timing
    print(f"Loading graphs from {data_path} ...")
    graphs = list(read_graphs_from_file(data_path))
    n_graphs = len(graphs)
    print(f"Loaded {n_graphs} graphs (16 vertices each)\n")

    # ── Benchmark is_edge_k_colorable (simple graph version) ─────────────
    print(f"{'='*60}")
    print(f"  is_edge_k_colorable  (k={K})")
    print(f"{'='*60}")

    simple_failures = []
    t_start = time.perf_counter()

    for i, G in enumerate(graphs, 1):
        colorable, _ = is_edge_k_colorable(G, K)
        if colorable:
            simple_failures.append(i)
        if i % 100 == 0 or i == n_graphs:
            elapsed = time.perf_counter() - t_start
            print(f"  [{i:>5}/{n_graphs}]  elapsed {elapsed:8.2f}s", end="\r")

    t_simple = time.perf_counter() - t_start
    print()  # newline after \r

    if simple_failures:
        print(f"  ❌  FAIL: {len(simple_failures)} graph(s) reported as colorable!")
        print(f"       indices (1-based): {simple_failures[:20]}{'...' if len(simple_failures) > 20 else ''}")
    else:
        print(f"  ✅  All {n_graphs} graphs confirmed UNCOLORABLE")

    print(f"  ⏱  Total time : {t_simple:.3f} s")
    print(f"  ⏱  Per graph  : {t_simple / n_graphs * 1000:.2f} ms")
    print()

    # ── Benchmark is_multigraph_edge_k_colorable (multigraph version) ────
    print(f"{'='*60}")
    print(f"  is_multigraph_edge_k_colorable  (k={K})")
    print(f"{'='*60}")

    # Convert each simple graph to a MultiGraph for the multigraph function
    multi_failures = []
    t_start = time.perf_counter()

    for i, G in enumerate(graphs, 1):
        MG = nx.MultiGraph(G)
        colorable, _ = is_multigraph_edge_k_colorable(MG, K)
        if colorable:
            multi_failures.append(i)
        if i % 100 == 0 or i == n_graphs:
            elapsed = time.perf_counter() - t_start
            print(f"  [{i:>5}/{n_graphs}]  elapsed {elapsed:8.2f}s", end="\r")

    t_multi = time.perf_counter() - t_start
    print()

    if multi_failures:
        print(f"  ❌  FAIL: {len(multi_failures)} graph(s) reported as colorable!")
        print(f"       indices (1-based): {multi_failures[:20]}{'...' if len(multi_failures) > 20 else ''}")
    else:
        print(f"  ✅  All {n_graphs} graphs confirmed UNCOLORABLE")

    print(f"  ⏱  Total time : {t_multi:.3f} s")
    print(f"  ⏱  Per graph  : {t_multi / n_graphs * 1000:.2f} ms")
    print()

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Graphs tested       : {n_graphs}")
    print(f"  is_edge_k_colorable : {t_simple:8.3f} s  ({t_simple / n_graphs * 1000:.2f} ms/graph)")
    print(f"  is_multigraph_edge  : {t_multi:8.3f} s  ({t_multi / n_graphs * 1000:.2f} ms/graph)")

    if t_simple > 0 and t_multi > 0:
        ratio = t_multi / t_simple
        faster = "is_edge_k_colorable" if ratio > 1 else "is_multigraph_edge_k_colorable"
        print(f"  Ratio (multi/simple): {ratio:.2f}x  →  {faster} is faster")

    all_ok = not simple_failures and not multi_failures
    print()
    if all_ok:
        print("  ✅  All correctness checks PASSED")
    else:
        print("  ❌  Some correctness checks FAILED")
    print()


if __name__ == "__main__":
    main()
