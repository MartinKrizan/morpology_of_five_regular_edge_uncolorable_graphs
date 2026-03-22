import networkx as nx
from functions_d.add_edge import add_edge, add_two_edges
from functions_d.is_colorable import is_edge_k_colorable
import matplotlib.pyplot as plt

def main():
    G =nx.from_graph6_bytes("Fpvoo".encode())

    G = add_edge(G, 0,1)
    G = add_edge(G, 5,2)
    G = add_edge(G, 4,1)
    G = add_edge(G, 2,3)
    
    #G = add_two_edges(G,"r1","r2")
    
    H = nx.convert_node_labels_to_integers(G)
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_edge_k_colorable(H,5))
    
    plt.figure(figsize=(10,10))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=14)
    plt.savefig("2ca.png")
    plt.close()
    
    
if __name__ == "__main__":
    main()


