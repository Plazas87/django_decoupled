#!/bin/bash

set -x
DEBUG_PORT=${DEBUG_PORT:-5682}

echo "MIGRATION INIT";
poetry run python -m django_decoupled.controllers.manage migrate --noinput
poetry run python -m django_decoupled.controllers.manage collectstatic --noinput
echo "MIGRATION FINISHED"

echo "RUNNING APPLICATION IN 0.0.0.0:8000..."
poetry run uvicorn --host 0.0.0.0 django_decoupled.controllers.config.asgi:application
