import networkx as nx
from functions_d.is_colorable import is_multigraph_edge_k_colorable
import matplotlib.pyplot as plt
from functions_d.draw_multigraph import draw_multigraph

def main():
    
    k5 = nx.complete_graph(4)
    
    G =nx.MultiGraph(k5)
    
    # two outgoing edges have same color
    G.add_edge(0,1)
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G,4))
    draw_multigraph(G)
    
    
if __name__ == "__main__":
    main()