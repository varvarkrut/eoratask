PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTHON_VENV := $(VENV)/bin/python

.PHONY: help env install setup clean run

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-12s %s\n", $$1, $$2}'

env: ## Create venv
	$(PYTHON) -m venv $(VENV)

install: ## Install dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

setup: ## Setup project
	$(PYTHON_VENV) setup.py

run: ## Run chat bot
	$(PYTHON_VENV) chat_bot.py