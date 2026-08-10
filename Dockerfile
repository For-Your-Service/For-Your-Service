# For Your Service - Production Docker Image
# Author: William Free Hall <whall4.wh@gmail.com>
# Organization: 7 Eagle Group

FROM python:3.9-slim

LABEL maintainer="William Free Hall <whall4.wh@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/For-Your-Service/For-Your-Service"
LABEL org.opencontainers.image.description="AI-powered veteran job matching platform"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/models

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# Expose port for web app
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command (Streamlit app)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
