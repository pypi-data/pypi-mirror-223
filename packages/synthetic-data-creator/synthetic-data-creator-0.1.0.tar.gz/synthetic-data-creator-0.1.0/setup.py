from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="synthetic-data-creator",
    version="0.1.0",
    author="Sarah Feyerabend",
    author_email="s.feyerabend14@gmx.de",
    description="A package for generating synthetic datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sarahfy/data_creator_package",
    packages=["data_creator_package"],
    install_requires=[
        "numpy",
        "pandas",
        "enum34"  # Required only for Python versions < 3.4
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
