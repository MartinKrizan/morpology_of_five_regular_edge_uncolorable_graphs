from __future__ import annotations

import itertools
import json
import math
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

import networkx as nx
from ortools.sat.python import cp_model


COLORS = tuple(range(5))


@dataclass(frozen=True)
class Gadget5Pole:
    n: int
    internal_edges: tuple[tuple[int, int], ...]
    port_vertices: tuple[int, int, int, int, int]

    def __post_init__(self) -> None:
        normalized_edges = tuple(sorted((min(u, v), max(u, v)) for u, v in self.internal_edges))
        object.__setattr__(self, "internal_edges", normalized_edges)
        object.__setattr__(self, "port_vertices", tuple(self.port_vertices))

    @classmethod
    def from_parts(
        cls,
        n: int,
        internal_edges: Iterable[tuple[int, int]],
        port_vertices: Iterable[int],
    ) -> "Gadget5Pole":
        ports = tuple(port_vertices)
        if len(ports) != 5:
            raise ValueError(f"expected exactly 5 ports, got {len(ports)}")
        return cls(n=n, internal_edges=tuple(internal_edges), port_vertices=ports)  # type: ignore[arg-type]

    def internal_graph(self) -> nx.Graph:
        graph = nx.Graph()
        graph.add_nodes_from(range(self.n))
        graph.add_edges_from(self.internal_edges)
        return graph

    def internal_degrees(self) -> list[int]:
        degrees = [0] * self.n
        for u, v in self.internal_edges:
            degrees[u] += 1
            degrees[v] += 1
        return degrees

    def port_counts(self) -> Counter[int]:
        return Counter(self.port_vertices)

    def to_dict(
        self,
        *,
        signatures: Iterable[tuple[int, int, int, int, int]] | None = None,
        min_cut: int | None = None,
        score: int | None = None,
        complete: bool | None = None,
    ) -> dict:
        data = {
            "n": self.n,
            "internal_edges": [list(edge) for edge in self.internal_edges],
            "ports": list(self.port_vertices),
        }
        if signatures is not None:
            signature_list = sorted(signatures)
            data["num_signatures"] = len(signature_list)
            data["signatures"] = [list(signature) for signature in signature_list]
        if min_cut is not None:
            data["min_cut"] = min_cut
        if score is not None:
            data["score"] = score
        if complete is not None:
            data["signature_enumeration_complete"] = complete
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Gadget5Pole":
        return cls.from_parts(
            int(data["n"]),
            (tuple(edge) for edge in data["internal_edges"]),
            data["ports"],
        )


@dataclass(frozen=True)
class BoundaryEnumeration:
    signatures: frozenset[tuple[int, int, int, int, int]]
    complete: bool
    status_name: str


@dataclass(frozen=True)
class CandidateResult:
    gadget: Gadget5Pole
    signatures: frozenset[tuple[int, int, int, int, int]]
    canonical_signature_set: tuple[tuple[int, int, int, int, int], ...]
    min_cut: int
    small_cut_count: int
    score: int
    complete: bool
    three_state_diagnostics: dict


def validate_port_count_5(gadget: Gadget5Pole) -> bool:
    return len(gadget.port_vertices) == 5


def validate_no_loops(gadget: Gadget5Pole) -> bool:
    return all(u != v for u, v in gadget.internal_edges)


def validate_simple_internal(gadget: Gadget5Pole) -> bool:
    return len(set(gadget.internal_edges)) == len(gadget.internal_edges)


def validate_connected(gadget: Gadget5Pole) -> bool:
    graph = gadget.internal_graph()
    return gadget.n > 0 and nx.is_connected(graph)


def validate_degree_5(gadget: Gadget5Pole) -> bool:
    if not validate_port_count_5(gadget):
        return False
    port_counts = gadget.port_counts()
    degrees = gadget.internal_degrees()
    return all(degrees[v] + port_counts[v] == 5 for v in range(gadget.n))


