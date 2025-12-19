# Requirements Management

This document explains how dependencies are managed in this project.

## Overview

All dependencies are now managed through two requirements files:
- `requirements.txt` - Production dependencies with pinned versions
- `requirements-dev.txt` - Development dependencies with pinned versions

The `setup.py` file reads from these requirements files, making them the **single source of truth** for all package versions.

## Pinned Versions

All dependencies use exact version pinning (`==`) instead of minimum version constraints (`>=`). This ensures:
- **Reproducible builds**: Same versions installed every time
- **Security**: Controlled updates through Dependabot PRs
- **Stability**: No unexpected breaking changes from dependency updates

## Dependency Updates

Dependency updates are handled automatically by **Dependabot**, configured in `.github/dependabot.yml`:
- Checks for updates weekly
- Creates pull requests for version updates
- Allows review and testing before merging
- Updates are applied in a controlled PR environment

## Installing Dependencies

### Production Dependencies (Core)
```bash
pip install -r requirements.txt
# Or install the package
pip install .
```

### Production Dependencies (with visualization)
```bash
pip install .[viz]
```

### Development Dependencies
```bash
pip install -r requirements-dev.txt
# Or install with dev extras
pip install .[dev]
```

### All Dependencies
```bash
pip install -r requirements.txt -r requirements-dev.txt
# Or
pip install .[viz,dev]
```

## Updating Dependencies

### Manual Updates
1. Update version in `requirements.txt` or `requirements-dev.txt`
2. Test the changes
3. Commit and push

### Automated Updates (Recommended)
1. Dependabot creates a PR with version updates
2. Review the PR and test changes
3. Merge the PR if tests pass

## Setup.py Integration

The `setup.py` file automatically reads dependencies from the requirements files:

```python
def read_requirements(filename: str, base_path: Path = None) -> List[str]:
    """Read requirements from a file and return as list.
    
    Args:
        filename: Name of the requirements file (e.g., 'requirements.txt')
        base_path: Base directory path. If None, uses the directory of this module.
    
    Returns:
        List of requirement strings without comments or empty lines
    """
    # Reads and parses requirements.txt or requirements-dev.txt
    # Skips comments and empty lines
    ...

REQUIRED_PACKAGES = read_requirements("requirements.txt")
DEV_PACKAGES = read_requirements("requirements-dev.txt")
```

This ensures:
- No duplicate version specifications
- Single place to update versions
- Consistency between pip install and setup.py

## Benefits

✅ **Single Source of Truth**: Update versions in one place (requirements files)
✅ **Reproducible Builds**: Exact versions ensure consistent installations
✅ **Security**: Automated updates through Dependabot PRs
✅ **Stability**: Changes reviewed before deployment
✅ **Easy Maintenance**: Clear separation of production and dev dependencies
