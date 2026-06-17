import networkx as nx


def replace_multiedge_vertices_with_k5(G):
    """
    Repeatedly replaces vertices that are incident to a multiedge with a K5.
    Returns a simple graph. If the input is a 5-regular multigraph, the
    output will be a 5-regular simple graph.
    """
    H = nx.MultiGraph(G)
    
    while True:
        target_v = None
        for v in H.nodes():
            # In a multigraph, a vertex is incident to a multiedge if its
            # number of unique neighbors is less than its degree.
            if len(set(H.neighbors(v))) < H.degree(v):
                target_v = v
                break
                
        if target_v is None:
            break
            
        incident_edges = list(H.edges(target_v, keys=True))
        
        # Exactly 5 incident edges are needed for a 5-regular-preserving substitution.
        if len(incident_edges) != 5:
            raise ValueError(f"Vertex {target_v} does not have degree 5 (has {len(incident_edges)}).")
            
        new_nodes = [f"k5_{target_v}_{i}" for i in range(5)]
        H.add_nodes_from(new_nodes)
        
        # Add the K5 internal edges
        for i in range(5):
            for j in range(i + 1, 5):
                H.add_edge(new_nodes[i], new_nodes[j])
                
        # Rewire the 5 incident edges to the 5 new vertices
        for i, edge in enumerate(incident_edges):
            u, v, key = edge
            neighbor = u if v == target_v else v
            
            # Add an edge between the neighbor and the i-th vertex of the K5
            H.add_edge(neighbor, new_nodes[i])
            
        # Remove the original vertex
        H.remove_node(target_v)
        
    return nx.Graph(H)
