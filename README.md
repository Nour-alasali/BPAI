# BPAI

### This repository has the data and code used for the research project "Flavours of History: Exploring Historical and Cultural Connections Through Ingredient Analysis Using NLP and Knowledge Graphs"
RQ: How can the analysis of culinary ingredients through NLP and knowledge graphs reveal historical connections and cultural exchanges between different global cultures?

## Setup

Use a terminal in the repository root for all commands below. The setup uses
Python **3.11.16**, pinned in `.python-version`, and exact dependency versions and
package hashes recorded in `uv.lock`.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed.
The setup was prepared with uv **0.12.12**; with an existing Python installation:

```sh
python -m pip install uv==0.12.12
```

Create the project environment and verify it:

```sh
uv sync --locked
uv run --locked python scripts/check_environment.py
```

`uv sync` downloads the pinned Python version if necessary, creates `.venv`, and
installs the locked packages, including the `en_core_web_sm` **3.8.0** model.
The first installation needs internet access to Python's package index, GitHub,
and uv's Python downloads. No separate spaCy model download is needed.
`--locked` rejects dependency changes that have not been recorded in the lockfile.

Launch JupyterLab using the same environment:

```sh
uv run --locked python -m ipykernel install --sys-prefix --name bpai --display-name "Python (BPAI)"
uv run --locked jupyter lab BPAI.ipynb
```

Select the **Python (BPAI)** kernel. The registration command installs it inside
the project environment; repeat it if you recreate `.venv` or move the project.
Run the notebook from the first cell
downward. The preprocessing reads the bundled `data/` directory and can take
time; the graph-generation cell writes `recipes.ttl` in the repository
root. Run the cells under **Queries** after graph generation. The final **Map**
cell launches an interactive Dash app and needs live Wikidata and map-tile access.
The locked Dash 2.18.2 environment supports the notebook's `app.run()` call.

The environment check loads every imported notebook module, runs the NLP model,
checks an RDF/SPARQL query, and checks the Dash startup API. It does not
execute the complete dataset analysis or access Wikidata.


## Repository structure
data/: Contains the dataset used in the research (Yummly-66k dataset in JSON format).

BPAI.ipynb: Contains the Jupyter Notebook used for data preprocessing, analysis, and visualisation.

recipes.ttl: Generated Turtle knowledge graph; created by the notebook and not tracked in Git.

pyproject.toml / uv.lock / .python-version: Dependency declarations, locked environment, and Python version.

scripts/check_environment.py: Quick check of notebook imports and core runtime functionality.

images/: Contains images used in the report and for analysis purposes.

README.md: This document.

Data source: http://123.57.42.89/FoodComputing__Dataset.html
