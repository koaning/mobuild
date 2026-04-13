import click
import pytest
from mobuild import export, init


def test_basics(tmp_path):
    out_file = tmp_path / "proj1_out" / "__init__.py"
    export(input_file="tests/proj1/__init__.py", output_path=out_file)
    out = out_file.read_text()
    assert "a = 1" in out
    assert "b = 2" not in out
    assert "## export" not in out.lower()  # Marker should be stripped
    assert '__all__' in out
    assert "'a'" in out


def test_custom_output_name(tmp_path):
    """The user can pick any file name for the output."""
    out_file = tmp_path / "my_module.py"
    export(input_file="tests/proj1/__init__.py", output_path=out_file)
    out = out_file.read_text()
    assert "a = 1" in out
    assert '__all__' in out


def test_selective_export(tmp_path):
    """Only cells marked with ## EXPORT should appear in the output."""
    out_file = tmp_path / "proj2_out" / "__init__.py"
    export(input_file="tests/proj2/__init__.py", output_path=out_file)
    out = out_file.read_text()

    # Exported definitions should be present
    assert "def greet" in out
    assert "class Tokenizer" in out
    assert "DEFAULT_SEP" in out

    # Non-exported code should be absent
    assert "_private_helper" not in out
    assert "mo.md" not in out
    assert 'result = greet("world")' not in out

    # Export markers should be stripped
    assert "## export" not in out.lower()

    # __all__ should list only public exported names
    assert "__all__" in out
    assert "'greet'" in out
    assert "'Tokenizer'" in out
    assert "'DEFAULT_SEP'" in out
    assert "_private_helper" not in out



def test_folder_is_not_sufficient(tmp_path):
    """Passing a directory instead of a file path should fail."""
    out_dir = tmp_path / "some_folder"
    out_dir.mkdir()
    with pytest.raises(click.exceptions.Exit):
        export(input_file="tests/proj1/__init__.py", output_path=out_dir)


def test_init(tmp_path):
    out_dir = tmp_path / "output"
    init(name="output", output_folder=tmp_path)
    assert (out_dir / "nbs" / "__init__.py").exists()
    assert (out_dir / "pyproject.toml").exists()
