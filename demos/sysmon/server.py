"""
Server
"""

import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
import logging
import os
import socket
from typing import Optional
import uvicorn
from sysmon.app import make_application

logger = logging.getLogger(__name__)


def initialise_logging() -> None:

    """Initialise logging"""
    logging.basicConfig(level=logging.DEBUG)


def start_uvicorn_server(
        host: str,
        port: int,
        ssl_enabled: bool = False,
        keyfile: Optional[str] = None,
        certfile: Optional[str] = None
) -> None:
    """Start the uvicorn server"""
    app = make_application()

    kwargs = {
        'host': host,
        'port': port,
        # 'loop': 'asyncio'
    }

    if ssl_enabled:
        kwargs['ssl_keyfile'] = keyfile
        kwargs['ssl_certfile'] = certfile

    uvicorn.run(app, **kwargs)


def start_hypercorn_server(
        host: str,
        port: int,
        ssl_enabled: bool = False,
        keyfile: Optional[str] = None,
        certfile: Optional[str] = None
) -> None:
    """Start the hypercorn server"""
    app = make_application()

    web_config = Config()
    web_config.bind = [f'{host}:{port}']

    if ssl_enabled:
        web_config.keyfile = keyfile
        web_config.certfile = certfile

    asyncio.run(serve(app, web_config))


def start_http_server(
        http_server: str,
        host: str,
        port: int,
        ssl_enabled: bool = False,
        keyfile: Optional[str] = None,
        certfile: Optional[str] = None
) -> None:
    """Start the http server"""
    if http_server == "uvicorn":
        start_uvicorn_server(host, port, ssl_enabled, keyfile, certfile)
    elif http_server == "hypercorn":
        start_hypercorn_server(host, port, ssl_enabled, keyfile, certfile)
    else:
        logger.error('Unknown http server "%s"', http_server)
        raise Exception(f'Unknown http server "{http_server}"')


def start_server() -> None:
    """Start the server"""
    hostname = socket.gethostname()

    http_server = 'uvicorn'  # 'hypercorn' or 'uvicorn'
    host = '0.0.0.0'
    port = 9009
    ssl_enabled = False
    keyfile = os.path.expanduser(f'~/.keys/{hostname}.key')
    certfile = os.path.expanduser(f'~/.keys/{hostname}.crt')

    initialise_logging()
    start_http_server(http_server, host, port, ssl_enabled, keyfile, certfile)
    logging.shutdown()


if __name__ == "__main__":
    start_server()
