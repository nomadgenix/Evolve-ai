#!/usr/bin/env python3
"""
Helper script to verify and fix Celery worker import paths
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

# Print current Python path for debugging
print("Current PYTHONPATH:")
for path in sys.path:
    print(f"  - {path}")

# Try importing required modules to verify they're available
try:
    import sqlalchemy
    print("✓ SQLAlchemy imported successfully")
except ImportError:
    print("✗ Failed to import SQLAlchemy")

try:
    import celery
    print("✓ Celery imported successfully")
except ImportError:
    print("✗ Failed to import Celery")

# Create a simple worker module if it doesn't exist
worker_path = '/app/superagi/worker.py'
if os.path.exists(worker_path):
    print(f"✓ Worker module exists at {worker_path}")
else:
    print(f"✗ Worker module not found at {worker_path}")

print("\nEnvironment variables:")
for key, value in os.environ.items():
    if key in ['PYTHONPATH', 'PATH', 'CELERY_APP']:
        print(f"  - {key}: {value}")
