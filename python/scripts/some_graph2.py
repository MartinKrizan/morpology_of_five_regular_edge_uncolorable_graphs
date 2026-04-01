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

    G.add_edge(6,7)
    G.add_edge(7,8)
    G.add_edge(8,9)
    G.add_edge(9,10)
    G.add_edge(10,11)
    G.add_edge(11,12)
    G.add_edge(12,13)
    G.add_edge(13,14)
    G.add_edge(14,6)
    G.add_edge(6,7)
    G.add_edge(7,8)
    G.add_edge(8,9)
    G.add_edge(9,10)
    G.add_edge(10,11)
    G.add_edge(11,12)
    G.add_edge(12,13)
    G.add_edge(13,14)
    G.add_edge(14,6)
    

    G.add_edge(0,6)
    G.add_edge(1,8)
    G.add_edge(2,9)
    G.add_edge(3,11)
    G.add_edge(4,13)

    G.add_edge(7,12)
    G.add_edge(10,14)

    print(nx.degree_histogram(G))
    print(multigraph_edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G, 5))
    
    
    

if __name__ == "__main__":
    main()
