#!/usr/bin/env bash
set -o errexit
pip install - requirements.txt
python manage.py makemigrations
python manage.py migrate
