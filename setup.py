from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Compress algorithms'
LONG_DESCRIPTION = 'A package that allows to compress different types of data using different algorithms such as LZW, LZ78, Deflate, Huffman'

# Setting up
setup(
    name="dalgorithms",
    version=VERSION,
    author="UCUgllekk",
    author_email="<pavlosiuk.pn@ucu.edu.ua>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tk==0.1.0'],
    keywords=['python', 'compress', 'compression', 'algorithm', 'lz78', 'lzw', 'huffman', 'deflate'],
    classifiers=[
        "Development Status :: 1 - Production",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)