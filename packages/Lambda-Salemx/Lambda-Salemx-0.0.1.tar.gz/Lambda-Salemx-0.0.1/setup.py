from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Salem to aws lamda funcs'

# Setting up
setup(
    name="Lambda-Salemx",
    version=VERSION,
    author="v4lv3s",
    author_email="gabrielalvesdealm@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy','scipy', 'six', 'pyproj', 'joblib', 'netCDF4', 'pandas', 'xarray'],
    keywords=['python', 'aws', 'salem'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)