<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/twcollect.svg?branch=main)](https://cirrus-ci.com/github/<USER>/twcollect)
[![ReadTheDocs](https://readthedocs.org/projects/twcollect/badge/?version=latest)](https://twcollect.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/twcollect/main.svg)](https://coveralls.io/r/<USER>/twcollect)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/twcollect.svg)](https://anaconda.org/conda-forge/twcollect)
[![Monthly Downloads](https://pepy.tech/badge/twcollect/month)](https://pepy.tech/project/twcollect)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/twcollect)
-->


# Twitter-Collect command-line interface: `twcollect`

[![PyPI-Server](https://img.shields.io/pypi/v/twcollect.svg)](https://pypi.org/project/twcollect/)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

> A simple CLI to collect data from the Twitter stream API

## Installation

```shell
pip install twcollect
```

## Usage

First, we need to specify the Twitter Bearer token to connect to the Twitter Stream API.
This needs to be specified in a YAML file (called `credentials.yml` by default) with the following format:

```yml
twitter_token: "<TWITTER_BEARER_TOKEN>"
```

The collection can be started by calling the `twcollect` module.

```shell
python -m twcollect
```

Please see the help for more options:

```shell
python -m twcollect --help
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
