# Contributing

## Development setup

```bash
git clone https://github.com/Sam-Razavi/bostadspuls.git
cd bostadspuls
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

## Linting

```bash
ruff check .
ruff format .
```

## Commit convention

Conventional Commits — prefix every commit:

- `feat:` new feature
- `fix:` bug fix
- `chore:` tooling, deps, config
- `docs:` documentation only
- `test:` tests only
- `ci:` CI/CD changes
- `style:` formatting, no logic change

## Branch naming

- `feat/<name>` — new feature
- `fix/<name>` — bug fix
- `chore/<name>` — maintenance
- `docs/<name>` — docs only
- `ci/<name>` — CI changes

## Pull requests

- One feature per PR.
- All tests must pass.
- `ruff check .` must be clean.
- Every dbt model must have a description and at least one test.
