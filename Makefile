VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install run migrate makemigrations createsuperuser test lint fmt check

venv:
	python3.11 -m venv $(VENV)
	$(PIP) install -U pip wheel

install: venv
	$(PIP) install -r requirements.txt

run:
	$(PY) manage.py runserver 0.0.0.0:8000

migrate:
	$(PY) manage.py migrate

makemigrations:
	$(PY) manage.py makemigrations

createsuperuser:
	$(PY) manage.py createsuperuser

test:
	$(PY) -m pytest -q

lint:
	$(VENV)/bin/ruff check .

fmt:
	$(VENV)/bin/ruff format .

check: lint test
