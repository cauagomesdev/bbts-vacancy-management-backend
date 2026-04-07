#!/bin/bash
set -e

echo "⏳  Aguardando PostgreSQL..."
until curl -sf http://db:5432 > /dev/null 2>&1 || \
      python -c "import psycopg2; psycopg2.connect('postgresql://bbts:bbts@db:5432/bbts')" 2>/dev/null; do
  sleep 1
done
echo "✅  PostgreSQL disponível."

echo "🔄  Rodando migrations..."
alembic upgrade head


echo "🚀  Iniciando API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
