"""Install runtime and dev dependencies from the Python project's pyproject.toml."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tomllib


def main() -> None:
    pyproject_path = pathlib.Path("python/pyproject.toml")
    project = tomllib.loads(pyproject_path.read_text())["project"]

    dependencies = [
        *project.get("dependencies", []),
        *project.get("optional-dependencies", {}).get("dev", []),
    ]

    subprocess.check_call([sys.executable, "-m", "pip", "install", *dependencies])


if __name__ == "__main__":
    main()
