#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="reconxploit",
    version="1.0.0",
    author="kernelpanic",
    author_email="contact@kernelpanic.io",
    description="Advanced Reconnaissance Automation Tool with Mr Robot Themes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kernelpanic/reconxploit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reconxploit=reconxploit:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["wordlists/*", "utils/*", "docs/*"],
    },
)