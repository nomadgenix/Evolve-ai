"""
Database initialization and seeding script for Evolve backend.
This script initializes the database and seeds it with initial data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models import User, Agent, Tool
from app.routers.auth import get_password_hash
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database by creating all tables."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")

def seed_db():
    """Seed the database with initial data."""
    logger.info("Seeding database with initial data...")
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            logger.info("Database already seeded. Skipping...")
            return
        
        # Create default admin user
        admin_user = User(
            username="admin",
            email="admin@evolve.ai",
            hashed_password=get_password_hash("admin"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info(f"Created admin user with ID: {admin_user.id}")
        
        # Create default tools
        tools = [
            Tool(name="Web Search", description="Search the web for information", icon="search"),
            Tool(name="Calculator", description="Perform calculations", icon="calculator"),
            Tool(name="Weather", description="Get weather information", icon="cloud"),
            Tool(name="Calendar", description="Manage calendar events", icon="calendar"),
            Tool(name="Email", description="Send and read emails", icon="envelope")
        ]
        db.add_all(tools)
        db.commit()
        logger.info(f"Created {len(tools)} default tools")
        
        # Create default agent for admin
        default_agent = Agent(
            name="General Assistant",
            description="A general-purpose AI assistant",
            model="gpt-3.5-turbo",
            owner_id=admin_user.id
        )
        db.add(default_agent)
        db.commit()
        logger.info(f"Created default agent with ID: {default_agent.id}")
        
        logger.info("Database seeding completed successfully.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_db()
