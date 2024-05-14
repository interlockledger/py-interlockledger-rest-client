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
from typing import List, Optional, Self
import datetime
from pydantic import Field, field_serializer, field_validator

from .base import BaseCamelModel
from ..utils.range import LimitedRange
from ..enum import DataFieldCast


class DataFieldEnumeration(BaseCamelModel):
    """
    Data field enumeration model.
    """
    id: int
    """
    Data field enumeration ID.
    """
    name: str
    """
    Name of the data field enumeration.
    """
    description: Optional[str] = None
    """
    Description of the data field enumeration.
    """

    @classmethod
    def from_concatenated_string(cls, value: str) -> List[Self]:
        """
        Parse a string with concatenated DataFieldEnumeration in the format: #<int>|<str>|[<str>|].

        Args:
            value (:obj:`str`): A string with concatenated DataFieldEnumerations in string format.

        Returns:
            [DataFieldEnumeration]: List of data field enumerations.
        """
        ret = []

        items = value.split('#')
        for item in items:
            if not item:
                continue
            v = item.split('|')
            cur_id = int(v[0])
            cur_name = v[1]
            cur_description = None
            if len(v) >= 3 and v[2]:
                cur_description = v[2]
            ret.append(DataFieldEnumeration(
                id=cur_id,
                name=cur_name,
                description=cur_description,
            )
            )
        return ret

    def to_il2_string(self) -> str:
        """
        :obj:`str`: IL2 string representation of the DataFieldEnumeration: #<int>|<str>|[<str>|]. 
        """
        ret = f'#{self.id}|{self.name}|'
        if self.description is not None:
            ret += f'{self.description}|'
        return ret


class DataFieldModel(BaseCamelModel):
    """
    Data field model.
    """

    cast: Optional[DataFieldCast] = None
    """
    Type of the data field.
    """
    description: Optional[str] = None
    """
    Data field description.
    """
    element_tag_id: Optional[int] = None
    """
    The type of the field in case it is an array.
    """
    enumeration: List[DataFieldEnumeration] = Field(default_factory=list)
    """
    A list of data field enumerations.
    """
    enumeration_as_flags: Optional[bool] = None
    """
    If `True`, the enumerations can be combined using bitwise-or. 
    If `False`, only one value can be used.
    """
    is_dreprecated: Optional[bool] = None
    """
    If `True` the field is deprecated.
    """
    is_opaque: Optional[bool] = None
    """
    If `True` the field is stored in raw bytes.
    """
    name: Optional[str] = None
    """
    Name of the data  field.
    """
    sub_data_fields: List['DataFieldModel'] = Field(default_factory=list)
    """
    If the data field in composed of more fields, indicates the metadata of the subdata fields.
    """
    tag_id: int = 0
    """
    Type of the field. (see tags in the InterlockLedger node documentation)
    """
    version: int = 0
    """
    Version of the data field.
    """

    @field_validator('enumeration', mode='before')
    @classmethod
    def pre_process_enumeration(cls, raw: str) -> List[DataFieldEnumeration]:
        """
        Deserialize from string.
        """
        if not raw:
            return raw
        ret = DataFieldEnumeration.from_concatenated_string(raw)
        return ret

    @field_serializer('enumeration', when_used='json')
    @classmethod
    def serialize_enumeration(cls, value: List[DataFieldEnumeration]):
        """
        Serialize DataField enumeration.
        """
        ret = ""
        for item in value:
            ret += item.to_il2_string()
        return ret


class DataIndexElementModel(BaseCamelModel):
    """
    Data index element.
    """

    descending_order: Optional[bool] = None
    """
    Indicate if the field is ordered in descending order.
    """
    field_path: Optional[str] = None
    """
    Path of the data field to be indexed.
    """
    function: Optional[str] = None
    """
    To be defined.
    """


class DataIndexModel(BaseCamelModel):
    """
    Index of the data model.
    """

    elements: List[DataIndexElementModel] = Field(default_factory=list)
    """
    Elements of the index.
    """
    is_unique: Optional[bool] = None
    """
    Indicate if the data field is unique.
    """
    name: Optional[str] = None
    """
    Name of the index.
    """


class DataModel(BaseCamelModel):
    """
    Data model for the payloads and actions for the records the application stores in the chains.
    """

    data_fields: List[DataFieldModel] = Field(default_factory=list)
    """
    The list of data fields.
    """
    description: Optional[str] = None
    """
    Description of the data model.
    """
    indexes: List[DataIndexModel] = Field(default_factory=list)
    """
    List of indexes for records of this type.
    """
    payload_name: Optional[str] = None
    """
    Name of the record model.
    """
    payload_tag_id: int = 0
    """
    Tag id for this payload type. It must be a number in the reserved ranges.
    """
    version: int = 0
    """
    Version of this data model, should start from 1.
    """


class InterlockAppTraitsModel(BaseCamelModel):
    """
    Interlock App details model.
    """

    app_version: str
    """
    Application semantic version, with four numeric parts.
    """
    data_models: List[DataModel]
    """
    The list of data models for the payloads of the records stored in the chains.
    """
    description: str
    """
    Description of the application.
    """
    id: int = 0
    """
    Unique ID for the application.
    """
    name: str
    """
    Application name.
    """
    publisher_id: str
    """
    Publisher ID, which is the identifier for the key the publisher uses to 
    sign the workflow requests in its own chain. 
    It should match the publisher_name
    """
    publisher_name: str
    """
    Publisher name as registered in the Genesis chain of the network.
    """
    reserved_il_tag_ids: List[LimitedRange] = Field(alias='reservedILTagIds')
    """
    The list of ranges of ILTagIds to reserve for the application.
    """
    start: datetime.datetime
    """
    The start date for the validity of the app, but if prior to the effective 
    publication of the app will be overridden with the publication date and time.
    """
    version: int = 0
    """
    Version of the application.
    """

    @field_validator('reserved_il_tag_ids', mode='before')
    @classmethod
    def pre_process_reserved_tags(cls, raw: List[str]) -> List[LimitedRange]:
        """
        Deserialize reserved tags from list of strings.
        """
        ret = []
        for item in raw:
            ret.append(LimitedRange.resolve(item))
        return ret

    @field_serializer('reserved_il_tag_ids', when_used='json')
    @classmethod
    def serialize_reserved_tags(cls, value: List[LimitedRange]):
        """
        Serialize reseved tags.
        """
        ret = []
        for item in value:
            ret.append(str(item))
        return ret


class AppsModel(BaseCamelModel):
    """
    List of valid apps in the network.
    """

    network: Optional[str] = None
    """
    Network name.
    """
    valid_apps: List[InterlockAppTraitsModel] = Field(default_factory=list)
    """
    Currently valid apps for this network.
    """
