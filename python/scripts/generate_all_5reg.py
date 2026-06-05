#!/usr/bin/env python3
"""
Exhaustive generator of all 5-regular loopless multigraphs on N vertices.
Checks 5-edge-colorability and outputs only uncolorable graphs.

Each graph is defined by an upper-triangular multiplicity matrix m[i][j]
for 0 <= i < j <= N-1, where m[i][j] in {0,1,2,3} and sum_j m[i][j] = 5
for all i. Graphs are enumerated in lexicographic order of the multiplicity
tuple over pairs (0,1),(0,2),...,(0,N-1),(1,2),...,(N-2,N-1).

Usage:
    python generate_all_5reg.py N [--resume] [--output FILE] [--checkpoint FILE]

Examples:
    python generate_all_5reg.py 4
    python generate_all_5reg.py 6 --resume
    python generate_all_5reg.py 4 --count-only
"""

import os
import sys
import time
import argparse
import json
import networkx as nx
from ortools.sat.python import cp_model

# Add parent directory to path so we can import functions_d
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions_d.is_colorable import is_multigraph_edge_k_colorable

MAX_MULTIPLICITY = 3
DEGREE = 5
K = 5  # number of colors for edge coloring

# List of fixed edges that MUST be present in all generated graphs.
# This improves performance by reducing the search space.
# Example: FIXED_EDGES = [(0, 1), (0, 1), (0, 2), (1, 2)]
FIXED_EDGES = [(0,1),(0,1),(0,2),(0,3),(0,4),(5,6),(5,6)]


def build_pairs(n):
    """Build the ordered list of vertex pairs (i, j) with i < j."""
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def precompute_remaining(n, pairs):
    """
    Precompute remaining_after[v][pair_idx] = number of pairs involving
    vertex v with index strictly greater than pair_idx.

    Used for pruning: after assigning multiplicity to pair pair_idx,
    vertex v must be able to reach its remaining degree with the
    remaining pairs, i.e. remaining_deg[v] <= MAX_MULT * remaining_after[v][pair_idx].
    """
    num_pairs = len(pairs)
    vertex_pairs = [[] for _ in range(n)]
    for idx, (i, j) in enumerate(pairs):
        vertex_pairs[i].append(idx)
        vertex_pairs[j].append(idx)

    remaining_after = [[0] * num_pairs for _ in range(n)]
    for v in range(n):
        for pair_idx in range(num_pairs):
            remaining_after[v][pair_idx] = sum(
                1 for p in vertex_pairs[v] if p > pair_idx
            )

    return remaining_after


def generate_all_5regular(n, resume_after=None):
    """
    Generate all 5-regular loopless multigraphs on n vertices
    (max edge multiplicity MAX_MULTIPLICITY).

    Yields tuples of multiplicities in the order of pairs:
    (0,1), (0,2), ..., (0,n-1), (1,2), ..., (n-2,n-1).

    Uses an optimized iterative state machine for maximum speed.
    """
    if n < 2 or n % 2 != 0:
        return

    pairs = build_pairs(n)
    num_pairs = len(pairs)
    remaining_after = precompute_remaining(n, pairs)

    multiplicities = [0] * num_pairs
    remaining_deg = [DEGREE] * n

    # Precalculate minimum multiplicities from FIXED_EDGES
    fixed_multiplicities = [0] * num_pairs
    for u, v in FIXED_EDGES:
        if u > v:
            u, v = v, u
        if 0 <= u < n and 0 <= v < n and u != v:
            try:
                p_idx = pairs.index((u, v))
                fixed_multiplicities[p_idx] += 1
            except ValueError:
                pass

    # Precalculate 1D arrays for bounds to avoid inner loop overhead
    max_mult_ri_after = [0] * num_pairs
    max_mult_rj_after = [0] * num_pairs
    for idx, (i, j) in enumerate(pairs):
        max_mult_ri_after[idx] = remaining_after[i][idx] * MAX_MULTIPLICITY
        max_mult_rj_after[idx] = remaining_after[j][idx] * MAX_MULTIPLICITY

    # State machine arrays
    state_m = [-1] * num_pairs
    max_m_stack = [0] * num_pairs
    
    pair_idx = 0
    skip_mode = resume_after is not None

    while pair_idx >= 0:
        if pair_idx == num_pairs:
            # Reached a valid leaf
            if all(r == 0 for r in remaining_deg):
                if skip_mode:
                    skip_mode = False
                else:
                    yield tuple(multiplicities)
            pair_idx -= 1
            continue

        if state_m[pair_idx] == -1:
            # First time visiting this level
            i, j = pairs[pair_idx]
            
            # Calculate bounds
            max_m = min(MAX_MULTIPLICITY, remaining_deg[i], remaining_deg[j])
            
            lb_i = remaining_deg[i] - max_mult_ri_after[pair_idx]
            lb_j = remaining_deg[j] - max_mult_rj_after[pair_idx]
            
            fixed_m = fixed_multiplicities[pair_idx]
            min_m = max(lb_i, lb_j, fixed_m, 0)

            if min_m > max_m:
                # Dead end, backtrack
                state_m[pair_idx] = -1
                pair_idx -= 1
                continue
                
            max_m_stack[pair_idx] = max_m
            m = min_m
            
        else:
            # Returning from a deeper level, undo previous state and increment m
            i, j = pairs[pair_idx]
            prev_m = state_m[pair_idx]
            remaining_deg[i] += prev_m
            remaining_deg[j] += prev_m
            m = prev_m + 1

        # Fast-forward for resume logic
        if skip_mode and resume_after is not None:
            if m < resume_after[pair_idx]:
                m = resume_after[pair_idx]
            elif m > resume_after[pair_idx]:
                skip_mode = False

        if m > max_m_stack[pair_idx]:
            # Exhausted all valid multiplicities for this level, backtrack
            state_m[pair_idx] = -1
            pair_idx -= 1
            continue

        # Apply state and go deeper
        state_m[pair_idx] = m
        multiplicities[pair_idx] = m
        remaining_deg[i] -= m
        remaining_deg[j] -= m
        pair_idx += 1


