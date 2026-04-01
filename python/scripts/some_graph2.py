import networkx as nx
from functions_d.is_colorable import is_multigraph_edge_k_colorable
import matplotlib.pyplot as plt
from functions_d.draw_multigraph import draw_multigraph

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
    
    for i in range(0,7):
        prev = (i-1)%7
        next = (i+1)%7
        G.add_edge(f"{i}_0",f"{i}_1")
        G.add_edge(f"{i}_0",f"{i}_1")
        
        G.add_edge(f"{i}_2",f"{i}_1")
        G.add_edge(f"{i}_2",f"{i}_1")
        
        G.add_edge(f"{i}_2",f"{i}_3")
        G.add_edge(f"{i}_2",f"{i}_3")
        
        G.add_edge(f"{i}_0",f"{i}_3")
        
        if i < (i+6)%7:
            G.add_edge(f"{i}_0",f"{(i+6)%7}_0")
        if i < (i+1)%7:
            G.add_edge(f"{i}_0",f"{(i+1)%7}_0")
        if i < (i+2)%7:
            G.add_edge(f"{i}_1",f"{(i+2)%7}_3")
        if i < (i+3)%7:
            G.add_edge(f"{i}_2",f"{(i+3)%7}_3")
        if i < (i+4)%7:
            G.add_edge(f"{i}_3",f"{(i+4)%7}_1")
        if i < (i+5)%7:
            G.add_edge(f"{i}_3",f"{(i+5)%7}_2")
        
    G.add_edge("4_2", "6_3")
    G.remove_edge("4_1","6_3")
    draw_multigraph(G,"multi.png")
        

    
    print(nx.degree_histogram(G))
    print(multigraph_edge_connectivity(G))
    print(is_multigraph_edge_k_colorable(G, 5))
    
    
    

if __name__ == "__main__":
    main()
