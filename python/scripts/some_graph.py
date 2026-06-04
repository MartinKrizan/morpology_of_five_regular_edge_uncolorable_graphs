import networkx as nx
from functions_d.add_edge import add_edge, add_two_edges
from functions_d.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable
import matplotlib.pyplot as plt
from functions_d.draw_multigraph import draw_multigraph


def main():
    G =nx.MultiGraph()
    
    for i in [(0, 1), (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 7), (1, 7), (2, 3), (2, 3), (2, 6), (3, 6), (3, 6), (4, 5), (4, 5), (4, 7), (4, 7), (5, 6), (5, 6), (5, 7)]:
        G.add_edge(i[0],i[1])
   
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G,5))
    draw_multigraph(G)
    
    
if __name__ == "__main__":
    main()