import sys

from morphology_graphs.core.is_colorable import is_multigraph_edge_k_colorable
from morphology_graphs.core.multicode import parse_multicode


def main():
    i=0
    for line in sys.stdin:
        i+=1
        G = parse_multicode(line)
        if(not is_multigraph_edge_k_colorable(G,5)[0]):
            print(line)
            
        if(i%1000 == 0):
            print(f"---{i}")

if __name__ == "__main__":
    main()
