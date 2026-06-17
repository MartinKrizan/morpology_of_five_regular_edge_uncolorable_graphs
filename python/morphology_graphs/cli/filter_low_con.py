import sys
import networkx as nx

from morphology_graphs.core.k5_substitution import replace_multiedge_vertices_with_k5
from morphology_graphs.core.is_colorable import is_edge_k_colorable
from morphology_graphs.core.multicode import parse_multicode


def main():
    graph_count = 0
    connectivity_counts = [0, 0, 0, 0, 0, 0, 0]
    print("started")

    for line in sys.stdin:
        if line.startswith("---") or len(line) < 10:
            continue
        graph_count += 1
        if graph_count % 1000 == 0:
            print("---", graph_count, connectivity_counts)

        try:
            multigraph = parse_multicode(line)
            simple_graph = replace_multiedge_vertices_with_k5(multigraph)
        except ValueError as e:
            print(f"Graph {line} skipped: {e}")
            continue

        edge_connectivity = nx.edge_connectivity(simple_graph)
        connectivity_counts[edge_connectivity] += 1

        if edge_connectivity > 3:
            colorable, _ = is_edge_k_colorable(
                nx.convert_node_labels_to_integers(simple_graph),
                5,
            )
            if colorable:
                print("error: graph is colorable")

            print(nx.to_graph6_bytes(simple_graph).decode())
            print("---edge-connectivity", edge_connectivity)

    print("---", connectivity_counts)

if __name__ == "__main__":
    main()
