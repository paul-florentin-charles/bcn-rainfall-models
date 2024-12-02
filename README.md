# bcn-rainfall-models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MyPy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

🚧 **Work In Progress** 🚧

## Requirements

- Python 3.12
- Pip
- Coverage.py / Pytest (coverage, tests)

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

1. Run **API**
   1. `uvicorn back.api.app:fastapi_app` via _Uvicorn_ command
   2. `python run.py --server api` via _Python_ script
2. Run **Webapp**
   1. `flask --app webapp.flask_app run` via _Uvicorn_ command
   2. `python run.py --server webapp` via _Python_ script

_N. B._ – Better to use it via Python since script runs server using settings written in `config.yml`.

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