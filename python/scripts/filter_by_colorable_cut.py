import networkx as nx
from functions_d.g_from_file import read_graphs_from_file
from functions_d.is_colorable import is_edge_k_colorable

def is_overfull(G):
    """
    Checks if a graph G is overfull.
    A graph G is overfull if |E| > delta(G) * floor(|V|/2).
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    
    if n == 0:
        return False
        
    degrees = [d for n, d in G.degree()]
    delta = max(degrees) if degrees else 0
    
    # Condition: |E| > delta * floor(n/2)
    return m > delta * (n // 2)

def process_graphs(filename):
    i=0
    checked=[]
    for G in read_graphs_from_file(filename):
        i+=1
        if i%100==0:
            print(i,len(checked), "\n")

        if i<600:
            continue
            
        # 1. Check edge connectivity
        connectivity = nx.edge_connectivity(G)

        if connectivity>4:
            print(f"Graph {i} is not 4-edge-connected")
            continue
        
        # 2. Find min-cut and remove edges in cut
        # stoer_wagner returns (cut_value, partition)
        # partition is a tuple of two sets of nodes
        cut_value, partition = nx.stoer_wagner(G)
        
        nodes1, nodes2 = partition
        
        # Create subgraphs (removing edges in cut is implicit by node decomposition)
        G1 = G.subgraph(nodes1).copy()
        G2 = G.subgraph(nodes2).copy()

        if ( 
            nx.to_graph6_bytes(G1).decode().strip().lstrip(">>graph6<<") in checked 
            and nx.to_graph6_bytes(G2).decode().strip().lstrip(">>graph6<<") in checked):
            continue
        
        
        # 3. Check 5-colorability of each component
        # Note: is_edge_k_colorable returns (bool, assignment)
        colorable1 = (False if nx.to_graph6_bytes(G1).decode().strip().lstrip(">>graph6<<") in checked 
            else is_edge_k_colorable(G1, 5)[0])
        checked.append(nx.to_graph6_bytes(G1).decode().strip().lstrip(">>graph6<<"))
        if not colorable1:
            continue
            
        colorable2 = (False if nx.to_graph6_bytes(G2).decode().strip().lstrip(">>graph6<<") in checked 
            else is_edge_k_colorable(G2, 5)[0])
        
        checked.append(nx.to_graph6_bytes(G2).decode().strip().lstrip(">>graph6<<"))

        if( (not is_overfull(G1)) and (not is_overfull(G2))):
            print("Graph has no overfull component", i)
            print(nx.edge_connectivity(G))
            print(nx.to_graph6_bytes(G1).decode().strip().lstrip(">>graph6<<"))
            print(nx.to_graph6_bytes(G2).decode().strip().lstrip(">>graph6<<"))
            print(nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<"))
            print("-" * 20)

        # 4. Print graph if both components are colorable
        if colorable1 and colorable2:
            g6_str = nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<")
            print(f"Connectivity: {connectivity}, Cut Value: {cut_value}")
            print(f"Graph: {g6_str}")
            print("-" * 20)

if __name__ == "__main__":
    import os
    results_path = "../data/uncol/16v/uncol_16.g6"
    if os.path.exists(results_path):
        process_graphs(results_path)
    else:
        print(f"File not found: {results_path}")
