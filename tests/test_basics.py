from mobuild import build
from pathlib import Path


def test_basics():
    build("tests/proj1", "tests/proj1_out")
    out = Path("tests/proj1_out/__init__.py").read_text()
    assert "a = 1" in out
    assert "b = 2" not in out