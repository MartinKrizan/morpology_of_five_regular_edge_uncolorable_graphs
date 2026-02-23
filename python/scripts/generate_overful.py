#!/usr/bin/env python3
import networkx as nx
import random
import argparse
import sys

def generate_overful(n, delta=5):
    """
    Tries to generate an overful graph with n vertices and max degree delta.
    An overful graph G has |E| > delta * floor(n/2).
    """
    if n % 2 == 0:
        # Overful graphs with delta > degree of any vertex can't exist for even n?
        # Actually, the definition says total edges > delta * floor(n/2).
        # But if max degree is delta, and n is even, max edges is delta * n / 2.
        # So it can't be > delta * (n/2).
        return None

    threshold = delta * (n // 2)
    
    # Try multiple times to find a dense enough graph
    for _ in range(100):
        G = nx.Graph()
        G.add_nodes_from(range(n))
        
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(edges)
        
        degrees = [0] * n
        for u, v in edges:
            if degrees[u] < delta and degrees[v] < delta:
                G.add_edge(u, v)
                degrees[u] += 1
                degrees[v] += 1
        
        if G.number_of_edges() >= threshold:
            return G
            
    return None

def main():
    parser = argparse.ArgumentParser(description="Generate overful graphs with max degree delta.")
    parser.add_argument("n", type=int, help="Number of vertices (must be odd)")
    parser.add_argument("--delta", type=int, default=5, help="Maximum degree (default: 5)")
    parser.add_argument("--count", type=int, default=1, help="Number of graphs to generate")
    
    args = parser.parse_args()
    
    if args.n % 2 == 0:
        print(f"Error: Number of vertices {args.n} must be odd for a graph to be overful with max degree {args.delta}.", file=sys.stderr)
        sys.exit(1)
        
    generated = 0
    attempts = 0
    max_attempts = args.count * 1000
    
    while generated < args.count and attempts < max_attempts:
        attempts += 1
        G = generate_overful(args.n, args.delta)
        if G:
            print(nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<"))
            generated += 1
            
    if generated < args.count:
        print(f"Warning: Only generated {generated} out of {args.count} requested graphs.", file=sys.stderr)

if __name__ == "__main__":
    main()
