@echo off
REM Set environment variables for devcontainer to use host UID/GID
REM On Windows, we'll use default values since WSL2 handles this differently

echo Setting devcontainer environment variables for Windows...

REM Set default UID/GID for Windows (WSL2 will handle the mapping)
set USER_UID=1000
set USER_GID=1000

echo USER_UID=%USER_UID%
echo USER_GID=%USER_GID%

REM Create .env file for devcontainer
echo USER_UID=%USER_UID% > .devcontainer\.env
echo USER_GID=%USER_GID% >> .devcontainer\.env

echo Environment variables saved to .devcontainer\.env
echo You can now open the project in VS Code with 'code .'
pause