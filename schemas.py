from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Agent schemas
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: str = "gpt-3.5-turbo"

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Execution schemas
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
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Tool schemas
class ToolBase(BaseModel):
    name: str
    description: str
    icon: Optional[str] = None

class ToolCreate(ToolBase):
    pass

class Tool(ToolBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# AgentTool schemas
class AgentToolBase(BaseModel):
    agent_id: int
    tool_id: int
    config: Optional[str] = None

class AgentToolCreate(AgentToolBase):
    pass

class AgentTool(AgentToolBase):
    id: int

    class Config:
        orm_mode = True

# Token schema for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
