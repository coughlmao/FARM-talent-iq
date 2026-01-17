# Makefile - Project automation scripts

# .PHONY tells Make that these are "command names" and not "actual files".
# (Explanation below the code block)
.PHONY: install compile lint

# Sync your local environment with the locked dependencies
install:
	pip install -r requirements/dev.txt
	pre-commit install

# Convert requirements.in files into locked requirements.txt files
# Run this whenever you add or update a library
compile:
	pip-compile requirements/base.in -o requirements/base.txt
	pip-compile requirements/dev.in -o requirements/dev.txt

# The "Auto-Fixer": Corrects code style and logic errors across all files
# 1. 'check --fix' removes unused imports and sorts them
# 2. 'format' fixes spacing, indentation, and quotes
lint:
	ruff check --fix .
	ruff format .

# Development Mode
# Uses 'fastapi dev' which enables auto-reload and useful debugging features.
dev:
	fastapi dev app/main.py

# Production MODE
# Uses 'fastapi run' which optimizes for performance.
# It disables auto-reload and typically spawns multiple workers.
prod:
	fastapi run app/main.py --port 8000