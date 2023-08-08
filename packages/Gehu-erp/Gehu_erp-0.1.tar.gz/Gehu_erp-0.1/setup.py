from setuptools import setup, find_packages

setup(
    name="Gehu_erp",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "Pillow",
        "beautifulsoup4"
    ],
    
    author="yato",
    description="A Python library for interacting with GEHU Student API",
    url="https://github.com/aminobot22",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
