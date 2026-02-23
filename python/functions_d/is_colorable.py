import networkx as nx
from ortools.sat.python import cp_model

def normalize_edge(u, v):
    """Ensure consistent undirected edge key."""
    return (u, v) if u < v else (v, u)

def is_edge_k_colorable(G, k, time_limit_s=10):
    """Check if undirected graph G is edge k-colorable using CP-SAT."""
    if not G.edges():
        return True, {}

    # 1. Early exits based on Graph Theory
    degrees = [d for n, d in G.degree()]
    max_degree = max(degrees) if degrees else 0
    
    # Vizing's theorem: Δ <= χ'(G) <= Δ + 1
    if k < max_degree:
        return False, None
    
    # Bipartite graphs: χ'(G) = Δ
    if nx.is_bipartite(G):
        if k >= max_degree:
            # We could return True here, but if the user wants an assignment, 
            # we may still need to run the solver or use a bipartite matching algorithm.
            # For now, let's just let the solver handle the assignment if k >= max_degree.
            pass

    model = cp_model.CpModel()

    # create variable for each undirected edge
    color = {}
    edge_list = list(G.edges())
    for u, v in edge_list:
        e = normalize_edge(u, v)
        color[e] = model.NewIntVar(0, k - 1, f"c_{e[0]}_{e[1]}")
    
    # 2. Symmetry Breaking: Fix colors of edges incident to the first vertex
    # This reduces the search space by fixing one set of constraints.
    first_node = next(iter(G.nodes()))
    for i, neighbor in enumerate(G.neighbors(first_node)):
        if i < k:
            e = normalize_edge(first_node, neighbor)
            model.Add(color[e] == i)

    # 3. Use AddAllDifferent for incident edges
    for v in G.nodes():
        incident = [color[normalize_edge(v, u)] for u in G.neighbors(v)]
        if len(incident) > 1:
            model.AddAllDifferent(incident)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        assignment = {e: solver.Value(color[e]) for e in color}
        # verify correctness
        for v in G.nodes():
            used = set()
            for u in G.neighbors(v):
                e = normalize_edge(u, v)
                c = assignment[e]
                if c in used:
                    print(f"❌ invalid edge coloring at vertex {v} color {c}")
                    return False, assignment
                used.add(c)
        return True, assignment
    else:
        return False, None

