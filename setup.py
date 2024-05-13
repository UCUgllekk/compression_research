'''Setup'''
from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Compress algorithms'
LONG_DESCRIPTION = 'A package that allows to compress different types of data using different algorithms such as LZW, LZ78, Deflate, Huffman'

setup(
    name="dalgorithms",
    version=VERSION,
    author="UCUgllekk",
    author_email="pavlosiuk.pn@ucu.edu.ua",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="algorithms"),
    url="https://github.com/UCUgllekk/compression_research",
    install_requires=["tk>=0.1.0"],
    extras_require={
        "dev": ["twine>=4.0.2"]},
    keywords=['python', 'compress', 'compression', 'algorithm',
              'lz78', 'lzw', 'huffman', 'deflate'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.11",
)
