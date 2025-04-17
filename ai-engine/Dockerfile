# Stage 1: Builder stage (install build dependencies)
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies first (for any required build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage (minimal image)
FROM python:3.10-slim

WORKDIR /app

# Copy only the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user and set permissions
RUN useradd -m appuser && \
    mkdir -p /app/models && \
    chown -R appuser:appuser /app


USER appuser

# Copy application code (after setting user to minimize permission changes)
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=2)" || exit 1

# Runtime command
CMD ["python", "src/main.py"]

EXPOSE 5000