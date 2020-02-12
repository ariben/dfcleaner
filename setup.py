# python3 setup.py sdist bdist_wheel

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dfcleaner",
    version="0.1.0",
    description="this package contains helper methods to clean pandas dataframe quickly and therefore simplifying the data cleaning process",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zahash/dfcleaner",
    author="zahash",
    author_email="zahash.z@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dfcleaner"],
    include_package_data=True,
    install_requires=["pandas", "numpy"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)
