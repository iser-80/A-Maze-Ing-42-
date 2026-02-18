NAME = a_maze_ing.py
CONFIG = config.txt
PYTHON = python3
PIP = pip3

all: install lint run

install:
	$(PIP) install --upgrade flake8 mypy toml

run:
	$(PYTHON) $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: all install run debug clean lint lint-strict