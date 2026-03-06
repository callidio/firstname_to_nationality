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
ARG USER=vscode
RUN groupadd --gid $USER_GID $USER \
    && useradd --uid $USER_UID --gid $USER_GID --shell /bin/bash --create-home $USER \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && mkdir -p /home/$USER/.config/containers

# Set the working directory and ensure it exists
WORKDIR /workspace

# Copy requirements and install Python dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files and set proper ownership
COPY . .
RUN chown -R $USER:$USER /workspace /home/$USER

# Switch to the host user
USER $USER

# Set the default command
CMD ["bash"]