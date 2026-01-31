# Use Python 3.14 slim image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY agent_availability.py .
COPY sample_data/ ./sample_data/

# Create directory for database and reports (visible directories)
RUN mkdir -p /app/data /app/reports

# Set permissions
RUN chmod +x agent_availability.py

# Volume mounts for persistent data (using bind mounts instead)
# The actual directories are on the host machine
VOLUME ["/app/data", "/app/reports"]

# Default command - run the interactive application
CMD ["python", "agent_availability.py"]
