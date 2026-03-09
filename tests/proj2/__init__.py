import marimo

__generated_with = "0.15.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    ## EXPORT

    def greet(name: str) -> str:
        return f"Hello, {name}!"
    return


@app.cell
def _():
    ## EXPORT

    class Tokenizer:
        def __init__(self, sep: str = " "):
            self.sep = sep

        def tokenize(self, text: str) -> list[str]:
            return text.split(self.sep)
    return


@app.cell
def _():
    def _private_helper():
        return 42
    return


@app.cell
def _():
    # This cell is for interactive exploration, not exported.
    result = greet("world")
    mo.md(f"Result: {result}")
    return


@app.cell
def _():
    ## EXPORT

    DEFAULT_SEP = " "
    return


if __name__ == "__main__":
    app.run()
