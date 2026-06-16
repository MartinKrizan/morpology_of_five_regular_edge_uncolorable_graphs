# Scripts

This directory contains helper scripts that are not part of the installable
Python package.

## Directories

- [`generator/`](generator/) - graph-generation shell scripts.
- [`test_coloring/`](test_coloring/) - legacy C++ edge-coloring checker and
  test runner.

## Files

- [`install_python_deps.py`](install_python_deps.py) - helper for installing
  Python dependencies in environments that need an explicit installer script.

Prefer the installable Python commands for new workflows. The scripts here are
kept for reproducibility of older data-generation and filtering steps.
