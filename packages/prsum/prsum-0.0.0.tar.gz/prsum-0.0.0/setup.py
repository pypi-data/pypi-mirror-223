#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name="prsum",
    version="0.0.0",
    license="MIT",
    description="Quick PR summary.",
    author="Liu Yongliang",
    author_email="liu_yongliang@hotmail.com",
    url="https://https://github.com/tlylt/prsum/tlylt/prsum",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Changelog": "https://https://github.com/tlylt/prsum/tlylt/prsum/blob/master/CHANGELOG.rst",
        "Issue Tracker": "https://https://github.com/tlylt/prsum/tlylt/prsum/issues",
    },
    python_requires=">=3.7",
    install_requires=[
        "click",
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },
    entry_points={
        "console_scripts": [
            "prsum = prsum.cli:main",
        ]
    },
)