def validate_gadget(gadget: Gadget5Pole, *, require_simple: bool = True) -> list[str]:
    errors = []
    if gadget.n <= 0:
        errors.append("n must be positive")
    if not validate_port_count_5(gadget):
        errors.append("gadget must have exactly 5 ports")
    for u, v in gadget.internal_edges:
        if not (0 <= u < gadget.n and 0 <= v < gadget.n):
            errors.append(f"internal edge {(u, v)} uses vertex outside 0..{gadget.n - 1}")
    for port_index, v in enumerate(gadget.port_vertices):
        if not 0 <= v < gadget.n:
            errors.append(f"port {port_index} is attached to vertex outside 0..{gadget.n - 1}")
    if not validate_no_loops(gadget):
        errors.append("internal loops are not allowed")
    if require_simple and not validate_simple_internal(gadget):
        errors.append("parallel internal edges are not allowed in simple mode")
    if not errors and not validate_degree_5(gadget):
        errors.append("every internal vertex must have internal degree plus port count equal to 5")
    if not errors and not validate_connected(gadget):
        errors.append("internal graph must be connected")
    return errors


def expected_internal_edge_count(n: int) -> int:
    if n % 2 == 0:
        raise ValueError("5-pole internal order must be odd because 5n - 5 must be even")
    return (5 * n - 5) // 2


def iter_geng_graphs(
    n: int,
    *,
    geng_path: str = "geng",
    require_connected: bool = True,
    min_degree: int = 4,
    max_degree: int = 5,
) -> Iterator[nx.Graph]:
    edge_count = expected_internal_edge_count(n)
    resolved = shutil.which(geng_path)
    if resolved is None:
        raise RuntimeError(f"nauty geng executable not found: {geng_path!r}")

    flags = ["-q", f"-d{min_degree}", f"-D{max_degree}"]
    if require_connected:
        flags.append("-c")
    command = [resolved, *flags, str(n), f"{edge_count}:{edge_count}"]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdout is not None
    for raw_line in process.stdout:
        line = raw_line.strip()
        if not line:
            continue
        yield nx.from_graph6_bytes(line)

    stderr = process.stderr.read().decode(errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"geng failed with exit code {return_code}: {stderr.strip()}")


def deficits_from_graph(graph: nx.Graph) -> list[int]:
    deficits: list[int] = []
    for vertex in sorted(graph.nodes()):
        degree = graph.degree(vertex)
        if degree > 5:
            raise ValueError(f"internal vertex {vertex} has degree {degree}, expected at most 5")
        deficits.extend([vertex] * (5 - degree))
    if len(deficits) != 5:
        raise ValueError(f"internal graph has total missing degree {len(deficits)}, expected 5")
    return deficits


def _augmented_port_graph(graph: nx.Graph, port_vertices: tuple[int, int, int, int, int]) -> nx.Graph:
    augmented = nx.Graph()
    for vertex in graph.nodes():
        augmented.add_node(("v", vertex), kind="internal")
    for u, v in graph.edges():
        augmented.add_edge(("v", u), ("v", v))
    for port_index, vertex in enumerate(port_vertices):
        port_node = ("p", port_index)
        augmented.add_node(port_node, kind=f"port_{port_index}")
        augmented.add_edge(port_node, ("v", vertex))
    return augmented


def iter_port_placements(
    graph: nx.Graph,
    *,
    reject_isomorphic: bool = True,
) -> Iterator[tuple[int, int, int, int, int]]:
    deficits = deficits_from_graph(graph)
    seen_augmented: list[nx.Graph] = []
    node_match = nx.algorithms.isomorphism.categorical_node_match("kind", None)

    for placement in sorted(set(itertools.permutations(deficits, 5))):
        if reject_isomorphic:
            augmented = _augmented_port_graph(graph, placement)
            if any(nx.is_isomorphic(augmented, seen, node_match=node_match) for seen in seen_augmented):
                continue
            seen_augmented.append(augmented)
        yield placement  # type: ignore[misc]


def iter_candidate_gadgets(
    n: int,
    *,
    geng_path: str = "geng",
    require_connected: bool = True,
    min_degree: int = 4,
    max_degree: int = 5,
    reject_isomorphic_ports: bool = True,
) -> Iterator[Gadget5Pole]:
    for graph in iter_geng_graphs(
        n,
        geng_path=geng_path,
        require_connected=require_connected,
        min_degree=min_degree,
        max_degree=max_degree,
    ):
        edges = tuple(sorted((min(u, v), max(u, v)) for u, v in graph.edges()))
        for port_vertices in iter_port_placements(graph, reject_isomorphic=reject_isomorphic_ports):
            gadget = Gadget5Pole.from_parts(n, edges, port_vertices)
            if not validate_gadget(gadget):
                yield gadget


