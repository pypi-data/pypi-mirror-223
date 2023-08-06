from setuptools import setup, find_packages

import os 

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='findbook',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.3',
    description='A command-line tool to search for books on Goodreads.',
    author='DShaarvin',
    author_email='domunshaarvin@gmail.com',
    url='',
    packages=['findbook/findbook'],
    install_requires=[
        'requests==2.26.0',
        'beautifulsoup4==4.9.3'
    ],
    entry_points={
        'console_scripts': [
            'findbook=findbook.findbook:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
