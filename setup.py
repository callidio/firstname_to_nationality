"""
Firstname to Nationality Predictor Setup for Python 3.13+

Implementation using ML libraries for nationality prediction.
"""

import setuptools
from pathlib import Path
from setup_utils import read_requirements, filter_packages_by_name, exclude_packages_by_name


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

# Visualization packages (explicitly defined)
VISUALIZATION_PACKAGES = {"matplotlib", "seaborn"}

# Optional packages for visualization
OPTIONAL_PACKAGES = {
    "viz": filter_packages_by_name(REQUIRED_PACKAGES, VISUALIZATION_PACKAGES),
    "dev": DEV_PACKAGES,
}

# Core packages (excluding optional visualization)
CORE_PACKAGES = exclude_packages_by_name(REQUIRED_PACKAGES, VISUALIZATION_PACKAGES)

setuptools.setup(
    name="firstname-to-nationality",
    version="1.1.8",
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