def min_gadget_cut(gadget: Gadget5Pole) -> int:
    if gadget.n <= 1:
        return 5

    port_counts = gadget.port_counts()
    best = math.inf
    vertices = range(gadget.n)
    # Checking both U and its complement is intentional: port edges belong to
    # whichever side contains their attachment vertex.
    for mask in range(1, (1 << gadget.n) - 1):
        subset = {v for v in vertices if mask & (1 << v)}
        crossing = 0
        for u, v in gadget.internal_edges:
            if (u in subset) != (v in subset):
                crossing += 1
        port_cut = sum(port_counts[v] for v in subset)
        best = min(best, crossing + port_cut)
    return int(best)


def count_small_cuts(gadget: Gadget5Pole, *, threshold: int = 5) -> int:
    if gadget.n <= 1:
        return 0

    port_counts = gadget.port_counts()
    count = 0
    vertices = range(gadget.n)
    for mask in range(1, (1 << gadget.n) - 1):
        subset = {v for v in vertices if mask & (1 << v)}
        crossing = sum(1 for u, v in gadget.internal_edges if (u in subset) != (v in subset))
        port_cut = sum(port_counts[v] for v in subset)
        if crossing + port_cut < threshold:
            count += 1
    return count


def is_internally_5_edge_connected(gadget: Gadget5Pole) -> bool:
    return min_gadget_cut(gadget) >= 5


def _build_coloring_model(gadget: Gadget5Pole) -> tuple[cp_model.CpModel, list[cp_model.IntVar]]:
    model = cp_model.CpModel()
    internal_vars = [
        model.NewIntVar(0, 4, f"e_{index}_{u}_{v}")
        for index, (u, v) in enumerate(gadget.internal_edges)
    ]
    port_vars = [model.NewIntVar(0, 4, f"p_{index}") for index in range(5)]

    incident: dict[int, list[cp_model.IntVar]] = defaultdict(list)
    for var, (u, v) in zip(internal_vars, gadget.internal_edges):
        incident[u].append(var)
        incident[v].append(var)
    for port_index, vertex in enumerate(gadget.port_vertices):
        incident[vertex].append(port_vars[port_index])

    for vertex in range(gadget.n):
        model.AddAllDifferent(incident[vertex])

    return model, port_vars


def is_5_edge_colorable(gadget: Gadget5Pole, *, time_limit_s: float = 10.0) -> bool:
    model, _ = _build_coloring_model(gadget)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    return status in (cp_model.FEASIBLE, cp_model.OPTIMAL)


def enumerate_port_color_signatures(
    gadget: Gadget5Pole,
    *,
    max_signatures: int | None = None,
    time_limit_s: float = 10.0,
) -> BoundaryEnumeration:
    model, port_vars = _build_coloring_model(gadget)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 8

    signatures: set[tuple[int, int, int, int, int]] = set()
    last_status = cp_model.UNKNOWN

    while max_signatures is None or len(signatures) < max_signatures:
        last_status = solver.Solve(model)
        if last_status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return BoundaryEnumeration(
                signatures=frozenset(signatures),
                complete=last_status == cp_model.INFEASIBLE,
                status_name=solver.StatusName(last_status),
            )

        signature = tuple(solver.Value(var) for var in port_vars)
        if tuple(sorted(signature)) != COLORS:
            raise AssertionError(f"invalid 5-pole signature with repeated color: {signature}")
        signatures.add(signature)  # type: ignore[arg-type]

        differs = []
        for port_index, value in enumerate(signature):
            differs_here = model.NewBoolVar(f"block_{len(signatures)}_{port_index}")
            model.Add(port_vars[port_index] != value).OnlyEnforceIf(differs_here)
            model.Add(port_vars[port_index] == value).OnlyEnforceIf(differs_here.Not())
            differs.append(differs_here)
        model.AddBoolOr(differs)

    return BoundaryEnumeration(
        signatures=frozenset(signatures),
        complete=False,
        status_name=solver.StatusName(last_status),
    )


