<!-- SPDX-License-Identifier: MIT -->

<div align="center">

# <img src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" height="40px"/> avro.py-cli

A simple CLI for avro.py to ease Bangla phonetic workflow inside your terminal.

[![Linting](https://github.com/hitblast/avro.py-cli/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/hitblast/avro.py-cli/actions/workflows/linting.yml)
![License](https://img.shields.io/pypi/l/avro.py-cli.svg?color=black&label=License)
![Python Version](https://img.shields.io/pypi/pyversions/avro.py-cli.svg?color=black&label=Python)

<img src="static/terminal_demo.png" alt="Terminal Demo">

</div>

## Installation

You can easily install this project in the form of a Python package using the following command:

```bash
# Install / upgrade.
$ pip install -U avro.py-cli
```

<br>

## Usage Guide

If you have done the installation correctly, the usage should be pretty easy as well:

```bash
# Get help regarding the CLI inside your terminal.
$ python3 -m avro --help 
$ avro --help 
# Minified, both of them can work depending on your environment.

# Parse a text.
$ avro parse --text "ami banglay gan gai."
$ avro parse -t "eije dekh waTar." 
# Minified --text option.

# Parse multiple texts.
$ avro parse -t "amar swopnera" -t "Dana mele ure cole" -t "obarito nIle."
```

Note that each time you parse some text, the output will be automatically copied to your clipboard for convenience.

<br>

## License

Licensed under the [MIT License](https://github.com/hitblast/avro.py-cli/blob/main/LICENSE).