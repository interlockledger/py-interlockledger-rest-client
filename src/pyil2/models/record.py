# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import datetime
from typing import (
    Optional,
    Dict,
    Any
)

from pydantic import (
    Field,
    field_serializer,
)

from ..enum import (
    RecordType,
    HashAlgorithms,
)
from .base import BaseCamelModel


class NewRecordModel(BaseCamelModel):
    """
    New record model to be added to the chain as raw bytes.
    """

    application_id: int = 0
    """
    Application id this record is associated with.
    """
    payload_bytes: bytes
    """
    Payload bytes.
    """
    type: RecordType = Field(default=RecordType.DATA)
    """
    Block type. Most records are of the type 'Data'.
    """

    @field_serializer('payload_bytes')
    @classmethod
    def serialize_reserved_tags(cls, value: bytes) -> str:
        """
        Serialize payload_bytes field.
        """
        return value.decode()


class BaseRecordModel(BaseCamelModel):
    """
    Base record model.
    """
    application_id: int = 0
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
    payload_tag_id: int = 0
    """
    The payload's TagId.
    """
    reference: str
    """
    Universal reference of this record.
    """
    serial: int = 0
    """
    Block serial number. For the first record this value is zero (0).
    """
    type: RecordType = Field(default=RecordType.ROOT)
    """
    Block type. Most records are of the type 'Data'.
    """
    version: int = 0
    """
    Version of this record structure.
    """


class RecordModel(BaseRecordModel):
    """
    Record model.
    """

    payload_bytes: Optional[bytes] = None
    """
    Payload bytes.
    """


class RecordAsJsonModel(BaseRecordModel):
    """
    Record model as JSON.
    """

    payload: Dict[str, Any]
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
    interlocked_record_offset: int = 0
    """
    Interlocked Record Offset.
    """
    interlocked_record_serial: int = 0
    """
    Interlocked Record Serial.
    """


class ForceInterlockModel(BaseCamelModel):
    """
    Force interlock parameter details.
    """

    hash_algorithm: HashAlgorithms = Field(default=HashAlgorithms.COPY)
    """
    Hash algorithm to use.
    """
    min_serial: int = 0
    """
    Required minimum of the serial of the last record in target chain whose 
    hash will be pulled.
    """
    target_chain: str
    """
    Id of chain to be interlocked.
    """


class OpaqueRecordModel(BaseCamelModel):
    """
    Opaque record details.
    """

    network: Optional[str] = None
    """
    Network name this chain is part.
    """
    chain_id: Optional[str] = None
    """
    Chain id that owns this record.
    """
    serial: int = 0
    """
    Block serial number. For the first record this value is zero (0).
    """
    application_id: int = 0
    """
    Application id this record is associated with.
    """
    payload_type_id: int = 0
    """
    The payload's TypeId.
    """
    payload_length: int = 0
    """
    The opaque payload length in bytes.
    """
    created_at: datetime.datetime
    """
    Time of record creation.
    """
    payload: Optional[bytes] = None
    """
    Opaque payload bytes.
    """
