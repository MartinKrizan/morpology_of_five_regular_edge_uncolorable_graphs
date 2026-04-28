import networkx as nx
from functions_d.add_edge import add_edge, add_two_edges
from functions_d.is_colorable import is_edge_k_colorable
import matplotlib.pyplot as plt
from functions_d.draw_multigraph import draw_multigraph


def main():
    G =nx.MultiGraph()
    
    for i in range(0,9):
        G.add_edge(f"{i}_1", f"{i}_2")
        G.add_edge(f"{i}_1", f"{i}_2")
    
    
    G.add_edge(f"0_1", f"3_1")
    G.add_edge(f"0_1", f"4_1")
    G.add_edge(f"0_1", f"5_1")
    G.add_edge(f"1_1", f"3_1")
    G.add_edge(f"1_1", f"4_1")
    G.add_edge(f"1_1", f"5_1")
    G.add_edge(f"2_1", f"3_1")
    G.add_edge(f"2_1", f"4_1")
    G.add_edge(f"2_1", f"5_1")

    G.add_edge(f"6_1", f"3_2")
    G.add_edge(f"6_1", f"4_2")
    G.add_edge(f"6_1", f"5_2")
    G.add_edge(f"7_1", f"3_2")
    G.add_edge(f"7_1", f"4_2")
    G.add_edge(f"7_1", f"5_2")
    G.add_edge(f"8_1", f"3_2")
    G.add_edge(f"8_1", f"4_2")
    G.add_edge(f"8_1", f"5_2")

    
    G.add_edge(f"6_2", f"0_2")
    G.add_edge(f"6_2", f"1_2")
    G.add_edge(f"6_2", f"2_2")
    G.add_edge(f"7_2", f"0_2")
    G.add_edge(f"7_2", f"1_2")
    G.add_edge(f"7_2", f"2_2")
    G.add_edge(f"8_2", f"0_2")
    G.add_edge(f"8_2", f"1_2")
    G.add_edge(f"8_2", f"2_2")
    
    
    print(nx.degree_histogram(G))
    print(nx.edge_connectivity(G))
    print(is_edge_k_colorable(G,5))
    draw_multigraph(G)
    
    
if __name__ == "__main__":
    main()