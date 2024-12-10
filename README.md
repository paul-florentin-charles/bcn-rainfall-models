# bcn-rainfall-models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## Requirements

- Python 3.12
- Pip
- Coverage.py / Pytest

## Get started

1. Clone repository
2. Install dependencies
3. Run **FastAPI** with Uvicorn
4. Open [Swagger UI](http://127.0.0.1:8000/docs)
5. Run **Flask**
6. Open [Webapp](http://127.0.0.1:5000)

### Linux Setup

```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-models.git
cd bcn-rainfall-models
pip install -r requirements.txt
```

### Windows Setup

```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-models.git
cd bcn-rainfall-models
python -m pip install -r requirements.txt
```

### Run servers

#### Run **API**

`python run.py --server api`

#### Run **Webapp**

`python run.py --server webapp`

## Coverage

### Linux
```commandline
coverage run -m pytest tst
coverage report
```

### Windows
```commandline
python -m coverage run -m pytest tst
python -m coverage report
```