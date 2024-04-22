from typing import Dict, List, Optional, Self
from pydantic import Field, field_serializer, field_validator
import datetime

from .base import BaseCamelModel
from ..utils.range import LimitedRange
from ..enum import DataFieldCast

class DataFieldEnumeration(BaseCamelModel):
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
    enumeration: Optional[str] = None
    """
    A string containing all enumerations concatenated in the format "#<number>|<name>|<description>|".
    """
    enumeration_as_flags: Optional[bool] = None
    """
    If `True`, the enumerations can be combined using bitwise-or. If `False`, only one value can be used.
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
    app_version: str
    data_models: List[DataModel]
    description: str
    id: int = 0
    name: str
    publisher_id: str
    publisher_name: str
    reserved_il_tag_ids: List[LimitedRange] = Field(alias='reservedILTagIds')
    start: datetime.datetime
    version: int = 0

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
    
    network: Optional[str] = None
    """
    Network name.
    """
    valid_apps: List[InterlockAppTraitsModel] = Field(default_factory=list)
    """
    Currently valid apps for this network.
    """
    