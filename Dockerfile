FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run
CMD ["python", "-m", "src.ingestion.main"]
