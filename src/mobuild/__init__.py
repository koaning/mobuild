import typer 
from marimo._ast.app import InternalApp
from pathlib import Path
import importlib
import importlib.util
import hashlib
import sys


def build(input_folder: Path, output_folder: Path):
    """Build a Python library from a folder of Marimo notebooks."""
    if not Path(input_folder).exists():
        typer.echo(f"Input folder {input_folder} does not exist")
        raise typer.Exit(1)
    files = Path(input_folder).glob("*.py")
    out_folder = Path(output_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    for file in files:
        try:
            # Load module uniquely by absolute file path; avoid temp files and sys.path reliance
            abs_path = str(Path(file).resolve())
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

            app = getattr(module, "app")
            app = InternalApp(app)
            order = app.execution_order

            codes = {k: v.code for k, v in app.graph.cells.items() if v.language=="python" and "## export" in v.code.lower()}
            code_export = ""
            for i in order:
                if i in codes:
                    code_export += codes[i].replace("## Export", "") + "\n"
            Path(out_folder / file.name).write_text(code_export)
        except (ImportError, AttributeError) as e:
            typer.echo(f"Error loading {file}: {e}")
            
