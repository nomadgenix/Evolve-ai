"""
Database connection testing script for Evolve backend.
This script tests the database connection and validates model mappings.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, check_db_connection
from app.models import User, Agent, Execution, ExecutionLog, Tool, AgentTool
import logging
from sqlalchemy import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test database connection."""
    logger.info("Testing database connection...")
    if check_db_connection():
        logger.info("Database connection successful!")
        return True
    else:
        logger.error("Database connection failed!")
        return False

def validate_models():
    """Validate that all models are properly mapped to database tables."""
    logger.info("Validating model mappings...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    models = [User, Agent, Execution, ExecutionLog, Tool, AgentTool]
    model_tables = [model.__tablename__ for model in models]
    
    logger.info(f"Database tables: {tables}")
    logger.info(f"Model tables: {model_tables}")
    
    missing_tables = [table for table in model_tables if table not in tables]
    if missing_tables:
        logger.error(f"Missing tables: {missing_tables}")
        return False
    
    logger.info("All models are properly mapped to database tables.")
    return True

def test_session():
    """Test database session creation and querying."""
    logger.info("Testing database session...")
    db = SessionLocal()
    try:
        # Try a simple query
        user_count = db.query(User).count()
        logger.info(f"User count: {user_count}")
        logger.info("Database session test successful!")
        return True
    except Exception as e:
        logger.error(f"Database session test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    connection_ok = test_connection()
    models_ok = validate_models() if connection_ok else False
    session_ok = test_session() if connection_ok else False
    
    if connection_ok and models_ok and session_ok:
        logger.info("All database tests passed!")
        sys.exit(0)
    else:
        logger.error("Database tests failed!")
        sys.exit(1)
