import networkx as nx

def read_graphs_from_file(filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # networkx expects bytes for from_graph6_bytes
            try:
                G = nx.from_graph6_bytes(line.encode())
            except Exception as e:
                print(f"Failed to parse line as graph6: {line!r} -> {e}")
                continue
            yield G