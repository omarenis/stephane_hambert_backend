#!/usr/bin/env bash
set -o errexit
poetry install
python manage.py makemigrations
python manage.py migrate
