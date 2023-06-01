# LogaVu

Log Analyzer and Visualizer

[![PyPI - Version](https://img.shields.io/pypi/v/logavu.svg)](https://pypi.org/project/logavu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/logavu.svg)](https://pypi.org/project/logavu)

-----

**Table of Contents**

- [LogaVu](#logavu)
  - [Installation](#installation)
  - [Commands](#commands)
  - [Usage](#usage)
  - [License](#license)

## Installation

```console
pip install logavu
```
or
```console
pipx install logavu
```

## Commands
```console
logavu
```

## Usage
Here is an example using [loguru](https://github.com/Delgan/loguru)
Put this code in the Python program you want to use with LogaVu 

```python
import socket
from loguru import logger

HOST, PORT = 'localhost', 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def logudp(message: str):
    sock.sendto(bytes(message, 'utf-8'), (HOST, PORT))

logger.add(logudp)

```

## License

`logavu` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
