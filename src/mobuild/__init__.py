import ast
import hashlib
import importlib.util
import re
import sys

from cookiecutter.main import cookiecutter
from marimo._ast.app import InternalApp
from pathlib import Path
import typer

app = typer.Typer(no_args_is_help=True)

_EXPORT_MARKER = re.compile(r"^## export\s*$", re.IGNORECASE | re.MULTILINE)


def _collect_top_level_names(code: str) -> list[str]:
    """Return public top-level names defined in *code* (skip _private names)."""
    names = []
    for node in ast.parse(code).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.append(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if not node.target.id.startswith("_"):
                names.append(node.target.id)
    return names


def _write_file(file: Path, out_path: Path):
    """Extract exported code from a single marimo notebook and write it as a plain Python file.

    Marimo notebooks are valid Python files. Each notebook defines a global ``app``
    object (a ``marimo.App``) whose cells are decorated functions. Internally, marimo
    represents these cells as a directed acyclic graph (DAG) where edges encode
    data dependencies between cells.

    This function:
      1. Dynamically imports the notebook file to obtain its ``app`` object.
      2. Wraps it in ``InternalApp`` to access the cell graph and topological
         execution order.
      3. Selects only cells whose source code contains the ``## EXPORT`` marker.
      4. Concatenates those cells in execution order (respecting the DAG) and
         writes the result to ``out_path``.
      5. Prepends an ``__all__`` so the generated module only exposes the
         public names that were explicitly exported.

    The ``## EXPORT`` marker itself is stripped from the output so the resulting
    file is clean library code.
    """
    abs_path = str(file.resolve())
    mod_name = "mobuild_runtime_" + hashlib.sha1(abs_path.encode()).hexdigest()[:10]
    spec = importlib.util.spec_from_file_location(mod_name, abs_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {abs_path}")
    module = importlib.util.module_from_spec(spec)
    try:
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    finally:
        # Ensure no global pollution
        sys.modules.pop(mod_name, None)

    # Every marimo notebook exposes an `app` object (a marimo.App instance).
    notebook = getattr(module, "app")

    # InternalApp gives access to the cell DAG and the topological execution order.
    internal = InternalApp(notebook)

    # execution_order is a list of cell IDs sorted so that dependencies come first.
    order = internal.execution_order

    # internal.graph.cells maps cell_id -> CellData. Each CellData has:
    #   .code      -- the Python source of that cell
    #   .language  -- "python" or "markdown" (marimo supports markdown cells)
    exported_cells = {
        cell_id: cell.code
        for cell_id, cell in internal.graph.cells.items()
        if cell.language == "python" and _EXPORT_MARKER.search(cell.code)
    }

    code_export = ""
    for cell_id in order:
        if cell_id in exported_cells:
            cleaned = _EXPORT_MARKER.sub("", exported_cells[cell_id])
            code_export += cleaned + "\n"

    names = _collect_top_level_names(code_export)
    if names:
        code_export = "__all__ = " + repr(names) + "\n\n" + code_export

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code_export)


@app.command(no_args_is_help=True)
def export(input_file: Path, output_path: Path):
    """Build a Python file from a single Marimo notebook."""
    input_file = Path(input_file)
    output_path = Path(output_path)
    if not input_file.exists():
        typer.echo(f"Input file {input_file} does not exist")
        raise typer.Exit(1)
    if output_path.is_dir():
        typer.echo(f"Output path {output_path} is a directory, please provide a file path")
        raise typer.Exit(1)
    _write_file(input_file, output_path)


@app.command(no_args_is_help=True)
def init(name: str, output_folder: Path = Path(".")):
    """Render a new project into the given output folder.

    Expects the template assets to live under the installed package at
    ``mobuild/static/cookiecutter/`` with a ``cookiecutter.json``.
    """
    cookie_folder = Path(__file__).parent / "static" / "cookiecutter"
    cookiecutter(
        str(cookie_folder),
        output_dir=str(output_folder),
        extra_context={"project_name": name},
        no_input=True,
    )


def runtime_sync(output_path: Path):
    """Write the current marimo notebook to the given output path as a normal Python file."""
    _write_file(Path(__file__), output_path)
