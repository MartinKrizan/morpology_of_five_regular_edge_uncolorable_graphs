#!/usr/bin/env python3
import sys
import os
import ast
import networkx as nx

# Add parent to path so we can import functions_d
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions_d.k5_substitution import replace_multiedge_vertices_with_k5
from functions_d.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable

def main():
    if len(sys.argv) < 2:
        print("Usage: python filter_k5.py <results_file.txt>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)
        
    print(f"Reading graphs from {filepath}")
    print("Applying K5 substitution and checking edge connectivity > 3...")
    print("-" * 60)
    
    with open(filepath, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if line_num%1000==0:
                print (line_num,"-----")
            
            parts = line.split(" | ", 1)
            if len(parts) != 2:
                continue
                
            index_str, edges_str = parts
            
            try:
                edges = ast.literal_eval(edges_str)
            except Exception as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
                
            G = nx.MultiGraph()
            G.add_edges_from(edges)
            
            # Apply K5 substitution
            try:
                simple_G = replace_multiedge_vertices_with_k5(G)
            except ValueError as e:
                print(f"Graph {index_str} skipped: {e}")
                continue
                
            # Check edge connectivity
            conn = nx.edge_connectivity(simple_G)
            col = is_multigraph_edge_k_colorable(G, 5)
            
            if conn > 3 or col[0]:
                print(f"Graph Index: {index_str}")
                print(f"  Transformed Nodes: {simple_G.number_of_nodes()}")
                print(f"  Transformed Edges: {simple_G.number_of_edges()}")
                print(f"  Edge Connectivity: {conn}")
                print(f"  Col: {col}")
                print(f"  Original Edges: {edges_str}")
                print("-" * 60)

if __name__ == "__main__":
    main()
