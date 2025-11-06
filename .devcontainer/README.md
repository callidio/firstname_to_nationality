# Dev Container Setup

This directory contains the development container configuration for the Firstname to Nationality project.

## 🐳 Features

- **Python 3.13** environment
- **Host UID/GID mapping** for proper file permissions
- **Pre-installed extensions** for Python development
- **Automatic dependency installation**
- **Port forwarding** for development servers

## 🚀 Quick Start

### For Linux/macOS:
```bash
# Set up permissions (run once)
bash .devcontainer/setup-permissions.sh

# Open in VS Code
code .
# Click "Reopen in Container" when prompted
```

### For Windows:
```batch
# Set up permissions (run once)
.devcontainer\setup-permissions.bat

# Open in VS Code
code .
# Click "Reopen in Container" when prompted
```

## 🔧 Manual Setup

If the automatic scripts don't work, you can manually set environment variables:

### Linux/macOS:
```bash
export USER_UID=$(id -u)
export USER_GID=$(id -g)
```

### Windows (WSL2):
```bash
# In WSL2 terminal
export USER_UID=$(id -u)
export USER_GID=$(id -g)
```

## 📁 File Structure

```
.devcontainer/
├── devcontainer.json         # Main configuration
├── Dockerfile               # Container definition
├── setup-permissions.sh     # Linux/macOS setup script
├── setup-permissions.bat    # Windows setup script
├── .env                     # Environment variables (auto-generated)
└── README.md               # This file
```

## ⚙️ Configuration Details

### Dockerfile Features:
- Python 3.13 slim base image
- System dependencies (build tools, git, sudo)
- Dynamic UID/GID mapping
- Non-root vscode user with sudo access

### VS Code Extensions:
- Python language support
- Black formatter
- isort import sorting
- Pylint linting
- Jupyter notebook support

### Port Forwarding:
- **8000**: Development server
- **8080**: Alternative server port

## 🔍 Troubleshooting

### Permission Issues:
1. Run the setup script for your platform
2. Rebuild the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

### Container Won't Start:
1. Check Docker is running
2. Verify the .env file exists in .devcontainer/
3. Try: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container Without Cache"

### File Permissions on Host:
- Files created in container should have your host user ownership
- If not, check that USER_UID and USER_GID are set correctly

## 🔄 Updating

To update the development environment:
1. Modify `Dockerfile` or `devcontainer.json` as needed
2. Rebuild: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

## 📋 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| USER_UID | Host user ID | 1000 |
| USER_GID | Host group ID | 1000 |
| PYTHONUNBUFFERED | Python output buffering | 1 |
| PYTHONDONTWRITEBYTECODE | Prevent .pyc files | 1 |