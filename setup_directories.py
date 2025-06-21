import os
from pathlib import Path

# Create necessary directories
os.makedirs("/home/ubuntu/manus_free_alternative/evolve_backend/app/services", exist_ok=True)

# Create __init__.py files for proper Python package structure
Path("/home/ubuntu/manus_free_alternative/evolve_backend/app/services/__init__.py").touch()
Path("/home/ubuntu/manus_free_alternative/evolve_backend/app/routers/__init__.py").touch()

# Create main entry point
print("Creating main entry point for Evolve backend...")
