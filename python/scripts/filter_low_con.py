import sys
import networkx as nx

from functions.k5_substitution import replace_multiedge_vertices_with_k5
from functions.is_colorable import is_edge_k_colorable

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
    stats = [0,0,0,0,0,0,0]
    print("started")

    for line in sys.stdin:
        if line.startswith("---") or len(line) < 10:
            continue
        i+=1
        if i%1000==0:
            print ("---",i, stats)

        try:
            G = parse_multicode(line)
            simple_G = replace_multiedge_vertices_with_k5(G)
        except ValueError as e:
            print(f"Graph {line} skipped: {e}")
            continue
            
        # Check edge connectivity
        conn = nx.edge_connectivity(simple_G)
        stats[conn]+=1
        
        if conn > 3 :
            col = is_edge_k_colorable(nx.convert_node_labels_to_integers(simple_G), 5)
            if col[0]:
                print("error: graph is colorable")

            print(nx.to_graph6_bytes(simple_G).decode())
            print("---con",conn)

    print("---",stats)

if __name__ == "__main__":
    main()
