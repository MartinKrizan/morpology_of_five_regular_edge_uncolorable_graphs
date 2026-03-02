#!/usr/bin/env python3
import sys
import networkx as nx
import os
from functions_d.g_from_file import read_graphs_from_file
from functions_d.is_colorable import is_edge_k_colorable


def main():
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.", file=sys.stderr)
        sys.exit(1)

    try:
        i=0
        for G in read_graphs_from_file(filename):
            i+=1
            if i%10==0:
                print(i)
            try:
                # Assuming k=5 based on the project context
                colorable, _ = is_edge_k_colorable(G, 5)
                if colorable:
                    print("colorable:",nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<"))
            except Exception as e:
                print(f"Error processing graph: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error reading file {filename}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
