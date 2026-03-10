import networkx as nx

def add_edge(G,u,v):
    if(not G.has_edge(u,v)):
        H = G.copy()
        H.add_edge(u,v)
        return H

    H = nx.Graph()
    
    c=0
    for edge in G.edges:
        if edge[0] != u and edge[1] != u:
            H.add_edge(edge[0], edge[1])
        else: 
            e = edge[0] if edge[1] == u else edge[1]
            H.add_edge(f"n_{u}_{c}", e)
            for i in range(4):
                H.add_edge(f"b_{u}_{i}", f"n_{u}_{c}")
            c+=1
        

    return H

def add_two_edges(G, u, v):
    H = nx.Graph()
    
    c=0
    for edge in G.edges:
        if edge[0] != u and edge[1] != u:
            H.add_edge(edge[0], edge[1])
            
        else: 
            e = edge[0] if edge[1] == u else edge[1]
            H.add_edge(f"n_{u}_{c}", e)
            
            for i in range(4):
                H.add_edge(f"b_{u}_{i}", f"n_{u}_{c}")
            c+=1
    
    for i in range(4):
        H.add_edge(f"b_{u}_{i}", f"n_{u}_3")
        H.add_edge(f"b_{u}_{i}", f"n_{u}_4")
    H.add_edge(f"{v}", f"n_{u}_3")
    H.add_edge(f"{v}", f"n_{u}_4")
        

    return H