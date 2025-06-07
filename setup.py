#!/usr/bin/env python3
"""
Setup script for MacWhisper Security Research
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="macwhisper-security-research",
    version="1.0.0",
    author="Security Research Team",
    author_email="research@example.com",
    description="A comprehensive security research toolkit for macOS application analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/macwhisper-security-research",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Education",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
    },
    entry_points={
        "console_scripts": [
            "macwhisper-research=core.license_server:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/macwhisper-security-research/issues",
        "Source": "https://github.com/yourusername/macwhisper-security-research",
        "Documentation": "https://github.com/yourusername/macwhisper-security-research/tree/main/docs",
    },
    keywords="security research macos analysis licensing",
    include_package_data=True,
    zip_safe=False,
)
