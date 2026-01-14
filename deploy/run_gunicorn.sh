#!/usr/bin/env bash
set -euo pipefail

export DJANGO_SETTINGS_MODULE=config.settings.prod
export PYTHONUNBUFFERED=1

exec .venv/bin/gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 2 \
  --access-logfile - \
  --error-logfile -
