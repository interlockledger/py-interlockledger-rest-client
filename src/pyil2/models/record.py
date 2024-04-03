import datetime
from typing import Optional

from pydantic import Field

from ..enum import (
    RecordType,
    HashAlgorithms,
)
from .base import BaseCamelModel


class BaseRecordModel(BaseCamelModel):
    application_id: int
    """
    Application id this record is associated with.
    """
    chain_id: str
    """
    Chain id that owns this record.
    """
    created_at: datetime.datetime
    """
    Time of record creation.
    """
    network: str
    """
    Network name this chain is part.
    """
    payload_tag_id: int
    """
    The payload's TagId.
    """
    reference: str
    """
    Universal reference of this record.
    """
    serial: int
    """
    Block serial number. For the first record this value is zero (0).
    """
    type: RecordType
    """
    Block type. Most records are of the type 'Data'.
    """
    version: int
    """
    Version of this record structure.
    """

class RecordModel(BaseRecordModel):
    """
    Record model.
    """
    
    payload_bytes: bytes
    """
    Payload bytes.
    """

class RecordAsJsonModel(BaseRecordModel):
    """
    Record model as JSON.
    """

    payload: str
    """
    Payload as JSON.
    """

class InterlockingRecordModel(BaseRecordModel):
    """
    Interlocking details.
    """

    payload_bytes: str
    """
    Payload bytes.
    """
    interlocked_chain_id: Optional[str] = None
    """
    Interlocked Chain.
    """
    interlocked_record_hash: Optional[str] = None
    """
    Interlock Record Hash.
    """
    interlocked_record_offset: int
    """
    Interlocked Record Offset.
    """
    interlocked_record_serial: int
    """
    Interlocked Record Serial.
    """

class ForceInterlockModel(BaseCamelModel):
    """
    Force interlock parameter details.
    """

    hash_algorithm: HashAlgorithms = Field(default=HashAlgorithms.Copy)
    """
    Hash algorithm to use.
    """
    min_serial: int = 0
    """
    Required minimum of the serial of the last record in target chain whose hash will be pulled.
    """
    target_chain: str
    """
    Id of chain to be interlocked.
    """
