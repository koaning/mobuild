import typer 
from marimo._ast.app import InternalApp
from pathlib import Path
import importlib


def build(input_folder: Path = Path("nbs"), output_folder: Path = Path("src")):
    """Build a Python library from a folder of Marimo notebooks."""
    if not Path(input_folder).exists():
        typer.echo(f"Input folder {input_folder} does not exist")
        raise typer.Exit(1)
    files = Path(input_folder).glob("*.py")
    out_folder = Path(output_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    for file in files:
        # Write everything into temp.py to avoid issues with imports of files like __init__.py later
        Path("temp.py").write_text(file.read_text())
        
        try:
            module = importlib.import_module("temp")
            app = getattr(module, "app")
            app = InternalApp(app)
            order = app.execution_order

            codes = {k: v.code for k, v in app.graph.cells.items() if v.language=="python" and "## export" in v.code.lower()}
            print(codes)
            code_export = ""
            for i in order:
                if i in codes:
                    code_export += codes[i].replace("## Export", "") + "\n"
            Path(out_folder / file.name).write_text(code_export)
        except (ImportError, AttributeError) as e:
            print(f"Error loading {file}: {e}")
        Path("temp.py").unlink()
