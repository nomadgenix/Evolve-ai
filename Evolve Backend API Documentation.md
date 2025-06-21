# Evolve Backend API Documentation

## Authentication Endpoints

### POST /api/v1/auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2025-06-06T21:52:14.000Z",
  "updated_at": "2025-06-06T21:52:14.000Z"
}
```

### POST /api/v1/auth/login
Login and get access token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## Agent Endpoints

### GET /api/v1/agents
Get all agents for the current user.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Research Assistant",
    "description": "Helps with research and information gathering",
    "model": "gpt-3.5-turbo",
    "owner_id": 1,
    "created_at": "2025-06-06T21:52:14.000Z",
    "updated_at": "2025-06-06T21:52:14.000Z"
  }
]
```

### POST /api/v1/agents
Create a new agent.

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "model": "gpt-3.5-turbo"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "model": "gpt-3.5-turbo",
  "owner_id": 1,
  "created_at": "2025-06-06T21:52:14.000Z",
  "updated_at": "2025-06-06T21:52:14.000Z"
}
```

### GET /api/v1/agents/{agent_id}
Get a specific agent by ID.

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "model": "gpt-3.5-turbo",
  "owner_id": 1,
  "created_at": "2025-06-06T21:52:14.000Z",
  "updated_at": "2025-06-06T21:52:14.000Z"
}
```

### PUT /api/v1/agents/{agent_id}
Update an agent.

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "model": "gpt-3.5-turbo"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "model": "gpt-3.5-turbo",
  "owner_id": 1,
  "created_at": "2025-06-06T21:52:14.000Z",
  "updated_at": "2025-06-06T21:52:14.000Z"
}
```

### DELETE /api/v1/agents/{agent_id}
Delete an agent.

## Execution Endpoints

### GET /api/v1/executions
Get all executions for the current user's agents.

**Response:**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "input": "Research quantum computing",
    "status": "completed",
    "output": "Quantum computing is a type of computing that uses quantum phenomena...",
    "created_at": "2025-06-06T21:52:14.000Z",
    "completed_at": "2025-06-06T21:52:14.000Z"
  }
]
```

### POST /api/v1/executions
Create a new execution.

**Request Body:**
```json
{
  "agent_id": 1,
  "input": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "agent_id": 1,
  "input": "string",
  "status": "in_progress",
  "output": null,
  "created_at": "2025-06-06T21:52:14.000Z",
  "completed_at": null
}
```

### GET /api/v1/executions/{execution_id}
Get a specific execution by ID.

**Response:**
```json
{
  "id": 1,
  "agent_id": 1,
  "input": "string",
  "status": "completed",
  "output": "string",
  "created_at": "2025-06-06T21:52:14.000Z",
  "completed_at": "2025-06-06T21:52:14.000Z"
}
```

### DELETE /api/v1/executions/{execution_id}
Delete an execution.

## Tool Endpoints

### GET /api/v1/tools
Get all available tools.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Web Search",
    "description": "Search the web for information",
    "icon": "search",
    "created_at": "2025-06-06T21:52:14.000Z"
  }
]
```

### POST /api/v1/tools
Create a new tool.

**Request Body:**
```json
{
  "name": "string",
  "description": "string",
  "icon": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "icon": "string",
  "created_at": "2025-06-06T21:52:14.000Z"
}
```

### GET /api/v1/tools/{tool_id}
Get a specific tool by ID.

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "description": "string",
  "icon": "string",
  "created_at": "2025-06-06T21:52:14.000Z"
}
```

### POST /api/v1/tools/agent/{agent_id}
Add a tool to an agent.

**Request Body:**
```json
{
  "tool_id": 1,
  "config": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "agent_id": 1,
  "tool_id": 1,
  "config": "string"
}
```

### DELETE /api/v1/tools/agent/{agent_id}/tool/{tool_id}
Remove a tool from an agent.
