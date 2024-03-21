import datetime

from ..enum import RecordType
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
    
    payload_bytes: str
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
    interlocked_chain_id: str = None
    """
    Interlocked Chain.
    """
    interlocked_record_hash: str = None
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
    