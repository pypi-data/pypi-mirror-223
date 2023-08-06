from setuptools import setup, find_packages

setup(
    name="shawn_api",
    version="0.3",
    description="A Python library for shawn test api",
    author="Shawn-Tam",
    author_email="shawn@dcoean.ai",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # or "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)