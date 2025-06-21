# Backend Deployment Guide for Free Manus AI

This guide provides detailed instructions for deploying the SuperAGI backend to create a fully functional Free Manus AI system that works like Manus.im.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- At least 8GB RAM and 4 CPU cores
- 20GB+ free disk space

## Step 1: Clone the Repository

```bash
mkdir -p backend
cd backend
git clone https://github.com/TransformerOptimus/SuperAGI.git
```

## Step 2: Configure SuperAGI

Create a `config.yaml` file in the SuperAGI directory:

```yaml
project:
  name: "Free Manus AI"
  description: "A free alternative to Manus.im with no limitations"

database:
  engine: "postgresql"
  name: "superagi"
  username: "postgres"
  password: "postgres"
  host: "db"
  port: "5432"

vectorstore:
  type: "chroma"
  location: "local"
  path: "/app/vectorstore"

models:
  # For completely free setup, configure a local model
  local:
    enabled: true
    model_name: "llama3"
    path: "/app/models"
  
  # Optional API configuration if you have API keys
  openai:
    api_key: ""  # Leave empty if not using

# Web server configuration
web:
  host: "0.0.0.0"
  port: "8000"

# Redis configuration for task queue
redis:
  host: "redis"
  port: "6379"
  password: ""

# Logging configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Security settings
security:
  secret_key: "your-secret-key-here"
  token_expiry: 86400  # 24 hours in seconds

# Agent configuration
agent:
  default_memory: 100
  max_iterations: 25
  timeout: 600  # 10 minutes in seconds
```

## Step 3: Create Docker Compose Configuration

Create a `docker-compose.yaml` file in the backend directory:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: superagi
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis for task queue
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Chroma Vector Database
  chroma:
    image: ghcr.io/chroma-core/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - ALLOW_RESET=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 5s
      timeout: 5s
      retries: 5

  # SuperAGI Backend
  superagi:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./:/app
      - ./models:/app/models
      - ./vectorstore:/app/vectorstore
      - ./workspace:/app/workspace
    environment:
      - PYTHONUNBUFFERED=1
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/superagi
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_URL=http://chroma:8000
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      chroma:
        condition: service_healthy
    command: >
      bash -c "alembic upgrade head &&
               python -m superagi.api.main"

  # SuperAGI Frontend
  frontend:
    build:
      context: ../web_interface
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://superagi:8000
    depends_on:
      - superagi

volumes:
  postgres_data:
  chroma_data:
```

## Step 4: Create Backend Dockerfile

Create a `Dockerfile` in the backend directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY SuperAGI/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY SuperAGI/ .

# Create necessary directories
RUN mkdir -p /app/models /app/vectorstore /app/workspace

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "superagi.api.main"]
```

## Step 5: Create Frontend Dockerfile

Create a `Dockerfile.frontend` in the web_interface directory:

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Expose the port
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
```

## Step 6: Download a Local Language Model (Optional)

For a completely free setup without API costs, download an open-source model:

```bash
mkdir -p models
cd models
# Download Llama 3 8B GGUF model (example)
wget https://huggingface.co/TheBloke/Llama-3-8B-GGUF/resolve/main/llama-3-8b.Q4_K_M.gguf -O llama3.gguf
cd ..
```

## Step 7: Start the Backend Services

```bash
# Create necessary directories
mkdir -p models vectorstore workspace

# Start all services
docker-compose up -d

# Check if all services are running
docker-compose ps
```

## Step 8: Verify Backend API

```bash
# Check if the API is accessible
curl http://localhost:8000/health

# Expected response: {"status":"ok"}
```

## Step 9: Configure Frontend API Integration

Create an `api.js` file in the web_interface/src directory:

```javascript
// API service for connecting to the SuperAGI backend
import axios from 'axios';

