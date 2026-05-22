#!/bin/sh
# Start script for ChickOrder backend.
# 1. Runs Alembic migrations to bring the DB schema up to date.
# 2. Seeds the database with admin user and sample products (idempotent).
# 3. Starts the uvicorn server.

set -e  # Exit immediately if any command fails

echo "==> Running database migrations..."
alembic upgrade head

echo "==> Seeding database (admin user + sample products)..."
python init_db.py

echo "==> Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
