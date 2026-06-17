import json

import networkx as nx
import pytest
from ortools.sat.python import cp_model

from morphology_graphs.core import gadget as gadget_module
from morphology_graphs.core.gadget import (
    CandidateResult,
    Gadget5Pole,
    analyze_three_state_encoding,
    canonical_signature_set_under_color_permutation,
    categorize_port_pairs,
    enumerate_port_color_signatures,
    graph_to_plain_graph6,
    is_5_edge_colorable,
    is_internally_5_edge_connected,
    load_gadget_json,
    min_gadget_cut,
    save_candidate_json,
    save_candidate_summary,
    save_gadget_dot,
    validate_degree_5,
    validate_gadget,
)


class UnknownSolver:
    def __init__(self):
        self.parameters = type("Parameters", (), {})()

    def Solve(self, model):
        return cp_model.UNKNOWN

    def StatusName(self, status):
        return "UNKNOWN"


def test_degree_validation_accepts_single_vertex_five_port_gadget():
    gadget = Gadget5Pole.from_parts(1, [], [0, 0, 0, 0, 0])

    assert validate_degree_5(gadget)
    assert validate_gadget(gadget) == []


def test_degree_validation_rejects_wrong_total_degree():
    gadget = Gadget5Pole.from_parts(2, [(0, 1)], [0, 0, 0, 1, 1])

    assert not validate_degree_5(gadget)
    assert validate_gadget(gadget)


def test_boundary_enumeration_returns_permutation_signatures():
    gadget = Gadget5Pole.from_parts(1, [], [0, 0, 0, 0, 0])

    enumeration = enumerate_port_color_signatures(gadget, max_signatures=8)

    assert len(enumeration.signatures) == 8
    assert not enumeration.complete
    assert all(sorted(signature) == [0, 1, 2, 3, 4] for signature in enumeration.signatures)
    assert is_5_edge_colorable(gadget)


def test_gadget_colorability_unknown_status_is_not_unsat(monkeypatch):
    monkeypatch.setattr(gadget_module.cp_model, "CpSolver", UnknownSolver)

    with pytest.raises(RuntimeError, match="UNKNOWN"):
        is_5_edge_colorable(Gadget5Pole.from_parts(1, [], [0, 0, 0, 0, 0]))


def test_signature_set_canonicalization_uses_global_color_renaming():
    signatures = {
        (2, 4, 0, 1, 3),
    }

    canonical = canonical_signature_set_under_color_permutation(signatures)

    assert canonical == ((0, 1, 2, 3, 4),)


def test_cut_checker_finds_small_cut():
    gadget = Gadget5Pole.from_parts(3, [(0, 1)], [2, 2, 2, 2, 2])

    assert min_gadget_cut(gadget) == 0
    assert not is_internally_5_edge_connected(gadget)


def test_serialization_outputs_machine_and_human_artifacts(tmp_path):
    gadget = Gadget5Pole.from_parts(1, [], [0, 0, 0, 0, 0])
    signatures = frozenset({(0, 1, 2, 3, 4)})
    result = CandidateResult(
        gadget=gadget,
        signatures=signatures,
        canonical_signature_set=canonical_signature_set_under_color_permutation(signatures),
        min_cut=5,
        small_cut_count=0,
        score=1001,
        complete=True,
        three_state_diagnostics=analyze_three_state_encoding(signatures),
    )

    json_path = tmp_path / "candidate.json"
    text_path = tmp_path / "candidate.txt"
    dot_path = tmp_path / "candidate.dot"

    save_candidate_json(result, json_path)
    save_candidate_summary(result, text_path)
    save_gadget_dot(gadget, dot_path)

    assert load_gadget_json(json_path) == gadget
    assert json.loads(json_path.read_text())["num_signatures"] == 1
    assert "allowed signatures = 1" in text_path.read_text()
    assert "p0" in dot_path.read_text()


def test_pair_categorization_detects_forced_different_ports_at_same_vertex():
    graph = nx.Graph()
    graph.add_node(0)

    category = categorize_port_pairs(graph, [0, 0, 0, 0, 0])

    assert category.forced_same == 0
    assert category.forced_different == 10
    assert category.flexible == 0
    assert category.blocked == 0
    assert category.file_stem() == "s0d10f0b0"


def test_plain_graph6_has_no_header():
    graph = nx.path_graph(3)

    assert not graph_to_plain_graph6(graph).startswith(">>graph6<<")
