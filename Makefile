setup: install build

install:
	uv sync .

test:
	uv run pytest

test_coverage:
	uv run pytest --cov=gendiff --cov-report=lcov:coverage.info

lint:
	uv run ruff check

check: test lint

build:
	uv build

.PHONY: install test lint selfcheck check build