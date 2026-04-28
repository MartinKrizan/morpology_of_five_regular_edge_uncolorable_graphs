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
        if first == arr[i] or arr[i-1] == arr[i]:
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
    
    n=11
    
    for i in range(0,n):
        G.add_edge(f"_{i}",f"_{(i+1)%n}")
        G.add_edge(f"_{i}",f"_{(i+1)%n}")
        free_nodes.append(f"_{i}")
    free_nodes.append(f"_{n+1}")
    free_nodes.append(f"_{n+1}")
    free_nodes.append(f"_{n+1}")
    free_nodes.append(f"_{n+2}")
    free_nodes.append(f"_{n+2}")
    free_nodes.append(f"_{n+2}")
    free_nodes.append(f"_{n+3}")
    free_nodes.append(f"_{n+3}")
    free_nodes.append(f"_{n+3}")
    G.add_edge(f"_{n+1}",f"_{n+2}")
    G.add_edge(f"_{n+1}",f"_{n+3}")
    G.add_edge(f"_{n+2}",f"_{n+3}")
    
    G.add_edge("_0", f"_{n+1}")
    free_nodes.remove("_0")
    free_nodes.remove(f"_{n+1}")
    
    cnt = 0
    for pairing in all_pairings(free_nodes):
        cnt+=1
        if cnt < 0: #5M
            continue
        if cnt % 1000 == 0:
            print (cnt, pairing)
        
       
        H = G.copy()
        for pair in pairing:
            H.add_edge(pair[0], pair[1])
        if cnt % 1000 == 0:
            draw_multigraph(H)
        
        if multigraph_edge_connectivity(H) >3:
            if not is_multigraph_edge_k_colorable(H,5)[0]:
                print("wiiii", pairing)
                nx.degree_histogram(H)
                print(nx.minimum_edge_cut(H),multigraph_edge_connectivity(H))
                draw_multigraph(H)
                return
            #print(multigraph_edge_connectivity(H))
            #draw_multigraph(H)
            #print(cnt, pairing)
        
    #print(is_multigraph_edge_k_colorable(G, 5))
    
    
    

if __name__ == "__main__":
    main()
