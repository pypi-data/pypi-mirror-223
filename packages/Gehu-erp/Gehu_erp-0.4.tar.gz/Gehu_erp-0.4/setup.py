from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Gehu_erp",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "requests",
        "Pillow",
        "beautifulsoup4"
    ],
    author="yato",
    description="A Python library for interacting with GEHU Student API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aminobot22/gehu_erp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
