import networkx as nx
from functions_d.add_edge import add_edge
from functions_d.is_colorable import is_edge_k_colorable
import matplotlib.pyplot as plt


def main():
    G = nx.Graph()
    G.add_edge(0,6)
    G.add_edge(1,6)
    G.add_edge(2,6)
    G.add_edge(7,6)
    G.add_edge(7,3)
    G.add_edge(7,4)
    G.add_edge(7,5)
    
    H = add_edge(G, 6, 7)
    plt.figure(figsize=(10,10))
    nx.draw(H, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=14)
    plt.savefig("2ca.png")
    plt.close()

if __name__ == "__main__":
    main()