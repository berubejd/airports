.PHONY: test lint format clean build

test:
	pytest

coverage:
	pytest --cov=airports --cov-report=term-missing

lint:
	flake8 .
	black . --check
	isort . --check

format:
	black .
	isort .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	python -m build