install:
	uv venv --allow-existing
	uv pip install -e ".[dev]"

test:
	uv run pytest

pypi:
	uv build
	uv publish
