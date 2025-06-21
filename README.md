# Evolve - Free AI Assistant Alternative

## Overview
Evolve is a free, open-source alternative to Manus AI that provides similar functionality without subscription costs. This project includes a simplified backend architecture designed to be clean, modular, and maintainable.

## Features
- Agent-based AI assistant capabilities
- Tool integration framework
- Execution tracking and management
- User authentication and management
- Docker-based deployment

## Architecture
The backend follows a clean, modular architecture with:
- FastAPI for the API layer
- SQLAlchemy for database interactions
- JWT authentication
- OpenAI integration for LLM capabilities
- Docker containerization

For more details, see [architecture.md](./evolve_backend/architecture.md).

## Getting Started

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (for LLM functionality)

### Installation
1. Clone this repository
2. Set your OpenAI API key in the environment:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```
3. Start the application:
   ```
   cd evolve_backend
   docker-compose up -d
   ```
4. Access the application at http://localhost:3000

## Development
The backend is built with FastAPI and follows modern Python practices:
- Models defined with SQLAlchemy
- API schemas defined with Pydantic
- Modular router structure
- Dependency injection for services

## Project Structure
```
evolve_backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── agents.py
│   │   ├── executions.py
│   │   └── tools.py
│   └── services/
│       └── llm_service.py
├── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## License
This project is open-source and free to use.
# monster
# Evolve-ai
