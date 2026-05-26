FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /app

# Copy full project
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages
RUN pip install -r backend/requirements.txt

# Move into backend
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Start Django with Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]