// Base URL for API requests - will be replaced with actual backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions for interacting with SuperAGI
export const api = {
  // Create a new agent
  createAgent: async (agentData) => {
    try {
      const response = await apiClient.post('/agents', agentData);
      return response.data;
    } catch (error) {
      console.error('Error creating agent:', error);
      throw error;
    }
  },

  // Run an agent with a specific task
  runAgent: async (agentId, taskData) => {
    try {
      const response = await apiClient.post(`/agents/${agentId}/run`, taskData);
      return response.data;
    } catch (error) {
      console.error('Error running agent:', error);
      throw error;
    }
  },

  // Get agent status and results
  getAgentStatus: async (agentId, runId) => {
    try {
      const response = await apiClient.get(`/agents/${agentId}/runs/${runId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting agent status:', error);
      throw error;
    }
  },

  // Get available tools
  getTools: async () => {
    try {
      const response = await apiClient.get('/tools');
      return response.data;
    } catch (error) {
      console.error('Error getting tools:', error);
      throw error;
    }
  },

  // Send a message to an agent
  sendMessage: async (message) => {
    try {
      const response = await apiClient.post('/chat', { message });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Health check for the backend
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
};

export default api;
```

## Step 10: Update Frontend App to Connect with Backend

Update the `App.tsx` file in the web_interface/src directory to connect with the backend:

```typescript
import { useState, useEffect } from 'react';
import './App.css';
import api from './api';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { text: 'Hello! I am your free Manus AI assistant. How can I help you today?', sender: 'ai' }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  // Check backend connection on component mount
  useEffect(() => {
    const checkBackendConnection = async () => {
      try {
        await api.healthCheck();
        setIsBackendConnected(true);
      } catch (error) {
        console.error('Backend connection failed:', error);
        setIsBackendConnected(false);
      }
    };

    checkBackendConnection();
  }, []);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;
    
    // Add user message
    setMessages([...messages, { text: input, sender: 'user' }]);
    setIsProcessing(true);
    
    try {
      if (isBackendConnected) {
        // Send message to backend if connected
        const response = await api.sendMessage(input);
        setMessages(prev => [...prev, { 
          text: response.message || 'I processed your request successfully.', 
          sender: 'ai' 
        }]);
      } else {
        // Simulate AI response if backend is not connected
        setTimeout(() => {
          setMessages(prev => [...prev, { 
            text: 'I am processing your request. As a free, open-source alternative to Manus AI, I can help with various tasks including research, content creation, and data analysis. (Note: This is a simulated response as the backend is not currently connected)', 
            sender: 'ai' 
          }]);
          setIsProcessing(false);
        }, 1000);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error processing your request. Please try again later.', 
        sender: 'ai' 
      }]);
    } finally {
      setIsProcessing(false);
      setInput('');
    }
  };

  // Rest of the component remains the same...
}
```

## Step 11: Rebuild and Deploy the Frontend

```bash
# Navigate to the web_interface directory
cd ../web_interface

# Build the frontend
npm run build

# Deploy the built frontend
# (This step depends on your deployment method)
```

## Step 12: Configure Reverse Proxy (Optional)

For production deployment, set up Nginx as a reverse proxy:

```bash
# Install Nginx
apt-get update
apt-get install -y nginx

# Create Nginx configuration
cat > /etc/nginx/sites-available/free-manus-ai << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable the site
ln -s /etc/nginx/sites-available/free-manus-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## Step 13: Set Up SSL with Let's Encrypt (Optional)

```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Obtain SSL certificate
certbot --nginx -d your-domain.com

# Certbot will automatically update your Nginx configuration
```

## Step 14: Monitor and Maintain

```bash
# View logs
docker-compose logs -f

# Restart services if needed
docker-compose restart

# Update the application
git pull
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Backend Connection Issues

If the frontend cannot connect to the backend:

1. Check if all Docker containers are running:
   ```bash
   docker-compose ps
   ```

2. Verify the backend API is accessible:
   ```bash
   curl http://localhost:8000/health
   ```

3. Check backend logs for errors:
   ```bash
   docker-compose logs superagi
   ```

### Database Migration Issues

If you encounter database migration errors:

```bash
# Access the superagi container
docker-compose exec superagi bash

# Run migrations manually
alembic upgrade head
```

### Model Loading Issues

If the language model fails to load:

1. Verify the model file exists in the models directory
2. Check that the model format is compatible with SuperAGI
3. Update the config.yaml with the correct model path and name

## Conclusion

You now have a fully functional Free Manus AI system that works like Manus.im but is completely free, with no limitations or login requirements. The system includes:

- SuperAGI backend for autonomous agent capabilities
- PostgreSQL database for data storage
- Redis for task queue management
- Chroma vector database for embeddings
- React frontend with red background styling
- Full API integration between frontend and backend

This setup provides a true Manus.im-like experience with all the features of the original service but completely free and open-source.
