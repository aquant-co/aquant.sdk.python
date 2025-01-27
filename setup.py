from setuptools import find_packages, setup

setup(
    name="aquant_sdk",
    version="1.0.0",
    description="Aquant SDK for Redis-based message processing and streaming.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sua Empresa",
    author_email="devs@suaempresa.com",
    url="https://your-private-pypi-url.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "redis>=4.6.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov", "flake8"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
