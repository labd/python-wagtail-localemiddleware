
install:
	uv sync

test:
	uv run pytest

retest:
	uv run pytest -vvv --lf

coverage:
	uv run pytest --cov=labd.middleware.locale --cov-report=term-missing --cov-report=html

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

release:
	rm -rf dist/*
	uv build
	uv publish
