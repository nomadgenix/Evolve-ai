#!/bin/bash

# Deployment script for Evolve backend to Render
# This script prepares and deploys the backend to Render

echo "Preparing Evolve backend for deployment..."

# Navigate to the backend directory
cd /home/ubuntu/manus_free_alternative/evolve_backend

# Install Render CLI if not already installed
if ! command -v render &> /dev/null; then
    echo "Installing Render CLI..."
    curl -s https://cli.render.com/install.sh | bash
fi

# Log in to Render (this will require authentication)
echo "Please authenticate with Render..."
render login

# Deploy using the render.yaml configuration
echo "Deploying to Render..."
render deploy --yaml render.yaml

echo "Backend deployment initiated!"
echo "Your backend will be available at https://evolve-backend.onrender.com once deployment is complete."
echo "This may take a few minutes. You can check the status on the Render dashboard."
