# Python Package

The Python package contains reusable graph helpers and command-line tools under
`morphology_graphs`.

Install it in editable mode from the repository root:

```sh
python -m pip install -e ./python
```

Install test dependencies as well:

```sh
python -m pip install -e './python[dev]'
```

## Package Layout

- `morphology_graphs/core/` - graph loading, edge-colorability checks,
  overfull checks, cut splitting, multicode helpers, and gadget utilities.
- `morphology_graphs/cli/` - command-line entry points.
- `tests/` - pytest tests for core behavior and gadget helpers.
- `benchmark/` - benchmark scripts and historical timing results.

## Commands

- `chcol`
- `check-overfull`
- `filter-by-colorable-cut`
- `filter-low-con`
- `filter-uncol`
- `generate-overful`
- `gadget-categorize`
- `gadget-search`

Most filters read graph data from standard input and write matching graphs to
standard output.

Example:

```sh
docker compose run --rm python filter-uncol < data/multigraphs/uncol_8_m2_all_small.txt
```

## Tests

From the repository root:

```sh
python -m pytest python/tests
```

or with Docker:

```sh
docker compose run --rm python python -m pytest python/tests
```
