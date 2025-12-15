# -------- Builder Stage --------
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /build

# Install build dependencies for psycopg and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/prod.txt .

# Build wheels
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir -r prod.txt -w /wheels

# -------- Runtime Stage --------
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY ./app ./app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]