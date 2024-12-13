# Contributing to Airports

## Development Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment
4. Install dev dependencies: `pip install -r requirements-dev.txt`
5. Install package in editable mode: `pip install -e .`

## Running Tests
```bash
pytest
pytest --cov=airports  # for coverage
```

## Code Style

- We use Black for formatting
- Sort imports with isort
- Follow flake8 guidelines
- Run black . && isort . && flake8 before committing

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md