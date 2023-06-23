#!/bin/sh


python manage.py collectstatic --no-input

gunicorn sinka97.wsgi:application --bind 0.0.0.0:8000