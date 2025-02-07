# bcn-rainfall-models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

> As of 07/02/2025, project is split into 2 main entities:
> 1. A "backend" made of:
>    1. **Custom classes** to easily load and manipulate _rainfall data_ from Barcelona.
>    2. An **API** written with FastAPI that exposes this data.
> 2. A **Webapp** run with Flask that calls the latter API to display data.
>
> The idea is the mid-run would be to split both entities into different repositories. 
> 
> Perhaps even make 3 repositories, and package them by the following order of priority:
> 1. Custom classes
> 2. API
> 3. Webapp

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

`uv run run.py api`

#### Run **Webapp**

`uv run run.py webapp`

## Tests & Coverage

```commandline
uv run coverage run -m pytest
uv run coverage report
```

## Code quality

```commandline
uv tool run mypy --check-untyped-defs .
uv tool run ruff check
uv tool run ruff format
```

---

<center>🄯 2023-2025 Paul Charles</center>