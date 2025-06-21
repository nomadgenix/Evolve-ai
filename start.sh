#!/bin/bash

# This script builds and runs the full SuperAGI stack with Docker

echo "Building and starting the SuperAGI stack..."

# Copy necessary files
echo "Copying Dockerfiles to appropriate directories..."
cp /home/ubuntu/manus_free_alternative/docker/Dockerfile.superagi /home/ubuntu/manus_free_alternative/backend/SuperAGI/Dockerfile
cp /home/ubuntu/manus_free_alternative/docker/Dockerfile.frontend /home/ubuntu/manus_free_alternative/web_interface/Dockerfile.frontend

# Navigate to docker directory
cd /home/ubuntu/manus_free_alternative/docker

# Build and start the containers
echo "Starting Docker containers..."
docker-compose up -d

echo "SuperAGI stack is now running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8001"
