from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)

@router.get("/", response_model=List[schemas.Tool])
def get_tools(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all available tools."""
    tools = db.query(models.Tool).offset(skip).limit(limit).all()
    return tools

@router.post("/", response_model=schemas.Tool, status_code=status.HTTP_201_CREATED)
def create_tool(
    tool: schemas.ToolCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new tool."""
    # Check if tool already exists
    db_tool = db.query(models.Tool).filter(models.Tool.name == tool.name).first()
    if db_tool:
        raise HTTPException(status_code=400, detail="Tool already exists")
    
    # Create new tool
    db_tool = models.Tool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.get("/{tool_id}", response_model=schemas.Tool)
def get_tool(
    tool_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific tool by ID."""
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.post("/agent/{agent_id}", response_model=schemas.AgentTool)
def add_tool_to_agent(
    agent_id: int,
    tool_id: int,
    config: str = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add a tool to an agent."""
    # Check if agent exists and belongs to user
    agent = db.query(models.Agent).filter(
        models.Agent.id == agent_id,
        models.Agent.owner_id == current_user.id
    ).first()
    
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if tool exists
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    # Check if agent already has this tool
    agent_tool = db.query(models.AgentTool).filter(
        models.AgentTool.agent_id == agent_id,
        models.AgentTool.tool_id == tool_id
    ).first()
    
    if agent_tool:
        raise HTTPException(status_code=400, detail="Tool already added to agent")
    
    # Add tool to agent
    agent_tool = models.AgentTool(
        agent_id=agent_id,
        tool_id=tool_id,
        config=config
    )
    db.add(agent_tool)
    db.commit()
    db.refresh(agent_tool)
    return agent_tool

@router.delete("/agent/{agent_id}/tool/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tool_from_agent(
    agent_id: int,
    tool_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Remove a tool from an agent."""
    # Check if agent exists and belongs to user
    agent = db.query(models.Agent).filter(
        models.Agent.id == agent_id,
        models.Agent.owner_id == current_user.id
    ).first()
    
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if agent has this tool
    agent_tool = db.query(models.AgentTool).filter(
        models.AgentTool.agent_id == agent_id,
        models.AgentTool.tool_id == tool_id
    ).first()
    
    if agent_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found for this agent")
    
    # Remove tool from agent
    db.delete(agent_tool)
    db.commit()
    return None
