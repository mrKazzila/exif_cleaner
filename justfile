#!/usr/bin/env just --justfile


# ===== Linters & Formatter automation =====
lint:
	@echo "Start linters ..."
	- ruff check --fix --silent .
	- ruff format --silent .
	@echo "Linters done!"
