import sys
import os
import re
from typing import Dict

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="test-pypi-uploads",
        description="Package for testing PyPi uploads.",
        version="0.1.0.rc2",
        author="angrybayblade",
        long_description="Package for testing PyPi uploads.",
        long_description_content_type="text/markdown",
        packages=find_packages(include=["test_pypi_uploads*"]),
        classifiers=[
            "Operating System :: MacOS",
            "Operating System :: Microsoft",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10"
        ],
        license="MIT",
        python_requires=">=3.8",
    )
