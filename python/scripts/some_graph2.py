import networkx as nx
from functions_d.is_colorable import is_multigraph_edge_k_colorable

def multigraph_edge_connectivity(G):
    H = nx.Graph()

    for u, v in G.edges():
        if H.has_edge(u, v):
            H[u][v]['capacity'] += 1
        else:
            H.add_edge(u, v, capacity=1)

    # global min cut (edge connectivity)
    cut_value, _ = nx.stoer_wagner(H, weight='capacity')
    return cut_value

def main():
    G = nx.MultiGraph()
    G.add_edges_from(nx.complete_graph(5).edges)

    G.add_edge(0,5)
    G.add_edge(3,5)
    G.add_edge(4,5)
    G.add_edge(1,5)
    G.add_edge(2,6)
    G.add_edge(5,6)

    
    print(nx.degree_histogram(G))
    print(multigraph_edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G, 5))
    
    
    

if __name__ == "__main__":
    main()
