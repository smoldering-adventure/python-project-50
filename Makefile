setup: install build

install:
	uv sync .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=hexlet_python_package --cov-report 

lint:
	uv run ruff check

check: test lint

build:
	uv build

.PHONY: install test lint selfcheck check build