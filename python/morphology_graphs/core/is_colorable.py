import networkx as nx
from ortools.sat.python import cp_model


def normalize_edge(u, v):
    """Ensure consistent undirected edge key."""
    return (u, v) if u < v else (v, u)


def normalize_multiedge(u, v, key):
    """Ensure consistent undirected multiedge key."""
    return (u, v, key) if u < v else (v, u, key)


def _is_sat_status(status):
    return status in (cp_model.FEASIBLE, cp_model.OPTIMAL)


def _status_name(solver, status):
    status_name = getattr(solver, "StatusName", None)
    if status_name is None:
        return str(status)
    return status_name(status)


def _max_degree(G):
    return max((degree for _, degree in G.degree()), default=0)


def _exceeds_matching_capacity(G, k):
    return G.number_of_edges() > k * (G.number_of_nodes() // 2)


def _make_solver(time_limit_s, solver, num_search_workers):
    if solver is not None:
        return solver

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = num_search_workers
    return solver


def _verify_assignment(incident_edges_by_node, assignment):
    for node, incident_edges in incident_edges_by_node.items():
        used = set()
        for edge in incident_edges:
            color = assignment[edge]
            if color in used:
                print(f"invalid edge coloring at vertex {node} color {color}")
                return False
            used.add(color)
    return True


def _add_symmetry_breaking(
    model,
    edge_vars,
    incident_edges_by_node,
    fixed_node,
    k,
    encoding,
):
    for color, edge in enumerate(incident_edges_by_node[fixed_node]):
        if color >= k:
            break
        if encoding == "bool":
            model.Add(edge_vars[(edge, color)] == 1)
        else:
            model.Add(edge_vars[edge] == color)


def _build_bool_model(edge_list, incident_edges_by_node, k, break_symmetry, fixed_node):
    model = cp_model.CpModel()
    edge_vars = {}

    for edge in edge_list:
        color_vars = []
        for color in range(k):
            var = model.NewBoolVar(f"e_{len(edge_vars)}")
            edge_vars[(edge, color)] = var
            color_vars.append(var)
        model.AddExactlyOne(color_vars)

    for incident_edges in incident_edges_by_node.values():
        if len(incident_edges) < 2:
            continue
        for color in range(k):
            model.AddAtMostOne(edge_vars[(edge, color)] for edge in incident_edges)

    if break_symmetry and edge_list:
        _add_symmetry_breaking(
            model,
            edge_vars,
            incident_edges_by_node,
            fixed_node,
            k,
            "bool",
        )

    return model, edge_vars


def _build_int_model(edge_list, incident_edges_by_node, k, break_symmetry, fixed_node):
    model = cp_model.CpModel()
    edge_vars = {
        edge: model.NewIntVar(0, k - 1, f"c_{'_'.join(map(str, edge))}")
        for edge in edge_list
    }

    if break_symmetry and edge_list:
        _add_symmetry_breaking(
            model,
            edge_vars,
            incident_edges_by_node,
            fixed_node,
            k,
            "int",
        )

    for incident_edges in incident_edges_by_node.values():
        if len(incident_edges) > 1:
            model.AddAllDifferent(edge_vars[edge] for edge in incident_edges)

    return model, edge_vars


def _solve_edge_coloring(
    edge_list,
    incident_edges_by_node,
    k,
    time_limit_s,
    solver,
    break_symmetry,
    encoding,
    return_assignment,
    verify_assignment,
    num_search_workers,
):
    fixed_node = max(
        incident_edges_by_node,
        key=lambda node: len(incident_edges_by_node[node]),
    )

    if encoding == "bool":
        model, edge_vars = _build_bool_model(
            edge_list,
            incident_edges_by_node,
            k,
            break_symmetry,
            fixed_node,
        )
    elif encoding == "int":
        model, edge_vars = _build_int_model(
            edge_list,
            incident_edges_by_node,
            k,
            break_symmetry,
            fixed_node,
        )
    else:
        raise ValueError(f"unknown edge coloring encoding: {encoding}")

    solver = _make_solver(time_limit_s, solver, num_search_workers)
    status = solver.Solve(model)

    if status == cp_model.INFEASIBLE:
        return False, None

    if not _is_sat_status(status):
        raise RuntimeError(
            "CP-SAT did not decide the edge-coloring instance: "
            f"{_status_name(solver, status)}"
        )

    if not return_assignment:
        return True, {}

    if encoding == "bool":
        assignment = {}
        for edge in edge_list:
            for color in range(k):
                if solver.BooleanValue(edge_vars[(edge, color)]):
                    assignment[edge] = color
                    break
    else:
        assignment = {edge: solver.Value(edge_vars[edge]) for edge in edge_list}

    if verify_assignment and not _verify_assignment(incident_edges_by_node, assignment):
        return False, assignment

    return True, assignment


def is_edge_k_colorable(
    G,
    k,
    time_limit_s=10,
    solver=None,
    break_symmetry=True,
    return_assignment=True,
    verify_assignment=True,
    encoding="int",
):
    """Check if undirected graph G is edge k-colorable using CP-SAT."""
    if not G.edges():
        return True, {}

    max_degree = _max_degree(G)
    if k < max_degree:
        return False, None

    if _exceeds_matching_capacity(G, k):
        return False, None

    if not return_assignment:
        if nx.is_bipartite(G):
            return True, {}

        # Vizing's theorem: every simple graph is edge-colorable with
        # max_degree + 1 colors.
        if k >= max_degree + 1:
            return True, {}

    edge_list = [normalize_edge(u, v) for u, v in G.edges()]
    incident_edges_by_node = {
        node: [normalize_edge(node, neighbor) for neighbor in G.neighbors(node)]
        for node in G.nodes()
    }

    return _solve_edge_coloring(
        edge_list,
        incident_edges_by_node,
        k,
        time_limit_s,
        solver,
        break_symmetry,
        encoding,
        return_assignment,
        verify_assignment,
        num_search_workers=1,
    )


def is_multigraph_edge_k_colorable(
    G,
    k,
    time_limit_s=10,
    solver=None,
    break_symmetry=True,
    return_assignment=True,
    verify_assignment=True,
    encoding="int",
):
    """Check if undirected multigraph G is edge k-colorable using CP-SAT."""
    if not G.edges():
        return True, {}

    max_degree = _max_degree(G)
    if k < max_degree:
        return False, None

    if _exceeds_matching_capacity(G, k):
        return False, None

    if not return_assignment and nx.is_bipartite(G):
        return True, {}

    edge_list = [normalize_multiedge(u, v, key) for u, v, key in G.edges(keys=True)]
    incident_edges_by_node = {
        node: [
            normalize_multiedge(u, v, key)
            for u, v, key in G.edges(node, keys=True)
        ]
        for node in G.nodes()
    }

    return _solve_edge_coloring(
        edge_list,
        incident_edges_by_node,
        k,
        time_limit_s,
        solver,
        break_symmetry,
        encoding,
        return_assignment,
        verify_assignment,
        num_search_workers=8,
    )
