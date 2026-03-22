import networkx as nx

def has_double_cycle(G):
    """
    Detects if a multigraph contains a 'double cycle'.
    A double cycle is a cycle where every edge between consecutive nodes
    has a multiplicity of at least 2.
    
    Returns:
        bool: True if a double cycle exists, False otherwise.
    """
    # Create a simple graph that only contains edges with multiplicity >= 2
    H = nx.Graph()
    
    for u, v in G.edges(keys=False):
        if G.number_of_edges(u, v) >= 2:
            H.add_edge(u, v)
            
    # Check if this new graph contains any cycle
    try:
        nx.find_cycle(H)
        return True
    except nx.NetworkXNoCycle:
        return False
