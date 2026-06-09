import networkx as nx

def split_by_cut(G):
    num, cut = nx.stoer_wagner(G)

    first = cut[0]
    second = cut[1]
    #print(first, second)

    fG = nx.Graph()
    fG.add_nodes_from(first)

    sG = nx.Graph()
    sG.add_nodes_from(second)

    for edge in G.edges:
        if edge[0] in first and edge[1] in first:
            fG.add_edge(edge[0],edge[1])
        if edge[0] in second and edge[1] in second:
            sG.add_edge(edge[0], edge[1])

    print(nx.to_graph6_bytes(fG).decode().strip().lstrip(">>graph6<<"))
    print(nx.to_graph6_bytes(sG).decode().strip().lstrip(">>graph6<<"))
