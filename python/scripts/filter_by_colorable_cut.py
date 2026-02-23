import networkx as nx
from functions_d.g_from_file import read_graphs_from_file
from functions_d.is_colorable import is_edge_k_colorable

def process_graphs(filename):
    i=0
    checked=[]
    for G in read_graphs_from_file(filename):
        i+=1
        if i%100==0:
            print(i,len(checked), "\n")
            
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

        # 4. Print graph if both components are colorable
        if colorable1 and colorable2:
            g6_str = nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<")
            print(f"Connectivity: {connectivity}, Cut Value: {cut_value}")
            print(f"Graph: {g6_str}")
            print("-" * 20)

if __name__ == "__main__":
    import os
    results_path = "results/uncol_16.g6"
    if os.path.exists(results_path):
        process_graphs(results_path)
    else:
        print(f"File not found: {results_path}")
