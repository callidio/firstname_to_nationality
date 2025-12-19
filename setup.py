"""
Firstname to Nationality Predictor Setup for Python 3.13+

Implementation using ML libraries for nationality prediction.
"""

import setuptools
from pathlib import Path


def read_requirements(filename):
    """Read requirements from a file and return as list.

    Supports:
    - Line continuations using a trailing backslash (`\`)
    - Inline comments starting with `#`
    """
    requirements_path = Path(__file__).parent / filename
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


# Read README file
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, mode="r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = (
        "Firstname to Nationality Predictor using Python 3.13 and scikit-learn"
    )

# Read dependencies from requirements.txt - single source of truth
REQUIRED_PACKAGES = read_requirements("requirements.txt")
DEV_PACKAGES = read_requirements("requirements-dev.txt")

# Optional packages for visualization
OPTIONAL_PACKAGES = {
    "viz": [req for req in REQUIRED_PACKAGES if any(pkg in req for pkg in ["matplotlib", "seaborn"])],
    "dev": DEV_PACKAGES,
}

# Core packages (excluding optional visualization)
CORE_PACKAGES = [req for req in REQUIRED_PACKAGES if not any(pkg in req for pkg in ["matplotlib", "seaborn"])]

setuptools.setup(
    name="firstname-to-nationality",
    version="1.1.6",
    author="Firstname to Nationality Team",
    author_email="",
    description="Nationality Prediction from Firstname using Python 3.13 and scikit-learn",
    install_requires=CORE_PACKAGES,
    extras_require=OPTIONAL_PACKAGES,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/callidio/firstname_to_nationality",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "firstname_to_nationality": [
            "best-model.pt",
            "firstname_nationalities.pkl",
            "country_nationality.csv",
        ]
    },
    python_requires=">=3.11",
    include_package_data=True,
    options={
        "build": {"build_base": "build"},
        "egg_info": {"egg_base": "build"},
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Typing :: Typed",
    ],
    keywords="firstname nationality prediction names machine-learning nlp",
    project_urls={
        "Documentation": "https://github.com/callidio/firstname_to_nationality#readme",
        "Source": "https://github.com/callidio/firstname_to_nationality",
        "Tracker": "https://github.com/callidio/firstname_to_nationality/issues",
    },
)
