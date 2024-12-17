# bcn-rainfall-models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## Requirements

- Python 3.12
- Pip

## Get started

1. Clone repository
2. Install dependencies
3. Run **FastAPI** with Uvicorn
   1. Open [Swagger UI](http://127.0.0.1:8000/docs)
4. Run **Flask**
   1. Open [Webapp](http://127.0.0.1:5000)

### Setup

```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-models.git
cd bcn-rainfall-models
pip install uv
uv sync
```

### Run servers

#### Run **API**

`uv run run.py -s api`

#### Run **Webapp**

`uv run run.py -s webapp`

## Tests & Coverage

```commandline
uv run coverage run -m pytest
uv run coverage report
```

## Code quality

```commandline
uv tool install ruff
ruff check
ruff format
```