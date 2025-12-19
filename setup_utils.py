"""
Utility functions for setup.py configuration.

This module provides helper functions for parsing requirements files
and managing package dependencies.
"""

import re
from pathlib import Path
from typing import List, Optional, Set


def _extract_package_name(requirement: str) -> str:
    """Extract package name from a requirement string.
    
    Handles various version specifiers: ==, >=, <=, >, <, !=, ~=, ===
    
    Args:
        requirement: Requirement string (e.g., 'numpy==1.0.0', 'pandas>=2.0')
        
    Returns:
        Package name without version specifier
    """
    # Use regex to extract package name before any version specifier
    match = re.match(r'^([a-zA-Z0-9\-_.]+)', requirement)
    if match:
        return match.group(1).strip()
    return requirement.strip()


def read_requirements(filename: str, base_path: Optional[Path] = None) -> List[str]:
    r"""Read requirements from a file and return as list.

    Supports:
    - Line continuations using a trailing backslash (\)
    - Inline comments starting with #

    Args:
        filename: Name of the requirements file (e.g., 'requirements.txt')
        base_path: Base directory path. If None, uses the directory of this module.

    Returns:
        List of requirement strings without comments or empty lines
    """
    if base_path is None:
        base_path = Path(__file__).parent
    
    requirements_path = base_path / filename
    if not requirements_path.exists():
        return []

    requirements = []
    current_line = ""
    with open(requirements_path, mode="r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            # Skip empty lines and full-line comments
            if not line or line.startswith("#"):
                continue

            # Handle line continuations with backslash
            if line.endswith("\\"):
                # Remove the trailing backslash and accumulate
                current_line += line[:-1].rstrip() + " "
                continue

            # Append the final segment of this logical line
            current_line += line

            # Strip inline comments from the accumulated logical line
            comment_index = current_line.find("#")
            if comment_index != -1:
                current_line = current_line[:comment_index].rstrip()

            if current_line:
                requirements.append(current_line)

            # Reset for the next logical requirement line
            current_line = ""

    # In case the file ends with a continuation without a final newline
    if current_line.strip():
        requirements.append(current_line.strip())
    return requirements


def filter_packages_by_name(requirements: List[str], package_names: Set[str]) -> List[str]:
    """Filter requirements list to include only specific package names.

    Uses exact package name matching (before == or other version specifiers).

    Args:
        requirements: List of requirement strings (e.g., ['numpy==1.0.0', 'pandas>=2.0'])
        package_names: Set of exact package names to include (e.g., {'numpy', 'pandas'})

    Returns:
        Filtered list of requirements matching the specified package names
    """
    filtered = []
    for req in requirements:
        package_name = _extract_package_name(req)
        if package_name in package_names:
            filtered.append(req)
    return filtered


def exclude_packages_by_name(requirements: List[str], package_names: Set[str]) -> List[str]:
    """Filter requirements list to exclude specific package names.

    Uses exact package name matching (before == or other version specifiers).

    Args:
        requirements: List of requirement strings (e.g., ['numpy==1.0.0', 'pandas>=2.0'])
        package_names: Set of exact package names to exclude (e.g., {'matplotlib', 'seaborn'})

    Returns:
        Filtered list of requirements excluding the specified package names
    """
    filtered = []
    for req in requirements:
        package_name = _extract_package_name(req)
        if package_name not in package_names:
            filtered.append(req)
    return filtered
