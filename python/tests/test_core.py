import networkx as nx
import pytest
from ortools.sat.python import cp_model

from morphology_graphs.core.is_colorable import (
    is_edge_k_colorable,
    is_multigraph_edge_k_colorable,
)
from morphology_graphs.core.k5_substitution import replace_multiedge_vertices_with_k5
from morphology_graphs.core.multicode import parse_multicode
from morphology_graphs.core.overfull import is_overfull


class UnknownSolver:
    def Solve(self, model):
        return cp_model.UNKNOWN

    def StatusName(self, status):
        return "UNKNOWN"


def test_parse_multicode_preserves_parallel_edges():
    graph = parse_multicode("2 1 0 1 3")

    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 3
    assert graph.number_of_edges(0, 1) == 3


def test_overfull_detects_dense_odd_complete_graph():
    assert is_overfull(nx.complete_graph(5))
    assert not is_overfull(nx.path_graph(5))


def test_edge_colorability_simple_cycle():
    colorable, assignment = is_edge_k_colorable(nx.cycle_graph(4), 2)

    assert colorable
    assert len(assignment) == 4


def test_edge_colorability_bool_encoding():
    colorable, assignment = is_edge_k_colorable(nx.cycle_graph(4), 2, encoding="bool")

    assert colorable
    assert len(assignment) == 4


def test_edge_colorability_unknown_status_is_not_unsat():
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        is_edge_k_colorable(nx.cycle_graph(4), 2, solver=UnknownSolver())


def test_edge_colorability_decision_only_fast_paths():
    complete_odd = nx.complete_graph(5)

    assert is_edge_k_colorable(complete_odd, 4, return_assignment=False)[0] is False
    assert is_edge_k_colorable(complete_odd, 5, return_assignment=False) == (True, {})
    assert is_edge_k_colorable(nx.complete_bipartite_graph(3, 3), 3, return_assignment=False) == (
        True,
        {},
    )


def test_multigraph_colorability_accounts_for_parallel_edges():
    graph = nx.MultiGraph()
    graph.add_nodes_from([0, 1])
    graph.add_edges_from([(0, 1), (0, 1), (0, 1)])

    assert is_multigraph_edge_k_colorable(graph, 2)[0] is False
    assert is_multigraph_edge_k_colorable(graph, 3)[0] is True


def test_multigraph_colorability_unknown_status_is_not_unsat():
    graph = nx.MultiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

    with pytest.raises(RuntimeError, match="UNKNOWN"):
        is_multigraph_edge_k_colorable(graph, 2, solver=UnknownSolver())


def test_k5_substitution_removes_multiedge_vertex():
    graph = nx.MultiGraph()
    graph.add_nodes_from(range(6))
    graph.add_edges_from([(0, 1), (0, 1), (0, 2), (0, 3), (0, 4)])

    simple = replace_multiedge_vertices_with_k5(graph)

    assert isinstance(simple, nx.Graph)
    assert simple.number_of_nodes() == 10
    assert all(len(set(simple.neighbors(v))) == simple.degree(v) for v in simple.nodes())
