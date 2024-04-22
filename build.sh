#!/usr/bin/env bash
# exit on error
set -o errexit

make install && poetry run python manage.py migrate