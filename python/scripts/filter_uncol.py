import sys
import os
import ast
import networkx as nx

# Add parent to path so we can import functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable


def parse_multicode(line):
    data = list(map(int, line.split()))

    n = data[0]
    m = data[1]

    G = nx.MultiGraph()
    G.add_nodes_from(range(n))

    pos = 2
    for _ in range(m):
        u = data[pos]
        v = data[pos + 1]
        mult = data[pos + 2]
        pos += 3

        for _ in range(mult):
            G.add_edge(u, v)

    return G


def main():
    i=0
    for line in sys.stdin:
        i+=1
        G = parse_multicode(line)
        if(not is_multigraph_edge_k_colorable(G,5)[0]):
            print(line)
            
        if(i%1000 == 0):
            print(f"---{i}")

if __name__ == "__main__":
    main()