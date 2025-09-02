from mobuild import main
import importlib
def test_basics():
    main("tests/proj1", "tests/proj1_out")
    out = Path("tests/proj1_out/__init__.py").read_text()
    assert "a = 1" in out
    assert "b = 2" not in out