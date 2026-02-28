#!/bin/bash

# Exit on any error
set -e

echo "Starting project setup..."

# Install System Dependencies
echo "Installing Python, PostgreSQL, and curl..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip postgresql postgresql-contrib curl redis-server openjdk-17-jdk
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list'
sudo apt update
sudo apt install elasticsearch -y
sudo systemctl start elasticsearch.service

# Install uv package manager
echo "Installing uv..."
if ! command -v uv &> /dev/null
then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "uv is already installed"
fi

# 1. Install dependencies using uv
echo "Installing dependencies..."
uv sync

# 2. Generate new migrations
echo "Generating migrations..."
uv run python manage.py makemigrations

# 3. Apply shared schema migrations
echo "Applying shared schema migrations..."
uv run python manage.py migrate_schemas --shared

# 4. Apply tenant schema migrations
echo "Applying tenant schema migrations..."
uv run python manage.py migrate_schemas --tenant

echo "Setup successfully completed! "
echo "You can now run the server with: uv run python manage.py runserver"
