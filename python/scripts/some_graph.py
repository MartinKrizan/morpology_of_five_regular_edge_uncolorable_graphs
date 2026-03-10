import networkx as nx
from functions_d.add_edge import add_edge, add_two_edges
from functions_d.is_colorable import is_edge_k_colorable
import matplotlib.pyplot as plt

def main():
    G =nx.Graph()
    
    G.add_node("g1")
    G.add_node("g2")
    G.add_node("g3")
    
    G.add_node("b1")
    G.add_node("b2")
    
    G.add_node("r1")
    G.add_node("r2")
    
    G.add_node("ble")
    
    G.add_edge("g1","g2")
    G.add_edge("g1","g3")
    G.add_edge("g2","g3")
    
    G.add_edge("g1","ble")
    G.add_edge("g1","b1")
    G.add_edge("g1","b2")
    G.add_edge("g2","ble")
    G.add_edge("g2","b1")
    G.add_edge("g2","b2")
    G.add_edge("g3","ble")
    G.add_edge("g3","b1")
    G.add_edge("g3","b2")
    
    G.add_edge("b1","b2")
    G.add_edge("b1","r2")
    G.add_edge("b2","r1")
    
    G.add_edge("r1","ble")
    G.add_edge("r2","ble")
    
    G.add_edge("r1","r2")
    G.add_edge("r1","r2")
    
    G = add_two_edges(G,"r1","r2")
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_edge_k_colorable(G,5))
    
    plt.figure(figsize=(10,10))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=14)
    plt.savefig("2ca.png")
    plt.close()
    
    
if __name__ == "__main__":
    main()