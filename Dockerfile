FROM python:3.11-slim

# Install system dependencies needed for compiling python packages (scikit-surprise, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# App directory
WORKDIR /app

# Copy the entire core_backend directory contents
COPY . /app

# Upgrade pip and install packages
RUN pip install --upgrade pip && \
    pip install -r backend/requirements.txt

# Set workdir to backend directory
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Render provides PORT at runtime. Keep 8000 as the local fallback.
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
