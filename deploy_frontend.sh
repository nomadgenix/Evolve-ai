#!/bin/bash

# Deployment script for Evolve frontend to Vercel
# This script prepares and deploys the frontend to Vercel

echo "Preparing Evolve frontend for deployment..."

# Navigate to the frontend directory
cd /home/ubuntu/manus_free_alternative/web_interface

# Install Vercel CLI if not already installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Build the frontend
echo "Building frontend..."
npm run build

# Deploy to Vercel
echo "Deploying to Vercel..."
echo "This will require authentication with Vercel."
echo "Please follow the instructions to authenticate."

# Deploy using the vercel.json configuration
vercel deploy --prod

echo "Frontend deployment completed!"
echo "Your frontend should now be available at the URL provided by Vercel."
