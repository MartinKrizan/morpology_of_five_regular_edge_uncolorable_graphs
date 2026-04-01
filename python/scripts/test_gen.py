import networkx as nx
import random

def add_nodes_and_edges_both_min(G, num_nodes, num_edges, max_degree=5):
    start_node = max(G.nodes) + 1 if G.nodes else 0
    new_nodes = list(range(start_node, start_node + num_nodes))
    G.add_nodes_from(new_nodes)
    edges_added = 0
    attempts = int(num_edges * 10)
    for _ in range(attempts):
        if edges_added >= num_edges: break
        valid_nodes = [n for n in G.nodes if (G.degree(n) < max_degree and n != 4)]
        if len(valid_nodes) < 2: break
            
        min_deg = min(G.degree(n) for n in valid_nodes)
        min_deg_nodes = [n for n in valid_nodes if G.degree(n) == min_deg]
        u = random.choice(min_deg_nodes)
        
        v_candidates = [n for n in valid_nodes if n != u and G.number_of_edges(u, n) < 2]
        if not v_candidates: continue
            
        v_min_deg = min(G.degree(n) for n in v_candidates)
        v_min_deg_nodes = [n for n in v_candidates if G.degree(n) == v_min_deg]
        v = random.choice(v_min_deg_nodes)
        
        G.add_edge(u, v)
        edges_added += 1
    return G

def add_nodes_and_edges_v_min(G, num_nodes, num_edges, max_degree=5):
    start_node = max(G.nodes) + 1 if G.nodes else 0
    new_nodes = list(range(start_node, start_node + num_nodes))
    G.add_nodes_from(new_nodes)
    edges_added = 0
    attempts = int(num_edges * 10)
    for _ in range(attempts):
        if edges_added >= num_edges: break
        valid_nodes = [n for n in G.nodes if (G.degree(n) < max_degree and n != 4)]
        if len(valid_nodes) < 2: break
            
        u = random.choice(valid_nodes)
        
        v_candidates = [n for n in valid_nodes if n != u and G.number_of_edges(u, n) < 2]
        if not v_candidates: continue
            
        v_min_deg = min(G.degree(n) for n in v_candidates)
        v_min_deg_nodes = [n for n in v_candidates if G.degree(n) == v_min_deg]
        v = random.choice(v_min_deg_nodes)
        
        G.add_edge(u, v)
        edges_added += 1
    return G

results_both = 0
results_v = 0
for i in range(1000):
    G = nx.MultiGraph()
    G.add_edge(0,1); G.add_edge(0,1); G.add_edge(0,1); G.add_edge(0,4); G.add_edge(1,4); G.add_edge(0,2); G.add_edge(1,3)
    add_nodes_and_edges_both_min(G, 9, 23)
    H = G.copy(); H.remove_nodes_from([0,1,4])
    if nx.edge_connectivity(H) >= 3: results_both += 1

    G = nx.MultiGraph()
    G.add_edge(0,1); G.add_edge(0,1); G.add_edge(0,1); G.add_edge(0,4); G.add_edge(1,4); G.add_edge(0,2); G.add_edge(1,3)
    add_nodes_and_edges_v_min(G, 9, 23)
    H = G.copy(); H.remove_nodes_from([0,1,4])
    if nx.edge_connectivity(H) >= 3: results_v += 1

print(f"Both min success: {results_both}/1000")
print(f"V min success: {results_v}/1000")
