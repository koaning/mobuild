install: 
    uv venv --allow-existing
    source .venv/bin/activate
    uv pip install -e . pytest marimo

test: 
    uv run pytest

clean: 
    rm .DS_Store
