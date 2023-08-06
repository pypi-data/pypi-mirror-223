from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vmman1",
    version="2.000",
    author="Jean-François Gratton <jean-francois@famillegratton.net>",
    description="Python3-based libvirt client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Parse requirements.txt to get dependencies
        line.strip() for line in open("requirements.txt") if not line.startswith("#")
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
