import sys
import networkx as nx

def is_overfull(G):
    """
    Checks if a graph G is overfull.
    A graph G is overfull if |E| > delta(G) * floor(|V|/2).
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    
    if n == 0:
        return False
        
    degrees = [d for n, d in G.degree()]
    delta = max(degrees) if degrees else 0
    
    # Condition: |E| > delta * floor(n/2)
    return m > delta * (n // 2)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_overfull.py <g6_string>")
        sys.exit(1)
        
    g6_str = sys.argv[1]
    try:
        if g6_str.startswith(":"):
            G = nx.from_graph6_bytes(g6_str.encode())
        else:
            G = nx.from_graph6_bytes(g6_str.encode())
    except Exception as e:
        print(f"Error parsing g6: {e}")
        sys.exit(1)

    G.remove_node(0)

    n = G.number_of_nodes()
    m = G.number_of_edges()
    degrees = [d for node, d in G.degree()]
    delta = max(degrees) if degrees else 0
    
    overfull = is_overfull(G)
    
    print(f"Nodes (n): {n}")
    print(f"Edges (m): {m}")
    print(f"Max degree (delta): {delta}")
    print(f"Threshold (delta * floor(n/2)): {delta * (n // 2)}")
    print(f"Is overfull: {overfull}")

if __name__ == "__main__":
    main()
