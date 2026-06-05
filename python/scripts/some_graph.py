import networkx as nx
from functions_d.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable
from functions_d.draw_multigraph import draw_multigraph


def main():
    G =nx.MultiGraph()
    
    for i in [(0, 1), (0, 1), (0, 2), (0, 3), (0, 4), (1, 9), (1, 9), (1, 9), (2, 7), (2, 7), (2, 8), (2, 8), (3, 4), (3, 6), (3, 6), (3, 9), (4, 5), (4, 6), (4, 7), (5, 6), (5, 6), (5, 7), (5, 8), (7, 8), (8, 9)]:
        G.add_edge(i[0],i[1])
   
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G,5))
    draw_multigraph(G)
    
    
if __name__ == "__main__":
    main()