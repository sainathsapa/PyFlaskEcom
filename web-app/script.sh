#!/bin/sh
source venv/bin/activate
gunicorn -b :7731 --access-logfile - --error-logfile - wsgi:app