def multiplicities_to_multigraph(n, pairs, mults):
    """Convert a multiplicity tuple to a networkx MultiGraph."""
    G = nx.MultiGraph()
    G.add_nodes_from(range(n))
    for idx, (i, j) in enumerate(pairs):
        for _ in range(mults[idx]):
            G.add_edge(i, j)
    return G


def save_checkpoint(filepath, n, mults, colorable_count, uncolorable_count):
    """Save checkpoint to file."""
    ckpt = {
        "n_vertices": n,
        "last_multiplicities": list(mults),
        "colorable_count": colorable_count,
        "uncolorable_count": uncolorable_count,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(filepath, "w") as f:
        json.dump(ckpt, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Generate all 5-regular loopless multigraphs on N vertices "
                    "(max edge multiplicity 3) and find uncolorable ones."
    )
    parser.add_argument("N", type=int,
                        help="Number of vertices (must be even, >= 2)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from last checkpoint")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file for uncolorable graphs "
                             "(default: results_5reg_<N>v.txt)")
    parser.add_argument("--checkpoint", type=str, default=None,
                        help="Checkpoint file path "
                             "(default: checkpoint_5reg_<N>v.json)")
    parser.add_argument("--time-limit", type=float, default=30.0,
                        help="Time limit per colorability check in seconds "
                             "(default: 30)")
    parser.add_argument("--count-only", action="store_true",
                        help="Only count the total number of valid graphs "
                             "(skip colorability check)")
    args = parser.parse_args()

    n = args.N
    if n % 2 != 0:
        print("Error: N must be even (5*N must be even for 5-regular graphs).",
              file=sys.stderr)
        sys.exit(1)
    if n < 2:
        print("Error: N must be at least 2.", file=sys.stderr)
        sys.exit(1)

    # ── Count-only mode ──────────────────────────────────────────────────
    if args.count_only:
        print(f"Counting all 5-regular loopless multigraphs on {n} vertices "
              f"(max multiplicity {MAX_MULTIPLICITY})...")
        t0 = time.perf_counter()
        count = 0
        for _ in generate_all_5regular(n):
            count += 1
            if count % 10000 == 0:
                print(f"  {count} graphs found so far...", end="\r")
        elapsed = time.perf_counter() - t0
        print(f"\nTotal graphs: {count}")
        print(f"Time: {elapsed:.2f}s")
        return

    # ── Full generation mode ─────────────────────────────────────────────
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = args.output or f"results_5reg_{n}v_{timestamp}.txt"
    checkpoint_file = args.checkpoint or f"checkpoint_5reg_{n}v_{timestamp}.json"
    pairs = build_pairs(n)

    # Load checkpoint if resuming
    resume_after = None
    colorable_count = 0
    uncolorable_count = 0

    if args.resume and os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            ckpt = json.load(f)
        if ckpt.get("n_vertices") != n:
            print(f"Error: checkpoint is for N={ckpt.get('n_vertices')}, "
                  f"but you specified N={n}", file=sys.stderr)
            sys.exit(1)
        resume_after = tuple(ckpt["last_multiplicities"])
        colorable_count = ckpt.get("colorable_count", 0)
        uncolorable_count = ckpt.get("uncolorable_count", 0)
        total_done = colorable_count + uncolorable_count
        print(f"Resuming from checkpoint:")
        print(f"  Last multiplicities: {resume_after}")
        print(f"  Already checked: {total_done} "
              f"(colorable: {colorable_count}, uncolorable: {uncolorable_count})")
        print()

    # Open output file (append if resuming, write if fresh)
    file_mode = "a" if resume_after is not None else "w"
    out_f = open(output_file, file_mode)

    if file_mode == "w":
        out_f.write(f"# 5-regular loopless multigraphs on {n} vertices "
                    f"(max multiplicity {MAX_MULTIPLICITY})\n")
        out_f.write(f"# Fixed edges: {FIXED_EDGES}\n")
        out_f.write(f"# Only UNCOLORABLE graphs listed below\n")
        out_f.write(f"# Format: <index> | <edge_list>\n")
        out_f.write(f"#\n")

    t_start = time.perf_counter()
    graph_index = colorable_count + uncolorable_count  # sequential index

    print(f"{'='*65}")
    print(f"  5-regular loopless multigraphs on {n} vertices")
    print(f"  Max edge multiplicity: {MAX_MULTIPLICITY}")
    print(f"  Output: {output_file}")
    print(f"  Checkpoint: {checkpoint_file}")
    print(f"{'='*65}")
    print()

    # Create reusable solver for colorability checks
    # Using 1 worker is dramatically faster when checking millions of tiny graphs 
    # because it avoids thread synchronization overhead.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = 1

    last_mults = None  # track for checkpoint

    try:
        for mults in generate_all_5regular(n, resume_after=resume_after):
            last_mults = mults

            # Build multigraph and check colorability
            G = multiplicities_to_multigraph(n, pairs, mults)
            colorable, _ = is_multigraph_edge_k_colorable(
                G, K, solver=solver
            )

            if colorable:
                colorable_count += 1
            else:
                uncolorable_count += 1
                edge_list = list(G.edges())
                line = f"{graph_index} | {edge_list}"
                print(f"\n  *** UNCOLORABLE #{uncolorable_count}: "
                      f"index={graph_index}, edges={edge_list}")
                out_f.write(line + "\n")

            graph_index += 1

            # Progress update and checkpointing every 1000 graphs
            if graph_index % 10000 == 0:
                out_f.flush()
                elapsed = time.perf_counter() - t_start
                print(
                    f"  [{graph_index}] "
                    f"col: {colorable_count}  uncol: {uncolorable_count}  "
                    f"elapsed: {elapsed:.1f}s  "
                    f"mults: {mults}",
                    end="\r"
                )
                save_checkpoint(checkpoint_file, n, mults,
                                colorable_count, uncolorable_count)

    except KeyboardInterrupt:
        print("\n\n  ⚠ Interrupted! Saving checkpoint...")
        if last_mults is not None:
            save_checkpoint(checkpoint_file, n, last_mults,
                            colorable_count, uncolorable_count)
            print(f"  Checkpoint saved to {checkpoint_file}")
            print(f"  Resume with: python {sys.argv[0]} {n} --resume")
        else:
            print("  No graphs were processed, no checkpoint saved.")
        out_f.close()
        sys.exit(1)

    out_f.close()

    # Final checkpoint (mark as completed)
    if last_mults is not None:
        ckpt = {
            "n_vertices": n,
            "last_multiplicities": list(last_mults),
            "colorable_count": colorable_count,
            "uncolorable_count": uncolorable_count,
            "completed": True,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(checkpoint_file, "w") as f:
            json.dump(ckpt, f, indent=2)

    elapsed = time.perf_counter() - t_start
    total = colorable_count + uncolorable_count

    print(f"\n\n{'='*65}")
    print(f"  DONE")
    print(f"{'='*65}")
    print(f"  Total graphs checked : {total}")
    print(f"  Colorable (class 1)  : {colorable_count}")
    print(f"  Uncolorable (class 2): {uncolorable_count}")
    print(f"  Total time           : {elapsed:.2f}s")
    if total > 0:
        print(f"  Avg per graph        : {elapsed / total * 1000:.1f} ms")
    print(f"  Results in           : {output_file}")
    print()


if __name__ == "__main__":
    main()
