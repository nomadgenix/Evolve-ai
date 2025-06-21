from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import os
import json
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Evolve API",
    description="Free open-source alternative to Manus AI",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes for testing
@app.get("/")
async def root():
    return {"message": "Welcome to Evolve - Free AI Assistant"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0"
    }

# Agent models
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    
class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Mock data for initial development
agents = [
    {
        "id": 1,
        "name": "Research Assistant",
        "description": "Helps with research and information gathering",
        "model": "gpt-3.5-turbo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "name": "Code Helper",
        "description": "Assists with coding tasks and debugging",
        "model": "gpt-4",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]

# Agent routes
@app.get("/agents", response_model=List[Agent])
async def get_agents():
    return agents

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: int):
    for agent in agents:
        if agent["id"] == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/agents", status_code=status.HTTP_201_CREATED)
async def create_agent(agent: AgentCreate):
    new_agent = agent.dict()
    new_agent["id"] = len(agents) + 1
    new_agent["created_at"] = datetime.now().isoformat()
    new_agent["updated_at"] = datetime.now().isoformat()
    agents.append(new_agent)
    return new_agent

# Execution models
class ExecutionBase(BaseModel):
    agent_id: int
    input: str
    
class ExecutionCreate(ExecutionBase):
    pass

class Execution(ExecutionBase):
    id: int
    status: str
    output: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

# Mock executions data
executions = [
    {
        "id": 1,
        "agent_id": 1,
        "input": "Research quantum computing",
        "status": "completed",
        "output": "Quantum computing is a type of computing that uses quantum phenomena...",
        "created_at": datetime.now().isoformat()
    }
]

# Execution routes
@app.get("/executions", response_model=List[Execution])
async def get_executions():
    return executions

@app.get("/executions/{execution_id}")
async def get_execution(execution_id: int):
    for execution in executions:
        if execution["id"] == execution_id:
            return execution
    raise HTTPException(status_code=404, detail="Execution not found")

@app.post("/executions", status_code=status.HTTP_201_CREATED)
async def create_execution(execution: ExecutionCreate):
    # Check if agent exists
    agent_exists = False
    for agent in agents:
        if agent["id"] == execution.agent_id:
            agent_exists = True
            break
    
    if not agent_exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    new_execution = execution.dict()
    new_execution["id"] = len(executions) + 1
    new_execution["status"] = "in_progress"
    new_execution["created_at"] = datetime.now().isoformat()
    
    # In a real implementation, this would trigger an async task
    # For now, we'll just simulate a completed execution
    new_execution["output"] = f"Response to: {execution.input}"
    new_execution["status"] = "completed"
    
    executions.append(new_execution)
    return new_execution

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
