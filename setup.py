"""
HEC-HMS 水文模型自动化系统
安装脚本
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hec-hms-hydromodel",
    version="2.0.0",
    author="HEC-HMS Team",
    author_email="admin@example.com",
    description="HEC-HMS 水文模型自动化系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/hec-hms-hydromodel",
    packages=find_packages(exclude=["legacy", "venv", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Hydrology",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "flake8>=3.8.0",
        ],
        "ml": [
            "torch>=1.9.0",
            "tensorflow>=2.5.0",
            "scikit-learn>=0.24.0",
        ],
    },
)
