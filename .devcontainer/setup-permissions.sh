#!/bin/bash
# Set environment variables for devcontainer to use host UID/GID
# This ensures file permissions are maintained between host and container

# Get current user UID and GID
export USER_UID=$(id -u)
export USER_GID=$(id -g)

echo "Setting devcontainer environment variables:"
echo "USER_UID=$USER_UID"
echo "USER_GID=$USER_GID"

# Create/update .env file for devcontainer
cat > .devcontainer/.env << EOF
USER_UID=$USER_UID
USER_GID=$USER_GID
EOF

echo "Environment variables saved to .devcontainer/.env"
echo "You can now open the project in VS Code with 'code .'"