CFLAGS = -std=c++20 -fopenmp -I../../ba-graph/include
LDFLAGS =
DBGFLAGS = -g -O0 -pedantic -Wall -Wextra -DBA_GRAPH_DEBUG
COMPILE_DBG = $(CXX) $(CFLAGS) $(DBGFLAGS)
COMPILE = $(CXX) $(CFLAGS) -DNDEBUG -O3

test_col:
	$(COMPILE) test_col.cpp -o test_col $(LDFLAGS)



clean:
	rm -rf *.out

