import datetime

from pydantic import Field

from .base import BaseCamelModel


class ChainIdModel(BaseCamelModel):
    """
    Chain summary.
    """

    id: str
    """
    Chain ID.
    """
    closed: bool = Field(alias='isClosedForNewTransactions', default=False)
    """
    If `True`, this chain is not able to accept new records.
    """
    last_record: int
    """
    Last record (serial number).
    """
    last_update: datetime.datetime
    """
    Date last record was added.
    """
    licensing_status: str = None
    """
    Licensing status.
    """
    name: str = None
    """
    Chain name.
    """
    size_in_bytes: int
    """
    Chain size in bytes.
    """
    