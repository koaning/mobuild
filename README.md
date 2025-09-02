# mobuild

This package let's you construct Python packages from notebooks. You can add "## EXPORT" to cells that need to be moved and then use the utilities from this library to construct Python projects that you can install with uv. 

> Install via `uv pip install mobuild` or run directly via `uvx mobuild`. 

## Cli Features

### `export`

Turn a folder of Marimo notebooks into plain Python files in an output folder.

```bash
uvx mobuild export path/to/nbs path/to/output_src
```

### `init`

Create a new project from the bundled template.

```bash
uvx mobuild init my_project_name --output-folder .
```

## Python API 

### `runtime_sync` from the notebook 

Write the current marimo notebook to a Python file in an output folder.

```python
from mobuild import runtime_sync

runtime_sync("src/package_name")
```
