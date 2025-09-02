import shutil 
from mobuild import build
from pathlib import Path


def test_basics():
    if Path("tests/proj1_out/").exists():
        shutil.rmtree("tests/proj1_out/")
    build(input_folder="tests/proj1/", output_folder="tests/proj1_out/")
    out = Path("tests/proj1_out/__init__.py").read_text()
    assert "a = 1" in out
    assert "b = 2" not in out
    shutil.rmtree("tests/proj1_out/")
