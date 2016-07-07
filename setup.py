from distutils.core import setup

from randomlineaccess import __version__

long_description = """
Quickly access arbitrary line numbers in a text file. A well tested library for Python 3.

For example:

    with IndexedOpen('big_text_file.txt') as f:
        print(f[35234:35300])  # happens fast

Does this by creating index files on demand of the locations of lines in a file.  The first call to a file is slow but subsequent calls are
very quick.
"""

setup(
    name="randomlineaccess",
    packages=["randomlineaccess"],
    version=__version__,
    description="Fast access to text files by line number.",
    author="Bryce Drennan",
    author_email="random-line-access@brycedrennan.org",
    url="https://github.com/brycedrennan/random-line-access",
    download_url='https://github.com/brycedrennan/random-line-access/tarball/' + __version__,
    keywords=["linecache", "random access", "text file", "indexing"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Text Processing :: Indexing",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='MIT',
    long_description=long_description
)
