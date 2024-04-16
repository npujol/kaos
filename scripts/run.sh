#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn kaos.wsgi:application -b :8080 --reload