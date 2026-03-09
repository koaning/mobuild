from mobuild import export, init


def test_basics(tmp_path):
    out_dir = tmp_path / "proj1_out"
    out_dir.mkdir()
    export(input_file="tests/proj1/__init__.py", output_folder=out_dir)
    out = (out_dir / "__init__.py").read_text()
    assert "a = 1" in out
    assert "b = 2" not in out
    assert "## export" not in out.lower()  # Marker should be stripped
    assert '__all__' in out
    assert "'a'" in out


def test_selective_export(tmp_path):
    """Only cells marked with ## EXPORT should appear in the output."""
    out_dir = tmp_path / "proj2_out"
    out_dir.mkdir()
    export(input_file="tests/proj2/__init__.py", output_folder=out_dir)
    out = (out_dir / "__init__.py").read_text()

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



def test_init(tmp_path):
    out_dir = tmp_path / "output"
    init(name="output", output_folder=tmp_path)
    assert (out_dir / "nbs" / "__init__.py").exists()
    assert (out_dir / "pyproject.toml").exists()