def canonical_signature_set_under_color_permutation(
    signatures: Iterable[tuple[int, int, int, int, int]],
) -> tuple[tuple[int, int, int, int, int], ...]:
    signature_tuple = tuple(signatures)
    if not signature_tuple:
        return ()

    best: tuple[tuple[int, int, int, int, int], ...] | None = None
    for permutation in itertools.permutations(COLORS):
        transformed = tuple(sorted(tuple(permutation[color] for color in signature) for signature in signature_tuple))
        if best is None or transformed < best:
            best = transformed
    assert best is not None
    return best


def permutation_parity(signature: tuple[int, int, int, int, int]) -> int:
    inversions = 0
    for i, value in enumerate(signature):
        inversions += sum(1 for later in signature[i + 1 :] if value > later)
    return inversions % 2


def analyze_three_state_encoding(signatures: Iterable[tuple[int, int, int, int, int]]) -> dict:
    signature_list = sorted(signatures)
    size = len(signature_list)
    parity_counts = Counter(permutation_parity(signature) for signature in signature_list)
    color_position_counts = {
        color: Counter(signature.index(color) for signature in signature_list)
        for color in COLORS
    }
    return {
        "size": size,
        "divisible_by_3": size % 3 == 0,
        "target_class_size": size // 3 if size % 3 == 0 else None,
        "parity_counts": dict(sorted(parity_counts.items())),
        "color_position_counts": {
            str(color): dict(sorted(counts.items()))
            for color, counts in color_position_counts.items()
        },
    }


def score_candidate(gadget: Gadget5Pole, signatures: Iterable[tuple[int, int, int, int, int]]) -> int:
    return 1000 * len(set(signatures)) + 100 * count_small_cuts(gadget) + gadget.n


def evaluate_candidate(
    gadget: Gadget5Pole,
    *,
    max_signatures: int | None = None,
    time_limit_s: float = 10.0,
) -> CandidateResult:
    enumeration = enumerate_port_color_signatures(
        gadget,
        max_signatures=max_signatures,
        time_limit_s=time_limit_s,
    )
    small_cut_count = count_small_cuts(gadget)
    signatures = enumeration.signatures
    incomplete_penalty = 1_000_000 if not enumeration.complete else 0
    return CandidateResult(
        gadget=gadget,
        signatures=signatures,
        canonical_signature_set=canonical_signature_set_under_color_permutation(signatures),
        min_cut=min_gadget_cut(gadget),
        small_cut_count=small_cut_count,
        score=1000 * len(signatures) + 100 * small_cut_count + gadget.n + incomplete_penalty,
        complete=enumeration.complete,
        three_state_diagnostics=analyze_three_state_encoding(signatures),
    )


def save_candidate_json(result: CandidateResult, path: Path) -> None:
    data = result.gadget.to_dict(
        signatures=result.signatures,
        min_cut=result.min_cut,
        score=result.score,
        complete=result.complete,
    )
    data["canonical_signature_set"] = [list(signature) for signature in result.canonical_signature_set]
    data["small_cut_count"] = result.small_cut_count
    data["three_state_diagnostics"] = result.three_state_diagnostics
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def load_gadget_json(path: Path) -> Gadget5Pole:
    return Gadget5Pole.from_dict(json.loads(path.read_text()))


def save_candidate_summary(result: CandidateResult, path: Path) -> None:
    lines = [
        f"n = {result.gadget.n}",
        f"internal edges = {len(result.gadget.internal_edges)}",
        f"port vertices = {list(result.gadget.port_vertices)}",
        f"min cut = {result.min_cut}",
        f"small cuts below 5 = {result.small_cut_count}",
        f"allowed signatures = {len(result.signatures)}",
        f"signature enumeration complete = {result.complete}",
        f"score = {result.score}",
        "signatures:",
    ]
    lines.extend(f"  {list(signature)}" for signature in sorted(result.signatures))
    path.write_text("\n".join(lines) + "\n")


def save_gadget_dot(gadget: Gadget5Pole, path: Path) -> None:
    lines = ["graph gadget {", "  node [shape=circle];"]
    for vertex in range(gadget.n):
        lines.append(f'  v{vertex} [label="{vertex}"];')
    for u, v in gadget.internal_edges:
        lines.append(f"  v{u} -- v{v};")
    lines.append("  node [shape=plaintext];")
    for port_index, vertex in enumerate(gadget.port_vertices):
        lines.append(f'  p{port_index} [label="p{port_index}"];')
        lines.append(f'  v{vertex} -- p{port_index} [label="p{port_index}"];')
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")
