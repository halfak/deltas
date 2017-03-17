import os

from setuptools import find_packages, setup

about_path = os.path.join(os.path.dirname(__file__), "deltas/about.py")
exec(compile(open(about_path).read(), about_path, "exec"))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name=__name__,  # noqa
    version=__version__,  # noqa
    author=__author__,  # noqa
    author_email=__author_email__,  # noqa
    description=__description__,  # noqa
    url=__url__,  # noqa
    license=__license__,  # noqa
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=['yamlconf'],
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
