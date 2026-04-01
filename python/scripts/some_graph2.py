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

def all_pairings(arr):
    if len(arr) % 2 != 0:
        raise ValueError("Array length must be even.")

    if not arr:
        yield []
        return

    first = arr[0]

    for i in range(1, len(arr)):
        pair = (first, arr[i])
        if first[:1] == arr[i][:1]:
            continue
        
        remaining = arr[1:i] + arr[i+1:]

        for rest in all_pairings(remaining):
            yield [pair] + rest

def isCon(pairing):
    first = False
    second = False
    third = False
    for pair in pairing:
        if pair[0][:1] == "0" and pair[1][:1] == "1":
            first = True
        if pair[0][:1] == "0" and pair[1][:1] == "2":
            second = True
        if pair[0][:1] == "0" and pair[1][:1] == "3":
            third = True
        if pair[0][:1] == "1":
            return first and second and third
    return False

def main():
    G = nx.MultiGraph()
    
    free_nodes = []
    
    for i in range(0,5):
        G.add_edge(f"{i}_0",f"{i}_1")
        G.add_edge(f"{i}_0",f"{i}_1")
        
        G.add_edge(f"{i}_2",f"{i}_1")
        G.add_edge(f"{i}_2",f"{i}_1")
        
        G.add_edge(f"{i}_2",f"{i}_3")
        G.add_edge(f"{i}_2",f"{i}_3")
        
        G.add_edge(f"{i}_0",f"{i}_3")
        free_nodes.append(f"{i}_0")
        free_nodes.append(f"{i}_0")
        free_nodes.append(f"{i}_1")
        free_nodes.append(f"{i}_2")
        free_nodes.append(f"{i}_3")
        free_nodes.append(f"{i}_3")
    
    free_nodes.remove("0_0")
    free_nodes.remove("1_3")
    G.add_edge("0_0","1_3")
    free_nodes.remove("0_3")
    free_nodes.remove("2_0")
    G.add_edge("0_3","2_0")
    free_nodes.remove("0_1")
    free_nodes.remove("3_0")
    G.add_edge("0_1","3_0")
    
    
    
    cnt = 0
    for pairing in all_pairings(free_nodes):
        cnt+=1
        if cnt < 0: #5M
            continue
        if cnt % 100000 == 0:
            print (cnt, pairing)
        
       
        H = G.copy()
        for pair in pairing:
            H.add_edge(pair[0], pair[1])
        if cnt % 10000 == 0:
            draw_multigraph(H)
        
        if multigraph_edge_connectivity(H) >4:
            print(multigraph_edge_connectivity(H))
            draw_multigraph(H)
            print(cnt, pairing)
            return
        
    print(is_multigraph_edge_k_colorable(G, 5))
    
    
    

if __name__ == "__main__":
    main()
