#!/usr/bin/env just --justfile


# ===== Linters & Formatter automation =====
format:
	@echo "Start linters ..."
	- ruff check --fix --silent .
	- ruff format --silent .
	@echo "Linters done!"


lint:
    @echo "Start pyright ..."
    - pyright app
    @echo "Pyright done!"
