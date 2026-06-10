#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from morphology_graphs.core.gadget import (
    CandidateResult,
    evaluate_candidate,
    expected_internal_edge_count,
    is_internally_5_edge_connected,
    iter_candidate_gadgets,
    save_candidate_json,
    save_candidate_summary,
    save_gadget_dot,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for 5-regular 5-port edge-coloring gadgets using nauty geng."
    )
    parser.add_argument("--n-min", type=int, default=5, help="Smallest internal order to search.")
    parser.add_argument("--n-max", type=int, default=9, help="Largest internal order to search.")
    parser.add_argument("--geng", default="geng", help="Path to nauty geng executable.")
    parser.add_argument(
        "--geng-min-degree",
        type=int,
        default=4,
        help="Minimum internal degree passed to geng. Default matches -d4.",
    )
    parser.add_argument(
        "--geng-max-degree",
        type=int,
        default=5,
        help="Maximum internal degree passed to geng. Default matches -D5.",
    )
    parser.add_argument(
        "--allow-disconnected",
        action="store_true",
        help="Do not pass -c to geng. Connected gadgets are required by default.",
    )
    parser.add_argument(
        "--require-cut-5",
        action="store_true",
        help="Reject candidates with a nontrivial gadget cut below 5.",
    )
    parser.add_argument(
        "--all-port-placements",
        action="store_true",
        help="Do not reject port placements related by internal automorphisms.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of best candidates to save.",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=None,
        help="Stop after evaluating this many candidate port placements.",
    )
    parser.add_argument(
        "--max-signatures",
        type=int,
        default=None,
        help="Stop boundary enumeration after this many signatures per candidate.",
    )
    parser.add_argument(
        "--solver-time-limit",
        type=float,
        default=10.0,
        help="CP-SAT time limit per solve, in seconds.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/gadgets"),
        help="Directory for JSON, text, and DOT candidate artifacts.",
    )
    return parser.parse_args()


def insert_ranked(results: list[CandidateResult], result: CandidateResult, max_results: int) -> None:
    results.append(result)
    results.sort(key=lambda item: (item.score, len(item.signatures), item.gadget.n, item.gadget.port_vertices))
    del results[max_results:]


def save_results(results: list[CandidateResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, result in enumerate(results, start=1):
        stem = f"candidate_{index:03d}_n{result.gadget.n}_s{len(result.signatures)}"
        save_candidate_json(result, output_dir / f"{stem}.json")
        save_candidate_summary(result, output_dir / f"{stem}.txt")
        save_gadget_dot(result.gadget, output_dir / f"{stem}.dot")


def main() -> None:
    args = parse_args()
    if args.n_min > args.n_max:
        print("error: --n-min must be at most --n-max", file=sys.stderr)
        raise SystemExit(2)

    results: list[CandidateResult] = []
    evaluated = 0

    for n in range(args.n_min, args.n_max + 1):
        if n % 2 == 0:
            continue
        edge_count = expected_internal_edge_count(n)
        print(f"Searching n={n} with {edge_count} internal edges...")

        for gadget in iter_candidate_gadgets(
            n,
            geng_path=args.geng,
            require_connected=not args.allow_disconnected,
            min_degree=args.geng_min_degree,
            max_degree=args.geng_max_degree,
            reject_isomorphic_ports=not args.all_port_placements,
        ):
            if args.require_cut_5 and not is_internally_5_edge_connected(gadget):
                continue

            result = evaluate_candidate(
                gadget,
                max_signatures=args.max_signatures,
                time_limit_s=args.solver_time_limit,
            )
            evaluated += 1
            insert_ranked(results, result, args.max_results)

            if evaluated % 100 == 0:
                best = results[0] if results else None
                best_text = f", best score {best.score}" if best is not None else ""
                print(f"  evaluated {evaluated} candidates{best_text}")

            if args.max_candidates is not None and evaluated >= args.max_candidates:
                save_results(results, args.output_dir)
                print(f"Stopped after {evaluated} candidates.")
                print(f"Saved {len(results)} ranked candidates to {args.output_dir}")
                return

    save_results(results, args.output_dir)
    print(f"Evaluated {evaluated} candidates.")
    print(f"Saved {len(results)} ranked candidates to {args.output_dir}")

    for index, result in enumerate(results[:10], start=1):
        print(f"Candidate #{index}:")
        print(f"  n = {result.gadget.n}")
        print(f"  internal edges = {len(result.gadget.internal_edges)}")
        print(f"  port vertices = {list(result.gadget.port_vertices)}")
        print(f"  min cut = {result.min_cut}")
        print(f"  allowed signatures = {len(result.signatures)}")
        print(f"  complete = {result.complete}")
        print(f"  score = {result.score}")


if __name__ == "__main__":
    main()
