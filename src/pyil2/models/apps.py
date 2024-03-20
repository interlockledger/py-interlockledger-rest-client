from typing import Dict, List, Self
from pydantic import Field, field_serializer, field_validator
import datetime

from .base import BaseCamelModel
from ..utils.range import LimitedRange
from ..enum import DataFieldCast

class DataFieldModel(BaseCamelModel):
    """
    Data field model.
    """
    
    cast: DataFieldCast = None
    """
    Type of the data field.
    """
    description: str = None
    """
    Data field description.
    """
    element_tag_id: int = None
    """
    The type of the field in case it is an array.
    """
    enumeration: str = None
    """
    A string containing all enumerations concatenated in the format "#<number>|<name>|<description>|".
    """
    enumeration_as_flags: bool = None
    """
    If `True`, the enumerations can be combined using bitwise-or. If `False`, only one value can be used.
    """
    is_dreprecated: bool = None
    """
    If `True` the field is deprecated.
    """
    is_opaque: bool = None
    """
    If `True` the field is stored in raw bytes.
    """
    name: str = None
    """
    Name of the data  field.
    """
    sub_data_fields: List['DataFieldModel'] = Field(default_factory=list)
    """
    If the data field in composed of more fields, indicates the metadata of the subdata fields.
    """
    tag_id: int
    """
    Type of the field. (see tags in the InterlockLedger node documentation)
    """
    version: int
    """
    Version of the data field.
    """
    
class DataIndexElementModel(BaseCamelModel):
    """
    Data index element.
    """
    
    descending_order: bool = None
    """
    Indicate if the field is ordered in descending order.
    """
    field_path: str = None
    """
    Path of the data field to be indexed.
    """
    function: str = None
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
    is_unique: bool = None
    """
    Indicate if the data field is unique.
    """
    name: str = None
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
    description: str = None
    """
    Description of the data model.
    """
    indexes: List[DataIndexModel] = Field(default_factory=list)
    """
    List of indexes for records of this type.
    """
    payload_name: str = None
    """
    Name of the record model.
    """
    payload_tag_id: int
    """
    Tag id for this payload type. It must be a number in the reserved ranges.
    """
    version: int
    """
    Version of this data model, should start from 1.
    """
    


class InterlockAppTraitsModel(BaseCamelModel):
    app_version: str
    data_models: List[DataModel]
    description: str
    id: int
    name: str
    publisher_id: str
    publisher_name: str
    reserved_il_tag_ids: List[LimitedRange] = Field(alias='reservedILTagIds')
    start: datetime.datetime
    version: int

    @field_validator('reserved_il_tag_ids', mode='before')
    @classmethod
    def pre_process_reserved_tags(cls, raw: List[str]) -> List[LimitedRange]:
        ret = []
        for item in raw:
            ret.append(LimitedRange.resolve(item))
        return ret
    
    @field_serializer('reserved_il_tag_ids', when_used='json')
    @classmethod
    def serialize_reserved_tags(cls, value: List[LimitedRange]):
        ret = []
        for item in value:
            ret.append(str(item))
        return ret

class AppsModel(BaseCamelModel):
    """
    List of valid apps in the network.
    """
    
    network: str = None
    """
    Network name.
    """
    valid_apps: List[InterlockAppTraitsModel] = Field(default_factory=list)
    """
    Currently valid apps for this network.
    """
    