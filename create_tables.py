"""
Database migration script for Evolve backend.
This script creates the initial database tables based on SQLAlchemy models.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import User, Agent, Execution, ExecutionLog, Tool, AgentTool

def create_tables():
    """Create all tables defined in the models."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

def drop_tables():
    """Drop all tables defined in the models."""
    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_tables()
    create_tables()
