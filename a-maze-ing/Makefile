NAME = a-maze-ing
CONFIG = config.txt
PYTHON = python3
PIP = pip3

all: install lint run

install:
	$(PIP) install --upgrade flake8 mypy toml

run:
	$(PYTHON) -m $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	rm -rf ./mazegen/__pycache__ ./mazegen/.mypy_cache ./__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: all install run debug clean lint lint-strict