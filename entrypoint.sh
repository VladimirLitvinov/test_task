#!/bin/bash
set -e
cd app/
poetry run alembic upgrade head
exec poetry run uvicorn main:app --host 0.0.0.0 --port 8000