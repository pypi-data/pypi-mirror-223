from setuptools import setup, find_packages
import os

    
VERSION = '0.0.6'
DESCRIPTION = 'Package to print fast, beautiful, and in a readable format.'


    
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
with open(os.path.join(this_directory, "README.md"), encoding='utf-8') as reader:
        long_description = reader.read()
# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="quiele",
    version=VERSION,
    author="Amirrezakhajavi",
    author_email="amirrezakhajavi.1380@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['colorama'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'print'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows", 'Programming Language :: Python :: 3',

    ],




)
