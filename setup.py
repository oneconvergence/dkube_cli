#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "tabulate==0.8.7", "dkube"]

setup_requirements = []

test_requirements = []

setup(
    author="oneconvergence",
    author_email="dkube@oneconvergence.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="CLI tool to operate dkube from command line",
    entry_points={
        "console_scripts": [
            "dkube=dkube_cli.cli:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="dkube_cli",
    name="dkube_cli",
    packages=find_packages(include=["dkube_cli", "dkube_cli.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/deepio-oc/dkube_cli",
    version="0.1.0",
    zip_safe=False,
)
