# SPDX-License-Identifier: MIT


# Import both local and third-party setup modules.
import codecs
import os

from setuptools import find_packages, setup

# Import version information from local module.
from avrocli import __version__

# Constants.
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Call the setup() function.
setup(
    name='avro.py-cli',
    version=__version__,
    description='A simple CLI for avro.py to ease Bangla phonetic workflow inside your terminal.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='HitBlast',
    author_email='hitblastlive@gmail.com',
    url='https://github.com/hitblast/avro.py-cli',
    packages=find_packages(),
    license='MIT',
    install_requires=['click', 'rich', 'pyclip', 'avro.py'],
    python_requires='>=3.8',
    keywords=[
        'python',
        'avro',
        'avro phonetic',
        'bangla',
        'bangla phonetics',
        'bengali',
        'bengali phonetics',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points='''
        [console_scripts]
        avro=avrocli.main:cli
    ''',
)
