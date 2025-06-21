# Evolve Deployment Guide

## Overview
This guide provides detailed instructions for deploying the Evolve platform (free Manus AI alternative) to production environments. The deployment consists of two main components:
1. Backend API (FastAPI) - deployed to Render
2. Frontend UI (React) - deployed to Vercel

## Prerequisites
- GitHub or GitLab account
- Render.com account (free tier available)
- Vercel account (free tier available)
- OpenAI API key

## Backend Deployment (Render)

### Step 1: Prepare Your Repository
1. Push your Evolve code to a GitHub or GitLab repository
2. Ensure the repository structure matches the one we've created

### Step 2: Create a Render Account
1. Go to [Render.com](https://render.com/) and sign up for a free account
2. Verify your email address

### Step 3: Create a PostgreSQL Database
1. In the Render dashboard, click "New" and select "PostgreSQL"
2. Configure your database:
   - Name: evolve-db
   - Database: evolve
   - User: evolve
   - Region: Choose the closest to your users
3. Click "Create Database" and wait for it to be provisioned
4. Note the "Internal Database URL" for the next step

### Step 4: Deploy the Backend Service
1. In the Render dashboard, click "New" and select "Web Service"
2. Connect your GitHub/GitLab repository
3. Configure the service:
   - Name: evolve-backend
   - Environment: Docker
   - Branch: main (or your default branch)
   - Root Directory: evolve_backend
   - Build Command: (leave default)
   - Start Command: (leave default)
4. Add the following environment variables:
   - DATABASE_URL: (paste the Internal Database URL from Step 3)
   - SECRET_KEY: (generate a random string or use a secure password generator)
   - OPENAI_API_KEY: (your OpenAI API key)
   - ACCESS_TOKEN_EXPIRE_MINUTES: 1440
   - CORS_ORIGINS: https://evolve-frontend.vercel.app
5. Click "Create Web Service"

### Step 5: Verify Backend Deployment
1. Wait for the deployment to complete (this may take a few minutes)
2. Once deployed, click on the service name to view details
3. Test the API by visiting the URL + "/docs" (e.g., https://evolve-backend.onrender.com/docs)
4. You should see the Swagger UI documentation for your API

## Frontend Deployment (Vercel)

### Step 1: Prepare Your Frontend
1. Ensure your frontend code is in the repository
2. Verify that the API URL in the code points to your Render backend

### Step 2: Create a Vercel Account
1. Go to [Vercel.com](https://vercel.com/) and sign up for a free account
2. Verify your email address

### Step 3: Deploy via Vercel CLI
1. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```
2. Navigate to your web_interface directory:
   ```
   cd /path/to/manus_free_alternative/web_interface
   ```
3. Login to Vercel:
   ```
   vercel login
   ```
4. Deploy your frontend:
   ```
   vercel
   ```
5. Follow the interactive prompts:
   - Set up and deploy: Yes
   - Link to existing project: No
   - Project name: evolve-frontend
   - Directory: ./
   - Override settings: No

### Step 4: Configure Environment Variables
1. Go to the Vercel dashboard
2. Select your project
3. Go to "Settings" > "Environment Variables"
4. Add the following variable:
   - REACT_APP_API_URL: https://evolve-backend.onrender.com/api/v1
5. Click "Save"
6. Redeploy your application for the changes to take effect

### Step 5: Verify Frontend Deployment
1. Visit your Vercel deployment URL (e.g., https://evolve-frontend.vercel.app)
2. Test the application by creating an account and logging in
3. Verify that the frontend can communicate with the backend

## Troubleshooting

### Backend Issues
- **Database Connection Errors**: Verify that the DATABASE_URL environment variable is correct
- **CORS Errors**: Ensure the CORS_ORIGINS variable includes your frontend URL
- **Authentication Errors**: Check that the SECRET_KEY is properly set

### Frontend Issues
- **API Connection Errors**: Verify that REACT_APP_API_URL points to your backend
- **Build Failures**: Check the build logs in Vercel for specific errors
- **Blank Page**: Inspect browser console for JavaScript errors

## Custom Domain Setup (Optional)

### Vercel Custom Domain
1. Go to your project in the Vercel dashboard
2. Click "Settings" > "Domains"
3. Add your custom domain and follow the verification steps

### Render Custom Domain
1. Go to your web service in the Render dashboard
2. Click "Settings" > "Custom Domain"
3. Add your domain and follow the verification steps

## Maintenance and Updates

### Updating Your Deployment
1. Push changes to your repository
2. Render and Vercel will automatically rebuild and deploy the updates

### Monitoring
1. Use the Render and Vercel dashboards to monitor your application
2. Check logs for any errors or issues

## Support
If you encounter any issues during deployment, please refer to the official documentation:
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
