import networkx as nx

def add_edge(G,u,v):
    if(not G.has_edge(u,v)):
        H = G.copy()
        H.add_edge(u,v)
        return H

    H = nx.Graph()
    
    for edge in G.edges:
        if edge[0] != u and edge[0] !=v and edge[1] != u and edge[1] !=v:
            H.add_edge(edge[0], edge[1])


    for i in G.neighbors(u):
        if i == v: continue
        H.add_node(f"b_{u}_{i}")    
        H.add_edge(f"b_{u}_{i}", i)
        for j in range(4):
            H.add_edge(f"bi_{u}_{j}", f"b_{u}_{i}")

    H.add_edge(f"bo_{u}_1", f"bo_{v}_2")
    H.add_edge(f"bo_{u}_2", f"bo_{v}_1")

    for j in range(4):
        H.add_edge(f"bi_{u}_{j}", f"bo_{u}_1")
        H.add_edge(f"bi_{u}_{j}", f"bo_{u}_2")
        H.add_edge(f"bi_{v}_{j}", f"bo_{v}_1")
        H.add_edge(f"bi_{v}_{j}", f"bo_{v}_2")
    
    for i in G.neighbors(v):
        if i == u: continue
        H.add_node(f"b_{v}_{i}")    
        H.add_edge(f"b_{v}_{i}", i)
        for j in range(4):
            H.add_edge(f"bi_{v}_{j}", f"b_{v}_{i}")

        
    return H