#!/bin/bash

echo "Starting project cleanup..."

# Remove Python cache directories and files
echo "Removing python cache files (__pycache__, *.pyc)..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove Django migration files (except __init__.py)
echo "Removing Django migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Remove the uv.lock file
echo "Removing uv.lock..."
rm -f uv.lock

# Remove the virtual environment
echo "Removing .venv directory..."
rm -rf .venv

echo "Cleanup successfully completed!"
