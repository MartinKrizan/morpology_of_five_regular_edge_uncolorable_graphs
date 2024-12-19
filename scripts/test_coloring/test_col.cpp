#include <iostream>

#include <impl/basic/include.hpp>
#include <io.hpp>
#include <invariants.hpp>

using namespace ba_graph;

int main(int argc, char** argv) {
    std::string filename = argv[1];

    std::ifstream inputFile(filename);

    std::string line;
    int i = 0;
    while (std::getline(inputFile, line)) {
        i++;
        if (i%100000 == 0){
            std::cerr << i << std::endl;
        }
        Graph graph = read_graph6_line(line);
        bool isCol = is_edge_colourable_basic(graph, 5);

        if (!isCol){
            std::cout << line << std::endl;
        }
    }

    return 0;
}

