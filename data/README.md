# Data

This directory contains graph data used by the project.

## Directories

- [`uncol/`](uncol/) - known 5-regular edge-uncolorable simple graphs.
- [`multigraphs/`](multigraphs/) - uncolorable 5-regular multigraph lists.
- [`benchmark/`](benchmark/) - graph instances used for solver benchmarks.
- [`all_graphs/`](all_graphs/) - placeholder for generated full graph lists;
  large generated files are not committed here.


Graph6 files use one graph per line. Multigraph files under `multigraphs/`
use nauty simple text output unless the local README states otherwise.
