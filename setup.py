'''Setup'''
from setuptools import setup, find_packages

LONG_DESCRIPTION = 'A package that allows to compress different types of data using different algorithms such as LZW, LZ78, Deflate, Huffman'

setup(
    name="di-compression",
    version="0.1.0",
    author="UCUgllekk",
    author_email="pavlosiuk.pn@ucu.edu.ua",
    description='Compress algorithms',
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
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