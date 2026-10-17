# CNPJ Checker

![CI](https://github.com/devbelloni/CNPJ_verificator/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

Validate Brazilian company IDs (**CNPJ**) and look companies up through the public
[BrasilAPI](https://brasilapi.com.br). It is available as a Python library, a command-line
tool and a small Tkinter desktop app.

## Features

- **Offline validation** of the two check digits (weighted modulo 11), so malformed input
  never costs a network request.
- **Alphanumeric CNPJ support**, the new format in force since 2026, in addition to the
  classic numeric one.
- **Typed errors**: `InvalidCNPJ`, `CompanyNotFound` and `ApiError` instead of generic
  exceptions, plus request timeouts and network-failure handling.
- **Clean architecture**: validation, HTTP client and GUI are separate modules; the client
  accepts an injectable session, which makes it fully testable without internet.

## Install

```bash
pip install -e ".[dev]"
```

## Use it

Command line:

```bash
python -m cnpj_checker 11.222.333/0001-81
```

Desktop app (no arguments):

```bash
python -m cnpj_checker
```

Library:

```python
from cnpj_checker import fetch_company, is_valid_cnpj, format_cnpj

is_valid_cnpj("12.ABC.345/01DE-35")     # True (alphanumeric format)
format_cnpj("11222333000181")           # '11.222.333/0001-81'

company = fetch_company("11.222.333/0001-81")
print(company.legal_name, company.main_activity, company.city, company.state)
```

## Tests

```bash
pytest -q && ruff check .
```

17 tests cover valid and invalid numbers (numeric and alphanumeric), formatting, the HTTP
client with a fake session (success, 404, server error, network failure) and the CLI.

## Project layout

```
src/cnpj_checker/
├── validator.py   # check digits, cleaning, formatting
├── client.py      # BrasilAPI client and Company model
├── gui.py         # Tkinter app
└── __main__.py    # CLI / GUI entry point
tests/
```

## Author

**Márcio Belloni**, AI/ML Engineer.
[LinkedIn](https://www.linkedin.com/in/marcio-belloni/) · [GitHub](https://github.com/devbelloni)
