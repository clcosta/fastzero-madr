#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 madr:app
