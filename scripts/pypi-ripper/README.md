# PyPI Ripper

Interactive utility for attempting to find Wikidata entries for Python packages, and showing useful information about said package.

## Setup

```sh
python3 -m pip install poetry
poetry install
```

## Sample usage

```sh
$ ./__main__.py
Provide the Python package name: 
> requests
Getting package information on Wikidata...
Getting package information on PyPI...
--- Results ---
Wikidata match: Q22661317
Classifiers: 
  Development Status :: 5 - Production/Stable
  Environment :: Web Environment
  Intended Audience :: Developers
  License :: OSI Approved :: Apache Software License
  Natural Language :: English
  Operating System :: OS Independent
  Programming Language :: Python
  Programming Language :: Python :: 3
  Programming Language :: Python :: 3 :: Only
  Programming Language :: Python :: 3.10
  Programming Language :: Python :: 3.11
  Programming Language :: Python :: 3.7
  Programming Language :: Python :: 3.8
  Programming Language :: Python :: 3.9
  Programming Language :: Python :: Implementation :: CPython
  Programming Language :: Python :: Implementation :: PyPy
  Topic :: Internet :: WWW/HTTP
  Topic :: Software Development :: Libraries
Homepage: https://requests.readthedocs.io
Depends on: 
  charset-normalizer (<3,>=2)
  idna (<4,>=2.5)
  urllib3 (<1.27,>=1.21.1)
  certifi (>=2017.4.17)
  PySocks (!=1.5.7,>=1.5.6) ; extra == 'socks'
  chardet (<6,>=3.0.2) ; extra == 'use_chardet_on_py3'
```

## Implementation

1. Query SPARQL to find an entry with a Python Package Index project which matches input.
2. Query PyPI's API to get data on project.
3. Show information.
