from multidict import CIMultiDict
from asyncio import AbstractEventLoop
from typing import Any, Union, List, Dict, Optional

from yarl import URL
from aiohttp import ClientSession, ClientResponse, ClientTimeout


__all__ = ['Session', 'EventLoop', 'Response', 'CIMDict', 'URL', 'Timeout', 'URLS']

URL = Optional[Union[str, URL]]
URLS = Union[
    List[URL],
    List[List[Union[Any, Dict[str, Any]]]]
]
EventLoop = Optional[AbstractEventLoop]
Session = Optional[ClientSession]
Response = Optional[ClientResponse]
CIMDict = Optional[CIMultiDict]
Timeout = Union[int, float, ClientTimeout, None]
