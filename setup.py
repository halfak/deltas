import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def requirements(fname):
	for line in open(os.path.join(os.path.dirname(__file__), fname)):
		yield line.strip()

setup(
    name = "deltas",
    version = read('VERSION').strip(),
    author = "Aaron Halfaker",
    author_email = "ahalfaker@wikimedia.org",
    description = "An experimental diff library for generating " + \
                  "operation deltas that represent the " + \
                  "difference between two sequences of comparable items.",
    license = "MIT",
    url = "https://github.com/halfak/Deltas",
    packages=find_packages(),
    long_description = read('README.rst'),
    install_requires = [],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering"
    ]
)
