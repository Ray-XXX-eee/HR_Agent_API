# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies using apt (Debian's package manager)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime image
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies if needed (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the rest of the app files
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
