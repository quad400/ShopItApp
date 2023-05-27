#!/bin/bash

APP_PORT=${PORT:-8000}

cd /app/

opt/venv/bin/python manage.py collectstatic --noinput
opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/gunicorn app:wsgi:application --bind "0.0.0.0:$APP_PORT"