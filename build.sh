#!/usr/bin/env bash
set -o errexit
curl -sSL https://install.python-poetry.org | python3.8 -
poetry install
python manage.py makemigrations
python manage.py migrate
