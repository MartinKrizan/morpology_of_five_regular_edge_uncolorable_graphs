#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from morphology_graphs.core.gadget import (
    categorize_port_pairs,
    deficits_from_graph,
    expected_internal_edge_count,
    graph_to_plain_graph6,
    iter_geng_graphs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate P-port 5-regular poles with nauty geng and group them by "
            "forced same/different port-color pair counts."
        )
    )
    parser.add_argument("--ports", "-p", type=int, required=True, help="Number of ports.")
    parser.add_argument("--n-min", type=int, required=True, help="Smallest internal order to search.")
    parser.add_argument("--n-max", type=int, required=True, help="Largest internal order to search.")
    parser.add_argument("--geng", default="geng", help="Path to nauty geng executable.")
    parser.add_argument(
        "--geng-min-degree",
        type=int,
        default=4,
        help="Minimum internal degree passed to geng. Default gives at most one port per vertex.",
    )
    parser.add_argument(
        "--geng-max-degree",
        type=int,
        default=5,
        help="Maximum internal degree passed to geng.",
    )
    parser.add_argument(
        "--allow-disconnected",
        action="store_true",
        help="Do not pass -c to geng.",
    )
    parser.add_argument(
        "--solver-time-limit",
        type=float,
        default=10.0,
        help="CP-SAT time limit per same/different decision, in seconds.",
    )
    parser.add_argument(
        "--max-graphs",
        type=int,
        default=None,
        help="Stop after categorizing this many generated graphs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/gadget_categories"),
        help="Directory for per-category .g6 files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    category_counts: Counter[str] = Counter()
    initialized_categories: set[str] = set()
    processed = 0

    for n in range(args.n_min, args.n_max + 1):
        try:
            edge_count = expected_internal_edge_count(n, args.ports)
        except ValueError:
            continue

        print(f"Searching n={n}, ports={args.ports}, internal edges={edge_count}...")
        for graph in iter_geng_graphs(
            n,
            ports=args.ports,
            geng_path=args.geng,
            require_connected=not args.allow_disconnected,
            min_degree=args.geng_min_degree,
            max_degree=args.geng_max_degree,
        ):
            port_vertices = tuple(deficits_from_graph(graph, args.ports))
            category = categorize_port_pairs(
                graph,
                port_vertices,
                time_limit_s=args.solver_time_limit,
            )
            category_name = f"n{n}p{args.ports}_{category.file_stem()}"
            category_path = args.output_dir / f"{category_name}.g6"
            open_mode = "a" if category_name in initialized_categories else "w"
            with category_path.open(open_mode) as category_file:
                category_file.write(graph_to_plain_graph6(graph) + "\n")
            initialized_categories.add(category_name)

            category_counts[category_name] += 1
            processed += 1

            if processed % 100 == 0:
                print(f"  categorized {processed} graphs")

            if args.max_graphs is not None and processed >= args.max_graphs:
                print(f"Stopped after {processed} graphs.")
                print("Categories:")
                for category_name, count in sorted(category_counts.items()):
                    print(f"  {category_name}: {count}")
                return

    print(f"Categorized {processed} graphs.")
    print("Categories:")
    for category_name, count in sorted(category_counts.items()):
        print(f"  {category_name}: {count}")


if __name__ == "__main__":
    main()
