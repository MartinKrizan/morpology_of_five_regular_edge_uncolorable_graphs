import networkx as nx


def parse_multicode(line):
    """Parse one multicode line into a NetworkX MultiGraph."""
    data = list(map(int, line.split()))

    n = data[0]
    m = data[1]

    graph = nx.MultiGraph()
    graph.add_nodes_from(range(n))

    pos = 2
    for _ in range(m):
        u = data[pos]
        v = data[pos + 1]
        multiplicity = data[pos + 2]
        pos += 3

        for _ in range(multiplicity):
            graph.add_edge(u, v)

    return graph
