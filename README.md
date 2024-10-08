# bcn-rainfall-models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![coverage badge](coverage.svg)](https://github.com/nedbat/coveragepy)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MyPy](https://camo.githubusercontent.com/247d658e0d85ae9cc243d7bd73e1c22cf5d30fca1f060328362f2da86b9c31de/68747470733a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](https://mypy-lang.org/)

🚧 **Work In Progress** 🚧

## Requirements

- Python 3.12
- Pip
- Coverage.py / Pytest (coverage, tests)

## Get started

1. Clone repository
2. Install dependencies
3. Execute `app.py` to run FastAPI with Uvicorn
4. Open [Swagger UI](http://127.0.0.1:8000/docs)

### Linux
```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-models.git
cd bcn-rainfall-models
pip install -r requirements.txt
python app.py
```

### Windows
```commandline
git clone https://github.com/paul-florentin-charles/bcn-rainfall-models.git
cd bcn-rainfall-models
python -m pip install -r requirements.txt
python app.py
```

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