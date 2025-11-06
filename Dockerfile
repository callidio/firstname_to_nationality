FROM python:3.7-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy the current directory into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Default command to run the script
CMD ["python", "predict.py"]