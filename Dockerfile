FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create cache directories and set permissions
RUN mkdir -p /tmp/hf_cache /tmp/matplotlib && \
    chmod 777 /tmp/hf_cache /tmp/matplotlib

# Set environment variables for cache directories
ENV HF_HOME=/tmp/hf_cache
ENV TRANSFORMERS_CACHE=/tmp/hf_cache
ENV MPLCONFIGDIR=/tmp/matplotlib

EXPOSE 8000

CMD ["python", "main.py"]