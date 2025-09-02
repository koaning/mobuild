install: 
    uv venv --allow-existing
    source .venv/bin/activate
    uv pip install -e . pytest marimo

test:
	uv run pytest

clean:
	rm -rf output/
	rm -rf __pycache__/
	rm -rf .pytest_cache/

build:
	uv run mobuild export nbs src
