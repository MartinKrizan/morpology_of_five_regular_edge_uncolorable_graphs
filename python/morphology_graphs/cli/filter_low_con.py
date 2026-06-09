import sys
import networkx as nx

from morphology_graphs.core.k5_substitution import replace_multiedge_vertices_with_k5
from morphology_graphs.core.is_colorable import is_edge_k_colorable
from morphology_graphs.core.multicode import parse_multicode


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
