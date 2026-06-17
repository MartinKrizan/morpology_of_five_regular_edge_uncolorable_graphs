# Morphology of 5-Regular Edge-Uncolorable Graphs

This repository contains data, scripts, and Python tools for studying
5-regular graphs that are not edge-colorable with 5 colors.

The project currently focuses on:

- enumerating and filtering 5-regular graphs and multigraphs,
- checking edge colorability with CP-SAT based tools,
- detecting overfull substructures and low edge cuts,
- searching for 5-pole gadgets with constrained boundary behavior,
- collecting benchmark instances for edge-coloring solvers.

## Repository Layout

- [`python/`](python/) - installable Python package and command-line tools.
- [`data/`](data/) - graph lists used by the experiments.
- [`scripts/`](scripts/) - generation and legacy checking scripts.
- [`output/`](output/) - generated gadget-category output.
- [`docs/`](docs/) - research notes and longer explanations.
- [`python/benchmark/`](python/benchmark/) - benchmark runner and historical results.

## Setup

The Python package is installed from the `python/` directory.

```sh
python -m pip install -e ./python
```

For development, install the optional test dependency:

```sh
python -m pip install -e './python[dev]'
```

The Docker image provides a reproducible environment with the package and
external graph-generation tools.

```sh
docker compose build
docker compose run --rm python generate-overfull 9 --count 3
```

## Command-Line Tools

The package exposes these commands:

- `chcol` - check edge colorability for a graph instance.
- `check-overfull` - test graphs for overfullness.
- `filter-by-colorable-cut` - filter graphs by colorability after cuts.
- `filter-low-con` - filter graphs by low edge connectivity.
- `filter-uncol` - keep graphs that are not edge-colorable with 5 colors.
- `generate-overfull` - generate overfull graph candidates.
- `gadget-categorize` - group generated 5-poles by port-pair constraints.
- `gadget-search` - search for 5-pole gadgets with boundary-signature data.

Most filter commands read graph data from standard input. For example:

```sh
docker compose run --rm python filter-uncol < data/multigraphs/uncol_8_m2_all_small.txt
```

See [`python/README.md`](python/README.md) for package and CLI details.

## Tests

Run the Python tests with:

```sh
docker compose run --rm python python -m pytest python/tests
```

or, after local installation:

```sh
python -m pytest python/tests
```

## Data

The main data sets are documented under [`data/`](data/):

- [`data/uncol/`](data/uncol/) contains known 5-regular edge-uncolorable simple
  graphs on 14 and 16 vertices.
- [`data/multigraphs/`](data/multigraphs/) contains uncolorable 5-regular
  multigraph lists with maximum edge multiplicity 2.
- [`data/benchmark/`](data/benchmark/) contains benchmark graph instances.

## Notes

Longer research notes are kept separate from the quickstart:

- [`docs/research-notes.md`](docs/research-notes.md)
- [`docs/gadget-search.md`](docs/gadget-search.md)

All commands, files, and prose use the standard term `overfull`.
