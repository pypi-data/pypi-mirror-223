import os

from setuptools import setup, Extension

long_description = ""

# if os.path.isfile("README.rst"):
#     with open("README.rst") as f:
#         long_description = f.read()

setup(
    name = "fastapi_ses",
    packages = ["fastapi_ses"],
    version = "1.0.0",
    license='MIT License',
    description = "A simple FastAPI email library for Amazon's Simple Email Service",
    author = "Ajit Jasrotia",
    author_email = "ajitjasrotia012@gmail.com",
    url = "https://github.com/ajitjasrotia/fastapi-ses",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
)
