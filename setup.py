from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="family_api",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
)
