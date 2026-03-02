import networkx as nx
from functions_d.add_edge import add_edge
from functions_d.is_colorable import is_edge_k_colorable

def all_pairings(arr):
    if len(arr) % 2 != 0:
        raise ValueError("Array length must be even.")

    if not arr:
        yield []
        return

    first = arr[0]

    for i in range(1, len(arr)):
        pair = (first, arr[i])
        remaining = arr[1:i] + arr[i+1:]

        for rest in all_pairings(remaining):
            yield [pair] + rest

def main():

    G = nx.from_graph6_bytes("Q{c??GB?_GcKOEDOAQGWOAgD_E?".encode())

    i = 0
    for pairing in all_pairings(list(G.nodes())):
        i+=1
        # 30000 - nothing
        if(i%10000 == 0):
            print(i)
        GC = G.copy()
        for (u,v) in pairing:
            GC=add_edge(GC, u, v)

        GC = nx.convert_node_labels_to_integers(GC)

        colorable = is_edge_k_colorable(GC, 5)

        if not colorable[0]:
            print("wiiii not colorable:", pairing)
            print(nx.to_graph6_bytes(G).decode().strip().lstrip(">>graph6<<"))


    



if __name__ == "__main__":
    main()