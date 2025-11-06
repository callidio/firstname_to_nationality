from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="firstname_to_nationality",
    version="0.1.0",
    author="callidio",
    description="Predict the most probable nationality from first names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/callidio/firstname_to_nationality",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'firstname-to-nationality=firstname_to_nationality.cli:main',
        ],
    },
)
