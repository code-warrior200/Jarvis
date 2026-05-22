"""
Setup configuration for JARVIS AI Assistant
Professional Python package setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = (
    requirements_file.read_text(encoding="utf-8").splitlines()
    if requirements_file.exists()
    else []
)
# Remove empty lines and comments
requirements = [
    line.strip()
    for line in requirements
    if line.strip() and not line.startswith("#")
]

setup(
    name="jarvis-ai",
    version="2.0.0",
    author="Developer",
    author_email="dev@example.com",
    description="Advanced AI Voice Assistant with Futuristic GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/jarvis/issues",
        "Documentation": "https://github.com/yourusername/jarvis/wiki",
        "Source Code": "https://github.com/yourusername/jarvis",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "docs", "scripts"]),
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.launcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: System :: Systems Administration",
    ],
    keywords="ai voice assistant gui automation",
    include_package_data=True,
    zip_safe=False,
)
