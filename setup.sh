#!/bin/bash

# Setup script for Evolve backend
# This script sets up the environment and initializes the database

# Create necessary directories
mkdir -p /home/ubuntu/manus_free_alternative/evolve_backend/app/services
mkdir -p /home/ubuntu/manus_free_alternative/evolve_backend/app/routers
mkdir -p /home/ubuntu/manus_free_alternative/evolve_backend/migrations

# Create __init__.py files for Python packages
touch /home/ubuntu/manus_free_alternative/evolve_backend/app/services/__init__.py
touch /home/ubuntu/manus_free_alternative/evolve_backend/app/routers/__init__.py
touch /home/ubuntu/manus_free_alternative/evolve_backend/migrations/__init__.py

# Set up virtual environment
echo "Setting up virtual environment..."
cd /home/ubuntu/manus_free_alternative/evolve_backend
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
cd /home/ubuntu/manus_free_alternative/evolve_backend
python migrations/create_tables.py

# Seed database with initial data
echo "Seeding database..."
python migrations/seed_db.py

# Test database connection
echo "Testing database connection..."
python migrations/test_db.py

echo "Setup completed successfully!"
