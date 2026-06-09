def is_overfull(graph):
    """
    Check whether a graph is overfull.

    A graph G is overfull when |E| > Delta(G) * floor(|V| / 2).
    """
    n = graph.number_of_nodes()
    m = graph.number_of_edges()

    if n == 0:
        return False

    degrees = [degree for _, degree in graph.degree()]
    max_degree = max(degrees) if degrees else 0

    return m > max_degree * (n // 2)
