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
