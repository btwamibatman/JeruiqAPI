# ---- Build Stage ----
FROM python:3.9-slim AS builder

WORKDIR /app

# Install dependencies separately to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Production Stage ----
FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy application files
COPY . .

# Expose the correct port
EXPOSE 5001

# Run Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]    