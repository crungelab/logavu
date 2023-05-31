# LogaVu

Log Analyzer and Visualizer


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