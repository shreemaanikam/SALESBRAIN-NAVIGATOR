# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (e.g. for shap and compilation)
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and necessary datasets
COPY backend/ ./backend/
COPY dataset/ ./dataset/

# Render requires binding to the dynamic PORT environment variable.
# We set a default of 8000 for local development.
ENV PORT=8000
EXPOSE $PORT

# Run using the shell form to allow environment variable expansion
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
