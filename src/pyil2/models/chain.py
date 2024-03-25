import datetime
from typing import List, Optional

from pydantic import Field

from .keys import CertificatePermitModel

from ..enum import (
    KeyStrength,
    Algorithms,
)

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


class ChainCreationModel(BaseCamelModel):
    addional_apps: List[int] = Field(default_factory=list)
    """
    List of additional apps (only numeric ids).
    """
    api_certificates: Optional[List[CertificatePermitModel]] = None
    """
    List of certificates to permit in the chain.
    """
    description: Optional[str] = None
    """
    Description (perhaps intended primary usage).
    """
    emergency_closing_key_password: str = Field(min_length=1)
    """
    Emergency closing key password.
    """
    emergency_closing_key_strength: KeyStrength = Field(default=KeyStrength.ExtraStrong)
    """
    Emergency closing key strength of key.
    """
    keys_algorithm: Optional[Algorithms] = Field(default=None)
    """
    Keys algorithm.
    """
    management_key_password: str = Field(min_length=1)
    """
    Key management key password.
    """
    management_key_strength: KeyStrength = Field(default=KeyStrength.Strong)
    """
    Key management strength of key.
    """
    name: str = Field(min_length=1)
    """
    Name of the chain.
    """
    operating_key_strength: KeyStrength = Field(default=KeyStrength.Normal)
    """
    Operating key strength of key.
    """
    operating_key_algorithm: Optional[Algorithms] = Field(default=None)
    """
    Operating key algorithm.
    """
    parent: Optional[str] = None
    """
    Parent chain ID.
    """
    

