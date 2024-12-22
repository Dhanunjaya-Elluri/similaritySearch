# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/

# Copy application code
COPY pyproject.toml .
COPY src/ src/

# Create virtual environment and install CPU-only PyTorch first
RUN uv venv -p 3.12 --seed /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install --no-cache-dir torch==2.5.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --no-cache-dir -e .

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src/nexmart /app/nexmart

# Create model cache directory
RUN mkdir -p /app/models

# Set up environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/app/models

EXPOSE 8000

CMD ["uvicorn", "nexmart.main:app", "--host", "0.0.0.0", "--port", "8000"]
