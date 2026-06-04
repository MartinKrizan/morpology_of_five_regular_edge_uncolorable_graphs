import networkx as nx
from functions_d.add_edge import add_edge, add_two_edges
from functions_d.is_colorable import is_edge_k_colorable, is_multigraph_edge_k_colorable
import matplotlib.pyplot as plt
from functions_d.draw_multigraph import draw_multigraph


def main():
    G =nx.MultiGraph()
    
    for i in range(0,5):
        G.add_edge(f"{i}_1", f"{i}_2")
        G.add_edge(f"{i}_1", f"{(i+1)%5}_1")
        G.add_edge(f"{i}_1", f"{(i+1)%5}_1")
        
        G.add_edge(f"{i}_2", f"{(i+2)%5}_2")
        G.add_edge(f"{i}_2", f"{(i+2)%5}_2")
   
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G,5))
    draw_multigraph(G)
    
    
if __name__ == "__main__":
    main()