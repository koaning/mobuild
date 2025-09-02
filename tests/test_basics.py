import shutil
import tempfile
from mobuild import export, init
from pathlib import Path
import pytest

@pytest.fixture
def tmpdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

def test_basics(tmpdir):
    out_dir = tmpdir / "proj1_out"
    out_dir.mkdir()
    export(input_folder="tests/proj1/", output_folder=out_dir)
    out = (out_dir / "__init__.py").read_text()
    assert "a = 1" in out
    assert "b = 2" not in out

def test_init(tmpdir):
    out_dir = tmpdir / "output"
    init(name="output", output_folder=tmpdir)
    print(list(out_dir.glob("*")))
    assert (out_dir / "nbs" / "__init__.py").exists()
    assert (out_dir / "pyproject.toml").exists()
