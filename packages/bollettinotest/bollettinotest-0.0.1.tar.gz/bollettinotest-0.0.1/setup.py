from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Test library to publish'
LONG_DESCRIPTION = 'Long description of test library'

# with open('requirements.txt', 'r') as f:
#     requirements = f.read().splitlines()

# Setting up
setup(
    name="bollettinotest",
    version=VERSION,
    author="Matteo Bollettino",
    author_email="<matteo.bollettino@moxoff.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','meteostat'],
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    keywords=['python', 'test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)