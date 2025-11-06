# Use Python 3.13 official image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a user that matches the host user for --userns=keep-id
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid $USER_GID bfrusteri \
    && useradd --uid $USER_UID --gid $USER_GID --shell /bin/bash --create-home bfrusteri \
    && echo "bfrusteri ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && mkdir -p /home/bfrusteri/.config/containers

# Set the working directory and ensure it exists
WORKDIR /workspace

# Copy requirements and install Python dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files and set proper ownership
COPY . .
RUN chown -R bfrusteri:bfrusteri /workspace /home/bfrusteri

# Switch to the host user
USER bfrusteri

# Set the default command
CMD ["bash"]