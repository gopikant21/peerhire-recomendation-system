# Use Python 3.10 slim image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Generate sample data
RUN python -m app --generate-data

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT} api.main:app