# Multi-stage Dockerfile for Starlink TAM Analysis Platform
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash starlink
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS development


# Copy source code first as root
COPY . /app/

# Change ownership to starlink user
RUN chown -R starlink:starlink /app

# Switch to starlink user
USER starlink
WORKDIR /app

# Install package in development mode
RUN pip install --user -e .

# Add user bin to PATH
ENV PATH="/home/starlink/.local/bin:$PATH"

# Set default command
CMD ["bash"]

# Production stage
FROM base as production

# Copy only necessary files as root and change ownership
COPY starlink_tam/ ./starlink_tam/
COPY config/ ./config/
COPY pyproject.toml requirements.txt ./

# Install package
RUN pip install --no-cache-dir .

# Create directories and change ownership to starlink user
RUN mkdir -p output logs data && chown -R starlink:starlink /app

# Switch to non-root user
USER starlink
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import starlink_tam; print('OK')" || exit 1

# Default command
CMD ["starlink-tam", "--help"]

# Jupyter stage for data science workflows
FROM development AS jupyter


# Expose Jupyter port
EXPOSE 8888

# Jupyter configuration
RUN mkdir -p /home/starlink/.jupyter
COPY --chown=starlink:starlink docker/jupyter_config.py /home/starlink/.jupyter/

# Default command for Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
