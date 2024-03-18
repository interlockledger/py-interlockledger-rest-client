from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import IL2Client

class BaseApi(ABC):
    '''
    Base class for the APIs.

    Args:
        client (:obj:`IL2Client`): IL2 client to be used to send requests.
    '''
    def __init__(self, client: IL2Client) -> None:
        self._client = client