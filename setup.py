"""
Firstname to Nationality Predictor Setup for Python 3.13+

Implementation using ML libraries for nationality prediction.
"""

import setuptools
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, mode="r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = (
        "Firstname to Nationality Predictor using Python 3.13 and scikit-learn"
    )

# Dependencies for Python 3.13
REQUIRED_PACKAGES = [
    "numpy>=1.25.0",
    "scikit-learn>=1.3.0",
    "joblib>=1.3.0",
    "pandas>=2.0.0",
    "geopy>=2.3.0",
]

OPTIONAL_PACKAGES = {
    "viz": ["matplotlib>=3.7.0", "seaborn>=0.12.0"],
    "dev": [
        "pytest>=7.4.0",
        "black>=23.0.0",
        "isort>=5.12.0",
        "pylint>=2.17.0",
        "mypy>=1.5.0",
    ],
}

setuptools.setup(
    name="firstname-to-nationality",
    version="1.1.3",
    author="Firstname to Nationality Team",
    author_email="",
    description="Nationality Prediction from Firstname using Python 3.13 and scikit-learn",
    install_requires=REQUIRED_PACKAGES,
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
