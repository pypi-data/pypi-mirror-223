# -*- coding: utf-8 -*-

"""
:copyright: (c) 2021 by Michael Krukov
:license: MIT, see LICENSE for more details.
"""

import os
import setuptools


assert os.environ.get('GITHUB_REF_TYPE') == 'tag'
assert os.environ.get('GITHUB_REF_NAME')
VERSION = os.environ['GITHUB_REF_NAME']


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="bounded_pool",
    version=VERSION,
    author="Michael Krukov",
    author_email="krukov.michael@ya.ru",
    keywords=["library"],
    description="Library for running tasks in bounded pool executors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelkryukov/bounded_pool",
    packages=setuptools.find_packages(include=('bounded_pool',)),
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
