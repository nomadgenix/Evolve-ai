# Evolve User Guide

## Introduction

Evolve is a free, open-source alternative to Manus AI that provides similar functionality without subscription costs. This guide will help you get started with Evolve and make the most of its features.

## Getting Started

### Installation

1. **Prerequisites**:
   - Docker and Docker Compose
   - OpenAI API key (for LLM functionality)

2. **Setup**:
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/evolve.git
   cd evolve
   
   # Set your OpenAI API key
   export OPENAI_API_KEY=your_api_key_here
   
   # Start the application
   cd evolve_backend
   docker-compose up -d
   ```

3. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Features

### User Management

- **Registration**: Create a new account with username, email, and password
- **Login**: Access your account securely with JWT authentication

### Agent Management

- **Create Agents**: Build custom AI assistants for different tasks
- **Configure Agents**: Choose models and customize agent behavior
- **Manage Agents**: Update, delete, or share your agents

### Tools

- **Available Tools**: Browse the collection of available tools
- **Tool Integration**: Add tools to your agents to extend their capabilities
- **Custom Configuration**: Configure tools for specific agent needs

### Agent Execution

- **Run Agents**: Execute agents with custom inputs
- **Monitor Executions**: Track the status and progress of agent executions
- **View Results**: See detailed outputs from your agent executions

## Usage Examples

### Creating and Running an Agent

1. Log in to your Evolve account
2. Click "Create Agent" and fill in the details:
   - Name: "Research Assistant"
   - Description: "Helps with research and information gathering"
   - Model: "gpt-3.5-turbo"
3. Add relevant tools to your agent (e.g., Web Search)
4. Save your agent
5. On the agent page, enter your query in the input field
6. Click "Run" and wait for the results

### Managing Tools

1. Navigate to the Tools section
2. Browse available tools
3. To add a tool to an agent:
   - Select the desired agent
   - Click "Add Tool"
   - Configure tool parameters if needed
   - Save changes

## Troubleshooting

### Common Issues

- **Login Problems**: Ensure your username and password are correct
- **Agent Execution Failures**: Check your OpenAI API key is valid and has sufficient credits
- **Missing Tools**: Verify that tools are properly added to your agent

### Support

For additional help, please:
- Check the documentation
- Visit our GitHub repository
- Submit an issue for bugs or feature requests

## Advanced Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Custom database connection string
- `SECRET_KEY`: JWT secret key for authentication

### Custom Deployment

For production deployment, consider:
- Using HTTPS with proper certificates
- Setting up a reverse proxy (Nginx, Traefik)
- Implementing proper backup strategies for the database

## Contributing

We welcome contributions to Evolve! Please see our contributing guidelines for more information on how to get involved.
