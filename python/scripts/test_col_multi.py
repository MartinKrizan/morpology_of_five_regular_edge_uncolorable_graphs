import networkx as nx
import random
import time
from functions_d.add_edge import add_edge
from functions_d.is_colorable import is_multigraph_edge_k_colorable
from functions_d.draw_multigraph import draw_multigraph
from functions_d.double_cycle import has_double_cycle

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

def add_nodes_and_edges(G, num_nodes, num_edges, max_degree=5):
    """
    Adds a given number of nodes and edges to the multigraph G,
    ensuring that the maximum degree does not exceed max_degree.
    """
    start_node = max(G.nodes) + 1 if G.nodes else 0
    new_nodes = list(range(start_node, start_node + num_nodes))
    G.add_nodes_from(new_nodes)
    
    edges_added = 0
    attempts = 0
    max_attempts = num_edges * 10
    
    while edges_added < num_edges and attempts < max_attempts:
        attempts += 1
        # Find nodes with degree strictly less than max_degree
        valid_nodes = [n for n in G.nodes if (G.degree(n) < max_degree and n != 4)]
        
        # Need at least two distinct nodes to form an edge without a self loop
        if len(valid_nodes) < 2:
            print(f"Warning: Cannot add more edges without exceeding max degree {max_degree}.")
            break
            
        u = random.choice(valid_nodes)
        v_candidates = [n for n in valid_nodes if n != u and G.number_of_edges(u, n) < 2]
        
        if not v_candidates:
            print("Warning: Cannot add more edges without exceeding max degree {max_degree}.")
            continue
            
        # To improve overall connectivity and degree distribution, preferentially
        # connect to candidates that currently have the minimum degree.
        v_min_deg = min(G.degree(n) for n in v_candidates)
        v_min_deg_nodes = [n for n in v_candidates if G.degree(n) == v_min_deg]
        v = random.choice(v_min_deg_nodes)
        
        G.add_edge(u, v)
        edges_added += 1

    return G

def main():
    G = nx.MultiGraph()
    G.add_edge(0,1)
    G.add_edge(0,1)
    G.add_edge(0,1)
    G.add_edge(0,4)
    G.add_edge(1,4)
    G.add_edge(0,2)
    G.add_edge(1,3)
    
    n = 12
    # Example: generating a random multigraph on 6 vertices with 14 edges, max degree 5
    add_nodes_and_edges(G, num_nodes=n, num_edges=n*5/2+2, max_degree=5)
    
    deg=nx.degree_histogram(G)
    if deg[1]!=0:
        return

    if has_double_cycle(G):
        return
        
    H = G.copy()
    H.remove_node(0)
    H.remove_node(1)
    H.remove_node(4)
    con = multigraph_edge_connectivity(H)
    if con < 4:
        return
    

    is_col = is_multigraph_edge_k_colorable(G, 5)
    if not is_col[0]:
        
        print(nx.degree_histogram(G), con)
        print(G.edges())
        print("Is 5-edge-colorable:", is_col)        
        draw_multigraph(G, f"out/_uncolorable_{n}_multigraph_no_double_cycle_{time.time()}.png")



if __name__ == "__main__":
    for  i in range(100000):
        if i%1000 == 0:
            print(i)
        main()
