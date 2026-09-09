"""Check notebook imports and the NLP model without running the full analysis."""

import ast
import importlib
import json
from pathlib import Path
import platform


def main():
    root = Path(__file__).resolve().parents[1]
    expected_python = (root / ".python-version").read_text().strip()
    if platform.python_version() != expected_python:
        raise RuntimeError(
            f"Expected Python {expected_python}, got {platform.python_version()}. "
            "Run this check with uv run --locked python scripts/check_environment.py."
        )

    notebook = json.loads((root / "BPAI.ipynb").read_text(encoding="utf-8"))
    modules = set()
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        for node in ast.walk(ast.parse("".join(cell["source"]))):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)

    for module in sorted(modules):
        importlib.import_module(module)

    import spacy
    from dash import Dash
    from rdflib import Graph

    nlp = spacy.load("en_core_web_sm")
    if nlp.meta["version"] != "3.8.0":
        raise RuntimeError("Expected en_core_web_sm 3.8.0.")
    doc = nlp("Fresh tomatoes and basil.")
    if not any(token.pos_ == "NOUN" for token in doc):
        raise RuntimeError("The NLP model did not produce noun annotations.")

    graph = Graph().parse(data="<urn:recipe> <urn:ingredient> <urn:basil> .", format="turtle")
    result = list(graph.query("SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }"))
    if int(result[0][0]) != 1:
        raise RuntimeError("The RDF/SPARQL smoke check failed.")
    if not callable(Dash(__name__).run):
        raise RuntimeError("Dash does not support the notebook's run API.")

    print(f"Python {platform.python_version()}: OK")
    print(f"All {len(modules)} notebook imports: OK")
    print(f"spaCy {spacy.__version__} / en_core_web_sm {nlp.meta['version']}: OK")
    print("RDF/SPARQL and Dash startup API: OK")
    print("Environment checks passed. Full analysis and live map are separate checks.")


if __name__ == "__main__":
    main()
