import networkx as nx
import matplotlib.pyplot as plt

def draw_multigraph(G, filename="multigraph.png"):
    """
    Draws a multigraph and saves it to a file.
    Handles multiple edges between the same nodes by using curved lines.
    """
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    
    # Color nodes with degree < 5 differently (e.g., orange)
    node_colors = ['orange' if G.degree(n) != 5 else 'lightblue' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors='black')
    nx.draw_networkx_labels(G, pos)
    
    ax = plt.gca()
    seen_edges = {}
    
    for u, v, key in G.edges(keys=True):
        # Normalize the order for undirected multigraphs to properly count edges
        node1, node2 = (u, v) if u < v else (v, u)
        
        if (node1, node2) not in seen_edges:
            seen_edges[(node1, node2)] = 0
            
        count = seen_edges[(node1, node2)]
        
        # Calculate radius for arc: 0, 0.2, -0.2, 0.4, -0.4, etc.
        if count == 0:
            rad = 0.0
        else:
            rad = 0.2 * ((count + 1) // 2) * (-1 if count % 2 == 1 else 1)
        
        ax.annotate("",
                    xy=pos[node2], xycoords='data',
                    xytext=pos[node1], textcoords='data',
                    arrowprops=dict(arrowstyle="-", color="black",
                                    shrinkA=15, shrinkB=15,
                                    patchA=None, patchB=None,
                                    connectionstyle=f"arc3,rad={rad}",
                                    ),
                    )
        seen_edges[(node1, node2)] += 1
        
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
